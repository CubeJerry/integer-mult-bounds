#!/usr/bin/env python3
"""Exact small cover/rank checks, not a physical pencil or runtime test."""
from itertools import product
from math import comb
from pathlib import Path
from fractions import Fraction
import hashlib, json, datetime


def rank2(values):
    basis = {}
    for v in values:
        while v:
            p = v.bit_length()-1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    return len(basis)


def case(q, r):
    words = list(product(range(q), repeat=r))
    n = len(words)
    pairs = [(u,v) for u in words for v in words
             if all(a != b for a,b in zip(u,v))]
    full = (1 << len(pairs))-1
    cuts = []
    # Complementing a cut leaves separation unchanged, so fix c(0)=0.
    for masks in product(range(1 << (q-1)), repeat=r):
        maps = tuple(mask << 1 for mask in masks)
        covered = 0
        for j,(u,v) in enumerate(pairs):
            if all(((c >> a) ^ (c >> b)) & 1
                   for c,a,b in zip(maps,u,v)):
                covered |= 1 << j
        cuts.append((maps, covered))
    remaining, chosen = full, []
    while remaining:
        best = max(cuts, key=lambda x:(x[1]&remaining).bit_count())
        removed = (best[1]&remaining).bit_count()
        assert removed > 0
        assert removed * (1 << r) >= remaining.bit_count()
        chosen.append(best)
        remaining &= ~best[1]
    K_bound = (1 << r)*(2*r*(q.bit_length()-1)+1)
    assert len(chosen) <= K_bound
    matrices, loads = [], [0]*n
    scalar_sum = 0
    covered_pairs = set()
    for masks, covered in chosen:
        for orientation in product((0,1), repeat=r):
            left = [i for i,w in enumerate(words) if all(
                ((mask >> a)&1)==bit for mask,a,bit in zip(masks,w,orientation))]
            right = [i for i,w in enumerate(words) if all(
                ((mask >> a)&1)!=(bit) for mask,a,bit in zip(masks,w,orientation))]
            if not left or not right:
                continue
            matrix = 0
            for i in left:
                loads[i] += 1
                for j in right:
                    assert all(a != b for a,b in zip(words[i],words[j]))
                    matrix |= 1 << (i*n+j)
                    covered_pairs.add((words[i],words[j]))
            matrices.append(matrix)
            scalar_sum ^= matrix
    assert covered_pairs == set(pairs)
    assert max(loads) <= len(chosen)
    target = sum(1 << (i*n+j) for i,u in enumerate(words)
                 for j,v in enumerate(words) if all(a != b for a,b in zip(u,v)))
    target_rows = [(target >> (i*n)) & ((1<<n)-1) for i in range(n)]
    assert rank2(target_rows) == n
    span_rank = rank2(matrices)
    solvable = rank2(matrices+[target]) == span_rank
    if len(matrices) < n:
        assert not solvable
    if q == 2:
        assert solvable and scalar_sum == target
    elif r:
        assert not solvable  # actual selected small greedy families, not universal
        assert scalar_sum != target
    # A true set cover can change multiplicities and still fail the exact identity.
    return {'q':q,'r':r,'words':n,'unequal_pairs':len(pairs),
            'cut_tuples':len(chosen),'proved_cut_bound':K_bound,
            'nonempty_rectangles':len(matrices),'max_source_incidence':max(loads),
            'target_rank':n,'rectangle_matrix_span_rank':span_rank,
            'scalar_weighted_identity_solvable_F2':solvable,
            'unit_weight_identity_correct':scalar_sum==target}


def main():
    cases=[case(q,r) for q,r in [(2,0),(2,1),(2,2),(2,3),(4,1),(4,2),(8,1)]]
    global_cases=[]
    for d in (4,8,16,32):
        h=2*d-1
        t=8*d
        z=(t-2)*d*d+2
        m=1<<z
        q=1<<t
        r=d-2
        C=comb(h,d)
        K=(1<<r)*(2*r*t+1)
        ratio=Fraction(C**(d+1)*(K*(1<<r))**d, q**(r*d))
        rank_floor=Fraction(m-1,m)
        assert ratio < rank_floor
        assert t*d*d == 2*d*d-2+z
        global_cases.append({'d':d,'t':t,'log2_m':z,
                             'rectangle_ratio_below_rank_floor':True,
                             'ratio_numerator_bits':ratio.numerator.bit_length(),
                             'ratio_denominator_bits':ratio.denominator.bit_length()})
    p=Path(__file__).resolve()
    result={'status':'PASS_EXACT_COVER_AND_RANK_CHECKS',
            'executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'checker_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'note_sha256':hashlib.sha256(p.with_name('overlapping-cover-rank-gap.md').read_bytes()).hexdigest(),
            'cases':cases,'balanced_parameter_rank_obstructions':global_cases,
            'scope':'Exact finite greedy coverage, independent matrix span/rank checks and integer inequalities; no physical pencil, asymptotic runtime or full multiplier execution.'}
    p.with_name('overlapping-cover-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
