#!/usr/bin/env python3
"""Recover the full ordinary divided square and arbitrary mod-four products from literal K1."""
from collections import Counter
from functools import cache
from pathlib import Path
from random import Random
import json
import runpy

binary = runpy.run_path(str(Path(__file__).with_name("verify-fibre-join.py")))
crt = runpy.run_path(str(Path(__file__).with_name("verify-trace-rader.py")))
mul = binary["xor_product"]
div = binary["divmod_binary"]
rem = lambda g,h: div(g,h)[1]


def parity_split(g):
    a = b = 0
    for i in range(g.bit_length()):
        if (g >> i) & 1:
            if i % 2:
                b |= 1 << (i//2)
            else:
                a |= 1 << (i//2)
    return a,b


def derivative(g):
    return mul(parity_split(g)[1],parity_split(g)[1])


def divided_square(g):
    if g < 2:
        return 0
    cut = (g.bit_length()+1)//2
    low = g & ((1 << cut)-1)
    high = g >> cut
    return divided_square(low) ^ (mul(low,high)<<cut) ^ (divided_square(high)<<(2*cut))


def literal_carry(f,h):
    """Monic long division of literal f by literal h mod four, using two coefficient bitplanes."""
    lo,hi = f,0
    while (lo|hi).bit_length()>=h.bit_length():
        top=(lo|hi).bit_length()-1
        mask=h << (top+1-h.bit_length())
        qlow=(lo>>top)&1
        qhigh=(hi>>top)&1
        if qhigh:
            hi ^= mask
        if qlow:
            hi ^= ~lo & mask
            lo ^= mask
    assert lo==rem(f,h)
    return hi


def slow_literal_carry(f,h):
    coeff=[(f>>i)&1 for i in range(f.bit_length())]
    degree=h.bit_length()-1
    for i in range(len(coeff)-1, degree-1, -1):
        q=coeff[i]
        for j in range(degree+1):
            coeff[i-degree+j]=(coeff[i-degree+j]-q*((h>>j)&1))%4
    return sum((x//2)<<i for i,x in enumerate(coeff[:degree]))


@cache
def factor_data(h):
    A,B=parity_split(h)
    square_x=rem(mul(A,binary["inverse_mod"](B,h)),h)
    assert rem(mul(square_x,square_x),h)==rem(2,h)
    def root(u):
        C,D=parity_split(rem(u,h))
        v=rem(C^mul(square_x,D),h)
        assert rem(mul(v,v),h)==rem(u,h)
        return v
    d=rem(mul(root(divided_square(h)),binary["inverse_mod"](derivative(h),h)),h)
    return d


@cache
def inventory(b):
    factors=binary["fs_order"](b)
    q=1 << b
    return factors,dict(zip(factors,crt["crt_idempotents"](factors,q),strict=True))


def from_first_carry(f,n,counts):
    if n==1:
        return 0
    b=max(3,3*((((2*n-2).bit_length())+2)//3))
    q=1 << b
    modulus=(1<<q)|2
    factors,idems=inventory(b)
    df=derivative(f)
    restored=0
    for h in factors:
        r=rem(f,h)
        dr=derivative(r)
        k=literal_carry(f,h)
        if b<=6:
            assert k==slow_literal_carry(f,h)
        shifted=k^rem(mul(factor_data(h),dr^rem(df,h)),h)
        quo=rem(mul(shifted,shifted)^divided_square(r),h)
        restored ^= rem(mul(idems[h],quo),modulus)
    counts["single_first_carry_calls"]+=1
    counts["actual_factor_carries_read"]+=len(factors)
    counts["distinct_root_degrees_used"]|={b}
    assert 2*n-1<=q and restored.bit_length()<=2*n-2
    return restored


def guarded_product(f0,f1,g0,g1,n):
    guard=(9*n).bit_length()
    def base(lo,hi):
        return sum((((lo>>i)&1)+2*((hi>>i)&1))<<(guard*i) for i in range(n))
    val=base(f0,f1)*base(g0,g1)
    lo=sum(((val>>(guard*j))&1)<<j for j in range(2*n-1))
    hi=sum(((val>>(guard*j+1))&1)<<j for j in range(2*n-1))
    return lo,hi


def unrestricted_product(f0,f1,g0,g1,n,counts):
    h=mul(f0,g0)
    bits = (from_first_carry(h,2*n-1,counts) ^
            mul(mul(f0,f0),from_first_carry(g0,n,counts)) ^
            mul(mul(g0,g0),from_first_carry(f0,n,counts)))
    high,odd=parity_split(bits)
    assert odd==0
    result=(h,high^mul(f0,g1)^mul(f1,g0))
    assert result==guarded_product(f0,f1,g0,g1,n)
    counts["complete_mod_four_products"]+=1
    counts["ordinary_coefficients_checked"]+=2*n-1


def main():
    rng=Random(0x1CA417)
    counts=Counter()
    counts["distinct_root_degrees_used"]=set()
    for n in (1,2,3,4,5,17,32,100,257,600):
        cases = ([(i,0,j,0) for i in range(1<<n) for j in range(1<<n)] if n<=2 else [])
        cases += [(rng.getrandbits(n),rng.getrandbits(n),rng.getrandbits(n),rng.getrandbits(n)),
                  ((1<<n)-1,(1<<n)-1,(1<<n)-1,(1<<n)-1)]
        for f0,f1,g0,g1 in cases:
            unrestricted_product(f0,f1,g0,g1,n,counts)
    for n in (1,3,4,5,32,140,700):
        cases=range(1<<n) if n<=5 else [rng.getrandbits(n), (1<<n)-1,1<<(n-1)]
        for f in cases:
            h=from_first_carry(f,n,counts)
            assert h==guarded_product(f,0,f,0,n)[1]
            counts["independent_ordinary_divided_squares"]+=1
    counts["distinct_root_degrees_used"]=sorted(counts["distinct_root_degrees_used"])
    print(json.dumps({"seed":"0x1ca417","counts":dict(sorted(counts.items()))},indent=2))


if __name__=="__main__":
    main()
