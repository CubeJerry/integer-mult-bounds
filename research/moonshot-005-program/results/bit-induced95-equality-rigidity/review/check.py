#!/usr/bin/env python3
"""Separate reconstruction of the induced95 rigidity premises and geometry."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

SOURCE = 'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
PIN = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
T = {14, 17, 19, 20, 96, 99, 101, 102}

def brank(values):
    pivots = {}
    for value in values:
        while value:
            p = value.bit_length()-1
            if p not in pivots:
                pivots[p] = value
                break
            value ^= pivots[p]
    return len(pivots)

def rowspace(rows):
    basis = {}
    for row in rows:
        v = list(map(Fraction, row))
        for j, other in sorted(basis.items()):
            x = v[j]
            if x:
                v = [a-x*b for a,b in zip(v,other)]
        pivot = next((j for j,x in enumerate(v) if x), None)
        if pivot is None:
            continue
        d = v[pivot]
        basis[pivot] = [x/d for x in v]
    return basis

def normal(basis):
    free = [j for j in range(8) if j not in basis]
    assert len(free) == 1
    vector = [Fraction(0)]*8
    vector[free[0]] = 1
    for j,row in sorted(basis.items(), reverse=True):
        vector[j] = -sum(row[k]*vector[k] for k in range(j+1,8))
    lcm = math.lcm(*(x.denominator for x in vector))
    vector = [int(x*lcm) for x in vector]
    divisor = math.gcd(*vector)
    vector = [x//divisor for x in vector]
    if next(x for x in vector if x)<0:
        vector = [-x for x in vector]
    return vector

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--author',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=(a.repo/SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==PIN
    roots=json.loads(raw)['native_roots']
    u=sorted(set(range(8,111))-T)
    dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    k=lambda i,j:int(i==j or dot(i,j)==0)
    star=json.loads((a.author/'STAR-CERTIFICATE.json').read_text())
    frame=star['frame'];edges=star['edges']
    assert len(frame)==len(set(frame))==8 and set(frame)<=set(u)
    assert all(k(i,j)==int(i==j) for i in frame for j in frame)
    assert len(edges)==21 and len({x['role'] for x in edges})==21
    assert len({tuple(x['points']) for x in edges})==21
    degree=Counter()
    for edge in edges:
        points=edge['points'];r=edge['role']
        assert r in set(u)-set(frame)
        assert [j for j,f in enumerate(frame) if k(r,f)]==points
        degree.update(points)
    assert [degree[i] for i in range(8)]==[5,5,5,5,5,5,7,5]
    for i,e in enumerate(edges):
        for f in edges[i+1:]:
            if set(e['points'])&set(f['points']):
                assert k(e['role'],f['role'])==0
    edge=edges[0];s,t=edge['points'];r=edge['role']
    xi={i:sum(k(i,f)<<j for j,f in enumerate(frame)) |
           ((k(i,r)^k(i,frame[s])^k(i,frame[t]))<<8) for i in u}
    assert brank(xi.values())==9
    assert all(((xi[i]&xi[j]).bit_count()&1)==k(i,j) for i in u for j in u)
    known=set(frame)|{e['role'] for e in edges}
    for i,anchors in star['ordered_anchors']:
        assert i in set(u)-known and len(anchors)==len(set(anchors))==8
        assert set(anchors)<=known and all(k(i,j)==0 for j in anchors)
        assert brank(xi[j] for j in anchors)==8
        known.add(i)
    assert known==set(u) and len(star['ordered_anchors'])==66
    supplied=json.loads((a.author/'FULL-SUPPORT-CERTIFICATE.json').read_text())
    cases={c['binary_code_mask']:c for c in supplied['all_nonzero_words']}
    assert set(cases)==set(range(1,512))
    histogram=Counter();proper=[]
    for mask in range(1,512):
        support=[i for i in u if (xi[i]&mask).bit_count()&1]
        assert support==cases[mask]['support']
        basis=rowspace(roots[i] for i in support)
        rank=len(basis);histogram[rank]+=1
        assert rank==cases[mask]['real_support_rank']
        if rank==7:
            n=normal(basis)
            assert all(sum(x*y for x,y in zip(n,roots[i]))==0 for i in support)
            proper.append({'mask':mask,'normal_line':n,'support_size':len(support)})
    assert histogram=={7:25,8:486}
    assert len({tuple(x['normal_line']) for x in proper})==25
    assert brank(x['mask'] for x in proper)==9
    assert next(x for x in proper if x['mask']==31)['normal_line']==[0,1,-1,0,-1,0,0,-1]
    # At any listed nonzero line, the scalar canonical shortening is 1D.
    shortening=[]
    for item in proper:
        n=item['normal_line']
        excluded=[i for i in u if sum(x*y for x,y in zip(n,roots[i]))]
        rank=brank(xi[i] for i in excluded)
        assert rank==8
        shortening.append({'mask':item['mask'],'excluded_evaluation_rank':rank,'shortening_dimension':1})
    result={'status':'PASS_INDEPENDENT_INDUCED95_RIGIDITY_PREMISES_AND_SUPPORTS',
            'source_sha256':PIN,'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),
            'star_edge_count':21,'degrees':[degree[i] for i in range(8)],'ordered_anchors':66,
            'all9025_Gram_entries_checked':True,'all511_support_ranks_recomputed':True,
            'support_rank_histogram':dict(sorted(histogram.items())),
            'proper_directions':proper,'proper_direction_rank':9,'all25_shortenings':shortening,
            'scope':'Finite premises independently reconstructed; arbitrary-block rigidity and equality-destination theorem reviewed separately. No formation price or complete supplier.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],dict(histogram),flush=True)

if __name__=='__main__':
    main()
