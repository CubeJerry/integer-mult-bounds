#!/usr/bin/env python3
"""Reproduce both closed public-bank words and the literal open alternative."""
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
    prefix=[sys.executable,'-I','-B'];out.mkdir(parents=True,exist_ok=True)
    for variant in('retained','allhosted'):
        target=out/variant
        run(prefix+[str(here/'build.py'),'--native',str(paths[variant+'_native']),'--seed',str(paths['seed']),
            '--engine',str(paths['replay']),'--codec',str(paths['codec']),'--dynamic',str(paths['dynamic_replay']),
            '--variant',variant,'--output',str(target)])
        run(prefix+[str(paths['map_checker']),'--parent',str(paths['seed']),'--word',str(target/'WORD.json.gz'),
            '--kind','partial','--engines',str(paths['clifford'].parent),'--output',str(target/'PHASES.json')])
    run(prefix+[str(here/'preserve_open.py'),'--old',str(paths['old_relay']),'--native',str(paths['retained_native']),
        '--engine',str(paths['replay']),'--codec',str(paths['codec']),'--output',str(out/'open-retained')])
    run(prefix+[str(here/'price.py'),'--full',str(paths['full_receipt']),'--changed',str(paths['changed_price']),
        '--engine',str(paths['interval']),'--results',str(out),'--output',str(out/'PRICE.json')])
    names=['PRICE.json']+[f'{v}/{name}'for v in('retained','allhosted')for name in('WORD.json.gz','RESULT.json','PHASES.json')]
    names+=['open-retained/WORD.json.gz','open-retained/RESULT.json'];outputs={}
    for name in names:
        fresh=sha(out/name)
        if fresh!=sha(here/'output'/name):raise ValueError('frozen artifact mismatch '+name)
        outputs[name]=fresh
    receipt={'status':'PASS_PUBLIC_AND_OPEN_GRAM_RETENTION_REPRODUCTION','source_pins':pins,'outputs':outputs,
        'scope':'Author deterministic reproduction, separate from independent review. No new kappa.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'source_pins':len(pins),'outputs':len(outputs)},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
