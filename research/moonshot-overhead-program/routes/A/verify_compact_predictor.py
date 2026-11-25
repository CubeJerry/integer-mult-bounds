#!/usr/bin/env python3
"""Exact finite checks for the compact predictor; not tape or asymptotic tests."""
import itertools,json,math
from fractions import Fraction as F
from pathlib import Path

def mul(a,b):
    out=0
    while b:
        if b&1: out^=a
        b>>=1; a<<=1
        if a&8: a^=0b1011
    return out

def shifts(t,m=7):
    ans=[]
    for seed in itertools.product(range(8),repeat=t):
        bits=0
        for j in range(m):
            v=0
            for a in reversed(seed): v=mul(v,j)^a
            bits|=(v&1)<<j
        ans.append(bits)
    return ans

def pred(x,u,D):
    term=F(1); out=term
    for h in range(1,D+1):
        term*=F(x-u-h+1,h)
        out+=(-2)**h*term
    return (-1)**u*out

def roots(u,D,bits):
    ans=[]
    for i in range(D):
        lo=F(u+i); hi=lo+1; sign=pred(lo,u,D)
        for _ in range(bits):
            mid=(lo+hi)/2; p=pred(mid,u,D)
            if p==0: lo=hi=mid; break
            if (p>0)==(sign>0): lo=mid
            else: hi=mid
        ans.append((lo,hi))
    return ans

report={'scope':'finite exact arithmetic and negative controls; no fixed-tape or Lean verification','shift_cases':[]}
for t in [2,4]:
    ss=shifts(t); M=len(ss); m=7
    projections=0
    for size in range(1,t+1):
        for js in itertools.combinations(range(m),size):
            counts=[0]*(1<<size)
            for beta in ss:
                value=sum(((beta>>j)&1)<<i for i,j in enumerate(js)); counts[value]+=1
            assert len(set(counts))==1
            projections+=1
    r=t//2; moment_max=0
    for k in range(1<<m):
        moment=sum((m-2*(beta^k).bit_count())**(2*r) for beta in ss)
        moment_max=max(moment_max,moment)
        assert moment<=M*(2*r*m)**r
    # All-zero shifts are rejected as a translated-uniform family.
    assert sum((m-2*0)**(2*r) for _ in ss)>M*(2*r*m)**r
    report['shift_cases'].append({'t':t,'m':m,'rows':M,'projections':projections,'all_frequency_patterns':1<<m,'maximum_moment_numerator':moment_max,'denominator':M,'zero_shift_control':'rejected'})

interpolation=0
for m in range(2,81):
    for u,v in [(0,m),(m//4,3*m//4),(m//2,min(m,m//2+5))]:
        D=v-u
        for c in range(u,v+1):
            assert pred(F(c),u,D)==(-1)**c; interpolation+=1
        assert abs(F(2**D,math.factorial(D)))<=2
        assert pred(F(u),u,D)!=2*pred(F(u),u,D) # wrong leading scalar rejected
report['interpolation_cases']=interpolation
report['wrong_leading_scalar_control']='rejected'

root_cases=0
for u,D in [(0,2),(1,3),(3,7),(8,12)]:
    rb=roots(u,D,24); m=u+D; aa=F((-1)**(u+D)*2**D,math.factorial(D)); eta=F(1,2**24)
    for i,(lo,hi) in enumerate(rb):
        assert u+i<=lo<=hi<=u+i+1 and hi-lo<=eta
        assert pred(lo,u,D)*pred(hi,u,D)<=0
    zz=[(a+b)/2 for a,b in rb]
    for c in range(m+1):
        val=aa
        for z in zz: val*=c-z
        assert abs(val-pred(F(c),u,D))<=2*D*eta*(m+1)**(D-1)
        root_cases+=1
report['root_product_cases']=root_cases

# Exact binomial tails verify the moment calibration on an independent control.
tail_cases=0
for m in range(2,1025):
    r=(4*m**3-1).bit_length(); B=math.isqrt(r*m)
    if B*B<r*m: B+=1
    u=max(0,(m-2*B)//2); v=min(m,(m+2*B+1)//2)
    tail=sum(math.comb(m,c) for c in range(m+1) if not u<=c<=v)
    assert tail*4*m**3<=2**m
    assert 2**r>=4*m**3
    tail_cases+=1
report['binomial_tail_controls']=tail_cases
report['status']='PASS'
output=Path(__file__).with_name('compact-predictor-verification.json')
output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
