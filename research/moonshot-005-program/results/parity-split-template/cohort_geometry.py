#!/usr/bin/env python3
"""Independent source derivation of cohort geometry and paired-bank gates.

This file imports no author verifier or recovered group table.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

F = Fraction
SOURCE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
FRAME = [5, 56, 65, 69, 77, 96, 100, 103]

def require(p, message):
    if not p:
        raise ValueError(message)

def space(basis):
    out = {0}
    for v in basis:
        out |= {x ^ v for x in out}
    return frozenset(out)

def bit_basis(values):
    pivots = {}
    for value in sorted(values):
        x = value
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    for bit in sorted(pivots):
        for hi in sorted(pivots):
            if hi > bit and (pivots[hi] >> bit) & 1:
                pivots[hi] ^= pivots[bit]
    return sorted(pivots.values())

def rank(matrix):
    if not matrix:
        return 0
    work = [list(map(F, row)) for row in matrix]
    piv = 0
    for col in range(len(work[0])):
        hit = next((i for i in range(piv, len(work)) if work[i][col]), None)
        if hit is None:
            continue
        work[piv], work[hit] = work[hit], work[piv]
        d = work[piv][col]
        work[piv] = [x / d for x in work[piv]]
        for i in range(len(work)):
            if i != piv and work[i][col]:
                d = work[i][col]
                work[i] = [x - d * y for x, y in zip(work[i], work[piv])]
        piv += 1
        if piv == len(work):
            break
    return piv

def root(bits):
    ones = [i for i in range(9) if (bits >> i) & 1]
    if len(ones) == 3:
        if 8 in ones:
            return [2 * int(i in ones) for i in range(8)]
        return [1 if i in ones else -1 for i in range(8)]
    require(len(ones) == 7, 'root bit weight')
    absent = [i for i in range(9) if i not in ones]
    i, j = absent
    if j == 8:
        return [1 if k == i else -1 for k in range(8)]
    return [2 * (int(k == i) - int(k == j)) for k in range(8)]

def derive(source):
    xs = sorted(source['live'])
    require(len(xs) == 104 and len(set(xs)) == 104, '104 distinct first-X roles')
    spans = [space(b) for b in source['frames']]
    roots = {x: root(source['frames'][source['initial'][x]][0]) for x in xs}
    gram = {(x,y): sum(a*b for a,b in zip(roots[x],roots[y])) for x in xs for y in xs}
    require(all(gram[x,y] == 8 * (x == y) for x in FRAME for y in FRAME), 'orthogonal selected frame')
    facets = {x: source['final'][x+112] for x in FRAME}
    dports = source['hosted']['Dports']
    hosted = {xs[i]: (source['hosted']['X2'][j], source['hosted']['Y2'][j]) for j,i in enumerate(dports)}
    coupled = sorted(set(xs) - set(hosted))
    for x,(b,d) in hosted.items():
        require(source['initial'][x] == source['initial'][b], 'paired line cochart')
        require(source['initial'][x+112] == source['initial'][d], 'paired Y initial cochart')
        require(source['final'][x] == source['final'][b] == 127, 'paired hub endpoint')
        require(source['final'][x+112] == source['final'][d], 'paired facet endpoint')
    groups = defaultdict(list)
    for x in xs:
        if x in FRAME:
            continue
        line = spans[source['initial'][x]]
        recipients = tuple(r for r in FRAME if line <= spans[facets[r]])
        nonzero = tuple(r for r in FRAME if gram[r,x] != 0)
        require(recipients == nonzero and len(recipients) == 4, 'four matching incidence and aggregate recipients')
        groups[recipients].append(x)
    derived=[]
    for recipients, donors in sorted(groups.items()):
        C = set.intersection(*(set(spans[facets[r]]) for r in recipients))
        basis=bit_basis(C)
        require(len(basis) == 6 and space(basis) == C, 'rank-six exact acquisition intersection')
        require(all(spans[source['initial'][d]] <= C for d in donors), 'all donor initial lines contained')
        A = [[-F(gram[r,d],8) for d in donors] for r in recipients]
        require(rank(A) == 4, 'full four-row acquisition rank')
        hosted_donors=[d for d in donors if d in hosted]
        coupled_donors=[d for d in donors if d not in hosted]
        AH=[[-F(gram[r,d],8) for d in hosted_donors] for r in recipients]
        AC=[[-F(gram[r,d],8) for d in coupled_donors] for r in recipients]
        annihilator=[n for n in range(512) if all((n & x).bit_count()%2 == 0 for x in basis)]
        odd=[n for n in annihilator if n.bit_count()%2]
        active_facets=[r for r in xs if C <= spans[source['final'][r+112]]]
        require(active_facets == list(recipients), 'exact source active-facet containment trap')
        derived.append(dict(receivers=list(recipients),facets=[facets[r] for r in recipients],donors=donors,
            intersection_basis=basis,annihilator=annihilator,odd_annihilator=odd,
            A=[[str(v) for v in row] for row in A],rank=4,
            hosted_donors=hosted_donors,coupled_donors=coupled_donors,
            hosted_rank=rank(AH),coupled_rank=rank(AC),
            exact_future_monotone_receiver_set=active_facets))
    require(len(groups)==14 and Counter(map(len,groups.values()))=={4:2,7:8,8:4}, '14 group source partition')
    require(sum(len(g['coupled_donors']) for g in derived)==8, 'all eight coupled donors located once')
    return dict(status='PASS_SOURCE_COHORT_GEOMETRY_AND_PAIRED_BANK_ALIAS_AUDIT',source_sha256=SOURCE_PIN,
        selected_frame=FRAME,ordinary_hosted_ports=len(hosted),coupled_roles=coupled,
        independent_X2_bank_missing_exactly_at=coupled,groups=derived,
        hosted_only_rank_profile=dict(Counter(g['hosted_rank'] for g in derived)),
        new_complete_kappa=None,
        scope='Exact finite source geometry and rational row ranks only. No literal cohort word or physical compiler claim.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=a.source.read_bytes();require(hashlib.sha256(raw).hexdigest()==SOURCE_PIN,'source byte pin')
    result=derive(json.loads(gzip.decompress(raw)))
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='groups'},indent=2))

if __name__=='__main__':main()
