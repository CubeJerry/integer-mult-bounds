#!/usr/bin/env python3
"""Independent literal review of the separately paid three-copy F8 source.

No constructor or author replay is imported. The only imported dependency is
C's frozen rational chart and rational-power arithmetic from S020.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

BASE = 'research/moonshot-005-program'
NATIVE = BASE + '/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
PARENT = BASE + '/sessions/2026-11-17-S020/checkpoint5-evidence/A/full-half-reservoir/WORD.json'
ARITH = BASE + '/sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py'
PINS = {
    'native': '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
    'parent': '6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980',
    'arithmetic': '41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
    'word': '9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6',
}
A, B = [14, 17, 19, 20], [96, 99, 101, 102]


def need(ok, label):
    if not ok:
        raise ValueError(label)


def field_product(a, b):
    # Polynomial multiplication and division by X^3+X+1; independent of A.
    polynomial = 0
    for j in range(3):
        if b & (1 << j):
            polynomial ^= a << j
    for degree in (4, 3):
        if polynomial & (1 << degree):
            polynomial ^= 0b1011 << (degree - 3)
    return polynomial


def column(copy, kind, role):
    return 222 * copy + (111 if kind == 'Y' else 0) + role


def name(copy, kind, role):
    return f'C{copy}__{kind}{role}'


def replay(word, charts, geometry, expected):
    values = {name(c, k, i): 1 << column(c, k, i)
              for c in range(3) for k in ('X', 'Y') for i in range(111)}
    places = {name(c, k, i): f'L{i}' if k == 'X' else 'zero'
              for c in range(3) for k in ('X', 'Y') for i in range(111)}
    xs = {name(c, 'X', i) for c in range(3) for i in range(111)}
    ymask = sum(1 << column(c, 'Y', i) for c in range(3) for i in range(111))
    owners, born = set(), set()
    counts, moves, descents = Counter(), Counter(), Counter()
    peak = dirty = 0
    cut = None
    for index, (opcode, source, *arguments) in enumerate(word['operations']):
        if index == word['carrier_interface_before_operation']:
            cut = values.copy(), places.copy(), owners.copy()
        counts[opcode] += 1
        if opcode == 'INIT':
            need(source not in values and source not in born, 'fresh owner')
            need(arguments[0] in charts, 'real birth chart')
            owners.add(source); born.add(source)
            values[source] = 0; places[source] = arguments[0]
        elif opcode == 'ADD':
            target = arguments[0]
            need(source != target and source in values and target in values, 'live ADD')
            need(charts[places[source]] == charts[places[target]], 'actual cochart ADD')
            values[target] ^= values[source]
            if target in xs:
                need(not values[target] & ymask, 'no baseline in an original X')
        elif opcode == 'MOVE':
            need(source in values and arguments[0] in charts, 'live real MOVE')
            before, after = charts[places[source]], charts[arguments[0]]
            gap = len(after) - len(before)
            if source in owners:
                need(gap < 0 and geometry.contained(after, before), 'strict owned descent')
                descents[-gap] += 1
            else:
                need(gap > 0 and geometry.contained(before, after), 'strict public ascent')
            moves[abs(gap)] += 1; places[source] = arguments[0]
        elif opcode == 'CLEAR':
            need(source in owners, 'owned retirement')
            dirty += bool(values[source]); owners.remove(source)
            del values[source], places[source]
        else:
            raise ValueError('unknown primitive')
        peak = max(peak, len(owners))
    need(cut is not None and not owners and len(values) == 666, 'closed endpoints')
    for c in range(3):
        for i in range(111):
            x, y = name(c, 'X', i), name(c, 'Y', i)
            need(values[x] == 1 << column(c, 'X', i) and places[x] == 'Hub', 'raw X endpoint')
            need(values[y] == expected[y] and places[y] == f'F{i}', 'arbitrary Y endpoint')
    return cut, {'counts': dict(counts), 'movement_profile': dict(sorted(moves.items())),
                 'owned_descent_profile': dict(sorted(descents.items())),
                 'peak_owned': peak, 'dirty_CLEAR': dirty}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--word', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    paths = {'native': args.repo / NATIVE, 'parent': args.repo / PARENT,
             'arithmetic': args.repo / ARITH, 'word': args.word}
    for key, path in paths.items():
        need(sha256(path.read_bytes()).hexdigest() == PINS[key], key + ' pin')
    spec = importlib.util.spec_from_file_location('separate_rational_chart_arithmetic', paths['arithmetic'])
    geometry = importlib.util.module_from_spec(spec); spec.loader.exec_module(geometry)
    roots = json.loads(paths['native'].read_bytes())['native_roots']
    parent = json.loads(paths['parent'].read_bytes())
    word = json.loads(paths['word'].read_bytes())
    charts = {key: geometry.chart(value) for key, value in word['charts'].items()}
    for i, r in enumerate(roots):
        need(charts[f'L{i}'] == geometry.basis((tuple(r),)), 'native line')
        need(charts[f'F{i}'] == geometry.kernel((tuple(r),)), 'actual final facet')
    native = [sum(1 << j for j, s in enumerate(roots) if sum(a * b for a, b in zip(r, s)) == 0)
              for r in roots]
    expected = {name(c, 'Y', i): (1 << column(c, 'Y', i)) ^
                ((1 << i if i < 8 else native[i] & 255) << (222 * c))
                for c in range(3) for i in range(111)}
    inverse_lambda = next(q for q in range(1, 8) if field_product(2, q) == 1)
    for group, other, scalar in ((A, B, 2), (B, A, inverse_lambda)):
        for j, role in enumerate(group):
            coefficients = {i: 1 for i in group if i != role}
            coefficients[other[(j - 1) % 4]] = 1
            coefficients[other[(j + 1) % 4]] = scalar
            for i, coefficient in coefficients.items():
                need(native[role] >> i & 1, 'every added field term is geometrically native')
                for c in range(3):
                    for d in range(3):
                        if field_product(coefficient, 1 << d) >> c & 1:
                            expected[name(c, 'Y', role)] ^= 1 << column(d, 'X', i)
    cut, stats = replay(word, charts, geometry, expected)
    values, places, owners = cut
    need(word['carrier_interface_before_operation'] == 6119, 'actual cut index')
    need(len(values) == 1218 and len(owners) == 552, 'complete current inventory')
    need(stats['counts'] == {'INIT': 552, 'ADD': 4412, 'MOVE': 1488, 'CLEAR': 552}, 'complete invoice')
    need(stats['movement_profile'] == {1: 489, 2: 357, 4: 309, 7: 333}, 'movement invoice')
    need(stats['owned_descent_profile'] == {1: 108}, 'no added owner movement')
    need(stats['peak_owned'] == stats['dirty_CLEAR'] == 552, 'every owned lifetime charged')
    for c in range(3):
        for i in range(111):
            need(values[name(c, 'X', i)] == 1 << column(c, 'X', i), 'all current X raw')
            need(places[name(c, 'X', i)] == 'Hub', 'all current X Hub')
            need(values[name(c, 'Y', i)] == expected[name(c, 'Y', i)], 'full current Y map')
            h = charts[places[name(c, 'Y', i)]]
            need(len(h) == (6 if i in A + B else 0), 'actual current Y chart rank')
            need(geometry.contained(h, charts[f'F{i}']), 'Y chart inside own facet')

    # Reconstruct every inherited field by an independent symbolic prefix trace.
    pv = {f'X{i}': 1 << i for i in range(111)} | {f'Y{i}': 1 << (111 + i) for i in range(111)}
    pp = {f'X{i}': f'L{i}' for i in range(111)} | {f'Y{i}': 'zero' for i in range(111)}
    for opcode, source, *q in parent['operations'][:parent['carrier_interface_before_operation']]:
        if opcode == 'INIT': pv[source] = 0; pp[source] = q[0]
        elif opcode == 'ADD': pv[q[0]] ^= pv[source]
        elif opcode == 'MOVE': pp[source] = q[0]
        elif opcode == 'CLEAR': del pv[source], pp[source]
        else: raise ValueError('parent primitive')
    need(len(pv) == 406, 'parent cut cardinality')
    targets = {f'Y{i}' for i in A + B}
    for c in range(3):
        for n in pv:
            if n not in targets:
                key = f'C{c}__{n}'
                need(values[key] == pv[n] << (222 * c), 'preserved parent field value')
                need(charts[places[key]] == charts[pp[n]], 'preserved parent field chart')

    # Each local word acts on SIX independently paid records, not one bit lane.
    compiler = word['construction']['local_ADD_programs']
    matrices = word['construction']['local_F8_matrices']
    local_controls = 0
    for matrix, program in zip(matrices, compiler):
        expected_matrix = [sum(((field_product(matrix[i // 3][j // 3], 1 << (j % 3)) >> (i % 3)) & 1) << j
                               for j in range(6)) for i in range(6)]
        row = [1 << i for i in range(6)]
        for source, target in program: row[target] ^= row[source]
        need(row == expected_matrix, 'six-record compiler exact matrix')
        for source, target in reversed(program): row[target] ^= row[source]
        need(row == [1 << i for i in range(6)], 'literal inverse')
        for omitted in range(len(program)):
            row = [1 << i for i in range(6)]
            for j, (source, target) in enumerate(program):
                if j != omitted: row[target] ^= row[source]
            need(row != expected_matrix, 'single local ADD omission detected')
            local_controls += 1

    controls = []
    for semantic in ('ground_inverse_ADD', 'native_seed_read', 'forward_pair_compiler_ADD',
                     'actual_three_copy_rendezvous', 'parent_cross_half_paid_unit_descent',
                     'parent_canonical_actual_Hub_gather'):
        index = word['semantic_operation_indices'][semantic][0]
        mutant = dict(word); mutant['operations'] = word['operations'][:index] + word['operations'][index + 1:]
        mutant['carrier_interface_before_operation'] = word['carrier_interface_before_operation'] - 1
        try:
            changed, _ = replay(mutant, charts, geometry, expected)
            need(changed == cut, 'entire current-field map preserved')
        except (ValueError, KeyError):
            controls.append(semantic)
        else:
            raise ValueError('accepted omission ' + semantic)
    normalized = {r: Fraction(n, 3) for r, n in stats['movement_profile'].items()}
    need(all(n.denominator == 1 for n in normalized.values()), 'integral normalized movement counts')
    moment = geometry.moment(normalized)
    gate = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        gate[1 + 7 * j] = gate.get(1 + 7 * j, 0) + 74
        gate[7 * j] = gate.get(7 * j, 0) - 74
    ceiling = tuple(v / 6 for v in geometry.moment(gate))
    room = ceiling[0] - moment[1], ceiling[1] - moment[0]
    result = {'status': 'PASS_INDEPENDENT_666_COLUMN_THREE_COPY_F8_SOURCE',
              'pins': PINS, 'all_original_columns': 666, 'current_fields': 1218,
              'stats': stats, 'all_24_target_Y_baselines_restored': True,
              'all_parent_fields_preserved_outside_24_target_Ys': True,
              'local_compiler_ADD_lengths': list(map(len, compiler)),
              'all_local_ADD_omission_controls': local_controls,
              'whole_source_omission_controls': controls,
              'normalized_moment_interval': list(map(str, moment)),
              'normalized_limiting_room_interval': list(map(str, room)),
              'new_complete_kappa': False,
              'scope': 'Literal three-copy partial source; all record movements and primitives paid. '
                       'Normalized margin is necessary only; no complete supplier or general batching admission.'}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'CERTIFICATE.json').write_text(json.dumps(result, indent=2) + '\n')
    (args.out / 'INDEPENDENT-CUT.json').write_text(json.dumps([
        {'name': n, 'chart': places[n], 'rank': len(charts[places[n]]), 'row_hex': hex(v)}
        for n, v in sorted(values.items())], indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'fields': len(values),
                      'local_controls': local_controls, 'source_controls': len(controls)}))


if __name__ == '__main__':
    main()
