"""Evaluate the first Witt carry and compare with signed literal Z/4 remainders."""
from functools import lru_cache
from random import Random
import json


def rem(a, g):
    while a.bit_length() >= g.bit_length():
        a ^= g << (a.bit_length()-g.bit_length())
    return a


def mul(a, b, g):
    h = 0
    while a:
        if a & 1:
            h ^= b
        a >>= 1
        b <<= 1
    return rem(h, g)


def inverse(a, g):
    assert a
    r, t = 1, (1<<(g.bit_length()-1))-2
    while t:
        if t & 1:
            r = mul(r,a,g)
        a = mul(a,a,g)
        t >>= 1
    return r


def halves(f):
    a, b = 0, 0
    for i in range(f.bit_length()):
        if f>>i&1:
            if i&1:
                b ^= 1<<(i//2)
            else:
                a ^= 1<<(i//2)
    return a,b


def derivative(f):
    return sum((f>>i&1)<<(i-1) for i in range(1,f.bit_length(),2))


def half_square(f):
    h=0
    while f:
        bit = f & -f
        f ^= bit
        h ^= f << (bit.bit_length()-1)
    return h


def packed_half(f):
    width = (f.bit_length()+1).bit_length()+1
    z = sum((f>>i&1)<<(width*i) for i in range(f.bit_length()))
    z *= z
    return sum((z>>(width*i+1)&1)<<i for i in range(2*f.bit_length()))


@lru_cache(None)
def sqrt_z(g):
    a,b = halves(g)
    return mul(a,inverse(rem(b,g),g),g)


@lru_cache(None)
def sqrt_g(a,g):
    u,v = halves(a)
    c = rem(u,g)^mul(sqrt_z(g),v,g)
    assert mul(c,c,g)==rem(a,g)
    return c


@lru_cache(None)
def shift(g):
    h = sqrt_g(rem(half_square(g),g),g)
    return mul(h,inverse(rem(derivative(g),g),g),g)


def irreducibles(b):
    gs = []
    for d in range(1,b+1):
        if b%d:
            continue
        for g in range(1<<d,2<<d):
            if all(rem(g,h) for i in range(1,d//2+1) for h in range(1<<i,2<<i)):
                gs.append(g)
    assert sum(g.bit_length()-1 for g in gs)==1<<b
    return gs


@lru_cache(None)
def columns(g,n):
    """Signed ordinary monic division of each successive monomial."""
    d = g.bit_length()-1
    x = [1]+[0]*(d-1)
    out = []
    for _ in range(n):
        out.append(tuple(x))
        lead=x[-1]
        x=[(t-lead*(g>>j&1))%4 for j,t in enumerate([0]+x[:-1])]
    return out


def actual(f,g,n,hi=0):
    col=columns(g,n)
    v=[0]*(g.bit_length()-1)
    bits=f|hi
    while bits:
        bit=bits&-bits
        bits ^= bit
        j=bit.bit_length()-1
        c=(f>>j&1)+2*(hi>>j&1)
        v=[x+c*y for x,y in zip(v,col[j])]
    return sum((x&1)<<i for i,x in enumerate(v)),sum((x>>1&1)<<i for i,x in enumerate(v))


def main():
    rng=Random(812003)
    counts=dict(binary_inputs=0,factor_checks=0,all_mod4_factor_checks=0,
                halfsquare_packed_checks=0,proper_subfield_checks=0,first_examples={})
    for b in (1,2,3,4,6):
        q=1<<b
        gs=irreducibles(b)
        inputs=(range(1<<q) if b<=4 else
                list(range(32))+[(1<<q)-1]+[1<<i for i in range(q)]+
                [(1<<i)|(1<<j) for i in range(q) for j in range(i)]+
                [rng.getrandbits(q) for _ in range(96)])
        for f in inputs:
            h=half_square(f)
            assert h==packed_half(f)
            counts['halfsquare_packed_checks']+=1
            counts['binary_inputs']+=1
            for g in gs:
                d=g.bit_length()-1
                r,oracle=actual(f,g,q)
                assert r==rem(f,g)
                lr=rem(half_square(r),g)
                core=rem(h,g)^lr
                df,dr=rem(derivative(f),g),rem(derivative(r),g)
                transport=mul(shift(g),df^dr,g)
                pred=sqrt_g(core,g)^transport
                assert pred==oracle,(b,f,g,oracle,pred)
                counts['factor_checks']+=1
                if 1<d<b:
                    counts['proper_subfield_checks']+=1
                    for name,wrong in (
                            ('omit_local_half',sqrt_g(rem(h,g),g)^transport),
                            ('omit_literal_shift',sqrt_g(core,g)),
                            ('omit_input_derivative',sqrt_g(core,g)^mul(shift(g),dr,g)),
                            ('omit_residue_derivative',sqrt_g(core,g)^mul(shift(g),df,g)),
                            ('omit_inverse_frobenius',core^transport)):
                        if wrong!=oracle and name not in counts['first_examples']:
                            counts['first_examples'][name]=dict(b=b,g=g,F=f,correct=oracle,wrong=wrong)
                if b<=3:
                    for hi in range(1<<q):
                        assert actual(f,g,q,hi)==(r,pred^rem(hi,g))
                        counts['all_mod4_factor_checks']+=1
    assert len(counts['first_examples'])==5
    print(json.dumps(counts,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
