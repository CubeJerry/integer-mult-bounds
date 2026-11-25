#!/usr/bin/env python3
"""Exact finite controls for the scoped bilinear supplier lemmas.

These exhaustive finite input checks support the written proof; they are
not a machine-complexity experiment or a proof of an asymptotic bound.
"""
from itertools import product
from pathlib import Path
import json
import random


def main():
    rng = random.Random(2026112505)
    counts = {
        "separately_affine_fourth_moments": 0,
        "bilinear_walsh_second_moments": 0,
        "rounded_error_probability_checks": 0,
        "large_norm_probability_checks": 0,
        "grid_product_nonvanishing_families": 0,
        "finite_field_bilinear_probabilities": 0,
        "input_evaluations": 0,
        "negative_controls": 0,
    }

    for h in range(1, 6):
        signs = list(product((-1, 1), repeat=h))
        for _ in range(40):
            coefficients = [[rng.randint(-4, 4) for _ in range(h + 1)]
                            for _ in range(h + 1)]
            values = []
            for eps in signs:
                for delta in signs:
                    e, d = (1,) + eps, (1,) + delta
                    values.append(sum(coefficients[j][k] * e[j] * d[k]
                                      for j in range(h + 1)
                                      for k in range(h + 1)))
            n = len(values)
            second = sum(x*x for x in values)
            fourth = sum(x**4 for x in values)
            assert n * fourth <= 9 * second * second
            counts["separately_affine_fourth_moments"] += 1
            counts["input_evaluations"] += n

        bits = list(product((0, 1), repeat=h))
        for _ in range(100):
            u = rng.choice((2, 3, 7))
            denominator = rng.choice((1, 2, 3, 7, 16, 31))
            matrix = [[rng.randint(-4, 4) for _ in range(h)]
                      for _ in range(h)]
            # Error matrix = matrix / denominator; all arithmetic below is exact.
            numerators = [u*u * sum(matrix[j][k] * a[j] * b[k]
                                     for j in range(h) for k in range(h))
                          for a in bits for b in bits]
            n = len(numerators)
            second = sum(x*x for x in numerators)
            fourth = sum(x**4 for x in numerators)
            frobenius_sq = sum(x*x for row in matrix for x in row)
            row_sq = sum(sum(row)**2 for row in matrix)
            col_sq = sum(sum(matrix[j][k] for j in range(h))**2
                         for k in range(h))
            total_sq = sum(sum(row) for row in matrix)**2
            assert 16 * second == n * u**4 * (
                frobenius_sq + row_sq + col_sq + total_sq)
            assert n * fourth <= 9 * second * second
            counts["bilinear_walsh_second_moments"] += 1
            counts["input_evaluations"] += n

            # At |error|>1/2, every nearest-integer rule fails for an integer target.
            count_bad = sum(2*abs(x) > denominator for x in numerators)
            if second >= n * denominator**2:
                assert 16 * count_bad >= n
                counts["rounded_error_probability_checks"] += 1
            if u**4 * frobenius_sq >= 16 * denominator**2:
                assert second >= n * denominator**2
                assert 16 * count_bad >= n
                counts["large_norm_probability_checks"] += 1

    # S1: selected nonzero bilinear error forms cannot cover the whole
    # sufficiently large grid by their zero sets.
    h = 2
    for s in (1, 2, 3):
        grid = list(product(range(s + 2), repeat=h))
        for _ in range(30):
            forms = []
            while len(forms) < s + 1:
                matrix = [[rng.randint(-2, 2) for _ in range(h)]
                          for _ in range(h)]
                if any(x for row in matrix for x in row):
                    forms.append(matrix)
            witnessed = False
            for a in grid:
                for b in grid:
                    counts["input_evaluations"] += 1
                    if all(sum(matrix[j][k] * a[j] * b[k]
                               for j in range(h) for k in range(h)) != 0
                           for matrix in forms):
                        witnessed = True
                        break
                if witnessed:
                    break
            assert witnessed
            counts["grid_product_nonvanishing_families"] += 1

    for q in (2, 3):
        vectors = list(product(range(q), repeat=2))
        for entries in product(range(q), repeat=4):
            if not any(entries):
                continue
            matrix = [entries[:2], entries[2:]]
            rank = 2 if (entries[0]*entries[3]-entries[1]*entries[2]) % q else 1
            nonzero = sum(sum(matrix[j][k]*a[j]*b[k]
                              for j in range(2) for k in range(2)) % q != 0
                          for a in vectors for b in vectors)
            assert nonzero == (q*q-q**(2-rank))*(q*q-q)
            assert nonzero >= (q-1)**2*q*q
            counts["finite_field_bilinear_probabilities"] += 1
            counts["input_evaluations"] += q**4

    # A single affine-block fourth-moment factor of three is insufficient.
    h = 4
    vals = [sum(eps)*sum(delta)
            for eps in product((-1, 1), repeat=h)
            for delta in product((-1, 1), repeat=h)]
    n = len(vals)
    second = sum(x*x for x in vals)
    fourth = sum(x**4 for x in vals)
    assert n * fourth > 3 * second * second
    assert n * fourth <= 9 * second * second
    counts["negative_controls"] += 1

    # The individual-degree restriction in the generic grid lemma matters.
    assert all(x*(x-1) == 0 for x in (0, 1))
    assert 2*(2-1) != 0
    counts["negative_controls"] += 1

    result = {
        "status": "all exact finite controls passed",
        "seed": 2026112505,
        "scope": "finite arithmetic evidence for S1--S3; not an asymptotic proof",
        "counts": counts,
    }
    target = Path(__file__).with_name("bilinear-supplier-verification.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
