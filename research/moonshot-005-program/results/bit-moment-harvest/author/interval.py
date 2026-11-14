#!/usr/bin/env python3
"""Rigorous 199/200 movement intervals for one actual partial word only."""
import argparse,json,hashlib
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
BITS=176;SCALE=1<<BITS

def need(b,m):
 if not b:raise ValueError(m)
def iroot(n,k):
 x=1<<((n.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+n//pow(x,k-1))//k
  if y>=x:break
  x=y
 while pow(x,k)>n:x-=1
 while pow(x+1,k)<=n:x+=1
 return x
_cache={}
def pow_interval(r):
 if r not in _cache:
  n=pow(r,199)*pow(SCALE,200);x=iroot(n,200)
  need(pow(x,200)<=n<pow(x+1,200),'exact integer-root enclosure')
  _cache[r]=(F(x,SCALE),F(x+1,SCALE))
 return _cache[r]
def measure(H):
 lo=F(0);hi=F(0)
 for r,c in H.items():
  a,b=pow_interval(r)
  if c>=0:lo+=c*a;hi+=c*b
  else:lo+=c*b;hi+=c*a
 return lo,hi

def add(A,B,weight=F(1)):
 C=dict(A)
 for r,v in B.items():C[r]=C.get(r,F(0))+weight*v
 return {r:v for r,v in C.items() if v}
def show(x):
 with localcontext() as c:
  c.prec=64;return str(Decimal(x.numerator)/Decimal(x.denominator))
def pack(I):return {'lower':show(I[0]),'upper':show(I[1]),'lower_rational':[str(I[0].numerator),str(I[0].denominator)],'upper_rational':[str(I[1].numerator),str(I[1].denominator)]}