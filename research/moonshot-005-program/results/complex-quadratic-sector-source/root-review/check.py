#!/usr/bin/env python3
"""Independent free-algebra and symplectic review; no author imports."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
def red(w):
 out=[]
 for x in w:
  if out and (out[-1],x) in [('a','A'),('A','a'),('k','k')]:out.pop()
  else:out.append(x)
 return tuple(out)
def add(*xs):
 out={}
 for x in xs:
  for w,c in x.items():out[w]=out.get(w,F(0))+c
 return {w:c for w,c in out.items() if c}
def scale(x,c):return {w:c*v for w,v in x.items() if c*v}
def mul(x,y):
 out={}
 for w,c in x.items():
  for v,d in y.items():
   z=red(w+v);out[z]=out.get(z,F(0))+c*d
 return {w:c for w,c in out.items() if c}
def mm(X,Y):return [[add(*(mul(X[i][k],Y[k][j]) for k in range(len(Y)))) for j in range(len(Y[0]))] for i in range(len(X))]
def ma(X,Y):return [[add(x,y) for x,y in zip(r,s)] for r,s in zip(X,Y)]
one={():F(1)};zero={};a={('a',):F(1)};ai={('A',):F(1)};k={('k',):F(1)}
neg=scale(one,-1);h=mul(mul(a,k),ai);a2=mul(a,a);b=mul(mul(a,k),a)
p=scale(add(one,h),F(1,2));q=scale(add(one,scale(h,-1)),F(1,2));v=scale(add(one,scale(k,-1)),F(1,2))
I=[[one if i==j else zero for j in range(3)] for i in range(3)]
K=[[one,zero,add(a,neg)],[a,zero,scale(a,-1)],[one,one,neg]]
C=[[p,zero,q],[zero,one,zero],[q,zero,p]]
Q=[[one,zero,add(one,scale(k,-1))],[zero,one,zero],[one,zero,one]]
W=K
for X in [C,K,Q,K]:W=mm(W,X)
W2=[[mul(a2,add(one,v)),mul(a2,v),add(b,scale(mul(a2,add(one,v)),-1))],[mul(a2,k),mul(a2,k),scale(mul(a2,k),-1)],[zero,zero,b]]
W3=[[zero,zero,mul(mul(a2,v),a)],[zero,zero,mul(mul(a2,k),a)],[zero,zero,zero]]
assert W==ma(W2,W3)
R=[[add(one,v),v,scale(add(one,v),-1)],[k,k,scale(k,-1)],[zero,zero,one]]
Ri=[[one,scale(mul(v,k),-1),one],[neg,mul(add(one,v),k),zero],[zero,zero,one]]
assert mm(R,Ri)==mm(Ri,R)==I
D=[[a2,zero,zero],[zero,a2,zero],[zero,zero,b]]
Di=[[mul(ai,ai),zero,zero],[zero,mul(ai,ai),zero],[zero,zero,mul(mul(ai,k),ai)]]
E=[[one,zero,neg],[zero,one,zero],[zero,zero,one]]
Wi=mm(mm(Ri,Di),E)
assert mm(W2,Wi)==mm(Wi,W2)==I
shear=[[one,zero,zero],[zero,one,a],[zero,zero,one]]
assert mm(E,W)==mm(mm(D,R),shear)
def elementary(i,j,c):
 M=[[dict(x) for x in row] for row in I];M[i][j]=add(M[i][j],scale(one,c));return M
def diag(x,y,z):return [[x,zero,zero],[zero,y,zero],[zero,zero,z]]
ops=[elementary(0,2,1),diag(one,one,scale(one,-2)),elementary(2,0,1),diag(one,one,h),elementary(2,0,-1),diag(one,one,scale(one,F(-1,2))),elementary(0,2,-1)]
got=I
for X in ops:got=mm(X,got)
assert got==C
mutants=[]
for removed in [1,3,5]:
 got=I
 for i,X in enumerate(ops):
  if i!=removed:got=mm(X,got)
 assert got!=C;mutants.append(removed)
got=I
for X in [elementary(0,2,1),diag(one,one,k),elementary(0,2,-1),elementary(2,0,1)]:got=mm(X,got)
assert got==Q
# Independent binary symplectic action, coordinates(x_a,x_b,x_c,z_a,z_b,z_c).
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def bm(X,Y):return [[sum(x*y for x,y in zip(row,col))%2 for col in zip(*Y)] for row in X]
def brank(M):
 rows=[sum(v<<j for j,v in enumerate(row)) for row in M];piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
def grank(M):return brank([row[3:] for row in M[:3]])
Cb=eye(6);Cb[1][4]=1
Db=eye(6);Db[4][1]=1
H=eye(6);H[3][2]=H[5][0]=1
J=eye(6);J[3][1]=J[4][0]=1
P=[[0]*6 for _ in range(6)]
for i,j in enumerate([2,0,1]):P[j][i]=P[j+3][i+3]=1
A=bm(bm(bm(Cb,Db),H),P);A2=bm(A,A);A3=bm(A2,A)
assert bm(H,A)==bm(A,J)
heads={'A':A,'A2':A2,'A3':A3,'AJA':bm(bm(A,J),A),'A2JA':bm(bm(A2,J),A)}
ranks={n:grank(M) for n,M in heads.items()}
assert list(ranks.values())==[1,2,3,2,3]
assert A3!=heads['A2JA']
out={'status':'PASS_ROOT_QUADRATIC_SECTOR_REVIEW','universal_identity_model':'free product of infinite cyclic a with involution k; h=a k a^-1',
 'source_identity':True,'W2_explicit_inverse':True,'normal_form':True,'primitive_C_and_Q':True,
 'removed_C_instruction_controls':mutants,'actual_head_binary_symplectic_ranks':ranks,
 'actual_cubic_heads_have_distinct_symplectic_actions':True,
 'component_physical_rank_multipliers':{'2':3,'3':1},'independent_endpoint_bank_count':3,
 'ordinary_equivalence_to_any_three_independent_Clifford_jobs':False,
 'scope':'fixed collective Clifford algebra at faithful widths; no arbitrary columnwise operations admitted',
 'new_complete_kappa':False}
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
