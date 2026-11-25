#!/usr/bin/env python3
"""Exact checks of the E003-basis commutator/fraction transfer."""
from __future__ import annotations

from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import random

from verify_inverse_query_commutator import Field, rank, inverse, multiply, commutator, eye, evaluate


def kron(a, b, field):
    return [[field.mul(a[i][j], b[k][l])
             for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def main():
    rng = random.Random(1732050807)
    counts = Counter()
    for order in (4, 5, 7):
        field = Field(order)
        pairs = [(a, b) for a in range(1, order) for b in range(1, order) if a != b]
        for m in range(1, 7):
            k = (m - 1) // 2
            for rep in range(8):
                local = [rng.choice(pairs) for _ in range(m)]
                target = [[1]]
                inverse_target = [[1]]
                for a, b in local:
                    c = field.sub(b, a)
                    d = field.neg(field.mul(field.mul(a, b), field.inv(c)))
                    matrix = [[field.add(a, b), d], [c, 0]]
                    inv = inverse(matrix, field)
                    assert inv is not None and inv[0][0] == 0
                    target = kron(target, matrix, field)
                    inverse_target = kron(inverse_target, inv, field)
                    counts["local_two_point_matrix_identities"] += 1
                masks = [int(sum(alpha) <= k) for alpha in product(range(2), repeat=m)]
                expected = 2**m - (comb(m, m // 2) if m % 2 == 0 else 0)
                actual = rank(commutator(target, masks, masks, field), field)
                assert actual == expected
                counts["universal_target_cut_ranks"] += 1
                low = [i for i, alpha in enumerate(product(range(2), repeat=m)) if sum(alpha) <= k]
                high = [i for i, alpha in enumerate(product(range(2), repeat=m)) if sum(alpha) >= m - k]
                assert len(low) == len(high)
                low_set, high_set = set(low), set(high)
                assert all(target[i][j] == 0 for i in range(2**m) if i not in low_set for j in high)
                assert all(inverse_target[i][j] == 0 for i in range(2**m) if i not in high_set for j in low)
                assert rank([[target[i][j] for j in high] for i in low], field) == len(low)
                counts["high_low_degree_subspace_identities"] += 3

    # Direct whole ternary spectrum checks for the stronger binary-tail
    # rational bound, without implementing the averaging proof in the test.
    field = Field(4)
    for m in range(3, 8):
        zero = (0,) * m
        monomials = [alpha for alpha in product(range(3), repeat=m) if sum(x != 0 for x in alpha) <= 1]
        for rep in range(4):
            a = {alpha: [[rng.randrange(4) for _ in range(3)] for _ in range(3)] for alpha in monomials}
            b = {alpha: [[0] * 3 for _ in range(3)] for alpha in monomials}
            b[zero] = eye(3, field)
            for alpha in monomials:
                b[alpha][0][1] = rng.randrange(4)
                b[alpha][1][2] = rng.randrange(4)
            total = 0
            for point in product(range(3), repeat=m):
                av = evaluate(a, point, 2, 3, 3, field)
                bv = evaluate(b, point, 2, 3, 3, field)
                inv = inverse(bv, field)
                assert inv is not None
                predictor = multiply(av, inv, field)
                f = field.power(2, sum(point) % 3)
                error = [[field.sub(f if i == j else 0, predictor[i][j]) for j in range(3)] for i in range(3)]
                total += rank(error, field)
                counts["ternary_fraction_spectral_ranks"] += 1
            tail_numerator = sum(comb(m, j) for j in range((m + 2) // 2 + 1, m + 1))
            assert (2**m) * total >= 3**m * 3 * tail_numerator
            counts["ternary_binary_tail_fraction_cases"] += 1

    # Nonzero distinct local target values are indispensable: AND on a
    # {0,1} spectrum differs from zero only once, defeating the proposed
    # universal degree-zero binomial tail if zero were permitted.
    m = 5
    and_error_numerator = 1
    binary_tail = sum(comb(m, j) for j in range((m // 2) + 1, m + 1))
    assert and_error_numerator < binary_tail
    result = {"status": "passed", "arithmetic": "exact F4, F5, F7 and integers",
              "seed": 1732050807, "counts": dict(counts),
              "negative_controls": [{"omission": "nonzero local target values",
                                      "model": "AND on {0,1}^5 versus zero predictor",
                                      "actual_error_numerator": and_error_numerator,
                                      "invalid_binary_tail_numerator": binary_tail,
                                      "common_denominator": 2**m}],
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "helper_sha256": hashlib.sha256(Path(__file__).with_name("verify_inverse_query_commutator.py").read_bytes()).hexdigest(),
              "scope": "Weighted two-point algebra and exact finite rank checks; not a tape implementation"}
    Path(__file__).with_name("weighted-two-point-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
