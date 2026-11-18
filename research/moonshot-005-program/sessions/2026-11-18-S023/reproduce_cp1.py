#!/usr/bin/env python3
"""Reproduce the three S023 checkpoint-one proof packages from pinned inputs."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pg = repo / 'research/moonshot-005-program'
    results = pg / 'results'
    native = pg / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    layout = results / 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    factor = results / 'bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json'
    gauge = results / 'bit-native-cycle-and-inlet-gates'
    quotient = results / 'bit-balanced-quotient-source-compiler'
    asymmetry = results / 'bit-native-plane-asymmetry'
    checks = []

    def run(name, script, argv, pairs):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        proc = subprocess.run([sys.executable, '-B', str(script), *map(str, argv)],
                              cwd=repo, capture_output=True, env=env)
        if proc.returncode:
            raise RuntimeError(name + ': ' + proc.stderr.decode())
        records = []
        for frozen, fresh in pairs:
            expected, actual = frozen.read_bytes(), fresh.read_bytes()
            if frozen.suffix == '.gz':
                expected = gzip.decompress(expected)
            if fresh.suffix == '.gz':
                actual = gzip.decompress(actual)
            if expected != actual:
                raise ValueError(name + ': output differs: ' + str(frozen))
            records.append({'path': str(frozen.relative_to(pg)),
                            'sha256_uncompressed': hashlib.sha256(actual).hexdigest()})
        checks.append({'check': name, 'outputs': records})
        print(name, 'PASS', flush=True)

    ga = out / 'gauge-author'
    run('gauge-author', gauge/'author/check.py',
        ['--native',native,'--layout',layout,'--factor',factor,'--out',ga],
        [(gauge/'author/output'/f,ga/f) for f in ['RESULT.json','SCHEME.json.gz']])
    gr = out / 'gauge-review.json'
    run('gauge-independent-review', gauge/'review/check.py', ['--repo',repo,'--out',gr],
        [(gauge/'review/output/RESULT.json',gr)])
    qa = out / 'quotient-author.json'
    run('quotient-author', quotient/'author/check.py',
        ['--layout',layout,'--factor',factor,'--out',qa],
        [(quotient/'author/output/RESULT.json.gz',qa)])
    qr = out / 'quotient-review'
    run('quotient-independent-review', quotient/'review/check.py',
        ['--layout',layout,'--author-result',qa,'--proof',quotient/'author/PROOF.md','--out',qr],
        [(quotient/'review/output/RESULT.json',qr/'RESULT.json')])
    aa = out / 'asymmetry-author'
    run('asymmetry-author', asymmetry/'author/check.py', ['--repo',repo,'--out',aa],
        [(asymmetry/'author/output'/f,aa/f) for f in ['RESULT.json','WITNESSES.json.gz']])
    ar = out / 'asymmetry-review'
    run('asymmetry-independent-review', asymmetry/'review/check.py',
        ['--layout',layout,'--witnesses',aa/'WITNESSES.json.gz',
         '--proof',asymmetry/'author/PROOF.md','--out',ar],
        [(asymmetry/'review/output/RESULT.json',ar/'RESULT.json')])
    (out/'VALIDATION.json').write_text(json.dumps({
        'status':'PASS', 'baseline_sha':'8cf982065bccdd62de2856b16635a6ee06dadb0c',
        'scope':'Six focused executions; exact fresh outputs plus independent mathematical reviews. No full legacy replay or new kappa.',
        'checks':checks}, indent=2)+'\n')


if __name__ == '__main__':
    main()
