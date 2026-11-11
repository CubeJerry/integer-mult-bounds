#!/usr/bin/env python3
"""Independent reverse-source verification of fourteen return quotient rows."""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def add(row, key, value):
    z = row.get(key, F(0)) + value
    if z:
        row[key] = z
    else:
        row.pop(key, None)

def reverse(program, cut, role):
    dual = {role: F(1)}
    for e in reversed(program[:cut]):
        op, dest = e[:2]
        a = dual.get(dest, F(0))
        if op == 'ADD':
            if a:
                add(dual, e[2], a * F(e[3]))
        elif op == 'SCALE':
            if a:
                dual.pop(dest)
                add(dual, dest, a * F(e[2]))
        elif op == 'COPY':
            dual.pop(dest, None)
            if a:
                add(dual, e[2], a * F(e[3]))
        elif op in ('INIT', 'CLEAR'):
            dual.pop(dest, None)
        else:
            need(op == 'MOVE', 'unknown source operator')
    return dual

def rank_basis(rows):
    basis = {}; selected = []; pivots = []
    for i, original in enumerate(rows):
        row = dict(original)
        while row:
            k = max(row)
            if k not in basis:
                lead = row[k]
                basis[k] = {j: a / lead for j, a in row.items()}
                selected.append(i); pivots.append(k)
                break
            lead = row[k]
            for j, a in basis[k].items():
                add(row, j, -lead * a)
    return len(basis), selected, pivots

def determinant(a):
    a = [list(x) for x in a]; d = F(1); n = len(a)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]; d = -d
        v = a[j][j]; d *= v
        for i in range(j + 1, n):
            q = a[i][j] / v
            for k in range(j + 1, n):
                a[i][k] -= q * a[j][k]
            a[i][j] = F(0)
    return d

def run(source, current, historical):
    raw = source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'source pin')
    w = json.loads(gzip.decompress(raw))
    mains = set(w['live']) | {i + 112 for i in w['live']} | set(w['hosted']['X2']) | set(w['hosted']['Y2'])
    entry = {i for i in mains if not w['frames'][w['initial'][i]]}
    need(len(mains) == 400 and len(entry) == 200, 'independent input partition')
    c = json.loads(current.read_text())['witnesses']; h = json.loads(historical.read_text())
    requests = sorted([(x['before_event'], 'current') for x in c] + [(x['event'], 'historical') for x in h])
    need(len(requests) == len({x[0] for x in requests}) == 14, 'distinct source events')
    rows = []; records = []
    for event, kind in requests:
        e = w['program'][event]
        need(e[0] == 'MOVE' and e[1] >= w['public'] and e[4] is True, 'owned return')
        full = reverse(w['program'], event, e[1])
        need(all(i < w['public'] for i in full), 'no uninitialized owned input')
        row = {i: a for i, a in full.items() if i in mains}
        out = {i: a for i, a in row.items() if i not in entry}
        rows.append(out)
        records.append({'event': event, 'kind': kind, 'role': e[1], 'destination': e[3], 'full_q_row': {str(i): str(a) for i, a in sorted(row.items())}, 'nonentry_support': len(out), 'entry_support': len(row) - len(out)})
    rank, selected, pivots = rank_basis(rows)
    need(rank == 10, 'fourteen-return quotient rank')
    minor = [[rows[i].get(j, F(0)) for j in pivots] for i in selected]
    det = determinant(minor); need(det != 0, 'independent rational rank minor')
    historical_rows = [rows[i] for i, r in enumerate(records) if r['kind'] == 'historical']
    hr, _, _ = rank_basis(historical_rows)
    need(hr == 4, 'historical rank four')
    hist_union = set().union(*(set(x) for x in historical_rows))
    need(len(hist_union) == 101, 'distributed historical input union')
    need(len({w['initial'][i] for i in hist_union}) == 101, 'distinct initial charts')
    need(all(len(x) == 52 for x in historical_rows), 'historical support52')
    pure = [r['event'] for r, row in zip(records, rows) if not row]
    need(pure == [33272, 33281], 'exact entry-only returns')
    altered = [list(x) for x in minor]; altered[-1] = [F(0) for _ in pivots]
    need(determinant(altered) == 0, 'rank-certificate deletion control')
    canonical = (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()
    receipt = {'status': 'PASS_INDEPENDENT_ADJOINT_QUOTIENT', 'source_sha256': PIN, 'requests': 14, 'quotient_rank': rank, 'historical_quotient_rank': hr, 'historical_nonentry_union': len(hist_union), 'entry_only_events': pure, 'minor_events': [records[i]['event'] for i in selected], 'minor_q_coordinates': pivots, 'minor_determinant': str(det), 'rows_sha256': hashlib.sha256(canonical).hexdigest(), 'negative_control': 'Deleting the last minor row destroys the nonzero determinant.', 'method': 'Independent reverse adjoints for each source cut; maximum-pivot rational elimination and a separate determinant check. No author forward-replay implementation imported.', 'scope': 'Exact source rows and abstract initial-chart quotient only; no physical arrival or paid-cost conclusion follows from rank10 alone.'}
    return receipt, records

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for key in ('source', 'current', 'historical', 'output', 'rows'):
        p.add_argument('--' + key, type=Path, required=True)
    a = p.parse_args(); receipt, rows = run(a.source, a.current, a.historical)
    a.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    a.rows.write_text(json.dumps(rows, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))
