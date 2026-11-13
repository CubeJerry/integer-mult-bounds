"""Exact controls for the ordered proof; no source census claim."""
import json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def add(A,B):return [[a^b for a,b in zip(r,s)] for r,s in zip(A,B)]
def mul(A,B):return [[sum(a*B[k][j] for k,a in enumerate(r))%2 for j in range(len(B[0]))] for r in A]
def inv(A):
 n=len(A);R=[r.copy()+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  p=next(i for i in range(j,n) if R[i][j]);R[j],R[p]=R[p],R[j]
  for i in range(n):
   if i!=j and R[i][j]:R[i]=[x^y for x,y in zip(R[i],R[j])]
 return [r[n:] for r in R]
I=[[1,0],[0,1]];U=[[[1,1],[0,1]],[[1,0],[1,1]],I];assert mul(U[0],U[1])!=mul(U[1],U[0])
L=[[[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0]],[[0,1,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],[[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]]
charts=[set(range(4)),{0,1},{0},set()];z0=[[1,0,0,0,1,0,0,0],[0,1,0,0,0,0,1,0]];states=[z0]
for u,l in zip(U,L):states.append(add(mul(u,states[-1]),l))
P=[None]*4;P[3]=I
for s in range(2,-1,-1):P[s]=mul(P[s+1],U[s])
checks=[]
for s in range(4):
 local=[[0]*8 for _ in range(2)]
 for t in range(s,3):local=add(local,mul(mul(inv(P[s]),P[t+1]),L[t]))
 assert add(mul(inv(P[s]),states[-1]),local)==states[s]
 support={j for row in local for j,v in enumerate(row) if v};assert support<=charts[s]
 checks.append({'read_index':s,'future_local_support':sorted(support),'ordered_identity':True})
wrong=mul(U[0],U[1]);assert wrong!=P[0]
correctlocal=add(states[0],mul(inv(P[0]),states[-1]));assert add(mul(inv(wrong),states[-1]),correctlocal)!=states[0]
out={'status':'PASS_ORDERED_BLOCK_IDENTITY_CONTROLS','field':'GF2','block_size':2,'noncommuting_units':True,'read_checks':checks,'commuted_product_rejected':True,'scope':'Concrete controls supporting written all-V proof; actual E7 geometry is a separately reviewed dependency.'}
p=Path(__file__).resolve().parent;(p/'ORDERED-ALGEBRA-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
