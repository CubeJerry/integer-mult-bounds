#!/usr/bin/env python3
"""Exact arbitrary-head source-cycle controls, independent of author code."""
from pathlib import Path
import json

def apply(A,x):
 y=0
 while x:
  b=x&-x;y^=A[b.bit_length()-1];x^=b
 return y
def mul(A,B):return tuple(apply(A,b)for b in B)
def rank(A):
 p={}
 for x in A:
  while x:
   b=x.bit_length()-1
   if b in p:x^=p[b]
   else:p[b]=x;break
 return len(p)
rows=[]
for d in range(2,13):
 perm=[(j-1)%d for j in range(d)];A=tuple(1<<p for p in perm)+tuple((1<<(d+p))^((1<<1)if p==1 else 0)for p in perm);I=tuple(1<<j for j in range(2*d));powers=[I]
 for k in range(1,2*d+1):powers.append(mul(A,powers[-1]))
 assert powers[-1]==I and len(set(powers[:-1]))==2*d
 mask=(1<<d)-1;ranks=[rank([x&mask for x in P[d:]])for P in powers[:-1]];expected=[min(k,2*d-k)for k in range(2*d)];assert ranks==expected
 signs=[1]*d+[-1]*d;reflect=[(d-1-j)%(2*d)for j in range(2*d)]
 assert all(signs[j]==signs[reflect[j]]for j in range(2*d))
 difference=[sum(signs[j]!=signs[(j+k)%(2*d)]for j in range(2*d))for k in range(2*d)];assert difference==[2*r for r in expected]
 rows.append({'head_dimension':d,'symplectic_order':2*d,'power_gaussian_ranks':ranks,'difference_ranks':difference,'reflection_preserves_sign_arcs':True})
out={'status':'PASS_ROOT_FIXED_HEAD_CYCLIC_CONTROLS','dimensions':rows,'scope':'Finite exact controls supplement universal commuting-source and even-cycle proof; fixed d only; no new kappa'};Path(__file__).with_name('ALL-HEAD-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'head_dimensions_checked':len(rows)}))
