#!/usr/bin/env python3
"""Focused reproducible source, interface and proof-premise checks for S019 checkpoint3."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
S=repo/'research/moonshot-005-program/sessions/2026-11-17-S019';E=S/'checkpoint3-evidence';tasks=[]
def add(name,script,args,actual,frozen,byte=False):tasks.append((name,script,args,actual,frozen,byte))
word=E/'A/interleaved-six/WORD.json';dest=out/'A-interleaved'
add('A-interleaved',E/'A/build_interleaved_carriers.py',['--repo',str(repo),'--out',str(dest)],dest/'WORD.json',word,True)
dest=out/'A-interleaved-contracts';add('A-interleaved-contracts',E/'A/check_interleaved_carriers.py',['--repo',str(repo),'--word',str(word),'--out',str(dest)],dest/'RESULT.json',E/'A/interleaved-six/verification/RESULT.json')
for name in ['spectator-two-bank-reduction','spectator-two-bank-s3-gate']:
 dest=out/('B-'+name);add('B-'+name,E/'B'/name/'check.py',['--repo',str(repo),'--out',str(dest)],dest/'RESULT.json',E/'B'/name/'RESULT.json')
for name,package in [('two-bank-review','spectator-two-bank-reduction'),('s3-review','spectator-two-bank-s3-gate')]:
 dest=out/('C-'+name);add('C-'+name,E/'C'/name/'check.py',['--repo',str(repo),'--package',str(E/'B'/package),'--out',str(dest)],dest/'RESULT.json',E/'C'/name/'output/RESULT.json')
dest=out/'C-interleaved';add('C-interleaved',E/'C/interleaved-review/check.py',['--repo',str(repo),'--word',str(word),'--out',str(dest)],dest/'RESULT.json',E/'C/interleaved-review/output/RESULT.json')
for name in ['dihedral-row-range','signed-s3-extension']:
 dest=out/('R-'+name);add('R-'+name,E/'R'/name/'check.py',['--out',str(dest)],dest/'RESULT.json',E/'R'/name/'output/RESULT.json')
dest=out/'C-dihedral';add('C-dihedral',E/'C/dihedral-review/check.py',['--package',str(E/'R/dihedral-row-range'),'--out',str(dest)],dest/'RESULT.json',E/'C/dihedral-review/output/RESULT.json')
# Source/custody extension is included when its independently reviewed frozen package is present.
if (E/'A/native57-masked-hub').exists():
 w=E/'A/native57-masked-hub/WORD.json';dest=out/'A-masked-Hub';add('A-masked-Hub',E/'A/build_native57_masked_hub.py',['--repo',str(repo),'--matching',str(E/'A/native57-masked-hub/MATCHING.json'),'--out',str(dest)],dest/'WORD.json',w,True)
 dest=out/'R-eight-cut';add('R-eight-cut',E/'R/masked-hub-eight-cut/check.py',['--repo',str(repo),'--word',str(w),'--out',str(dest)],dest/'RESULT.json',E/'R/masked-hub-eight-cut/output/RESULT.json')
 dest=out/'A-masked-Hub-contracts';add('A-masked-Hub-contracts',E/'A/check_native57_masked_hub.py',['--repo',str(repo),'--word',str(w),'--matching',str(E/'A/native57-masked-hub/MATCHING.json'),'--out',str(dest)],dest/'RESULT.json',E/'A/native57-masked-hub/verification/RESULT.json')
 dest=out/'C-masked-Hub';add('C-masked-Hub',E/'C/masked-hub-review/check.py',['--repo',str(repo),'--word',str(w),'--cut-package',str(E/'R/masked-hub-eight-cut'),'--out',str(dest)],dest/'RESULT.json',E/'C/masked-hub-review/output/RESULT.json')
def run(task):
 name,script,args,actual,frozen,byte=task;proc=subprocess.run([sys.executable,'-B',str(script),*args],cwd=repo,capture_output=True,text=True);(out/(name+'.log')).write_text(proc.stdout+proc.stderr)
 if proc.returncode:raise RuntimeError(name+' failed: '+proc.stderr[-2500:])
 if byte:equal=actual.read_bytes()==frozen.read_bytes()
 else:
  x=json.loads(actual.read_text());y=json.loads(frozen.read_text());x.pop('sympy_version',None);y.pop('sympy_version',None);equal=x==y
 if not equal:raise RuntimeError(name+' disagrees with frozen evidence')
 return {'name':name,'status':'PASS','comparison':'byte-identical-word'if byte else'exact-JSON-mathematical-receipt','script':str(script.relative_to(repo)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'result_sha256':hashlib.sha256(actual.read_bytes()).hexdigest()}
with ThreadPoolExecutor(max_workers=max(1,min(a.jobs,8)))as pool:results=list(pool.map(run,tasks))
report={'status':'PASS_S019_CP3_FOCUSED_REPRODUCTION','scope':'New exact sources and independently reviewed algebra/cut premises, not a whole-programme supplier certificate.','checks':results};(out/'REPRODUCTION.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status']);print(len(results),'scoped checks passed')
