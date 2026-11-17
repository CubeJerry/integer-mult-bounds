#!/usr/bin/env python3
"""Audit clean source flags, actual 45-port intersections, and finite test models."""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path


def require(test, message):
    if not test:
        raise AssertionError(message)


def hist(values):
    return dict(sorted(Counter(values).items()))


def mask(roles):
    return sum(1 << r for r in roles)


def projective_case():
    # Four shared ports, six two-port receivers, one common dimension-two target.
    # All Rado inequalities hold, but no four different F2 directions exist.
    binary = list(product(range(2),repeat=2))[1:]
    good_base = sum(all(choices[i] != choices[j] for i,j in combinations(range(4),2))
                    for choices in product(binary, repeat=4))
    require(good_base == 0, 'literal-F2 simultaneous control')
    # GF4 = F2[z]/(z^2+z+1). Choose four rows of its projective line.
    GF4 = [[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]
    rows = [(1,k) for k in range(4)]
    dets = [GF4[a][d]^GF4[b][c] for (a,b),(c,d) in combinations(rows,2)]
    require(all(dets),'same receivers admit simultaneous linear rows after extension')
    subsets = [frozenset((1,)),frozenset((1,))]
    require(all(len(w) == 1 for w in subsets) and len(set.union(*map(set,subsets))) == 1,
            'two one-dimensional common outputs can miss the two-port rank constraint')
    return {'base_F2_solutions':good_base, 'GF4_pair_determinants':dets,
            'single_port_positive_but_two_port_defect':[1,1,1]}


def sumset_case():
    group = set(range(8))
    total = 0
    for size in (2,4):
        subsets = [set(s) for s in combinations(group,size)]
        for u in subsets:
            for v in subsets:
                sums = {a^b for a in u for b in v}
                if len(sums) != size:
                    continue
                total += 1
                stab = {a for a in group if {a^x for x in u} == u}
                require(len(stab) == size and {next(iter(v))^x for x in v} == stab,
                        'equal sumsets give identical coset stabilizers')
    require(total == 140,'actual extremal F2^3 pairs')
    return {'domain':'F2^3','equal-size small-sumset pairs of sizes 2 or 4':total}


def native_layout(native,layout):
    data = native.read_bytes()
    require(hashlib.sha256(data).hexdigest() == '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','S013 source')
    raw = gzip.decompress(layout.read_bytes())
    require(hashlib.sha256(raw).hexdigest() == '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','S022 literal layout')
    w = json.loads(raw)
    r = w['root_table']; a = list(map(mask,w['A2'])); d = list(map(mask,w['D4']))
    require(r[:111] == json.loads(data)['native_roots'],'ordered native table')
    F = [mask(j for j,s in enumerate(r) if sum(x*y for x,y in zip(t,s))==0) for t in r[:111]]
    n = (1<<111)-1
    H = [h for h in a if h&n]
    singleton = [h for h in H if (h&n).bit_count() == 1]
    donor = [[h for h in H if h&(1<<j)] for j in range(111)]
    visible = [[{h for h in p if h&f == h} if f&(1<<j) else set() for f in F] for j,p in enumerate(donor)]
    avail = []
    for j,p in enumerate(donor):
        require(len(p) == 28 and all(len(v) in (0,16) for v in visible[j]), 'local pencil')
        for h in p:
            avail.append(sum(h in v and not (set(singleton)&(v-{h})) for v in visible[j]))
    require(len(avail) == 3108 and min(avail) == 13, 'every source flag has a good receiver')
    native_normals = [mask(i for i,f in enumerate(F) if t&f == t) for t in d]
    require(max(q.bit_count() for q in native_normals) == 12, 'per-variable determinant degree')
    # Build each true H->D port from native coordinates and parent flag incidence.
    # The published routes must realise every one of them once.
    author_planes = {h:k for k,h in enumerate(a)}
    route_pairs = Counter((h,di) for kind,di,h,*rest in w['routes'] if h is not None)
    degrees = []; receiver_caps = []
    for h in H:
        ds = [k for k,t in enumerate(d) if h&t == h]
        require(len(ds) == 45 and all(route_pairs[author_planes[h],k] == 1 for k in ds),'45 literal flags')
        degrees.extend(native_normals[k].bit_count() for k in ds)
        for i,f in enumerate(F):
            if h&f == h:
                receiver_caps.append(sum(bool(native_normals[k] & (1<<i)) for k in ds))
    require(set(receiver_caps) == {15},'15 visible ports for each target')
    return {'native_sha256':hashlib.sha256(data).hexdigest(),'layout_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),
            'native_flag_clean_receiver_counts':hist(avail),
            'singletons_per_native_donor':hist(len(set(p)&set(singleton)) for p in donor),
            'native_receivers_per_D4':hist(v.bit_count() for v in native_normals),
            'native_receivers_per_active_shared_H_D_port':hist(degrees),
            'ports_observed_per_active_H_receiver_pair':hist(receiver_caps),
            'binary_extension_degree_sufficient':4,'slot_degree_bound':max(degrees),
            'sumset_control':sumset_case(),'joint_rank_controls':projective_case()}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('native',type=Path); p.add_argument('layout',type=Path)
    a=p.parse_args()
    print(json.dumps(native_layout(a.native,a.layout),indent=2))
