#!/usr/bin/env python3
"""Exercise artifact rejection through the actual standalone CLIs.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
All mutations occur in private copies; this file never rewrites the package.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise RuntimeError(message)


def inventory(root):
    return {str(p.relative_to(root)): (p.stat().st_mode & 0o777,
                                      hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob('*') if p.is_file()}


def change_json(path, change):
    value = json.loads(path.read_text())
    change(value)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def mutate(root, case):
    if case == 'word':
        path = root / 'inputs/pr6144-WORD.json.gz'
        value = bytearray(path.read_bytes())
        value[len(value) // 2] ^= 1
        path.write_bytes(value)
    elif case == 'readme':
        with (root / 'inputs/pr6144-README.md').open('ab') as stream:
            stream.write(b'\nchanged source\n')
    elif case == 'repin':
        change_json(root / 'SOURCES.json',
                    lambda value: value['vendored_inputs'][0].update(commit='0' * 40))
    elif case == 'certificate':
        change_json(root / 'CERTIFICATE.json',
                    lambda value: value['minor'].update(determinant='0'))
    elif case == 'independent_receipt':
        change_json(root / 'INDEPENDENT.json',
                    lambda value: value.update(final_residual_rank=1))
    else:
        raise RuntimeError('unknown control')


def main():
    original = inventory(HERE)
    cases = [
        ('word', 'verify.py', 'immutable vendored input bytes'),
        ('readme', 'verify.py', 'immutable vendored input bytes'),
        ('repin', 'verify.py', 'source identity'),
        ('certificate', 'verify.py', 'complete certificate equality'),
        ('independent_receipt', 'independent.py', 'complete independent receipt mismatch'),
    ]
    for case, script, failure in cases:
        with tempfile.TemporaryDirectory(prefix='root2-packet-control-') as tmp:
            root = Path(tmp) / 'package'
            shutil.copytree(HERE, root)
            mutate(root, case)
            before = inventory(root)
            argv = [sys.executable, '-I', '-B']
            if sys.flags.optimize:
                argv.append('-O')
            argv.append(str(root / script))
            result = subprocess.run(argv, cwd=tmp, text=True, capture_output=True,
                                    timeout=120)
            require(result.returncode != 0, case + ' accepted a damaged artifact')
            require(failure in result.stderr, case + ' failed for the wrong reason: ' + result.stderr)
            require(inventory(root) == before, case + ' verifier changed files')
    require(inventory(HERE) == original, 'original package changed')
    print('PASS_ROOT2_PACKET_CUT_ARTIFACT_CONTROLS rejected=5 read_only=true')


if __name__ == '__main__':
    main()
