#!/usr/bin/env python3
"""Finite controls for the nonlinear coset-partition gauge obstruction."""
from argparse import ArgumentParser
from itertools import combinations,permutations
from hashlib import sha256
import json
from pathlib import Path

def require(x,msg):
    if not x:raise ValueError(msg)

def part(line,p):
    # p takes coded coordinates to arbitrary raw original labels.
    return tuple(sorted(tuple(sorted((p[x],p[x^line]))) for x in range(8) if x<x^line))

def joined(s):
    groups=[{x} for x in range(8)]
    for pairing in s:
        for a,b in pairing:
            A=next(g for g in groups if a in g);B=next(g for g in groups if b in g)
            if A!=B:A|=B;groups.remove(B)
    return tuple(sorted(map(len,groups)))

def main():
    p=ArgumentParser();p.add_argument('--native-review',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();dat=a.native_review.read_bytes();native=json.loads(dat)['D3']
    require(native['per_body_span_ranks']=={'26':94,'29':96} and len(native['receivers'])==12,'native obstruction ranks')
    require(native['eight_copy_span_ranks']=={'26':752,'29':768},'physical lift')
    W=range(8);checked=extremal=0
    for k in range(1,9):
        subsets=list(map(frozenset,combinations(W,k)))
        for A in subsets:
            for B in subsets:
                checked+=1
                total={x^y for x in A for y in B}
                if len(total)!=k:continue
                U={x^min(A) for x in A};V={y^min(B) for y in B}
                require(U==V and {u^v for u in U for v in U}==U,'extremal finite sumset has common cosets')
                extremal+=1
    # Each pair of direction subspaces has the same dimension on both sides.
    # The join of all three separates the two labelled partition systems.
    fam0=(1,2,4);fam1=(1,2,3)
    base=tuple(range(8))
    for selected in combinations(range(3),2):
        require(joined([part(fam0[t],base) for t in selected])==joined([part(fam1[t],base) for t in selected]),
                'individual and pairwise joins agree in nonlinear control')
    A=set();B=set()
    for p in permutations(W):
        A.add(tuple(part(d,p) for d in fam0));B.add(tuple(part(d,p) for d in fam1))
    require(not A&B and len(A)==5040 and len(B)==1260,'all arbitrary bijections separately exhausted')
    require(joined([part(d,base) for d in fam0])==(8,) and joined([part(d,base) for d in fam1])==(4,4),
            'three-way join obstruction')
    out={'native_review_sha256':sha256(dat).hexdigest(),'native':native,
         'native_join_log2_class_sizes':{'donor26':4512,'donor29':4608},
         'toy_equal_cardinality_subset_pairs':checked,'toy_extremal_pairs':extremal,
         'all_arbitrary_local_permutations_each':40320,'distinct_labelled_partition_families':[len(A),len(B)],
         'common_relabelled_families':len(A&B),'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
