#!/usr/bin/env python3
"""Independent source reconstruction and filtration controls; Apache-2.0.
@CubeJerry with OpenAI assistance. No author verifier imported.
"""
import argparse
import gzip
import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path

def need(condition, message):
    if not condition:
        raise ValueError(message)

def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length()-1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return len(pivots)

def lift(rows, width):
    result = []
    for row in rows:
        for a in range(width):
            result.append(sum(((row >> j) & 1) << (j*width+a) for j in range(111)))
    return result

def multiply(a, b, n):
    return [sum((sum(((a[i] >> k)&1)*((b[k] >> j)&1) for k in range(n))%2)<<j for j in range(n)) for i in range(n)]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--author', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78', 'native pin')
    source = json.loads(gzip.decompress(raw))
    roots = [[Fraction(x) for x in source['frames'][str(source['start'][i])]['B'][0]] for i in range(111)]
    K = [sum(int(i == j or sum(x*y for x,y in zip(roots[i],roots[j])) == 0)<<j for j in range(111)) for i in range(111)]
    need(rank(K) == 9, 'canonical code dimension')
    sets = [[2,9,12,30,38,42], [2,26,63,65,81,87]]
    masks = [sum(1<<j for j in s) for s in sets]
    available = [[i for i in range(111) if i not in s and K[i]&m == m and K[i].bit_count()-1 <= 58] for s,m in zip(sets,masks)]
    need([len(s) for s in available] == [17,17] and len(set(available[0]) & set(available[1])) == 5, 'source patch incidence')
    F = [row ^ (masks[0] if i in available[0] else masks[1] if i in available[1] else 0) for i,row in enumerate(K)]
    need(all((row>>i)&1 and row&~K[i] == 0 for i,row in enumerate(F)), 'scalar fitting contract')
    ell = sum(int(r.bit_count()-1>36)+int(r.bit_count()-1>52) for r in F)
    need(ell == 193 and rank(F) == 11 and rank(F+K) == 11, 'sharp scalar fitting')
    frozen = json.loads((args.author/'SCALAR-FITTING.json').read_text())
    need([int(x,16) for x in frozen['fitting_rows_hex']] == F, 'independently reconstructed frozen fitting')
    need([int(x,16) for x in frozen['canonical_rows_hex']] == K, 'canonical source agreement')
    tensors = []
    for v in [1,2,3,5,8]:
        a,c = lift(F,v),lift(K,v)
        d = rank(a+c)-rank(c)
        need(rank(a)==11*v and d==2*v, 'sharp tensor lift')
        tensors.append({'width':v,'rank':rank(a),'quotient':d,'ell':ell})

    # Alter only extant foreign blocks, so the fitting support and ell stay fixed.
    foreign = [(i,j) for i in range(111) for j in range(111) if i!=j and (F[i]>>j)&1]
    controls = []
    for name,v,perturbations in [
        ('noncommuting_triangular',3,[(0,0,1),(1,1,2)]),
        ('invariant_layers_2_plus_3',5,[(0,0,1),(1,1,0),(2,2,3),(3,3,4),(4,4,2),(5,0,4)])
    ]:
        rows = lift(F,v)
        for f,a,b in perturbations:
            i,j = foreign[f]
            rows[i*v+a] ^= 1<<(j*v+b)
        c = lift(K,v)
        d = rank(rows+c)-rank(c)
        layers = [1,1,1] if v==3 else [2,3]
        ds=[]
        start=0
        for size in layers:
            columns=[j*v+a for j in range(111) for a in range(start,start+size)]
            restricted=[sum(((rows[i*v+a]>>old)&1)<<new for new,old in enumerate(columns)) for i in range(111) for a in range(start,start+size)]
            cc=lift(K,size)
            ds.append(rank(restricted+cc)-rank(cc))
            start+=size
        need(d >= sum(ds), 'stacked rectangular filtration rank')
        need(all(z >= 2*s for z,s in zip(ds,layers)) if name=='noncommuting_triangular' else d>=7, 'claimed filtration lower bound')
        controls.append({'name':name,'width':v,'layers':layers,'layer_quotients':ds,'quotient':d})
    e12=[2,0,0];e23=[0,4,0]
    need(multiply(e12,e23,3)!=multiply(e23,e12,3), 'noncommuting flag-preserving blocks')
    # Opposite nilpotents have distinct kernels even after scalar extension.
    n12=[2,0];n21=[0,1]
    need([x for x in [1,2,3] if all((row&x).bit_count()%2==0 for row in n12)]==[1], 'first unique kernel line')
    need([x for x in [1,2,3] if all((row&x).bit_count()%2==0 for row in n21)]==[2], 'second unique kernel line')
    # Rectangular block sizes are deliberately unequal. Above-diagonal blocks
    # are unrestricted; diagonal minors witness the universal proof in REVIEW.
    rng=random.Random(20261114)
    count=0
    for heights,widths in [([2,4,1],[3,1,5]),([1,3],[4,2]),([3,2,4],[1,5,2])]:
        offsets=[0]
        for w in widths: offsets.append(offsets[-1]+w)
        for _ in range(100):
            whole=[];lower=0
            for a,h in enumerate(heights):
                diagonal=[]
                for _ in range(h):
                    row=0
                    for b in range(a,len(widths)):
                        row |= rng.randrange(1<<widths[b])<<offsets[b]
                    diagonal.append((row>>offsets[a])&((1<<widths[a])-1))
                    whole.append(row)
                lower+=rank(diagonal)
            need(rank(whole)>=lower, 'rectangular upper-triangular rank control')
            count+=1
    need(rank([3,3])==1, 'below-diagonal negative control')
    # Rank must not count repeated rows as new directions.
    need(rank([1,1,2,3])==2, 'duplicate-row rank control')
    report={'status':'PASS_INDEPENDENT_INVARIANT_FILTRATION_REVIEW',
        'author_proof_sha256':hashlib.sha256((args.author/'PROOF.md').read_bytes()).hexdigest(),
        'native_sha256':hashlib.sha256(raw).hexdigest(),'scalar_ell':ell,
        'tensor_controls':tensors,'operator_controls':controls,
        'rectangular_rank_controls':count,
        'negative_controls':['nonzero lower block invalidates diagonal rank sum','opposite nilpotents have no common invariant line','repeated rows do not add rank'],
        'universal_status':'Direct mathematical proof reviewed separately; finite controls are not the theorem.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'])

if __name__=='__main__':
    main()
