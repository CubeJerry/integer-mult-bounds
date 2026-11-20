"""Verify the Petersen entropy dual in its 34-dimensional symmetry quotient."""
import argparse
from collections import Counter
from functools import cache
import gzip
from hashlib import sha256
from itertools import combinations,permutations
import json
from pathlib import Path


def audit(roots, witness):
    native=witness['native']
    pairs=list(combinations(range(5),2))
    vertices=native['pair_to_native'];anchors=native['anchors']
    assert len(set(anchors+vertices))==14 and len(anchors)==4
    assert list(map(tuple,native['pair_order']))==pairs
    def adjacent(i,j):
        return i!=j and sum(a*b for a,b in zip(roots[i],roots[j]))==0
    for i in anchors:
        assert not any(adjacent(i,j) for j in anchors+vertices)
    for i,j in combinations(range(10),2):
        assert adjacent(vertices[i],vertices[j])==set(pairs[i]).isdisjoint(pairs[j])
    # Under the averaged entropy function all subsets in an orbit have the same value.
    # Use unlabeled graphs on five labels as orbit keys. Sum the 21 raw inequalities
    # only once in 34 dimensions. This is independent of the 120-permutation expansion.
    idx={p:i for i,p in enumerate(pairs)}
    maps=[tuple(idx[tuple(sorted((q[i],q[j])))] for i,j in pairs) for q in permutations(range(5))]
    @cache
    def graph_orbit(S):
        return min(sum(1<<p[i] for i in range(10) if (S>>i)&1) for p in maps)
    counts=Counter()
    constant=0
    def add(S,weight):
        counts[graph_orbit(S)]+=weight
    dual=witness['petersen_certificate']['weighted_raw_terms']
    for weight,kind,S,i,*extra in dual:
        assert not S&(1<<i)
        T=S|(1<<i)
        if kind=='submod':
            j,=extra
            assert weight>=0 and i!=j and not S&(1<<j)
            add(T,weight);add(S|(1<<j),weight)
            add(S,-weight);add(T|(1<<j),-weight)
        else:
            assert kind in ('decode','mono')
            if kind=='decode':
                assert all(not adjacent(vertices[j],vertices[i]) for j in range(10) if S&(1<<j))
                constant+=weight
            else:assert weight>=0
            add(T,weight);add(S,-weight)
    counts={k:v for k,v in counts.items() if v}
    assert counts=={0:-2,1023:2} and constant==10
    orbits=Counter(graph_orbit(S) for S in range(1024))
    assert len(orbits)==34
    return {'symmetry_orbits':len(orbits),'quotient_coefficients':counts,
            'right_side':constant,'native_contacts_in_four_plus_petersen':sum(adjacent(i,j) for i,j in combinations(anchors+vertices,2)),
            'dual_has_signed_decoding_inequalities_used_as_equalities':sum(w<0 for w,k,*_ in dual if k=='decode'),
            'lower_GF64_fields_at_3840':9*3840,'target_GF64_fields_at_870':34688,'maximum_excess_GF64_fields_at_870':128}


def main():
    p=argparse.ArgumentParser()
    for f in ('repo','witness','out'):p.add_argument('--'+f,required=True,type=Path)
    a=p.parse_args();src=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(src.read_bytes())
    assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    roots=json.loads(raw)['root_table'][:111];w=json.loads(a.witness.read_bytes())
    result=audit(roots,w)
    w['petersen_certificate']['weighted_raw_terms'][-1][0]+=1
    try:audit(roots,w)
    except AssertionError:result['rejected_altered_decoding_multiplier']=True
    else:raise ValueError('altered decoding multiplier accepted')
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
