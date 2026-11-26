#!/usr/bin/env python3
"""Exact partial-Fourier preconditioning and endpoint-call accounting."""
from fractions import Fraction
from itertools import product, combinations
from math import comb,prod
from random import Random
from pathlib import Path
import json
from verify_joint_rectangle_fourier import basis, first_difference


def dot(a,b): return (a&b).bit_count()%2

def linear(columns,z):
    out=0
    for i,c in enumerate(columns):
        if z>>i&1: out^=c
    return out


def transforms():
    rng=Random(4107); cases=entries=degenerate=wrong_dual=wrong_scale=0
    for d in range(1,6):
        n=1<<d; samples={tuple(1<<i for i in range(d))}
        target=min(20,prod((1<<d)-(1<<i) for i in range(d)))
        while len(samples)<target:
            cols=tuple(rng.randrange(1,n) for _ in range(d))
            if len(basis(cols))==d: samples.add(cols)
        for cols in sorted(samples):
            dual={sum(dot(c,w)<<i for i,c in enumerate(cols)):w for w in range(n)}
            assert len(dual)==n
            for h in range(d+1):
                ch=d-h; hs=1<<h; cs=1<<ch; cases+=1
                gram=[sum(dot(cols[i],cols[j])<<j for j in range(h)) for i in range(h)]
                if len(basis(gram))<h: degenerate+=1
                for source in range(n):
                    full=[-1 if dot(w,source) else 1 for w in range(n)]
                    adapted=[full[dual[eta]] for eta in range(n)]
                    for xi in range(hs):
                        for c in range(cs):
                            numerator=sum((-1 if dot(c,eta) else 1)*adapted[xi|(eta<<h)] for eta in range(cs))
                            actual=Fraction(numerator,cs)
                            expected=sum((-1 if dot(xi,hh) else 1) for hh in range(hs) if linear(cols,hh|(c<<h))==source)
                            assert actual==expected; entries+=1
                            if ch and expected:
                                assert numerator!=expected; wrong_scale+=1
                            bad=sum((-1 if dot(c,eta) else 1)*full[xi|(eta<<h)] for eta in range(cs))
                            if Fraction(bad,cs)!=expected: wrong_dual+=1
    assert degenerate and wrong_dual and wrong_scale
    return dict(basis_subspace_cases=cases,exact_identity_entries=entries,
                degenerate_restricted_subspace_cases=degenerate,
                omitted_dual_change_negative_controls=wrong_dual,
                omitted_inverse_scale_negative_controls=wrong_scale)


def incidence(q,L):
    labels=tuple(product(range(q),repeat=L)); N=len(labels); index={v:i for i,v in enumerate(labels)}
    rows=[sum(((1-sum(a!=b for a,b in zip(v,w)))%2)<<j for j,w in enumerate(labels)) for v in labels]
    D=len(basis(rows)); assert D==2+L*(q-2)
    t=q.bit_length()-1
    lam=sum(comb(L,k)*t**k for k in range(1,L+1,2))
    deriv=sum(k*comb(L,k)*t**(k-1) for k in range(1,L+1,2))
    mass=rectangles=0
    for k in range(1,L+1,2):
        for S in combinations(range(L),k):
            other=tuple(i for i in range(L) if i not in S)
            for common in product(range(q),repeat=len(other)):
                def whole(values):
                    word=[0]*L
                    for i,v in zip(other,common): word[i]=v
                    for i,v in zip(S,values): word[i]=v
                    return index[tuple(word)]
                for factors in product(first_difference(q),repeat=k):
                    A=tuple(whole(v) for v in product(*(f[0] for f in factors)))
                    B=tuple(whole(v) for v in product(*(f[1] for f in factors)))
                    rank=len(basis(rows[v] for v in A))
                    assert rank==1+sum(len(f[0])-1 for f in factors)
                    assert len(A)==len(B)
                    mass+=(rank-1)*len(A)+rank*len(B); rectangles+=1
    K=Fraction(mass,N); assert K==lam+2*(q-1-t)*deriv
    old=2*D*lam; new=2*(D-1)+2*K
    if t>=2: assert new<old
    result=dict(q=q,L=L,labels=N,D=D,lambda_value=lam,lambda_derivative=deriv,K=int(K),
                product_side_rank_checks=rectangles,old_axis_invoice=old,new_axis_invoice=int(new))
    if L==2:
        star=2*(D-1)+4*(q-1)
        assert star<=new
        result['singleton_source_star_invoice']=star
    return result


def phase_checks():
    identity_entries=wrong_order=aggregation_entries=0
    for a in range(1,4):
        n=1<<(2*a); mask=(1<<a)-1; denominator=1<<a
        phase=[-1 if dot(x&mask,x>>a) else 1 for x in range(n)]
        fourier=[[Fraction(-1 if dot(x,y) else 1,denominator) for y in range(n)] for x in range(n)]
        forward=[[fourier[x][y]*phase[y] for y in range(n)] for x in range(n)]
        adjoint=[[phase[x]*fourier[x][y] for y in range(n)] for x in range(n)]
        for x in range(n):
            for y in range(n):
                assert sum(forward[x][z]*adjoint[z][y] for z in range(n))==(x==y)
                identity_entries+=1
                if forward[x][y]!=adjoint[x][y]: wrong_order+=1
        ordinary=[(x%7)-3 for x in range(n)]
        frequency=[(x%5)-2 for x in range(n)]
        for x in range(n):
            assembled=phase[x]*(ordinary[x]+sum(fourier[x][y]*frequency[y] for y in range(n)))
            separate=phase[x]*ordinary[x]+sum(adjoint[x][y]*frequency[y] for y in range(n))
            assert assembled==separate
            aggregation_entries+=1
        # The distinguished query phase is a disjoint-coordinate scalar.
        for mainx,mainy in product(range(2),repeat=2):
            for z in range(n):
                fullphase=(-1 if (mainx*mainy+dot(z&mask,z>>a))%2 else 1)
                assert fullphase==(-1 if mainx*mainy else 1)*phase[z]
    assert wrong_order>0
    return dict(full_phase_adjoint_identity_entries=identity_entries,
                wrong_output_phase_order_negative_controls=wrong_order,
                two_channel_aggregation_entries=aggregation_entries)


def main():
    cases=[incidence(q,L) for q,L in [(2,2),(2,4),(2,6),(4,2),(4,4),(8,2),(16,2)]]
    receipt=dict(status='pass',scope='finite identities and exact source call invoices; no full tape execution',
                 partial_transform_checks=transforms(),phase_and_adjoint_checks=phase_checks(),incidence_cases=cases,
                 total_product_side_rank_checks=sum(c['product_side_rank_checks'] for c in cases))
    Path(__file__).with_name('fourier-preconditioning-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
