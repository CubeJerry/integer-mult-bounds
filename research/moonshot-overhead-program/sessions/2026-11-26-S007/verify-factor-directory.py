#!/usr/bin/env python3
"""Check the deterministic power-projection adapter and the two-plane/FS1 join."""

from functools import cache, reduce
from math import isqrt
from operator import xor
from pathlib import Path
import json
import random
import runpy

binary = runpy.run_path(str(Path(__file__).with_name('verify-grouped-words.py')))
pmul = binary['pmul']
pdiv = binary['pdiv']
pgcd = binary['pgcd']
invmod = binary['inverse_mod']
rank_rows = binary['left_inverse']


def degree(x):
    return x.bit_length()-1


def irreducible(p,d):
    xbar = pdiv(2,p)[1]
    z = xbar
    for i in range(1,d+1):
        z = pdiv(pmul(z,z),p)[1]
        if i<=d//2 and pgcd(z^xbar,p)!=1:
            return False
    return z==xbar


@cache
def field_modulus(d,alternate):
    choices = range((1<<d)+1,2<<d,2)
    if alternate:
        choices = reversed(choices)
    return next(p for p in choices if irreducible(p,d))


class Field:
    def __init__(self,d,alternate=False):
        self.b = d
        self.modulus = field_modulus(d,alternate)
        self.hankel = sum((pdiv(1<<i,self.modulus)[1]&1)<<i for i in range(2*d-1))

    def mul(self,a,b):
        return pdiv(pmul(a,b),self.modulus)[1]

    def pow(self,a,k):
        acc=1
        while k:
            if k&1: acc=self.mul(acc,a)
            a=self.mul(a,a)
            k//=2
        return acc

    def orbit(self,z):
        result=[z]
        out=self.mul(z,z)
        while out!=z:
            result.append(out)
            out=self.mul(out,out)
        return result

    def normal(self,allowed=None):
        choices=range((1<<self.b)-1,0,-1) if allowed is None else allowed
        for a in choices:
            orbit=self.orbit(a)
            try:
                rank_rows(orbit,self.b)
            except ValueError:
                continue
            if allowed is None and len(orbit)!=self.b:
                continue
            return orbit
        raise AssertionError('no normal element')

    def minimal_by_roots(self,z):
        poly=[1]
        for a in self.orbit(z):
            nxt=[0]*(len(poly)+1)
            for j,v in enumerate(poly):
                nxt[j]^=self.mul(v,a)
                nxt[j+1]^=v
            poly=nxt
        assert all(a in [0,1] for a in poly)
        return sum(a<<j for j,a in enumerate(poly))

    def horner(self,r,z):
        acc=0
        for i in reversed(range(r.bit_length())):
            acc=self.mul(acc,z)^((r>>i)&1)
        return acc


def lex_lyndons(k):
    w=[0]
    while w:
        yield tuple(w)
        n=len(w)
        while len(w)<k:
            w.append(w[len(w)%n])
        while w and w[-1]==1:
            w.pop()
        if w:
            w[-1]=1


def from_bits(bits,columns):
    return reduce(xor,(v for a,v in zip(bits,columns,strict=True) if a),0)


def fs1(b):
    table=[]
    for d in range(1,b+1):
        if b%d: continue
        ext=Field(d,True)
        basis=ext.normal()
        for key in lex_lyndons(d):
            if len(key)==d:
                z=from_bits(key,basis)
                u=ext.minimal_by_roots(z)
                assert degree(u)==d
                table.append((d,key,u))
    assert len({u for _,_,u in table})==len(table)
    assert sum(d for d,_,_ in table)==1<<b
    product=1
    for _,_,u in table:
        product=pmul(product,u)
    assert product==(1<<(1<<b))^2
    return table


def baby_powers(ext,z):
    b=ext.b
    s=isqrt(2*b-1)+1
    baby=[1]
    for _ in range(s-1):
        baby.append(ext.mul(baby[-1],z))
    return s,baby,ext.mul(baby[-1],z)


def moment_rows(ext,z,y):
    b=ext.b
    s,baby,base=baby_powers(ext,z)
    lowmask=(1<<b)-1
    def functional(a):
        # The row k -> constant(F^(-1)(a X^k)) is a single fixed Hankel product.
        rev=sum(((a>>i)&1)<<(b-1-i) for i in range(b))
        coefficients=(pmul(rev,ext.hankel)>>(b-1))&lowmask
        return [(coefficients&value).bit_count()%2 for value in baby]
    left=[]
    right=[]
    giant=1
    for _ in range(s):
        left.extend(functional(giant))
        right.extend(functional(ext.mul(y,giant)))
        giant=ext.mul(giant,base)
    return left[:2*b],right[:b]


def pade(seen,b):
    F=1<<(2*b)
    G=sum(v<<(2*b-1-j) for j,v in enumerate(seen))
    old,r=F,G
    u0,u1=1,0
    v0,v1=0,1
    while degree(r)>=b:
        q,nxt=pdiv(old,r)
        old,r=r,nxt
        u0,u1=u1,u0^pmul(q,u1)
        v0,v1=v1,v0^pmul(q,v1)
    assert r==pmul(u1,F)^pmul(v1,G)
    assert pgcd(u1,v1)==1 and degree(v1)<=b
    return v1,u1,r


def projected_remainder(ext,z,y):
    s,t=moment_rows(ext,z,y)
    m,a,residual=pade(s,ext.b)
    d=degree(m)
    tprefix=sum(t[j]<<(d-1-j) for j in range(d))
    num=pmul(tprefix,m)>>d
    return m,pdiv(pmul(num,invmod(a,m)),m)[1],residual


