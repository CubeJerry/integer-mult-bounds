#!/usr/bin/env python3
"""Relocation-safe frozen independent-review replay."""
import argparse,hashlib,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve();out.parent.mkdir(parents=True,exist_ok=True)
cmd=[sys.executable,str(HERE/'review-c'/'check.py'),'--author',str(HERE/'author'),'--output',str(out)]
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';subprocess.run(cmd,check=True,env=env)
if hashlib.sha256(out.read_bytes()).hexdigest()!='978ee023a6c5519b602fa6ed75f1d3cb0696581f825d31a99dce8d37b3e59368':raise ValueError('independent receipt changed')
print('PASS_RELOCATED_BYTE_IDENTICAL_REVIEW')
