#!/usr/bin/env python3
"""Rebuild the three literal words, exact maps and complete signed invoices."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(command):
    result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stdout+'\n'+result.stderr)
def main(args):
    here=Path(__file__).resolve().parent;out=args.output.resolve()
    if out==here or here in out.parents:raise ValueError('reproduction output must be outside frozen package')
    source=json.loads((here/'SOURCES.json').read_text());paths={};pins={}
    for name,item in source['runtime_dependencies'].items():
        path=here/item['local_path']if'local_path'in item else args.repo/item['repo_path']
        if sha(path)!=item['sha256']:raise ValueError('dependency pin: '+name)
        paths[name]=path;pins[name]=item['sha256']
    out.mkdir(parents=True,exist_ok=True)
    prefix=[sys.executable,'-I','-B']
    for k in (2,4,8):
        target=out/('k'+str(k))
        run(prefix+[str(here/'build.py'),'--native',str(paths['native']),'--seed',str(paths['seed']),
                    '--engine',str(paths['replay_engine']),'--codec',str(paths['codec_utility']),
                    '--size',str(k),'--output',str(target)])
        run(prefix+[str(here/'check_maps.py'),'--seed',str(paths['seed']),'--word',str(target/'WORD.json.gz'),
                    '--engines',str(paths['clifford_engine'].parent),'--output',str(target/'PHASES.json')])
    run(prefix+[str(here/'price.py'),'--full',str(paths['full_caller']),'--engine',str(paths['interval_engine']),
                '--results',str(out),'--output',str(out/'PRICE.json')])
    outputs={}
    names=['PRICE.json']+[f'k{k}/{name}'for k in(2,4,8)for name in('WORD.json.gz','RESULT.json','PHASES.json')]
    for name in names:
        fresh=sha(out/name)
        if fresh!=sha(here/'output'/name):raise ValueError('frozen output mismatch: '+name)
        outputs[name]=fresh
    receipt={'status':'PASS_AUTHOR_PAIRED_CLIQUE_REPRODUCTION','source_pins':pins,'output_sha256':outputs,
             'scope':'Author reproduction using credited retained engines. Independent review is separate; no new kappa.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'source_pin_count':len(pins),'output_file_count':len(outputs)},sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
