#!/usr/bin/env python3
"""Rebuild S018 checkpoint5 controls without modifying frozen evidence."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
P=repo/'research/moonshot-005-program';S=P/'sessions/2026-11-16-S018';E=S/'checkpoint5-evidence';commands=[];comparisons=[]
def run(script,*args):
 cmd=[sys.executable,'-B',str(script),*map(str,args)];r=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if r.returncode:print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError(cmd)
 commands.append({'script':str(script.relative_to(repo)),'args':[str(x).replace(str(repo),'$REPO').replace(str(out),'$OUT')for x in args],'exit_code':r.returncode});print('PASS',script.name,flush=True)
def same(actual,frozen):
 b=frozen.read_bytes();assert actual.read_bytes()==b,('not byte identical',actual,frozen)
 comparisons.append({'frozen':str(frozen.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest(),'byte_identical':True})
d=out/'lower57';run(E/'A/build_lower_history.py','--repo',repo,'--word',E/'A/d4-cohort-paid46/WORD.json','--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/lower-history57-paid/{n}.json')
f=out/'lower59';run(E/'A/extend_local_pairs.py','--repo',repo,'--word',d/'WORD.json','--out',f)
for n in ['WORD','RESULT']:same(f/f'{n}.json',E/f'A/lower-history59-paid/{n}.json')
r=out/'lower-controls.json';run(E/'A/check_lower_history.py','--repo',repo,'--word',f/'WORD.json','--out',r);same(r,E/'A/lower-history59-paid/CONTROLS.json')
d=out/'lower-review';run(E/'C/review_lower_histories.py','--repo',repo,'--work',E,'--out',d)
for n in ['PAID57-RESULT','PAID59-RESULT']:same(d/f'{n}.json',E/f'C/lower-history-review/{n}.json')
d=out/'seven-cut';run(E/'R/local-cut-descents/check.py','--repo',repo,'--word',E/'A/lower-history59-paid/WORD.json','--proof',E/'R/local-cut-descents/PROOF.md','--out',d)
for n in ['RESULT','NONLOCAL-SOURCE-CONTROL-WORD']:same(d/f'{n}.json',E/f'R/local-cut-descents/control/{n}.json')
d=out/'seven-cut-review';run(E/'C/review_local_cut_descents.py','--repo',repo,'--work',E,'--out',d)
for n in ['RESULT','NONLOCAL-CUT-CONTROL','SEVEN-DESCENT-CONTROL','ORTHOGONAL-PAIR-CONTROL']:same(d/f'{n}.json',E/f'C/local-cut-review/{n}.json')
for bits,folder in [('11111','shared-proper-five46'),('10101','shared-proper-five46-control10101')]:
 d=out/folder;run(E/'A/build_shared_proper_masks.py','--repo',repo,'--bits',bits,'--out',d)
 for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/{folder}/{n}.json')
r=out/'shared-controls.json';run(E/'A/check_shared_proper_masks.py','--repo',repo,'--word',E/'A/shared-proper-five46/WORD.json','--out',r);same(r,E/'A/shared-proper-five46/CONTROLS.json')
d=out/'shared-review';run(E/'C/review_shared_proper_five.py','--repo',repo,'--work',E,'--out',d);same(d/'RESULT.json',E/'C/shared-proper-five-review/RESULT.json')
d=out/'initial-chart';run(E/'R/initial-chart-cut/check.py','--repo',repo,'--work',E,'--proof',E/'R/initial-chart-cut/PROOF.md','--out',d)
for n in ['RESULT','PAID59-ALL111-WORD','FIVE46-ALL111-WORD','NATIVE-CACHED57-WORD']:same(d/f'{n}.json',E/f'R/initial-chart-cut/control/{n}.json')
d=out/'initial-chart-review';run(E/'C/review_initial_chart_cut.py','--repo',repo,'--work',E,'--out',d);same(d/'RESULT.json',E/'C/initial-chart-cut-review/RESULT.json')
r=out/'g512.json';run(E/'B/check_g512_whole_interface_gate-v1.py','--repo',repo,'--out',r);same(r,E/'B/G512-WHOLE-INTERFACE-RESULT-v1.json')
r=out/'g512-review.json';run(E/'R/g512-review/check.py','--repo',repo,'--proof',E/'B/G512-WHOLE-INTERFACE-GATE-v1.md','--out',r);same(r,E/'R/g512-review/RESULT.json')
report={'status':'PASS_S018_CHECKPOINT5_REPRODUCTION','commands':commands,'byte_comparisons':comparisons,'scope':'Universal proofs separately reviewed. Actual multistage history, unknown-source corrections, complete native222 columns, fixed-cut acyclic transcript floors, literal all111 sharp controls, actual native-cache57 repair and full512 coefficient-algebra hypotheses. No complete target-compatible supplier or new kappa.'}
(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons')
