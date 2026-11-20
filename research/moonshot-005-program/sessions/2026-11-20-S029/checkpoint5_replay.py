"""Reproduce the global native rank result, its two reviews and certificate hashes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    repo = args.repo.resolve()
    out = args.out.resolve()
    pkg = repo / 'research/moonshot-005-program/results/bit-global-native-rank-rigidity'
    inputs = out / 'input'
    inputs.mkdir(parents=True, exist_ok=True)
    wit = json.loads(gzip.decompress((pkg / 'author/output/WITNESS.json.gz').read_bytes()))
    (inputs / 'CLOSURE.json').write_bytes(gzip.decompress((pkg / 'review/input/CLOSURE.json.gz').read_bytes()))
    compact = {'separators': (',', ':')}
    data = [
        ('WEIGHTED', {k: wit[k] for k in ('tree','closure')}, compact),
        ('DIAGONALS', {str(i): wit['diagonal_pivots'][str(i)] for i in range(111)}, compact),
        ('ODD', {k: wit['odd_minor'][k] for k in ('rows','cols','det','weight')}, {}),
    ]
    for name, value, options in data:
        (inputs / (name+'.json')).write_text(json.dumps(value, **options))
    jobs = [
        ('author', 'author/check.py', [], 'RESULT.json'),
        ('unweighted', 'review/check.py', ['--closure', inputs/'CLOSURE.json'], 'RESULT.json'),
        ('weighted', 'review/weighted.py', ['--certificates', inputs], 'WEIGHTED-REVIEW.json'),
    ]
    def replay(job):
        name, script, flags, filename = job
        subprocess.run([sys.executable,'-B',pkg/script,'--repo',repo,'--out',out/name,*flags], check=True, stdout=subprocess.DEVNULL)
        result = (out/name/filename).read_bytes()
        reference = (pkg/Path(script).parent/'output'/filename).read_bytes()
        if result != reference:
            raise ValueError('scientific output changed: '+name)
        return name, sha256(result).hexdigest()
    with ThreadPoolExecutor(max_workers=3) as pool:
        receipt = dict(pool.map(replay,jobs))
    (out/'VALIDATION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
