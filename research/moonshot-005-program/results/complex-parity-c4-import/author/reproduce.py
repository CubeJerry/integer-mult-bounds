#!/usr/bin/env python3
"""Rebuild the C4 base and actual coupled-import word and their exact bills."""
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
        if sha(path)!=item['sha256']:raise ValueError('dependency pin: '+name)
        paths[name]=path;pins[name]=item['sha256']
    out.mkdir(parents=True,exist_ok=True);prefix=[sys.executable,'-I','-B']
    for variant in('base','imported'):
        target=out/variant
        run(prefix+[str(here/'build.py'),'--native',str(paths['native']),'--seed',str(paths['seed']),
                    '--parity',str(paths['parity_word']),'--engine',str(paths['replay_engine']),
                    '--codec',str(paths['codec_utility']),'--variant',variant,'--output',str(target)])
        run(prefix+[str(here/'check_maps.py'),'--seed',str(paths['seed']),'--word',str(target/'WORD.json.gz'),
                    '--engines',str(paths['clifford_engine'].parent),'--output',str(target/'PHASES.json')])
    run(prefix+[str(here/'price.py'),'--full',str(paths['full_caller']),'--engine',str(paths['interval_engine']),
                '--results',str(out),'--output',str(out/'PRICE.json')])
    names=['PRICE.json']+[f'{v}/{n}'for v in('base','imported')for n in('WORD.json.gz','RESULT.json','PHASES.json')];outputs={}
    for name in names:
        fresh=sha(out/name)
        if fresh!=sha(here/'output'/name):raise ValueError('frozen output mismatch: '+name)
        outputs[name]=fresh
    receipt={'status':'PASS_AUTHOR_C4_PARITY_AND_REAL_IMPORT_REPRODUCTION','source_pins':pins,'output_sha256':outputs,
             'scope':'Author reproduction through credited retained engines. Independent review separate; no new kappa.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'source_pin_count':len(pins),'output_file_count':len(outputs)},sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
