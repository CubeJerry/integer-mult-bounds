#!/usr/bin/env python3
"""Reproduce the third S030 connected-source, array-anchor and complete-source cut receipts."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True)
    cli.add_argument('--out', type=Path, required=True)
    cli.add_argument('--jobs', type=int, default=2)
    cli.add_argument('--collect-existing', action='store_true', help='Compare previously executed fresh root replay outputs; default executes each checker.')
    args = cli.parse_args()
    repo = args.repo.resolve()
    base = repo/'research/moonshot-005-program/results'
    args.out.mkdir(parents=True, exist_ok=True)
    jobs = [
        ('connected-source', 'bit-coupled-native-three-chain-source/review-b/check.py', 'RESULT.json', 'bit-coupled-native-three-chain-source/review-b/RESULT.json', True, False),
        ('hybrid-source', 'bit-coupled-native-three-chain-source/review-fibre-only-b/check.py', 'RESULT.json', 'bit-coupled-native-three-chain-source/review-fibre-only-b/RESULT.json', True, False),
        ('full-complex-source-cut', 'complex-native-source-cut/root-review/check.py', 'RESULT.json', 'complex-native-source-cut/root-review/RESULT.json', True, False),
        ('array-anchor-general', 'bit-array-anchor-degeneracy/review-b/check.py', 'RESULT.json', 'bit-array-anchor-degeneracy/review-b/RESULT.json', True, False),
        ('array-anchor-applications', 'bit-array-anchor-degeneracy/applications/review-b/check.py', 'RESULT.json', 'bit-array-anchor-degeneracy/applications/review-b/RESULT.json', True, False),
    ]
    def run(job):
        name, script, output, expected, needs_repo, optimized = job
        destination = args.out/name
        command = [sys.executable, '-B']
        if optimized:
            command += ['-O']
        command += [str(base/script), '--out', str(destination)]
        if needs_repo:
            command += ['--repo', str(repo)]
        if not args.collect_existing:
            process = subprocess.run(command, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (args.out/(name+'.log')).write_text(process.stdout)
            if process.returncode:
                raise RuntimeError(name+' failed: '+process.stdout[-3000:])
        actual_bytes, expected_bytes = (destination/output).read_bytes(), (base/expected).read_bytes()
        actual, retained = json.loads(actual_bytes), json.loads(expected_bytes)
        normalized = []
        if actual != retained:
            raise ValueError(name+' substantive receipt differs')
        return {'name': name, 'script': script, 'script_sha256': sha256((base/script).read_bytes()).hexdigest(),
                'expected': expected, 'expected_sha256': sha256(expected_bytes).hexdigest(),
                'matched': True, 'normalized_metadata': normalized, 'optimized': optimized}
    with ThreadPoolExecutor(max_workers=max(1, min(args.jobs, 4))) as pool:
        receipts = list(pool.map(run, jobs))
    result = {'status': 'PASS_S030_CHECKPOINT3_REPRODUCTION',
              'parent_baseline': 'ef071187ffe94f1469b6401c8d217c2c3c175557',
              'execution_mode': 'collected separate fresh S030 root executions' if args.collect_existing else 'executed by this replay',
              'jobs': receipts, 'independent_review': 'Separate proof/code reviews in the three admissions; these executions are reproduction, not additional independent reviews.',
              'new_complete_kappa': False}
    (args.out/'VALIDATION.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'], len(receipts), flush=True)


if __name__ == '__main__':
    main()
