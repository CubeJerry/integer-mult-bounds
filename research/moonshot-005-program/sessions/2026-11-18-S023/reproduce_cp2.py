#!/usr/bin/env python3
"""Rebuild the paid native words, scalar port cuts, and unrestricted cubic package."""
import argparse,gzip,hashlib,json,os,subprocess,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);pg=repo/'research/moonshot-005-program';r=pg/'results'
 layout=r/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';factor=r/'bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json';records=[]
 def run(name,script,args,pairs):
  proc=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],cwd=repo,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  if proc.returncode:raise RuntimeError(name+': '+proc.stderr.decode())
  checked=[]
  for frozen,fresh in pairs:
   x,y=frozen.read_bytes(),fresh.read_bytes()
   if frozen.suffix=='.gz':x=gzip.decompress(x)
   if fresh.suffix=='.gz':y=gzip.decompress(y)
   if x!=y:raise ValueError(name+' changed output '+str(frozen))
   checked.append({'path':str(frozen.relative_to(pg)),'sha256_uncompressed':hashlib.sha256(y).hexdigest()})
  records.append({'check':name,'outputs':checked});print(name,'PASS',flush=True)
 n=r/'bit-seven-source-shared-quotients'
 for tag,script,source in [('four',n/'four/build.py',n/'four/output'),('seven',n/'seven/build.py',n/'seven/output'),('seven-shared',n/'seven/build_shared.py',n/'seven/shared-output')]:
  dest=out/tag
  run(tag+'-author',script,['--layout',layout,'--out',dest],[(source/f,dest/f)for f in ['WORD.json','RESULT.json']])
  review=out/(tag+'-second-replay')
  run(tag+'-second-replay',n/'second-replay/check.py',['--layout',layout,'--word',dest/'WORD.json','--author-result',dest/'RESULT.json','--out',review],[(n/'second-replay'/tag/'RESULT.json',review/'RESULT.json')])
  if tag!='four':
   proof=n/'seven'/('SHARED-D4-PROOF.md'if tag=='seven-shared'else'PROOF.md');output=out/(tag+'-root.json');frozen=n/'review'/('SHARED-RESULT.json'if tag=='seven-shared'else'DIRECT-RESULT.json')
   run(tag+'-root-review',n/'review/check.py',['--layout',layout,'--word',dest/'WORD.json','--proof',proof,'--out',output],[(frozen,output)])
 q=r/'bit-replicated-scalar-port-cut';qa=out/'replicated-author.json';qr=out/'replicated-review.json'
 run('replicated-author',q/'author/check.py',['--layout',layout,'--factor',factor,'--out',qa],[(q/'author/RESULT.json.gz',qa)])
 run('replicated-root-review',q/'review/check.py',['--repo',repo,'--author-result',qa,'--proof',q/'author/PROOF.md','--out',qr],[(q/'review/RESULT.json',qr)])
 c=r/'complex-unrestricted-cubic-gate';ca=out/'cubic-author.json';cr=out/'cubic-review.json'
 run('cubic-author',c/'author/check.py',['--repo',repo,'--out',ca],[(c/'author/RESULT.json',ca)])
 run('cubic-independent-review',c/'review/check.py',['--repo',repo,'--proof',c/'author/PROOF.md','--pins',c/'author/SOURCE-PINS.json','--out',cr],[(c/'review/RESULT.json',cr)])
 s=r/'bit-stripe-varying-port-cut';sa=out/'stripe-author';sr=out/'stripe-review'
 run('stripe-author',s/'author/check.py',['--repo',repo,'--out',sa],[(s/'author/output'/f,sa/f)for f in ['RESULT.json','DECISIONS.json.gz']])
 run('stripe-independent-review',s/'review/check.py',['--layout',layout,'--factor',factor,'--author-result',s/'author/output/DECISIONS.json.gz','--proof',s/'author/PROOF.md','--out',sr],[(s/'review/output/RESULT.json.gz',sr/'RESULT.json')])
 (out/'VALIDATION.json').write_text(json.dumps({'status':'PASS','baseline_sha':'2ca4122b27043874d765a492d4366bcdd9eb3cdf','scope':'Fourteen scoped author and independent review runs; no full legacy replay or new kappa.','checks':records},indent=2)+'\n')
if __name__=='__main__':main()
