#!/usr/bin/env python3
"""Exact positive nine-port partition certificate; no optimization oracle."""
from __future__ import annotations
import argparse
import collections
import gzip
import hashlib
import itertools
import json
import pathlib

LAYOUT_SHA = '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR_SHA = '346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'

def mul(a, b, polynomial=0b100101):
    c = 0
    while b:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
        if a & 32:
            a ^= polynomial
    return c

def power(a, n):
    r = 1
    while n:
        if n & 1:
            r = mul(r, a)
        a = mul(a, a)
        n >>= 1
    return r

def rank(rows):
    a = [list(r) for r in rows]
    if not a:
        return 0
    nr, nc, p = len(a), len(a[0]), 0
    for j in range(nc):
        k = next((k for k in range(p,nr) if a[k][j]), None)
        if k is None:
            continue
        a[p],a[k]=a[k],a[p]
        inv=power(a[p][j],30)
        a[p]=[mul(inv,x) for x in a[p]]
        for k in range(p+1,nr):
            if a[k][j]:
                v=a[k][j]
                a[k]=[x ^ mul(v,y) for x,y in zip(a[k],a[p])]
        p+=1
        if p==nr:
            break
    return p

def canonical(v):
    s=next(x for x in v if x)
    return tuple(v if s>0 else [-x for x in v])

def binary_rows(a):
    rows=[]
    for rr in a:
        for bit in range(5):
            row=0
            for j,c in enumerate(rr):
                for k in range(5):
                    row |= ((mul(c,1<<k)>>bit)&1)<<(5*j+k)
            rows.append(row)
    return rows

def binary_word(a):
    n=len(a); rows=binary_rows(a)
    original=list(rows); operations=[]
    def add(dst,src):
        assert dst!=src
        rows[dst]^=rows[src]
        operations.append([dst,src])
    for j in range(5*n):
        p=next(k for k in range(j,5*n) if (rows[k]>>j)&1)
        if p!=j:
            add(j,p);add(p,j);add(j,p)
        for k in range(5*n):
            if k!=j and ((rows[k]>>j)&1):add(k,j)
    assert rows==[1<<j for j in range(5*n)]
    word=operations[::-1]
    replay=[1<<j for j in range(5*n)]
    for dst,src in word:replay[dst]^=replay[src]
    assert replay==original
    return word

