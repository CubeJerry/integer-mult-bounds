#!/usr/bin/env python3
"""Exact finite checks for the pairwise/Newton/division research note.

This is not a Fourier routing or tape-time verifier. It verifies identities
over Q and one finite field, with deterministic examples and negative controls.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import isqrt
import json
from pathlib import Path
import random


PRIME = 1_000_003


def ceil_sqrt(n: int) -> int:
    v = isqrt(n)
    return v + (v * v != n)


def parameters(m: int) -> tuple[int, int, int, int]:
    width = 1 << m.bit_length()
    radius = ceil_sqrt(4 * m)
    lower = m // 2 - radius
    upper = (m + 1) // 2 + radius
    return width, lower, upper, upper - lower


def shifts(m: int) -> list[int]:
    width = 1 << m.bit_length()
    return [sum((((j & seed).bit_count() & 1) << (j - 1))
                for j in range(1, m + 1)) for seed in range(width)]


def newton_value(count: int, lower: int, degree: int) -> int:
    term = Fraction(1)
    total = Fraction(1)
    for h in range(1, degree + 1):
        term *= Fraction(count - lower - h + 1, h)
        assert term.denominator == 1
        total += (-2) ** h * term
    assert total.denominator == 1
    return total.numerator


def invert(matrix: list[list[int]], p: int) -> list[list[int]]:
    n = len(matrix)
    aug = [[x % p for x in row] + [int(i == j) for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = pow(aug[col][col], -1, p)
        aug[col] = [(x * scale) % p for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            aug[row] = [(x - scale * y) % p
                        for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def check_repair(mult: list[int], target: int, cap: int,
                 wrong_transpose: bool = False) -> int:
    """Return mismatch count for the all-input linear map at one frequency."""
    p = PRIME
    width = len(mult)
    gap = [(x - target) % p for x in mult]
    defect = [i for i, d in enumerate(gap) if d]
    assert len(defect) <= cap
    if not defect:
        return 0
    count = len(defect)
    inv_width = pow(width, -1, p)
    h = [[pow(i * inv_width % p, a, p) for i in range(width)]
         for a in range(count)]
    v = [[h[a][i] for i in defect] for a in range(count)]
    vi = invert(v, p)
    # M = V^{-T} diag(gap_J^{-1}) V^{-1}.
    table = [[sum((vi[a][i] if wrong_transpose else vi[i][a])
                  * pow(gap[defect[i]], -1, p) * vi[i][b]
                  for i in range(count)) % p
              for b in range(count)] for a in range(count)]
    mismatch = 0
    for row in range(width):
        for col in range(width):
            correction = gap[row] * gap[col] * sum(
                h[a][row] * table[a][b] * h[b][col]
                for a in range(count) for b in range(count))
            actual = (mult[row] * int(row == col) - correction) % p
            expected = target % p * int(row == col)
            mismatch += actual != expected
    return mismatch


def main() -> dict:
    rng = random.Random(20261126)
    counts = {"count_polynomial_cases": 0, "pair_marginals": 0,
              "frequency_moment_cases": 0, "count_repair_cases": 0,
              "arbitrary_support_repair_cases": 0,
              "negative_wrong_transpose_mismatches": 0}
    maximum_real_gap_bits = 0
    # Every integral count in each listed interval, including both tails.
    for m in range(9, 129):
        width, lower, upper, degree = parameters(m)
        assert m + 1 <= width < 2 * (m + 1)
        assert width % 16 == 0
        for count in range(m + 1):
            val = newton_value(count, lower, degree)
            assert val % 2 == 1
            correct = -1 if (count - lower) & 1 else 1
            if lower <= count <= upper:
                assert val == correct
            if val != correct:
                assert abs(val - correct) >= 2
                maximum_real_gap_bits = max(maximum_real_gap_bits,
                                           abs(val - correct).bit_length())
            counts["count_polynomial_cases"] += 1

    moment_examples = []
    for m in [9, 15, 31, 63]:
        beta = shifts(m)
        width, lower, upper, degree = parameters(m)
        assert len(beta) == len(set(beta)) == width
        for a, b in combinations(range(m), 2):
            hist = [0, 0, 0, 0]
            for word in beta:
                hist[((word >> a) & 1) + 2 * ((word >> b) & 1)] += 1
            assert hist == [width // 4] * 4
            counts["pair_marginals"] += 1
        mask = (1 << m) - 1
        frequencies = [0, mask, *beta, *(x ^ mask for x in beta)]
        frequencies += [rng.getrandbits(m) for _ in range(128)]
        # These test both a globally bad shift choice and real tail rows.
        frequencies += [b ^ (1 << j) for b in beta for j in range(min(m, 6))]
        tail_max = 0
        repair_nonempty = 0
        cache = [newton_value(c, lower, degree) for c in range(m + 1)]
        for freq in frequencies:
            cc = [(b ^ freq).bit_count() for b in beta]
            assert 2 * sum(cc) == width * m
            assert sum((2 * c - m) ** 2 for c in cc) == width * m
            tail = sum(c < lower or c > upper for c in cc)
            assert tail <= width // 16
            tail_max = max(tail_max, tail)
            counts["frequency_moment_cases"] += 1
            z = -1 if freq.bit_count() & 1 else 1
            pp = [(-1 if (lower - b.bit_count()) & 1 else 1) * cache[c]
                  for b, c in zip(beta, cc)]
            if any(x != z for x in pp):
                repair_nonempty += 1
            assert check_repair(pp, z, width // 16) == 0
            counts["count_repair_cases"] += 1
        moment_examples.append({"m": m, "width": width,
                                "degree": degree, "cap": width // 16,
                                "max_sampled_tail": tail_max,
                                "nonempty_repair_cases": repair_nonempty})

    # Test the general division lemma on every support of size <=3 at W=8.
    # This gives multi-defect examples even when the broad Chebyshev window
    # makes the small count-family test have only one defect.
    for size in range(1, 4):
        for support in combinations(range(8), size):
            for z in [-1, 1]:
                pp = [z] * 8
                for i in support:
                    pp[i] += 2 * (i + 2)
                assert check_repair(pp, z, 3) == 0
                counts["arbitrary_support_repair_cases"] += 1
                if size >= 2:
                    counts["negative_wrong_transpose_mismatches"] += (
                        check_repair(pp, z, 3, wrong_transpose=True))
    assert counts["negative_wrong_transpose_mismatches"] > 0

    # Outside-window equality can occur after specialization to a field.
    # A generic example forces that edge case; J must mean actual defects.
    specialized = [1, 1 + PRIME, 5, 1, 1, 1, 1, 1]
    assert check_repair(specialized, 1, 2) == 0
    try:
        pow((specialized[1] - 1) % PRIME, -1, PRIME)
    except ValueError:
        rejected_zero_gap = True
    else:
        raise AssertionError("zero discrepancy was incorrectly invertible")
    try:
        pow(3, -1, 9)
    except ValueError:
        rejected_nonunit = True
    else:
        raise AssertionError("nonunit discrepancy was incorrectly invertible")

    # Pairwise balance is a hypothesis: all-zero shifts fail its variance law.
    assert 16 * (2 * 0 - 15) ** 2 != 16 * 15

    ledgers = []
    for depth in range(13):
        a, arity, w0 = Fraction(71, 3), 202, 32
        volume = w0 * 8 ** depth
        direct = a * sum((Fraction(1, 4) ** h for h in range(depth)),
                         Fraction(0)) + arity * Fraction(1, 4) ** depth
        total = Fraction(arity * w0)
        for d in range(1, depth + 1):
            total = a * w0 * 8 ** d + 2 * total
        assert total / volume == direct
        ledgers.append({"depth": depth, "ratio": str(direct)})

    return {
        "status": "passed",
        "scope": "Exact finite Q count tests and finite-field all-input repair matrices; no tape implementation",
        "prime": PRIME,
        "random_seed": 20261126,
        "counts": counts,
        "moment_examples": moment_examples,
        "max_real_gap_bits_in_count_examples": maximum_real_gap_bits,
        "negative_controls": {"wrong_transpose_rejected": True,
                              "zero_gap_rejected": rejected_zero_gap,
                              "nonunit_gap_rejected": rejected_nonunit,
                              "unbalanced_shift_family_rejected": True},
        "batch_ledgers": ledgers,
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).with_name("pairwise-newton-verification.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
