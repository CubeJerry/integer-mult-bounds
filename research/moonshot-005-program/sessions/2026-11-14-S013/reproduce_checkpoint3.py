#!/usr/bin/env python3
"""Six bounded source/proof-premise reproductions; never overwrite frozen evidence."""
import argparse,hashlib,json,shutil,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();R=a.repo.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False);D=R/'research/moonshot-005-program/results';N=R/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';G=D/'bit-quadratic-exterior/author/check.py';jobs=[]
 def py(script,*args,opt=False):return['python','-B']+(['-O']if opt else[])+list(map(str,[script,*args]))
 def job(name,steps):jobs.append((name,steps))
 A=D/'eisenstein-cycle-native/author';V=D/'eisenstein-cycle-native/review-root';E=O/'eisenstein';E.mkdir();shutil.copy2(A/'symmetry.py',E/'symmetry.py')
 job('full120-cycle',[py(E/'symmetry.py'),py(A/'build.py','--symmetry',E/'SYMMETRY.json','--output-dir',E,opt=True),py(A/'operators.py','--word',E/'WORD.json.gz','--symmetry',E/'SYMMETRY.json','--output',E/'OPERATORS.json',opt=True),py(A/'budget.py','--output',E/'BUDGET.json',opt=True),py(A/'phase.py','--engines',D/'proper-chart-relay/author/dependencies','--word',E/'WORD.json.gz','--output',E/'PHASE.json'),py(V/'check.py','--package',A,'--output',E/'INDEPENDENT.json'),py(V/'budget_check.py','--output',E/'INDEPENDENT-BUDGET.json')])
 A=D/'bit-pivot-point-puncture/author';V=D/'bit-pivot-point-puncture/review-c';E=O/'point-puncture'
 job('point-puncture',[py(A/'build.py','--native',N,'--prefix',D/'bit-purified-quadratic-history/author/output/PREFIX.json.gz','--pivot-geometry',D/'bit-pivot-filter-geometry/author/GEOMETRY.json','--outdir',E,opt=True),py(A/'price.py','--result',E/'RESULT.json','--output',E/'BUDGET.json'),py(V/'check.py','--repo',R,'--prefix',A/'output/PREFIX.json.gz','--output',O/'POINT-INDEPENDENT.json'),py(V/'check_strict.py','--repo',R,'--output',O/'POINT-STRICT.json')])
 for name,label in [('bit-proper-flat-cubic-generators','flat-cubic'),('bit-proper-sixteen-class','sixteen-class')]:
  A=D/name/'author';V=D/name/'review-root';job(label,[py(A/'check.py','--repo',R,'--geometry-check',G,'--output',O/(label+'-AUTHOR.json'),opt=True),py(V/'check.py','--repo',R,'--certificate',A/'RESULT.json','--output',O/(label+'-INDEPENDENT.json'))])
 A=D/'bit-canonical-pair-gate/author';V=D/'bit-canonical-pair-gate/review-root'
 job('canonical-pair-gate',[py(A/'check.py','--repo',R,'--geometry-check',G,'--output',O/'PAIR-AUTHOR.json',opt=True),py(V/'check.py','--repo',R,'--certificate',A/'RESULT.json','--output',O/'PAIR-INDEPENDENT.json')])
 A=D/'bit-pentagon-history-fork/author';V=D/'bit-pentagon-history-fork/review-root';E=O/'fork'
 job('pentagon-history-fork',[py(A/'build.py','--native',N,'--outdir',E,opt=True),py(A/'price.py','--result',E/'RESULT.json','--output',E/'BUDGET.json'),py(V/'check.py','--repo',R,'--package',A/'output','--output',O/'FORK-INDEPENDENT.json'),py(V/'check_continuable.py','--repo',R,'--package',A/'output','--output',O/'FORK-LIVE-INDEPENDENT.json'),py(V/'price_check.py','--output',O/'FORK-PRICE-INDEPENDENT.json')])
 def run(item):
  name,steps=item;start=time.monotonic();receipt=[]
  for i,cmd in enumerate(steps):
   p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,timeout=180);log=O/f'{name}-{i}.log';log.write_text(p.stdout+p.stderr);receipt.append({'command':cmd,'exit':p.returncode,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
   if p.returncode:return{'name':name,'status':'FAIL','steps':receipt,'last_output':(p.stdout+p.stderr)[-1800:]}
  return{'name':name,'status':'PASS','steps':receipt,'seconds':round(time.monotonic()-start,3)}
 results=[]
 with ThreadPoolExecutor(max_workers=3)as pool:
  for f in as_completed([pool.submit(run,item)for item in jobs]):
   d=f.result();results.append(d);print(json.dumps({'name':d['name'],'status':d['status'],'last_output':d.get('last_output','')}),flush=True)
 receipt={'status':'PASS'if all(d['status']=='PASS'for d in results)else'FAIL','baseline_sha':'5f4f9a1be068937d0e3ae1a78e81bf7f6b0a6e9d','utc':datetime.now(timezone.utc).isoformat(),'classification':'Author reproduction, independent source/premise implementations, written universal proofs and retained phase-engine evidence are distinct. No new kappa.','jobs':sorted(results,key=lambda d:d['name'])};(O/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
 raise SystemExit(0 if receipt['status']=='PASS' else 1)
if __name__=='__main__':main()
