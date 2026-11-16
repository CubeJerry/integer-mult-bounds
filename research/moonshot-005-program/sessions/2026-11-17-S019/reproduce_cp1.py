#!/usr/bin/env python3
"""Reproduce only the newly reviewed S019 checkpoint1 gates and recovered evidence."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, hashlib, json, subprocess, sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
session=repo/'research/moonshot-005-program/sessions/2026-11-17-S019';ev=session/'checkpoint1-evidence';old=repo/'research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint6-evidence'
common=['--repo',str(repo),'--evidence',str(old)];dual=ev/'R/PETERSEN-SHORT-DUAL.json'
tasks=[
('C-native',ev/'C/portable/audit_cp6.py',common+['--out',str(out/'C')],out/'C/RESULT.json',ev/'C/portable/output/RESULT.json'),
('C-static',ev/'C/portable/audit_static.py',common+['--out',str(out/'C')],out/'C/STATIC-RESULT.json',ev/'C/portable/output/STATIC-RESULT.json'),
('C-entropy',ev/'C/portable/review_nonlinear.py',common+['--dual',str(dual),'--out',str(out/'C')],out/'C/NONLINEAR-REVIEW-RESULT.json',ev/'C/portable/output/NONLINEAR-REVIEW-RESULT.json'),
('B-complex',ev/'B/cp6-independent-review/check.py',common+['--out',str(out/'B-RESULT.json')],out/'B-RESULT.json',ev/'B/cp6-independent-review/RESULT.json'),
('R-entropy',ev/'R/check_petersen_gate.py',['--repo',str(repo),'--word',str(old/'A/local-canonical9-source/WORD.json'),'--dual',str(dual),'--out',str(out/'R-RESULT.json')],out/'R-RESULT.json',ev/'R/PETERSEN-GATE-RESULT.json')]
def run(t):
 name,script,args,result,frozen=t
 proc=subprocess.run([sys.executable,'-B',str(script),*args],cwd=repo,text=True,capture_output=True)
 (out/(name+'.log')).write_text(proc.stdout+proc.stderr)
 if proc.returncode: raise RuntimeError(f'{name} failed: '+proc.stderr[-3000:])
 obj=json.loads(result.read_text());expected=json.loads(frozen.read_text())
 if obj!=expected:raise RuntimeError(name+' differs from frozen receipt')
 return {'name':name,'status':obj['status'],'script':str(script.relative_to(repo)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'result_sha256':hashlib.sha256(result.read_bytes()).hexdigest(),'frozen_receipt_json_equal':True,'command':['python','-B',str(script.relative_to(repo)),*args]}
with ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(run,tasks))
receipt={'status':'PASS_S019_CP1_FRESH_REPRODUCTION','scope':'Five new review/gate checks; not a claim to rerun every inherited primitive invoice.','checks':results}
(out/'REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['status']);print('Five independently scoped checks matched their frozen JSON receipts.')
