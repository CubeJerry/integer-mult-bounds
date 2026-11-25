#!/usr/bin/env python3
"""Exact finite spectral-rank tests; no general-machine lower bound."""
from itertools import product
from pathlib import Path
import json, random


def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return r


def power(a,n):
    r=1
    for _ in range(n%3 if a else n):r=mul(r,a)
    return r


def rank(a):
    a=[r[:] for r in a];k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];iv=mul(a[k][j],a[k][j])
        a[k]=[mul(x,iv) for x in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                v=a[i][j];a[i]=[x^mul(v,y) for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k


def add(a,b):return [[x^y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[mul(x,c) for x in r] for r in a]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):
    out=[]
    for row in a:
        rr=[]
        for j in range(len(b[0])):
            z=0
            for k in range(len(b)):z^=mul(row[k],b[k][j])
            rr.append(z)
        out.append(rr)
    return out


def neighbors(q):
    for j in range(len(q)):
        for val in (1,2,3):
            if val!=q[j]:
                r=list(q);r[j]=val;yield j,tuple(r)


def run():
    counts=dict(product_difference_bounds=0, rectangular_program_bounds=0,
                approximate_rank_bounds=0, predictor_essential_coordinates=0,
                constant_spectrum_controls=0)
    rng=random.Random(95317)
    def rm(n,m):return [[rng.randrange(4) for _ in range(m)] for _ in range(n)]
    for case in range(8):
        w,m=4,3;factors=[]
        for t in range(3):
            coeff=[mm(rm(w,1),rm(1,w)) for _ in range(m)]
            a0=rm(w,w) if case%2 else [[0]*w for _ in range(w)]
            factors.append((a0,coeff,1+t%2))
        prices=[sum(rank(co[j]) for _,co,_ in factors) for j in range(m)]
        vals={}
        for q in product((1,2,3),repeat=m):
            p=ident(w)
            for a0,co,ex in factors:
                f=a0
                for j in range(m):f=add(f,scale(co[j],power(q[j],ex)))
                p=mm(f,p)
            vals[q]=p
        for q in vals:
            for j,r in neighbors(q):
                assert rank(add(vals[q],vals[r]))<=prices[j]
                counts['product_difference_bounds']+=1
    for case in range(4):
        n,w,m=6,4,2
        injection=rm(n,w);projection=rm(w,n);mixers=[rm(n,n) for _ in range(4)]
        vals={}
        for q in product((1,2,3),repeat=m):
            p=injection
            for t,mix in enumerate(mixers):
                d=ident(n);d[t][t]=q[t%2]
                p=mm(mix,mm(d,p))
            vals[q]=mm(projection,p)
        for q in vals:
            for j,r in neighbors(q):
                assert rank(add(vals[q],vals[r]))<=2
                counts['rectangular_program_bounds']+=1
    w,m,rerr=8,3,2;vals={}
    for q in product((1,2,3),repeat=m):
        scalar=1
        for x in q:scalar=mul(scalar,x)
        target=scale(ident(w),scalar);actual=[r[:] for r in target]
        start=sum((i+1)*x for i,x in enumerate(q))%w
        for i in range(rerr):actual[(start+i)%w][(start+i)%w]^=1
        assert rank(add(actual,target))==rerr
        vals[q]=actual
    for q in vals:
        for j,r in neighbors(q):
            assert rank(add(vals[q],vals[r]))>=w-2*rerr
            counts['approximate_rank_bounds']+=1
    for t in (2,4,8,16):
        m=max(2,t-1)
        for u in range(-t,t+1):
            for j in range(m):
                f=lambda c:power(2,(c-u)%t)
                assert f(0)!=f(1) or f(1)!=f(2)
                counts['predictor_essential_coordinates']+=1
    for m in range(3,7):
        vals={}
        for q in product((1,2,3),repeat=m):
            val=1
            for x in q:val^=power(x,3)^1
            assert val==1;vals[q]=val
        for q in vals:
            for j,r in neighbors(q):
                assert vals[q]==vals[r]
                counts['constant_spectrum_controls']+=1
    return dict(status='pass',counts=counts,
                scope='separate scalar-query rank; fixed linear programs and finite spectra only')


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('spectral-query-rank-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
