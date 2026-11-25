#!/usr/bin/env python3
"""Exact finite checks for HF1/HF2; these do not prove asymptotic optimality."""
from fractions import Fraction
from itertools import product, combinations
from math import prod, isqrt
from random import Random
from pathlib import Path
import json
from verify_joint_rectangle_fourier import predictor, binomial_coefficients, first_difference, basis


def rank_mod(matrix,p):
    rows=[list(row) for row in matrix]; rank=0
    for col in range(len(rows[0])):
        pivot=next((j for j in range(rank,len(rows)) if rows[j][col]%p),None)
        if pivot is None: continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        inverse=pow(rows[rank][col],-1,p)
        rows[rank]=[v*inverse%p for v in rows[rank]]
        for j in range(rank+1,len(rows)):
            factor=rows[j][col]%p
            if factor:
                rows[j]=[(a-factor*b)%p for a,b in zip(rows[j],rows[rank])]
        rank+=1
        if rank==len(rows): break
    return rank


def elementary(values,r):
    es=[1]+[0]*r
    for a in values:
        for j in range(r,0,-1): es[j]+=a*es[j-1]
    return es[r]


def eigen_data(qs):
    L=len(qs); r=L//2; cs=binomial_coefficients(L)
    assert cs[r]==Fraction(1,2**r)
    data=[]
    for mask in range(2**L):
        T={i for i in range(L) if mask>>i&1}
        value=Fraction(0)
        for j in range(len(T),r+1):
            for S in combinations(range(L),j):
                if T.issubset(S):
                    value+=cs[j]*prod(qs[i] for i in range(L) if i not in S)
        multiplicity=prod(qs[i]-1 for i in T)
        data.append((value,multiplicity,len(T)))
    return data


def matrix_case(qs):
    L=len(qs); labels=tuple(product(*(range(q) for q in qs))); N=len(labels)
    data=eigen_data(qs)
    expected_rank=sum(mult for value,mult,_ in data if value)
    degree_rank=sum(mult for value,mult,k in data if k==L//2 and value)
    assert degree_rank==elementary([q-1 for q in qs],L//2)
    assert expected_rank>=degree_rank
    prime=next(p for p in [101,103,107,109,127,131,137,139,149,151]
               if all(value.numerator%p for value,_,_ in data if value))
    gram=[]; P=[]; rational_gram=[]
    for v in labels:
        bits=0; row=[]; grow=[]
        for j,w in enumerate(labels):
            distance=sum(a!=b for a,b in zip(v,w))
            gamma=(1-distance)%2
            if gamma: bits|=1<<j
            grow.append(gamma)
            z=predictor(distance,L)
            row.append(z.numerator*pow(z.denominator,-1,prime)%prime)
        gram.append(bits); P.append(row); rational_gram.append(grow)
    D=len(basis(gram)); assert D==2+sum(q-2 for q in qs)
    computed_rank=rank_mod(P,prime)
    assert computed_rank==expected_rank
    field_negative=False
    if qs==(4,4):
        # The same zero-one Gram matrix has different rank over Q and F2.
        assert rank_mod(rational_gram,prime)==N and D<N
        field_negative=True
    ts=[q.bit_length()-1 for q in qs]
    for i,q in enumerate(qs):
        rectangles=first_difference(q)
        for v in range(q):
            assert sum(v in A for A,B in rectangles)==ts[i]
            assert sum(v in B for A,B in rectangles)==ts[i]
    lam=(prod(1+t for t in ts)-prod(1-t for t in ts))//2
    direct=sum(prod(ts[i] for i in S) for k in range(1,L+1,2)
               for S in combinations(range(L),k))
    assert lam==direct
    return dict(qs=qs,labels=N,binary_gram_rank=D,rational_charged_rank=computed_rank,
                top_degree_rank_lower_bound=degree_rank,free_load=lam,prime=prime,
                wrong_field_rank_negative=field_negative)


def profiles():
    rng=Random(414771)
    cases=[]
    for x in [256,512,1024,2048,4096,8192]:
        for r in range(1,33):
            t=max(1,(x+r-1)//r)
            vectors=[[t]*(2*r),[1]*r+[t]*(r),
                     [max(1,t//2)]*r+[2*t]*r,
                     [1]*(r-1)+[t]* (r+1),
                     [1]*(2*r-1)+[r*t],
                     [max(1,t+(i%3)-1) for i in range(2*r)]]
            cases.extend((x,v) for v in vectors)
    for _ in range(300):
        x=rng.randint(256,8192); r=rng.randint(1,32)
        cases.append((x,[rng.randint(1,max(2,2*x//r)) for _ in range(2*r)]))
    for x,ts in cases:
        ts=sorted(ts); r=len(ts)//2; T=sum(ts[:r]); qs=[1<<t for t in ts]
        N=prod(qs); D=2+sum(q-2 for q in qs)
        er=elementary([q-1 for q in qs],r)
        lam=(prod(1+t for t in ts)-prod(1-t for t in ts))//2
        assert D>=max(qs)
        assert er*(1<<(T+r))>=N
        assert lam>=1<<(2*r-1)
        assert lam*r**r>=T**r
        # An exact integer lower target at most (1/8)*sqrt(x*log2 x).
        target=isqrt(x*(x.bit_length()-1))//8
        assert D*(lam*N+(1<<x)*er)>=N*(1<<target)
    return dict(integer_profiles=len(cases),x_min=min(x for x,_ in cases),
                x_max=max(x for x,_ in cases),largest_coordinate_count=max(len(ts) for _,ts in cases),
                claim='finite majorant checks only; universal theorem is the written inequality proof')


def main():
    tuples=[(2,2),(2,4),(4,4),(2,8),(4,8),(8,8),
            (2,2,2,2),(2,2,2,4),(2,2,4,4),(2,4,4,4),
            (4,4,4,4),(2,2,2,8),(2,2,2,2,2,2)]
    cases=[matrix_case(qs) for qs in tuples]
    # Adverse heterogeneity can make lower-degree eigenvalues vanish;
    # the full top-degree lower bound remains intact.
    zero_case=(2,4,8,8)
    data=eigen_data(zero_case)
    assert any(value==0 and k<len(zero_case)//2 for value,_,k in data)
    assert all(value!=0 for value,_,k in data if k==len(zero_case)//2)
    receipt=dict(status='pass',scope='exact finite ranks, incidences and integer invoice majorants',
                 matrix_cases=cases,profile_checks=profiles(),
                 lower_degree_zero_control=list(zero_case),
                 total_matrix_entries=sum(case['labels']**2 for case in cases))
    Path(__file__).with_name('heterogeneous-fourier-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
