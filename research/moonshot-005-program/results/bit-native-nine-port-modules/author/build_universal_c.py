#!/usr/bin/env python3
"""Discover one universal 18x18 crosswave; checker validates all minors."""
from __future__ import annotations
import itertools
import json
import pathlib
import numpy as np
from check import mul,power

def kernel(a):
    a=[list(r) for r in a]
    n=len(a[0]); piv=[]; p=0
    for j in range(n):
        k=next((k for k in range(p,len(a)) if a[k][j]),None)
        if k is None: continue
        a[p],a[k]=a[k],a[p]
        inv=power(a[p][j],30)
        a[p]=[mul(inv,x) for x in a[p]]
        for k in range(len(a)):
            if k!=p and a[k][j]:
                v=a[k][j]
                a[k]=[x^mul(v,y) for x,y in zip(a[k],a[p])]
        piv.append(j);p+=1
        if p==len(a):break
    free=[j for j in range(n) if j not in piv]
    out=[]
    for j in free:
        v=[0]*n;v[j]=1
        for k,c in enumerate(piv):v[c]=a[k][j]
        out.append(v)
    return out

def main():
    v=[[power(a,j) for j in range(18)] for a in range(1,19)]
    coeff=[]
    for pp in itertools.combinations(range(9),3):
        rows=[2*p+s for p in pp for s in (0,1)]
        for j in range(2):
            n=kernel([[v[r][9*j+c] for c in range(9)] for r in rows])
            l=kernel([[v[r][3*j+c] for r in rows] for c in range(3)])
            assert len(n)==len(l)==3
            weights=np.zeros((3,3,18,18),dtype=np.uint8)
            for a in range(3):
                for b in range(3):
                    for t,r in enumerate(rows):
                        for c in range(9):
                            weights[a,b,r,9*j+c]=mul(l[a][t],n[b][c])
            coeff.append(weights.reshape((3,3,324)))
    coeff=np.array(coeff,dtype=np.uint8)
    product=np.array([[mul(a,b)for b in range(32)]for a in range(32)],dtype=np.uint8)
    state=0x6e696e652d706f72
    def nextword():
        nonlocal state
        state ^= (state<<13)&((1<<64)-1)
        state ^= state>>7
        state ^= (state<<17)&((1<<64)-1)
        state &= (1<<64)-1
        return state
    attempt=0
    while True:
        attempt+=1
        c=np.array([nextword()&31 for _ in range(324)],dtype=np.uint8)
        a=np.bitwise_xor.reduce(product[coeff,c],axis=3)
        det=np.zeros(168,dtype=np.uint8)
        for p in itertools.permutations(range(3)):
            det ^= product[product[a[:,0,p[0]],a[:,1,p[1]]],a[:,2,p[2]]]
        if np.all(det):
            out={'field_polynomial':'z^5+z^2+1','seed_hex':'6e696e652d706f72','attempt':attempt,'matrix':c.reshape((18,18)).tolist(),'all_168_reduced_determinants':det.tolist()}
            (pathlib.Path(__file__).parent/'UNIVERSAL-C.json').write_text(json.dumps(out,indent=2)+'\n')
            print('SUCCESS',attempt)
            return
        if attempt%100==0:print('attempt',attempt,flush=True)

if __name__=='__main__':main()
