"""Portable serial replay of the S027 source and middle construction packages."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--group',choices=['baseline','source','all'],default='all');a=ap.parse_args()
 repo=a.repo.resolve();base=repo/'research/moonshot-005-program/results';a.out.mkdir(parents=True,exist_ok=True)
 info=base/'bit-middle-information-factorization';phase=base/'bit-paid-middle-phase-completion'
 tile=base/'bit-native-irreducible-target-tile';row=base/'bit-native-irreducible-target-projection'
 gate=base/'bit-clifford-one-evaluation-gate';source=base/'bit-clifford-two-evaluation-source'
 jobs=[]
 def add(group,name,script,args,expected,output='RESULT.json'):jobs.append((group,name,script,args,expected,output))
 for name,p in [('information',info),('paid-phase',phase)]:
  add('baseline',name+'-author',p/'author/check.py',[],p/'author/output/RESULT.json')
  add('baseline',name+'-review',p/'review/check.py',['--author',p/'author'],p/'review/output/RESULT.json')
 add('baseline','tile-author',tile/'author/build.py',['--repo',repo],tile/'author/output/RESULT.json')
 add('baseline','tile-controls',tile/'author/controls.py',['--repo',repo,'--word',tile/'author/output/WORD.json.gz'],tile/'author/controls/RESULT.json')
 add('baseline','tile-review',tile/'review/check.py',['--repo',repo,'--author',tile/'author'],tile/'review/output/RESULT.json')
 add('baseline','projection-author',row/'author/build.py',['--repo',repo,'--tile',tile/'author/output/WORD.json.gz'],row/'author/output/RESULT.json')
 add('baseline','projection-controls',row/'author/controls.py',['--repo',repo,'--word',row/'author/output/WORD.json.gz','--routing',row/'author/output/ROUTING.json.gz'],row/'author/controls/RESULT.json')
 add('baseline','projection-review',row/'review/check.py',['--repo',repo,'--author',row/'author','--tile',tile/'author/output/WORD.json.gz'],row/'review/output/RESULT.json')
 add('baseline','one-evaluation-author',gate/'author/check.py',['--repo',repo],gate/'author/output/RESULT.json')
 add('baseline','one-evaluation-review',gate/'review/check.py',['--repo',repo,'--author',gate/'author'],gate/'review/output/RESULT.json')
 add('source','two-evaluation-author',source/'author/check.py',['--repo',repo,'--basis',source/'author/BASIS.json','--witness',source/'author/output/WITNESS.json'],source/'author/output/RESULT.json')
 add('source','two-evaluation-review',source/'review/check.py',['--repo',repo,'--author',source/'author','--basis',source/'author/BASIS.json'],source/'review/output/RESULT.json')
 add('source','two-evaluation-phase-review',source/'review/phase_check.py',['--repo',repo,'--author',source/'author','--basis',source/'author/BASIS.json'],source/'review/output/PHASE-RESULT.json','PHASE-RESULT.json')
 add('source','shared-plane-scope-author',source/'shared-plane-scope/check.py',['--repo',repo],source/'shared-plane-scope/output/RESULT.json')
 add('source','shared-plane-scope-review',source/'scope-review/check.py',['--repo',repo],source/'scope-review/output/RESULT.json')
 results=[]
 for group,name,script,args,expected,output in jobs:
  if a.group!='all' and group!=a.group:continue
  start=time.monotonic();dest=a.out/name;cmd=[sys.executable,'-B',str(script),*map(str,args),'--out',str(dest)]
  proc=subprocess.run(cmd,cwd=repo,text=True,capture_output=True,timeout=900)
  if proc.returncode:raise RuntimeError(name+' failed\n'+proc.stdout[-2000:]+'\n'+proc.stderr[-4000:])
  actual=json.loads((dest/output).read_text());wanted=json.loads(expected.read_text())
  if actual!=wanted:raise RuntimeError(name+' differs from admitted receipt')
  result={'name':name,'script':str(script.relative_to(repo)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'matches_admitted_json':True,'seconds':round(time.monotonic()-start,3)}
  results.append(result);print(json.dumps(result),flush=True)
 receipt={'status':'PASS_S027_CHECKPOINT2_INTEGRATED_REPLAY','group':a.group,'checks':results,'separate_reviews':'Per-package review/REVIEW.md; this replay is not another independent review.','new_complete_kappa':False}
 (a.out/'VALIDATION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
