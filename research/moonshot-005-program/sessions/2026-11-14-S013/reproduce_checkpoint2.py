from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess,time
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
R=args.repo.resolve()
P=R/'research/moonshot-005-program';D=P/'results'
OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
native=R/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
old=D/'proper-chart-relay/author/20/WORD.json.gz'
jobs=[]
def job(name,steps):jobs.append((name,steps))
def py(script,*args,opt=False):return ['python','-B']+(['-O']if opt else[])+[str(script)]+[str(x)for x in args]
def author(name):return D/name/'author'
def rev(name,which='review-root'):return D/name/which

a=author('relay-gram-fitting-rigidity');r=rev('relay-gram-fitting-rigidity')
job('gram-rigidity',[py(a/'check.py','--source',old,'--output',OUT/'gram-author.json'),py(r/'check.py','--source',old,'--output',OUT/'gram-independent.json')])
a=author('relay-rank-two-skew-repair');r=rev('relay-rank-two-skew-repair');o=OUT/'skew';o.mkdir(exist_ok=True)
job('rank-two-skew',[py(a/'build.py','--source',old,'--out',o,opt=True),py(a/'algebra.py','--source',old,'--output',o/'ARITHMETIC.json'),py(a/'forward.py','--source',o/'WORD.json.gz','--out',o/'forward',opt=True),py(a/'phase.py','--engines',D/'proper-chart-relay/author/dependencies','--word',o/'forward/WORD.json.gz','--output',o/'PHASE.json'),py(a/'price.py','--old-price',D/'proper-chart-relay/author/20/PRICE.json','--output',o/'PRICE.json'),py(r/'check.py','--repo',R,'--package',a,'--output',OUT/'skew-independent.json')])
a=author('bit-quadratic-history-pivot');r=rev('bit-quadratic-history-pivot');o=OUT/'pivot'
job('quadratic-pivot',[py(a/'build.py','--native',native,'--outdir',o,opt=True),py(a/'price.py','--result',o/'RESULT.json','--output',o/'BUDGET.json'),py(r/'check.py','--repo',R,'--package',a,'--engine',rev('bit-moment-harvest')/'check.py','--output',OUT/'pivot-independent.json')])
a=author('bit-purified-quadratic-history');r=rev('bit-purified-quadratic-history','review-c');o=OUT/'purified'
job('purified-pivot',[py(a/'build.py','--native',native,'--pivot',author('bit-quadratic-history-pivot')/'output/PREFIX.json.gz','--rank-certificate',D/'bit-minimum-rank-nine/CERTIFICATE.json','--rigidity-certificate',D/'bit-fitting-rigidity/global/CERTIFICATE.json','--outdir',o,opt=True),py(a/'price.py','--result',o/'RESULT.json','--output',o/'BUDGET.json'),py(r/'check.py','--repo',R,'--prefix',a/'output/PREFIX.json.gz','--output',OUT/'purified-independent.json'),py(r/'check_strict.py','--repo',R,'--output',OUT/'strict-independent.json')])
a=author('bit-moment-harvest');r=rev('bit-moment-harvest');o=OUT/'harvest';o.mkdir(exist_ok=True)
job('moment-harvest',[py(a/'build.py','--native',native,'--selected','8,10,12','--outdir',o/'cubic',opt=True),py(a/'build.py','--native',native,'--selected','8,10,12,13','--outdir',o/'d4',opt=True),py(a/'price.py','--cubic',o/'cubic/RESULT.json','--d4',o/'d4/RESULT.json','--output',o/'BUDGET.json'),py(r/'check.py','--repo',R,'--package',a,'--output',OUT/'harvest-independent.json')])
a=author('bit-pivot-filter-geometry');r=rev('bit-pivot-filter-geometry')
job('pivot-filter-geometry',[py(a/'check_geometry.py','--repo',R,'--output',OUT/'pivot-filter-author.json',opt=True),py(r/'check.py','--repo',R,'--certificate',a/'GEOMETRY.json','--output',OUT/'pivot-filter-independent.json')])
a=author('bit-cubic-koszul');r=rev('bit-cubic-koszul')
job('cubic-koszul',[py(a/'check.py','--repo',R,'--geometry-check',author('bit-quadratic-exterior')/'check.py','--output',OUT/'cubic-author.json',opt=True),py(r/'check.py','--repo',R,'--output',OUT/'cubic-independent.json')])
def run(item):
 name,steps=item;start=time.monotonic();runs=[]
 for j,cmd in enumerate(steps):
  p=subprocess.run(cmd,cwd=R,capture_output=True,text=True);log=OUT/f'{name}-{j}.log';log.write_text(p.stdout+p.stderr)
  runs.append({'command':cmd,'exit':p.returncode,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'log_bytes':log.stat().st_size})
  if p.returncode:return{'name':name,'status':'FAIL','steps':runs,'last_output':(p.stdout+p.stderr)[-2000:]}
 return{'name':name,'status':'PASS','steps':runs,'seconds':round(time.monotonic()-start,3)}
results=[]
with ThreadPoolExecutor(max_workers=4)as pool:
 for future in as_completed([pool.submit(run,item)for item in jobs]):
  r=future.result();results.append(r);print(json.dumps({'name':r['name'],'status':r['status'],'last_output':r.get('last_output','')}),flush=True)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'baseline_sha':'7ff42586f6405428990867eaf42a2924bf851308','status':'PASS'if all(x['status']=='PASS'for x in results)else'FAIL','classification':'Author reproduction, distinct independent mathematical/source implementations, and inherited phase engines are explicitly separated. No new kappa.','jobs':sorted(results,key=lambda x:x['name'])}
(OUT/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
raise SystemExit(0 if receipt['status']=='PASS' else 1)
