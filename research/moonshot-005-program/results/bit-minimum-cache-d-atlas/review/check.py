#!/usr/bin/env python3
"""Direct GF(64) audit of the D-chart certificates. Requires NumPy, no author imports."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np


LAYOUT = 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
ROUTES = 'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
LAYOUT_HASH = '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
ROUTES_HASH = '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
CERT_HASH = '9e2fbdb0a1ec95926903b65acea48b7428f1a2bf0c8233271ac655d76e630e15'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_pin(path, digest):
    data = gzip.decompress(path.read_bytes())
    require(hashlib.sha256(data).hexdigest() == digest, f'payload hash: {path}')
    return data


def field():
    # Enumerate powers of the residue z. Its complete 63-cycle verifies this
    # representation is a field and z is primitive.
    powers = []
    z = 1
    for _ in range(63):
        powers.append(z)
        z *= 2
        if z >= 64:
            z ^= 67
    require(set(powers) == set(range(1, 64)) and z == 1, 'primitive orbit')
    table = np.zeros((64, 64), dtype=np.uint8)
    inverse = np.zeros(64, dtype=np.uint8)
    for i, a in enumerate(powers):
        inverse[a] = powers[-i % 63]
        for j, b in enumerate(powers):
            table[a, b] = powers[(i + j) % 63]
    return table, inverse


PRODUCT, INVERSE = field()
BASIS = np.array([1, 2, 4, 8, 16, 32], dtype=np.uint8)
BIT_COST = [sum(int(x).bit_count() for x in PRODUCT[a, BASIS]) for a in range(64)]


def determinant_nonzero(matrices):
    """Independent Gaussian elimination; no symbolic Cauchy determinant identity."""
    a = np.array(matrices, dtype=np.uint8, copy=True)
    count, height, width = a.shape
    require(height == width, 'square batch')
    batch = np.arange(count)
    live = np.ones(count, dtype=bool)
    for col in range(width):
        avail = a[:, col:, col] != 0
        live &= np.any(avail, axis=1)
        pivot = col + np.argmax(avail, axis=1)
        a[batch, col], a[batch, pivot] = a[batch, pivot].copy(), a[batch, col].copy()
        row = PRODUCT[INVERSE[a[:, col, col]][:, None], a[:, col, col:]]
        a[:, col+1:, col:] ^= PRODUCT[a[:, col+1:, col, None], row[:, None, :]]
    return live


def rank(matrix):
    a = np.array(matrix, dtype=np.uint8, copy=True)
    height, width = a.shape
    h = 0
    for col in range(width):
        if h == height:
            break
        choices = np.flatnonzero(a[h:, col])
        if choices.size == 0:
            continue
        i = h + choices[0]
        a[[h, i]] = a[[i, h]]
        unit = PRODUCT[INVERSE[a[h, col]], a[h]]
        a[h+1:] ^= PRODUCT[a[h+1:, col, None], unit[None, :]]
        h += 1
    return h


def cauchy(h, w):
    rows = np.arange(h, dtype=np.uint8)
    columns = np.arange(32, 32+w, dtype=np.uint8)
    return INVERSE[rows[:, None] ^ columns[None, :]]


def chart_matrix(m, n, weights):
    r = len(weights)
    early = cauchy(m+r, m)
    late = cauchy(n, n+r)
    source = early[m:]
    delivery = PRODUCT[late[:, n:], np.array(weights, dtype=np.uint8)[None, :]]
    cross = np.zeros((n, m), dtype=np.uint8)
    for s in range(r):
        cross ^= PRODUCT[delivery[:, s, None], source[None, s, :]]
    physical = np.block([[early[:m], np.zeros((m, n), dtype=np.uint8)], [cross, late[:, :n]]])
    return physical, source, delivery


def binary_rows(matrix):
    result = []
    for row in matrix:
        block = [0]*6
        for field_col, value in enumerate(row):
            for t, product in enumerate(PRODUCT[value, BASIS]):
                for u in range(6):
                    if int(product) & (1 << u):
                        block[u] |= 1 << (6*field_col+t)
        result.extend(block)
    return result


@lru_cache(maxsize=None)
def check_pure(n):
    field = cauchy(n, n)
    require(rank(field) == n, 'pure phase field determinant')
    image = binary_rows(field)
    m = 6*n
    identity = [1 << i for i in range(m)]
    reduction = image[:]
    word = []

    def xor(dst, src):
        require(dst != src, 'illegal in-place ADD')
        reduction[dst] ^= reduction[src]
        word.append((dst, src))

    for col in range(m):
        mask = 1 << col
        if not (reduction[col] & mask):
            source = next(p for p in range(col+1, m) if reduction[p] & mask)
            xor(col, source)
            xor(source, col)
            xor(col, source)
        for dest in range(m):
            if dest != col and reduction[dest] & mask:
                xor(dest, col)
    require(reduction == identity, 'pure reduction identity')
    run = identity[:]
    for dst, src in reversed(word):
        run[dst] ^= run[src]
    require(run == image, 'literal forward bits')
    for dst, src in word:
        run[dst] ^= run[src]
    require(run == identity, 'literal inverse bits')
    return len(word)


def routes_by_d(space, geometry):
    routes = [json.loads(line) for line in read_pin(space/ROUTES, ROUTES_HASH).splitlines()]
    roots, planes, d4 = (geometry[name] for name in ('root_table', 'A2', 'D4'))
    vectors = np.array(roots, dtype=np.int64)
    perpendicular = (vectors @ vectors.T) == 0
    duals = []
    for d in d4:
        duals.append(np.flatnonzero(np.all(perpendicular[d, :], axis=0)).tolist())
    require(all(x == d4[y] for x,y in zip(duals,geometry['dual_D4'])), 'root-derived D duals')
    charts = defaultdict(list)
    seen = set()
    for phase, role, col, h, d, k, right_line, terminal in routes:
        require(phase in ('X','Y') and 0 <= col < 480 and 0 <= role < 111, 'owner range')
        identity = (phase, role, col)
        require(identity not in seen, 'duplicate physical owner')
        seen.add(identity)
        if d is None:
            continue
        if h is not None:
            require(set(planes[h]) <= set(d4[d]), 'incoming H does not meet D')
        if k is not None:
            require(set(planes[k]) <= set(duals[d]), 'outgoing K does not meet D-perp')
        charts[d].append((identity, h, k))
    require(len(seen) == 2*111*480 and len(charts) == 3150, 'entire atlas')
    return charts, duals


def memberships(charts, d, planes, donors, receivers):
    # Tuple sorting puts original X before original Y, then native role and
    # original column in both phases, independently of route-file order.
    physical = sorted(charts[d])
    m = sum(owner[0] == 'X' for owner, _, _ in physical)
    input_slots = [[t for t, (_, h, _) in enumerate(physical) if h is not None and j in planes[h]]
                   for j in donors]
    output_slots = [[t for t, (_, _, k) in enumerate(physical) if k is not None and i in planes[k]]
                    for i in receivers]
    require(all(len(x)==len(set(x))==8 for x in input_slots+output_slots), 'real eight-slot tuples')
    return m, len(physical)-m, np.array(input_slots), np.array(output_slots)


def submatrices(word, outputs, inputs):
    return word[outputs[:,None,:,None], inputs[None,:,None,:]].reshape(-1,8,8)


def faults(d, m, n, weights, dins, outs, deltas):
    r = len(weights)
    require(r > 0 and max(deltas.flatten()) == r, 'witness-chart deficit')
    matrix, _, _ = chart_matrix(m,n,weights)
    i, j = np.argwhere(deltas == r)[0]
    witnessed = matrix[np.ix_(outs[i], dins[j])]
    disabled, _, _ = chart_matrix(m,n,weights[:-1]+[0])
    failed = disabled[np.ix_(outs[i], dins[j])]
    require(rank(witnessed) == 8 and rank(failed) == 7 and rank(disabled[m:,:m]) == r-1,
            'missing one actual cross-phase direction')
    rew, _, _ = chart_matrix(m,n,[1]*r)
    bad = np.flatnonzero(~determinant_nonzero(submatrices(rew,outs,dins)))
    require(rank(rew[m:,:m]) == r and len(bad) > 0, 'nonzero weights can fail pair rank')
    swapped = matrix.copy()
    swapped[[0,m]] = swapped[[m,0]]
    require(rank(swapped)==m+n and np.any(swapped[0,m:]), 'cross-phase order mutation')
    tampered = None
    for p in range(m):
        for q in range(p):
            swapped = matrix.copy()
            swapped[[p,q]] = swapped[[q,p]]
            miss = np.flatnonzero(~determinant_nonzero(submatrices(swapped,outs,dins)))
            if len(miss):
                require(rank(swapped[:m,:m])==m and not np.any(swapped[:m,m:]),
                        'same-phase label control')
                tampered = [int(p),int(q),int(len(miss))]
                break
        if tampered:
            break
    require(tampered is not None, 'actual early owner reassignment broke an audited cut')
    return {'chart': d, 'maximal_deficit': r, 'rank_after_dropping_one_cache': rank(failed),
            'all_weights_one_bad_cuts_with_full_cross_rank': len(bad),
            'late_before_early_detected_with_full_total_rank': True,
            'same_phase_owner_swap_and_bad_cuts': tampered}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--charts', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    base = args.repo/'research/moonshot-005-program/results'
    geometry = json.loads(read_pin(base/LAYOUT, LAYOUT_HASH))
    weights = json.loads(read_pin(args.charts, CERT_HASH))
    charts, duals = routes_by_d(base, geometry)
    require(len(weights)==len(charts) and [w[0] for w in weights]==list(range(3150)), 'certificate coverage')
    charges, ranks, differences = Counter(), Counter(), Counter()
    controls = None
    for d, supplied_m, supplied_n, w in weights:
        native_d = [j for j in geometry['D4'][d] if j < 111]
        native_r = [i for i in duals[d] if i < 111]
        m,n,dins,outs = memberships(charts,d,geometry['A2'],native_d,native_r)
        deficits = (dins < m).sum(axis=1)[None,:] - (outs < m).sum(axis=1)[:,None]
        require((m,n) == (supplied_m,supplied_n) and min(deficits.flatten())>=0, 'chart phase dimensions')
        r = int(max(deficits.flatten()))
        require(r==len(w) and all(isinstance(z,int) and 0<z<64 for z in w), 'charged cache width')
        matrix, capture, delivery = chart_matrix(m,n,w)
        require(rank(matrix[m:,:m])==r and not np.any(matrix[:m,m:]), 'realized width and causality')
        require(np.all(determinant_nonzero(submatrices(matrix,outs,dins))), f'actual native minor at D{d}')
        require(rank(matrix)==m+n, 'full chart inverse')
        counts = np.bincount(deficits.flatten())
        differences.update({k:int(nc) for k,nc in enumerate(counts)})
        ranks[r] += 1
        charges['pure_forward_ADD'] += check_pure(m)+check_pure(n)
        charges['pure_inverse_ADD'] += check_pure(m)+check_pure(n)
        charges['snapshot_write_ADD'] += sum(BIT_COST[int(q)] for q in capture.flat)
        charges['snapshot_read_ADD'] += sum(BIT_COST[int(q)] for q in delivery.flat)
        charges['INIT'] += 6*r
        charges['dirty_CLEAR'] += 6*r
        if d==0:
            controls = faults(d,m,n,w,dins,outs,deficits)
    charges['total_ADD'] = sum(v for k,v in charges.items() if k.endswith('_ADD'))
    report = {'status': 'PASS_ALL_DIRECT_GF64_D_RANKS', 'method': 'primitive-element field table and direct Gaussian elimination on original owner cuts',
              'charts': len(charts), 'passed_8_by_8_minors': sum(differences.values()),
              'cache_rank_histogram': dict(sorted(ranks.items())), 'deficit_histogram': dict(sorted(differences.items())),
              'base_cache_fields': sum(k*v for k,v in ranks.items()),
              'base_costs': dict(charges), 'bank3840_costs': {k:8*v for k,v in charges.items()},
              'pure_and_full_matrix_ranks_checked': {'charts':3150, 'pure_shape_word_classes': check_pure.cache_info().currsize},
              'controls':controls,'layout_payload':LAYOUT_HASH, 'routes_payload':ROUTES_HASH, 'charts_payload':CERT_HASH,
              'scope':'formal native D cuts, local rank and paid linear chart normalization only; no prescribed endpoint or new kappa'}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__ == '__main__':
    main()
