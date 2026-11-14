#!/usr/bin/env python3
"""Rebuild inherited caller instances and replay the new source-specific gates."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stdout+'\n'+r.stderr)
def main(out):
    here=Path(__file__).resolve().parent;out=out.resolve()
    if out==here or here in out.parents:raise ValueError('external output directory required')
    out.mkdir(parents=True,exist_ok=True);prefix=[sys.executable,'-I','-B'];checks={}
    for a in(1,2,6):
        target=out/f'a{a}'
        run(prefix+[str(here/'source/short-build.py'),'--arms',str(a),'--body','8','--out',str(target)])
        for n in('CALLER.json.gz','BUILD.json'):
            if sha(target/n)!=sha(here/f'output/a{a}'/n):raise ValueError('actual caller mismatch')
            checks[f'a{a}/{n}']=sha(target/n)
    run(prefix+[str(here/'check.py'),'--output',str(out/'RESULT.json')])
    run([sys.executable,'-I','-B','-O',str(here/'check.py'),'--output',str(out/'RESULT-OPTIMIZED.json')])
    if sha(out/'RESULT.json')!=sha(out/'RESULT-OPTIMIZED.json')or sha(out/'RESULT.json')!=sha(here/'RESULT.json'):raise ValueError('exact receipt differs')
    result={'status':'PASS_NORMALIZER_DEBT_REPRODUCTION','caller_outputs':checks,'result_sha256':sha(out/'RESULT.json'),
        'normal_and_optimized_identical':True,'scope':'Author deterministic reproduction; independent review is separate. No new kappa.'}
    (out/'REPRODUCTION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
