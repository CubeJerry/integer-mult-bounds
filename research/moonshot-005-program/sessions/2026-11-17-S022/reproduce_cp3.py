#!/usr/bin/env python3
"""Reproduce both author and independent checks for the weighted inlet theorems."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args = cli.parse_args()
    repo,out = args.repo.resolve(),args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    p = repo / 'research/moonshot-005-program'
    linear = p / 'results/bit-minimum-transcript-inlets'
    nonlinear = p / 'results/bit-nonlinear-weighted-inlets'
    report = []
    for name, base, filename, extra in [
        ('linear-source',linear/'author','CERTIFICATE.json',[]),
        ('linear-independent',linear/'review','RESULT.json',[]),
        ('nonlinear-source',nonlinear/'author','RESULT.json',[]),
        ('nonlinear-independent',nonlinear/'review','CERTIFICATE.json',['--weights',nonlinear/'author/WEIGHTS.json'])]:
        dest = out / (name+'.json')
        subprocess.run([sys.executable,'-B',str(base/'check.py'),'--repo',str(repo),'--out',str(dest),*map(str,extra)],check=True)
        actual,expected = dest.read_bytes(),(base/filename).read_bytes()
        if actual != expected:
            raise ValueError(f'scientific bytes differ for {name}')
        report.append({'check':name,'source_sha256':hashlib.sha256((base/'check.py').read_bytes()).hexdigest(),
                       'certificate':str((base/filename).relative_to(p)),'verified_sha256':hashlib.sha256(actual).hexdigest()})
    (out/'VALIDATION.json').write_text(json.dumps({'status':'PASS','byte_equal':True,'checks':report},indent=2)+'\n')


if __name__=='__main__':
    main()
