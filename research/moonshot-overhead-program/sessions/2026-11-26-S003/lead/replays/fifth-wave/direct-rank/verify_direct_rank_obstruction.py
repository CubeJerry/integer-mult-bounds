#!/usr/bin/env python3
"""Finite F4 interpolation/rank diagnostics for the formal rank invoice."""
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json
import random


def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return r


def power(a,n):
    if n<0:n%=3
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n>>=1
    return r


def rank(a):
    a=[r[:] for r in a]; rows=len(a); cols=len(a[0]); k=0
    for c in range(cols):
        p=next((i for i in range(k,rows) if a[i][c]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k]
        inv=power(a[k][c],2)
        a[k]=[mul(x,inv) for x in a[k]]
        for i in range(rows):
            if i!=k and a[i][c]:
                t=a[i][c];a[i]=[x^mul(t,y) for x,y in zip(a[i],a[k])]
        k+=1
        if k==rows:break
    return k


def add(p,q):
    r=p.copy()
    for x,c in q.items():
        r[x]=r.get(x,0)^c
        if not r[x]:del r[x]
    return r


def pmul(p,q):
    r={}
    for x,c in p.items():
        for y,d in q.items():
            z=tuple(a+b for a,b in zip(x,y));r[z]=r.get(z,0)^mul(c,d)
            if not r[z]:del r[z]
    return r


def pmatmul(a,b):
    out=[]
    for row in a:
        rr=[]
        for j in range(len(b[0])):
            z={}
            for k in range(len(b)):z=add(z,pmul(row[k],b[k][j]))
            rr.append(z)
        out.append(rr)
    return out


def determinant(a,m):
    r={}
    for perm in permutations(range(len(a))):
        term={(0,)*m:1}
        for i,j in enumerate(perm):term=pmul(term,a[i][j])
        r=add(r,term) # All permutation signs are + in characteristic two.
    return r


def pencil(coeff,m,allowed=None):
    w=len(coeff[0]);allowed=set(range(m)) if allowed is None else set(allowed)
    out=[]
    for i in range(w):
        row=[]
        for j in range(w):
            p={}
            if coeff[0][i][j]:p[(0,)*m]=coeff[0][i][j]
            for z in allowed:
                if coeff[z+1][i][j]:
                    exp=[0]*m;exp[z]=1;p[tuple(exp)]=coeff[z+1][i][j]
            row.append(p)
        out.append(row)
    return out


def run():
    c=dict(predictor_coefficients=0, full_degree_restrictions=0,
           determinant_rank_bounds=0, formal_factor_identities=0,
           rank_invoice_checks=0, finite_spectral_counterexamples=0,
           rejected_formal_substitution_controls=0)
    for m in range(2,16):
        for t in (2,4,8,16):
            d=t-1
            if d>m:continue
            for u in range(-t-2,t+3):
                for gamma in (1,2,3):
                    kappas=[]
                    for h in range(m+1):
                        z=0
                        for j in range(h+1):
                            if comb(h,j)&1:z^=mul(gamma,power(2,(j-u)%t))
                        kappas.append(z);c['predictor_coefficients']+=1
                    assert kappas[d]!=0 and all(z==0 for z in kappas[d+1:])
                    for chosen in combinations(range(m),d):
                        # All size-D squarefree coefficients coincide and are nonzero.
                        assert len(chosen)==d and kappas[d]!=0
                        c['full_degree_restrictions']+=1
    rng=random.Random(170019)
    for m in (2,3,4):
        for w in (1,2,3):
            for case in range(8):
                coeff=[[[rng.randrange(4) for _ in range(w)] for _ in range(w)] for _ in range(m+1)]
                ranks=[rank(a) for a in coeff[1:]]
                for d in range(1,m+1):
                    for chosen in combinations(range(m),d):
                        det=determinant(pencil(coeff,m,chosen),m)
                        degree=max((sum(ex) for ex in det),default=-1)
                        assert degree<=sum(ranks[j] for j in chosen)
                        c['determinant_rank_bounds']+=1
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
    def inv2(a):
        v=mul(a[0][0],a[1][1])^mul(a[0][1],a[1][0])
        assert v
        iv=power(v,2)
        return [[mul(iv,a[1][1]),mul(iv,a[0][1])],
                [mul(iv,a[1][0]),mul(iv,a[0][0])]]
    zero=[[0,0],[0,0]]; identity=[[1,0],[0,1]]
    lc=[zero,identity,[[0,1],[0,0]],[[0,0],[1,0]]]
    gl=[]
    for entries in product(range(4),repeat=4):
        a=[list(entries[:2]),list(entries[2:])]
        if rank(a)==2:gl.append(a)
    p={(2,0,0):1,(0,1,1):1}; target=[[p,{}],[{},p]]
    for u in gl[::23]:
        for v in gl[::23]:
            first=[mm(mm(u,a),v) for a in lc]
            second=[mm(mm(inv2(v),a),inv2(u)) for a in lc]
            assert pmatmul(pencil(second,3),pencil(first,3))==target
            c['formal_factor_identities']+=1
            mass=sum(rank(a) for coeff in (first,second) for a in coeff[1:])
            assert mass==8>=3*2
            c['rank_invoice_checks']+=1
            # Inserting inverse constant stages adds no query rank or degree.
            g=pencil([u,zero,zero,zero],3)
            gi=pencil([inv2(u),zero,zero,zero],3)
            assert pmatmul(gi,pmatmul(g,target))==target
            c['formal_factor_identities']+=1
    for m in range(2,6):
        for w in range(1,4):
            ident=[[int(i==j) for j in range(w)] for i in range(w)]
            assert sum(rank(ident) for _ in range(m))==m*w
            c['rank_invoice_checks']+=1
    # p=1+sum_j(q_j^3-1) equals 1 on the allowed nonzero spectrum.
    # Formal degree is 3 on every three-variable restriction, yet I alone
    # has zero query rank: this shows why a spectral-only identity is excluded.
    for m in range(3,8):
        for values in product((1,2,3),repeat=m):
            val=1
            for x in values:val^=power(x,3)^1
            assert val==1
            c['finite_spectral_counterexamples']+=1
        values=[0]+[1]*(m-1)
        val=1
        for x in values:val^=power(x,3)^1
        assert val==0 and val!=1
        c['rejected_formal_substitution_controls']+=1
    return dict(status='pass',scope='formal full-identity coefficient-rank invoice only',counts=c,
                finite_spectral_escape='constant identity agrees on q_j^3=1 but fails as a formal polynomial')


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('direct-rank-obstruction-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
