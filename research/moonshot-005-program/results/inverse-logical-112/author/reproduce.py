#!/usr/bin/env python3
"""Reproduce the literal inverse, actual phases and unchanged tariff."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
def main(a):
    here=Path(__file__).resolve().parent;out=a.output.resolve()
    if out==here or here in out.parents:raise ValueError('external reproduction required')
    sources=json.loads((here/'SOURCES.json').read_text());paths={}
    for k,v in sources['runtime_dependencies'].items():
        q=here/v['local_path']if'local_path'in v else a.repo/v['repo_path']
        if sha(q)!=v['sha256']:raise ValueError('dependency pin '+k)
        paths[k]=q
    for k,v in sources['provenance_only'].items():
        if sha(here/v['local_path'])!=v['sha256']:raise ValueError('provenance pin '+k)
    out.mkdir(parents=True,exist_ok=True);prefix=[sys.executable,'-I','-B']
    run(prefix+[str(here/'build.py'),'--source',str(paths['forward']),'--dynamic',str(paths['dynamic_replay']),
        '--engine',str(paths['replay']),'--output',str(out)])
    run(prefix+[str(paths['map_checker']),'--parent',str(paths['seed']),'--word',str(out/'WORD.json.gz'),
        '--kind','partial','--engines',str(paths['clifford'].parent),'--output',str(out/'PHASES.json')])
    run(prefix+[str(here/'price.py'),'--engine',str(paths['interval']),'--word',str(out/'WORD.json.gz'),'--output',str(out/'PRICE.json')])
    outputs={}
    for name in('WORD.json.gz','RESULT.json','PHASES.json','PRICE.json'):
        if sha(out/name)!=sha(here/'output'/name):raise ValueError('artifact mismatch '+name)
        outputs[name]=sha(out/name)
    r={'status':'PASS_INVERSE_SOURCE_REPRODUCTION','source_pins':len(paths),'outputs':outputs,
      'scope':'Author deterministic reproduction. Explicit reverse-boundary service; separate independent review and mixed-orientation caller proof remain.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
