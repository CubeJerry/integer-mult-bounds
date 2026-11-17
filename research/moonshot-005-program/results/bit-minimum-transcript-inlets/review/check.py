#!/usr/bin/env python3
"""Independent integer-lattice, ownership, cyclic-basis and tariff checks."""
import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import cache
from pathlib import Path

P = Path('research/moonshot-005-program')
ROOTS = P / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
CODE = P / 'results/bit-induced95-equality-rigidity/author/FULL-SUPPORT-CERTIFICATE.json'
PRICES = P / 'results/bit-low-exterior-formation-gate/author/output/RESULT.json'
SOURCES = [
    ('sessions/2026-11-17-S020/checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json', 'a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc'),
    ('results/bit-two-copy-field-compiler/author/output/WORD.json', '9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550'),
    ('results/bit-three-copy-field-compiler/author/output/WORD.json', '9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6')]
T = {14, 17, 19, 20, 96, 99, 101, 102}
U = sorted(set(range(8, 111)) - T)


def need(value, label):
    if not value:
        raise ValueError(label)


def read(path, digest):
    data = path.read_bytes()
    need(hashlib.sha256(data).hexdigest() == digest, f'wrong source {path}')
    return json.loads(data)


def gcd_reduce(row):
    common = math.gcd(*row)
    return tuple(x // common for x in row) if common else tuple(row)


@cache
def integer_basis(rows):
    basis = {}
    for row in rows:
        v = gcd_reduce(row)
        for j, p in sorted(basis.items()):
            if v[j]:
                v = gcd_reduce([p[j]*x-v[j]*y for x,y in zip(v,p)])
        if any(v):
            k = next(j for j,x in enumerate(v) if x)
            basis[k] = v
    return tuple(v for _,v in sorted(basis.items()))


@cache
def chart_info(kind, rows, roots):
    basis = integer_basis(rows)
    in_span = {i for i,v in enumerate(roots) if len(integer_basis((*basis,v))) == len(basis)}
    perpendicular = {i for i,v in enumerate(roots) if all(sum(x*y for x,y in zip(v,p)) == 0 for p in basis)}
    if kind == 'span':
        dimension, contained, normals = len(basis), in_span, perpendicular
    else:
        need(kind == 'ann', 'unknown chart')
        dimension, contained, normals = 8-len(basis), perpendicular, in_span
    return dimension, sum(1 << i for i in contained), normals


def audit_source(repo, b, roots, entry):
    path, pin = entry
    word = read(repo/P/path, pin)
    cut = word['carrier_interface_before_operation']
    charts = {key:chart_info(v['kind'], tuple(map(tuple,v['rows'])), roots) for key,v in word['charts'].items()}
    live = {}
    def public(c, kind, i):
        return (f'C{c}__' if b > 1 else '') + kind + str(i)
    for c in range(b):
        for i in range(111):
            live[public(c,'X',i)] = (f'L{i}', 1 << (222*c+i))
            live[public(c,'Y',i)] = ('zero', 1 << (222*c+111+i))
    originals = set(live)
    for op, field, *rest in word['operations'][:cut]:
        if op == 'INIT':
            need(field not in live, 'initialization')
            live[field] = (rest[0],0)
        elif op == 'MOVE':
            live[field] = (rest[0],live[field][1])
        elif op == 'ADD':
            key = rest[0]
            need(charts[live[key][0]] == charts[live[field][0]], 'summands')
            live[key] = (live[key][0],live[field][1] ^ live[key][1])
        else:
            need(op == 'CLEAR','unknown operation')
            del live[field]
    mask = sum(1<<i for i in U)
    sensitive = Counter()
    for loc,bits in live.values():
        rank, native, normals = charts[loc]
        for c in range(b):
            support = (bits >> (222*c)) & mask
            need(support & ~native == 0, 'locality at source cut')
            if support and rank <= 5:
                need(set(U).intersection(normals), 'exterior holds low input')
                sensitive[rank] += 1
    for c in range(b):
        for i in range(111):
            need(charts[live[public(c,'X',i)][0]][0] == 8, 'Hub endpoints')
            rank,_,normals = charts[live[public(c,'Y',i)][0]]
            need(i in normals, 'public Y outside its monotone closure')
            if i in T:
                need(rank == 6, 'private rank')
            if i < 8:
                need(rank == 0, 'public axis')
    invoices = defaultdict(list)
    for op,field,*rest in word['operations'][cut:]:
        if op != 'CLEAR':
            need(op == 'MOVE' and field in originals, 'suffix move is prepaid public')
            invoices[field].append(rest[0])
    for c in range(b):
        for i in range(8):
            need(invoices[public(c,'Y',i)] == [f'F{i}'], 'axis paid direct jump')
    need(len(live) == [410,812,1218][b-1], 'source inventory')
    return {'copies':b,'cut':cut,'live_fields':len(live),'columns':222*b,
            'sensitive_low_fields_by_copy_rank':dict(sorted(sensitive.items())),'single_prepaid_axes':8*b}


def rank2(rows):
    pivots = {}
    for v in rows:
        while v:
            j = v.bit_length()-1
            if j not in pivots:
                pivots[j] = v
                break
            v ^= pivots[j]
    return len(pivots)


def bases(repo):
    code = read(repo/CODE, '012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963')['canonical_vectors']
    order = json.loads(Path(__file__).with_name('CYCLIC-BASES.json').read_bytes())
    need(sorted(order) == U,'native permutation')
    vec = {i:sum(bit<<j for j,bit in enumerate(code[str(i)])) for i in order}
    windows = [(order*2)[s:s+9] for s in range(95)]
    need(all(rank2(vec[i] for i in window) == 9 for window in windows), 'cyclic information bases')
    need(set(Counter(i for w in windows for i in w).values()) == {9}, 'uniform incidences')
    need(rank2(vec[i] for i in (windows[0][:-1]+[windows[0][0]])) == 8,'duplicate control')
    return {'bases':95,'slots_per_basis':9,'multiplicity_of_each_role':9,'duplicate_role_control_rank':8}


def price_bounds(g):
    scale = 10**24
    left, right = 0, 9*scale
    target = scale**200 * g**199
    while right-left > 1:
        middle = (left+right)//2
        if middle**200 <= target:
            left = middle
        else:
            right = middle
    return F(left,scale), F(right,scale)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    roots = tuple(map(tuple, read(args.repo/ROOTS,'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e')['native_roots']))
    sources = [audit_source(args.repo,b,roots,entry) for b,entry in enumerate(SOURCES,1)]
    independent_bases = bases(args.repo)
    certified = read(args.repo/PRICES,'befef29e616a3adebe070251a87c6f85c94a81bf687db2dceafdbbf067017145')['sources']
    gamma = F(95,9)
    beta = F(9651,10000)
    layer = {1:F(1), 2:F(24589,25000), 3:F(1), 4:F(95,108), 5:F(95,108)}
    edge_checks = [(s,d,sum(w for r,w in layer.items() if d<=r<s)) for s in range(1,9) for d in range(s)]
    need(all(w**200 <= (s-d)**199 for s,d,w in edge_checks),'positive descending edges')
    remaining = [sum(w for r,w in layer.items() if r>=s) for s in range(6)]
    g = [price_bounds(i) for i in range(9)]
    # The independent exact GF(257) real-flat census supplies these capacities.
    u,axis = [0,1,3,6,12],[0,1,3,6,11]
    witnesses = []
    min_slack = None
    for s in range(1,6):
        for a in range(s):
            need((u[a]*remaining[s]/gamma)**200 <= (s-a)**199,'owned ascending inlet')
            demand = axis[a]*remaining[s]/gamma
            actual = g[a][0]+g[s-a][0]+g[7-s][0]-g[7][1]
            margin = beta+actual-demand
            need(margin>=0,'public split-cover premium')
            min_slack = margin if min_slack is None else min(margin,min_slack)
            if demand>beta:
                witnesses.append([a,s,str(demand)])
    need([3,4,'1'] in witnesses,'dropping the public split must fail')
    bound = 9*sum(layer.values())+8*(1-beta)
    surplus = []
    for source in certified:
        _,hi = map(F,source['normalized_room']['rational'])
        need(bound>hi,'source buys more than available room')
        surplus.append(str(bound-hi))
    out = {'source_cut_replays':sources,'cyclic_basis_certificate':independent_bases,
           'descending_pairs':len(edge_checks),'positive_inlet_pairs':15,'lower_bound':str(bound),
           'excess_over_each_room_upper_endpoint':surplus,'minimum_public_split_slack_lower_bound':str(min_slack),
           'failing_if_the_split_premium_is_erased':witnesses}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS all three physical cuts, 95 cyclic bases, all 36 descending and 15 split-inlet prices')


if __name__ == '__main__':
    main()
