#!/usr/bin/env python3
"""Portable final potential-family checks, preserving frozen evidence."""
import argparse,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--core-only',action='store_true');a=ap.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);src=repo/'research/moonshot-005-program/results/complex-parabolic-potential-limits';q=out/'package';shutil.copytree(src,q,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));cs=[];ds=[]
def run(label,script,*args):
 cmd=[sys.executable,'-B',str(q/script),*map(str,args)];t=time.monotonic();r=subprocess.run(cmd,cwd=out,capture_output=True,text=True);(out/(label+'.log')).write_text(r.stdout+r.stderr);cs.append({'label':label,'command':cmd,'exit_code':r.returncode,'seconds':round(time.monotonic()-t,3)});assert r.returncode==0,(label,r.stderr[-2000:])
def compare(n):
 x=(src/n).read_bytes();y=(q/n).read_bytes();assert json.loads(x)==json.loads(y),n;ds.append({'committed':str((src/n).relative_to(repo)),'reproduced':str((q/n).relative_to(out)),'comparison':'byte_identical'if x==y else'json_equal','committed_sha256':hashlib.sha256(x).hexdigest()})
run('core','author-b/check.py','--out',q/'author-b/RESULT.json','--spaces-out',q/'author-b/LAGRANGIANS.json')
for n in ['RESULT.json','LAGRANGIANS.json']:compare('author-b/'+n)
run('independent-enumeration','independent-c/enumerate.py');compare('independent-c/TABLE.json')
run('independent-core','independent-c/check_author.py','--author',q/'author-b');compare('independent-c/RESULT.json')
run('hilbert-review','author-b/check_hilbert.py','--spaces',q/'author-b/LAGRANGIANS.json','--out',q/'author-b/HILBERT-RESULT.json');compare('author-b/HILBERT-RESULT.json')
run('diagonal','independent-c/diagonal.py');compare('independent-c/DIAGONAL-RESULT.json')
run('block-root','block-root/check.py','--table',q/'independent-c/TABLE.json','--out',q/'block-root/output');compare('block-root/output/RESULT.json')
if not a.core_only:
 run('block-independent','block-review-a/check.py','--source',q/'block-root','--out',q/'block-review-a/output');compare('block-review-a/output/RESULT.json')
(out/'COMMANDS.json').write_text(json.dumps(cs,indent=2)+'\n');(out/'COMPARISONS.json').write_text(json.dumps(ds,indent=2)+'\n');print(json.dumps({'status':'PASS_CP10_POTENTIAL_REPRODUCTION','commands':len(cs),'comparisons':len(ds),'byte_identical':sum(x['comparison']=='byte_identical'for x in ds),'core_only':a.core_only}))
