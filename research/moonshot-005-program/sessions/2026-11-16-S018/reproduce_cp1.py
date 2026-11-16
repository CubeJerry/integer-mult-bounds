#!/usr/bin/env python3
"""Reproduce the four S018 CP1 packages without changing frozen evidence."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
P=repo/'research/moonshot-005-program';S=P/'sessions/2026-11-16-S018';R=S/'root-review'
proj=P/'results/bit-protected-source-projection';hub=P/'results/bit-full-hub-programmable-source'
rest=P/'results/bit-collective-carrier-restoration';comp=P/'results/complex-coherent-diagonal-exclusion'
commands=[];comparisons=[]
def run(script,*args):
 cmd=[sys.executable,'-B',str(script),*map(str,args)]
 r=subprocess.run(cmd,cwd=repo,text=True,capture_output=True)
 if r.returncode:
  print(r.stdout);print(r.stderr,file=sys.stderr);raise RuntimeError(cmd)
 commands.append({'script':str(script.relative_to(repo)),'args':[str(x).replace(str(repo),'$REPO').replace(str(out),'$OUT')for x in args],'exit_code':r.returncode})
 print('PASS',script.name,flush=True)
def same(actual,frozen):
 aa=actual.read_bytes();bb=frozen.read_bytes()
 if aa!=bb:raise AssertionError(('not byte-identical',str(actual),str(frozen)))
 comparisons.append({'frozen':str(frozen.relative_to(repo)),'sha256':hashlib.sha256(bb).hexdigest(),'byte_identical':True})
run(proj/'author/release_projection.py','--repo',repo,'--out',out/'projection','--maximal')
for name in ['WORD.json','RESULT.json']:same(out/'projection'/name,proj/'author'/name)
run(proj/'author/price_projection.py','--result',out/'projection/RESULT.json','--out',out/'projection/PRICE.json')
same(out/'projection/PRICE.json',proj/'author/PRICE.json')
run(hub/'author/build_full_hub.py','--repo',repo,'--out',out/'full-hub')
for name in ['WORD.json','RESULT.json']:same(out/'full-hub'/name,hub/'author/full-hub'/name)
run(hub/'author/build_arbitrary_retention.py','--repo',repo,'--base',out/'full-hub/WORD.json','--out',out/'arbitrary-six')
for name in ['WORD.json','RESULT.json']:same(out/'arbitrary-six'/name,hub/'author/arbitrary-six'/name)
for name,word,frozen in [('projection',proj/'author/WORD.json',proj/'root-review/REPLAY.json'),('full-hub',hub/'author/full-hub/WORD.json',hub/'root-review/FULL-HUB.json'),('arbitrary-six',hub/'author/arbitrary-six/WORD.json',hub/'root-review/ARBITRARY-SIX.json')]:
 target=out/(name+'-root.json');run(R/'review_current.py','--repo',repo,'--word',word,'--out',target);same(target,frozen)
run(R/'review_projection.py','--repo',repo,'--word',proj/'author/WORD.json','--out',out/'interface.json')
same(out/'interface.json',proj/'root-review/INTERFACE.json')
run(R/'review_source_families.py','--repo',repo,'--hub',hub/'author/full-hub/WORD.json','--family',hub/'author/arbitrary-six/WORD.json','--out',out/'source-family.json')
same(out/'source-family.json',hub/'root-review/SOURCE-FAMILY.json')
run(rest/'independent-review/check.py','--proof',rest/'PROOF.md','--out',out/'restoration.json')
same(out/'restoration.json',rest/'independent-review/RESULT.json')
run(comp/'author/check_pivot_propagation.py','--repo',repo,'--out',out/'complex-author.json')
same(out/'complex-author.json',comp/'author/RESULT.json')
run(R/'review_pivot.py','--proof',comp/'author/PIVOT-PROPAGATION.md','--out',out/'complex-root.json')
same(out/'complex-root.json',comp/'root-review/RESULT.json')
report={'status':'PASS_S018_CHECKPOINT1_REPRODUCTION','commands':commands,'byte_comparisons':comparisons,'claims':'Universal proofs separately reviewed; command execution alone is not an independent theorem. Three literal words, source interfaces, masks and prices checked; restoration and complex proofs reviewed; no supplier or new kappa.'}
(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(commands),'commands;',len(comparisons),'byte comparisons',flush=True)
