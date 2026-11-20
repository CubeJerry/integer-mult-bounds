"""Replay the general native floor, sharp nonlinear gap, and two target tariffs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(exist_ok=True,parents=True)
    R=repo/'research/moonshot-005-program/results';P=R/'bit-native-petersen-converse';N=R/'bit-nonlinear-separable-native-minimum';F=R/'bit-covariant-rebalanced-cutoffs';G=R/'bit-odd-native-sign-evaluations'
    layout=R/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';w=P/'author/output/WITNESS.json'
    charts=N/'sharp/output/THREE-COLUMNS.json.gz';detours=N/'sharp-review/output/TRIPLE-DETOURS.json.gz'
    (out/'sharp').mkdir(exist_ok=True);shutil.copyfile(charts,out/'sharp/THREE-COLUMNS.json.gz')
    jobs=[('floor',P/'author/check.py',['--layout',layout,'--witness',w],P/'author/output/RESULT.json'),
          ('floor-review',P/'review/review.py',['--repo',repo,'--witness',w],P/'review/output/RESULT.json'),
          ('additive',N/'author/check.py',['--repo',repo],N/'author/output/RESULT.json'),
          ('detours',N/'detours/check.py',['--repo',repo],N/'detours/output/RESULT.json'),
          ('sharp',N/'sharp/triples.py',['--layout',layout],N/'sharp/output/TRIPLE-RESULT.json'),
          ('sharp-review',N/'sharp-review/check.py',['--repo',repo,'--charts',charts,'--detours',detours],N/'sharp-review/output/RESULT.json'),
          ('finite',F/'author/check.py',['--repo',repo],F/'author/output/RESULT.json'),
          ('finite-review',F/'review/verify.py',['--repo',repo],F/'review/output/RESULT.json')]
    def run(job):
        key,script,flags,reference=job
        subprocess.run([sys.executable,'-B',script,*flags,'--out',out/key],check=True,stdout=subprocess.DEVNULL)
        data=(out/key/reference.name).read_bytes()
        if data!=reference.read_bytes():raise ValueError('replay mismatch '+key)
        return key,sha256(data).hexdigest()
    with ThreadPoolExecutor(max_workers=3) as pool:result=dict(pool.map(run,jobs))
    (out/'VALIDATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
