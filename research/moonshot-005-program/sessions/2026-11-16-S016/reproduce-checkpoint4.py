"""Rebuild source words and run independent CP4 reviews in fresh outputs."""
import argparse,concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=a.repo.resolve();o=a.out.resolve();o.mkdir(parents=True,exist_ok=True)
b=r/'research/moonshot-005-program/results';bit=b/'bit-forked-shared-history'
old=b/'bit-singular-eight-seed-source';family=b/'complex-boolean-sign-family'
normal=b/'complex-four-source-normalization';records=[]
def run(name,args):
 cmd=[sys.executable,'-B']+list(map(str,args));q=subprocess.run(cmd,cwd=r,text=True,capture_output=True,timeout=240)
 (o/(name+'.log')).write_text(q.stdout+q.stderr)
 item={'name':name,'command':cmd,'returncode':q.returncode};records.append(item)
 if q.returncode:raise RuntimeError(name+' failed; see log')
 return item
def build(name,base,filters=None):
 src=bit/'author'/name;dest=o/name
 args=[src/'build.py','--repo',r,'--base',base,'--out',dest]
 if filters:args+=['--filters',filters]
 run(name+'-build',args);run(name+'-author-check',[src/'check.py','--repo',r,'--out',dest])
 run(name+'-price',[src/'price.py','--out',dest])
 if name.startswith('history-'):run(name+'-author-history',[src/'history.py','--repo',r,'--out',dest])
 expected=(src/'output/WORD.json').read_bytes();actual=(dest/'WORD.json').read_bytes()
 assert actual==expected,name+' rebuilt word differs'
 return dest
base=old/'author/output/WORD.json'
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:
 fut=[ex.submit(build,n,base)for n in ['history-twelve','fifteen']]
 built=[f.result()for f in fut]
build('history-fifteen',o/'fifteen/WORD.json',o/'history-twelve/WORD.json')
jobs=[]
for name in ['history-twelve','fifteen','history-fifteen']:
 args=[bit/'independent-c/check.py','--repo',r,'--word',o/name/'WORD.json','--seed',old/'seed/SOURCE.json','--mode',12 if name=='history-twelve'else 15,'--out',o/(name+'-independent')]
 if name.startswith('history-'):args+=['--snapshots',o/name/'HISTORY-SNAPSHOTS.json']
 jobs.append((name+'-independent-c',args))
jobs += [
 ('root-words-prices',[bit/'root-review/check.py','--repo',r,'--engine',b/'bit-shared-meet-funnel/root-review','--history-twelve',o/'history-twelve/WORD.json','--fifteen',o/'fifteen/WORD.json','--history-fifteen',o/'history-fifteen/WORD.json','--out',o/'root-words']),
 ('family-author',[family/'author/check.py','--repo',r,'--out',o/'family-author.json','--catalogue',o/'family-catalogue.json']),
 ('family-independent-root',[family/'root-review/check.py','--proof',family/'author/PROOF.md','--out',o/'family-review']),
 ('normalization-independent-b',[normal/'independent-b/check.py','--out',o/'normalization-review.json']),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
 futures=[ex.submit(run,n,args)for n,args in jobs]
 for f in futures:f.result()
out={'status':'PASS_CP4_REPRODUCTION','rebuilt_words':3,'commands':records,
     'scope':'Author rebuilds and independent implementations are separately labelled; no complete supplier or kappa result.'}
(o/'REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'commands':len(records),'rebuilt_words':3}))
