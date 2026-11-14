#!/usr/bin/env python3
"""Reproduce all three448-input source words outside the frozen package."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(command):
    r=subprocess.run(command,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
def main(args):
    here=Path(__file__).resolve().parent;out=args.output.resolve()
    if out==here or here in out.parents:raise ValueError('output must be outside frozen author package')
    s=json.loads((here/'SOURCES.json').read_text());paths={};pins={}
    for key,item in s['runtime_dependencies'].items():
        path=here/item['local_path']if'local_path'in item else args.repo/item['repo_path']
        if sha(path)!=item['sha256']:raise ValueError('source pin '+key)
        paths[key]=path;pins[key]=item['sha256']
    for key,item in s['provenance_only'].items():
        if sha(here/item['local_path'])!=item['sha256']:raise ValueError('provenance pin '+key)
    prefix=[sys.executable,'-I','-B'];out.mkdir(parents=True,exist_ok=True)
    for variant in('R0','R1'):
        target=out/variant
        run(prefix+[str(here/'build.py'),'--native',str(paths['native']),'--seed',str(paths['seed']),
            '--engine',str(paths['replay']),'--codec',str(paths['codec']),'--dynamic',str(paths['dynamic_replay']),
            '--geometry',str(paths['geometry']),'--variant',variant,'--output',str(target)])
    run(prefix+[str(here/'minimal.py'),'--source',str(out/'R0/WORD.json.gz'),'--engine',str(paths['replay']),
        '--codec',str(paths['codec']),'--dynamic',str(paths['dynamic_replay']),'--output',str(out/'R0-minimal')])
    for variant in('R0','R0-minimal','R1'):
        run(prefix+[str(paths['map_checker']),'--parent',str(paths['seed']),'--word',str(out/variant/'WORD.json.gz'),
            '--kind','partial','--engines',str(paths['clifford'].parent),'--output',str(out/variant/'PHASES.json')])
    run(prefix+[str(here/'price.py'),'--engine',str(paths['interval']),'--results',str(out),'--output',str(out/'PRICE.json')])
    names=['PRICE.json']+[f'{v}/{n}'for v in('R0','R0-minimal','R1')for n in('WORD.json.gz','RESULT.json','PHASES.json')];outputs={}
    for name in names:
        fresh=sha(out/name)
        if fresh!=sha(here/'output'/name):raise ValueError('frozen artifact mismatch '+name)
        outputs[name]=fresh
    receipt={'status':'PASS_FULL112_SOURCE_REPRODUCTION','source_pins':pins,'outputs':outputs,
        'scope':'Author deterministic reproduction, separate from independent review. No physical caller admission or new kappa.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'source_pins':len(pins),'outputs':len(outputs)},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
