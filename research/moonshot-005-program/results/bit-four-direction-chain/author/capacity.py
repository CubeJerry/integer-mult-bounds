#!/usr/bin/env python3
"""Finite chain-map controls; the all-field capacity proof is in PROOF.md."""
import argparse,itertools,json
from collections import Counter
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1;b>>=1
  if a&4:a^=7
 return c

def dot(a,b):
 x=0
 for u,v in zip(a,b):x^=mul(u,v)
 return x

def reduce(M,ncols):
 A=[list(r) for r in M];piv=[];k=0
 for j in range(ncols):
  q=next((r for r in range(k,len(A)) if A[r][j]),None)
  if q is None:continue
  A[k],A[q]=A[q],A[k];z=next(x for x in (1,2,3) if mul(x,A[k][j])==1)
  A[k]=[mul(z,x) for x in A[k]]
  for r in range(len(A)):
   if r!=k and A[r][j]:
    z=A[r][j];A[r]=[x^mul(z,y) for x,y in zip(A[r],A[k])]
  piv.append(j);k+=1
 return A,piv

def kernel(M,ncols):
 A,piv=reduce(M,ncols);out=[]
 for j in range(ncols):
  if j not in piv:
   v=[0]*ncols;v[j]=1
   for r,p in enumerate(piv):v[p]=A[r][j]
   out.append(v)
 return out

def solve(M,b):
 ncols=len(M[0]);A,piv=reduce([r+[x] for r,x in zip(M,b)],ncols)
 if any(not any(r[:ncols]) and r[-1] for r in A):return None
 x=[0]*ncols
 for r,p in enumerate(piv):x[p]=A[r][-1]
 return x

def project(v):
 z=next((x for x in v if x),None)
 if z is None:return None
 inv=next(x for x in (1,2,3) if mul(x,z)==1)
 return tuple(mul(inv,x) for x in v)

def phi(U):
 return [[(U[r][j] if j<3 else 0) if t==0 else (U[r][j-1] if j else 0)
          for j in range(4)] for r in range(2) for t in range(2)]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 conic={project([1,t,mul(t,t)]):[1,t,mul(t,t),mul(t,mul(t,t))] for t in range(4)}
 conic[(0,0,1)]=[0,0,0,1]
 codes=[[0,1,2,0],[0,1,2,3],[3,1,2,0]]
 counts=Counter();binary=[];rank_census=Counter();all_cases=0
 for flat in itertools.product(range(4),repeat=6):
  U=[list(flat[:3]),list(flat[3:])];KU=kernel(U,3)
  if len(KU)!=1:continue
  all_cases+=1;P=phi(U);KP=kernel(P,4);parameter=project(KU[0]);exceptional=parameter in conic
  need(len(KP)==int(exceptional),'exact conic degeneracy')
  if exceptional:need(project(KP[0])==project(conic[parameter]),'cubic kernel')
  rank_census[4-len(KP)]+=1;preimage=solve(P,[1,0,0,1])
  if preimage is None:continue
  cover=[all(dot(c,z)==0 for z in KP) and dot(c,preimage)!=0 for c in codes]
  if all(x<2 for x in flat):
   need(sum(cover)>=2,'binary two-of-three scalar cover')
   counts[sum(cover)]+=1;binary.append({'U':U,'identity_preimage':preimage,'exceptional':exceptional,'coverage':cover})
   for coeff in itertools.product(range(4),repeat=len(KP)):
    alt=list(preimage)
    for z,b in zip(KP,coeff):alt=[x^mul(b,y) for x,y in zip(alt,z)]
    need([all(dot(c,z)==0 for z in KP) and dot(c,alt)!=0 for c in codes]==cover,'preimage-independent scalar coverage')
 need(all_cases==3780 and len(binary)==36,'exact finite matrix domains')
 need(dict(counts)=={2:21,3:15},'binary coverage census')
 U=[[0,1,2],[1,0,3]];P=phi(U);KP=kernel(P,4);preimage=[0,1,0,0]
 need([dot(r,preimage) for r in P]==[1,0,0,1],'larger-field identity preimage')
 cover=[all(dot(c,z)==0 for z in KP) and dot(c,preimage)!=0 for c in codes]
 need(cover==[True,False,False],'fixed three-code cover fails outside binary types')
 need(project(kernel(U,3)[0])==(1,3,2),'fourth conic parameter scope control')
 need(solve(phi([[1,0,0],[0,0,0]]),[1,0,0,1]) is None,'rank-one selector cannot erase identity')
 out={'status':'PASS_CHAIN_CAPACITY_CONTROLS','all_full_rank_F4_selectors':all_cases,'map_rank_census':dict(rank_census),
      'binary_full_rank_selectors':42,'binary_identity_admitting_selectors':len(binary),'binary_cover_census':dict(counts),
      'fixed_scalar_codes_over_F4':codes,'binary_cases':binary,
      'larger_field_boundary':{'U':U,'kernel':[1,3,2],'identity_preimage':preimage,'fixed_code_coverage':cover},
      'universal_proof':'PROOF.md; finite controls do not prove the all-field theorem',
      'claim':'at most three exceptional conic types imply ell>=197; all binary chains satisfy this premise','new_kappa':None}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','all_full_rank_F4_selectors','binary_identity_admitting_selectors','binary_cover_census']}))
if __name__=='__main__':main()
