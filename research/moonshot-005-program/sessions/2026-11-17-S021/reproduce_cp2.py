#!/usr/bin/env python3
"""Focused reproduction of the four S021 checkpoint2 admissions."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[4])
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    results = repo / 'research/moonshot-005-program/results'
    f4 = results / 'bit-two-copy-field-compiler'
    cuts = results / 'bit-separated-private-transcript'
    mixed = results / 'complex-mixed-all-profile-gate'
    terminal = results / 'bit-native-repair-terminal-gate'
    f8 = results / 'bit-three-copy-field-compiler/author/output/WORD.json'
    jobs = [
        ('f4-author', f4/'author', 'build.py', ['--repo', repo],
         ['WORD.json', 'RESULT.json', 'CUT-INVENTORY.json', 'COMPILER.json']),
        ('cuts-author', cuts/'author', 'check.py', ['--repo', repo, '--triple-word', f8],
         ['CERTIFICATE.json', 'FRAME-CERTIFICATE.json', 'SINGLE-CUT.json', 'TRIPLE-CUT.json']),
        ('f4-physical', f4/'physical-review', 'check.py',
         ['--repo', repo, '--word', out/'f4-author/WORD.json', '--theorem-checker', cuts/'author/check.py'],
         ['CERTIFICATE.json', 'INDEPENDENT-CUT.json']),
        ('f4-algebra', f4/'review', 'check.py',
         ['--repo', repo, '--word', out/'f4-author/WORD.json', '--cut', out/'f4-physical/INDEPENDENT-CUT.json'],
         ['CERTIFICATE.json']),
        ('mixed-author', mixed/'author', 'check.py', ['--repo', repo],
         ['RESULT.json', 'WITNESSES.json', 'MANIFEST.json']),
        ('mixed-review', mixed/'review', 'check.py', ['--author', mixed/'author'],
         ['RESULT.json', 'SOURCE-MATRICES.json']),
        ('terminal-author', terminal/'author', 'check.py', ['--repo', repo],
         ['RESULT.json', 'INVERSE-CERTIFICATE.json']),
        ('terminal-review', terminal/'review', 'check.py', ['--repo', repo, '--author', terminal/'author'],
         ['CERTIFICATE.json']),
    ]
    receipt = {'status': 'PASS', 'python': platform.python_version(), 'commands': [], 'outputs': []}
    for label, package, script, arguments, files in jobs:
        command = [sys.executable, '-B', str(package/script)] + list(map(str, arguments)) + ['--out', str(out/label)]
        run = subprocess.run(command, cwd=repo, text=True, capture_output=True)
        (out/(label+'.log')).write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError(label+' failed: '+run.stderr[-3000:])
        receipt['commands'].append({'label': label, 'exit_code': run.returncode,
                                    'checker_sha256': sha256((package/script).read_bytes()).hexdigest()})
        for filename in files:
            frozen = package/'output'/filename
            generated = out/label/filename
            old, new = frozen.read_bytes(), generated.read_bytes()
            if json.loads(old) != json.loads(new):
                raise ValueError('Scientific output differs: '+str(frozen))
            canonical = json.dumps(json.loads(new), sort_keys=True, separators=(',', ':')).encode()
            receipt['outputs'].append({
                'path': str(frozen.relative_to(repo)),
                'frozen_sha256': sha256(old).hexdigest(),
                'generated_sha256': sha256(new).hexdigest(),
                'canonical_json_sha256': sha256(canonical).hexdigest(),
                'all_scientific_fields_equal': True, 'byte_equal': old == new})
        print(label+' PASS', flush=True)
    (out/'VALIDATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'status': 'PASS_S021_CP2', 'checks': len(jobs), 'exact_outputs': len(receipt['outputs'])}))


if __name__ == '__main__':
    main()
