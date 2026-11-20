"""Independent binary-polynomial and native four-copy data conversion."""
import numpy as np
from functools import lru_cache
N=(1<<24)-1
POLY=0x100001b
RECIP=sum(((POLY>>i)&1)<<(24-i) for i in range(25))
def reduce(a,f):
    while a.bit_length()>=f.bit_length():a^=f<<(a.bit_length()-f.bit_length())
    return a
def product(a,b,f):
    x=0
    while b:
        lo=b&-b;x^=a<<(lo.bit_length()-1);b^=lo
    return reduce(x,f)
def powr(x,k,f):
    y=1
    while k:
        if k&1:y=product(y,x,f)
        x=product(x,x,f);k>>=1
    return y
def lookup(cols):
    return np.array([[sumxor(cols[t*8+j]for j in range(8)if k>>j&1)for k in range(256)]for t in range(3)],dtype=np.uint32)
def sumxor(seq):
    s=0
    for v in seq:s^=v
    return s
def change(x,t):return t[0,x&255]^t[1,(x>>8)&255]^t[2,(x>>16)&255]
def inverse_columns(cols):
    rows=[sum(((v>>j)&1)<<i for i,v in enumerate(cols))|(1<<(24+j)) for j in range(24)]
    for c in range(24):
        k=next(u for u in range(c,24)if rows[u]>>c&1);rows[c],rows[k]=rows[k],rows[c]
        for u in range(24):
            if u!=c and rows[u]>>c&1:rows[u]^=rows[c]
    return [sum(((r>>(j+24))&1)<<i for i,r in enumerate(rows))for j in range(24)]
class Basis:
    def __init__(self):
        assert all(powr(2,N//p,POLY)!=1 for p in (3,5,7,13,17,241))and powr(2,N,POLY)==1
        u=1519883;assert powr(u,6,POLY)^u^1==0
        self.native=[product(1<<h,powr(u,j,POLY),POLY)for h in range(4)for j in range(6)]
        self.fwd=lookup(self.native);self.inv=lookup(inverse_columns(self.native))
        rinv=powr(2,N-1,RECIP);assert product(rinv,2,RECIP)==1
        self.rec=lookup([powr(rinv,j,RECIP)for j in range(24)])
        self.rr=lookup(inverse_columns([powr(rinv,j,RECIP)for j in range(24)]))
        assert np.array_equal(change(change(np.arange(1<<16,dtype=np.uint32),self.rec),self.rr),np.arange(1<<16,dtype=np.uint32))
    def wrap(self,limbs):
        s=limbs.astype(np.uint32)
        return change(s[...,0]^(s[...,1]<<6)^(s[...,2]<<12)^(s[...,3]<<18),self.fwd)
    def limbs(self,x):
        q=change(x,self.inv)
        return np.stack([(q>>(6*l))&63 for l in range(4)],axis=-1).astype(np.uint8)
    def times_x(self,x):
        return ((x<<1)&N)^np.where(x&(1<<23),27,0).astype(np.uint32)
    def matrix(self,F):
        r=[]
        for t in range(4):
            r.append(self.limbs(F));F=self.times_x(F)
        return np.stack(r,axis=-1)
