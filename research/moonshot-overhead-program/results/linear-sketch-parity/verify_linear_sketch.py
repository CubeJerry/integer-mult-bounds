#!/usr/bin/env python3
"""Exact fiber and rational Fourier controls; no physical algorithm test."""
from __future__ import annotations
import itertools,json
from fractions import Fraction
from pathlib import Path
from random import Random


def advantage(p, columns, shift=0):
    r=len(columns[0]); signed={}
    for x in range(1<<len(columns)):
        y=[0]*r; z=x^shift
        for j,col in enumerate(columns):
            if z>>j&1:
                for i,a in enumerate(col): y[i]=(y[i]+a)%p
        key=tuple(y)
        signed[key]=signed.get(key,0)+(-1 if x.bit_count()%2 else 1)
    return Fraction(sum(abs(v) for v in signed.values()),1<<len(columns))


def good_characters(p,columns):
    return sum(all(sum(ti*ai for ti,ai in zip(t,a))%p for a in columns)
               for t in itertools.product(range(p),repeat=len(columns[0])))


def main():
    exact=general=shifts=degree=zeros=0
    for r,max_m in ((1,6),(2,4)):
        choices=list(itertools.product(range(3),repeat=r))
        for m in range(1,max_m+1):
            for cols in itertools.product(choices,repeat=m):
                delta=advantage(3,cols); good=good_characters(3,cols)
                assert delta**2<=good*Fraction(3,4)**m
                assert good<=3**r-1
                if delta==1:
                    assert 2*r>=m
                    degree+=1
                if (0,)*r in cols:
                    assert delta==0
                    zeros+=1
                exact+=1
    rng=Random(20261125)
    for p in (3,5,7,11):
        for r in (1,2,3):
            for m in range(1,9):
                for _ in range(5):
                    cols=[tuple(rng.randrange(p) for _ in range(r)) for _ in range(m)]
                    delta=advantage(p,cols)
                    # sin(pi/(2p))>=1/p gives an exact rational weaker bound.
                    assert delta**2<=(p**r-1)*Fraction(p*p-1,p*p)**m
                    if delta==1:
                        assert r*(p-1)>=m
                        degree+=1
                    assert advantage(p,cols,rng.randrange(1<<m))==delta
                    shifts+=1;general+=1
    groupings=0
    for p in (3,5,7,11):
        for m in range(1,11):
            r=(m+p-2)//(p-1)
            cols=[tuple(int(i==j//(p-1)) for i in range(r)) for j in range(m)]
            assert advantage(p,cols)==1
            groupings+=1
    delta=advantage(2,[(1,)]*8)
    assert delta==1 and delta**2>Fraction(3,4)**8
    cols=[(1,0,0)]*2+[(0,1,0)]*2+[(0,0,1)]*2
    delta=advantage(3,cols)
    assert delta==1 and delta**2>2*Fraction(3,4)**6
    result={'status':'PASS','exact_arithmetic':True,
      'scope':'finite sketches and rational Fourier bounds; no tape algorithm',
      'ternary_exact_parseval_cases':exact,'general_odd_prime_bound_cases':general,
      'shift_invariance_cases':shifts,'exact_prediction_degree_cases':degree,
      'zero_column_balancing_cases':zeros,'optimal_grouping_cases':groupings,
      'negative_controls':{'characteristic_two_extension':True,'dimension_free_bound':True}}
    Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
