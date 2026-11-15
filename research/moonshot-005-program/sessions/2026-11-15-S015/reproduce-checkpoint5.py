#!/usr/bin/env python3
"""Portable reproduction of all checkpoint5 packages and exact certificate comparison."""
from pathlib import Path
import argparse,subprocess,concurrent.futures,json,hashlib,shutil
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();P=repo/'research/moonshot-005-program/results';R=a.out.resolve();R.mkdir(parents=True,exist_ok=True)
base=P/'bit-delayed-mixed-feedback/author/output/WORD.json';assert base.exists()
commands=[];comparisons=[]
def cmd(args):
 a=['python3','-B']+[str(x)for x in args];z=subprocess.run(a,cwd=repo,capture_output=True,text=True);commands.append({'argv':a,'exit_code':z.returncode});assert z.returncode==0,(a,z.stdout[-2000:],z.stderr[-3000:]);return z.stdout
def compare(x,y):
 kind='byte_identical';detail=[]
 if x.read_bytes()!=y.read_bytes():
  aa=json.loads(x.read_text());bb=json.loads(y.read_text());assert '/independent-a/output/' in str(x),(x,y)
  if x.name.endswith('-HISTORY.json'):
   keys=['actual_raw_increment_rows_hex','actual_raw_increment_witnesses_hex']
   assert sorted(zip(aa[keys[0]],aa[keys[1]]))==sorted(zip(bb[keys[0]],bb[keys[1]]))
   for receipt in [aa,bb]:
    rows=[int(z,16)for z in receipt['rows_hex']]
    for rk,wk in [(keys[0],keys[1]),('W_rows_hex','W_witnesses_hex')]:
     for target,encoded in zip(receipt[rk],receipt[wk]):
      value=0;coeff=int(encoded,16)
      for i,z in enumerate(rows):
       if coeff>>i&1:value^=z
      assert value==int(target,16)and coeff>>len(rows)==0
   for k in keys:aa.pop(k);bb.pop(k)
   detail=keys
  elif x.name=='RESULT.json':
   for n in list(aa):
    if isinstance(aa[n],dict):
     for k in list(aa[n]):
      if k in ['W14_plus_W66_increment_witness','W66_from_increments_and_six_W_witness']:
       for receipt,folder in [(aa,x.parent),(bb,y.parent)]:
        hist=json.loads((folder/(n+'-HISTORY.json')).read_text());rows=[int(z,16)for z in hist['actual_raw_increment_rows_hex']];W=[int(z,16)for z in hist['W_rows_hex']]
        if k.startswith('W66'):rows += [W[i]for i in[8,14,22,30,38,59]];target=W[66]
        else:target=W[14]^W[66]
        coeff=int(receipt[n][k],16);value=0
        for i,z in enumerate(rows):
         if coeff>>i&1:value^=z
        assert value==target and coeff>>len(rows)==0
       aa[n].pop(k);bb[n].pop(k);detail.append(n+'/'+k)
  else:raise AssertionError((x,y,'unallowed difference'))
  assert aa==bb,(x,y,'semantic mismatch');kind='basis_order_equivalent_with_exact_witness_validation'
 comparisons.append({'expected':str(x.relative_to(P)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'reproduced':str(y.relative_to(R)),'reproduced_sha256':hashlib.sha256(y.read_bytes()).hexdigest(),'comparison':kind,'reindexed_fields':detail})
def raw():
 p=P/'bit-raw-query-lift-gate';o=R/'raw';o.mkdir(exist_ok=True)
 cmd([p/'author/check.py','--repo',repo,'--source',base,'--out',o/'author.json']);compare(p/'author/CERTIFICATE.json',o/'author.json')
 cmd([p/'review-root/check.py','--repo',repo,'--source',base,'--out',o/'root.json']);compare(p/'review-root/RESULT.json',o/'root.json')
def aug():
 p=P/'bit-augmented-acquisition';o=R/'aug';o.mkdir(exist_ok=True)
 cmd([p/'author/build.py','--source',base,'--out',o/'output'])
 for n in ['PRESERVED-WORD','PRESERVED-CLOSED-WORD','SPARE-WORD','SPARE-CLOSED-WORD']:compare(p/f'author/output/{n}.json',o/f'output/{n}.json')
 for n,v in [('PRESERVED','preserved-verification'),('SPARE','spare-verification')]:
  cmd([p/'author/check.py','--repo',repo,'--word',o/f'output/{n}-CLOSED-WORD.json','--out',o/v])
  for f in ['RESULT.json','HISTORY.json']:compare(p/f'author/{v}/{f}',o/v/f)
 cmd([p/'independent-a/check.py','--repo',repo,'--package',o,'--out',o/'review'])
 for f in (p/'independent-a/output').glob('*.json'):compare(f,o/'review'/f.name)
def q9():
 p=P/'bit-two-demand-slack';o=R/'q9';o.mkdir(exist_ok=True);source=P/'bit-augmented-acquisition/author/output/SPARE-WORD.json'
 cmd([p/'author/check.py','--repo',repo,'--source',source,'--out',o/'author.json']);compare(p/'author/CERTIFICATE.json',o/'author.json')
 cmd([p/'review-root/check.py','--repo',repo,'--source',source,'--certificate',o/'author.json','--out',o/'root.json']);compare(p/'review-root/RESULT.json',o/'root.json')
def cohort():
 p=P/'bit-reprogrammed-cohort';o=R/'cohort';o.mkdir(exist_ok=True)
 cmd([p/'author/build.py','--repo',repo,'--base',base,'--out',o/'output'])
 for f in ['WORD.json','CLOSED-WORD.json']:compare(p/'author/output'/f,o/'output'/f)
 cmd([p/'author/check.py','--repo',repo,'--word',o/'output/CLOSED-WORD.json','--out',o/'author-check'])
 for f in ['RESULT.json','HISTORY.json']:compare(p/'author/verification'/f,o/'author-check'/f)
 cmd([p/'author/capacity.py','--repo',repo,'--word',o/'output/WORD.json','--out',o/'CAPACITY.json']);compare(p/'author/CAPACITY.json',o/'CAPACITY.json')
 cmd([p/'independent-a/check.py','--repo',repo,'--package',o,'--out',o/'review'])
 for f in (p/'independent-a/output').glob('*.json'):
  if f.name!='STRUCTURE.json':compare(f,o/'review'/f.name)
 sc=o/'structure-code';sc.mkdir(exist_ok=True);(sc/'output').mkdir(exist_ok=True)
 for n in ['structure.py','check.py']:shutil.copy2(p/'independent-a'/n,sc/n)
 cmd([sc/'structure.py','--package',o]);compare(p/'independent-a/output/STRUCTURE.json',sc/'output/STRUCTURE.json')
 cmd([p/'capacity-review-root/check.py','--repo',repo,'--word',o/'output/WORD.json','--certificate',o/'CAPACITY.json','--out',o/'root.json']);compare(p/'capacity-review-root/RESULT.json',o/'root.json')
def dihedral():
 p=P/'complex-dihedral-interstage';o=R/'dihedral';o.mkdir(exist_ok=True)
 cmd([p/'author/check.py','--repo',repo,'--out',o/'author.json']);compare(p/'author/RESULT.json',o/'author.json')
 for n in ['check.py','check_all_heads.py']:shutil.copy2(p/'review-root'/n,o/n)
 cmd([o/'check.py']);compare(p/'review-root/RESULT.json',o/'RESULT.json')
 cmd([o/'check_all_heads.py']);compare(p/'review-root/ALL-HEAD-RESULT.json',o/'ALL-HEAD-RESULT.json')
 cmd([p/'corollary-independent-b/check.py','--repo',repo,'--proof',p/'review-root/ALL-HEAD-CYCLIC-COROLLARY.md','--out',o/'corollary.json']);compare(p/'corollary-independent-b/RESULT.json',o/'corollary.json')
def lane():
 p=P/'bit-lane-service-boundary';o=R/'lane';o.mkdir(exist_ok=True);cmd([p/'independent-c/check.py','--proof',p/'author/PROOF.md','--out',o/'RESULT.json']);compare(p/'independent-c/RESULT.json',o/'RESULT.json')
def twocopy():
 p=P/'bit-two-copy-cohort-source';o=R/'two-copy';o.mkdir(exist_ok=True)
 cmd([p/'conditional-origin/build.py','--repo',repo,'--base',base,'--out',o/'conditional'])
 for f in ['WORD.json','CLOSED-WORD.json']:compare(p/'conditional-origin/output'/f,o/'conditional'/f)
 cmd([p/'conditional-origin/check.py','--repo',repo,'--word',o/'conditional/CLOSED-WORD.json','--out',o/'conditional-check'])
 for f in ['RESULT.json','HISTORY.json']:compare(p/'conditional-origin/verification'/f,o/'conditional-check'/f)
 cmd([p/'author/expand.py','--source',o/'conditional','--out',o/'output'])
 for f in ['WORD.json','CLOSED-WORD.json']:compare(p/'author/output'/f,o/'output'/f)
 cmd([p/'author/check.py','--repo',repo,'--word',o/'output/CLOSED-WORD.json','--conditional',o/'conditional/CLOSED-WORD.json','--out',o/'author-check'])
 for f in ['RESULT.json','HISTORY.json']:compare(p/'author/verification'/f,o/'author-check'/f)
 cmd([p/'independent-a/check.py','--repo',repo,'--package',o,'--out',o/'review'])
 for f in (p/'independent-a/output').glob('*.json'):compare(f,o/'review'/f.name)
def middle():
 p=P/'complex-zero-ordinary-middle';o=R/'middle';o.mkdir(exist_ok=True)
 shutil.copytree(p/'author',o/'author',dirs_exist_ok=True);cmd([o/'author/check_middle_gate.py','--repo',repo]);compare(p/'author/MIDDLE-GATE-RESULT.json',o/'author/MIDDLE-GATE-RESULT.json')
 shutil.copytree(p/'review-root',o/'root',dirs_exist_ok=True);cmd([o/'root/check.py']);compare(p/'review-root/RESULT.json',o/'root/RESULT.json')
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
 fs={ex.submit(f):f.__name__ for f in[raw,aug,q9,cohort,dihedral,lane,twocopy,middle]}
 errors=[]
 for f in concurrent.futures.as_completed(fs):
  try:f.result();print('PASS',fs[f],flush=True)
  except Exception as exc:errors.append((fs[f],str(exc)));print('FAIL',fs[f],str(exc),flush=True)
(R/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');(R/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n')
assert not errors,errors
print(json.dumps({'status':'PASS_CP5_PORTABLE_REPRODUCTION','commands':len(commands),'json_comparisons':len(comparisons),'byte_identical':sum(x['comparison']=='byte_identical'for x in comparisons)}))
