#!/usr/bin/env python3
"""Rebuild the literal codec, exact reduction and three-stage interface."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(out):
    out=out.resolve()
    if out==HERE or HERE in out.parents:raise ValueError('external output required')
    out.mkdir(parents=True,exist_ok=True);codec=out/'R0-CODEC.json'
    commands=[('codec.py',['--output',str(codec)]),('check.py',['--output',str(out/'RESULT.json'),'--codec',str(codec)]),('routes.py',['--output',str(out),'--codec',str(codec)])]
    for name,args in commands:
        r=subprocess.run([sys.executable,'-I','-B',str(HERE/name)]+args,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
    names=['R0-CODEC.json','RESULT.json','ROUTES3.json','INTERFACE-PROGRAM.json']
    for n in names:
        if sha(out/n)!=sha(HERE/n):raise ValueError('artifact mismatch '+n)
    r={'status':'PASS_THREE_HALF_AUTHOR_REPRODUCTION','files':{n:sha(out/n)for n in names},'new_kappa':False}
    (out/'REPRODUCTION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
