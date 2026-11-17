#!/usr/bin/env python3
"""Focused S021 checkpoint1 source/field-compiler reproduction."""
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
    args = p.parse_args(); repo = args.repo.resolve(); out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    base = repo / 'research/moonshot-005-program'
    old = base / 'sessions/2026-11-17-S020'
    new = base / 'results/bit-three-copy-field-compiler'
    tasks = [
        ('pair-source', [old / 'checkpoint10-evidence/C/four-arrival-frame-review/check.py',
                        '--native', base / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json',
                        '--word', old / 'checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json',
                        '--parent', old / 'checkpoint5-evidence/A/full-half-reservoir/WORD.json',
                        '--arithmetic', old / 'checkpoint2-evidence/C/four-plane-review/check.py',
                        '--interpreter', old / 'checkpoint8-evidence/C/owned-upward-half-rebase/build.py',
                        '--out', out / 'pair-source']),
        ('three-copy-author', [new / 'author/build.py', '--repo', repo, '--out', out / 'author']),
        ('three-copy-review', [new / 'review/check.py', '--repo', repo,
                               '--word', out / 'author/WORD.json', '--out', out / 'review']),
    ]
    receipt = {'status': 'PASS', 'python': platform.python_version(), 'commands': [], 'outputs': []}
    for label, arguments in tasks:
        command = [sys.executable, '-B'] + list(map(str, arguments))
        run = subprocess.run(command, cwd=repo, text=True, capture_output=True)
        (out / (label + '.log')).write_text(run.stdout + run.stderr)
        if run.returncode:
            raise RuntimeError(label + ' failed: ' + run.stderr[-2000:])
        receipt['commands'].append({'label': label, 'exit_code': run.returncode})
    comparisons = [
        (out / 'pair-source/CERTIFICATE.json', old / 'checkpoint10-evidence/C/four-arrival-frame-review/output/CERTIFICATE.json'),
        (out / 'pair-source/INDEPENDENT-CUT.json', old / 'checkpoint10-evidence/C/four-arrival-frame-review/output/INDEPENDENT-CUT.json'),
    ]
    comparisons += [(out / 'author' / f, new / 'author/output' / f)
                    for f in ('WORD.json', 'RESULT.json', 'CUT-INVENTORY.json', 'COMPILER.json')]
    comparisons += [(out / 'review' / f, new / 'review/output' / f)
                    for f in ('CERTIFICATE.json', 'INDEPENDENT-CUT.json')]
    for generated, frozen in comparisons:
        data = generated.read_bytes()
        reference = frozen.read_bytes()
        if json.loads(data) != json.loads(reference):
            raise ValueError('Scientific output differs: ' + str(generated))
        canonical = json.dumps(json.loads(data), sort_keys=True, separators=(',', ':')).encode()
        receipt['outputs'].append({'path': str(frozen.relative_to(repo)),
                                   'frozen_sha256': sha256(reference).hexdigest(),
                                   'generated_sha256': sha256(data).hexdigest(),
                                   'canonical_json_sha256': sha256(canonical).hexdigest(),
                                   'all_scientific_fields_equal': True,
                                   'byte_equal': data == reference})
    (out / 'VALIDATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': 'PASS_S021_CP1', 'checks': len(tasks), 'exact_outputs': len(comparisons)}))


if __name__ == '__main__':
    main()
