"""Quadratic noncover certificates strengthen native-source first-exit counts."""
from pathlib import Path
from collections import Counter
from math import gcd, lcm
import argparse
import hashlib
import itertools
import json
import sympy as sp
from build_quartet_compression_source import SOURCE, SHA, CHECK, HELPER, module
from build_four_plane_correction import replay_general
from review_half_sum_gate import independent_rows
from check_raw_cache_reactivation import quotient_basis, residual

PARENT_SHA = '4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'


def binary_dual(rows, target):
    b = quotient_basis(rows); r = residual(b, target); assert r
    pivot = (r & -r).bit_length()-1
    d = sum(((residual(b, 1 << j) >> pivot) & 1) << j for j in range(111))
    assert (d & target).bit_count() % 2 and all(not (d & x).bit_count() % 2 for x in rows)
    return d


def independent_indices_mod(rows, prime=1009):
    pivots = {}; selected = []
    for i, row in enumerate(rows):
        row = [int(x) % prime for x in row]
        for pivot in sorted(pivots):
            v = row[pivot]
            if v: row = [(x-v*y) % prime for x, y in zip(row, pivots[pivot])]
        if any(row):
            pivot = next(j for j, x in enumerate(row) if x)
            inv = pow(row[pivot], -1, prime)
            pivots[pivot] = [x*inv % prime for x in row]
            selected.append(i)
    return selected


