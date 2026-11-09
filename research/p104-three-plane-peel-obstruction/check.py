#!/usr/bin/env python3
"""Exact source-bound obstruction; no predecessor imports or network access.
python3 -I -B research/p104-three-plane-peel-obstruction/check.py
Use --write-result once to reproduce RESULT.json. All proof tests use exceptions,
including under Python -O. Arithmetic is Fraction throughout the linear replay.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = 'ab5c1c05383a8d3a84995f1a8368e08173e776608d635ff06871651d9e494590'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def add(row, other, scalar):
    for j, value in other.items():
        v = row.get(j, 0) + scalar * value
        if v:
            row[j] = v
        else:
            row.pop(j, None)

def replay(program, public, registers):
    rows = [{i: Q(1)} if i < public else {} for i in range(registers)]
    for e in program:
        op, r = e[:2]
        if op in ('INIT', 'CLEAR'):
            rows[r] = {}
        elif op == 'MOVE':
            pass
        elif op == 'SCALE':
            c = Q(e[2]); rows[r] = {j: c*v for j, v in rows[r].items()}
        elif op in ('ADD', 'COPY'):
            if op == 'COPY':
                rows[r] = {}
            add(rows[r], rows[e[2]], Q(e[3]))
        else:
            raise ValueError('unknown source opcode')
    return rows

def span(basis):
    out = {0}
    for v in basis:
        require(v not in out, 'dependent source frame')
        out |= {v ^ x for x in out}
    return frozenset(out)

def rank(rows):
    basis = {}
    for original in rows:
        row = dict(original)
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = {j: c/scale for j, c in row.items()}
                break
            add(row, basis[pivot], -row[pivot])
    return len(basis)

def submatrix(matrix, ri, ci):
    return [[matrix[i].get(j, Q(0)) for j in ci] for i in ri]

def small_rank(a):
    return rank([{j: c for j, c in enumerate(row) if c} for row in a])

def serialized(a):
    return [[str(x) for x in row] for row in a]

def census(w, core, inverse):
    n = w['public']; frames = [span(f) for f in w['frames']]
    initial = [frames[f] for f in w['initial']]
    final = [frames[f] for f in w['final']]
    zero, full = frozenset([0]), frozenset(range(512))
    main = set(w['live']) | {x+112 for x in w['live']} | set(w['hosted']['X2']) | set(w['hosted']['Y2'])
    moves = defaultdict(list)
    for i, event in enumerate(w['program']):
        if event[0] == 'MOVE':
            moves[event[1]].append((i, event))
    records = []; survivors = []; nx = ny = pair_count = positive = 0
    for q in w['ports']:
        require(q.bit_count() % 2 == 1, 'port is not anisotropic')
        qframe = frozenset([0, q])
        perp = frozenset(x for x in range(512) if (x&q).bit_count() % 2 == 0)
        xs = []; ys = []
        for r in range(n):
            if r in main or initial[r] != zero or final[r] != full or not moves[r]:
                continue
            first, last = moves[r][0], moves[r][-1]
            if frames[first[1][2]] == zero and frames[first[1][3]] == qframe:
                xs.append([r, first[0]])
            if frames[last[1][2]] == perp and frames[last[1][3]] == full:
                ys.append([r, last[0]])
        nx += len(xs); ny += len(ys); pair_count += len(xs)*len(ys)
        allowed_output = {final[j] for j in range(n) if initial[j] == qframe} | {perp}
        allowed_input = {initial[j] for j in range(n) if final[j] == perp} | {qframe}
        x_bad = []; y_bad = []; x_good = []; y_good = []
        for h, cut in xs:
            witness = next(((j, core[j][h]) for j in range(n) if final[j] not in allowed_output and h in core[j]), None)
            if witness:
                x_bad.append({'register': h, 'move': cut, 'forbidden_row': witness[0], 'exact_coefficient': str(witness[1])})
            else:
                x_good.append(h)
        for g, cut in ys:
            witness = next(((j, c) for j, c in sorted(core[g].items()) if initial[j] not in allowed_input), None)
            if witness:
                y_bad.append({'register': g, 'move': cut, 'forbidden_column': witness[0], 'exact_coefficient': str(witness[1])})
            else:
                y_good.append(g)
        q_old = [j for j in range(n) if initial[j] == qframe]
        p_old = [j for j in range(n) if final[j] == perp]
        require(small_rank(submatrix(core, p_old, q_old)) == 1, 'source forward-plane positive control')
        require(small_rank(submatrix(inverse, q_old, p_old)) == 1, 'source reverse-plane positive control')
        positive += 1
        for h in x_good:
            for g in y_good:
                require(h != g, 'same helper on both boundaries')
                qi, po = q_old+[h], p_old+[g]
                f, b = submatrix(core, po, qi), submatrix(inverse, qi, po)
                rf, rb = small_rank(f), small_rank(b)
                require((rf, rb) != (2, 1), 'a third forward plane survives; theorem must stop')
                require((rf, rb) != (1, 2), 'a third reverse plane survives; theorem must stop')
                survivors.append({'q': q, 'h': h, 'g': g, 'q_input_group': qi, 'perp_output_group': po,
                                  'forward_block': serialized(f), 'inverse_block': serialized(b), 'ranks': [rf, rb]})
        records.append({'q': q, 'x_candidates': xs, 'y_candidates': ys,
                        'x_zero_block_witnesses': x_bad, 'y_zero_block_witnesses': y_bad,
                        'x_zero_block_survivors': x_good, 'y_zero_block_survivors': y_good})
    require((nx, ny, pair_count) == (363, 295, 984), 'inventory coverage changed')
    require([(s['q'], s['h'], s['g'], s['ranks']) for s in survivors] == [(268, 793, 1352, [1, 1]), (268, 1202, 1352, [1, 1])], 'residual family changed')
    # The inverse condition is essential: both residuals meet the desired forward
    # block rank of a reverse shear, yet fail its required inverse rank two.
    require(all(s['ranks'][0] == 1 and s['ranks'][1] != 2 for s in survivors), 'inverse-rank negative control')
    return {'ports': len(w['ports']), 'x_candidates': nx, 'y_candidates': ny,
            'candidate_pairs': pair_count, 'zero_block_survivor_pairs': len(survivors),
            'source_two_plane_positive_controls': positive, 'survivors': survivors, 'inventory': records}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--write-result', action='store_true'); opts = ap.parse_args()
    raw = (HERE/'data/word.json.gz').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PIN, 'source byte pin')
    w = json.loads(gzip.decompress(raw)); n = w['public']; nr = n+w['owned_fields']; p = w['program']
    lo = next(i for i, e in enumerate(p) if e[0] == 'MOVE'); hi = max(i for i, e in enumerate(p) if e[0] == 'MOVE')
    frames = [span(b) for b in w['frames']]; zero = frozenset([0]); full = frozenset(range(512))
    require(all(e[0] in ('ADD', 'SCALE') and frames[e[-1]] == zero for e in p[:lo]), 'initial boundary is not all Z')
    require(all(e[0] in ('ADD', 'SCALE') and frames[e[-1]] == full for e in p[hi+1:]), 'final boundary is not all V')
    require(all(e[0] not in ('ADD', 'COPY', 'SCALE') or frames[e[-1]] not in (zero, full) for e in p[lo:hi+1]), 'core uses a peeled endpoint chart')
    current = list(w['initial']) + [None]*w['owned_fields']; owned = set()
    for e in p:
        op, r = e[:2]
        if op == 'MOVE':
            require(current[r] == e[2] and bool(e[4]) == (r in owned), 'source MOVE ownership/frame')
            a, b = frames[e[2]], frames[e[3]]
            require((a < b or b < a) if r in owned else a < b, 'source MOVE nesting')
            current[r] = e[3]
        elif op == 'INIT':
            require(r >= n and r not in owned, 'source INIT'); owned.add(r); current[r] = e[2]
        elif op == 'CLEAR':
            require(r in owned and current[r] == e[2], 'source CLEAR'); owned.remove(r); current[r] = None
        else:
            require(current[r] == e[-1], 'source scalar destination chart')
            if op != 'SCALE':
                require(r != e[2] and current[e[2]] == e[-1], 'source scalar source chart')
    require(not owned and current[:n] == w['final'], 'source final frame calendar')
    target = [{i: Q(1)} for i in range(n)]; inverse_events = []
    for x in w['live']:
        target[x+112][x] = Q(1); inverse_events.append(['ADD', x+112, x, '-1', 0])
    for x, y in zip(w['hosted']['X2'], w['hosted']['Y2']):
        target[x][y] = Q(-1); inverse_events.append(['ADD', x, y, '1', 0])
    endpoint = replay(p, n, nr)
    require(endpoint[:n] == target and all(not r for r in endpoint[n:]), 'source arbitrary-input endpoint')
    core = replay(p[lo:hi+1], n, nr)[:n]
    inverse = replay(p[hi+1:]+inverse_events+p[:lo], n, n)
    # The exact whole-word identity proves this is K^-1: T=Gout K Gin.
    # An additional full rational product checks all public rows independently
    # of the derivation's multiplication-order convention.
    for i, row in enumerate(core):
        product = {}
        for j, c in row.items():
            add(product, inverse[j], c)
        require(product == {i: Q(1)}, 'exact core/inverse product row '+str(i))
    result = census(w, core, inverse)
    result.update({'source_sha256_gzip': PIN, 'source_sha256_json': hashlib.sha256(gzip.decompress(raw)).hexdigest(),
                   'source_events': len(p), 'core_range_inclusive': [lo, hi],
                   'exact_core_inverse_rows': n, 'arithmetic': 'fractions.Fraction; no modular rank argument',
                   'scope': 'one extra independent unit shear at one source port; one helper peeled at each endpoint; unchanged interior scalar word; arbitrary invertible endpoint basis changes within each declared frame group'})
    # Mutated complete word: a doubled nonzero core update must change its map.
    j = next(i for i in range(lo, hi+1) if p[i][0] == 'ADD')
    bad = list(p); e = list(p[j]); e[3] = str(2*Q(e[3])); bad[j] = e
    require(replay(bad, n, nr)[:n] != target, 'changed native gate was not rejected')
    result['negative_controls'] = ['doubled first core ADD changes exact endpoint', 'forward block alone misses both residual inverse obstructions']
    result['binding_checks'] = ['exact source digest', 'coverage counts and residual pair list', 'retained result equality on default replay']
    path = HERE/'RESULT.json'
    if opts.write_result:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(json.loads(path.read_text()) == result, 'retained result differs from exact replay')
    print('PASS_P104_THREE_PLANE_ENDPOINT_PEEL_OBSTRUCTION')
    print('984 helper pairs excluded; 104 source two-plane controls; 1375 exact inverse rows; two exact residual inverse blocks of rank1.')

if __name__ == '__main__':
    main()
