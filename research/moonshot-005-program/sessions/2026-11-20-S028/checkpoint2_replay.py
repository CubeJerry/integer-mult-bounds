#!/usr/bin/env python3
"""Relocated S028 checkpoint2 reproduction, separate from independent reviews."""
import argparse,gzip,hashlib,json,platform,subprocess,sys,time
from pathlib import Path
P='research/moonshot-005-program'
def need(x,s):
    if not x:raise ValueError(s)
def canonical(value):
    if isinstance(value,list):return [canonical(x)for x in value]
    if not isinstance(value,dict):return value
    return {k:canonical(v)for k,v in value.items()if k not in ('elapsed_seconds','seconds')}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--group',choices=['middle','source-spread','all'],default='all');a=ap.parse_args()
    repo=a.repo.resolve();a.out.mkdir(parents=True,exist_ok=True)
    k=f'{P}/results/bit-shared-k-filtered-quotient';dual=f'{P}/results/bit-clifford-adjoint-interface'
    jobs=[('k-cut-author',k+'/author/check.py',[],k+'/author/output',['RESULT.json']),
      ('k-mixer-author',k+'/author/mixer.py',[],k+'/author/mixer-output',['RESULT.json','MATRIX.json','WORD.json.gz']),
      ('k-review',k+'/review/check.py',['--author',str(repo/k/'author')],k+'/review/output',['RESULT.json']),
      ('dual-author',dual+'/author/check.py',[],dual+'/author/output',['RESULT.json']),
      ('dual-review',dual+'/review/check.py',['--author',str(repo/dual/'author')],dual+'/review/output',['RESULT.json'])]
    source=f'{P}/results/bit-coupled-source-reduced-determinants';spread=f'{P}/results/bit-orthogonal-spread-port-allocation'
    more=[('coupled-author',source+'/author/check.py',[],source+'/author/output',['RESULT.json','SPAN-WITNESSES.json','GRAPHS.json']),
      ('coupled-review',source+'/review/check.py',['--author',str(repo/source/'author')],source+'/review/output',['RESULT.json','SPAN-CENSUS.json']),
      ('spread-author',spread+'/author/discover.py',[],spread+'/author/output',['RESULT.json','WITNESS.json.gz']),
      ('spread-review',spread+'/review/check.py',['--author',str(repo/spread/'author')],spread+'/review/output',['RESULT.json'])]
    jobs=jobs if a.group=='middle' else more if a.group=='source-spread' else jobs+more
    receipts=[]
    for name,script,extra,expected,outputs in jobs:
        output=a.out/name;output.mkdir(exist_ok=True);log=a.out/(name+'.log')
        command=[sys.executable,'-B',str(repo/script),'--repo',str(repo),'--out',str(output),*extra];start=time.monotonic()
        with log.open('w')as stream:r=subprocess.run(command,cwd=repo,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
        need(r.returncode==0,f'{name} failed; see {log}');checked=[]
        for filename in outputs:
            old=repo/expected/filename;new=output/filename
            oldbytes=old.read_bytes();newbytes=new.read_bytes()
            if filename.endswith('.gz'):
                oldbytes=gzip.decompress(oldbytes);newbytes=gzip.decompress(newbytes)
                need(oldbytes==newbytes,f'{name} changed decompressed {filename}')
            else:need(canonical(json.loads(oldbytes))==canonical(json.loads(newbytes)),f'{name} changed {filename}')
            checked.append({'file':filename,'payload_stored_sha256':hashlib.sha256(oldbytes).hexdigest(),'payload_replay_sha256':hashlib.sha256(newbytes).hexdigest()})
        receipts.append({'name':name,'command':command,'exit_code':0,'wall_seconds':time.monotonic()-start,'outputs':checked,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
        print(name,'PASS',round(receipts[-1]['wall_seconds'],2),flush=True)
    result={'status':'PASS_S028_CHECKPOINT2_RELOCATED_REPRODUCTION','baseline_sha':'fb59a4ae85b7d81dce79ee5189f7b9f081542a3c','jobs':receipts,'python':sys.version,'platform':platform.platform(),
      'normalization':'Only elapsed_seconds/seconds runtime metadata is ignored. Compressed artifacts are compared by exact decompressed bytes. All scientific fields and pins must agree.',
      'independence':'Reproduction is separate from the mathematical and independently implemented reviews already in each package.',
      'group':a.group,'new_complete_kappa':False,'all_five_foundations_retained':True}
    (a.out/'VALIDATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':main()
