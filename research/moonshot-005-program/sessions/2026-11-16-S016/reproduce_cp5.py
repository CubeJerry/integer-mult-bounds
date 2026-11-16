"""Rebuild changed source and reproduce independent CP5 checks."""
import argparse,concurrent.futures,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
R=a.repo/'research/moonshot-005-program/results';B=R/'bit-prescribed-code-completion';U=R/'bit-canonical-history-source';G=R/'complex-rank-degree-gate';E=R/'bit-shared-meet-funnel/root-review';old=R/'bit-forked-shared-history/author';done=[]
def run(name,path,*args):
 cmd=[sys.executable,'-B',str(path)]+list(map(str,args));q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (a.out/(name+'.log')).write_text(q.stdout);rec={'name':name,'command':cmd,'returncode':q.returncode};done.append(rec)
 if q.returncode:raise RuntimeError(name+': '+q.stdout[-2500:])
 return rec
run('changed-build',U/'author/build.py','--repo',a.repo,'--base',old/'fifteen/output/WORD.json','--filters',old/'history-fifteen/output/WORD.json','--out',a.out/'changed')
assert (a.out/'changed/WORD.json').read_bytes()==(U/'author/output/WORD.json').read_bytes()
seed=B/'author/SEED-SOURCE.json';source=U/'completion/SOURCE.json'
tasks=[]
for name,script,out in [('point-closure',B/'point-closure/check.py','point-closure'),('point-threshold',B/'point-threshold/check.py','point-threshold'),('changed-author',U/'author/check.py','changed'),('changed-history',U/'author/history.py','changed')]:tasks.append((name,script,'--repo',a.repo,'--out',a.out/out))
for name,script in [('seed-screen','screen.py'),('seed-saturation','certify_saturation.py'),('nonlinear-receipt','check_nonlinear_family.py')]:tasks.append((name,B/'author'/script,'--repo',a.repo,'--seed',seed,'--out',a.out/name))
for name,script in [('changed-completion','certify.py'),('changed-point-closure','check_point_closure.py')]:tasks.append((name,U/'completion'/script,'--repo',a.repo,'--source',source,'--out',a.out/name))
tasks += [('complex-author',G/'author/check.py','--repo',a.repo,'--out',a.out/'complex-author.json'),('complex-root',G/'root-review/check.py','--engine',R/'complex-boolean-sign-family/root-review/check.py','--out',a.out/'complex-root.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda x:run(*x),tasks))
run('seed-certify',B/'author/certify.py','--repo',a.repo,'--seed',seed,'--screen',a.out/'seed-screen/RESULT.json','--out',a.out/'seed-certify')
run('seed-root',B/'root-review/check.py','--repo',a.repo,'--seed',seed,'--closure',a.out/'point-closure/RESULT.json','--threshold',a.out/'point-threshold/THRESHOLD-CERTIFICATE.json','--completion',a.out/'seed-screen/RESULT.json','--out',a.out/'seed-root.json')
run('static-cost',B/'static-cost-gate/check.py','--word',old/'history-fifteen/output/WORD.json','--seed',seed,'--engine',E,'--out',a.out/'static-cost.json')
run('changed-price',U/'author/price.py','--out',a.out/'changed')
run('changed-root',U/'root-review/check.py','--repo',a.repo,'--word',a.out/'changed/WORD.json','--source',source,'--closure',a.out/'changed-point-closure/POINT-CLOSURE.json','--engine',E,'--out',a.out/'changed-root.json')
run('changed-independent-c',U/'independent-c/check.py','--repo',a.repo,'--word',a.out/'changed/WORD.json','--snapshots',a.out/'changed/HISTORY-SNAPSHOTS.json','--code',source,'--out',a.out/'changed-independent-c')
out={'status':'PASS_CP5_REPRODUCTION','rebuilt_words':1,'commands':done,'scope':'Author rebuild/checks and independent source/geometry/proof-witness checks separately labelled; no complete supplier.'}
(a.out/'REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(done),'commands')
