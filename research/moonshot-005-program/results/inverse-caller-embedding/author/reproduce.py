#!/usr/bin/env python3
"""Rebuild all bridge certificates and both actual hybrid source words."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
def main(out):
    here=Path(__file__).resolve().parent;out=out.resolve()
    if out==here or here in out.parents:raise ValueError('external output required')
    out.mkdir(parents=True,exist_ok=True);prefix=[sys.executable,'-I','-B']
    run(prefix+[str(here/'check.py'),'--output',str(out/'ROUTES.json')])
    run(prefix+[str(here/'check_boundaries.py'),'--output',str(out/'BOUNDARIES.json')])
    run(prefix+[str(here/'build_hybrid.py'),'--output',str(out)])
    outputs={};names=['ROUTES.json','BOUNDARIES.json','HYBRIDS.json']
    names += [f'{v}/{name}'for v in('inverse-XY','inverse-UV')for name in('WORD.json.gz','RESULT.json')]
    for name in names:
        if sha(out/name)!=sha(here/'output'/name):raise ValueError('artifact mismatch '+name)
        outputs[name]=sha(out/name)
    r={'status':'PASS_MIXED_ORIENTATION_BRIDGE_REPRODUCTION','outputs':outputs,'source_pins':json.loads((here/'SOURCES.json').read_text())['pins'],
      'scope':'Author deterministic reproduction. Independent review, full mixed caller and complete kappa status remain separate.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
