# Exact rational row-space routines. @CubeJerry with OpenAI assistance. Apache-2.0.
import collections,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b,c=Q(1)):
 for j,v in b.items():
  z=a.get(j,Q(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def span(a):
 s={0}
 for x in a:s.update(x^v for v in tuple(s))
 return frozenset(s)
def put(B,row):
 a=row.copy()
 while a:
  p=max(a)
  if p in B:add(a,B[p],-a[p])
  else:
   z=a[p];B[p]={j:v/z for j,v in a.items()};return True
 return False
def basis(rows):
 B={}
 for r in rows:put(B,r)
 return B
def reduce(r,B):
 z=r.copy()
 for p in sorted(B,reverse=True):
  if p in z:add(z,B[p],-z[p])
 return z
def intersection(rows,B):
 U={};out=[]
 for row in basis(rows).values():
  a=reduce(row,B);x=row.copy()
  while a:
   p=max(a)
   if p not in U:
    z=a[p];U[p]=({j:v/z for j,v in a.items()},{j:v/z for j,v in x.items()});break
   ar,xr=U[p];c=-a[p];add(a,ar,c);add(x,xr,c)
  if not a and x:out.append(x)
 return basis(out)
def serial(rows):return [{str(j):str(c) for j,c in sorted(r.items())} for r in rows]

def reps(data):
 B={}
 for j,row in data.items():
  a=row.copy();c={j:Q(1)}
  while a:
   p=max(a)
   if p not in B:
    z=a[p];B[p]=({k:v/z for k,v in a.items()},{k:v/z for k,v in c.items()});break
   b,d=B[p];z=-a[p];add(a,b,z);add(c,d,z)
 return B
def solve(r,B):
 a=r.copy();c={}
 for p,(b,d) in sorted(B.items(),reverse=True):
  if p in a:
   z=a[p];add(a,b,-z);add(c,d,z)
 need(not a,'not in supplied span');return c
def check(row,co,source):
 a={}
 for j,c in co.items():add(a,source[j],c)
 need(a==row,'representation')
def show(a):return {str(j):str(c) for j,c in sorted(a.items())}
