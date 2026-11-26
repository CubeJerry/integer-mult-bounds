#!/usr/bin/env python3
"""Exact invariant-sector controls, without floating eigenvalue calculations."""
from datetime import datetime, timezone
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json
import platform

ROOT = Path(__file__).resolve().parent


def det3(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def char_value(matrix, value):
    return det3([[(value if i == j else 0) - matrix[i][j]
                  for j in range(3)] for i in range(3)])


def apply(weights, vector):
    total = sum(weights)
    return [sum(b * x for b, x in zip(weights, vector[1:]))] + [
        b * vector[0] + (total - b) * vector[j]
        for j, b in enumerate(weights, 1)]


def main():
    families = invariant_checks = quotient_checks = determinant_checks = 0
    for m in range(2, 33):
        for positive in range(1, m):
            negative = m - positive
            weights = [1] * positive + [-1] * negative
            total = positive - negative
            for indices, eigenvalue in ((range(1, positive + 1), total - 1),
                                       (range(positive + 1, m + 1), total + 1)):
                anchor = indices.start
                for j in list(indices)[1:]:
                    vector = [0] * (m + 1)
                    vector[anchor], vector[j] = -1, 1
                    assert apply(weights, vector) == [eigenvalue * x for x in vector]
                    invariant_checks += 1
            basis = [[1] + [0] * m,
                     [0] + [1] * positive + [0] * negative,
                     [0] + [0] * positive + [1] * negative]
            matrix = [[0, positive, -negative], [1, total - 1, 0], [-1, 0, total + 1]]
            for j in range(3):
                expected = [sum(matrix[i][j] * basis[i][row] for i in range(3))
                            for row in range(m + 1)]
                assert apply(weights, basis[j]) == expected
                quotient_checks += 1
            assert apply(weights, [1] * (m + 1)) == [total] * (m + 1)
            for value in (-m - 2, 0, m + 2, m + 3):
                expected = (value - total) * (value * value - total * value - (m + 1))
                assert char_value(matrix, value) == expected
                determinant_checks += 1
            families += 1

    seed_checks = 0
    for width in range(2, 10):
        for seed in range(1, 1 << width):
            weights = [(-1) ** ((seed & query).bit_count() % 2)
                       for query in range(1, 1 << width)]
            assert weights.count(1) == (1 << (width - 1)) - 1
            assert weights.count(-1) == 1 << (width - 1)
            assert sum(weights) == -1
            seed_checks += 1

    nonsquare_checks = 0
    for width in range(2, 129):
        discriminant = 1 + (1 << (width + 2))
        root = isqrt(discriminant)
        assert root * root < discriminant < (root + 1) ** 2
        nonsquare_checks += 1

    matrix = [[0, 1, -2], [1, -2, 0], [-1, 0, 0]]
    assert char_value(matrix, 0) == -4
    assert char_value(matrix, 0) != -3  # Wrong m instead of m+1.
    wrong_sign = [[0, 1, 2], [1, -2, 0], [-1, 0, 0]]
    assert char_value(wrong_sign, 0) != char_value(matrix, 0)
    assert isqrt(1 + (1 << 3)) ** 2 == 1 + (1 << 3)  # Excluded r=1.
    all_positive = [1, 1, 1]
    assert apply(all_positive, [3, -1, -1, -1]) == [-3, 1, 1, 1]

    files = [Path(__file__), ROOT / "STAR-SPECTRAL-TEST-SECTOR.md"]
    receipt = {
        "status": "passed", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "sign_count_families": families,
        "zero_sum_eigenvector_checks": invariant_checks,
        "three_dimensional_quotient_checks": quotient_checks,
        "exact_determinant_values": determinant_checks,
        "nonzero_seed_count_checks": seed_checks,
        "nonsquare_discriminants": nonsquare_checks, "negative_controls": 4,
        "small_test_sector": {"m": 3, "positive": 1, "negative": 2,
                              "quadratic": "lambda^2+lambda-4", "discriminant": 17},
        "sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in files},
        "scope": "Exact finite invariant-sector checks; no full-star basis, tape timing or multiplier execution."
    }
    (ROOT / "star-spectral-sector-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
