#!/usr/bin/env python3
"""Exact finite partitions and source-side contracts, not a tape simulation."""
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


def bit_rectangles(q):
    t=q.bit_length()-1
    assert q == 1<<t
    result=[]
    for j in range(t):
        tail=t-j-1
        for prefix in range(1<<j):
            for orientation in (0,1):
                left=tuple((prefix<<(tail+1))+(orientation<<tail)+s for s in range(1<<tail))
                right=tuple((prefix<<(tail+1))+((1-orientation)<<tail)+s for s in range(1<<tail))
                result.append((left,right))
    return result


def distance(a,b):
    return sum(x!=y for x,y in zip(a,b))


def rectangles(d,q):
    h=2*d-1
    alphabet=tuple(range(q))
    bit_parts=bit_rectangles(q)
    for selected in combinations(range(h),d):
        inactive=tuple(i for i in range(h) if i not in selected)
        for common in product(alphabet,repeat=len(inactive)):
            for a,b in product(alphabet,repeat=2):
                for parts in product(bit_parts,repeat=d-2):
                    left=[None]*h
                    right=[None]*h
                    for i,c in zip(inactive,common):
                        left[i]=right[i]=(c,)
                    left[selected[0]]=(a,)
                    right[selected[0]]=tuple(c for c in alphabet if c!=a)
                    left[selected[1]]=tuple(c for c in alphabet if c!=b)
                    right[selected[1]]=(b,)
                    for i,(l,r) in zip(selected[2:],parts):
                        left[i],right[i]=l,r
                    yield tuple(product(*left)),tuple(product(*right))


def check_case(d,q):
    h,t=2*d-1,q.bit_length()-1
    words=list(product(range(q),repeat=h))
    index={w:i for i,w in enumerate(words)}
    n=len(words)
    seen=set()
    source,destination=Counter(),Counter()
    rectangle_count=side_pair_checks=0
    for left,right in rectangles(d,q):
        rectangle_count+=1
        assert left and right
        for side in (left,right):
            for v,w in combinations(side,2):
                assert distance(v,w)<d
                side_pair_checks+=1
        source.update(left)
        destination.update(right)
        for v,w in product(left,right):
            assert distance(v,w)==d
            key=index[v]*n+index[w]
            assert key not in seen
            seen.add(key)
    expected={i*n+j for i,v in enumerate(words) for j,w in enumerate(words) if distance(v,w)==d}
    assert seen==expected
    C=comb(h,d)
    alpha=C*(q-1)*t**(d-2)
    R=C*q**(h-d)*q*q*(2*(q-1))**(d-2)
    assert rectangle_count==R
    assert all(source[w]==destination[w]==alpha for w in words)
    old_alpha=C*(q-1)*t**(d-1)
    old_R=C*2**(d-1)*q**d*(q-1)**d
    assert R*2*(q-1)**2==old_R*q
    assert alpha*t==old_alpha
    removed=next(iter(seen))
    assert seen-{removed} != expected
    # Removing the source pin would permit a cross equality at that position.
    v=[0]*h
    w=[0]*h
    for i in range(d):
        w[i]=1
    v[0]=1
    assert distance(tuple(v),tuple(w))==d-1
    return {'d':d,'q':q,'words':n,'rectangles':R,'edges':len(seen),
            'regular_incidence':alpha,'old_incidence':old_alpha,
            'within_side_pair_checks':side_pair_checks,
            'omission_and_unpin_controls':2,
            'wrong_old_incidence_control':int(t>1)}


def main():
    cases=[check_case(d,q) for d,q in ((2,2),(2,4),(2,8),(3,2),(3,4),(4,2))]
    outer_formula_cases=0
    for d,q in product((2,3,4,8),(2,4,8,16)):
        h,t=2*d-1,q.bit_length()-1
        C,n0=comb(h,d),q**h
        alpha=C*(q-1)*t**(d-2)
        R_in=C*q**(h-d)*q*q*(2*(q-1))**(d-2)
        R=C*n0**(h-d)*R_in**d
        N=n0**h
        power=d*(d-2)
        assert R*q**power == N*C**(d+1)*2**power*(q-1)**power
        assert C*alpha**d == C**(d+1)*(q-1)**d*t**power
        outer_formula_cases+=1
    receipt={'status':'PASS','scope':'finite exact partition, incidence and Gram-side checks; not a physical runtime proof',
             'cases':cases,'total_rectangles':sum(c['rectangles'] for c in cases),
             'total_partitioned_edges':sum(c['edges'] for c in cases),
             'total_words':sum(c['words'] for c in cases),
             'within_side_pair_checks':sum(c['within_side_pair_checks'] for c in cases),
             'outer_formula_cases':outer_formula_cases,
             'negative_controls':sum(c['omission_and_unpin_controls']+c['wrong_old_incidence_control'] for c in cases)}
    Path(__file__).with_name('cross-pinned-partition-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
