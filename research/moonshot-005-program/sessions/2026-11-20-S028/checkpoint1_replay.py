#!/usr/bin/env python3
"""Serial relocated S028 checkpoint1 reproduction; distinct from review."""
import argparse,hashlib,json,platform,subprocess,sys,time
from pathlib import Path
P='research/moonshot-005-program'
def need(x,s):
    if not x:raise ValueError(s)
def canonical(value):
    if isinstance(value,list):return [canonical(x)for x in value]
    if not isinstance(value,dict):return value
    out={k:canonical(v)for k,v in value.items()if k not in ('source_pins','elapsed_seconds')}
    if 'source_pins'in value:out['source_pin_hashes']=sorted(x['sha256']for x in value['source_pins'])
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--group',choices=['core','class','all'],default='all');a=ap.parse_args()
    repo=a.repo.resolve();a.out.mkdir(parents=True,exist_ok=True)
    src=f'{P}/work-in-progress/2026-11-19-S027/covariant-trace-source'
    target=f'{P}/results/bit-two-sided-covariant-target';gate=f'{P}/results/bit-fully-early-source-divisibility';review=f'{P}/results/bit-covariant-source-existence/review'
    jobs=[('source-author',src+'/check.py',[],src+'/output',['RESULT.json']),
      ('source-review',review+'/independent.py',[],review+'/output',['REVIEW-RESULT.json']),
      ('target-author',target+'/author/check.py',[],target+'/author/output',['RESULT.json','ASSIGNMENT.json']),
      ('target-review',target+'/review/check.py',['--author',str(repo/target/'author')],target+'/review/output',['RESULT.json']),
      ('divisibility-author',gate+'/author/check.py',[],gate+'/author/output',['RESULT.json','GEOMETRY.json']),
      ('divisibility-review',gate+'/review/check.py',['--author',str(repo/gate/'author')],gate+'/review/output',['RESULT.json'])]
    cls=f'{P}/results/bit-fixed-class-relabel-obstruction'
    more=[('class-author',cls+'/author/check.py',[],cls+'/author/output',['RESULT.json']),
      ('class-review',cls+'/review/check.py',['--author',str(repo/cls/'author')],cls+'/review/output',['RESULT.json'])]
    jobs=jobs if a.group=='core' else more if a.group=='class' else jobs+more
    receipts=[]
    for name,script,extra,expected,outputs in jobs:
        output=a.out/name;output.mkdir(exist_ok=True);log=a.out/(name+'.log')
        command=[sys.executable,'-B',str(repo/script),'--repo',str(repo),'--out',str(output),*extra];start=time.monotonic()
        with log.open('w')as stream:r=subprocess.run(command,cwd=repo,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
        need(r.returncode==0,f'{name} failed; see {log}');checked=[]
        for filename in outputs:
            old=repo/expected/filename;new=output/filename
            need(canonical(json.loads(old.read_bytes()))==canonical(json.loads(new.read_bytes())),f'{name} changed {filename}')
            checked.append({'file':filename,'stored_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'replay_sha256':hashlib.sha256(new.read_bytes()).hexdigest()})
        receipts.append({'name':name,'command':command,'exit_code':0,'wall_seconds':time.monotonic()-start,'outputs':checked,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
        print(name,'PASS',round(receipts[-1]['wall_seconds'],2),flush=True)
    result={'status':'PASS_S028_CHECKPOINT1_RELOCATED_REPRODUCTION','baseline_sha':'9e3fa0639d8a2bcf5660a950482af6ce9e0af57c','jobs':receipts,'python':sys.version,'platform':platform.platform(),
      'normalization':'Source-pin path spellings may relocate and elapsed_seconds is runtime metadata; source hash multiset and all scientific fields must agree.',
      'independence':'This reproduction is separate from the mathematical and independently implemented reviews already in each package.',
      'group':a.group,'new_complete_kappa':False,'all_five_foundations_retained':True}
    (a.out/'VALIDATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':main()
