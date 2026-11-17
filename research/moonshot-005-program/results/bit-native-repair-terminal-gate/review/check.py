#!/usr/bin/env python3
"""Independent finite premises for the native rank repair and terminal gate."""
import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

BASE = 'research/moonshot-005-program'
SOURCE = BASE + '/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SOURCE_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PRICE = BASE + '/sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py'
PRICE_SHA = '41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'

def binary_rank(rows):
    pivots = {}
    for value in rows:
        while value:
            p = value.bit_length() - 1
            if p not in pivots:
                pivots[p] = value
                break
            value ^= pivots[p]
    return len(pivots)

def rational_rank(rows):
    a = [list(map(Fraction, row)) for row in rows]
    p = 0
    for j in range(8):
        k = next((k for k in range(p, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[p], a[k] = a[k], a[p]
        scale = a[p][j]
        a[p] = [x / scale for x in a[p]]
        for k in range(p + 1, len(a)):
            scale = a[k][j]
            a[k] = [x - scale * y for x, y in zip(a[k], a[p])]
        p += 1
    return p

def product(a, b):
    out = []
    for row in a:
        v = 0
        for j, other in enumerate(b):
            if row & (1 << j):
                v ^= other
        out.append(v)
    return out

def interval_json(pair):
    return {'lower': str(pair[0]), 'upper': str(pair[1])}

def combine(*terms):
    out = Counter()
    for coefficient, profile in terms:
        for rank, count in profile.items():
            out[rank] += coefficient * count
    return {k: v for k, v in sorted(out.items()) if v}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--author', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    raw = (a.repo / SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    roots = json.loads(raw)['native_roots']
    assert len(roots) == 111
    dot = lambda x, y: sum(u * v for u, v in zip(x, y))
    native = [sum(1 << j for j, s in enumerate(roots) if not dot(r, s)) for r in roots]
    canonical = [row ^ (1 << i) for i, row in enumerate(native)]
    repair_edges = [(0, 1), (1, 0), (2, 3)]
    repair = [0] * 111
    repaired = native[:]
    for i, j in repair_edges:
        assert native[i] & (1 << j)
        repair[i] ^= 1 << j
        repaired[i] ^= 1 << j
    assert [binary_rank(x) for x in (native, canonical, repair, repaired)] == [108, 9, 3, 111]
    advertised = json.loads((a.author / 'output/INVERSE-CERTIFICATE.json').read_text())
    assert list(map(lambda x: int(x, 16), advertised['M_rows_hex'])) == repaired
    inverse = list(map(lambda x: int(x, 16), advertised['inverse_rows_hex']))
    identity = [1 << i for i in range(111)]
    assert product(repaired, inverse) == identity == product(inverse, repaired)
    spans = []
    for i, row in enumerate(repaired):
        selected = []
        for j in range(111):
            if not row & (1 << j):
                continue
            assert dot(roots[i], roots[j]) == 0
            if rational_rank([roots[k] for k in selected] + [roots[j]]) > len(selected):
                selected.append(j)
            if len(selected) == 7:
                break
        assert len(selected) == 7
        spans.append({'receiver': i, 'seven_independent_uncached_roots': selected})
    controls = []
    for i, j in repair_edges:
        altered = repaired[:]
        altered[i] ^= 1 << j
        rank = binary_rank(altered)
        assert rank == 110
        controls.append({'omitted_edge': [i, j], 'rank': rank})
    assert len({j for i, j in repair_edges}) == 3
    # The geometry is reconstructed here; only directed interval arithmetic
    # comes from a separately reviewed frozen implementation.
    price_path = a.repo / PRICE
    assert hashlib.sha256(price_path.read_bytes()).hexdigest() == PRICE_SHA
    spec = importlib.util.spec_from_file_location('reviewed_interval_only', price_path)
    price = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(price)
    q = {1: 780, 6: 3, 7: 108, 8: 9}
    gate = Counter({127: 37, 64: 74, 1: -74})
    for j in range(1, 9):
        gate[1 + 7 * j] += 74
        gate[7 * j] -= 74
    b = tuple(x / 6 for x in price.moment(gate))
    qi = price.moment(q)
    room = (b[0] - qi[1], b[1] - qi[0])
    assert room[0] > 0
    n = {1: 1386, 2: 1253, 3: 62, 4: 47, 5: 9, 6: 104, 7: 10}
    h = {2: 1, 4: 25, 6: 1, 8: 410}
    p2 = combine((36, n), (444, {1: 1}), (444, {7 * j: 1 for j in range(1, 9)}))
    t2 = combine((36, h), (222, {127: 1}), (444, {1 + 7 * j: 1 for j in range(1, 10)}))
    finite = []
    for m in (2, 4, 6):
        paid = combine((m // 2, p2), (-18 * (m - 1), n), (18 * (m - 1), q))
        target = combine((m // 2, t2), (-18 * (m - 1), h))
        gap = price.moment(combine((1, target), (-1, paid)))
        finite.append({'m': m, 'target_minus_paid': interval_json(gap), 'positive': gap[0] > 0})
    assert [item['positive'] for item in finite] == [False, False, True]
    result = {
        'status': 'PASS_INDEPENDENT_NATIVE_REPAIR_AND_TERMINAL_SPAN_PREMISES',
        'source_sha256': SOURCE_SHA,
        'author_proof_sha256': hashlib.sha256((a.author / 'PROOF.md').read_bytes()).hexdigest(),
        'ranks_N_K_R_M': [108, 9, 3, 111],
        'both_inverse_products_identity': True,
        'repair_edges': repair_edges,
        'all111_full_facet_span_witnesses': spans,
        'three_omission_controls': controls,
        'hypothetical_maximum_movement_profile': q,
        'hypothetical_movement': interval_json(qi),
        'hypothetical_limiting_room': interval_json(room),
        'finite_caller_screens': finite,
        'complete_source_constructed': False,
        'scope': 'Exact finite premises plus separately reviewed arbitrary-bank terminal theorem. The favourable arithmetic belongs to an architecture excluded under the stated terminal information contract.',
        'no_new_kappa': True,
    }
    (a.out / 'CERTIFICATE.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'all111_full_facet_span_witnesses'}))

if __name__ == '__main__':
    main()
