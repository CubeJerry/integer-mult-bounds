#!/usr/bin/env python3
"""Independent native geometric/gap15 source port-gate review.

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


def kron(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    return MUL[left[:, None, :, None], right[None, :, None, :]].reshape(
        left.shape[0] * right.shape[0], left.shape[1] * right.shape[1])


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


def u_polynomial(v, centre):
    numerator = np.zeros(17, dtype=np.uint8)
    for degree, coefficient in [(8, v), (16, power(v, 2)), (14, power(v, 4)),
                                (5, power(v, 4)), (1, power(v, 8)),
                                (2, power(v, 16)), (4, power(v, 32))]:
        numerator[degree] ^= coefficient
    numerator[0] = xor(MUL[numerator[d], power(centre, d)] for d in range(1, 17))
    answer = np.zeros(16, dtype=np.uint8)
    answer[15] = numerator[16]
    for d in range(14, -1, -1):
        answer[d] = numerator[d + 1] ^ MUL[centre, answer[d + 1]]
    need(numerator[0] == MUL[centre, answer[0]], 'exact division by z+centre')
    return answer


def root_product(nodes):
    result = np.array([1], dtype=np.uint8)
    for node in sorted(nodes):
        new = np.zeros(len(result) + 1, dtype=np.uint8)
        new[1:] ^= result
        new[:-1] ^= MUL[node, result]
        result = new
    return result


def binary_map(inputs, outputs):
    pairs = dict(zip(inputs, outputs))
    basis, span = [], {0: 0}
    for v in inputs:
        if v not in span:
            basis.append(v)
            span.update({w ^ v: image ^ pairs[v] for w, image in list(span.items())})
    need(len(basis) == 6 and len(span) == len(set(span.values())) == 64,
         'independent full binary parameter isomorphism')
    need(all(span[v] == w for v, w in zip(inputs, outputs)), 'all native parameter images')
    return span, basis


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    here = Path(__file__).resolve().parent
    for path, expected in json.loads((here / 'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo / path).read_bytes()).hexdigest() == expected, 'pinned input ' + path)
    base = repo / 'research/moonshot-005-program/results'
    layout = json.loads(gzip.decompress((base / 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    basis = json.loads((base / 'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    roots = root_coordinates(layout, basis)
    planes, charts = [set(x) for x in layout['A2']], [set(x) for x in layout['D4']]
    adjacency = [{i for i, y in enumerate(roots) if i != j and not polar(x, y)} for j, x in enumerate(roots)]
    data = json.loads((base / 'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes = data['H_nodes']
    parameters = {int(j): {int(i): v for i, v in row.items()} for j, row in data['receiver_parameters'].items()}
    centre, h, donors = 49, 263, [0, 61, 62]
    receivers = [i for i in range(111) if planes[h] <= adjacency[i]]
    need(planes[h] == set(donors) and nodes[h] == centre and len(receivers) == 33 and
         80 not in receivers and 10 not in donors, 'literal native identity-target H263')
    stars = {j: [p for p, plane in enumerate(planes) if j in plane] for j in donors}
    U = np.array([u_polynomial(1 << p, centre) for p in range(6)], dtype=np.uint8).T
    bits = lambda v: np.array([v >> p & 1 for p in range(6)], dtype=np.uint8)[:, None]
    need(rank(U) == 6 and all(np.array_equal(mm(U, bits(v))[:, 0], u_polynomial(v, centre))
                              for v in range(64)), 'literal additive six-dimensional fibre core')
    derivatives = {}
    for i in receivers:
        derivatives[i] = []
        for j in donors:
            v = parameters[j][i]
            off = {nodes[p] for p in stars[j] if p != h and planes[p] <= adjacency[i]}
            need(len(off) == 15, 'actual off-H node set')
            need(np.array_equal(u_polynomial(v, centre), MUL[power(v, 2), root_product(off)]),
                 'closed polynomial identity matches actual fifteen-plane kernel')
            d = power(v, 8) ^ int(MUL[power(centre, 4), power(v, 4)])
            evaluation = np.array([[power(centre, p) for p in range(16)]], dtype=np.uint8)
            need(d != 0 and mm(evaluation, u_polynomial(v, centre)[:, None])[0, 0] == d,
                 'actual nonzero central readout')
            derivatives[i].append(d)
    maps = []
    for donor in donors[1:]:
        inputs = [parameters[0][i] for i in receivers]
        outputs = [parameters[donor][i] for i in receivers]
        mapping, chosen = binary_map(inputs, outputs)
        graph = {v: {w for w in inputs if w != v and v ^ w in inputs} for v in inputs}
        seen, queue = {inputs[0]}, [inputs[0]]
        while queue:
            for other in graph[queue.pop()] - seen:
                seen.add(other)
                queue.append(other)
        need(len(seen) == 33, 'connected additive parameter graph')
        maps.append({'donor': donor, 'basis': chosen, 'images': [mapping[1 << p] for p in range(6)],
                     'graph_vertices': len(seen), 'graph_edges': sum(map(len, graph.values())) // 2})

    shift = np.zeros((16, 16), dtype=np.uint8)
    for i in range(16):
        shift[(i + 1) % 16, i] = 1
    identity = np.eye(16, dtype=np.uint8)
    pencil_certificates = []
    for c in sorted(set(nodes)):
        need(c != 1, 'allowed geometric nodes omit1')
        core = np.array([u_polynomial(1 << p, c) for p in range(6)], dtype=np.uint8).T
        N = shift ^ MUL[c, identity]
        t = int(INV[1 ^ c])
        pencil = mm(identity ^ MUL[t, N], core)
        need(rank(core) == rank(pencil) == 6, 'unique potentially singular pencil remains injective')
        evaluation = np.array([[power(c, p) for p in range(16)]], dtype=np.uint8)
        derivative = np.array([[power(1 << p, 8) ^ MUL[power(c, 4), power(1 << p, 4)]
                                for p in range(6)]], dtype=np.uint8)
        need(np.array_equal(mm(evaluation, core), derivative), 'derivative matrix identity')
        need(not np.any(mm(evaluation, mm(N, core)) ^ MUL[power(c, 16) ^ 1, core[15:16]]),
             'linear matrix-feedback coefficient cancels')
        need(not np.any(mm(N, core)[15]), 'quadratic matrix-feedback coefficient cancels')
        pencil_certificates.append({'node': c, 'exceptional_scalar': t, 'rank_certificate': certificate(pencil)})

    # Force the exceptional eigenvalue and a nontrivial Jordan coupling.
    exceptional = int(INV[1 ^ centre])
    A = MUL[exceptional, np.eye(3, dtype=np.uint8)]
    A[0, 1] = A[1, 2] = 1
    N = shift ^ MUL[centre, identity]
    E = kron(U, np.eye(3, dtype=np.uint8)) ^ kron(mm(N, U), A)
    need(rank(E) == 18, 'nonsemisimple exceptional-eigenvalue matrix pencil')
    evaluation = np.array([[power(centre, p) for p in range(16)]], dtype=np.uint8)
    selector = np.zeros((1, 16), dtype=np.uint8)
    selector[0, 15] = power(centre, 16) ^ 1
    Q = kron(evaluation, np.eye(3, dtype=np.uint8)) ^ kron(selector, A)
    for i in receivers:
        K = mm(E, kron(bits(parameters[0][i]), np.eye(3, dtype=np.uint8)))
        need(np.array_equal(mm(Q, K), MUL[derivatives[i][0], np.eye(3, dtype=np.uint8)]),
             'nonsemisimple matrix source readout')

    exits, quota = {}, Counter()
    routes = gzip.decompress((base / 'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
    for line in routes.splitlines():
        phase, role, coordinate, plane, d, _, source, _ = json.loads(line)
        if plane == h:
            need(phase == 'X' and source == role and role in donors, 'actual original early owner')
            quota[role] += 1
            exits.setdefault(d, set()).update((role, coordinate, lane) for lane in range(8))
    need(quota == {0: 30, 61: 30, 62: 30} and len(exits) == 45 and
         set(map(len, exits.values())) == {16}, 'full physical H263 owner cut')
    need(all(sum(len(slots) for d, slots in exits.items() if charts[d] <= adjacency[i]) == 240
             for i in receivers), 'every actual receiver has exactly240 visible fields')
    need(108 in exits and planes[h] <= charts[108] and all(charts[108] <= adjacency[i] for i in (5, 7)),
         'D108 is an actual shared exit')
    ratios = {i: int(MUL[derivatives[i][0], INV[derivatives[i][1]]]) for i in receivers}
    need((ratios[5], ratios[7]) == (26, 49), 'distinct literal field readout ratios')
    mixing = np.array([[1, 3, 2], [0, 1, 4], [0, 0, 1]], dtype=np.uint8)
    row = lambda i: np.hstack([MUL[INV[derivatives[i][0]], np.eye(3, dtype=np.uint8)],
                               MUL[INV[derivatives[i][1]], mixing]])
    need(rank(np.vstack([row(5), row(7)])) == 6, 'zero common two-donor row space')
    need(ratios[4] == ratios[7] and rank(np.vstack([row(4), row(7)])) == 3,
         'equal-ratio positive control')
    need(not charts[108] <= adjacency[0], 'wrong receiver port control')
    damaged = pencil.copy()
    damaged[:, -1] = damaged[:, -2]
    need(rank(damaged) == 5, 'duplicate core column invalidates universal-pencil certificate')

    result = {'status': 'PASS_INDEPENDENT_GEOMETRIC_GAP15_PORT_GATE', 'no_author_code_imports': True,
              'H': h, 'donors': donors, 'native_receivers': receivers,
              'actual_polynomial_fibres_checked': 99, 'exceptional_pencils': 28,
              'parameter_maps': maps, 'nonsemisimple_control_core_rank': 18,
              'actual_early_owners': 720, 'actual_visible_cut_fields': 240,
              'shared_exit': 108, 'witness_receivers': [5, 7], 'ratios': [26, 49],
              'two_donor_union_rank': 6, 'equal_ratio_control_rank': 3,
              'duplicate_core_column_rank': 5,
              'arbitrary_GF64_linear_whole_bank_gauges': True,
              'arbitrary_binary_linear_gauges': False,
              'all_positive_admissible_widths_and_finite_extensions': True,
              'nonlinear_downstream_allowed': True, 'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    (args.out / 'PENCIL-CERTIFICATES.json').write_text(json.dumps(pencil_certificates, sort_keys=True, indent=2) + '\n')
    print(result['status'], 99, 28, 33, 108, 26, 49, flush=True)


if __name__ == '__main__':
    main()
