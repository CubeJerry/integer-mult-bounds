#!/usr/bin/env python3
"""Rebuild S018 checkpoint3 controls without changing frozen evidence."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
P=repo/'research/moonshot-005-program';S=P/'sessions/2026-11-16-S018';E=S/'checkpoint3-evidence';commands=[];comparisons=[]
def run(script,*args):
 cmd=[sys.executable,'-B',str(script),*map(str,args)];r=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if r.returncode:print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError(cmd)
 commands.append({'script':str(script.relative_to(repo)),'args':[str(x).replace(str(repo),'$REPO').replace(str(out),'$OUT')for x in args],'exit_code':r.returncode});print('PASS',script.name,flush=True)
def same(actual,frozen):
 b=frozen.read_bytes();assert actual.read_bytes()==b,('not byte identical',actual,frozen)
 comparisons.append({'frozen':str(frozen.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest(),'byte_identical':True})
for base,num in [('pruned78',54),('paid46',111)]:
 d=out/('d4-cohort-'+base)
 run(E/'A/build_d4_cohort.py','--repo',repo,'--base',base,'--out',d)
 for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/d4-cohort-{base}/{n}.json')
 run(E/'A/check_d4_cohort_controls.py','--repo',repo,'--word',d/'WORD.json','--out',d/'CONTROLS.json');same(d/'CONTROLS.json',E/f'A/d4-cohort-{base}/CONTROLS.json')
 run(E/'A/price_d4_cohort.py','--result',d/'RESULT.json','--out',d/'PRICE.json');same(d/'PRICE.json',E/f'A/d4-cohort-{base}/PRICE.json')
 r=out/('d4-'+base+'-review');run(E/'C/review_d4_cohort.py','--repo',repo,'--work',E,'--base',base,'--out',r);same(r/'RESULT.json',E/f'C/d4-{base}-review/RESULT.json')
 z=out/f'd4-reset{num}';run(E/'A/build_d4_reset_benchmark.py','--repo',repo,'--word',d/'WORD.json','--out',z)
 for n in ['WORD','RESULT']:same(z/f'{n}.json',E/f'A/d4-reset{num}/{n}.json')
 review=out/f'd4-reset{num}-review.json';run(S/'root-review/review_current.py','--repo',repo,'--word',z/'WORD.json','--out',review);same(review,E/f'R/D4-RESET{num}-REVIEW.json')
 f=out/('d4-feedback-'+base);run(E/'A/build_d4_feedback.py','--repo',repo,'--word',d/'WORD.json','--out',f)
 for n in ['WORD','RESULT']:same(f/f'{n}.json',E/f'A/d4-feedback-{base}/{n}.json')
 ctrl=out/('d4-feedback-'+base+'-controls');run(E/'A/check_d4_feedback.py','--repo',repo,'--word',f/'WORD.json','--out',ctrl);same(ctrl/'CONTROLS.json',E/f'A/d4-feedback-{base}/CONTROLS.json')
 same(ctrl/'PRICE.json',E/f'A/d4-feedback-{base}/PRICE.json')
 r=out/('d4-feedback-'+base+'-review');run(E/'C/review_d4_feedback.py','--repo',repo,'--work',E,'--base',base,'--out',r);same(r/'RESULT.json',E/f'C/d4-feedback-{base}-review/RESULT.json')
z=out/'y-skeleton-control';run(E/'C/build_y_skeleton_control.py','--repo',repo,'--work',E,'--out',z)
for n in ['OLD-WORD','RESET-WORD','UNPREPARED-WORD','LATE-PRELOAD-NEGATIVE','RESULT']:same(z/f'{n}.json',E/f'C/y-skeleton-control/{n}.json')
r=out/'y-skeleton-review.json';run(E/'R/y-skeleton-review/check.py','--repo',repo,'--work',E,'--out',r);same(r,E/'R/y-skeleton-review/RESULT.json')
r=out/'active-first.json';run(E/'R/active-first-gate/check.py','--repo',repo,'--proof',E/'R/active-first-gate/PROOF.md','--out',r);same(r,E/'R/active-first-gate/RESULT.json')
r=out/'active-first-review.json';run(E/'B/review_active_first_gate.py','--root-package',E/'R/active-first-gate','--out',r);same(r,E/'B/ACTIVE-FIRST-INDEPENDENT-REVIEW.json')
r=out/'middle-pivot.json';run(E/'B/check_middle_pivot_all_ordinary.py','--repo',repo,'--out',r);same(r,E/'B/MIDDLE-PIVOT-ALL-ORDINARY-RESULT.json')
r=out/'middle-pivot-review.json';run(E/'R/middle-pivot-review/check.py','--repo',repo,'--proof',E/'B/MIDDLE-PIVOT-ALL-ORDINARY-GATE.md','--out',r);same(r,E/'R/middle-pivot-review/RESULT.json')
d=out/'noncommuting-compiler';run(E/'R/noncommuting-compiler/check.py','--repo',repo,'--proof',E/'R/noncommuting-compiler/PROOF.md','--out',d)
for n in ['RESULT','EXAMPLE-WORD','EXAMPLE-INVERSE-WORD','GENERAL-WORD','GENERAL-INVERSE-WORD']:same(d/f'{n}.json',E/f'R/noncommuting-compiler/control/{n}.json')
d=out/'noncommuting-compiler-review';run(E/'C/review_noncommuting_compiler.py','--repo',repo,'--work',E,'--out',d)
for n in ['RESULT','GAUSSIAN-CONTROL-WORD']:same(d/f'{n}.json',E/f'C/noncommuting-compiler-review/{n}.json')
report={'status':'PASS_S018_CHECKPOINT3_REPRODUCTION','commands':commands,'byte_comparisons':comparisons,'scope':'Universal proofs separately reviewed. Native all222-column words, exact custody and geometry, full partial invoices, literal complex phases, all-width algebraic certificates and paid ordinary words checked. No complete supplier or new kappa.'};(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons')
