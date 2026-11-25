#!/usr/bin/env python3
"""Exact finite checks for the explicit 2-power cyclotomic inverses.

This checks ring identities and the symbolic dimension majorants. It is not
an implementation or test of the complete tape multiplication algorithm.
"""

from __future__ import annotations

import json
from math import gcd


def times_power(poly: list[int], exponent: int) -> list[int]:
    """Multiply modulo Y^d + 1, where d is the coefficient-vector length."""
    d = len(poly)
    answer = [0] * d
    for i, coefficient in enumerate(poly):
        quotient, residue = divmod(i + exponent, d)
        answer[residue] += coefficient * (-1 if quotient & 1 else 1)
    return answer


def times_one_minus_power(poly: list[int], exponent: int) -> list[int]:
    shifted = times_power(poly, exponent)
    return [a - b for a, b in zip(poly, shifted)]


def main() -> None:
    inverse_cases = 0
    reductions = 0
    negative_controls = 0
    for root_order in (4, 8, 16, 32, 64, 128):
        d = root_order // 2
        for exponent in range(1, root_order):
            order = root_order // gcd(exponent, root_order)
            numerator = [1] + [0] * (d - 1)
            for odd in range(3, order, 2):
                numerator = times_one_minus_power(numerator, exponent * odd)
            product = times_one_minus_power(numerator, exponent)
            assert product == [2] + [0] * (d - 1)
            assert sum(abs(a) for a in numerator) <= 2 ** (d - 1)
            inverse_cases += 1
            for prime in (3, 5, 7, 11, 17):
                half = pow(2, -1, prime)
                reduced = [(a * half) % prime for a in numerator]
                modular_product = [a % prime for a in times_one_minus_power(reduced, exponent)]
                assert modular_product == [1] + [0] * (d - 1)
                reductions += 1
            # Omitting the factor 1/2 must fail in odd characteristic.
            assert [a % 7 for a in product] != [1] + [0] * (d - 1)
            negative_controls += 1

    dimension_cases = 0
    for m in range(2, 257):
        for degree in (2, max(2, m // 2), m):
            log_b = (degree - 1).bit_length()
            b = 1 << log_b
            assert degree <= b <= 2 * m
            log_dimension_bound = (1 << m) * log_b
            assert log_dimension_bound <= 1 << (2 * m)
            assert m + log_dimension_bound <= 1 << (2 * m + 1)
            dimension_cases += 1

    print(json.dumps({
        "status": "passed",
        "cyclotomic_inverse_cases": inverse_cases,
        "odd_characteristic_reductions": reductions,
        "negative_controls_missing_half": negative_controls,
        "symbolic_dimension_cases": dimension_cases,
        "scope": "Exact finite ring identities and symbolic bounds; no full tape implementation.",
    }, indent=2))


if __name__ == "__main__":
    main()
