#!/usr/bin/env python3
"""Rebuild S018 checkpoint4 controls without modifying frozen evidence."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
P=repo/'research/moonshot-005-program';S=P/'sessions/2026-11-16-S018';E=S/'checkpoint4-evidence';commands=[];comparisons=[]
def run(script,*args):
 cmd=[sys.executable,'-B',str(script),*map(str,args)];r=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if r.returncode:print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError(cmd)
 commands.append({'script':str(script.relative_to(repo)),'args':[str(x).replace(str(repo),'$REPO').replace(str(out),'$OUT') for x in args],'exit_code':r.returncode});print('PASS',script.name,flush=True)
def same(actual,frozen):
 b=frozen.read_bytes();assert actual.read_bytes()==b,('not byte identical',actual,frozen)
 comparisons.append({'frozen':str(frozen.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest(),'byte_identical':True})
d=out/'m0-pair55';run(E/'C/build_m0_pair_extension.py','--repo',repo,'--work',E,'--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'C/m0-pair55/{n}.json')
f=out/'masked55';run(E/'A/build_m0_masked_feedback.py','--repo',repo,'--word',d/'WORD.json','--purify','--out',f)
for n in ['WORD','RESULT']:same(f/f'{n}.json',E/f'A/m0-masked19-pure-pruned55/{n}.json')
r=out/'masked-review';run(E/'C/review_masked_m0.py','--repo',repo,'--work',E,'--out',r);same(r/'RESULT.json',E/'C/masked19-source-review/RESULT.json')
d=out/'mask-reset';run(E/'C/build_mask_preserving_reset.py','--repo',repo,'--work',E,'--out',d)
for n in ['OLD-WORD','RESET-WORD','SOURCE-WORD','LIBERATED-SOURCE-WORD','UNPREPARED-WORD','RESULT']:same(d/f'{n}.json',E/f'C/mask-preserving-reset/{n}.json')
r=out/'mask-reset-review.json';run(E/'R/mask-reset-review/check.py','--repo',repo,'--work',E,'--out',r);same(r,E/'R/mask-reset-review/RESULT.json')
r=out/'clean-first.json';run(E/'B/check_clean_first_column_square_gate-v1.py','--repo',repo,'--square-package',S/'checkpoint2-evidence/R/square-normalizer','--out',r);same(r,E/'B/CLEAN-FIRST-COLUMN-SQUARE-RESULT-v1.json')
r=out/'clean-first-review.json';run(E/'R/clean-first-review/check.py','--repo',repo,'--proof',E/'B/CLEAN-FIRST-COLUMN-SQUARE-GATE-v1.md','--out',r);same(r,E/'R/clean-first-review/RESULT.json')
r=out/'idle-first-review.json';run(E/'B/review_necessary_idle_first_column.py','--proof',E/'R/necessary-idle-first-column/PROOF.md','--out',r);same(r,E/'B/NECESSARY-IDLE-FIRST-REVIEW.json')
r=out/'all-clean.json';run(E/'B/check_all_clean_first_column_gate-v1.py','--out',r);same(r,E/'B/ALL-CLEAN-FIRST-COLUMN-RESULT-v1.json')
r=out/'all-clean-review.json';run(E/'R/all-clean-review/check.py','--repo',repo,'--proof',E/'B/ALL-CLEAN-FIRST-COLUMN-GATE-v1.md','--out',r);same(r,E/'R/all-clean-review/RESULT.json')
d=out/'nonclean-wrapper';run(E/'R/nonclean-reduction-review/check.py','--repo',repo,'--proof',E/'B/NONCLEAN-IDLE-REDUCTION-v1.md','--out',d)
for n in ['C-WORD','C-INVERSE-WORD','Q-WORD','Q-INVERSE-WORD','RESULT']:same(d/f'{n}.json',E/f'R/nonclean-reduction-review/control/{n}.json')
r=out/'inverse-cut.json';run(E/'B/check_inverse_cut_support_gate-v2.py','--repo',repo,'--out',r);same(r,E/'B/INVERSE-CUT-SUPPORT-RESULT-v2.json')
r=out/'inverse-cut-review.json';run(E/'R/inverse-cut-review/check.py','--repo',repo,'--proof',E/'B/INVERSE-CUT-SUPPORT-GATE-v2.md','--out',r);same(r,E/'R/inverse-cut-review/RESULT.json')
report={'status':'PASS_S018_CHECKPOINT4_REPRODUCTION','commands':commands,'byte_comparisons':comparisons,'scope':'Universal proofs separately reviewed. Actual unknown-source acquisition, full222 native words, chronology/custody, distinct reset interfaces, exact invoices, faithful-width ordinary gates and paid wrapper controls. No complete supplier or new kappa.'}
(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons')
