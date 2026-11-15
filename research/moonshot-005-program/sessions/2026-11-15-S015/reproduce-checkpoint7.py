#!/usr/bin/env python3
"""Portable CP7 author/independent replays without changing frozen evidence."""
import argparse,concurrent.futures,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',choices=['relay','mds','onehop','singlecell']);a=ap.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);root=repo/'research/moonshot-005-program/results';commands=[];comparisons=[]
 def group(name):
  work=out/name;work.mkdir(exist_ok=True);cs=[];ds=[]
  def copy(src,dst):shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  def run(label,script,*args):
   cmd=[sys.executable,'-B',str(script),*map(str,args)];start=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,cwd=work);(work/(label+'.log')).write_text(p.stdout+p.stderr);cs.append({'group':name,'label':label,'command':cmd,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3)});assert p.returncode==0,(label,p.stderr[-2000:])
  def compare(src,dst):
   x=src.read_bytes();y=dst.read_bytes();assert json.loads(x)==json.loads(y),(name,str(src),str(dst));ds.append({'group':name,'committed':str(src.relative_to(repo)),'reproduced':str(dst.relative_to(out)),'comparison':'byte_identical'if x==y else'json_equal','committed_sha256':hashlib.sha256(x).hexdigest()})
  if name=='relay':
   p=root/'bit-paired-nonlocal-relay';q=work/'author';copy(p/'author',q);base=root/'bit-paired-flag-source/author/output/WORD.json'
   run('build',q/'build.py','--base',base,'--out',q/'output');run('author',q/'check.py','--repo',repo,'--package',q,'--out',q/'verification');run('puncture',q/'check_puncture.py','--repo',repo,'--package',q)
   for n in ['output/WORD.json','output/CLOSED-WORD.json','verification/RESULT.json','verification/PUNCTURE-RESULT.json','verification/WORD-HISTORY.json','verification/CLOSED-WORD-HISTORY.json']:compare(p/'author'/n,q/n)
   rr=work/'review';run('review',p/'review-root/check.py','--repo',repo,'--package',q,'--out',rr);run('price',p/'review-root/price.py','--review',rr/'RESULT.json','--author',q/'verification/RESULT.json','--out',rr/'PRICE.json')
   for n in ['RESULT.json','WORD-HISTORY.json','CLOSED-WORD-HISTORY.json','PRICE.json']:compare(p/'review-root/output'/n,rr/n)
  elif name=='mds':
   p=root/'bit-shared-facet-mds';q=work/'author';copy(p/'author',q)
   run('build',q/'build.py','--repo',repo);run('word',q/'check_word.py','--repo',repo);run('mds',q/'certify_mds.py')
   for n in ['four-chart-word/WORD.json','four-chart-word/COMPLETED-CONTROL-WORD.json','four-chart-word/verification/LOCAL-RESULT.json','four-chart-word/verification/COMPLETED-CONTROL-RESULT.json','four-chart-word/verification/NEGATIVE-CONTROLS.json','MDS-CERTIFICATE.json']:compare(p/'author'/n,q/n)
   rr=work/'review'
   for label,script,extra,receipt in [('word-review','check.py',['--repo',repo],'RESULT.json'),('cover-review','check_cover.py',['--repo',repo],'COVER-RESULT.json'),('mds-review','check_mds.py',[],'MDS-RESULT.json'),('budget-review','check_budget.py',[],'BUDGET-RESULT.json')]:
    run(label,p/'independent-a'/script,*extra,'--source',q,'--out',rr);compare(p/'independent-a/output'/receipt,rr/receipt)
  elif name=='onehop':
   p=root/'bit-shared-facet-one-hop-gate';q=work/'independent-c';copy(p/'independent-c',q);rr=work/'root';run('root',p/'author-root/check.py','--repo',repo,'--out',rr)
   for n in ['RESULT.json','GEOMETRY.json','MATRIX-CONTROLS.json']:compare(p/'author-root/output'/n,rr/n)
   run('independent-c',q/'check.py','--repo',repo);compare(p/'independent-c/RESULT.json',q/'RESULT.json')
  elif name=='singlecell':
   p=root/'bit-paired-single-cell-gate';q=work/'author';copy(p/'author',q);run('author',q/'check.py','--repo',repo,'--base',root/'bit-paired-flag-source/author/output/WORD.json');compare(p/'author/RESULT.json',q/'RESULT.json');rr=work/'root';run('review',p/'review-root/check.py','--repo',repo,'--source',q,'--out',rr);compare(p/'review-root/output/RESULT.json',rr/'RESULT.json')
  return cs,ds
 names=[a.only]if a.only else['relay','mds','onehop','singlecell']
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
  for cs,ds in ex.map(group,names):commands+=cs;comparisons+=ds
 (out/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');(out/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n');print(json.dumps({'status':'PASS_CP7_PORTABLE_REPLAY','commands':len(commands),'comparisons':len(comparisons),'byte_identical':sum(x['comparison']=='byte_identical'for x in comparisons)}))
if __name__=='__main__':main()
