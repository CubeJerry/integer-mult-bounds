#!/usr/bin/env python3
"""Independent finite algebra checks for A/stable-hermite-checks.md.

Toy dimensions test the inverse-Gram repair identity and strict Gram tests;
the all-parameter probabilistic existence statement is checked by proof.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import random


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in transpose(b)] for row in a]


def inverse(a):
    n = len(a)
    rows = [[F(v) for v in row] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for i in range(n):
        pivot = next(j for j in range(i, n) if rows[j][i])
        rows[i], rows[pivot] = rows[pivot], rows[i]
        c = rows[i][i]
        rows[i] = [v / c for v in rows[i]]
        for j in range(n):
            if j != i:
                c = rows[j][i]
                rows[j] = [x - c * y for x, y in zip(rows[j], rows[i])]
    return [row[n:] for row in rows]


def positive_definite(a):
    n = len(a)
    diagonal = []
    lower = [[F(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        d = F(a[i][i]) - sum((lower[i][j] ** 2 * diagonal[j] for j in range(i)), F(0))
        if d <= 0:
            return False
        diagonal.append(d)
        for j in range(i + 1, n):
            lower[j][i] = (F(a[j][i]) - sum((lower[j][k] * lower[i][k] * diagonal[k] for k in range(i)), F(0))) / d
    return True


def main():
    rng = random.Random(2026112609)
    width, rows, maximum_support = 5, 64, 3
    supports = [j for count in range(1, maximum_support + 1) for j in combinations(range(width), count)]
    attempted = 0
    while True:
        attempted += 1
        h = [[F(rng.choice((-1, 1))) for _ in range(width)] for _ in range(rows)]
        full_gram = multiply(transpose(h), h)
        valid = True
        for support in supports:
            gram = [[full_gram[i][j] for j in support] for i in support]
            lo = [[2 * gram[i][j] - rows * (i == j) for j in range(len(support))] for i in range(len(support))]
            hi = [[3 * rows * (i == j) - 2 * gram[i][j] for j in range(len(support))] for i in range(len(support))]
            valid &= positive_definite(lo) and positive_definite(hi)
        if valid:
            break
        assert attempted < 10000
    # Frobenius norm gives this deliberately generous global positive control.
    assert rows * width < 64 * (rows + width)
    cases, supersets, wrong_inverse_failures = 0, 0, 0
    for support in supports:
        v = [[row[j] for j in support] for row in h]
        gram = multiply(transpose(v), v)
        gi = inverse(gram)
        c = multiply(multiply(gi, transpose(v)), h)
        wrong_b = multiply(transpose(h), v)
        for z in (-1, 1):
            for extra_correct in (False, True):
                p = [z] * width
                for t, j in enumerate(support):
                    p[j] = z if extra_correct and t % 2 == 0 else z * (2 * t + 3)
                d = [F(-(p[j] + 2 * z), 2) for j in support]
                q = [[sum((c[t][i] * d[t] * c[t][j] for t in range(len(support))), F(0)) for j in range(width)] for i in range(width)]
                wrong_q = [[sum((wrong_b[i][t] * d[t] * c[t][j] for t in range(len(support))), F(0)) for j in range(width)] for i in range(width)]
                bad = False
                for i in range(width):
                    g = F(3 * p[i] - p[i] ** 3, 2)
                    for j in range(width):
                        result = g * (i == j) - (p[i] - z) * q[i][j] * (p[j] - z)
                        assert result == z * (i == j)
                        wrong = g * (i == j) - (p[i] - z) * wrong_q[i][j] * (p[j] - z)
                        bad |= wrong != z * (i == j)
                cases += 1
                supersets += extra_correct
                wrong_inverse_failures += bad
    assert wrong_inverse_failures > 0
    result = {
        "status": "pass",
        "scope": "exact inverse-Gram repair and strict Gram tests in toy dimensions; existence probability checked by proof",
        "rows": rows, "width": width, "maximum_support": maximum_support,
        "sign_matrices_tried": attempted, "support_gram_tests": 2 * len(supports),
        "all_input_matrix_identities": cases, "exception_superset_cases": supersets,
        "negative_omitted_right_inverse_cases_detected": wrong_inverse_failures,
    }
    Path(__file__).with_name("stable-review-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
