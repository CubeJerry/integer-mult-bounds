#!/usr/bin/env python3
"""Reconstruct the frozen feedback's native partition and transport defects.

No source-construction or predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and different pivot choices.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np


def need(value, message):
    if not value:
        raise AssertionError(message)


def xor(values):
    answer = 0
    for value in values:
        answer ^= int(value)
    return answer


def product(x, y):
    result = 0
    while y:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 64:
            x ^= 67
    return result


MUL = np.array([[product(x, y) for y in range(64)] for x in range(64)], dtype=np.uint8)
INV = np.array([0] + [next(y for y in range(1, 64) if MUL[x, y] == 1)
                           for x in range(1, 64)], dtype=np.uint8)


def power(x, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = int(MUL[answer, x])
        x = int(MUL[x, x])
        exponent >>= 1
    return answer


def mm(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    need(left.ndim == right.ndim == 2 and left.shape[1] == right.shape[0], 'matrix dimensions')
    answer = np.zeros((left.shape[0], right.shape[1]), dtype=np.uint8)
    for col in range(left.shape[1]):
        answer ^= MUL[left[:, col, None], right[col, None, :]]
    return answer


def echelon(matrix):
    matrix = np.array(matrix, dtype=np.uint8, copy=True)
    pivots = []
    determinant = 1
    for col in range(matrix.shape[1]):
        row = len(pivots)
        choices = np.flatnonzero(matrix[row:, col])
        if not len(choices):
            continue
        chosen = row + int(choices[0])
        matrix[[row, chosen]] = matrix[[chosen, row]]
        determinant = int(MUL[determinant, matrix[row, col]])
        matrix[row, col:] = MUL[INV[matrix[row, col]], matrix[row, col:]]
        if row + 1 < len(matrix):
            matrix[row + 1:, col:] ^= MUL[matrix[row + 1:, col, None], matrix[row, None, col:]]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots, determinant


def rank(matrix):
    return len(echelon(matrix)[1])


def null(matrix):
    rows, pivots, _ = echelon(matrix)
    free = [j for j in range(rows.shape[1]) if j not in pivots]
    result = np.zeros((rows.shape[1], len(free)), dtype=np.uint8)
    result[free] = np.eye(len(free), dtype=np.uint8)
    for i in range(len(pivots) - 1, -1, -1):
        result[pivots[i]] = mm(rows[i:i + 1, pivots[i] + 1:], result[pivots[i] + 1:])[0]
    need(not np.any(mm(matrix, result)), 'independent nullspace identity')
    return result


def certificate(matrix):
    _, cols, _ = echelon(matrix)
    _, rows, _ = echelon(matrix[:, cols].T)
    minor = matrix[np.ix_(rows, cols)]
    _, pivots, determinant = echelon(minor)
    kernel = null(matrix)
    need(len(pivots) == len(cols) and determinant != 0, 'nonzero maximal minor')
    need(rank(kernel) == matrix.shape[1] - len(cols), 'independent upper-rank certificate')
    return {'shape': list(matrix.shape), 'rank': len(cols), 'minor_rows': rows,
            'minor_columns': cols, 'minor_determinant': determinant,
            'kernel_columns': kernel.tolist(), 'matrix_sha256': hashlib.sha256(matrix.tobytes()).hexdigest()}


def quadratic(x):
    return ((x & (x >> 1)) & 85).bit_count() & 1


def polar(x, y):
    return (x & (((y & 85) << 1) | ((y & 170) >> 1))).bit_count() & 1


def root_coordinates(layout, basis):
    columns = basis['lattice_basis_columns']
    lattice = [[columns[j][i] for j in range(8)] for i in range(8)]
    hyperbolic = basis['hyperbolic_basis_masks']
    reverse = {xor(hyperbolic[j] for j in range(8) if mask >> j & 1): mask for mask in range(256)}
    need(len(reverse) == 256, 'binary lattice coordinate isomorphism')
    roots = []
    for original in layout['root_table']:
        coordinates = [0] * 8
        for i in range(7, -1, -1):
            coordinates[i], remainder = divmod(original[i] - sum(lattice[i][j] * coordinates[j]
                                                               for j in range(i + 1, 8)), lattice[i][i])
            need(remainder == 0, 'exact integral root coordinates')
        roots.append(reverse[sum((x & 1) << i for i, x in enumerate(coordinates))])
    need(len(set(roots)) == 120 and set(roots) == {x for x in range(256) if quadratic(x)},
         'all actual anisotropic root labels')
    return roots


GAPS = (3, 6, 7, 9, 10, 11, 12, 13, 15)


def frozen_feedback(donor):
    matrix = np.zeros((3, 48), dtype=np.uint8)
    for slot in GAPS:
        tag = f'native-polynomial-feedback/{donor}/0/{slot}'
        matrix[:, 3 * slot:3 * slot + 3] = np.frombuffer(
            hashlib.shake_256(tag.encode('ascii')).digest(9), dtype=np.uint8).reshape(3, 3) & 63
    matrix[:, 9:12] = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    matrix[:, 18:21] = np.diag([1, 0, 0]).astype(np.uint8)
    return matrix


def quotient(node, feedback):
    return np.kron(np.array([[power(node, j) for j in range(16)]], dtype=np.uint8),
                   np.eye(len(feedback), dtype=np.uint8)) ^ MUL[power(node, 16) ^ 1, feedback]


def multiply_polynomials(left, right):
    answer = np.zeros(len(left) + len(right) - 1, dtype=np.uint8)
    for i, value in enumerate(left):
        answer[i:i + len(right)] ^= MUL[value, right]
    return answer


def hermite_fibre(off_nodes, width):
    g = np.array([1], dtype=np.uint8)
    for node in sorted(off_nodes):
        g = multiply_polynomials(g, np.array([node, 1], dtype=np.uint8))
    gpower = np.array([1], dtype=np.uint8)
    for _ in range(width):
        gpower = multiply_polynomials(gpower, g)
    result = np.zeros((16 * width, width), dtype=np.uint8)
    for j in range(width):
        result[j:j + len(gpower), j] = gpower
    return result


def transport_equations(targets, relations, twist):
    width = targets[0].shape[1]
    rows = targets[0].shape[0] * relations.shape[1]
    answer = np.zeros((rows, len(targets) * width * width), dtype=np.uint8)
    for i, target in enumerate(targets):
        target = target.copy()
        for _ in range(twist):
            target = MUL[target, target]
        for a in range(width):
            for b in range(width):
                answer[:, i * width * width + a * width + b] = MUL[
                    target[:, a, None], relations[i * width + b, None, :]].reshape(-1)
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = args.repo.resolve()
    paths = json.loads((here / 'SOURCE-PINS.json').read_text())['files']
    for path, expected in paths.items():
        need(hashlib.sha256((repo / path).read_bytes()).hexdigest() == expected, 'frozen source ' + path)
    base = repo / 'research/moonshot-005-program/results'
    layout = json.loads(gzip.decompress((base / 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    basis = json.loads((base / 'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    roots = root_coordinates(layout, basis)
    planes, charts = [set(x) for x in layout['A2']], [set(x) for x in layout['D4']]
    adjacency = [{i for i, y in enumerate(roots) if i != j and not polar(x, y)} for j, x in enumerate(roots)]
    node_data = json.loads((base / 'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes = node_data['H_nodes']
    centre, donors = 263, [0, 61, 62]
    need(planes[centre] == set(donors) and nodes[centre] == 49, 'literal H263 with common node49')
    receivers = [i for i in range(111) if planes[centre] <= adjacency[i]]
    need(len(receivers) == 33 and 80 not in receivers and 10 not in donors, 'identity-target native receivers')
    stars = {j: [h for h, plane in enumerate(planes) if j in plane] for j in donors}
    need(all(len(star) == 28 and len({nodes[h] for h in star}) == 28 for star in stars.values()),
         'literal donor stars have28 distinct shared nodes')
    old_result = json.loads((base / 'bit-coupled-native-polynomial-feedback/author/output/RESULT.json').read_text())
    fibres, zero_fibres, off_nodes, coefficients, hashes = {}, {}, {}, {}, {}
    source_checks = 0
    for donor in donors:
        feedback = frozen_feedback(donor)
        coefficients[donor] = {h: quotient(nodes[h], feedback) for h in stars[donor]}
        hashes[donor] = hashlib.sha256(b''.join(coefficients[donor][h].tobytes() for h in sorted(stars[donor]))).hexdigest()
        need(hashes[donor] == old_result['source_coefficient_sha256'][str(donor)], 'literal frozen source coefficient hash')
        fibres[donor], zero_fibres[donor], off_nodes[donor] = {}, {}, {}
        for receiver in receivers:
            off = [h for h in stars[donor] if h != centre and planes[h] <= adjacency[receiver]]
            need(len(off) == 15, 'actual fifteen off-H observations')
            observation = np.vstack([coefficients[donor][h] for h in off])
            kernel = null(observation)
            need(kernel.shape == (48, 3) and rank(kernel) == 3, 'entire width-three inverse fibre')
            need(rank(mm(coefficients[donor][centre], kernel)) == 3, 'complete source cut is invertible')
            fibres[donor][receiver] = kernel
            zero_fibres[donor][receiver] = null(np.vstack([quotient(nodes[h], np.zeros((3, 48), dtype=np.uint8)) for h in off]))
            off_nodes[donor][receiver] = {nodes[h] for h in off}
            source_checks += 1

    # Authenticate the actual whole-bank fully early cut, independently of the
    # source reconstruction. One source-only component is not a physical word.
    exits, quota = {}, Counter()
    route_bytes = gzip.decompress((base / 'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
    for line in route_bytes.splitlines():
        phase, role, coordinate, plane, d, _, source, _ = json.loads(line)
        if plane == centre:
            need(phase == 'X' and source == role and role in donors, 'genuine fully early source owners')
            quota[role] += 1
            exits.setdefault(d, set()).update((role, coordinate, lane) for lane in range(8))
    need(quota == {0: 30, 61: 30, 62: 30} and len(exits) == 45 and
         set(map(len, exits.values())) == {16}, '720 early fields and45 physical16-field exits')
    need(all(sum(len(slots) for d, slots in exits.items() if charts[d] <= adjacency[i]) == 240
             for i in receivers), '240-field visible native H cut')

    def join_rank(donor, selected, family=fibres):
        return rank(np.hstack([family[donor][i] for i in selected]))

    pair_histogram, triple_histogram, discrepancies = Counter(), Counter(), []
    for selected in itertools.combinations(receivers, 2):
        profile = tuple(join_rank(j, selected) for j in donors)
        need(profile == (6, 6, 6), 'all pair joins agree and have full rank')
        pair_histogram[str(profile)] += 1
    for selected in itertools.combinations(receivers, 3):
        profile = tuple(join_rank(j, selected) for j in donors)
        triple_histogram[str(profile)] += 1
        if len(set(profile)) != 1:
            discrepancies.append({'receivers': list(selected), 'ranks': list(profile)})
    expected = [{'receivers': [52, 73, 98], 'ranks': [9, 8, 8]},
                {'receivers': [53, 75, 96], 'ranks': [9, 8, 9]},
                {'receivers': [54, 74, 98], 'ranks': [9, 8, 9]}]
    need(discrepancies == expected, 'complete census of minimal receiver witnesses')
    union = [52, 53, 54, 73, 74, 75, 96, 98]
    need([join_rank(j, union) for j in donors] == [24, 21, 23], 'three independent frozen rank defects')
    witnesses = {}
    for selected in [row['receivers'] for row in expected] + [union]:
        key = ','.join(map(str, selected))
        witnesses[key] = {j: certificate(np.hstack([fibres[j][i] for i in selected])) for j in donors}

    # Companion examples have equal rank contributions on these witnesses.
    # Consequently they cannot cancel a nonzero number of frozen components,
    # even if a later whole-bank bijection mixes all the components.
    companion_profiles = {}
    for mode, width in [('geometric_tensor', 3), ('Hermite', 3), ('Hermite', 12)]:
        family = zero_fibres if mode == 'geometric_tensor' else {
            j: {i: hermite_fibre(off_nodes[j][i], width) for i in union} for j in donors}
        profile = [join_rank(j, union, family) for j in donors]
        triples = [[join_rank(j, row['receivers'], family) for j in donors] for row in expected]
        need(len(set(profile)) == 1 and all(len(set(row)) == 1 for row in triples), 'balanced companion rank profiles')
        companion_profiles[f'{mode}{width}'] = {'union_ranks': profile, 'triple_ranks': triples}
    need(companion_profiles['geometric_tensor3']['union_ranks'] == [15] * 3 and
         companion_profiles['Hermite3']['union_ranks'] == [24] * 3 and
         companion_profiles['Hermite12']['union_ranks'] == [96] * 3, 'literal companion dimensions')

    # A separate algebraic obstruction is stronger than a mere failed search.
    # It also provides a reusable transport system for future parameter choices.
    selected12 = [84, 85, 86, 87, 92, 93, 94, 95, 96, 97, 98, 99]
    source12 = np.hstack([fibres[0][i] for i in selected12])
    relations12 = null(source12)
    need(source12.shape == (48, 36) and relations12.shape == (36, 6), 'twelve-receiver30-dimensional source core')
    transport_certificates = []
    for twist in range(6):
        equations = transport_equations([fibres[61][i] for i in selected12], relations12, twist)
        need(equations.shape == (288, 108) and rank(equations) == 108, 'six exact zero-transport systems')
        _, rows, _ = echelon(equations.T)
        minor = equations[rows]
        _, pivots, determinant = echelon(minor)
        need(len(pivots) == 108 and determinant != 0, 'nonsingular108-square transport certificate')
        transport_certificates.append({'Frobenius': twist, 'shape': [288, 108], 'rank': 108,
                                       'minor_rows': rows, 'minor_determinant': determinant,
                                       'equation_sha256': hashlib.sha256(equations.tobytes()).hexdigest()})
    same_source = transport_equations([fibres[0][i] for i in selected12], relations12, 0)
    identity = np.tile(np.eye(3, dtype=np.uint8).reshape(-1), 12)[:, None]
    need(not np.any(mm(same_source, identity)) and rank(source12) == 30, 'positive identity transport control')
    malformed = minor.copy()
    malformed[-1] = malformed[-2]
    need(rank(malformed) == 107, 'duplicate-row negative transport certificate')
    for row in expected:
        need(all([join_rank(j, selected) for j in donors] == [6] * 3
                 for selected in itertools.combinations(row['receivers'], 2)), 'deleting any receiver removes triple rank discrepancy')

    result = {'status': 'PASS_FROZEN_FEEDBACK_NATIVE_PARTITION_OBSTRUCTION',
              'baseline': '5953b86befe08da02dbaa5ff6c16111aea8a81d4',
              'no_predecessor_executable_imports': True,
              'field': {'size': 64, 'binary_modulus': 67},
              'centre': centre, 'donors': donors, 'receivers': receivers,
              'literal_source_sha256': hashes, 'native_source_cuts_checked': source_checks,
              'early_fields_at_bank3840': 720, 'visible_cut_fields_at_bank3840': 240,
              'all_receiver_pairs': dict(pair_histogram), 'all_receiver_triples': dict(triple_histogram),
              'minimal_receiver_count_for_join_rank_discrepancy': 3,
              'triple_discrepancies': discrepancies, 'union_receivers': union,
              'union_rank_profile': [24, 21, 23], 'union_rank_gap': 3,
              'balanced_companion_examples': companion_profiles,
              'transport_receivers': selected12, 'transport_source_span': 30,
              'all_six_transport_shapes': [[288, 108]] * 6,
              'all_six_transport_ranks': [108] * 6,
              'duplicate_minor_row_rank': 107,
              'arbitrary_nonlinear_separate_bank_gauges_excluded': True,
              'gauge_scope': 'the frozen diagrams, repetitions, finite extensions and companions with equal listed join-rank contributions',
              'arbitrary_changed_companions_excluded': False,
              'near_minimum_return_excess_bound_claimed': False,
              'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    (args.out / 'JOIN-CERTIFICATES.json').write_text(json.dumps(witnesses, sort_keys=True, indent=2) + '\n')
    (args.out / 'TRANSPORT-MINORS.json').write_text(json.dumps(transport_certificates, sort_keys=True, indent=2) + '\n')
    data = {'fibres': {j: {i: matrix.tolist() for i, matrix in fs.items()} for j, fs in fibres.items()},
            'twelve_receiver_relations': relations12.tolist()}
    (args.out / 'FIBRES.json.gz').write_bytes(gzip.compress(json.dumps(data, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    print(result['status'], source_checks, 528, 5456, result['union_rank_profile'], 6, 108, flush=True)


if __name__ == '__main__':
    main()
