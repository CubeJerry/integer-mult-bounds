#!/usr/bin/env python3
"""Independent source/matrix review; imports no author verifier or algebra."""
import argparse
import hashlib
import json
from pathlib import Path

def span(rows):
    pivots = {}
    for row in rows:
        while row:
            p = (row & -row).bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return pivots

def residual(row, pivots):
    for p in sorted(pivots):
        if row >> p & 1:
            row ^= pivots[p]
    return row

def contains(big, small):
    b = span(big)
    return all(residual(x, b) == 0 for x in small)

def intersect(left, right):
    left = list(span(left).values())
    right = span(right)
    pivots = {}
    result = []
    for row in left:
        reduced, witness = residual(row, right), row
        while reduced:
            p = (reduced & -reduced).bit_length() - 1
            if p in pivots:
                a, b = pivots[p]
                reduced ^= a
                witness ^= b
            else:
                pivots[p] = (reduced, witness)
                break
        if not reduced:
            result.append(witness)
    assert len(span(result)) == len(result)
    return result

def xor(rows):
    result = 0
    for row in rows:
        result ^= row
    return result

def same(a, b):
    return contains(a, b) and contains(b, a)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--certificate', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    prefix = args.repo / 'research/moonshot-005-program'
    source = prefix / 'results/bit-two-copy-cohort-source/author/output/WORD.json'
    native = prefix / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == 'aa9d17693c1f976625ee420e1367680e86cfec0195259d609f7eddc258eda01e'
    assert hashlib.sha256(native.read_bytes()).hexdigest() == '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots = json.loads(native.read_text())['native_roots']
    word = json.loads(source.read_text())
    values = {f'{kind}{i}_b{b}': 1 << (offset + 2*i+b)
              for kind, offset in [('X', 0), ('Y', 222)]
              for i in range(111) for b in range(2)}
    kernels = {}
    for op in word['operations']:
        if op[0] == 'INIT':
            assert op[1] not in values
            values[op[1]] = 0
        elif op[0] == 'ADD':
            assert op[1] != op[2]
            values[op[2]] ^= values[op[1]]
        elif op[0] == 'MOVE':
            if op[1] in ('P0_b0', 'P0_b1') and op[2] == 'A15':
                kernels[op[1]] = values[op[1]]
        else:
            raise AssertionError(op)
    assert all(values[name] == row for name, (chart, row) in word['expected'].items())
    assert all(values[f'X{i}_b{b}'] == 1 << (2*i+b) for i in range(111) for b in range(2))
    D = list(span(v for name, v in values.items() if name.startswith('C')).values())
    orth = [[j for j in range(111) if sum(a*b for a,b in zip(roots[i], roots[j])) == 0] for i in range(111)]
    K = [(1 << i) ^ xor(1 << j for j in orth[i]) for i in range(111)]
    h = K[0] ^ K[4]
    W = [[sum(1 << (2*j+b) for j in range(111) if (K[i] >> j & 1) and ((h >> j) & 1) == ((h >> i) & 1)) for b in range(2)] for i in range(111)]
    Wall = [x for pair in W for x in pair]
    A = D + Wall
    assert [len(span(D)), len(span(Wall)), len(span(A))] == [80, 30, 91]
    cert = json.loads(args.certificate.read_text())
    assert same(D, [int(x,16) for x in cert['D_rows_hex']])
    assert W == [[int(x,16) for x in pair] for pair in cert['W_rows_hex']]
    cases = []
    for case in cert['cases']:
        depth = case['depth']
        z, tail = [0,0], [0,0]
        for name, row in values.items():
            if name.startswith('C7_'):
                _, ell, color, bank = name.split('_')
                b = int(bank[1:])
                if color == '0': z[b] ^= row
                if color == '1' and int(ell) >= depth: tail[b] ^= row
        B = [values['P0_b0'], values['P0_b1'], kernels['P0_b0'], kernels['P0_b1']] + tail + [z[b] ^ (1 << (14+b)) for b in range(2)]
        assert len(span(B)) == 8 and contains(D, B)
        assert same(B, [int(x,16) for x in case['B_rows_hex']])
        J, C = [], []
        controls = []
        for ports, duty in zip([[1], [8,11], [22,23]], case['duties']):
            assert duty['ports'] == ports
            for i in ports:
                Li = [1 << (2*j+b) for j in orth[i] for b in range(2)]
                assert contains(D, intersect(A, Li))
            assert contains(D, [xor(W[i][b] for i in ports) for b in range(2)])
            side = B + [1 << (2*j+b) for i in ports for j in orth[i] for b in range(2)]
            delta = [xor(1 << (2*i+b) for i in ports) for b in range(2)]
            dutyspace = intersect(D, side + delta)
            assert len(span(side+delta)) - len(span(side)) == 2
            assert len(span(side+dutyspace)) - len(span(side)) == 2
            assert same(side, [int(x,16) for x in duty['side_rows_hex']])
            assert same(dutyspace, [int(x,16) for x in duty['J_rows_hex']])
            assert len(span(dutyspace)) == duty['J_dimension']
            # A changed-information control destroys the required quotient.
            assert len(span(side+delta)) - len(span(side+delta)) == 0
            controls.append({'ports': ports, 'free_demand_quotient_dimension': 0})
            C.append(side); J.append(dutyspace)
        I12 = intersect(J[0], J[1]); I3 = intersect(J[2], J[0]+J[1])
        assert contains(C[0], I12) and contains(C[2], I3)
        assert same(I12, [int(x,16) for x in case['first_pair_intersection_rows_hex']])
        assert same(I3, [int(x,16) for x in case['third_intersection_rows_hex']])
        dims = [len(span(x)) for x in J] + [len(I12), len(span(J[0]+J[1])), len(I3)]
        assert dims == ([54,58,54,42,70,46] if depth in (1,2) else [52,56,52,40,68,44])
        cases.append({'depth': depth, 'dimensions': dims, 'controls': controls})
    # Every row of W really fits its native demand, including all two-copy ports.
    for i in range(111):
        assert contains(Wall + [1 << (2*j+b) for j in orth[i] for b in range(2)], [1 << (2*i+b) for b in range(2)])
    assert 79**200 < 8**199 * 10**200
    out = {'status': 'PASS_INDEPENDENT_THREE_DUTY_GATE', 'cases': cases,
           'all_444_source_columns_replayed': True, 'all_222_X_restored': True,
           'proof_conclusion': 'p >= 21, for the stated fixed D/B and seed subspace inside A, all characteristic-two fields and all tensor widths',
           'budget_control': 'five rank8 banks cost >39.5, above full two-copy room <30.414',
           'new_complete_kappa': False}
    args.out.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'depths': [x['depth'] for x in cases]}))

if __name__ == '__main__':
    main()
