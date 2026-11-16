#!/usr/bin/env python3
"""Independent exact coefficient/geometry audit of the frozen leaf-capacity cut.

No author checker is imported. This verifies the finite hypotheses of the
separate dimension/counting proof, rather than inferring a theorem from tests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

PORTS = (7, 11, 12, 41, 28, 44, 19, 27)
DEMANDS = ((18,), (26,), (53, 57, 85), (24,), (45,), (29, 62, 63), (8, 9, 36, 37), (42,))


def binary_basis(rows):
    out = {}
    for row in rows:
        while row:
            j = row.bit_length()-1
            if j in out:
                row ^= out[j]
            else:
                out[j] = row
                break
    return list(out.values())


def coordinate_rows(mask):
    return [1 << j for j in range(111) if mask >> j & 1]


def echelon(rows):
    a = [[Fraction(z) for z in r] for r in rows]
    n = 0
    pivots = []
    for j in range(8):
        k = next((k for k in range(n, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[n], a[k] = a[k], a[n]
        q = a[n][j]
        a[n] = [x/q for x in a[n]]
        for k in range(len(a)):
            if k != n:
                q = a[k][j]
                a[k] = [x-q*y for x, y in zip(a[k], a[n])]
        pivots.append(j)
        n += 1
    return a[:n], pivots


def chart_basis(rec):
    rows, pivots = echelon(rec['rows'])
    if rec['kind'] == 'span':
        return rows
    assert rec['kind'] == 'ann'
    out = []
    for j in set(range(8))-set(pivots):
        v = [Fraction(0)]*8
        v[j] = 1
        for i, p in enumerate(pivots):
            v[p] = -rows[i][j]
        out.append(v)
    return out


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--word', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    raw = a.word.read_bytes()
    w = json.loads(raw)
    src = (a.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(src).hexdigest() == w['source_sha256']
    roots = json.loads(src)['native_roots']
    cb = {n: chart_basis(rec) for n, rec in w['charts'].items()}
    mask111 = (1 << 111)-1
    loc = {f'X{i}': f'L{i}' for i in range(111)} | {f'Y{i}': 'zero' for i in range(111)}
    val = {f'X{i}': 1 << i for i in range(111)} | {f'Y{i}': 1 << (111+i) for i in range(111)}
    hist = [(n, loc[n], v) for n, v in val.items()]
    for op, n, *q in w['operations']:
        if op == 'INIT':
            val[n], loc[n] = 0, q[0]
        elif op == 'ADD':
            val[q[0]] ^= val[n]
            n = q[0]
        elif op == 'MOVE':
            loc[n] = q[0]
        elif op == 'CLEAR':
            del val[n], loc[n]
            continue
        else:
            raise AssertionError(op)
        hist.append((n, loc[n], val[n]))
    assert set(val) == {f'{p}{i}' for p in 'XY' for i in range(111)}
    for i in range(111):
        assert val[f'X{i}'] == 1 << i
        assert val[f'Y{i}'] == (1 << (111+i)) ^ ((1 << i) if i in w['targets'] else 0)
    h0 = sum(1 << i for i, h in enumerate(w['singular_h']) if h == 0)
    extra = sum(1 << i for i in w['history_extra_query_roles'])
    h1 = (mask111 ^ h0) & ~extra
    g0 = int(w['extra_source_delivery']['first_retention_hex'], 16)
    g1 = int(w['higher_source_delivery']['first_retention_hex'], 16)
    bank_rows = (coordinate_rows(h0)+[g1], coordinate_rows(h0), coordinate_rows(h0),
                 coordinate_rows(h1), coordinate_rows(h1), coordinate_rows(h1),
                 coordinate_rows(extra)+[g0], coordinate_rows(h0)+[g1])
    witnesses = []
    floors = []
    for k, J in enumerate(DEMANDS):
        assert set(J).isdisjoint(w['targets'])
        jm = sum(1 << j for j in J)
        assert all(dot(roots[i], roots[j]) != 0 for i in J for j in J)
        side_rows = []
        visible_counts = {}
        for i in J:
            assert dot(roots[i], roots[PORTS[k]]) == 0
            for p, port in enumerate(PORTS):
                if p != k and dot(roots[i], roots[port]) == 0:
                    side_rows.extend(row & jm for row in bank_rows[p])
            visible = [x for x in hist if all(dot(roots[i], b) == 0 for b in cb[x[1]])]
            assert all(not (v & jm) for _, _, v in visible)
            visible_counts[str(i)] = len(visible)
        side_basis = binary_basis(side_rows)
        floor = len(J)-len(side_basis)
        floors.append(floor)
        witnesses.append({'port': PORTS[k], 'demand_tuple': list(J),
                          'visible_history_counts': visible_counts,
                          'zero_projected_old_history': True,
                          'generously_shared_side_basis_hex': [hex(r) for r in side_basis],
                          'side_rank': len(side_basis), 'capacity_floor': floor})
    assert floors == [1, 1, 3, 1, 1, 2, 3, 1], floors
    out = {'status': 'PASS_ROOT_INDEPENDENT_LEAF_CAPACITY_HYPOTHESES',
           'word_sha256': hashlib.sha256(raw).hexdigest(),
           'native_sha256': hashlib.sha256(src).hexdigest(),
           'historical_states': len(hist), 'all_222_final_columns': True,
           'capacity_floor': floors, 'total_floor': sum(floors),
           'witnesses': witnesses,
           'scope': 'Exact finite source hypotheses for the separate all-field linear and finite-field fixed-length nonlinear theorem. Full chronology and movement proof are independently reviewed separately.'}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=2)+'\n')
    print(out['status'], out['total_floor'], out['historical_states'])


if __name__ == '__main__':
    main()
