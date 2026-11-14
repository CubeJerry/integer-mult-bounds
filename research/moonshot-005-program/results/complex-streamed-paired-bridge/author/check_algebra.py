#!/usr/bin/env python3
"""Finite exact controls for the all-field streaming paired factorization."""
from __future__ import annotations
import argparse,json,random
from pathlib import Path
from fractions import Fraction as F

def need(ok,msg):
 if not ok:raise ValueError(msg)
def norm(x,p):return x%p if p else F(x)
def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def zeros(n,m):return [[0]*m for _ in range(n)]
def trans(A):return list(map(list,zip(*A)))
def mul(A,B,p):return [[norm(sum(x*y for x,y in zip(row,col)),p)for col in zip(*B)]for row in A]
def add(A,B,p,c=1):return [[norm(x+c*y,p)for x,y in zip(ar,br)]for ar,br in zip(A,B)]
def inv(A,p):
 n=len(A);B=[[norm(x,p)for x in row]+eye(n)[i]for i,row in enumerate(A)]
 for j in range(n):
  k=next(k for k in range(j,n)if B[k][j]);B[j],B[k]=B[k],B[j];v=B[j][j];iv=pow(int(v),-1,p)if p else 1/v;B[j]=[norm(x*iv,p)for x in B[j]]
  for k in range(n):
   if k!=j:
    v=B[k][j];B[k]=[norm(x-v*y,p)for x,y in zip(B[k],B[j])]
 return [row[n:]for row in B]
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

def stream(P,Q,L,r,V,p,mutant=None):
 nx=len(P[0]);ny=len(Q);n=2*nx+ny;I=eye(n);x=I[:nx];b=I[nx:2*nx];d=I[2*nx:];b0=[row[:]for row in b];z=zeros(ny,n);u=zeros(V,n);history=[];prefix=[]
 if mutant=='dirty_output':
  z=[row[:]for row in d]
 for i in range(r):
  Pi=P[i*V:(i+1)*V];Qi=[row[i*V:(i+1)*V]for row in Q];Li=L[i*V:(i+1)*V]
  u=add(u,mul(Pi,x,p),p)
  history.extend([row[:]for row in u]) # Actual C-to-D transported rows.
  if i and mutant!='omit_previous_adjoint':
   Qprev=[row[(i-1)*V:i*V]for row in Q];u=add(u,mul(trans(Qprev),d,p),p,-1)
  if mutant is None:need(u==mul(Pi,x,p),'genuine primal at D after adjoint cancellation')
  z=add(z,mul(Qi,u,p),p)
  prefix.append([row[:]for row in z])
  if mutant=='wrong_cleanup_row':
   Li=L[:V]
  u=add(u,mul(Li,z,p),p,-1)
  if mutant is None:need(u==zeros(V,n),'prefix left inverse cleans actual carrier')
  u=add(u,mul(trans(Qi),d,p),p);history.extend([row[:]for row in u]);b=add(b,mul(trans(Pi),u,p),p,-1)
 history.extend([row[:]for row in u]) # Final C-to-D cleanup transfer.
 if mutant!='omit_final_cleanup':
  Qlast=[row[(r-1)*V:r*V]for row in Q];u=add(u,mul(trans(Qlast),d,p),p,-1)
 wanted_z=mul(mul(Q,P,p),x,p);wanted_b=add(b0,mul(trans(mul(Q,P,p)),d,p),p,-1)
 return {'correct':z==wanted_z and b==wanted_b and u==zeros(V,n),'transported_boundary_rank':rank(history,p),'rankP':rank(P,p),'rankQ':rank(Q,p),'rankF':rank(mul(Q,P,p),p),'input_columns':n,'prefix_count':len(prefix)}

def main(a):
 rng=random.Random(12122026);cases=[]
 for p in [0,2,3,5,7]:
  for r in [1,2,3]:
   for V in [1,2]:
    for deficient in [False,True]:
     nv=r*V;px=(r+1)*V;my=(r+1)*V;M=eye(nv)
     for _ in range(4*nv):
      if nv==1:continue
      i,j=rng.sample(range(nv),2);c=rng.choice([-2,-1,1,2]);M[i]=[norm(x+c*y,p)for x,y in zip(M[i],M[j])]
     Q0=eye(nv)+[[rng.randrange(-2,3)for _ in range(nv)]for _ in range(my-nv)];Q=mul(Q0,M,p);Minv=inv(M,p);L=[row+[0]*(my-nv)for row in Minv];need(mul(L,Q,p)==eye(nv),'actual full left inverse')
     P=[eye(nv)[i]+[rng.randrange(-2,3)for _ in range(px-nv)]for i in range(nv)]
     if deficient and nv>1:P[-1]=P[0][:]
     result=stream(P,Q,L,r,V,p);need(result['correct'],'all-column paired stream identity');need(result['transported_boundary_rank']==result['rankP']+nv,'actual transported boundary-mode rank');cases.append({'field':'Q'if not p else p,'factors':r,'V':V,'deficient_P':deficient,**result})
 P=[[1,1,0],[0,1,1]];Q=[[1,0],[0,1],[1,1]];L=[[1,0,0],[0,1,0]];negative=[]
 for label in ['omit_previous_adjoint','wrong_cleanup_row','omit_final_cleanup','dirty_output']:
  need(not stream(P,Q,L,2,1,0,mutant=label)['correct'],'negative control '+label);negative.append(label)
 out={'status':'PASS_STREAMED_PAIRED_FACTOR_ALGEBRA','cases':cases,'matrix_cases':len(cases),'negative_controls':negative,'scope':'Finite exact tests of general rectangular/block factorization, all input columns and transported boundary-mode rank; universal proof and isolated-interface lower bound are separate in PROOF.md.'};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args())
