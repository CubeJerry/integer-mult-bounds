#!/usr/bin/env python3
"""Exact finite controls for the proved paired commutator and its scope.

This is an author check. The all-field theorem is in PROOF.md.
"""
from __future__ import annotations
import argparse,itertools,json,random
from fractions import Fraction as F
from pathlib import Path

def need(b,m):
 if not b:raise ValueError(m)
def matmul(A,B,p):
 return [[norm(sum(a*b for a,b in zip(row,col)),p)for col in zip(*B)]for row in A]
def norm(x,p):return x%p if p else F(x)
def zero(n,m):return [[0]*m for _ in range(n)]
def identity(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def rank(A,p):
 A=[[norm(x,p)for x in row]for row in A];r=0
 for j in range(len(A[0])if A else 0):
  k=next((k for k in range(r,len(A))if A[k][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];v=A[r][j];iv=pow(int(v),-1,p)if p else 1/v;A[r]=[norm(x*iv,p)for x in A[r]]
  for k in range(len(A)):
   if k!=r:
    v=A[k][j];A[k]=[norm(x-v*y,p)for x,y in zip(A[k],A[r])]
  r+=1
  if r==len(A):break
 return r

def left_inverse(A,p):
 n=len(A[0]);chosen=[]
 for i,row in enumerate(A):
  if rank([A[j]for j in chosen]+[row],p)>len(chosen):chosen.append(i)
  if len(chosen)==n:break
 need(len(chosen)==n,'full column rank for output cleanup')
 B=[[norm(x,p)for x in A[j]]+[int(i==q)for q in range(n)]for i,j in enumerate(chosen)]
 for j in range(n):
  k=next(k for k in range(j,n)if B[k][j]);B[j],B[k]=B[k],B[j];z=B[j][j];iv=pow(int(z),-1,p)if p else 1/z;B[j]=[norm(x*iv,p)for x in B[j]]
  for k in range(n):
   if k!=j:
    z=B[k][j];B[k]=[norm(x-z*y,p)for x,y in zip(B[k],B[j])]
 L=zero(n,len(A))
 for i in range(n):
  for q,j in enumerate(chosen):L[i][j]=B[i][n+q]
 need(matmul(L,A,p)==identity(n),'actual left inverse')
 return L

def execute(P,Q,field,stages=None,dirty=True,zero_mode=None):
 nx,nr,ny=len(P[0]),len(P),len(Q);size=2*(nx+ny+nr)
 ix=list(range(nx));ib=list(range(nx,2*nx));iy=list(range(2*nx,2*nx+ny));idd=list(range(2*nx+ny,2*nx+2*ny));ir=list(range(2*nx+2*ny,2*nx+2*ny+nr));iss=list(range(2*nx+2*ny+nr,size))
 R=identity(size)
 if not dirty:
  for i in ir+iss:R[i]=[0]*size
 if zero_mode=='output_cleanup':
  for i in iy:R[i]=[0]*size
 def add(dst,src,c):R[dst]=[norm(x+c*y,field)for x,y in zip(R[dst],R[src])]
 def A(M,sgn):
  for i,row in enumerate(M):
   for j,c in enumerate(row):
    if c:add(ir[i],ix[j],sgn*c);add(ib[j],iss[i],-sgn*c)
 def B(M,sgn):
  for i,row in enumerate(M):
   for j,c in enumerate(row):
    if c:add(iy[i],ir[j],sgn*c);add(iss[j],idd[i],-sgn*c)
 if zero_mode:
  for i,row in enumerate(P):
   for j,c in enumerate(row):
    if c:add(ir[i],ix[j],c)
  for i,row in enumerate(Q):
   for j,c in enumerate(row):
    if c:add(iy[i],ir[j],c);add(iss[j],idd[i],c)
  for i,row in enumerate(P):
   for j,c in enumerate(row):
    if c:add(ib[j],iss[i],-c)
  if zero_mode in ('roundtrip','output_cleanup'):
   if zero_mode=='output_cleanup':
    L=left_inverse(Q,field)
    for i,row in enumerate(L):
     for j,c in enumerate(row):
      if c:add(ir[i],iy[j],-c)
   for i,row in enumerate(P if zero_mode=='roundtrip'else []):
    for j,c in enumerate(row):
     if c:add(ir[i],ix[j],-c)
   for i,row in enumerate(Q):
    for j,c in enumerate(row):
     if c:add(iss[j],idd[i],-c)
 else:
  for family,c in stages or [('A',1),('B',1),('A',-1),('B',-1)]:
   (A if family=='A' else B)(P if family=='A'else Q,c)
 want=identity(size)
 if not dirty:
  for i in ir+iss:want[i]=[0]*size
 if zero_mode=='output_cleanup':
  for i in iy:want[i]=[0]*size
 Z=matmul(Q,P,field)
 for i,row in enumerate(Z):
  for j,c in enumerate(row):want[iy[i]][ix[j]]=c;want[ib[j]][idd[i]]=norm(-c,field)
 return R,want,ir+iss,ix+ib+iy+idd

def main(a):
 rng=random.Random(120121);cases=[];negative=[];cleanup_cases=0
 for field in [0,2,3,5,7]:
  for p,m,k,V in [(1,1,1,1),(2,3,1,1),(3,2,2,1),(3,4,2,2),(2,2,2,2),(2,3,3,3),(1,3,2,2),(3,1,2,2)]:
   for singular in [False,True]:
    P=[[rng.randrange(-2,3)for _ in range(p*V)]for _ in range(k*V)];Q=[[rng.randrange(-2,3)for _ in range(k*V)]for _ in range(m*V)]
    if singular:
     for i in range(1,len(P)):P[i]=P[0][:]
    R,want,relays,public=execute(P,Q,field);need(R==want,'dirty all-column paired identity')
    Rz,wz,rz,pz=execute(P,Q,field,dirty=False,zero_mode='roundtrip');need(Rz==wz,'zero-roundtrip all-column identity and zero restoration')
    Re,we,re,pe=execute(P,Q,field,dirty=False,zero_mode='erasure');need(all(Re[i]==we[i]for i in pe),'two-transfer public interface')
    if rank(Q,field)==len(P):
     Rc,wc,rc,pc=execute(P,Q,field,dirty=False,zero_mode='output_cleanup');need(Rc==wc,'zero-output local cleanup');cleanup_cases+=1
    cases.append({'field':'Q'if not field else field,'p':p,'m':m,'k':k,'V':V,'singular_control':singular,'rank_P':rank(P,field),'rank_Q':rank(Q,field),'all_independent_input_columns':len(R)})
 # A source-compatible noncommuting-block counterexample to reversing QP.
 P=[[1,1],[0,1]];Q=[[1,0],[1,1]]
 need(matmul(P,Q,0)!=matmul(Q,P,0),'noncommuting factor control');negative.append('reversed_factor_order')
 for label,stages in [('omit_A_inverse',[('A',1),('B',1),('B',-1)]),('omit_B_inverse',[('A',1),('B',1),('A',-1)]),('reverse_echo_order',[('B',1),('A',1),('B',-1),('A',-1)])]:
  R,w,_,_=execute(P,Q,0,stages=stages);need(R!=w,label);negative.append(label)
 # Independent dirty relays cannot be replaced by zero initial values in proof.
 Rd,wd,_,_=execute([[1]],[[1]],0,stages=[('A',1),('B',1)])
 need(Rd!=wd,'two-stage dirty substitution');negative.append('dirty_as_zero_substitution')
 # A dirty output cannot replace the actual zero-born output cache.
 y,x=F(3),F(2);r=x;yout=y+r;r-=yout;need(r!=0,'dirty-output cleanup must fail');negative.append('dirty_output_as_zero_cache')
 short=0;restored=0
 for field in [2,3,5]:
  alphabet=list(itertools.product('AB',range(1,field)))
  for n in range(1,4):
   for stages in itertools.product(alphabet,repeat=n):
    R,w,relays,public=execute([[1]],[[1]],field,stages=list(stages));short+=1
    I=identity(len(R))
    if all(R[i]==I[i]for i in relays):
     restored+=1;need(R==I,'no nontrivial <=3-stage restored dirty macro')
 out={'status':'PASS_PAIRED_RELAY_ALGEBRA_AND_SCOPE_CONTROLS','matrix_cases':len(cases),'zero_output_cleanup_cases':cleanup_cases,'cases':cases,'short_words_checked':short,'short_relay_restored_words_identity':restored,'negative_controls':negative,'scope':'Finite controls over Q and GF(2,3,5,7), rectangular/singular/noncommuting examples. The universal theorem and four-stage minimum are proved in PROOF.md; no finite test is their proof.'};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args())
