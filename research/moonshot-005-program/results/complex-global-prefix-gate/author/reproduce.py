#!/usr/bin/env python3
"""Reproduce finite source witnesses and the exact scoped movement invoice."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main(args):
    here=Path(__file__).resolve().parent
    sources=json.loads((here/'SOURCES.json').read_text())
    checked={}
    for name,item in sources['runtime_dependencies'].items():
        path=(here/item['local_path']) if 'local_path' in item else (args.repo/item['repo_path'])
        if sha(path)!=item['sha256']:raise ValueError('dependency pin: '+name)
        checked[name]=item['sha256']
    args.output.mkdir(parents=True,exist_ok=True)
    commands=[
        [sys.executable,'-I','-B',str(here/'check_geometry.py'),'--native',str(here/'dependencies/native.json.gz'),'--output',str(args.output)],
        [sys.executable,'-I','-B',str(here/'price.py'),'--full',str(here/'dependencies/FULL-RESULT.json'),'--engine',str(here/'dependencies/interval.py'),'--output',str(args.output/'PRICE.json')]]
    for command in commands:subprocess.run(command,check=True,capture_output=True,text=True)
    verified={}
    for name in ('GEOMETRY.json.gz','GEOMETRY-RECEIPT.json','PRICE.json'):
        fresh=sha(args.output/name);old=sha(here/'output'/name)
        if fresh!=old:raise ValueError('frozen output mismatch: '+name)
        verified[name]=fresh
    receipt={'status':'PASS_AUTHOR_REPRODUCTION','source_pins':checked,'output_hashes':verified,
             'scope':'Repeated exact author checks; independent review remains separate. No physical word or new kappa.'}
    (args.output/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
