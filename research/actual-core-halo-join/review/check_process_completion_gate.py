"""Adversarial checks of the retained physical process-completion gate.

This checks receipt acceptance, not a second physical or numerical replay.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.package.resolve()
    original = json.loads((source/'PHYSICAL-EXIT.json').read_text())
    if original.get('exit_code') != 0 or original.get('teardown_completed') is not True:
        raise ValueError('A completed baseline is required before testing rejection controls')
    cases = [
        ('missing-exit-record', None, 'observed successful exit after trailing teardown required'),
        ('nonzero-process-exit', {'exit_code': 1}, 'separate observed process-completion gate'),
        ('unfinished-teardown', {'teardown_completed': False}, 'separate observed process-completion gate'),
        ('changed-execution-log', {'bad_log': True}, 'process-completion record binds exact log'),
        ('different-reference', {'reference_sha256': '0'*64}, 'same completed source identity'),
    ]
    records = []
    with tempfile.TemporaryDirectory(prefix='core-halo-completion-gate-') as temporary:
        package = Path(temporary)/'research'/'actual-core-halo-join'
        shutil.copytree(source, package)
        completion_path = package/'PHYSICAL-EXIT.json'
        # A portable export may be read-only; mutate only this disposable copy.
        package.chmod(0o755)
        completion_path.chmod(0o644)
        for name, mutation, expected in cases:
            if mutation is None:
                completion_path.unlink(missing_ok=True)
            else:
                completion = deepcopy(original)
                if mutation.get('bad_log'):
                    completion['log']['sha256'] = '0'*64
                else:
                    completion.update(mutation)
                completion_path.write_text(json.dumps(completion)+'\n')
            for optimized in (False, True):
                argv = [sys.executable, '-I', '-B']
                if optimized:
                    argv.append('-O')
                argv.append(str(package/'replay.py'))
                result = subprocess.run(argv, cwd=package.parents[1], capture_output=True,
                                        text=True, timeout=10, check=False)
                if result.returncode == 0 or expected not in result.stderr:
                    raise ValueError('Expected completion rejection was not observed: '+name)
                if 'PASS ' in result.stdout:
                    raise ValueError('Completion rejection occurred after replay began: '+name)
                records.append(dict(control=name, optimization=int(optimized),
                                    exit_code=result.returncode, rejection=expected,
                                    no_replay_started=True))
    answer = dict(status='PASS_ADVERSARIAL_PROCESS_COMPLETION_GATE',
                  scope='Retained completion-record admission only; no physical replay.',
                  controls=records,
                  source_sha256={name:sha256((source/name).read_bytes()).hexdigest()
                                 for name in ('replay.py','PHYSICAL-EXIT.json','PHYSICAL-RESULT.json',
                                              'PHYSICAL-EXECUTION.log')})
    args.output.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    print(answer['status'])


if __name__ == '__main__':
    main()
