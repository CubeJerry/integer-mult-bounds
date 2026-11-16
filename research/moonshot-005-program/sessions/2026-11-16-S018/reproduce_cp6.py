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

d=out/'mode48';run(E/'A/build_mode_preserving_d4.py','--repo',repo,'--word',E/'A/shared-proper-five46/WORD.json','--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/mode-preserving48/{n}.json')
f=out/'mode50';run(E/'A/extend_local_pairs.py','--repo',repo,'--word',d/'WORD.json','--out',f)
for n in ['WORD','RESULT']:same(f/f'{n}.json',E/f'A/mode-preserving50/{n}.json')
r=out/'mode-controls.json';run(E/'A/check_mode_preserving.py','--repo',repo,'--word',f/'WORD.json','--out',r);same(r,E/'A/mode-preserving50/CONTROLS.json')
d=out/'mode-review';run(E/'C/review_mode_preserving50.py','--repo',repo,'--work',E,'--out',d)
for n in ['RESULT48','RESULT50']:same(d/f'{n}.json',E/f'C/mode-preserving50-review/{n}.json')
d=out/'ascending';run(E/'A/build_ascending_corrections.py','--repo',repo,'--word',E/'A/pruned78/WORD.json','--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/ascending-canonical3/{n}.json')
r=out/'ascending-controls.json';run(E/'A/check_ascending_corrections.py','--repo',repo,'--word',d/'WORD.json','--out',r);same(r,E/'A/ascending-canonical3/CONTROLS.json')
f=out/'native65';run(E/'A/add_ascending_native_bank.py','--repo',repo,'--word',d/'WORD.json','--out',f)
for n in ['WORD','RESULT']:same(f/f'{n}.json',E/f'A/ascending-canonical3-native65/{n}.json')
r=out/'static-closure.json';run(E/'A/audit_ascending_static.py','--repo',repo,'--word',d/'WORD.json','--out',r);same(r,E/'A/ascending-canonical3/OPTIMISTIC-CLOSURE.json')
d=out/'ascending-review';run(E/'C/review_ascending_corrections.py','--repo',repo,'--work',E,'--out',d);same(d/'RESULT.json',E/'C/ascending-corrections-review/RESULT.json')
d=out/'reset-source';run(E/'C/build_canonical3_reset_source.py','--repo',repo,'--work',E,'--out',d)
for n in ['LIBERATED-CACHED48-WORD','MATCHED-CUT-WORD','RESULT']:same(d/f'{n}.json',E/f'C/canonical3-reset-source/{n}.json')
d=out/'reset-control';run(E/'C/build_canonical3_reset_control.py','--work',E,'--out',d)
for n in ['OLD-CONTROL-WORD','RESET-CONTROL-WORD','MISSING-PRELOAD-WORD','RESULT']:same(d/f'{n}.json',E/f'C/canonical3-reset-control/{n}.json')


d=out/'reset-review';run(E/'A/review_canonical3_reset.py','--repo',repo,'--work',E,'--out',d)
for n in ['RESULT','MANIFEST']:same(d/f'{n}.json',E/f'A/canonical3-reset-review/{n}.json')
d=out/'native-static-review';run(E/'C/review_ascending_native_static.py','--repo',repo,'--work',E,'--out',d);same(d/'RESULT.json',E/'C/ascending-native-static-review/RESULT.json')
d=out/'first49';run(E/'C/build_first_unknown49.py','--repo',repo,'--work',E,'--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'C/first-unknown49/{n}.json')
r=out/'first49-root.json';run(E/'R/first-unknown-review/check.py','--repo',repo,'--work',E,'--out',r);same(r,E/'R/first-unknown-review/RESULT.json')
d=out/'canonical9';run(E/'A/build_canonical9_source.py','--repo',repo,'--work',E,'--out',d)
for n in ['WORD','RESULT']:same(d/f'{n}.json',E/f'A/canonical9-source/{n}.json')
r=d/'CONTROLS.json';run(E/'A/check_canonical9_source.py','--repo',repo,'--word',d/'WORD.json','--out',r)
for n in ['CONTROLS','J8-CUT-GATE']:same(d/f'{n}.json',E/f'A/canonical9-source/{n}.json')
r=out/'canonical9-root.json';run(E/'R/canonical-augmentation/check.py','--repo',repo,'--word',d/'WORD.json','--out',r);same(r,E/'R/canonical-augmentation/RESULT.json')
r=out/'pure-prefix.json';run(E/'B/check_pure_prefix_image_gate-v2.py','--repo',repo,'--out',r);same(r,E/'B/PURE-PREFIX-IMAGE-RESULT-v2.json')
d=out/'pure-prefix-root';run(E/'R/pure-prefix-review/check.py','--proof',E/'B/PURE-PREFIX-IMAGE-GATE-v2.md','--out',d)
for n in ['RESULT','ORDINARY-WORDS']:same(d/f'{n}.json',E/f'R/pure-prefix-review/{n}.json')
r=out/'aligned-independent.json';run(E/'B/check_aligned_selective_component-v2.py','--work',E,'--out',r);same(r,E/'B/ALIGNED-SELECTIVE-COMPONENT-RESULT-v2.json')
d=out/'residue';run(E/'B/check_residue_selective_component-v1.py','--work',E,'--out',d)
for n in ['WORDS','RESULT']:same(d/f'{n}.json',E/f'B/residue-selective-v1/{n}.json')
r=out/'residue-root.json';run(E/'R/residue-review/check.py','--work',E,'--out',r);same(r,E/'R/residue-review/RESULT.json')

d=out/'canonical9-review';run(E/'C/review_canonical9_source.py','--repo',repo,'--work',E,'--out',d);same(d/'RESULT.json',E/'C/canonical9-source-review/RESULT.json')

report={'status':'PASS_S018_CHECKPOINT6_REPRODUCTION','commands':commands,'byte_comparisons':comparisons,'scope':'Universal proofs independently reviewed separately. Mode-preserving earlier decodes, actual ascending-original corrections and57 binary masks, native65 captures and fixed static closure, actual cached48 reset and known-column repairs, pure-prefix obstruction and aligned rank4 component with literal ordinary inverses. No complete target-compatible supplier or new kappa.'}
(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons')
