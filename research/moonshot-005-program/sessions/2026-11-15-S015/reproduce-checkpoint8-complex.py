#!/usr/bin/env python3
"""Portable reproduction of admitted complex source controls; no frozen-file mutation."""
import argparse,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);src=repo/'research/moonshot-005-program/results/complex-entangling-native-source';q=out/'package';shutil.copytree(src,q,dirs_exist_ok=True);commands=[];comparisons=[]
def run(label,file,*args):
 cmd=[sys.executable,'-B',str(q/file),*map(str,args)];t=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,cwd=out);(out/(label+'.log')).write_text(r.stdout+r.stderr);commands.append({'label':label,'command':cmd,'exit_code':r.returncode,'seconds':round(time.monotonic()-t,3)});assert r.returncode==0,(label,r.stderr[-3000:])
def compare(n):
 x=(src/n).read_bytes();y=(q/n).read_bytes();assert json.loads(x)==json.loads(y),n;comparisons.append({'committed':str((src/n).relative_to(repo)),'reproduced':str((q/n).relative_to(out)),'comparison':'byte_identical'if x==y else'json_equal','committed_sha256':hashlib.sha256(x).hexdigest()})
for label,script,receipt,extra in [('order9','check.py','RESULT.json',['--repo',repo]),('order15','check_entangling_source.py','ENTANGLING-RESULT.json',['--repo',repo]),('admission','check_source_admission.py','SOURCE-ADMISSION-RESULT.json',['--repo',repo]),('wreath','check_local_wreath.py','LOCAL-WREATH-RESULT.json',[])]:
 run(label,'author/'+script,*extra);compare('author/'+receipt)
run('independent-source','independent-a/check_source.py','--source',q/'author','--repo',repo);compare('independent-a/output/SOURCE-RESULT.json')
run('independent-wreath','independent-a/check_wreath.py','--source',q/'author');compare('independent-a/output/WREATH-RESULT.json')
run('independent-budget','independent-a/check_budget.py');compare('independent-a/output/BUDGET-RESULT.json')
run('independent-admission','review-root/check.py','--out',q/'review-root/output');compare('review-root/output/RESULT.json')
(out/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');(out/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n');print(json.dumps({'status':'PASS_CP8_COMPLEX_REPRODUCTION','commands':len(commands),'comparisons':len(comparisons),'byte_identical':sum(x['comparison']=='byte_identical'for x in comparisons)}))
