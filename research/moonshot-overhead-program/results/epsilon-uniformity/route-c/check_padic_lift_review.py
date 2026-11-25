#!/usr/bin/env python3
"""Independent finite checks of the p-adic obstruction's displayed identities.

These do not compute the astronomical full label matrix or prove factor rank.
"""

from itertools import product
from math import comb, gcd
import json


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def inner_eigenvalue(p, q, weight):
    h = 2 * p - 1
    return sum(
        (-1) ** j * (q - 1) ** (p - j)
        * choose(weight, j) * choose(h - weight, p - j)
        for j in range(p + 1)
    )


def main():
    spectral_cases = 0
    fractions = 0
    for p in (3, 5, 7, 11, 17):
        h = 2 * p - 1
        c = comb(h, p)
        beta = comb(h - 1, p - 1)
        assert c % (p * p) == 1
        assert beta % p == 0 and beta % (p * p) != 0
        assert (2 * p - 1) * beta == p * c
        for q in (2, 4, 5, 8, 16, 31, 2 * h * h):
            if gcd(p, q) != 1:
                continue
            a = inner_eigenvalue(p, q, p - 1)
            b = inner_eigenvalue(p, q, h)
            assert b == -c
            assert (1 + a - q ** p) % p == 0
            # Direct elementary-symmetric evaluation, without replacing b by -1.
            lam = 1 + comb(h - 1, p) * b ** p
            lam += a * comb(h - 1, p - 1) * b ** (p - 1)
            assert lam % p == 0
            assert lam % (p * p) != 0
            assert (lam // p + q ** p) % p == 0
            # Reduction mod p is intentionally blind to this block.
            assert lam % p == 0
            spectral_cases += 1
            if q >= 2 * h * h:
                multiplicity = h * comb(h, p - 1) * (q - 1) ** (h * h - p)
                total = q ** (h * h)
                assert multiplicity * q ** p >= total
                assert 2 * (q - 1) ** h >= q ** h
                m = 2 * ((q - 1) ** h - 1) + 1
                assert m > 2 * ((q - 1) ** h - 1)
                assert q ** h < 2 * m
                fractions += 1

    # Full inner matrix at p=3,q=2: verify each Walsh character eigenvector.
    p, q, h = 3, 2, 5
    words = range(1 << h)
    neighbours = {
        x: [y for y in words if (x ^ y).bit_count() == p] for x in words
    }
    character_equations = 0
    for character in words:
        lam = inner_eigenvalue(p, q, character.bit_count())
        for x in words:
            lhs = sum((-1) ** ((character & y).bit_count()) for y in neighbours[x])
            rhs = lam * (-1) ** ((character & x).bit_count())
            assert lhs == rhs
            character_equations += 1

    # A focused non-field negative control: rank over F_3 is zero, but the
    # two-by-two 3I block over Z/9 cannot factor through a single column.
    tested_factor_pairs = 0
    for u0, u1, v0, v1 in product(range(9), repeat=4):
        entries = (u0 * v0 % 9, u0 * v1 % 9, u1 * v0 % 9, u1 * v1 % 9)
        assert entries != (3, 0, 0, 3)
        tested_factor_pairs += 1

    polynomial_values = 0
    for p in (3, 5, 7, 11, 17):
        for x in range(2 * p):
            value = (1 - x ** (p - 1)) ** 2 % (p * p)
            assert value == int(x in (0, p))
            polynomial_values += 1

    print(json.dumps({
        "scope": "Exact finite checks of spectral formulas, fractions and polynomial values; the full label matrix and universal factor-rank theorem are not computed.",
        "spectral_parameter_cases": spectral_cases,
        "large_q_fraction_cases": fractions,
        "full_inner_character_equations": character_equations,
        "rank_one_factor_pairs_excluded_mod_9": tested_factor_pairs,
        "polynomial_value_cases": polynomial_values,
    }, indent=2))


if __name__ == "__main__":
    main()
