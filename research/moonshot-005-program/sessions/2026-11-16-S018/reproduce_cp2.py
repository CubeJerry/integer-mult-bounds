#!/usr/bin/env python3
"""Rebuild S018 checkpoint2 evidence without changing frozen files."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
P=repo/'research/moonshot-005-program';S=P/'sessions/2026-11-16-S018';E=S/'checkpoint2-evidence';commands=[];comparisons=[]
def run(script,*args):
 cmd=[sys.executable,'-B',str(script),*map(str,args)];r=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if r.returncode:print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError(cmd)
 commands.append({'script':str(script.relative_to(repo)),'args':[str(x).replace(str(repo),'$REPO').replace(str(out),'$OUT')for x in args],'exit_code':r.returncode});print('PASS',script.name,flush=True)
def same(actual,frozen):
 b=frozen.read_bytes();assert actual.read_bytes()==b,('not byte identical',actual,frozen)
 comparisons.append({'frozen':str(frozen.relative_to(repo)),'sha256':hashlib.sha256(b).hexdigest(),'byte_identical':True})
run(E/'C/release_conduits.py','--repo',repo,'--out',out/'released78')
for n in ['WORD.json','RESULT.json']:same(out/'released78'/n,E/'C/released78'/n)
run(E/'C/price_projection.py','--result',out/'released78/RESULT.json','--out',out/'released78/PRICE.json');same(out/'released78/PRICE.json',E/'C/released78/PRICE.json')
for num,base in [(73,P/'results/bit-protected-source-projection/author/WORD.json'),(78,out/'released78/WORD.json')]:
 folder=out/f'pruned{num}';script='prune_projected.py'if num==73 else'prune_projected78.py'
 run(E/'A'/script,'--repo',repo,'--base',base,'--out',folder)
 for n in ['WORD.json','RESULT.json']:same(folder/n,E/f'A/pruned{num}'/n)
 target=out/f'PRUNED{num}-REVIEW.json';run(E/f'C/review_pruned{num}.py','--repo',repo,'--base',base,'--word',folder/'WORD.json','--out',target);same(target,E/f'C/PRUNED{num}-REVIEW-RESULT.json')
run(E/'R/review_conduits.py','--repo',repo,'--word',out/'released78/WORD.json','--pruned',out/'pruned78/WORD.json','--pruned-result',out/'pruned78/RESULT.json','--proof',E/'C/CONDUIT-EXTENSION.md','--out',out/'conduits-review.json');same(out/'conduits-review.json',E/'R/CONDUIT78-REVIEW.json')
for feedback in [False,True]:
 label='control-feedback'if feedback else'control';script='build_feedback_control.py'if feedback else'build_control.py'
 run(E/'R/cut-reset'/script,'--repo',repo,'--word',out/'pruned78/WORD.json','--source-result',out/'pruned78/RESULT.json','--out',out/'reset'/label)
 for n in ['OLD-WORD.json','RESET-WORD.json','RESULT.json']:same(out/'reset'/label/n,E/'R/cut-reset'/label/n)
 target=out/('reset-feedback-review'if feedback else'reset-review');args=['--repo',repo,'--work',E,'--out',target]+(['--feedback']if feedback else[])
 run(E/'C/review_cut_reset.py',*args);same(target/'RESULT.json',E/'C'/('cut-reset-feedback-review'if feedback else'cut-reset-review')/'RESULT.json')
for feedback in [False,True]:
 label='normalization-feedback-control'if feedback else'normalization-control';script='ground_output_feedback_control.py'if feedback else'ground_output_normalization.py';folder=out/label
 run(E/'C'/script,'--repo',repo,'--out',folder)
 for n in ['WORD.json','UNNORMALIZED-WORD.json','RESULT.json']:same(folder/n,E/'C'/label/n)
 target=out/(label+'-review.json');run(E/'R/review_ground_normalization.py','--repo',repo,'--word',folder/'WORD.json','--raw',folder/'UNNORMALIZED-WORD.json','--proof',E/'C/GROUND-OUTPUT-NORMALIZATION.md','--out',target);same(target,E/'R'/('GROUND-FEEDBACK-REVIEW.json'if feedback else'GROUND-NORMALIZATION-REVIEW.json'))
run(E/'B/check_square_controls.py','--repo',repo,'--out',out/'Boolean-square.json');same(out/'Boolean-square.json',E/'B/SQUARE-CONTROLS-RESULT.json')
run(E/'R/square-normalizer/check.py','--repo',repo,'--proof',E/'R/square-normalizer/PROOF.md','--out',out/'complete-square.json');same(out/'complete-square.json',E/'R/square-normalizer/RESULT.json')
run(E/'B/review_square_normalizer.py','--root-package',E/'R/square-normalizer','--out',out/'complete-square-review.json');same(out/'complete-square-review.json',E/'B/SQUARE-NORMALIZER-INDEPENDENT-REVIEW.json')
run(E/'R/review_square_controls.py','--proof',E/'B/SOURCE-SQUARE-CONTROLS.md','--classification-result',out/'complete-square.json','--out',out/'Boolean-square-review.json');same(out/'Boolean-square-review.json',E/'R/SQUARE-CONTROLS-REVIEW.json')
report={'status':'PASS_S018_CHECKPOINT2_REPRODUCTION','commands':commands,'byte_comparisons':comparisons,'scope':'Universal statements separately reviewed. Native all222-column words, actual custody/geometry, full partial ledgers, exact source phases and explicit recipes checked. Neither strict supplier nor new complete kappa is established.'};(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons')
