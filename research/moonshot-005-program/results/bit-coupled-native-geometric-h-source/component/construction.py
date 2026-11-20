"""Geometric inverse fibres and a quadratic-annihilator H263 word.

The three central quotients are constructed on the common 18-dimensional
fibre span.  The physical nine-port grouping differs from the old marking.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(ok, message):
    if not ok:
        raise ValueError(message)


def context(repo):
    base = repo / "research/moonshot-005-program/results"
    f = module(base / "bit-spread-disjoint-h-sources/author/families.py", "geometric_families")
    pair = module(base / "bit-spread-overlap-source/author/pair.py", "geometric_kernel")
    return f, f.Atlas(repo), pair


def rref(matrix, a):
    matrix = np.array(matrix, dtype=np.uint8, copy=True)
    pivots = []
    for col in range(matrix.shape[1]):
        row = len(pivots)
        choices = np.flatnonzero(matrix[row:, col])
        if not len(choices):
            continue
        other = row + int(choices[0])
        matrix[[row, other]] = matrix[[other, row]]
        matrix[row] = a.product[a.inverse[matrix[row, col]], matrix[row]]
        factors = matrix[:, col].copy()
        factors[row] = 0
        matrix ^= a.product[factors[:, None], matrix[row, None, :]]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots


def inverse(matrix, a):
    n = len(matrix)
    reduced, _ = rref(np.hstack([matrix, np.eye(n, dtype=np.uint8)]), a)
    require(np.array_equal(reduced[:, :n], np.eye(n, dtype=np.uint8)), "invertible matrix")
    return reduced[:, n:]


def power(x, n, a):
    value = 1
    for _ in range(n):
        value = int(a.product[value, x])
    return value


def quadratic(x, a):
    return power(x, 9, a) ^ power(x, 18, a) ^ power(x, 36, a)


def xor(values):
    result = 0
    for value in values:
        result ^= int(value)
    return result


def witt(space, q):
    space = set(space)
    basis = []
    while len(space) > 1:
        polar = lambda x, y: q(x ^ y) ^ q(x) ^ q(y)
        zeros = sorted(x for x in space if x and not q(x))
        if zeros:
            e = zeros[0]
            v = next(x for x in zeros if polar(e, x))
        else:
            e = min(space - {0})
            v = min(space - {0, e})
        basis += [e, v]
        space = {x for x in space if not polar(x, e) and not polar(x, v)}
    return basis


def geometry(f, a, prm):
    chart = f.Chart(a, prm["H"], 3)
    u, v = (a.masks[j] for j in chart.donors[:2])
    space = {x for x in range(256) if not a.algebra.polar(x, u) and not a.algebra.polar(x, v)}
    basis = witt(space, a.algebra.quadratic)
    target = witt(range(64), lambda x: quadratic(x, a))
    nodes = {xor(basis[p] for p in range(6) if mask >> p & 1):
             xor(target[p] for p in range(6) if mask >> p & 1) for mask in range(64)}
    require(len(nodes) == 64 and all(a.algebra.quadratic(x) == quadratic(y, a) for x, y in nodes.items()),
            "the actual H-perpendicular quadratic isometry")
    f4basis = prm["F4_basis"]
    omega = prm["omega"]
    require(a.product[omega, omega] ^ omega == 1, "literal F4 subfield")
    coordinates = {
        xor(f4basis[p] for p in range(6) if mask >> p & 1):
        tuple(((mask >> (2*p)) & 1) ^ int(a.product[omega, (mask >> (2*p+1)) & 1]) for p in range(3))
        for mask in range(64)}
    require(len(coordinates) == 64 and
            all(quadratic(x, a) == xor(power(t, 3, a) for t in r) for x, r in coordinates.items()),
            "q is the three-coordinate Hermitian norm")
    by_coordinate = {r: x for x, r in coordinates.items()}
    rotation = {x: by_coordinate[tuple(int(a.product[omega, t]) for t in r)] for x, r in coordinates.items()}
    all_ports = [d for d, D in enumerate(a.charts) if a.planes[chart.h] <= D]
    ports = [d for d in all_ports if all(rotation[nodes[x]] in {nodes[y] for y in a.spread["D_radicals"][d]}
                                       for x in a.spread["D_radicals"][d])]
    require(ports == prm["ports"] and len(ports) == 9, "nine actual Desarguesian D exits")
    chart.ports = ports
    chart.radical = {d: sorted(set(a.spread["D_radicals"][d]) - {0}) for d in ports}
    receiver = {i: coordinates[nodes[a.masks[i]]] for i in chart.views}
    E1 = np.array([[power(t, 2, a) for t in coordinates[nodes[chart.radical[d][0]]]] for d in ports], dtype=np.uint8)
    E2 = np.array([[a.product[x, x], a.product[y, y], a.product[z, z],
                    a.product[x, y], a.product[x, z], a.product[y, z]] for x, y, z in E1], dtype=np.uint8)
    require(a.rank(E1) == 3 and a.rank(E2) == 6, "linear and quadratic evaluation dimensions")
    for i, r in receiver.items():
        values = a.mm(E1, np.array(r, dtype=np.uint8)[:, None])[:, 0]
        visible = [q for q, d in enumerate(ports) if a.charts[d] <= a.adj[i]]
        require(set(visible) == set(np.flatnonzero(values == 0)) and len(visible) == 3,
                "actual visible exits are precisely the three zero evaluations")
    return chart, nodes, receiver, E1, E2


def build(f, a, pair, prm):
    chart, nodes, receiver, E1, E2 = geometry(f, a, prm)
    aa, bb = np.asarray(prm["weights"], dtype=np.uint8)
    require(all(aa) and all(bb) and all(aa ^ bb), "nonzero three coefficient weights")
    W = [pair.null_basis(a.product[c[:, None], E2].T, a).T for c in (aa ^ bb, bb, aa)]
    require(all(matrix.shape == (3, 9) for matrix in W), "three quadratic annihilators")
    T = np.vstack(W)
    Hword = inverse(T, a)
    D, fibres, readouts = {}, {}, {}
    points = {x: np.kron(a.vandermonde([nodes[x]], 16), np.eye(3, dtype=np.uint8)) for x in chart.singular}
    zero = np.zeros((3, 3), dtype=np.uint8)
    for i, r in receiver.items():
        values = a.mm(E1, np.array(r, dtype=np.uint8)[:, None])[:, 0]
        A0 = a.product[values[:, None], a.product[aa[:, None], E1]]
        A1 = a.product[values[:, None], a.product[bb[:, None], E1]]
        A = np.hstack([A0, A1])
        require(a.rank(A[values != 0]) == 6, "all six actual unseen output coordinates")
        D[i] = [a.mm(W[0], A0), a.mm(W[1], A0), a.mm(W[2], A1)]
        require(all(a.rank(matrix) == 3 for matrix in D[i]), "all three central fibre pencils invertible")
        expected = np.block([[D[i][0], D[i][0]], [D[i][1], zero], [zero, D[i][2]]])
        require(np.array_equal(a.mm(T, A), expected), "exact quadratic-annihilator identity")
        visible = [q for q, d in enumerate(chart.ports) if a.charts[d] <= a.adj[i]]
        readouts[i] = [a.mm(Hword[np.ix_(visible, range(3*j, 3*(j+1)))], D[i][j]) for j in range(3)]
        require(a.rank(readouts[i][0]) == 3 and np.array_equal(readouts[i][0], readouts[i][1])
                and np.array_equal(readouts[i][0], readouts[i][2]), "common invertible H readout")
        xs = [x for x in chart.singular if not a.algebra.polar(x, a.masks[i])]
        K = pair.null_basis(np.vstack([points[x] for x in xs]), a)
        require(K.shape == (48, 3), "whole geometric off-H inverse fibre")
        fibres[i] = a.product[power(nodes[a.masks[i]], 2, a), K]
    joined = np.hstack(list(fibres.values()))
    _, pivots = rref(joined, a)
    S = joined[:, pivots]
    require(S.shape == (48, 18), "six-dimensional scalar fibre core, repeated three times")
    _, rows = rref(S.T, a)
    left = inverse(S[rows], a)
    annihilator = pair.null_basis(S.T, a).T
    controls = []
    for j in range(3):
        target = np.hstack([D[i][j] for i in chart.views])[:, pivots]
        F = np.zeros((3, 48), dtype=np.uint8)
        F[:, rows] = a.mm(target, left)
        require(all(np.array_equal(a.mm(F, K), D[i][j]) for i, K in fibres.items()),
                "the central linear pencil extends on the entire actual fibre core")
        tail = f.coefficients(f"geo-quadratic-tail/{chart.h}/{prm['weight_seed']}/{prm['tail_seed']}/{j}", (3, 30))
        F ^= a.mm(tail, annihilator)
        controls.append(F)
    maps = {j: chart.maps(points, j, controls[p]) for p, j in enumerate(chart.donors)}
    return {"chart": chart, "maps": maps, "controls": controls, "points": points, "fibres": fibres,
            "E1": E1, "E2": E2, "T": T, "Hword": Hword, "pencils": D,
            "core": S, "annihilator": annihilator, "nodes": nodes}
