#!/usr/bin/env python3
"""Rebuild actual converted natives, fresh sources and their complete prices."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(command):
    r=subprocess.run(command,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
def main(args):
    here=Path(__file__).resolve().parent;out=args.output.resolve()
    if out==here or here in out.parents:raise ValueError('reproduction output must be outside frozen author package')
    sources=json.loads((here/'SOURCES.json').read_text());paths={};pins={}
    for name,item in sources['runtime_dependencies'].items():
        path=here/item['local_path']if'local_path'in item else args.repo/item['repo_path']
        if sha(path)!=item['sha256']:raise ValueError('dependency pin '+name)
        paths[name]=path;pins[name]=item['sha256']
    out.mkdir(parents=True,exist_ok=True);prefix=[sys.executable,'-I','-B']
    for variant in('orthogonal','allhosted'):
        target=out/variant
        run(prefix+[str(here/'build.py'),'--native',str(paths['native']),'--caller',str(paths['caller']),
             '--engine',str(paths['complete_engine']),'--full',str(paths['full_receipt']),
             '--variant',variant,'--output',str(target)])
        run(prefix+[str(here/'check_adapters.py'),'--native',str(paths['native']),'--word',str(target/'WORD.json.gz'),
             '--variant',variant,'--output',str(target/'ADAPTERS.json')])
        run(prefix+[str(here/'check_maps.py'),'--parent',str(paths['native']),'--word',str(target/'WORD.json.gz'),
             '--kind','complete','--engines',str(paths['clifford_engine'].parent),'--output',str(target/'PHASES.json')])
    for variant in('gram','parity'):
        target=out/('allhosted-'+variant)
        run(prefix+[str(here/'build_partial.py'),'--native',str(out/'allhosted'/'WORD.json.gz'),
             '--seed',str(paths['seed']),'--engine',str(paths['replay_engine']),'--codec',str(paths['codec']),
             '--variant',variant,'--output',str(target)])
        run(prefix+[str(here/'check_maps.py'),'--parent',str(paths['seed']),'--word',str(target/'WORD.json.gz'),
             '--kind','partial','--engines',str(paths['clifford_engine'].parent),'--output',str(target/'PHASES.json')])
    run(prefix+[str(here/'price.py'),'--full',str(paths['full_receipt']),'--caller',str(paths['caller']),
         '--engine',str(paths['interval_engine']),'--results',str(out),'--output',str(out/'PRICE.json')])
    names=['PRICE.json']+[f'{v}/{n}'for v in('orthogonal','allhosted')for n in('WORD.json.gz','CALLER.json','RESULT.json','ADAPTERS.json','PHASES.json')]
    names+=[f'allhosted-{v}/{n}'for v in('gram','parity')for n in('WORD.json.gz','RESULT.json','PHASES.json')]
    outputs={}
    for name in names:
        fresh=sha(out/name)
        if fresh!=sha(here/'output'/name):raise ValueError('frozen output mismatch '+name)
        outputs[name]=fresh
    receipt={'status':'PASS_AUTHOR_ALLHOSTED_INTERFACE_REPRODUCTION','source_pins':pins,'output_sha256':outputs,
             'scope':'Author exact reproduction through retained engines. Independent review separate; no new kappa.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'source_pin_count':len(pins),'output_file_count':len(outputs)},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
