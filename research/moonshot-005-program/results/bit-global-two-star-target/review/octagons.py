"""Prove the virgin canonical subgraph has girth at least ten, directly on native original fields."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from check import mod,req
def main(a):
 b=a.repo/'research/moonshot-005-program/results';f=mod(b/'bit-spread-h263-source/review/check.py','ff');g=mod(b/'bit-spread-overlap-source/review/check.py','geo').Native(a.repo,f);h=mod(b/'bit-spread-source-owner-compiler/author/compile_source.py','fee');ar=mod(a.arithmetic,'ffops').Arithmetic(a.library,f,h);pr=mod(a.previous,'previous');mm=ar.mm
 adj=[set(g.adj[i])&set(range(111))for i in range(111)];I=sorted(set(range(111))-adj[10]-{80});J=sorted(set(range(111))-adj[80]-{10});A=np.load(a.rim,mmap_mode='r');req(sha256(A).hexdigest()==json.loads(a.receipt.read_bytes())['rim_global_original_sha256'],'genuine complete native rim');x=pr.rand('actual original length-four donor transports',(480,1));w=12;src={};dst={};ids={}
 for i in I:
  js=sorted(adj[i].intersection(J));B={j:A[480*i:480*(i+1),480*j:480*(j+1)]for j in js};v=np.hstack([mm(B[j],x)for j in js])
  for k in js:
   ri=ar.reduce(B[k],True)[0];Y=mm(ri,v)
   for z,j in enumerate(js):
    if k!=j:src[i,k,j]=Y[:,z].copy();dst[i,k,j]=mm(ri[:w],B[j])
 batches={};probes={}
 for d in J:
  for s in J:
   if d==s:continue
   q=sorted(adj[d].intersection(adj[s],I));ids[d,s]=q
   if q:batches[d,s]=np.stack([src[i,d,s]for i in q],axis=1);probes[d,s]=np.vstack([dst[i,d,s]for i in q])
 digest=sha256();paths=pairs=0;raw=np.dtype((np.void,w))
 for n,s in enumerate(J):
  for d in J[n+1:]:
   patterns=[]
   for k in J:
    if k in (d,s)or(d,k)not in probes or(k,s)not in batches:continue
    p,q=ids[d,k],ids[k,s];Y=mm(probes[d,k],batches[k,s]).reshape(len(p),w,len(q)).transpose(0,2,1);patterns.append(Y[np.not_equal.outer(p,q)])
   if not patterns:continue
   full=np.ascontiguousarray(np.vstack(patterns));words=full.view(raw).reshape(-1);req(len(np.unique(words))==len(words),'two native length-four transports agree on all 12 output fields')
   paths+=len(full);pairs+=len(full)*(len(full)-1)//2;digest.update(bytes([s,d]));digest.update(full)
  if n%12==0:print('octagon donor',n,flush=True)
 best=96;win=None
 for n in range(2,50):
  for m in range(2,49):
   for e in range(2*max(n,m),n*m+1):
    v=m+n;u=2*e-v
    if 2*e*(u*v*v+u**3)>(n*(n-1)+m*(m-1))*v**3:break
    q=97-v+e
    if q>best:best=q;win=(n,m,e)
 out={'virgin_receivers':49,'virgin_donors':48,'input_vector_sha256':sha256(x).hexdigest(),'original_output_fields_per_sample':w,'simple_length_four_paths':paths,'same_endpoint_distinct_transport_pairs':pairs,'ordered_native_sample_sha256':digest.hexdigest(),'minimum_girth_of_simultaneously_calibrated_canonical_subgraph':10,'free_canonical_edge_upper':best,'worst_pruned_core':win,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'GIRTH-TEN.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out,flush=True)
if __name__=='__main__':
 p=ArgumentParser()
 for k in ('repo','arithmetic','library','previous','rim','receipt','out'):p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
