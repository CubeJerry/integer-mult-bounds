"""Reproduce CP3 in fresh output directories; independent code is labelled."""
import argparse, concurrent.futures, json, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=a.repo.resolve();o=a.out.resolve();o.mkdir(parents=True,exist_ok=True)
b=r/'research/moonshot-005-program/results'
s=b/'bit-singular-eight-seed-source';t=b/'nonlinear-compact-control'
f=b/'fixed-monomial-compact-bridge';c=b/'complex-nonclifford-native-source'
jobs=[
 ('seed-author',[s/'seed/check_seed.py','--repo',r,'--out',o/'seed']),
 ('word-independent-c',[s/'independent-c/check.py','--repo',r,'--word',s/'author/output/WORD.json','--seed',s/'seed/SOURCE.json','--out',o/'word']),
 ('seed-word-independent-root',[s/'root-review/check.py','--repo',r,'--seed',s/'seed/SOURCE.json','--word',s/'author/output/WORD.json','--funnel-review',b/'bit-shared-meet-funnel/root-review','--out',o/'seed-word']),
 ('toffoli-author',[t/'author/check.py','--out',o/'toffoli']),
 ('toffoli-independent-c',[t/'independent-c/check.py','--out',o/'toffoli-review']),
 ('fixed-monomial-author',[f/'author/check.py','--out',o/'fixed']),
 ('fixed-monomial-independent-root',[f/'root-review/check.py','--source',f/'author/PROOF.md','--out',o/'fixed-review']),
 ('nonclifford-author',[c/'author/check.py','--repo',r,'--out',o/'nonclifford-author.json']),
 ('nonclifford-independent-root',[c/'root-review/check.py','--out',o/'nonclifford-review']),
]
def run(job):
 name,args=job;cmd=[sys.executable,'-B']+list(map(str,args))
 q=subprocess.run(cmd,cwd=r,text=True,capture_output=True,timeout=180)
 (o/(name+'.log')).write_text(q.stdout+q.stderr)
 return {'name':name,'returncode':q.returncode,'command':cmd}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 results=list(ex.map(run,jobs))
if all(x['returncode']==0 for x in results):
 results.append(run(('word-independent-price',[s/'independent-c/price.py','--review',o/'word/RESULT.json','--out',o/'word-price'])))
status='PASS_CP3_REPRODUCTION' if all(x['returncode']==0 for x in results) else 'FAIL'
(o/'REPRODUCTION.json').write_text(json.dumps({'status':status,'commands':results},indent=2)+'\n')
print(json.dumps({'status':status,'commands':len(results),'failed':[x['name'] for x in results if x['returncode']]}))
raise SystemExit(0 if status.startswith('PASS') else 1)