def rectangular_add_count(a):
    return sum(mul(c,1<<k).bit_count() for row in a for c in row for k in range(5))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    args=ap.parse_args()
    raw=gzip.decompress((args.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==LAYOUT_SHA
    atlas=json.loads(raw)
    factor_raw=(args.repo/'research/moonshot-005-program/results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json').read_bytes()
    assert hashlib.sha256(factor_raw).hexdigest()==FACTOR_SHA
    factor=dict(json.loads(factor_raw)['factors'])
    roots=atlas['root_table']
    a2=[tuple(sorted(h)) for h in atlas['A2']]
    d4=[tuple(sorted(d)) for d in atlas['D4']]
    dsets=list(map(set,d4))
    root_id={canonical(v):j for j,v in enumerate(roots)}
    a_id={h:j for j,h in enumerate(a2)}
    d_id={d:j for j,d in enumerate(d4)}
    assert len(root_id)==120 and len(a_id)==1120 and len(d_id)==3150
    x={h:12//sum(j<111 for j in hh)+factor.get(h,0) for h,hh in enumerate(a2) if min(hh)<111}
    assert all(45*sum(x[h] for h,hh in enumerate(a2) if j in hh)==5760 for j in range(111))
    assert collections.Counter(x[h] for h,hh in enumerate(a2) if max(hh)<111)=={4:709,5:84,6:88}
    assert all(sum(x*x for x in v)==4 for v in roots)
    ortho=[{j for j,v in enumerate(roots) if sum(x*y for x,y in zip(u,v))==0} for u in roots]
    plane_ports=[[d for d,ds in enumerate(dsets) if set(h)<=ds] for h in a2]
    receivers=[[i for i,o in enumerate(ortho) if set(h)<=o] for h in a2]
    assert set(map(len,plane_ports))=={45}
    assert set(map(len,receivers))=={36}
    reflections=[]
    for s in roots:
        perm=[]
        for v in roots:
            dot=sum(x*y for x,y in zip(s,v))
            assert dot%2==0
            perm.append(root_id[canonical([x-(dot//2)*y for x,y in zip(v,s)])])
        assert sorted(perm)==list(range(120))
        assert all(perm[perm[j]]==j for j in range(120))
        reflections.append(perm)
    base=json.loads((pathlib.Path(__file__).parent/'BASE-PARTITION.json').read_text())
    start=base['H']
    assert base['ports']==plane_ports[start]
    assert base['receivers']==receivers[start]
    classes={start:[[base['ports'][p] for p in c] for c in base['classes']]}
    predecessors={start:None}
    todo=collections.deque([start])
    while todo:
        h=todo.popleft()
        for generator,perm in enumerate(reflections):
            hh=a_id[tuple(sorted(perm[j] for j in a2[h]))]
            if hh in classes:
                continue
            dd={d:d_id[tuple(sorted(perm[j] for j in d4[d]))] for d in plane_ports[h]}
            classes[hh]=[sorted(dd[d] for d in c) for c in classes[h]]
            predecessors[hh]=[h,generator]
            todo.append(hh)
    assert len(classes)==1120
    intersections=collections.Counter()
    native_inc=collections.Counter()
    pair_intersections=collections.Counter()
    used_triples=set()
    for h in range(1120):
        cl=classes[h]
        assert len(cl)==5 and set(map(len,cl))=={9}
        assert sorted(itertools.chain.from_iterable(cl))==plane_ports[h]
        m=sum(j<111 for j in a2[h])
        for i in receivers[h]:
            visible=[d for d in plane_ports[h] if dsets[d]<=ortho[i]]
            assert len(visible)==15
            seen=set(visible)
            for c in cl:
                local=tuple(k for k,d in enumerate(c) if d in seen)
                assert len(local)==3
                used_triples.add(local)
            intersections[(m,len(visible))]+=1
            if i<111:
                native_inc[m]+=1
        for c in cl:
            patterns=[set(d for d in c if dsets[d]<=ortho[i]) for i in receivers[h]]
            for a,b in itertools.combinations(patterns,2):
                pair_intersections[len(a&b)]+=1
    # A complete field and Vandermonde verification, independent of the
    # closed determinant formula used in the proof.
    assert all(mul(x,power(x,30))==1 for x in range(1,32))
    v9=[[power(a,j) for j in range(9)] for a in range(1,10)]
    v18=[[power(a,j) for j in range(18)] for a in range(1,19)]
    assert rank(v9)==9 and rank(v18)==18
    full_minor_count=0
    for rows in itertools.combinations(range(9),3):
        for donor in range(3):
            assert rank([[v9[r][j] for j in range(3*donor,3*donor+3)] for r in rows])==3
            full_minor_count+=1
    hermite_minor_count=0
    for ports in itertools.combinations(range(9),3):
        nodes=[2*p+s+1 for p in ports for s in (0,1)]
        mat=[]
        for a in nodes:
            mat.append([power(a,j) for j in range(12)])
            mat.append([power(a,j-1) if j&1 else 0 for j in range(12)])
        assert rank(mat)==12
        hermite_minor_count+=1
    cross=json.loads((pathlib.Path(__file__).parent/'UNIVERSAL-C.json').read_text())
    c=cross['matrix']
    assert len(c)==18 and all(len(r)==18 for r in c)
    assert all(0<=x<32 for row in c for x in row)
    punctured_minor_count=0
    zero_crosswave_ranks=collections.Counter()
    for ports in itertools.combinations(range(9),3):
        rows=[2*p+s for p in ports for s in (0,1)]
        for donor in range(2):
            mat=[[v18[r][j] for j in range(9*donor,9*donor+9)]+[0]*3 for r in rows]
            mat += [[c[r][j] for j in range(9*donor,9*donor+9)]+[v18[r][j] for j in range(3*donor,3*donor+3)] for r in rows]
            assert rank(mat)==12
            punctured_minor_count+=1
            zero=[[v18[r][j] for j in range(9*donor,9*donor+9)]+[0]*3 for r in rows]
            zero += [[0]*9+[v18[r][j] for j in range(3*donor,3*donor+3)] for r in rows]
            zero_crosswave_ranks[rank(zero)]+=1
    full_holder_checks=0
    for x in (2,3,4,5,6):
        strata=[[] for _ in range(3*x)]
        for donor in range(3):
            for p in range(9):
                for s in range(x):strata[s+x*((donor+p)%3)].append((donor,p,s))
        for stripe in strata:
            assert collections.Counter(d for d,p,s in stripe)=={0:3,1:3,2:3}
            assert sorted(p for d,p,s in stripe)==list(range(9))
            full_holder_checks+=1
    strata=[[] for _ in range(6)]
    for donor in range(2):
        for p in range(9):
            for s in range(2):strata[s+2*((donor+p)%3)].append((donor,p,s))
    ground_per_port=collections.Counter()
    for stripe in strata:
        assert collections.Counter(d for d,p,s in stripe)=={0:3,1:3}
        occupied=collections.Counter(p for d,p,s in stripe)
        assert max(occupied.values())==1
        for p in range(9):ground_per_port[p]+=2-occupied[p]
    assert set(ground_per_port.values())=={8}
    word9=binary_word(v9);word18=binary_word(v18)
    c_adds=rectangular_add_count(c)
    derivative=[[power(a,j-1) if j&1 else 0 for j in range(18)]for a in range(1,19)]
    derivative_adds=rectangular_add_count(derivative)
    full_add_bound=120*(len(word9)+8*3*5)
    punctured_add_bound=30*(2*len(word18)+2*17*3*5+c_adds+18*5)
    singleton_adds=30*(len(word18)+derivative_adds+9*5)
    # Two-wave literal public/cache replay, on all 180 independent input
    # columns, including an arbitrary independent late baseline.
    early=[1<<j for j in range(90)]
    late=[1<<(90+j) for j in range(90)]
    cache=list(early)
    for dst,src in word18:early[dst]^=early[src]
    for dst,src in word18:late[dst]^=late[src]
    late_before=list(late)
    c_binary=binary_rows(c)
    for dst,row in enumerate(c_binary):
        for src in range(90):
            if (row>>src)&1:late[dst]^=cache[src]
    v_binary=binary_rows(v18)
    assert early==v_binary
    assert late==[(v<<90)^cc for v,cc in zip(v_binary,c_binary)]
    assert cache==[1<<j for j in range(90)]
    assert late!=late_before
    early=[1<<j for j in range(90)]
    late=[1<<(90+j) for j in range(90)]
    odd_bits=[5*j+k for j in range(1,18,2) for k in range(5)]
    cache=[early[j] for j in odd_bits]
    for dst,src in word18:early[dst]^=early[src]
    derivative_binary=binary_rows(derivative)
    for dst,row in enumerate(derivative_binary):
        for k,src in enumerate(odd_bits):
            if (row>>src)&1:late[dst]^=cache[k]
    assert early==v_binary
    assert late==[(1<<(90+j))^dd for j,dd in enumerate(derivative_binary)]
    assert cache==[1<<j for j in odd_bits]
    cert={'base_plane':start,'predecessors':predecessors,'classes':classes}
    cert_bytes=json.dumps(cert,sort_keys=True,separators=(',',':')).encode()
    result={
        'status':'PASS_NATIVE_NINE_PORT_PARTITION',
        'layout_sha256':LAYOUT_SHA,
        'factor_sha256':FACTOR_SHA,
        'parent_planes':1120,
        'native_plane_histogram':dict(collections.Counter(sum(j<111 for j in h) for h in a2)),
        'parent_receiver_plane_incidences':sum(intersections.values()),
        'native_receiver_plane_incidences_by_native_donor_count':dict(native_inc),
        'classes_per_plane':5,'ports_per_class':9,'receiver_ports_per_class':3,
        'within_class_receiver_pair_intersection_histogram':dict(pair_intersections),
        'distinct_sorted_class_receiver_triples':len(used_triples),
        'field_polynomial':'z^5+z^2+1','field_size':32,
        'v9_full_rank':True,'v18_full_rank':True,
        'full_v9_donor_minors_checked':full_minor_count,
        'singleton_hermite_minors_checked':hermite_minor_count,
        'universal_two_donor_full_transfer_minors_checked':punctured_minor_count,
        'zero_crosswave_rank_histogram':dict(zero_crosswave_ranks),
        'full_holder_stripes_checked':full_holder_checks,
        'public_two_wave_replay_independent_binary_columns':180,
        'arbitrary_late_baseline_replayed':True,
        'stationary_cache_dirty_at_clear':True,
        'literal_binary_word_adds':{'V9':len(word9),'V18':len(word18),'C18':c_adds,'Hermite_D18':derivative_adds},
        'local_ordinary_invoice':{
            'full_three_donor':{'ADD_bound_per_H':full_add_bound,'INIT_per_H':0,'CLEAR_per_H':0,'planes':881},
            'punctured_two_donor':{'ADD_bound_per_H':punctured_add_bound,'INIT_per_H':2700,'CLEAR_per_H':2700,'planes':227},
            'singleton':{'ADD_per_H':singleton_adds,'INIT_per_H':1350,'CLEAR_per_H':1350,'planes':11},
            'total_ADD_bound':881*full_add_bound+227*punctured_add_bound+11*singleton_adds,
            'total_INIT':227*2700+11*1350,
            'total_CLEAR':227*2700+11*1350,
            'additional_MOVE':0,
            'binary_native_copies_per_field_copy':5,
        },
        'partition_certificate_sha256':hashlib.sha256(cert_bytes).hexdigest(),
        'global_source_gluing_constructed':False,
        'complete_kappa_theorem':False,
    }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'PARTITIONS.json.gz').write_bytes(gzip.compress(cert_bytes,mtime=0))
    (args.out/'ADD-WORDS.json.gz').write_bytes(gzip.compress(json.dumps({'V9':word9,'V18':word18},separators=(',',':')).encode(),mtime=0))
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
