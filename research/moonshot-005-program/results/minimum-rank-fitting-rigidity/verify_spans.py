#!/usr/bin/env python3
"""Exact modular minor certificates for native E8 block-rank8 rigidity."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
if not __debug__:raise SystemExit('Exact assertion checks require Python without -O')
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';B=[5,56,69,100,65,77,96,103];P=65537

def choose_basis(rows,n,stop=None):
 base={};chosen=[];cols=[]
 for label,rr in rows:
  v=np.array(rr,dtype=np.int64)%P
  for j in range(n):
   if not v[j]:continue
   if j in base:v=(v-int(v[j])*base[j])%P
   else:base[j]=v*pow(int(v[j]),-1,P)%P;chosen.append(label);cols.append(j);break
  if stop and len(base)==stop:break
 return chosen,cols

def detmod(rows):
 A=np.array(rows,dtype=np.int64)%P;n=len(A);assert A.shape==(n,n);ans=1
 for j in range(n):
  k=next((k for k in range(j,n) if A[k,j]),None)
  if k is None:return 0
  if k!=j:A[[j,k]]=A[[k,j]];ans=-ans
  d=int(A[j,j]);ans=ans*d%P;A[j]=A[j]*pow(d,-1,P)%P
  if j+1<n:A[j+1:,j:]=(A[j+1:,j:]-A[j+1:,j,None]*A[None,j,j:])%P
 return ans%P

def main(a):
 raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;s=json.loads(gzip.decompress(raw));H=[s['live'][i] for i in s['hosted']['Dports']] if a.source_set=='hosted96' else s['live'];N=len(H);assert N==(96 if a.source_set=='hosted96' else 104) and set(B)<=set(H)
 def root(h):
  n=s['frames'][s['initial'][h]][0];t=[j for j in range(9) if n>>j&1]
  if len(t)==3:return [2 if j in t else -1 for j in range(9)]
  z=[j for j in range(9) if j not in t];return [3*(int(j==z[0])-int(j==z[1])) for j in range(9)]
 r={h:root(h) for h in H};dot=lambda x,y:sum(u*v for u,v in zip(x,y));G={(h,j):F(dot(r[h],r[j]),18) for h in H for j in H};g={h:[G[h,b] for b in B] for h in H}
 assert all(G[h,j]==int(h==j) for h in B for j in B) and all(G[h,j]==sum(g[h][p]*g[j][p] for p in range(8)) for h in H for j in H)
 sym=list(itertools.combinations_with_replacement(range(8),2));v={h:[int(4*g[h][p]*g[h][q]) for p,q in sym] for h in H};assert all(F(x,4)==g[h][p]*g[h][q] for h in H for (p,q),x in zip(sym,v[h]))
 proj,pc=choose_basis([(h,v[h]) for h in H],36);assert len(proj)==36;dp=detmod([v[h] for h in proj]);assert dp
 adj=[sum(1<<j for j,k in enumerate(H) if i!=j and not G[h,k]) for i,h in enumerate(H)];frames=[]
 def clique(prefix,cand):
  if len(prefix)==8:frames.append([H[i] for i in prefix]);return
  while cand.bit_count()+len(prefix)>=8:
   j=(cand&-cand).bit_length()-1;cand^=1<<j;clique(prefix+[j],cand&adj[j])
 clique([], (1<<N)-1);assert len(frames)==(369 if N==96 else 759)
 target=[4*int(p==q) for p,q in sym];assert all([sum(v[h][t] for h in fr) for t in range(36)]==target for fr in frames)
 ref=frames[0];crel={k:[int(h in fr)-int(h in ref) for h in H] for k,fr in enumerate(frames[1:])};cbasis,cc=choose_basis(list(crel.items()),N);assert len(cbasis)==N-36;dc=detmod([[crel[k][j] for j in cc] for k in cbasis]);assert dc
 ts=list(itertools.combinations_with_replacement(range(36),2));pairs=[(h,h) for h in H]+[(h,j) for k,h in enumerate(H) for j in H[k+1:] if not G[h,j]]
 def tensor(i,j):return [v[i][p]*v[j][q]+(v[i][q]*v[j][p] if p!=q else 0) for p,q in ts]
 tbasis,tc=choose_basis([(pair,tensor(*pair)) for pair in pairs],666,666);assert len(tbasis)==666;dt=detmod([tensor(*pair) for pair in tbasis]);assert dt
 duplicate=[v[h] for h in proj];duplicate[-1]=duplicate[0];assert detmod(duplicate)==0
 out={'status':'PASS_EXACT_JORDAN_RIGIDITY_SPAN_CERTIFICATES','native_sha256':PIN,'B':B,'hosted':H,'modulus':P,'source_coordinates':{str(h):[str(x) for x in g[h]] for h in H},'Sym8_coordinates':[list(x) for x in sym],'source_set':a.source_set,'source_projector_rank':36,'projector_basis':proj,'projector_minor_mod_p':dp,'native_orthoframes':len(frames),'reference_frame':ref,'context_relation_rank':len(cbasis),'context_relation_basis_frames':[frames[k+1] for k in cbasis],'context_relation_minor_columns':cc,'context_relation_minor_mod_p':dc,'Sym2_Sym8_dimension':666,'Jordan_tensor_rank':666,'Jordan_tensor_basis_pairs':[list(x) for x in tbasis],'Jordan_tensor_minor_mod_p':dt,'negative_controls':{'duplicated_projector_minor_row_rejected':True},'scope':'Exact nonzero integer minors modulo65537 prove the three rational ranks. Universal theorem separately uses the matrix algebra proof. Characteristic-zero all positive volumes; no symmetry/PSD/contact-invertibility premise, no physical construction or kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'SPAN-CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','source_projector_rank','projector_minor_mod_p','native_orthoframes','context_relation_rank','context_relation_minor_mod_p','Jordan_tensor_rank','Jordan_tensor_minor_mod_p']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-set',choices=['hosted96','full104'],required=True);main(p.parse_args())
