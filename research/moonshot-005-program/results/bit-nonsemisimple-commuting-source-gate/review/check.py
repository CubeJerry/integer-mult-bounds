#!/usr/bin/env python3
"""Independent native readback for two scoped S027 gates; no author imports."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from hashlib import sha256
import gzip, json


def rank(rows):
    # Deliberately use explicit coordinate arrays, not the author's bit pivots.
    rows = list(rows)
    n = max((v.bit_length() for v in rows), default=0)
    a = [[(v >> k) & 1 for k in range(n)] for v in rows]
    p = 0
    for k in range(n):
        t = next((t for t in range(p, len(a)) if a[t][k]), None)
        if t is None: continue
        a[t], a[p] = a[p], a[t]
        for j in range(len(a)):
            if j != p and a[j][k]: a[j] = [u ^ v for u, v in zip(a[j], a[p])]
        p += 1
    return p


def graph_dimension(units):
    n = len(units[0])
    return rank((1 << r) | (A[r] << n) | (B[r] << (2*n))
                for A in units for B in units for r in range(n))


def f4(a, b):
    v = 0
    while b:
        if b & 1: v ^= a
        a <<= 1
        if a & 4: a ^= 7
        b >>= 1
    return v


def algebra_controls():
    # Local nonsplit algebra F4[eps]/eps^2 in its four-dimensional F2 module.
    def left_matrix(a, b):
        cols = []
        for j in range(4):
            c, d = (1 << j) & 3, (1 << j) >> 2
            cols.append(f4(a, c) | ((f4(a, d) ^ f4(b, c)) << 2))
        return [sum(((cols[j] >> i) & 1) << j for j in range(4)) for i in range(4)]
    nonsplit = {}
    for a in (1, 2, 3):
        family = [left_matrix(a, b) for b in range(4)]
        assert all(rank(A) == 4 for A in family)
        dim = graph_dimension(family)
        assert dim == 8 < 12
        nonsplit[str(a)] = dim
    # Three-dimensional single primary block, nonzero radical rank two.
    I, N, N2 = [1, 2, 4], [2, 4, 0], [4, 0, 0]
    units = [[I[j] ^ (u*N[j]) ^ (v*N2[j]) for j in range(3)]
             for u, v in product((0, 1), repeat=2)]
    jordan_dim = graph_dimension(units)
    assert jordan_dim == 7 < 9
    gl2 = [list(A) for A in product(range(4), repeat=2) if rank(A) == 2]
    assert graph_dimension(gl2) == 6
    return {'nonsplit_fixed_residue_spans': nonsplit,
            'nonsplit_full_input_dimension': 12,
            'jordan3_span': jordan_dim, 'jordan3_input_dimension': 9,
            'unrestricted_noncommuting_GL2_span': 6}


def load_repo(repo):
    base = repo/'research/moonshot-005-program/results'
    paths = [base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
             base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz']
    raw = [gzip.decompress(p.read_bytes()) for p in paths]
    assert sha256(raw[0]).hexdigest() == '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    assert sha256(raw[1]).hexdigest() == '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
    layout = json.loads(raw[0]); routes = [json.loads(line) for line in raw[1].splitlines()]
    roots = layout['root_table']
    orth = [{j for j in range(len(roots)) if sum(a*b for a,b in zip(x, roots[j])) == 0}
            for x in roots]
    return base, layout, routes, orth, [{'path':str(p.relative_to(repo)), 'sha256':sha256(p.read_bytes()).hexdigest()} for p in paths]


def commuting(layout, routes, orth):
    h = 263; H = list(map(set, layout['A2'])); D = list(map(set, layout['D4']))
    native = set(range(111)); donors = H[h] & native
    assert donors == {0, 61, 62}
    visible = {}
    for j in donors:
        visible[j] = {i:[P for P in H if j in P and P <= orth[i]]
                      for i in range(111) if H[h] <= orth[i]}
    receivers = [i for i in range(111) if all(i in visible[j] and len(visible[j][i]) == 16
                  and all(len(P & native) > 1 for P in visible[j][i]) for j in donors)]
    assert len(receivers) == 33 and 80 not in receivers and 10 not in donors
    ports = [d for d,P in enumerate(D) if H[h] <= P]
    masks = {d:sum(1 << i for i in receivers if i in D[layout['dual_D4'][d]]) for d in ports}
    assert len(ports) == 45 and all(masks.values())
    common = Counter((masks[a] & masks[b]).bit_count() for a,b in combinations(ports, 2))
    assert 0 not in common and sum(common.values()) == 990
    assert all(sum((masks[d] >> i) & 1 for d in ports) == 15 for i in receivers)
    atH = [r for r in routes if r[3] == h]
    assert len(atH) == 90 and all(r[0] == 'X' for r in atH)
    assert Counter(r[1] for r in atH) == Counter({j:30 for j in donors})
    assert Counter(r[4] for r in atH) == Counter({d:2 for d in ports})
    assert len({(r[1],r[2]) for r in atH}) == 90
    # A missing route is observable; the all-early premise is not inferred from
    # normalized prices or from the abstract incidence alone.
    assert len(atH[1:]) != 3*30
    changed = dict(masks); changed[ports[0]] = 1 << 111
    assert any(not(changed[a]&changed[b]) for a,b in combinations(ports, 2))
    return {'status':'PASS_INDEPENDENT_COMMUTING_EARLY_GATE_REVIEW',
            'H':h, 'donors':sorted(donors), 'joint_tight_receivers':receivers,
            'actual_early_owners':len(atH), 'ports':len(ports),
            'pairwise_audience_intersections':dict(common),
            'algebra':algebra_controls(), 'missing_route_control_rejected':True,
            'disjoint_audience_control_rejected':True,
            'older_balanced_phase_transfer_claimed':False}


def support(base, layout, routes, orth):
    pairpath = base/'bit-near-minimum-foreign-rank/author/output/ALL-PAIR-CUTS.json.gz'
    raw = gzip.decompress(pairpath.read_bytes())
    assert sha256(raw).hexdigest() == '9ec1cca0763b1c365a7c76a3ada6fcbd0ae90e434e9fed347cf5a958ff22ed50'
    coefficients = {(v['receiver'],v['donor']):Fraction(v['coefficient']) for v in json.loads(raw)}
    receipts = []
    for i in (26,34,80):
        neighbors = orth[i] & set(range(111))
        incomingX = [r for r in routes if r[0]=='X' and r[7]==i]
        incomingY = [r for r in routes if r[0]=='Y' and r[1]==i]
        assert len(incomingX)==360 and len(incomingY)==480
        cs = [coefficients[i,j] for j in neighbors]
        ratio = (Fraction(len(neighbors))-21)/sum(cs)
        if i in (26,34):
            assert len(neighbors)==60 and Counter(cs)==Counter({Fraction(3):57,Fraction(7,2):3})
            assert ratio==Fraction(26,121)
        else:
            assert len(neighbors)==62 and ratio==Fraction(2952,14239)
        floors=[]
        for bank in (480,1920,5760):
            h=0
            while sum(max(0,bank-(c*h).numerator//(c*h).denominator) for c in cs)>21*bank: h+=1
            floors.append(h)
        if i in (26,34): assert floors==[104,413,1238]
        receipts.append({'receiver':i,'degree':len(neighbors),'terminal_fields':840,
                         'excess_ratio':str(ratio),'copied_bank_floors':floors})
    D=list(map(set,layout['D4'])); H=list(map(set,layout['A2']))
    tiles=[12,99,549,600,968]
    union=set().union(*(D[d]&set(range(111)) for d in tiles))
    assert len(union)==31 and {1,80}<=H[370]
    assert all(H[370]<=D[layout['dual_D4'][d]] for d in tiles)
    # Nonlinear alphabet control: one two-donor packet that applies an arbitrary
    # binary relabeling still cannot recover two independent output bits.
    scalar_checks=0
    for table in product(range(2),repeat=4):
        for decode in product(range(4),repeat=2):
            image=[decode[table[x]] for x in range(4)]
            assert image!=list(range(4))
            scalar_checks+=1
    assert Fraction(182,121)>Fraction(279,1000)
    return {'status':'PASS_INDEPENDENT_ONE_D_SUPPORT_GATE_REVIEW',
            'receivers':receipts,'shared_K370_support':sorted(union),
            'nonlinear_alphabet_controls':scalar_checks,
            'rank_coefficients_inherited_not_reproved':True,
            'coefficient_file_sha256':sha256(pairpath.read_bytes()).hexdigest(),
            'unrestricted_K_excluded':False}


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--kind',choices=['commuting','support'],required=True);a=ap.parse_args()
    base,layout,routes,orth,pins=load_repo(a.repo)
    result=commuting(layout,routes,orth) if a.kind=='commuting' else support(base,layout,routes,orth)
    result.update({'pins':pins,'proof_sha256':sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),
                   'author_code_imported':False,'new_complete_kappa':False})
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])


if __name__=='__main__': main()
