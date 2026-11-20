#!/usr/bin/env python3
"""Reproduce the second S030 source, propagation and complex-cut receipts."""
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
    args = cli.parse_args()
    repo = args.repo.resolve()
    base = repo/'research/moonshot-005-program/results'
    args.out.mkdir(parents=True, exist_ok=True)
    jobs = [
        ('forty-source-review', 'bit-coupled-native-forty-h-source/root-review/check.py', 'RESULT.json', 'bit-coupled-native-forty-h-source/root-review/output/RESULT.json', True, False),
        ('all111-source-review', 'bit-coupled-native-forty-h-source/review-all-donors-b/check.py', 'RESULT.json', 'bit-coupled-native-forty-h-source/review-all-donors-b/RESULT.json', True, False),
        ('single-anchor-author', 'bit-single-rs-anchor-obstruction/author/check.py', 'RESULT.json', 'bit-single-rs-anchor-obstruction/author/output/RESULT.json', True, True),
        ('single-anchor-review', 'bit-single-rs-anchor-obstruction/review-b/check.py', 'RESULT.json', 'bit-single-rs-anchor-obstruction/review-b/RESULT.json', True, False),
        ('static-cut-review', 'complex-native-static-route-cut/review-b/check.py', 'RESULT.json', 'complex-native-static-route-cut/review-b/RESULT.json', True, False),
        ('static-price-review', 'complex-native-static-route-cut/root-price/check.py', 'RESULT.json', 'complex-native-static-route-cut/root-price/output/RESULT.json', True, False),
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
        process = subprocess.run(command, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (args.out/(name+'.log')).write_text(process.stdout)
        if process.returncode:
            raise RuntimeError(name+' failed: '+process.stdout[-3000:])
        actual_bytes, expected_bytes = (destination/output).read_bytes(), (base/expected).read_bytes()
        actual, retained = json.loads(actual_bytes), json.loads(expected_bytes)
        normalized = []
        if name == 'static-cut-review':
            for value in (actual, retained):
                value.pop('seconds', None)
            normalized = ['elapsed wall-clock runtime only']
        if actual != retained:
            raise ValueError(name+' substantive receipt differs')
        return {'name': name, 'script': script, 'script_sha256': sha256((base/script).read_bytes()).hexdigest(),
                'expected': expected, 'expected_sha256': sha256(expected_bytes).hexdigest(),
                'matched': True, 'normalized_metadata': normalized, 'optimized': optimized}
    with ThreadPoolExecutor(max_workers=max(1, min(args.jobs, 4))) as pool:
        receipts = list(pool.map(run, jobs))
    result = {'status': 'PASS_S030_CHECKPOINT2_REPRODUCTION',
              'parent_baseline': 'c09b211672fb9349db98bcb69ac234be3cb6ae9b',
              'jobs': receipts, 'independent_review': 'Separate proof/code reviews in the three admissions; these executions are reproduction, not additional independent reviews.',
              'new_complete_kappa': False}
    (args.out/'VALIDATION.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'], len(receipts), flush=True)


if __name__ == '__main__':
    main()
