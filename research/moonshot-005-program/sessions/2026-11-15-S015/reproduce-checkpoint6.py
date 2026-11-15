#!/usr/bin/env python3
"""Rebuild and review checkpoint6 evidence in a separate output directory."""
import argparse,concurrent.futures,hashlib,json,shutil,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',choices=['paired','collector','gate','commuting']);a=ap.parse_args()
repo=a.repo.resolve();P=repo/'research/moonshot-005-program/results';R=a.out.resolve();R.mkdir(parents=True,exist_ok=True)
commands=[];comparisons=[]
def cmd(args):
 argv=['python3','-B']+[str(x)for x in args];r=subprocess.run(argv,cwd=repo,capture_output=True,text=True)
 commands.append({'argv':argv,'exit_code':r.returncode});assert r.returncode==0,(argv,r.stdout[-2000:],r.stderr[-3000:])
def compare(x,y):
 kind='byte_identical'
 if x.read_bytes()!=y.read_bytes():
  assert 'bit-paired-flag-source/independent-c/output' in str(x) and x.name.endswith('-HISTORY.json'),(str(x),str(y),'unallowed difference')
  aa=json.loads(x.read_text());bb=json.loads(y.read_text())
  ca=aa.pop('coverage');cb=bb.pop('coverage')
  assert {k:sorted(v)for k,v in ca.items()}=={k:sorted(v)for k,v in cb.items()} and aa==bb
  kind='unordered_coverage_lists_identical_as_sets_all_other_fields_exact'
 comparisons.append({'expected':str(x.relative_to(P)),'reproduced':str(y.relative_to(R)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'reproduced_sha256':hashlib.sha256(y.read_bytes()).hexdigest(),'comparison':kind})
def paired():
 p=P/'bit-paired-flag-source';o=R/'paired';o.mkdir(exist_ok=True)
 cmd([p/'author/build.py','--repo',repo,'--out',o/'output'])
 for n in ['WORD.json','CLOSED-WORD.json']:compare(p/'author/output'/n,o/'output'/n)
 cmd([p/'author/check.py','--repo',repo,'--package',o,'--out',o/'author-check'])
 for f in (p/'author/verification').glob('*.json'):compare(f,o/'author-check'/f.name)
 cmd([p/'author/capacity.py','--word',o/'output/WORD.json','--out',o/'capacity.json']);compare(p/'author/CAPACITY.json',o/'capacity.json')
 cmd([p/'independent-c/check.py','--repo',repo,'--author',o,'--out',o/'review'])
 for f in (p/'independent-c/output').glob('*.json'):
  if f.name!='PRICE.json':compare(f,o/'review'/f.name)
 shutil.copy2(p/'independent-c/price.py',o/'price.py');cmd([o/'price.py']);compare(p/'independent-c/output/PRICE.json',o/'output/PRICE.json')
def collector():
 p=P/'bit-facet-collector-source';o=R/'collector';o.mkdir(exist_ok=True)
 source=P/'bit-two-copy-cohort-source/conditional-origin/output/WORD.json'
 cmd([p/'author/build.py','--repo',repo,'--source',source,'--out',o/'output'])
 for n in ['WORD.json','CLOSED-WORD.json']:compare(p/'author/output'/n,o/'output'/n)
 cmd([p/'author/check.py','--repo',repo,'--word-dir',o/'output','--out',o/'author-check'])
 for f in (p/'author/verification').glob('*.json'):
  if f.name not in ['PRICE.json','CODE-DIAGNOSTIC.json']:compare(f,o/'author-check'/f.name)
 cmd([p/'author/diagnose.py','--repo',repo,'--word',o/'output/WORD.json','--out',o/'diagnostic.json']);compare(p/'author/verification/CODE-DIAGNOSTIC.json',o/'diagnostic.json')
 shutil.copy2(p/'author/price.py',o/'price.py');cmd([o/'price.py']);compare(p/'author/verification/PRICE.json',o/'verification/PRICE.json')
 cmd([p/'independent-a/check.py','--repo',repo,'--package',o,'--predecessor',P/'bit-two-copy-cohort-source/author/output/WORD.json','--out',o/'review'])
 for f in (p/'independent-a/output').glob('*.json'):compare(f,o/'review'/f.name)
def gate():
 p=P/'bit-packed-three-duty-gate';o=R/'gate';o.mkdir(exist_ok=True)
 source=P/'bit-two-copy-cohort-source/author/output/WORD.json'
 cmd([p/'author/check.py','--repo',repo,'--source',source,'--out',o/'author.json']);compare(p/'author/CERTIFICATE.json',o/'author.json')
 cmd([p/'review-root/check.py','--repo',repo,'--certificate',o/'author.json','--out',o/'review.json']);compare(p/'review-root/RESULT.json',o/'review.json')
 shutil.copy2(p/'budget-root/check.py',o/'budget.py');cmd([o/'budget.py']);compare(p/'budget-root/RESULT.json',o/'RESULT.json')
 # Preserve the independent reviewer's original relative source layout.
 layout=o/'budget-review-layout';rr=layout/'worker-a/review-two-copy-budget';hh=layout/'worker-a/paired-flag-source';bb=layout/'root/two-copy-budget'
 for d in [rr,hh,bb]:d.mkdir(parents=True,exist_ok=True)
 shutil.copy2(p/'budget-independent-a/check.py',rr/'check.py')
 shutil.copy2(P/'bit-paired-flag-source/author/check.py',hh/'check.py')
 for n in ['check.py','RESULT.json']:shutil.copy2(p/'budget-root'/n,bb/n)
 cmd([rr/'check.py']);compare(p/'budget-independent-a/RESULT.json',rr/'RESULT.json')
def commuting():
 p=P/'complex-commuting-rank-conservation';o=R/'commuting';o.mkdir(exist_ok=True)
 for script,result in [('check_pauli_split.py','PAULI-SPLIT-RESULT.json'),('check_conservation.py','CONSERVATION-RESULT.json')]:
  cmd([p/'author'/script,'--repo',repo,'--out',o/result]);compare(p/'author'/result,o/result)
 cmd([p/'review-root/check.py','--out',o/'review.json']);compare(p/'review-root/RESULT.json',o/'review.json')
 cmd([p/'faithfulness-independent-b/check.py','--proof',p/'review-root/FAITHFULNESS-SUPPLEMENT.md','--out',o/'faithfulness.json']);compare(p/'faithfulness-independent-b/RESULT.json',o/'faithfulness.json')
errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
 fs={ex.submit(f):f.__name__ for f in [paired,collector,gate,commuting] if a.only is None or f.__name__==a.only}
 for f in concurrent.futures.as_completed(fs):
  try:f.result();print('PASS',fs[f],flush=True)
  except Exception as e:errors.append((fs[f],str(e)));print('FAIL',fs[f],str(e),flush=True)
(R/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');(R/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n')
assert not errors,errors
print(json.dumps({'status':'PASS_CP6_PORTABLE_REPRODUCTION','commands':len(commands),'json_comparisons':len(comparisons),'byte_identical_json':sum(x['comparison']=='byte_identical'for x in comparisons)}))
