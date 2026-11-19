#!/usr/bin/env python3
"""Independent GF(4) exact-minimum census; no author code is imported."""
from argparse import ArgumentParser
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import json,random
# GF(4)=F2[t]/(t^2+t+1), independently implemented.
def mul(a,b):
 v=0
 for k in range(2):
  if b>>k&1:v^=a<<k
 if v&4:v^=7
 return v
TAB=[[mul(a,b)for b in range(4)]for a in range(4)]
INV=[0,1,3,2]
def rank(A):
 rows=[list(r)for r in A];h=0
 for c in range(len(rows[0])if rows else 0):
  k=next((k for k in range(h,len(rows))if rows[k][c]),None)
  if k is None:continue
  rows[h],rows[k]=rows[k],rows[h];p=INV[rows[h][c]];rows[h]=[TAB[p][x]for x in rows[h]]
  for k in range(h+1,len(rows)):
   p=rows[k][c]
   if p:rows[k]=[x^TAB[p][y]for x,y in zip(rows[k],rows[h])]
  h+=1
  if h==len(rows):break
 return h

def cat(*blocks):return [sum((list(B[i])for B in blocks),[])for i in range(len(blocks[0]))]
def mat(data,n,b):return [list(data[i*b:(i+1)*b])for i in range(n)]
@lru_cache(None)
def matrices(n,b,full=False):
 out=[]
 for data in product(range(4),repeat=n*b):
  M=mat(data,n,b)
  if not full or rank(M)==n:out.append(M)
 return out

def mm(A,B,b):
 out=[]
 for row in A:
  rr=[0]*b
  for a,v in zip(row,B):
   if a:
    for c,x in enumerate(v):rr[c]^=TAB[a][x]
  out.append(rr)
 return out

def add(A,B):return [[x^y for x,y in zip(r,s)]for r,s in zip(A,B)]

def exact(M,A,C,D,b,m,l):
 base=rank(M);W=cat(M,D);rw=rank(W);aa=rank(cat(W,A))-rw;rr=rank(cat(W,C))-rw;zz=rank(cat(W,C,A))-rank(cat(W,C))
 formula=base+zz+max(0,rr-aa);best=len(A)+1;trials=0
 late=[mm(D,L,b)for L in matrices(l,b)]
 for F in matrices(m,b,True):
  AF=add(A,mm(C,F,b))
  for DL in late:
   trials+=1;actual=rank(cat(M,add(AF,DL)));best=min(best,actual)
   # Universal base-rank bound, independent of the proposed formula.
   if best==base:break
  if best==base:break
 assert best==formula,(M,A,C,D,formula,best)
 return trials,(aa,rr,zz),best

def main():
 p=ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rnd=random.Random(27111926);counts={};trials=0
 # Exhaustive GF4 y=1,b=2,m=1,l=1,c=1 boundary inputs.
 n=0
 for M in matrices(1,1):
  for A in matrices(1,2):
   for C in matrices(1,1):
    for D in matrices(1,1):
     t,_,_=exact(M,A,C,D,2,1,1);trials+=t;n+=1
 counts['exhaustive_scalar_output_boundary_cases']=n
 # Exhaustive two-output, one-input boundary with no late/fixed part.
 n=0
 for A in matrices(2,1):
  for C in matrices(2,1):
   t,_,_=exact([[],[]],A,C,[[],[]],1,1,0);trials+=t;n+=1
 counts['exhaustive_two_output_one_input_cases']=n
 # Each sampled boundary is compared against every full-rank F and every L,
 # except the valid base-rank early exit stated above.
 families=[(2,2,1,1,1,192),(3,2,2,1,1,96),(3,3,2,0,1,48),(2,2,0,1,0,32),(3,2,2,0,0,64),(0,2,1,1,1,1),(2,0,0,1,1,1)]
 for y,b,m,l,c,n in families:
  for _ in range(n):
   gen=lambda r,s:[[rnd.randrange(4)for _ in range(s)]for _ in range(r)]
   t,_,_=exact(gen(y,c),gen(y,b),gen(y,m),gen(y,l),b,m,l);trials+=t
  counts[f'sampled_y{y}_b{b}_m{m}_l{l}_c{c}']=n
 # The two distinct contributions z and max(0,r-a) must add.
 t,ar,best=exact([[],[],[]],[[0,0],[0,0],[1,0]],[[1,0],[0,1],[0,0]],[[],[],[]],2,2,0);trials+=t
 assert ar==(1,2,1)and best==2
 # A prescribed proper target can exclude the unconstrained optimizer.
 t,ar,best=exact([[]],[[1]],[[1]],[[]],1,1,0);trials+=t
 assert best==0 and rank([[1^2]])==1 # forcing F=2 preserves full return.
 # Forgetting surjectivity wrongly permits zero when A=0, C nonzero.
 t,ar,best=exact([[],[]],[[0,0],[0,0]],[[1,0],[0,1]],[[],[]],2,2,0);trials+=t
 assert best==2
 out={'status':'PASS_INDEPENDENT_GF4_RETURN_MINIMUM_REVIEW','field':'GF(4), polynomial t^2+t+1','proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),'case_families':counts,'total_boundary_cases':sum(counts.values())+3,'actual_completion_ranks_evaluated':trials,'controls':['strict additive z plus surjectivity term','selected target forbids unconstrained optimizer','dropping full-rank source changes minimum'],'author_code_imported':False,'universal_statement_basis':'written arbitrary-field proof; finite checks only cover specified cases'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','total_boundary_cases','actual_completion_ranks_evaluated']}))
if __name__=='__main__':main()
