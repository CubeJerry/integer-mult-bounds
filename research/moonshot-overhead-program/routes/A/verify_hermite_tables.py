#!/usr/bin/env python3
"""Finite exact checks of the binary Hermite table; not a recursive tape proof."""

from fractions import Fraction as F
from itertools import combinations
import json
import random


def polynomial_roots_integer(roots):
    coeff = [1]
    for root in roots:
        out = [0] * (len(coeff) + 1)
        for degree, value in enumerate(coeff):
            out[degree] -= root * value
            out[degree + 1] += value
        coeff = out
    return coeff


def lagrange_inverse(nodes):
    rows, deltas = [], []
    for at, node in enumerate(nodes):
        others = [x for index, x in enumerate(nodes) if index != at]
        delta = 1
        for other in others:
            delta *= node - other
        rows.append([F(value, delta) for value in polynomial_roots_integer(others)])
        deltas.append(delta)
    return rows, deltas


def mv(matrix, vector):
    return [sum(a * x for a, x in zip(row, vector)) for row in matrix]


def verify():
    rng = random.Random(2026112601)
    checks = 0
    superset_checks = 0
    nonsymmetric_wrong_failed = False
    for M in range(2, 13):
        for s in range(1, min(M, 5) + 1):
            H = [[F(node ** degree) for node in range(1, M + 1)] for degree in range(s)]
            for j in range(1, s + 1):
                subsets = list(combinations(range(M), j))
                if len(subsets) > 12:
                    subsets = rng.sample(subsets, 12)
                for J in subsets:
                    nodes = [i + 1 for i in J]
                    inv, deltas = lagrange_inverse(nodes)
                    V = [[F(node ** degree) for node in nodes] for degree in range(j)]
                    for row in range(j):
                        for col in range(j):
                            assert sum(inv[row][q] * V[q][col] for q in range(j)) == (row == col)
                    for delta in deltas:
                        assert 1 <= abs(delta) <= M ** (j - 1)
                    for row in inv:
                        assert max(abs(x) for x in row) <= (M + 1) ** (j - 1)
                    m, D = 5, 3
                    z = rng.choice((-1, 1))
                    p = [z] * M
                    for index in J:
                        p[index] = rng.randrange(-2 * m ** D, 2 * m ** D + 1)
                    # Include a nominal exception whose prediction is already correct.
                    if j >= 2:
                        p[J[0]] = z
                        superset_checks += 1
                    diag = [F(-p[index] - 2 * z, 2) for index in J]
                    A = [[sum(inv[t][a] * diag[t] * inv[t][b] for t in range(j))
                          for b in range(j)] for a in range(j)]
                    Q = 2
                    for delta in deltas:
                        Q *= delta * delta
                    assert Q <= 2 * M ** (2 * j * (j - 1))
                    for row in A:
                        for value in row:
                            assert Q % value.denominator == 0
                            assert abs(value) <= 2 * j * m ** D * (M + 1) ** (2 * (j - 1))
                    x = [F(rng.randrange(-20, 21)) for _ in range(M)]
                    hx = mv(H, x)
                    hpx = mv(H, [p_i * x_i for p_i, x_i in zip(p, x)])
                    error_checks = [hpx[a] - z * hx[a] for a in range(j)]
                    a = mv(A, error_checks) + [F(0)] * (s - j)
                    Z = [sum(H[degree][index] * a[degree] for degree in range(s))
                         for index in range(M)]
                    result = [(F(3, 2) * p_i - F(1, 2) * p_i ** 3) * x_i - p_i * Z_i + z * Z_i
                              for p_i, x_i, Z_i in zip(p, x, Z)]
                    assert result == [z * x_i for x_i in x]
                    if j >= 2:
                        wrong = [[sum(inv[a][t] * diag[t] * inv[t][b] for t in range(j))
                                  for b in range(j)] for a in range(j)]
                        if mv(wrong, error_checks) != mv(A, error_checks):
                            nonsymmetric_wrong_failed = True
                    checks += 1
    assert nonsymmetric_wrong_failed
    return {"status": "passed", "scope": "exact finite algebra, not full tape bound",
            "hermite_cases": checks, "exception_superset_cases": superset_checks,
            "negative_control_detected": "omitting inverse transpose"}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
