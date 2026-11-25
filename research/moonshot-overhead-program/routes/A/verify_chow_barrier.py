#!/usr/bin/env python3
"""Exact small checks for the formal-predictor Chow-compression barrier."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from math import comb


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    a = [[entry % prime for entry in row] for row in matrix]
    if not a:
        return 0
    pivot_row = 0
    for column in range(len(a[0])):
        pivot = next((r for r in range(pivot_row, len(a)) if a[r][column]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        inverse = pow(a[pivot_row][column], -1, prime)
        a[pivot_row] = [(value * inverse) % prime for value in a[pivot_row]]
        for r in range(pivot_row + 1, len(a)):
            coefficient = a[r][column]
            if coefficient:
                a[r] = [(v - coefficient * w) % prime for v, w in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def disjointness_matrix(m: int, degree: int, order: int) -> list[list[int]]:
    left = [sum(1 << i for i in subset) for subset in combinations(range(m), order)]
    right = [sum(1 << i for i in subset) for subset in combinations(range(m), degree - order)]
    return [[int(not (a & b)) for b in right] for a in left]


def sign(exponent: int) -> int:
    return -1 if exponent % 2 else 1


def generalized_binomial(a: int, k: int) -> int:
    answer = Fraction(1)
    for i in range(k):
        answer *= Fraction(a - i, i + 1)
    assert answer.denominator == 1
    return answer.numerator


def predictor(m: int, degree: int, offset: int, beta: int) -> dict[int, Fraction]:
    # Generate the formal multilinear elementary symmetric polynomials in
    # I_j=(1-(-1)^beta_j q_j)/2, truncated only in the auxiliary T degree.
    elementary: list[dict[int, Fraction]] = [{0: Fraction(1)}] + [{} for _ in range(degree)]
    for j in range(m):
        query_sign = sign((beta >> j) & 1)
        for r in range(min(j + 1, degree), 0, -1):
            for mask, coefficient in list(elementary[r - 1].items()):
                elementary[r][mask] = elementary[r].get(mask, Fraction(0)) + coefficient / 2
                changed = mask | (1 << j)
                elementary[r][changed] = elementary[r].get(changed, Fraction(0)) - query_sign * coefficient / 2
    answer: dict[int, Fraction] = {}
    phase = sign(offset - beta.bit_count())
    for r in range(degree + 1):
        weight = phase * sum((-2)**h * generalized_binomial(-offset, h - r) for h in range(r, degree + 1))
        for mask, coefficient in elementary[r].items():
            answer[mask] = answer.get(mask, Fraction(0)) + weight * coefficient
    return {mask: coefficient for mask, coefficient in answer.items() if coefficient}


def main() -> None:
    rank_cases = 0
    for m in range(2, 11):
        for degree in range(1, min(m, 6) + 1):
            for order in range(degree // 2 + 1):
                matrix = disjointness_matrix(m, degree, order)
                assert rank_mod(matrix, 65537) == comb(m, order)
                rank_cases += 1

    modular_negative_controls = 0
    for prime in (3, 5, 7):
        m = prime + 1
        matrix = disjointness_matrix(m, 2, 1)  # J-I, constant eigenvalue p.
        assert rank_mod(matrix, prime) == m - 1
        assert rank_mod(matrix, 65537) == m
        modular_negative_controls += 1

    predictor_cases = 0
    top_coefficients = 0
    phase_negative_controls = 0
    for m in range(2, 8):
        beta_values = {0, (1 << m) - 1, sum(1 << i for i in range(0, m, 2))}
        for degree in range(1, m + 1):
            for offset in (-2, m // 2, m + 2):
                for beta in beta_values:
                    polynomial = predictor(m, degree, offset, beta)
                    phase = sign(offset - beta.bit_count())
                    for subset in combinations(range(m), degree):
                        mask = sum(1 << i for i in subset)
                        expected = phase * sign((mask & beta).bit_count())
                        assert polynomial.get(mask, Fraction(0)) == expected
                        if phase == -1:
                            assert polynomial[mask] != sign((mask & beta).bit_count())
                            phase_negative_controls += 1
                        top_coefficients += 1
                    assert max(mask.bit_count() for mask in polynomial) == degree
                    predictor_cases += 1

    print(json.dumps({
        "status": "passed",
        "full_rank_modular_certificates": rank_cases,
        "odd_characteristic_rank_drop_controls": modular_negative_controls,
        "formal_predictor_cases": predictor_cases,
        "top_degree_coefficients": top_coefficients,
        "missing_phase_negative_controls": phase_negative_controls,
        "scope": "Exact finite algebra checks; formal-polynomial barrier only, no general pencil or tape lower bound.",
    }, indent=2))


if __name__ == "__main__":
    main()
