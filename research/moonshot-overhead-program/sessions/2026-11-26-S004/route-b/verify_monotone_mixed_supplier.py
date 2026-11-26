#!/usr/bin/env python3
"""Exact controls for the scoped monotone mixed-supplier count."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

COUNTS={}

def count(name,n=1):
    COUNTS[name]=COUNTS.get(name,0)+n

def lower(h,s):
    return h*h-s*h+(s*s)//4

def main():
    for h in range(1,8):
        subsets=[[j for j in range(h) if mask>>j&1] for mask in range(1,1<<h)]
        for a in subsets:
            for b in subsets:
                sums={j+k for j in a for k in b}
                assert (len(sums)==1)==(len(a)==len(b)==1)
                count('nonempty_rectangle_singleton_controls')

    for h in range(1,65):
        lengths=[sum(j+k==i for j in range(h) for k in range(h)) for i in range(2*h-1)]
        descending=sorted(lengths,reverse=True)
        for s in range(2*h):
            omitted=sum(descending[:s])
            assert omitted==s*h-(s*s)//4
            assert h*h-omitted==lower(h,s)==((2*h-s)**2)//4
            count('exact_extremal_antidiagonal_counts')

    # Exhaust every zero/one coefficient subcandidate for h<=4.
    for h in range(1,5):
        full=(1<<(h*h))-1
        masks=[sum(1<<(j*h+k) for j in range(h) for k in range(h) if j+k==i)
               for i in range(2*h-1)]
        minima=[h*h+1]*(2*h)
        for candidate in range(1<<(h*h)):
            missing=full^candidate
            outliers=sum(bool(missing&mask) for mask in masks)
            q=candidate.bit_count()
            assert q>=lower(h,outliers)
            minima[outliers]=min(minima[outliers],q)
            count('exhaustive_zero_one_subcandidates')
        for s in range(2*h):
            assert min(minima[:s+1])==lower(h,s)
            count('attained_global_product_minima')

    # Nonnegative fractional coefficients cannot cancel omitted monomials.
    h,u=2,2
    for coefficients in product((Fraction(0),Fraction(1,2),Fraction(1)),repeat=h*h):
        q=sum(x>0 for x in coefficients)
        for threshold in (1,u*u):
            worst=0
            for a in product((0,u),repeat=h):
                for b in product((0,u),repeat=h):
                    errors=[sum((1-coefficients[j*h+k])*a[j]*b[k]
                                for j in range(h) for k in range(h) if j+k==i)
                            for i in range(2*h-1)]
                    assert all(x>=0 for x in errors)
                    worst=max(worst,sum(x>=threshold for x in errors))
                    count('fractional_candidate_corner_evaluations')
            all_high=[u*u*sum(1-coefficients[j*h+k]
                             for j in range(h) for k in range(h) if j+k==i)
                      for i in range(2*h-1)]
            assert worst==sum(x>=threshold for x in all_high)
            assert q>=lower(h,worst)
            count('fractional_mixed_supplier_bounds')

    # Signed output recombination evades the nonnegative-factor model.
    for a in product(range(4),repeat=2):
        for b in product(range(4),repeat=2):
            p0=a[0]*b[0]
            p2=a[1]*b[1]
            middle=(a[0]+a[1])*(b[0]+b[1])-p0-p2
            assert [p0,middle,p2]==[a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1]]
            count('signed_cancellation_negative_controls')
    assert 3<lower(2,0)

    # When threshold exceeds U², zero candidate at h=1 has no outlier.
    u,threshold=3,10
    assert all(a*b<threshold for a,b in product((0,u),repeat=2))
    assert 0<lower(1,0)
    count('large_threshold_negative_control')

    result={'status':'all exact finite controls passed',
            'scope':'nonnegative bilinear product count, not a general tape-time lower bound',
            'counts':COUNTS}
    Path(__file__).with_name('monotone-mixed-supplier-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
