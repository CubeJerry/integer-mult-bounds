#!/usr/bin/env python3
"""Finite support for NC; exact combinatorial checks, not a runtime bound."""
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def rank2(rows):
    pivots = {}
    for value in rows:
        while value:
            p = value.bit_length()-1
            if p not in pivots:
                pivots[p] = value
                break
            value ^= pivots[p]
    return len(pivots)


def max_clique(adj):
    best = []
    def expand(chosen, candidates):
        nonlocal best
        remaining, order, colors, color = candidates, [], [], 0
        while remaining:
            color += 1
            current = remaining
            while current:
                bit = current & -current
                v = bit.bit_length()-1
                order.append(v)
                colors.append(color)
                remaining ^= bit
                current &= ~bit
                current &= ~adj[v]
        for i in range(len(order)-1,-1,-1):
            if len(chosen)+colors[i] <= len(best):
                return
            v = order[i]
            next_candidates = candidates & adj[v]
            if next_candidates:
                expand(chosen+[v], next_candidates)
            elif len(chosen)+1 > len(best):
                best = chosen+[v]
            candidates &= ~(1<<v)
    expand([], (1<<len(adj))-1)
    assert all((adj[a]>>b)&1 for a,b in combinations(best,2))
    return best


def binary_case(d):
    h, e = 2*d-1, d//2
    points = [sum(1<<j for j in s) for s in combinations(range(h),d)]
    matrix, compatible = [], []
    for a in points:
        row, neighbors = 0, 0
        for j,b in enumerate(points):
            c = (a&b).bit_count()
            value = sum(comb(c,r) for r in range(e)) % 2
            assert value == int(c % e == 0)
            assert value == int(a == b or (a^b).bit_count() == d)
            row |= value << j
            if a != b and (a^b).bit_count() != d:
                neighbors |= 1<<j
        matrix.append(row)
        compatible.append(neighbors)
    M = sum(comb(h,r) for r in range(e))
    rank = rank2(matrix)
    assert rank <= M
    chosen = max_clique(compatible)
    assert len(chosen) <= M
    for i,a in enumerate(chosen):
        for j,b in enumerate(chosen):
            assert ((matrix[a]>>b)&1) == int(i == j)
    return {'d':d,'points':len(points),'polynomial_rank':rank,
            'monomial_bound':M,'exact_largest_independent_family':len(chosen),
            'family_bitmasks':[points[i] for i in chosen]}


def qary_case(d,q):
    h=2*d-1
    points=[w for w in product(range(q),repeat=h) if sum(x!=0 for x in w)==d]
    compatible=[]
    for a in points:
        compatible.append(sum(1<<j for j,b in enumerate(points)
                              if a!=b and sum(x!=y for x,y in zip(a,b))!=d))
    chosen=max_clique(compatible)
    bound=(1<<(h-1))*q**(d-1)
    assert len(chosen)<=bound
    return {'d':d,'q':q,'far_neighbors':len(points),
            'exact_largest_independent_family':len(chosen),'rank_bound':bound}


def main():
    binary=[binary_case(d) for d in (2,4)]
    qary=[qary_case(2,q) for q in (2,4)]
    binomial_cases=0
    for d in (2,4,8,16,32,64,128,256,512):
        h=2*d-1
        C=comb(h,d)
        M=sum(comb(h,j) for j in range(d//2))
        assert C**8 >= (1<<d)*M**8
        binomial_cases+=1
    uniform_cases=0
    for d,t in product((2,4,8,16,32),range(1,13)):
        h,q=2*d-1,1<<t
        C=comb(h,d)
        C0=1<<(h-1)
        M=sum(comb(h,j) for j in range(d//2))
        lower=max(C*Fraction(C,M)**d,
                  C*Fraction(C*(q-1)**d,C0*q**(d-1))**d)
        assert lower**32 >= (1<<(d*d+d*t))
        z=t*d*d-2*d*d+2
        if z>=1:
            assert (d*d+d*t)**3 >= z*z
        uniform_cases+=1
    outer_checks=0
    for d in (2,4):
        h=2*d-1
        inner=(1<<d)-1
        words=[tuple(inner if i in s else 0 for i in range(h))
               for s in combinations(range(h),d)]
        for a,b in combinations(words,2):
            assert any((x^y).bit_count()==d for x,y in zip(a,b))
            outer_checks+=1
    # Power-of-two and zero-Gram assumptions are necessary for these proofs.
    assert sum(comb(6,j) for j in range(3))%2 == 0
    assert binary[0]['points'] > binary[0]['monomial_bound']
    receipt={'status':'PASS','scope':'finite exact algebra and geometry, not tape/runtime lower bounds',
             'binary_cases':binary,'qary_cases':qary,
             'binomial_inequalities':binomial_cases,
             'uniform_incidence_inequalities':uniform_cases,
             'different_outer_support_checks':outer_checks,
             'negative_assumption_controls':2}
    Path(__file__).with_name('noncanonical-incidence-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