def compose(ext,r,z):
    s,baby,base=baby_powers(ext,z)
    blocks=[]
    for start in range(0,ext.b,s):
        blocks.append(reduce(xor,(baby[i] for i in range(s) if (r>>(start+i))&1),0))
    result=0
    for h in reversed(blocks):
        result=ext.mul(result,base)^h
    return result


def plane_order(ext,c):
    n=1<<c
    def trace(z): return z^ext.pow(z,n)^ext.pow(z,n*n)
    sub=[z for z in range(1<<ext.b) if ext.pow(z,n)==z]
    basis=next(ext.orbit(z) for z in sub if len(ext.orbit(z))==c and rank(ext.orbit(z))==c)
    word=lambda v:from_bits(((v>>(c-1-i))&1 for i in range(c)),basis)
    values=[word(v) for v in range(n)]
    to_word={z:i for i,z in enumerate(values)}
    assert len(sub)==n and values[-1]==1
    reps=[]
    for i in range(n//2):
        orbit={to_word[z] for root in (values[i],values[i]^1) for z in ext.orbit(root)}
        if i==min(orbit): reps.append(values[i])
    kernel=[z for z in range(1<<ext.b) if trace(z)==0]
    v=next(z for z in kernel if z)
    line={ext.mul(v,l) for l in sub}
    w=next(z for z in kernel if z not in line)
    ordered=[alpha^side^ext.mul(v,l)^ext.mul(w,r) for alpha in reps for side in [0,1] for l in values for r in values]
    assert len(ordered)==len(set(ordered))==2*len(reps)*n*n
    return reps,ordered


def rank(vectors):
    basis={}
    for v in vectors:
        while v:
            k=degree(v)
            if k not in basis:
                basis[k]=v
                break
            v^=basis[k]
    return len(basis)


def trial(c):
    b=3*c
    q=1<<b
    ext=Field(b)
    directory=fs1(b)
    reps,order=plane_order(ext,c)
    oracle={z:ext.minimal_by_roots(z) for z in order}
    assert set(oracle.values())=={m for _,_,m in directory}
    rng=random.Random(5871+983*c)
    modulus=(1<<q)^2
    first=[rng.getrandbits(d) for d,_,_ in directory]
    coefficients=0
    for (_,_,m),reply in zip(directory,first,strict=True):
        g,err=pdiv(modulus,m)
        assert not err
        inv=invmod(pdiv(g,m)[1],m)
        coefficients^=pmul(g,pdiv(pmul(inv,reply),m)[1])
    assert degree(coefficients)<q
    payload={m:r for (_,_,m),r in zip(directory,first,strict=True)}
    # Restore plane order from arbitrary canonical factor residues.
    points=[(z,compose(ext,payload[oracle[z]],z)) for z in order]
    probe=points if b<=9 else rng.sample(points,32)
    for z,y in probe:
        assert ext.horner(coefficients,z)==y
    for (_,_,m),r in zip(directory,first,strict=True):
        assert pdiv(coefficients,m)[1]==r
    # Run the two stable joins; duplicate geometric occurrences must agree.
    proposals=[]
    short=zero=wrong_pade=0
    for serial,(z,y) in enumerate(points):
        u,r,rest=projected_remainder(ext,z,y)
        assert u==oracle[z] and r==payload[u]
        assert y==ext.horner(r,z)
        proposals.append((u,serial,r))
        short+=degree(u)<b
        zero+=z==0 and u==2 and rest==0
        wrong_pade+=rest!=r
    grouped={}
    for u,serial,r in sorted(proposals):
        assert grouped.setdefault(u,r)==r
    recovered=[grouped[m] for _,_,m in directory]
    assert first==recovered and zero==1 and wrong_pade
    # An independently chosen ordinary coefficient input returns the true FS1 residues.
    poly=rng.getrandbits(q)
    replies={m:pdiv(poly,m)[1] for _,_,m in directory}
    for z in order:
        m=oracle[z]
        new_y=ext.horner(replies[m],z)
        assert projected_remainder(ext,z,new_y)[:2]==(m,replies[m])
    exhaustive = 0
    if b<=6:
        for z in range(q):
            u = ext.minimal_by_roots(z)
            for residue in range(1 << degree(u)):
                value = ext.horner(residue, z)
                assert projected_remainder(ext,z,value)[:2]==(u,residue)
                assert compose(ext,residue,z)==value
                exhaustive += 1
    # Functional selecting bit 1 vanishes on F2 in these ambient fields.
    # For z=1 it would have no recurrence information about X+1.
    bad_source=[(ext.pow(1,j)>>1)&1 for j in range(2*b)]
    assert not any(bad_source) and ext.minimal_by_roots(1)==3
    wrong_order=sum(a!=b for a,b in zip([m for _,_,m in directory],sorted(grouped),strict=True))
    return dict(b=b,c=c,raw_size=q,quotient_representatives=len(reps),points=len(points),
                true_FS1_factors=len(directory),duplicates=len(points)-len(directory),short_orbit_points=short,
                actual_ambient_polynomial=ext.modulus,independent_FS1_ambient_polynomial=field_modulus(b,True),
                direct_full_polynomial_samples=len(probe),inverse_first_bits=q,forward_first_bits=q,
                all_legal_value_pairs_in_small_ambient_fields=exhaustive,
                annihilating_invalid_functional_detected=True,
                first_below_cutoff_zero_for_x=zero,wrong_Euclidean_remainder_as_reply=wrong_pade,
                numerical_polynomial_sort_differs_at=wrong_order)


if __name__=='__main__':
    print(json.dumps([trial(c) for c in (1,2,3,4)],indent=2))
