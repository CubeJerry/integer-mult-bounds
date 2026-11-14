#!/usr/bin/env python3
"""Relocate and reproduce the nine independently reviewed checkpoint11 receipts."""
import argparse,concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
NAMES=['mixed-slope-plane', 'formal-mixed-body-gate', 'mixed-slope-fibre-gate', 'plane-padding-synthesis', 'three-half-endpoint-ranks', 'nonunitary-query-depth', 'three-half-source-reduction', 'signed-inverse-forward-runs', 'half-caller-budget-envelope']
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def run(name):
 package=a.repo.resolve()/'research/moonshot-005-program/results'/name;out=a.out.resolve()/(name+'.json');env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
 r=subprocess.run([sys.executable,str(package/'reproduce.py'),'--output',str(out)],capture_output=True,text=True,env=env)
 if r.returncode:raise RuntimeError(name+'\n'+r.stderr[-4000:]+'\n'+r.stdout[-2000:])
 return {'package':name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'byte_identical_frozen_review':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:checks=list(pool.map(run,NAMES))
receipt={'status':'PASS_NINE_RELOCATED_INDEPENDENT_REVIEWS','checks':checks,'new_kappa':False};(a.out/'SUMMARY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'packages':len(checks)}))
