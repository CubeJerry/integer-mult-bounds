#!/usr/bin/env python3
"""Integer/Fraction proof controls for the pentagon-cut rank representation."""
from fractions import Fraction
from pathlib import Path
import json

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n):return [[0]*n for _ in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def power(a,n):
 out=eye(len(a))
 for _ in range(n):out=mm(out,a)
 return out
def block(a,b,c,d):return [x+y for x,y in zip(a,b)]+[x+y for x,y in zip(c,d)]
def rank(a):
 a=[[Fraction(x) for x in row] for row in a];r=0
 for c in range(len(a[0])):
  k=next((j for j in range(r,len(a)) if a[j][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];s=a[r][c];a[r]=[x/s for x in a[r]]
  for j in range(r+1,len(a)):
   s=a[j][c]
   if s:a[j]=[x-s*y for x,y in zip(a[j],a[r])]
  r+=1
 return r
n=5;I=eye(n);Z=zero(n);R=zero(n);J=zero(n)
for j in range(n):R[(j+1)%n][j]=1;J[(-j-1)%n][j]=1
P=[[((1 if i in [0,4] else -1) if i==j else 0) for j in range(n)] for i in range(n)]
assert power(R,5)==I and mm(J,J)==I and mm(mm(J,R),J)==power(R,4)
assert mm(P,J)==mm(J,P)
g={(k,e):mm(power(R,k),power(J,e)) for k in range(5) for e in range(2)}
ranks={}
for (k,e),a in g.items():
 diff=rank(sub(a,mm(mm(P,a),P)));assert diff==2*[0,1,2,2,1][k];ranks[f'{k},{e}']=diff
 for (l,f),b in g.items():assert mm(a,b)==g[((k+(-1)**e*l)%5,(e+f)%2)]
P2=block(P,Z,Z,P);native=[]
for sig in [-1,1]:
 for eps in [-1,1]:
  for c in [-1,1]:
   a=power(R,sig%5);b=scale(power(R,(sig+eps)%5),c);m=block(a,b,Z,a)
   d=rank(sub(m,mm(mm(P2,m),P2)));assert d==4;native.append([sig,eps,c,d])
query_checks=0
for (k,e),a in g.items():
 for mode in ['inplace','shear']:
  m=block(a,Z,Z,I) if mode=='inplace' else block(I,a,Z,I)
  assert rank(sub(m,mm(mm(P2,m),P2)))==2*[0,1,2,2,1][k];query_checks+=1
Nplus=block(R,power(R,2),Z,R);Nminus=block(R,scale(power(R,2),-1),Z,R)
assert mm(Nplus,Nminus)==block(power(R,2),Z,Z,power(R,2))
assert rank(sub(mm(Nplus,Nminus),mm(mm(P2,mm(Nplus,Nminus)),P2)))==8
assert mm(P,R)!=mm(R,P) # Agreement would fail if the paid rotation were declared free.
out={'status':'PASS_EXACT_PENTAGON_CUT_CONSERVATION','arithmetic':'Python integers and exact Fraction elimination','group_products_checked':100,'difference_ranks':ranks,'native_checks':native,'query_mode_checks':query_checks,'sharp_control':{'native_halves':2,'total_endpoint_rank':4,'difference_rank':8},'ordinary_agreement_on_inverter':True,'false_free_rotation_rejected':True,'scope':'D10 coefficients and Mat(C[T]) ordinary encodings only; full monomial Clifford ordinary family remains open.','new_kappa':False}
path=Path(__file__).with_name('PENTAGON-GATE-RESULT.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