def primitive_integer_row(row):
    den = lcm(*(int(x.q) for x in row)); out = [int(x*den) for x in row]
    div = gcd(*out); out = [x//div for x in out]
    if next(x for x in out if x) < 0: out = [-x for x in out]
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--word', type=Path, default=Path(__file__).resolve().parent/'ground-retention-known8/WORD.json')
    ap.add_argument('--out', type=Path, required=True); a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
    geo = module(a.repo/CHECK, 'quadratic_first_exit_geometry'); h = module(a.repo/HELPER, 'quadratic_first_exit_helper')
    rb = (a.repo/SOURCE).read_bytes(); assert hashlib.sha256(rb).hexdigest() == SHA
    R = json.loads(rb)['native_roots']; wb = a.word.read_bytes(); assert hashlib.sha256(wb).hexdigest() == PARENT_SHA
    w = json.loads(wb); charts, values, places, stats = replay_general(w, R, geo)
    xmask = (1 << 111)-1
    N = [{j for j, s in enumerate(R) if sum(x*y for x, y in zip(r, s)) == 0} for r in R]
    K = [(1 << i) ^ sum(1 << j for j in N[i]) for i in range(111)]
    bank = independent_rows(K+[1 << j for j in range(8)]+[values[f'Y{i}'] & xmask for i in range(111)])
    assert len(bank) == 29
    native_lines = {charts[f'L{i}']: i for i in range(111)}
    native_fields = {}; other_fields = []
    for name, v in values.items():
        j = native_lines.get(charts[places[name]])
        if j is None: other_fields.append(name)
        else:
            assert v & xmask in [0, 1 << j]
            native_fields.setdefault(j, []).append(name)
    assert set(native_fields) == set(range(111))
    observations = {i: bank+[values[name] & xmask for name in other_fields
                             if geo.sub(charts[places[name]], charts[f'F{i}'])] for i in range(111)}
    demands = {j: [] for j in range(111)}
    for i in range(8, 111):
        assert residual(quotient_basis(observations[i]+[1 << k for k in N[i]]), 1 << i) == 0
        for j in N[i]:
            if residual(quotient_basis(observations[i]+[1 << k for k in N[i] if k != j]), 1 << i):
                demands[j].append(i)
    pairs = list(itertools.combinations_with_replacement(range(7), 2))
    rows = []; dual_count = 0
    for j in range(8, 111):
        D = demands[j]; assert len(geo.basis(tuple(tuple(R[i]) for i in D))) == 7
        deleted = next(k for k, x in enumerate(R[j]) if x); coords = [k for k in range(8) if k != deleted]
        quadratic_rows = [[R[i][coords[a]]*R[i][coords[b]] for a, b in pairs] for i in D]
        selected_quad = independent_indices_mod(quadratic_rows)
        qrank = len(selected_quad); poly = None; matrix_rank = None
        if qrank == 27:
            selected = [D[k] for k in selected_quad]
            M = sp.Matrix([quadratic_rows[k] for k in selected_quad]); kernel = M.nullspace()
            assert M.rank() == 27 and len(kernel) == 1
            poly = primitive_integer_row(kernel[0]); matrix = sp.zeros(7)
            assert all(sum(x*y for x, y in zip(row, poly)) == 0 for row in quadratic_rows)
            for (a0, b0), coefficient in zip(pairs, poly):
                matrix[a0, b0] = matrix[b0, a0] = 2*coefficient if a0 == b0 else coefficient
            matrix_rank = matrix.rank(); assert matrix_rank == 6
            minimum = 3
        else:
            selected = [D[k] for k in independent_indices_mod([R[i] for i in D])]
            assert len(selected) == 7; minimum = 2
        witnesses = []
        for i in selected:
            obs = observations[i]+[1 << k for k in N[i] if k != j]
            d = binary_dual(obs, 1 << i); assert d >> j & 1
            witnesses.append({'receiver': i, 'dual_hex': hex(d)})
        dual_count += len(witnesses)
        public = [name for name in native_fields[j] if name.startswith(('X', 'Y'))]
        assert public in [[], [f'X{j}']]
        rows.append({'source_role': j, 'all_forced_receivers': D, 'normal_rank': 7,
                     'deleted_normal_coordinate': deleted, 'remaining_normal_coordinates': coords,
                     'quadratic_evaluation_rank': qrank, 'primitive_quadratic_kernel': poly,
                     'symmetric_twice_quadratic_matrix_rank': matrix_rank,
                     'minimum_native_departures': minimum, 'current_native_public_carriers': public,
                     'duals': witnesses})
    assert Counter(r['minimum_native_departures'] for r in rows) == {3: 71, 2: 32}
    assert dual_count == 71*27+32*7 == 2141
    total = sum(r['minimum_native_departures'] for r in rows)
    active = sum(len(r['current_native_public_carriers']) for r in rows)
    ground = [name for name in values if name.startswith(('X', 'Y')) and not charts[places[name]]]
    assert total == 277 and active == 71 and len(ground) == 95
    assert all(bool(r['current_native_public_carriers']) == (r['minimum_native_departures'] == 3) for r in rows)
    owned = total-active-len(ground); assert owned == 111
    for row in rows:
        j = row['source_role']
        for z in row['duals']:
            i = z['receiver']; d = int(z['dual_hex'], 16)
            assert d >> i & 1 and d >> j & 1
            assert all((d & x).bit_count() % 2 == 0 for x in observations[i])
            assert all(not (d >> k & 1) for k in N[i] if k != j)
    suffix_moves = [op for op in w['operations'][w['carrier_interface_before_operation']:] if op[0] == 'MOVE']
    assert len(suffix_moves) == 222 and len({op[1] for op in suffix_moves}) == 222
    assert all(op[2] == ('Hub' if op[1].startswith('X') else 'F'+op[1][1:]) for op in suffix_moves)
    moment = h.moment(stats['movement_profile']); mandatory = Counter(stats['movement_profile']); mandatory[1] += owned
    lower = h.moment(mandatory); gate = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9): gate[1+7*j] = gate.get(1+7*j, 0)+74; gate[7*j] = gate.get(7*j, 0)-74
    ceiling = tuple(x/6 for x in h.moment(gate)); excess = (lower[0]-ceiling[1], lower[1]-ceiling[0])
    assert excess[0] > 37
    artificial = [[int(a == i) for a in range(7)] for i in range(7)]
    assert sp.Matrix(artificial).rank() == 7
    reducible = [int(a == 0 and b == 1) for a, b in pairs]
    assert all(sum(v[a]*v[b]*c for (a, b), c in zip(pairs, reducible)) == 0 for v in artificial)
    result = {'status': 'PASS_QUADRATIC_FIRST_EXIT_BANK_EXCLUSION', 'word_sha256': PARENT_SHA,
              'native_sha256': SHA, 'cut': w['carrier_interface_before_operation'], 'live_fields': len(values),
              'all_original_columns': 222, 'bank': 'C+all8_axis_units+actual_old_sign_query_span', 'bank_rank': 29,
              'quadratic_monomial_order': [list(p) for p in pairs], 'source_rows': rows,
              'verified_binary_duals': dual_count, 'departure_histogram': {2: 32, 3: 71},
              'native_departures': total, 'native_public_departure_allowance': active,
              'ground_public_departure_allowance': len(ground), 'minimum_future_owned_ascents': owned,
              'Q0_profile': stats['movement_profile'], 'Q0': h.record(moment),
              'mandatory_profile': dict(sorted(mandatory.items())), 'mandatory_moment': h.record(lower),
              'excess_above_limiting_allowance': h.record(excess),
              'controls': {'rank7_linear_span_alone_does_not_exclude_two_hyperplanes': True,
                           'all_raw_units_in_bank_remove_forcing': all(residual(quotient_basis([1 << j for j in range(111)]), 1 << i) == 0 for i in range(111))},
              'scope': 'Exact95-ground-Y cut; monotone public routes; arbitrary paid nested owned routes; linear processing over characteristic2 fields with any block width; every future descending complete X row stays in the declared rank29 bank. New descending directions are outside this theorem.',
              'new_complete_kappa': False}
    h.save(a.out/'CERTIFICATE.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'source_rows'}, indent=2))


if __name__ == '__main__': main()
