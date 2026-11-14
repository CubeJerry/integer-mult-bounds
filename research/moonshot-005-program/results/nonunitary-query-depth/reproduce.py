#!/usr/bin/env python3
"""Relocation-safe replay of the frozen independent review."""
import argparse,hashlib,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve();out.parent.mkdir(parents=True,exist_ok=True)
cmd=[sys.executable,str(HERE/'review-c'/'check.py')]
if True:cmd+=['--author',str(HERE/'author')]
cmd+=['--output',str(out)]
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';subprocess.run(cmd,check=True,env=env)
if hashlib.sha256(out.read_bytes()).hexdigest()!='f2ae142c217fcafc1d0c4310d06878d65474f212516b1f9279f618b93cda7840':raise ValueError('independent receipt changed')
print('PASS_RELOCATED_BYTE_IDENTICAL_REVIEW')
