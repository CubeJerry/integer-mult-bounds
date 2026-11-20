#!/usr/bin/env python3
"""Independent literal-matrix protected two-H source review.

No source-construction or predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and last available pivot rows.
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
        chosen = row + int(choices[-1])
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


def inverse(A):
    n = len(A)
    R, pivots, _ = echelon(np.hstack((A, np.eye(n, dtype=np.uint8))))
    need(pivots == list(range(n)), 'invertible square matrix')
    for i in range(n - 1, -1, -1):
        R[:i, i:] ^= MUL[R[:i, i, None], R[i, None, i:]]
    answer = R[:, n:]
    need(np.array_equal(mm(A, answer), np.eye(n, dtype=np.uint8)), 'inverse residual')
    return answer


def q(x):
    return power(x, 9) ^ power(x, 18) ^ power(x, 36)


def field_polar(x, y):
    return q(x ^ y) ^ q(x) ^ q(y)


def witt(space, form):
    space, answer = set(space), []
    while len(space) > 1:
        b = lambda x, y: form(x ^ y) ^ form(x) ^ form(y)
        zeros = sorted(x for x in space if x and not form(x))
        if zeros:
            first = zeros[0]
            second = next(x for x in zeros if b(first, x))
        else:
            first = min(space - {0})
            second = min(space - {0, first})
        answer += [first, second]
        space = {x for x in space if not b(x, first) and not b(x, second)}
    return answer


def binary_span(values):
    span = {0}
    for value in values:
        span |= {x ^ value for x in list(span)}
    return span


def read_json(path):
    raw = path.read_bytes()
    if path.suffix == '.gz':
        raw = gzip.decompress(raw)
    return json.loads(raw), raw


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    repo = args.repo.resolve()
    here = Path(__file__).resolve().parent
    pins = json.loads((here / 'SOURCE-PINS.json').read_text())['files']
    for name, digest in pins.items():
        need(hashlib.sha256((repo / name).read_bytes()).hexdigest() == digest, 'pin ' + name)
    base = repo / 'research/moonshot-005-program/results'
    package = base / 'bit-shared-h-s031-construction'
    coeff, coefficient_raw = read_json(package / 'moving-fibres/output/COEFFICIENTS.json.gz')
    recorded_fibres, fibre_raw = read_json(package / 'moving-fibres/output/FIBRES.json.gz')
    layout, _ = read_json(base / 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
    basis, _ = read_json(base / 'bit-clifford-one-evaluation-gate/author/BASIS.json')
    roots = root_coordinates(layout, basis)
    planes = [set(x) for x in layout['A2']]
    charts = [set(x) for x in layout['D4']]
    adjacency = [{i for i, y in enumerate(roots) if i != j and not polar(x, y)}
                 for j, x in enumerate(roots)]
    need(all(len(x) == 63 for x in adjacency), 'all geometric adjacency degrees')
    selected, _ = read_json(base / 'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')
    selected = set(selected['selected_D'])
    maps = {int(j): {int(h): np.array(M, dtype=np.uint8) for h, M in rows.items()}
            for j, rows in coeff['maps'].items()}
    nodes = {int(j): {int(h): int(a) for h, a in rows.items()}
             for j, rows in coeff['base_nodes'].items()}
    need(set(maps) == set(nodes) == {0, 45, 61, 62, 100}, 'five literal sources')
    stars = {j: [h for h, P in enumerate(planes) if j in P] for j in maps}
    Q = {a for a in range(64) if not q(a)}
    blocks = {frozenset(a for a in Q if field_polar(v, a) == (1 ^ q(v))): v for v in range(1, 64)}
    need(len(Q) == 28 and len(blocks) == 63 and all(len(B) == 16 for B in blocks),
         'literal geometric evaluation design')
    eye = np.eye(3, dtype=np.uint8)
    evaluation = lambda a: kron(np.array([[power(a, d) for d in range(16)]], dtype=np.uint8), eye)
    visible = {(j, i): [h for h in stars[j] if planes[h] <= adjacency[i]]
               for j in maps for i in adjacency[j]}
    old_maps = {j: {h: evaluation(nodes[j][h]) for h in stars[j]} for j in maps}
    source_rows, source_certificates = [], []
    expected_edits = {0: [116, 263], 45: [642], 61: [263, 642], 62: [263, 643], 100: [642]}
    for j in sorted(maps):
        need(set(maps[j]) == set(nodes[j]) == set(stars[j]) and len(stars[j]) == 28,
             'every actual source-plane coefficient')
        need(set(nodes[j].values()) == Q, 'complete geometric node assignment')
        need(all(M.shape == (3, 48) and np.all(M < 64) for M in maps[j].values()), 'literal quotient dimensions')
        edits = [h for h in stars[j] if not np.array_equal(maps[j][h], old_maps[j][h])]
        need(edits == expected_edits[j], 'exact limited edit count')
        seen = set()
        for i in sorted(adjacency[j]):
            hs = visible[j, i]
            need(len(hs) == 16, 'actual sixteen-plane source cut')
            block = frozenset(nodes[j][h] for h in hs)
            need(block in blocks, 'geometric incidence, not only 28 distinct labels')
            seen.add(blocks[block])
            A = np.vstack([maps[j][h] for h in hs])
            _, pivots, determinant = echelon(A)
            need(len(pivots) == 48 and determinant, 'full literal source view')
            source_certificates.append({'donor': j, 'receiver': i, 'planes': hs,
                                        'parameter': blocks[block], 'determinant': determinant})
        need(seen == set(range(1, 64)), 'all 63 geometric block labels exactly once')
        source_rows.append({'donor': j, 'geometric_cuts': 63,
                            'native_cuts': len(adjacency[j] & set(range(111))),
                            'edited_planes': edits, 'uniform_propagation_upper': 42 if len(edits) == 2 else 30})

    # Rebuild whole inverse fibres and the physical provider from literal data.
    H_rows, fibre_certificates = [], {}
    kernels = {}
    for h in [263, 642]:
        donors = sorted(planes[h])
        receivers = [i for i in range(120) if planes[h] <= adjacency[i]]
        ports = [d for d in sorted(selected) if planes[h] <= charts[d]]
        word = np.array(coeff['Hwords'][str(h)], dtype=np.uint8)
        need(len(donors) == 3 and set(donors) <= set(maps) and 10 not in donors and 80 not in receivers,
             'literal identity-target chart')
        need(len(ports) == 9 and len(receivers) == 36 and word.shape == (9, 9) and rank(word) == 9,
             'actual nine marked ports and invertible H word')
        moved = []
        fibre_certificates[str(h)] = {}
        for i in receivers:
            K = []
            for j in donors:
                off = [p for p in visible[j, i] if p != h]
                A = np.vstack([maps[j][p] for p in off])
                kernel = null(A)
                need(A.shape == (45, 48) and kernel.shape == (48, 3), 'whole off-H fibre')
                kernels[j, h, i] = kernel
                K.append(kernel)
            need(all(rank(np.hstack((K[0], k))) == 3 for k in K[1:]), 'equal whole donor fibres')
            positions = [t for t, d in enumerate(ports) if charts[d] <= adjacency[i]]
            need(len(positions) == 3, 'three actual receiver-visible ports')
            readouts = [mm(word[np.ix_(positions, range(3 * s, 3 * s + 3))], mm(maps[j][h], K[0]))
                        for s, j in enumerate(donors)]
            need(rank(readouts[0]) == 3 and all(np.array_equal(readouts[0], R) for R in readouts[1:]),
                 'common invertible readout on the full kernel')
            old = null(np.vstack([old_maps[donors[0]][p] for p in visible[donors[0], i] if p != h]))
            changed = rank(np.hstack((old, K[0]))) > 3
            if changed:
                moved.append(i)
            recorded = recorded_fibres[str(h)][str(i)]
            RK = np.array(recorded['kernel'], dtype=np.uint8)
            RR = np.array(recorded['readout'], dtype=np.uint8)
            need(RK.shape == (48, 3) and rank(RK) == rank(np.hstack((RK, K[0]))) == 3,
                 'provided fibre certificate equals the independently computed kernel')
            need(all(np.array_equal(mm(word[np.ix_(positions, range(3 * s, 3 * s + 3))], mm(maps[j][h], RK)), RR)
                     for s, j in enumerate(donors)) and rank(RR) == 3, 'provided common readout residual')
            need(bool(recorded['moved_from_geometric_base']) == changed, 'provided movement label')
            fibre_certificates[str(h)][str(i)] = {'kernel': K[0].tolist(), 'readout': readouts[0].tolist()}
        need(len(moved) == (20 if h == 263 else 0), 'first-centre movement and retained second fibres')
        H_rows.append({'H': h, 'donors': donors, 'ports': ports, 'geometric_common_fibres': 36,
                       'native_common_fibres': len(set(receivers) & set(range(111))),
                       'moved_receivers': moved, 'moved_native_fibres': len(set(moved) & set(range(111)))})

    # Authenticate the geometric overlap actually used by the triangular glue.
    cores = {a: np.array([u_polynomial(1 << s, a) for s in range(6)], dtype=np.uint8).T for a in Q}
    need(all(rank(S) == 6 for S in cores.values()), 'six-dimensional scalar cores')
    overlap_count = 0
    linear = np.zeros((16, 2), dtype=np.uint8)
    linear[0, 0] = linear[1, 1] = 1
    for a in sorted(Q):
        for b in sorted(Q - {a}):
            values = [v for v in range(1, 64) if field_polar(v, a) == (1 ^ q(v)) and
                      field_polar(v, b) == (1 ^ q(v))]
            P = np.array([u_polynomial(v, b) for v in values], dtype=np.uint8).T
            line = np.zeros((16, 1), dtype=np.uint8)
            line[0, 0], line[1, 0] = a, 1
            need(len(values) == 20 and rank(P) == 5, 'two-node propagation family')
            need(rank(np.hstack((cores[a], cores[b]))) == 10 and
                 rank(np.hstack((cores[a], linear))) == rank(np.hstack((cores[b], linear))) == 6,
                 'full core intersection exactly span(1,z)')
            need(rank(np.hstack((cores[a], P))) == 10 and
                 rank(np.hstack((cores[a], line))) == 6 and rank(np.hstack((P, line))) == 5,
                 'propagation intersection exactly span(z+a)')
            overlap_count += 1
    P = kron(np.array([u_polynomial(v, 60) for v in range(1, 64) if q(v) == 1 and
                       not field_polar(v, 60)], dtype=np.uint8).T, eye)
    need(rank(P) == 15 and rank(np.hstack((kron(cores[0], eye), P))) == 30, 'actual 0,60 overlap dimensions')
    for j, companion in [(0, 116), (61, 642), (62, 643)]:
        need(nodes[j][263] == 0 and nodes[j][companion] == 60, 'actual companion nodes')
        need(not np.any(mm(maps[j][263], P)) and not np.any(maps[j][263][:, 3:6]) and
             rank(maps[j][263][:, :3]) == 3, 'protected companion core and invertible constant block')
        need(np.array_equal(maps[j][companion], maps[61][642]), 'literal copied companion edit')

    # Rebuild original early owners and the two-lane 96-dimensional bases.
    quota = Counter()
    route_raw = gzip.decompress((base / 'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
    for line in route_raw.splitlines():
        phase, owner, _, plane, _, _, source, _ = json.loads(line)
        if phase == 'X' and plane is not None:
            need(owner == source, 'genuine original early owner')
            quota[owner, plane] += 1
    need(Counter(quota.values()) == {15: 2675, 30: 422, 45: 11}, 'raw early quota census')
    early_rows = []
    for j in sorted(maps):
        chart = 263 if j in planes[263] else 642
        seed = coeff['actual_early_seeds'][str(j)]
        rows = []
        need(max(quota[j, h] for h in stars[j]) == 30, 'ordinary donor, no singleton')
        for h in stars[j]:
            F = maps[j][h]
            count = quota[j, h] // 15
            need(count in (1, 2), 'ordinary one/two-lane quota')
            if count == 2:
                rows.append(kron(np.eye(2, dtype=np.uint8), F))
            elif h in [263, 642]:
                rows.append(np.hstack((F, np.zeros_like(F))))
            else:
                tag = f'early/{chart}/3/{j}/{h}/{seed}'
                A = np.frombuffer(hashlib.shake_256(tag.encode('ascii')).digest(18), dtype=np.uint8).reshape(3, 6) & 63
                need(rank(A) == 3, 'local early frame extends to a full quotient frame')
                rows.append(np.hstack((mm(A[:, :3], F), mm(A[:, 3:], F))))
        E = np.vstack(rows)
        _, pivots, determinant = echelon(E)
        need(E.shape == (96, 96) and len(pivots) == 96, 'full actual early source basis')
        early_rows.append({'donor': j, 'rank': 96, 'determinant': determinant, 'seed': seed,
                           'source_chart': chart})

    # Relevant faults: a missing reflected edit, and a deleted actual quotient.
    omitted = []
    for i in [i for i in range(120) if planes[263] <= adjacency[i]]:
        A = np.vstack([old_maps[0][p] if p == 116 else maps[0][p] for p in visible[0, i] if p != 263])
        K = null(A)
        if rank(np.hstack((K, kernels[61, 263, i]))) > 3:
            omitted.append(i)
    need(len(omitted) == 20, 'omitted copied edit destroys the affected common fibres')
    receiver = min(adjacency[61] & set(range(111)))
    full = np.vstack([maps[61][h] for h in visible[61, receiver]])
    need((rank(full), rank(full[:-3])) == (48, 45), 'deleting an actual quotient loses three dimensions')

    # Reconstruct the ancillary quadratic-pencil premise without importing it.
    parameters, _ = read_json(base / 'bit-coupled-native-geometric-h-source/component/output/PARAMETERS.json')
    u, v = (roots[j] for j in sorted(planes[263])[:2])
    perpendicular = {x for x in range(256) if not polar(x, u) and not polar(x, v)}
    source_basis, field_basis = witt(perpendicular, quadratic), witt(range(64), q)
    field_chart = {xor(source_basis[s] for s in range(6) if mask >> s & 1):
                   xor(field_basis[s] for s in range(6) if mask >> s & 1) for mask in range(64)}
    omega = parameters['omega']
    coordinates = {xor(parameters['F4_basis'][s] for s in range(6) if mask >> s & 1):
                   [((mask >> (2 * t)) & 1) ^ int(MUL[omega, (mask >> (2 * t + 1)) & 1]) for t in range(3)]
                   for mask in range(64)}
    need(len(field_chart) == len(coordinates) == 64 and all(q(a) == xor(power(t, 3) for t in r)
                                                            for a, r in coordinates.items()), 'literal Hermitian coordinates')
    E = []
    for d in H_rows[0]['ports']:
        span = binary_span(roots[j] for j in charts[d])
        radical = sorted(x for x in span if all(not polar(x, y) for y in span))
        need(len(span) == 16 and len(radical) == 4 and set(radical) <= perpendicular,
             'actual D4 radical from root labels')
        E.append([power(t, 2) for t in coordinates[field_chart[radical[1]]]])
    E = np.array(E, dtype=np.uint8)
    E2 = np.array([[MUL[x, x], MUL[y, y], MUL[z, z], MUL[x, y], MUL[x, z], MUL[y, z]]
                   for x, y, z in E], dtype=np.uint8)
    N = null(E2.T).T
    schur = np.vstack([MUL[N[p], E[:, t]] for p in range(3) for t in range(3)])
    need(rank(E) == 3 and rank(E2) == rank(schur) == 6 and not np.any(mm(schur, E)),
         'universal pencil theorem finite Schur premise')
    alpha, beta = np.array(parameters['weights'], dtype=np.uint8)
    need(all(alpha) and all(beta) and all(alpha ^ beta), 'three nowhere-zero weights')
    W = [null(MUL[c[:, None], E2].T).T for c in [alpha ^ beta, beta, alpha]]
    need(rank(np.vstack(W)) == 9, 'literal quadratic provider invertible')
    for s, weights in [(0, alpha), (1, alpha), (2, beta)]:
        pencil = np.array([mm(W[s], MUL[weights[:, None], MUL[E[:, t, None], E]]).reshape(-1)
                           for t in range(3)], dtype=np.uint8).T
        need(rank(pencil) == 3, 'literal pencil has no nonzero extension-field zero')
    alpha_bad = MUL[omega, beta]
    W_bad = [null(MUL[c[:, None], E2].T).T for c in [alpha_bad ^ beta, beta, alpha_bad]]
    need(rank(np.vstack(W_bad)) == 3, 'proportional weight negative control')

    # Bind the nonzero-centre obstruction to the actual native parameter chart.
    global_nodes, _ = read_json(base / 'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json')
    a = global_nodes['H_nodes'][263]
    need(a == 49 and power(omega, 2) ^ omega == 1, 'literal nonzero centre and F4 unit')
    moore = np.array([[power(1 << r, 1 << s) for s in range(6)] for r in range(6)], dtype=np.uint8)
    moore_inverse = inverse(moore)
    receiver_parameters = global_nodes['receiver_parameters']
    native_R = []
    for donor in sorted(planes[263]):
        X, Y = [], []
        for i in [i for i in range(120) if planes[263] <= adjacency[i]]:
            v = receiver_parameters[str(donor)][str(i)]
            bits = [v >> s & 1 for s in range(6)]
            if rank(np.array(X + [bits], dtype=np.uint8)) > len(X):
                X.append(bits)
                Y.append(coordinates[field_chart[roots[i]]])
        need(len(X) == 6, 'native parameters span the full binary core')
        R = mm(inverse(np.array(X, dtype=np.uint8)), np.array(Y, dtype=np.uint8))
        values = {v: mm(np.array([[v >> s & 1 for s in range(6)]], dtype=np.uint8), R)[0]
                  for v in range(64)}
        need(all(np.array_equal(values[receiver_parameters[str(donor)][str(i)]], coordinates[field_chart[roots[i]]])
                 for i in range(120) if planes[263] <= adjacency[i]), 'all actual Hermitian coordinate bindings')
        need(all(xor(power(t, 3) for t in values[v]) == q(v) ^ field_polar(v, a) for v in range(64)),
             'entire native Hermitian norm identity')
        coefficients = mm(moore_inverse, np.array([values[1 << s] for s in range(6)], dtype=np.uint8))
        need(all(np.array_equal(mm(np.array([[power(v, 1 << s) for s in range(6)]], dtype=np.uint8), coefficients)[0], values[v])
                 for v in range(64)) and np.any(coefficients[4]), 'linearized R has nonzero v16 coefficient')
        native_R.append({'donor': donor, 'centre': 263, 'node': 49, 'R_coefficients': coefficients.tolist(),
                         'r4': coefficients[4].tolist()})
    need(all(q(int(MUL[omega, v])) == q(v) for v in range(64)), 'q is F4 invariant')
    need(rank(np.array([[field_polar(1 << r, 1 << s) for s in range(6)] for r in range(6)], dtype=np.uint8)) == 6,
         'nondegenerate binary polar form')

    args.out.mkdir(parents=True, exist_ok=True)
    result = {'status': 'PASS_INDEPENDENT_PROTECTED_TWO_H_MOVING_FIBRES',
              'source_cuts': len(source_certificates), 'native_source_cuts': sum(x['native_cuts'] for x in source_rows),
              'source_rows': source_rows, 'H': H_rows, 'actual_early_bases': early_rows,
              'geometric_incidence_authenticated': True, 'all_ordered_core_overlap_pairs': overlap_count,
              'quadratic_pencil_schur_rank': 6, 'proportional_weight_provider_rank': 3,
              'native_nonzero_centre_parameter_bindings': native_R,
              'omitted_companion_edit_failures': omitted, 'deleted_quotient_ranks': [48, 45],
              'coefficient_payload_sha256': hashlib.sha256(coefficient_raw).hexdigest(),
              'fibre_payload_sha256': hashlib.sha256(fibre_raw).hexdigest(),
              'author_executable_imports': False, 'new_complete_kappa': False,
              'complete_bank_invoice': False, 'global_middle_word': False}
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    (args.out / 'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(source_certificates, sort_keys=True, indent=2) + '\n')
    payload = (json.dumps(fibre_certificates, sort_keys=True, separators=(',', ':')) + '\n').encode()
    (args.out / 'INDEPENDENT-FIBRES.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    print(result['status'], len(source_certificates), result['native_source_cuts'], overlap_count, flush=True)


if __name__ == '__main__':
    main()
