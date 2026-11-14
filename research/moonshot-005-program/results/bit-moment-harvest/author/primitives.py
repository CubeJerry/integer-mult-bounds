#!/usr/bin/env python3
"""Exact binary rank and rational-chart primitives, shared source provenance."""
import argparse,gzip,hashlib,json,itertools
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(b,m):
 if not b:raise ValueError(m)
def rank(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def dot(a,b):return sum(F(x)*F(y) for x,y in zip(a,b))
def nullspace(A,n=8):
 a=[list(map(F,r)) for r in A];p=[]
 for c in range(n):
  h=next((h for h in range(len(p),len(a)) if a[h][c]),None)
  if h is None:continue
  k=len(p);a[k],a[h]=a[h],a[k];z=a[k][c];a[k]=[v/z for v in a[k]]
  for h in range(len(a)):
   if h!=k:
    z=a[h][c];a[h]=[u-z*v for u,v in zip(a[h],a[k])]
  p.append(c)
 out=[]
 for j in range(n):
  if j not in p:
   r=[F(0)]*n;r[j]=1
   for k,c in enumerate(p):r[c]=-a[k][j]
   out.append(r)
 return out
