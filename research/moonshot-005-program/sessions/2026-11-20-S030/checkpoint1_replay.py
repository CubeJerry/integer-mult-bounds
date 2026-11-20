#!/usr/bin/env python3
"""Reproduce the first S030 source and significant-price receipts."""
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
        ('source-author', 'bit-rs-source-fibre-census/author/check.py', 'CENSUS.json', 'bit-rs-source-fibre-census/author/output/CENSUS.json', True, True),
        ('source-review', 'bit-rs-source-fibre-census/review-large-kappa/check.py', 'RESULT.json', 'bit-rs-source-fibre-census/review-large-kappa/RESULT.json', True, False),
        ('price-author', 'kappa-significant-gain-screen/verify.py', 'RESULT.json', 'kappa-significant-gain-screen/RESULT.json', False, False),
        ('price-review', 'kappa-significant-gain-screen/root-review/check.py', 'RESULT.json', 'kappa-significant-gain-screen/root-review/output/RESULT.json', False, False),
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
        if name == 'source-author':
            for value in (actual, retained):
                value.pop('elapsed', None)
            normalized = ['elapsed wall-clock runtime only']
        if actual != retained:
            raise ValueError(name+' substantive receipt differs')
        return {'name': name, 'script': script, 'script_sha256': sha256((base/script).read_bytes()).hexdigest(),
                'expected': expected, 'expected_sha256': sha256(expected_bytes).hexdigest(),
                'matched': True, 'normalized_metadata': normalized, 'optimized': optimized}
    with ThreadPoolExecutor(max_workers=max(1, min(args.jobs, 4))) as pool:
        receipts = list(pool.map(run, jobs))
    result = {'status': 'PASS_S030_CHECKPOINT1_REPRODUCTION',
              'parent_baseline': 'dc063045868f2072e0be1ef9f3fbb4ca3d43c8f2',
              'jobs': receipts, 'independent_review': 'Separate proof/code reviews in the two admissions; these executions are reproduction, not additional independent reviews.',
              'new_complete_kappa': False}
    (args.out/'VALIDATION.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'], len(receipts), flush=True)


if __name__ == '__main__':
    main()
