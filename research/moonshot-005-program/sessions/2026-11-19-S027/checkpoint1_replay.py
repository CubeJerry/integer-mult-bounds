"""Serial portable replay of the four admitted S027 checkpoint-one packages."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    repo=a.repo.resolve();base=repo/'research/moonshot-005-program/results';a.out.mkdir(parents=True,exist_ok=True)
    irr=base/'bit-irreducible-low-excess-target';cl=base/'bit-class-separated-middle-gate';cut=base/'bit-triangle-joint-repair-floor';gauge=base/'bit-triangle-donor-gauge-gate';source=cut/'source'
    jobs=[('irreducible-author',irr/'author/check.py',['--repo',repo],irr/'author/output/RESULT.json','RESULT.json'),('irreducible-review',irr/'review/check.py',['--repo',repo],irr/'review/output/RESULT.json','RESULT.json'),('irreducible-budget',irr/'review/budget.py',[],irr/'review/output/BUDGET.json','BUDGET.json'),('class-author',cl/'author/check.py',['--repo',repo],cl/'author/output/RESULT.json','RESULT.json'),('class-review',cl/'review/check.py',['--repo',repo,'--author',cl/'author'],cl/'review/output/RESULT.json','RESULT.json'),('joint-cut-author',cut/'author/reconstruct.py',['--repo',repo,'--source',source],cut/'author/output/RECONSTRUCTION.json','RECONSTRUCTION.json'),('joint-cut-review',cut/'review/check.py',['--repo',repo,'--author',cut/'author'],cut/'review/output/RESULT.json','RESULT.json'),('gauge-author',gauge/'author/check.py',['--repo',repo,'--triangle-author',source],gauge/'author/output/RESULT.json','RESULT.json'),('gauge-review',gauge/'review/check.py',['--repo',repo,'--author',gauge/'author','--triangle',source],gauge/'review/output/RESULT.json','RESULT.json')]
    results=[]
    for name,script,args,expected,output in jobs:
        start=time.monotonic();dest=a.out/name;cmd=[sys.executable,'-B',str(script),*map(str,args),'--out',str(dest)]
        proc=subprocess.run(cmd,cwd=repo,text=True,capture_output=True,timeout=900)
        if proc.returncode:raise RuntimeError(name+' failed\n'+proc.stdout[-2000:]+'\n'+proc.stderr[-4000:])
        actual=json.loads((dest/output).read_text());wanted=json.loads(expected.read_text())
        if actual!=wanted:raise RuntimeError(name+' result differs from admitted receipt')
        result={'name':name,'script':str(script.relative_to(repo)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'matches_admitted_json':True,'seconds':round(time.monotonic()-start,3)};results.append(result);print(json.dumps(result),flush=True)
    receipt={'status':'PASS_S027_CHECKPOINT1_INTEGRATED_REPLAY','checks':results,'separate_mathematical_reviews':'Per-package review/REVIEW.md; this serial replay is not another independent review.','new_complete_kappa':False}
    (a.out/'VALIDATION.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
