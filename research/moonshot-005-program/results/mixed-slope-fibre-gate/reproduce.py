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
if hashlib.sha256(out.read_bytes()).hexdigest()!='717b6164fed760bd8525bd53def17586ad453b7a5474cefd61bb3c75fe9918f6':raise ValueError('independent receipt changed')
print('PASS_RELOCATED_BYTE_IDENTICAL_REVIEW')
