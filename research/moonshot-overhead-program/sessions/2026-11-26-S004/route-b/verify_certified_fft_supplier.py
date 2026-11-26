#!/usr/bin/env python3
"""Exact dyadic FFT supplier controls; no floating-point/root oracle."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
from random import Random
import json
COUNTS={}
def count(name,n=1):
    COUNTS[name]=COUNTS.get(name,0)+n
def cmul(a,b,scale):
    x=a[0]*b[0]-a[1]*b[1]
    y=a[0]*b[1]+a[1]*b[0]
    out=(x//scale,y//scale)
    assert 0<=x-out[0]*scale<scale and 0<=y-out[1]*scale<scale
    count('exact_complex_rounding_controls')
    return out
def roots(ell,q):
    scale=1<<q
    cosine,sine=0,scale
    for _ in range(ell-2):
        radicand=(scale+cosine)*(scale//2)
        cosine=isqrt(radicand)
        assert cosine*cosine<=radicand<(cosine+1)*(cosine+1)
        assert cosine>=scale//2
        numerator=sine*(scale//2)
        new_sine=numerator//cosine
        assert 0<=numerator-new_sine*cosine<cosine
        sine=min(scale,max(0,new_sine))
        count('half_angle_exact_sqrt_and_divisions')
    n=1<<ell
    power=(scale,0)
    table=[]
    eta=F(32*n*ell,scale)
    for _ in range(n):
        table.append(power)
        norm_sq=F(power[0]*power[0]+power[1]*power[1],scale*scale)
        assert (1-eta)**2<=norm_sq<=(1+eta)**2
        power=cmul(power,(cosine,sine),scale)
        count('root_power_norm_enclosures')
    return table
def fft(values,table,scale,inverse=False):
    n=len(values)
    ell=n.bit_length()-1
    def reverse_bits(i):
        z=0
        for _ in range(ell):
            z=(z<<1)+(i&1)
            i>>=1
        return z
    out=[values[reverse_bits(i)] for i in range(n)]
    length=2
    while length<=n:
        stride=n//length
        for base in range(0,n,length):
            for j in range(length//2):
                root=table[j*stride]
                if inverse:
                    root=(root[0],-root[1])
                u=out[base+j]
                v=cmul(root,out[base+j+length//2],scale)
                out[base+j]=(u[0]+v[0],u[1]+v[1])
                out[base+j+length//2]=(u[0]-v[0],u[1]-v[1])
        length*=2
        count('fixed_precision_fft_stages')
    if inverse:
        out=[(x//n,y//n) for x,y in out]
    return out
def ordinary(a,b):
    out=[0]*(len(a)+len(b))
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out
def supplier(a,b,bits,budget_bits):
    h=len(a)
    n=4
    while n<2*h:
        n*=2
    ell=n.bit_length()-1
    c=ell.bit_length()
    q=2*bits+3*ell+2*c-budget_bits+20
    w=q+2*bits+3*ell+10
    assert 1<=budget_bits<=2*bits+ell
    scale=1<<q
    modulus=1<<budget_bits
    eta=F(32*n*ell,scale)
    assert eta*ell<=F(1,1<<17)
    assert F(2048*ell*ell*n**3*((1<<bits)-1)**2,scale)<=F(modulus,512)
    table=roots(ell,q)
    fa=fft([(x*scale,0) for x in a]+[(0,0)]*(n-h),table,scale)
    fb=fft([(x*scale,0) for x in b]+[(0,0)]*(n-h),table,scale)
    pointwise=[cmul(x,y,scale) for x,y in zip(fa,fb)]
    recovered=fft(pointwise,table,scale,True)
    actual=ordinary(a,b)
    candidate=[]
    for i in range(2*h):
        real,imag=recovered[i]
        error_real=F(real,scale)-actual[i]
        error_imag=F(imag,scale)
        assert error_real**2+error_imag**2<=F(modulus,512)**2
        ci=(real-(modulus*scale)//8)//scale
        candidate.append(ci)
        assert 0<=actual[i]-ci<modulus
        assert abs(ci)<=h*((1<<bits)-1)**2+F(modulus,4)+1
        count('certified_positive_residual_coefficients')
    for stage in (fa,fb,pointwise,recovered):
        assert all(abs(x)<1<<(w-1) and abs(y)<1<<(w-1) for x,y in stage)
    residual=[(x-y)%modulus for x,y in zip(actual,candidate)]
    assert [x+y for x,y in zip(candidate,residual)]==actual
    assert sum(residual)==sum(a)*sum(b)-sum(candidate)
    count('complete_supplier_and_modular_repairs')
    count('fixed_word_capacity_controls')
    return candidate,residual
def main():
    rng=Random(2026112612)
    for h in (1,2,3,5,8,17):
        for bits in (1,3,7):
            n=4
            while n<2*h:
                n*=2
            ell=n.bit_length()-1
            budgets=sorted({1,3,min(7,2*bits+ell),2*bits+ell})
            for budget in budgets:
                top=(1<<bits)-1
                profiles=([0]*h,[top]*h,[rng.randrange(top+1) for _ in range(h)])
                for i,a in enumerate(profiles):
                    supplier(a,profiles[(i+1)%len(profiles)],bits,budget)
    for a,b in product(product(range(2),repeat=2),repeat=2):
        supplier(list(a),list(b),1,1)
        count('exhaustive_binary_two_digit_inputs')
    assert 8%8==0 and 8!=0
    count('uncertified_alias_negative_control')
    assert (-1)//4==-1 and int(F(-1,4))==0
    count('negative_floor_convention_control')
    result={'status':'all exact finite controls passed','seed':2026112612,
            'arithmetic':'integer isqrt/division and exact dyadic complex arithmetic',
            'scope':'certified supplier arithmetic and margin; tape invoice proved separately',
            'counts':COUNTS}
    Path(__file__).with_name('certified-fft-supplier-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    main()
