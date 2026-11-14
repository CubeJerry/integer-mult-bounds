#!/usr/bin/env python3
"""Reproduce all four standalone source words and their exact receipts."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(out):
    out=out.resolve()
    if out==HERE or HERE in out.parents:raise ValueError('external output required')
    out.mkdir(parents=True,exist_ok=True)
    for script,args in(('build.py',['--output',str(out)]),('price.py',['--output',str(out/'PRICE.json')])):
        r=subprocess.run([sys.executable,'-I','-B',str(HERE/script)]+args,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
    names=['RESULT.json','PRICE.json']+[f'{v}/{n}'for v in('forward-XY','forward-UV','inverse-XY','inverse-UV')for n in('WORD.json.gz','RESULT.json')]
    for n in names:
        if sha(out/n)!=sha(HERE/'output'/n):raise ValueError('artifact mismatch '+n)
    r={'status':'PASS_FOUR_PLANE_AUTHOR_REPRODUCTION','outputs':{n:sha(out/n)for n in names},'new_kappa':False}
    (out/'REPRODUCTION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
