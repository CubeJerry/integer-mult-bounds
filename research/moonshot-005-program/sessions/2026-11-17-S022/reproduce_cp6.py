#!/usr/bin/env python3
"""Reproduce the fixed-source surplus gates and the unrestricted quartic endpoint theorem."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--repo',required=True,type=Path);a.add_argument('--out',required=True,type=Path)
    args=a.parse_args();repo,out=args.repo.resolve(),args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    pg=repo/'research/moonshot-005-program';r=pg/'results';near=r/'bit-surplus-transcript-and-factor-gates';cx=r/'complex-unrestricted-quartic'
    engine=r/'complex-spectator-preserving-interface/author'
    coverage=r/'bit-nonlinear-weighted-inlets/review/CERTIFICATE.json'
    jobs=[
      (near/'surplus/check.py',['--repo',repo,'--coverage',coverage,'--out',out/'surplus.json'],near/'surplus/CERTIFICATE.json',out/'surplus.json'),
      (near/'factors/check.py',['--repo',repo],near/'factors/CERTIFICATE.json',None),
      (near/'review/check.py',['--repo',repo,'--out',out/'review.json'],near/'review/RESULT.json',out/'review.json'),
      (cx/'author/check.py',['--engine',engine,'--out',out/'quartic'],cx/'author/output/RESULT.json',out/'quartic/RESULT.json'),
      (cx/'review/quartic.py',['--proof',cx/'author/PROOF.md','--out',out/'quartic-review.json'],cx/'review/QUARTIC-RESULT.json',out/'quartic-review.json')]
    records=[]
    for path,argv,frozen,result in jobs:
        r=subprocess.run([sys.executable,'-B',str(path),*map(str,argv)],cwd=repo,capture_output=True,check=True)
        actual=r.stdout if result is None else result.read_bytes()
        if actual!=frozen.read_bytes():raise ValueError(f'Mismatch for {frozen}')
        records.append({'source':str(path.relative_to(pg)),'certificate':str(frozen.relative_to(pg)),'sha256':hashlib.sha256(actual).hexdigest()})
    (out/'VALIDATION.json').write_text(json.dumps({'status':'PASS','byte_equal':True,'checks':records},indent=2)+'\n')
    print('PASS five source and independent certificates')

if __name__=='__main__':
    main()
