#!/usr/bin/env python3
"""Exact finite tests of the JR transfer; this does not prove JR itself."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def clog(n):
    return (n-1).bit_length()


def root(n, p):
    lo, hi = 0, 1 << ((n.bit_length()+p-1)//p)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**p >= n:
            hi = mid
        else:
            lo = mid
    return hi


def predictor(k, L):
    v = Fraction(1)
    for r in range(1, L//2+1):
        v *= Fraction(2*r-k, 2*r)
    return v


def binomial_coefficients(L):
    cs = []
    for j in range(L//2+1):
        cs.append(predictor(L-j, L)-sum(cs[r]*comb(j,r) for r in range(j)))
    for k in range(L+1):
        assert sum(c*comb(L-k,j) for j,c in enumerate(cs) if j<=L-k)==predictor(k,L)
    for v in cs+[predictor(k,L) for k in range(L+1)]:
        assert v.denominator & (v.denominator-1) == 0
    return cs


def first_difference(q):
    t=clog(q)
    assert 2**t==q
    out=[]
    for first in range(t):
        s=t-first-1
        for prefix in range(2**first):
            low=prefix << (s+1)
            zero=tuple(range(low, low+2**s))
            one=tuple(range(low+2**s, low+2**(s+1)))
            out.extend([(zero,one),(one,zero)])
    assert Counter((x,y) for A,B in out for x in A for y in B)==Counter({(x,y):1 for x in range(q) for y in range(q) if x!=y})
    return out


def correlated_partition(q,k):
    # Split each side of a known product partition into checksum classes.
    # These refined rectangles have correlated sides, still form a partition,
    # and are NOT asserted to meet the hypothetical JR asymptotic load bound.
    for factors in product(first_difference(q),repeat=k):
        A=tuple(product(*(f[0] for f in factors)))
        B=tuple(product(*(f[1] for f in factors)))
        for a in range(2):
            aa=tuple(w for w in A if sum(w)%2==a)
            for b in range(2):
                bb=tuple(w for w in B if sum(w)%2==b)
                if aa and bb:
                    yield aa,bb


def is_product(words):
    size=1
    for coordinate in zip(*words):
        size*=len(set(coordinate))
    return size==len(words)


def embed(word,q):
    return 1+sum(1 << (1+i*q+v) for i,v in enumerate(word))


def basis(vectors):
    bs={}
    for v in vectors:
        while v:
            p=v.bit_length()-1
            if p in bs:
                v ^= bs[p]
            else:
                bs[p]=v
                break
    return tuple(bs.values())


def finite_case(q,L):
    labels=tuple(product(range(q),repeat=L)); n=len(labels)
    index={w:i for i,w in enumerate(labels)}
    vs=tuple(embed(w,q) for w in labels)
    cs=binomial_coefficients(L)
    charged_count=sum(comb(L,j)*q**j for j in range(L//2+1))
    assert charged_count<=2**L*q**(L//2)
    cover=Counter(); left_load=Counter(); right_load=Counter()
    rectangles=correlated=both_correlated=span_checks=0
    for k in range(1,L+1,2):
        parts=tuple(correlated_partition(q,k))
        for diff in combinations(range(L),k):
            same=tuple(i for i in range(L) if i not in diff)
            for common in product(range(q),repeat=len(same)):
                def whole(part):
                    w=[0]*L
                    for i,v in zip(same,common): w[i]=v
                    for i,v in zip(diff,part): w[i]=v
                    return index[tuple(w)]
                for A,B in parts:
                    rectangles+=1
                    ac,bc=not is_product(A),not is_product(B)
                    correlated+=ac+bc; both_correlated+=ac and bc
                    ia,ib=tuple(map(whole,A)),tuple(map(whole,B))
                    left_load.update(ia); right_load.update(ib)
                    hb=basis(vs[j] for j in ib)
                    for i in ia:
                        for h in hb:
                            assert (vs[i]&h).bit_count()%2==0
                            span_checks+=1
                        for j in ib:
                            assert sum(a!=b for a,b in zip(labels[i],labels[j]))==k
                            cover[i,j]+=1
    missing=even_negative=0; gram=[]
    for i,A in enumerate(labels):
        row=0
        for j,B in enumerate(labels):
            d=sum(a!=b for a,b in zip(A,B)); matches=L-d
            val=sum(c*comb(matches,r) for r,c in enumerate(cs) if r<=matches)
            assert val==predictor(d,L)
            assert cover[i,j]==(d%2==1)
            assert val-cover[i,j]*predictor(d,L)==(i==j)
            if d%2 and val:
                assert val!=(i==j); missing+=1
            gamma=(1-d)%2
            assert gamma==(vs[i]&vs[j]).bit_count()%2
            if d>0 and d%2==0:
                assert gamma==1; even_negative+=1
            if gamma: row|=1<<j
        gram.append(row)
    rank=len(basis(gram)); assert rank<=1+L*q
    if q>=4 and L>=4: assert both_correlated>0
    actual_bound=2*sum(comb(L,k)*clog(q)**k for k in range(1,L+1,2))
    assert max(left_load.values())<=actual_bound
    assert max(right_load.values())<=actual_bound
    return dict(q=q,L=L,labels=n,charged_rectangles=charged_count,free_rectangles=rectangles,
                nonproduct_sides=correlated,both_nonproduct_rectangles=both_correlated,
                source_load=max(left_load.values()),destination_load=max(right_load.values()),
                gamma_rank=rank,endpoint_span_checks=span_checks,identity_checks=n*n,
                missing_free_negative_controls=missing,even_distance_negative_controls=even_negative)


def profiles():
    xs=sorted(set(range(1,4097))|{2**p for p in range(13,41)})
    count=label_checks=0
    for c in range(2,17):
        for x in xs:
            r3=root(x,3); d=1<<clog(max(2,r3)); h=2*d-1
            ti=(x+2*d*d-2+d*d-1)//(d*d)
            logD=h*ti+clog(4*h)
            loglam=h*(d+1)+d*ti+d*(d-1)*clog(c)+c*d*clog(ti+1)
            assert logD+1+loglam<=100*(1+c+clog(c))*r3*r3
            r2=root(x,2); L=2*((max(2,r2)+1)//2); tf=2+(2*x+L-1)//L
            major=tf+clog(2*L)+1+L*clog(1+c)+c*clog(tf+1)
            assert major<=100*(1+c+clog(c))*r2
            assert x+L-(L//2)*tf<=0
            assert L*tf<=2*x+3*L
            if x>=36:
                assert L*tf<=3*x; label_checks+=1
            count+=1
    return dict(integer_profiles=count,polynomial_universe_checks=label_checks,x_max=max(xs),c_range=[2,16])


def chains():
    cases=sorted(set(range(65,1025))|{2**p+o for p in range(11,31) for o in (0,1,17)})
    edges=0
    for initial in cases:
        y=initial; total_arity=total_loss=depth=0
        while y>64:
            z=root(y*y,3); assert z<y//2
            y-=z+1; total_arity+=z; total_loss+=root(z,2); depth+=1; edges+=1
        assert total_arity<initial
        assert total_loss<=20*root(initial*initial,3)
        assert depth<=20*root(initial,3)
    return dict(integer_chain_cases=len(cases),chain_edges=edges,largest_log_width=max(cases),scope='smoke test; analytic telescoping is in the theorem')


def main():
    cases=[finite_case(q,L) for q,L in [(2,2),(2,4),(2,6),(2,8),(4,2),(4,4),(8,2)]]
    receipt=dict(status='pass',scope='Exact finite identity and correlated endpoint checks; JR remains unproved.',finite_cases=cases,profile_checks=profiles(),recurrence_checks=chains())
    keys=['identity_checks','endpoint_span_checks','both_nonproduct_rectangles','missing_free_negative_controls','even_distance_negative_controls']
    receipt['totals']={key:sum(case[key] for case in cases) for key in keys}
    Path(__file__).with_name('joint-rectangle-fourier-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
