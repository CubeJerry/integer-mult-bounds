#!/usr/bin/env python3
"""Rebuild S018 checkpoint6 controls without modifying frozen evidence."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
P=repo/'research/moonshot-005-program';S=P/'sessions/2026-11-16-S018';E=S/'checkpoint6-evidence';commands=[];comparisons=[]
def run(script,*args):
 cmd=[sys.executable,'-B',str(script),*map(str,args)];r=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if r.returncode:print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError(cmd)
 commands.append({'script':str(script.relative_to(repo)),'args':[str(x).replace(str(repo),'$REPO').replace(str(out),'$OUT')for x in args],'exit_code':r.returncode});print('PASS',script.name,flush=True)
def same(actual,frozen):
 b=frozen.read_bytes();assert actual.read_bytes()==b,('not byte identical',actual,frozen)
 comparisons.append({'frozen':str(frozen.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest(),'byte_identical':True})


d=out/'local-source';run(E/'A/build_local_canonical_source.py','--repo',repo,'--work',E,'--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/local-canonical9-source/{n}.json')
r=d/'CONTROLS.json';run(E/'A/check_local_canonical_source.py','--repo',repo,'--work',E,'--word',d/'WORD.json','--out',r);same(r,E/'A/local-canonical9-source/CONTROLS.json')
d=out/'local-review';run(E/'C/review_local_canonical9_source.py','--repo',repo,'--work',E,'--out',d);same(d/'RESULT.json',E/'C/local-canonical9-source-review/RESULT.json')
r=out/'local-root.json';run(E/'R/local-canonical-review/check.py','--repo',repo,'--word',E/'A/local-canonical9-source/WORD.json','--out',r);same(r,E/'R/local-canonical-review/RESULT.json')
r=out/'pure-v3.json';run(E/'B/check_pure_prefix_image_gate-v3.py','--repo',repo,'--out',r);same(r,E/'B/PURE-PREFIX-IMAGE-RESULT-v3.json')
report={'status':'PASS_S018_CHECKPOINT6_EARLY_ACQUISITION_SUPPLEMENT','commands':commands,'byte_comparisons':comparisons,'scope':'Exact early F74 acquisition with actual raw48/native63/nine canonical modes, independent native and proof reviews,417 author omission controls, retained8-descent floor now below allowance, plus v3 proof-bound2048 complex controls. No physical63-receiver completion or kappa.'}
(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons')
