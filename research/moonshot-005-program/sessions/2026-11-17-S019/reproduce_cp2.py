#!/usr/bin/env python3
"""Focused reproduction of S019's newly admitted source mechanisms and gates."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
S=repo/'research/moonshot-005-program/sessions/2026-11-17-S019';E=S/'checkpoint2-evidence';old=repo/'research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint6-evidence';source=S/'checkpoint1-evidence/R/check_petersen_gate.py';word6=E/'A/common-carrier-six/WORD.json';word12=E/'A/d4-hybrid-twelve/WORD.json';tasks=[]
def add(name,script,args,actual,frozen,byte=False):tasks.append((name,script,args,actual,frozen,byte))
def ccheck(name,script,word,folder,output='RESULT.json'):
 dest=out/name;args=['--repo',str(repo),'--out',str(dest)]
 if word:args+=['--word',str(word)]
 add(name,E/'C'/script,args,dest/output,E/'C'/folder/'output'/output)
for name,builder,word,extra in [('A-six','build_common_carrier_fanout.py',word6,[]),('A-twelve','build_d4_hybrid.py',word12,['--problem',str(E/'A/D4-ROUTE-PROBLEM.json'),'--candidate',str(E/'A/D4-HYBRID-HEURISTIC.json')])]:
 dest=out/name;add(name,E/'A'/builder,['--repo',str(repo),'--out',str(dest)]+extra,dest/'WORD.json',word,True)
ccheck('C-six','fanout-review/check.py',word6,'fanout-review')
ccheck('C-twelve','d4-review/check.py',word12,'d4-review')
ccheck('C-native-residual','fanout-residual/check_residual.py',word6,'fanout-residual')
ccheck('C-last-shared','fanout-last-meeting-review/check_last_meeting.py',word6,'fanout-last-meeting-review')
ccheck('C-facet-application','facet-source-gate/check_facet_source.py',None,'facet-source-gate')
add('C-location',E/'C/wave2/check_location_gate.py',['--repo',str(repo),'--evidence',str(old),'--out',str(out/'C-location')],out/'C-location/LOCATION-GATE-RESULT.json',E/'C/wave2/output/LOCATION-GATE-RESULT.json')
for name in ['ordinary-character-gate','correct-character-prefix','component-augmentation-gate','forward-row-range-and-spectator-kernels']:
 dest=out/('B-'+name);add('B-'+name,E/'B'/name/'check.py',['--repo',str(repo),'--out',str(dest)],dest/'RESULT.json',E/'B'/name/'RESULT.json')
for name,author in [('character-review','ordinary-character-gate'),('kernel-review','correct-character-prefix'),('augmentation-review','component-augmentation-gate')]:
 dest=out/('R-'+name);args=['--author',str(E/'B'/author),'--out',str(dest)]
 if name!='character-review':args+=['--root-control',str(E/'R/character-review/check.py')]
 add('R-'+name,E/'R'/name/'check.py',args,dest/'RESULT.json',E/'R'/name/'RESULT.json')
for name in ['fanout-residual-review','last-shared-chart']:
 dest=out/('R-'+name);add('R-'+name,E/'R'/name/'check.py',['--repo',str(repo),'--word',str(word6),'--root-source',str(source),'--author',str(E/'C/fanout-residual/output/RESULT.json'),'--out',str(dest)],dest/'RESULT.json',E/'R'/name/'RESULT.json')
add('R-location',E/'R/location-review/check.py',['--repo',str(repo),'--word',str(old/'A/local-canonical9-source/WORD.json'),'--author',str(E/'C/wave2/output/LOCATION-GATE-RESULT.json'),'--root-source',str(source),'--out',str(out/'R-location')],out/'R-location/RESULT.json',E/'R/location-review/RESULT.json')
# A later independent reviewer is included automatically only when its frozen package is present.
spect=E/'C/spectator-review'
if spect.exists():
 add('C-spectator',spect/'check.py',['--package',str(E/'B/forward-row-range-and-spectator-kernels'),'--out',str(out/'C-spectator')],out/'C-spectator/RESULT.json',spect/'output/RESULT.json')
def run(task):
 name,script,args,actual,frozen,byte=task;proc=subprocess.run([sys.executable,'-B',str(script),*args],cwd=repo,capture_output=True,text=True)
 (out/(name+'.log')).write_text(proc.stdout+proc.stderr)
 if proc.returncode:raise RuntimeError(name+' failed: '+proc.stderr[-3000:])
 if byte:equal=actual.read_bytes()==frozen.read_bytes()
 else:
  x=json.loads(actual.read_text());y=json.loads(frozen.read_text())
  # Runtime version is recorded, but mathematical replay does not depend on spelling of a newer compatible version.
  x.pop('sympy_version',None);y.pop('sympy_version',None);equal=x==y
 if not equal:raise RuntimeError(name+' disagrees with frozen evidence')
 return {'name':name,'status':'PASS','comparison':'byte-identical-word'if byte else'exact-JSON-mathematical-receipt','script':str(script.relative_to(repo)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'result_sha256':hashlib.sha256(actual.read_bytes()).hexdigest()}
with ThreadPoolExecutor(max_workers=max(1,min(a.jobs,8)))as pool:results=list(pool.map(run,tasks))
report={'status':'PASS_S019_CP2_FOCUSED_REPRODUCTION','scope':'New source words, exact premises, independent proofs and controls; not a rerun of all inherited supplier/frontier suites.','checks':results}
(out/'REPRODUCTION.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status']);print(len(results),'scoped reproduction checks passed')
