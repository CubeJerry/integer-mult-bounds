#!/usr/bin/env python3
"""Exact parity-support weighted reduction and rational rank checks."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
from verify_joint_rectangle_fourier import predictor, binomial_coefficients, first_difference
from verify_heterogeneous_fourier import rank_mod


def parity_rectangles(q,L):
    labels=tuple(product(range(q),repeat=L)); idx={v:i for i,v in enumerate(labels)}
    if q==2:
        even=tuple(i for i,v in enumerate(labels) if sum(v)%2==0)
        odd=tuple(i for i,v in enumerate(labels) if sum(v)%2==1)
        return labels,[(Fraction(1),even,odd),(Fraction(1),odd,even)]
    rectangles=[]
    for k in range(1,L+1,2):
        for S in combinations(range(L),k):
            other=tuple(i for i in range(L) if i not in S)
            for common in product(range(q),repeat=len(other)):
                def whole(values):
                    word=[0]*L
                    for i,v in zip(other,common): word[i]=v
                    for i,v in zip(S,values): word[i]=v
                    return idx[tuple(word)]
                for factors in product(first_difference(q),repeat=k):
                    A=tuple(whole(v) for v in product(*(f[0] for f in factors)))
                    B=tuple(whole(v) for v in product(*(f[1] for f in factors)))
                    rectangles.append((Fraction(1),A,B))
    return labels,rectangles


def weighted_case(q,L):
    labels,rects=parity_rectangles(q,L); N=len(labels)
    # Replace one genuine rectangle by an overlapping signed identity.
    pos=next(i for i,(_,A,B) in enumerate(rects) if len(A)>1 and len(B)>1)
    w,A,B=rects.pop(pos); A1=A[:len(A)//2]; A2=A[len(A)//2:]
    B1=B[:len(B)//2]; B2=B[len(B)//2:]
    rects.extend([(w,A1,B),(w,A,B1),(w,A2,B2),(-w,A1,B1)])
    # Explicitly exercise rational weights with an odd denominator.
    w,A,B=rects.pop(); rects.extend([(w/3,A,B),(2*w/3,A,B)])
    O=defaultdict(Fraction); original_left=Counter(); original_right=Counter()
    for alpha,A,B in rects:
        original_left.update(A); original_right.update(B)
        for i in A:
            for j in B:
                assert sum(a!=b for a,b in zip(labels[i],labels[j]))%2==1
                O[i,j]+=alpha
    cs=binomial_coefficients(L)
    F=defaultdict(Fraction); new_left=Counter(); new_right=Counter(); pieces=0
    for alpha,A,B in rects:
        for j,c in enumerate(cs):
            if not c: continue
            for S in combinations(range(L),j):
                left_groups=defaultdict(list); right_groups=defaultdict(list)
                for i in A: left_groups[tuple(labels[i][s] for s in S)].append(i)
                for i in B: right_groups[tuple(labels[i][s] for s in S)].append(i)
                for key in left_groups.keys() & right_groups.keys():
                    aa,bb=left_groups[key],right_groups[key]; pieces+=1
                    new_left.update(aa); new_right.update(bb)
                    for u in aa:
                        for v in bb:
                            assert sum(a!=b for a,b in zip(labels[u],labels[v]))%2==1
                            F[u,v]-=alpha*c
    wrong_unweighted=0
    for i,A in enumerate(labels):
        for j,B in enumerate(labels):
            d=sum(a!=b for a,b in zip(A,B))
            assert O[i,j]==(d%2==1)
            assert F[i,j]==(i==j)-predictor(d,L)
            if O[i,j] and -O[i,j]!=(i==j)-predictor(d,L):
                wrong_unweighted+=1
    cap=sum(__import__('math').comb(L,j) for j,c in enumerate(cs) if c)
    for i in range(N):
        assert new_left[i]<=cap*original_left[i]
        assert new_right[i]<=cap*original_right[i]
    return dict(q=q,L=L,labels=N,weighted_odd_rectangles=len(rects),free_pieces=pieces,
                original_max_load=max(max(original_left.values()),max(original_right.values())),
                new_max_load=max(max(new_left.values()),max(new_right.values())),
                cylinder_load_multiplier=cap,identity_checks=N*N,
                omitted_polynomial_negative_controls=wrong_unweighted,
                includes_negative_and_odd_denominator_weights=True)


def rank_case(qs):
    labels=tuple(product(*(range(q) for q in qs))); N=len(labels)
    matrix=[[sum(a!=b for a,b in zip(v,w))%2 for w in labels] for v in labels]
    if 2 in qs:
        expected=1
        for q in qs:
            if q>2: expected*=q
        expected+=1
    else:
        expected=N
    # For these small sizes, 101 avoids every nonzero tensor eigenvalue.
    rank=rank_mod(matrix,101)
    assert rank==expected
    return dict(qs=qs,labels=N,rational_rank=rank,full_rank=(rank==N))


def main():
    weighted=[weighted_case(q,L) for q,L in [(2,2),(2,4),(2,6),(4,2),(8,2)]]
    ranks=[rank_case(qs) for qs in [(2,2),(2,2,2,2),(2,4),(2,2,4,4),
                                  (4,4),(4,8),(8,8),(4,4,4,4)]]
    receipt=dict(status='pass',scope='finite exact reduction/rank tests; OWL is unproved',
                 weighted_reductions=weighted,rank_cases=ranks,
                 identity_checks=sum(x['identity_checks'] for x in weighted),
                 negative_controls=sum(x['omitted_polynomial_negative_controls'] for x in weighted))
    Path(__file__).with_name('parity-weighted-fourier-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
