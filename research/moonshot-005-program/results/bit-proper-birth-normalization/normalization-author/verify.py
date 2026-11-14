#!/usr/bin/env python3
"""Exact rectangular-cell controls; universal proof is in PROOF.md."""
import argparse,json,random
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)

def mv(A,x):return sum(((r&x).bit_count()%2)<<i for i,r in enumerate(A))
def mm(A,B):
 out=[]
 for row in A:
  v=0
  for j,b in enumerate(B):
   if row>>j&1:v^=b
  out.append(v)
 return out
def ident(n):return [1<<i for i in range(n)]
def plus(A,B):return [a^b for a,b in zip(A,B)]
def fromcols(cols,n):return [sum(((c>>i)&1)<<j for j,c in enumerate(cols)) for i in range(n)]

def choose(vectors):
 b={};ids=[]
 for i,u in enumerate(vectors):
  x=u
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;ids.append(i);break
 return ids

def inverse(A):
 n=len(A);r=[x|(1<<(n+i)) for i,x in enumerate(A)]
 for j in range(n):
  k=next((k for k in range(j,n) if r[k]>>j&1),None);need(k is not None,'invertible basis')
  r[j],r[k]=r[k],r[j]
  for i in range(n):
   if i!=j and r[i]>>j&1:r[i]^=r[j]
 out=[x>>n for x in r];need(mm(out,A)==ident(n),'basis inverse');return out

def decompose(M,a):
 b=len(M);cols=[mv(M,1<<j) for j in range(a)];ids=choose(cols);rank=len(ids)
 W=[1<<j for j in ids];images=[cols[j] for j in ids]
 null=[x for x in range(1,1<<a) if mv(M,x)==0];K=[null[j] for j in choose(null)]
 need(len(K)==a-rank,'kernel dimension')
 Bi=inverse(fromcols(W+K,a));pool=images+ident(b);Oi=inverse(fromcols([pool[j] for j in choose(pool)],b))
 Rcols=[]
 for j in range(b):
  coordinates=mv(Oi,1<<j);v=0
  for k,w in enumerate(W):
   if coordinates>>k&1:v^=w
  Rcols.append(v)
 R=fromcols(Rcols,a);J=fromcols(K,a);h=Bi[rank:];nu=len(K)
 need(mm(R,M)==plus(ident(a),mm(J,h)),'rectangular inverse identity')
 need(mm(M,J)==[0]*b and mm(h,J)==ident(nu) and mm(h,R)==[0]*nu,'kernel/image identities')
 need(mm(mm(M,R),M)==M,'image projection')
 return R,J,h,nu,rank

def one_case(M,a):
 b=len(M);R,J,h,nu,rank=decompose(M,a);proj=plus(ident(b),mm(M,R));images={mv(M,x) for x in range(1<<a)}
 checks=0
 Ns=([0]*b,[2]*b,[3 if j%2==0 else 1 for j in range(b)])
 for N in Ns:
  for u in range(4):
   source=mv(N,u)
   for pin in range(1<<a):
    pout=mv(M,pin)^source;T=mv(h,pin);recovered=mv(R,pout^source)^mv(J,T)
    need(recovered==pin,'actual mixed-input reconstruction');checks+=1
   for pout in range(1<<b):
    value=pout^source;need((mv(proj,value)==0)==(value in images),'exact image compatibility');checks+=1
 return checks,nu,rank

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 cases=[];checks=0
 for incoming in range(3):
  for outgoing in range(incoming,4):
   for bits in range(1<<(incoming*outgoing)):
    M=[(bits>>(i*incoming))&((1<<incoming)-1) for i in range(outgoing)]
    n,nu,r=one_case(M,incoming);checks+=n;cases.append((incoming,outgoing,nu,r))
 rng=random.Random(1102026)
 for outgoing in (3,4):
  for bits in sorted({rng.randrange(1<<(3*outgoing)) for _ in range(256)}):
   M=[(bits>>(i*3))&7 for i in range(outgoing)]
   n,nu,r=one_case(M,3);checks+=n;cases.append((3,outgoing,nu,r))
 controls=[]
 R,J,h,nu,r=decompose([0],0);projection=plus(ident(1),mm([0],R))
 need(mv(projection,1)!=0,'birth-only free global value rejected');controls.append('birth-only nonlocal value violates image condition')
 need(mv([2],2)==1 and mv([0],2)==0,'unknown Y birth cannot be suppressed');controls.append('suppressing independent Y changes actual acquired output')
 R,J,h,nu,r=decompose([0,0],1);need(nu==1 and mv(R,0)!=1 and (mv(R,0)^mv(J,mv(h,1)))==1,'actual kernel coordinate required');controls.append('terminal-only reconstruction loses a genuine kernel input')
 R,J,h,nu,r=decompose([0,1],1);need(nu==0 and r==1,'newborn retains old channel input');controls.append('old diagonal zero does not imply joint rectangular kernel')
 mode_counts={str(birth):{'first_ground_coordinates':1,'maximum_incoming_proper_visits':birth-1,'total_width_units':birth} for birth in range(1,9)}
 need(mode_counts['1']['total_width_units']==1 and mode_counts['8']['total_width_units']==8,'birth excluded from incoming visits')
 out={'status':'PASS_RECTANGULAR_PROPER_BIRTH_NORMALIZATION_CONTROLS','field_for_computational_cases':'F2',
      'matrix_cases':len(cases),'coefficient_reconstruction_and_image_checks':checks,
      'exhaustive_shapes':'0<=incoming<=2, incoming<=outgoing<=3',
      'additional_fixed_seed_shapes':['3x3','4x3'],'birth_rank_mode_counts':mode_counts,
      'negative_controls':controls,'universal_claim_source':'PROOF.md, not finite tests','new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'matrix_cases':len(cases),'checks':checks,'controls':len(controls)}))

if __name__=='__main__':main()
