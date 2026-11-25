#!/usr/bin/env python3
"""Exact finite certificate checks; general local-load proof is in the note."""
from itertools import product
from math import comb
from fractions import Fraction
from pathlib import Path
import json


def edge(x,y):
    return all(a!=b for a,b in zip(x,y))


def partition(q):
    return [(tuple((x,b) for x in range(q) if x!=a),
             tuple((a,y) for y in range(q) if y!=b))
            for a in range(q) for b in range(q)]


def check_partition(q):
    labels=tuple(product(range(q),repeat=2))
    counts={};left={x:0 for x in labels};right={x:0 for x in labels}
    rectangles=partition(q)
    for A,B in rectangles:
        for x in A:left[x]+=1
        for y in B:right[y]+=1
        for x in A:
            for y in B:
                assert edge(x,y)
                counts[x,y]=counts.get((x,y),0)+1
    for x in labels:
        for y in labels:
            assert counts.get((x,y),0)==int(edge(x,y))
    assert set(left.values())==set(right.values())=={q-1}
    assert len(counts)==q*q*(q-1)**2
    assert Fraction(q-1)>=Fraction(2*(q-1),q)**2
    assert comb(2*(q-1),q-1)>=q
    return dict(q=q,rectangles=len(rectangles),edges=len(counts),load=q-1)


def all_sides(q,k):
    labels=tuple(product(range(q),repeat=k));n=len(labels);cases=0
    for mask in range(1,1<<n):
        A=[labels[i] for i in range(n) if mask>>i&1]
        projections=[{x[j] for x in A} for j in range(k)]
        B=list(product(*([a for a in range(q) if a not in projections[j]] for j in range(k))))
        if not B:continue
        assert all(edge(x,y) for x in A for y in B)
        assert len(A)*len(B)*4**k<=q**(2*k)
        # Correlated A can have fewer points than its coordinate box.
        assert len(A)<=__import__('math').prod(len(p) for p in projections)
        cases+=1
    return cases


def main():
    families=[check_partition(q) for q in range(2,13)]
    sides=sum(all_sides(q,k) for q,k in [(2,2),(2,3),(3,2),(4,2)])
    q4=partition(4)
    expected={ (tuple(sorted(4*x+y for x,y in A)),tuple(sorted(4*x+y for x,y in B))) for A,B in q4 }
    cert=Path(__file__).with_name('q4-k2-load3.json')
    if cert.exists():
        data=json.loads(cert.read_text())
        actual={(tuple(sorted(A)),tuple(sorted(B))) for A,B in data['certificate']['rectangles']}
        assert actual==expected
    # Duplicate a valid rectangle: still a Boolean cover but not a partition.
    A,B=q4[0]; counts={}
    for X,Y in q4+[q4[0]]:
        for x in X:
            for y in Y:counts[x,y]=counts.get((x,y),0)+1
    assert all(counts[x,y]>=1 for x,y in counts)
    assert any(v==2 for v in counts.values())
    # Removing one certificate rectangle loses exactly its nine edges.
    before={(x,y) for X,Y in q4 for x in X for y in Y}
    after={(x,y) for X,Y in q4[1:] for x in X for y in Y}
    assert len(before-after)==9
    assert Fraction(2*(4-1),4)**2>2
    result={'status':'pass','scope':'finite exact local-load and certificate identities; no general JR witness',
            'two_coordinate_families':families,'correlated_left_side_capacity_cases':sides,
            'q4_certificate_matches_formula':cert.exists(),'negative_controls':3,
            'q4_global_optimal_load':3,'basis':'written universal lower bound plus exact partition'}
    Path(__file__).with_name('jr-local-load-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
