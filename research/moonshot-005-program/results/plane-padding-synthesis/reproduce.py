#!/usr/bin/env python3
"""Relocation-safe replay of the frozen independent review."""
import argparse,hashlib,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve();out.parent.mkdir(parents=True,exist_ok=True)
cmd=[sys.executable,str(HERE/'review-root'/'check.py')]
if True:cmd+=['--author',str(HERE/'author')]
cmd+=['--output',str(out)]
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';subprocess.run(cmd,check=True,env=env)
if hashlib.sha256(out.read_bytes()).hexdigest()!='99145c72678da5367eba58761dd7f1c22b275f8069a15535857e2739a5a7ed8e':raise ValueError('independent receipt changed')
print('PASS_RELOCATED_BYTE_IDENTICAL_REVIEW')
