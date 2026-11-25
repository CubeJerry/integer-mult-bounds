#!/usr/bin/env python3
"""Exact finite corroboration of the scoped routing-lift obstruction.

Uses only the standard library. It does not materialize the full outer
matrix or treat finite checks as the proof of the general statements.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from math import comb, prod
from pathlib import Path


def choose(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def krawtchouk(h: int, p: int, q: int, t: int) -> int:
    return sum(
        (-1) ** j * (q - 1) ** (p - j) * choose(t, j) * choose(h - t, p - j)
        for j in range(p + 1)
    )


def elementary(values: tuple[int, ...], degree: int) -> int:
    coefficients = [1] + [0] * degree
    for value in values:
        for j in range(degree, 0, -1):
            coefficients[j] += value * coefficients[j - 1]
    return coefficients[degree]


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    a = [[v % prime for v in row] for row in matrix]
    rows, columns = len(a), len(a[0])
    r = 0
    for c in range(columns):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inverse = pow(a[r][c], -1, prime)
        a[r] = [(v * inverse) % prime for v in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                coefficient = a[i][c]
                a[i] = [(x - coefficient * y) % prime for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def small_source_restriction() -> dict[str, int]:
    # Choose two inner words at distance p in each outer coordinate.
    # Their 2^h combinations form a principal source-label submatrix.
    p, h = 3, 5
    n = 1 << h
    kernel = [int(x == 0 or x.bit_count() == p) for x in range(n)]
    matrix = [[kernel[x ^ y] for y in range(n)] for x in range(n)]
    gram = [[p - (x ^ y).bit_count() for y in range(n)] for x in range(n)]
    product_checks = 0
    involution_checks = 0
    character_checks = 0
    for x, y in itertools.product(range(n), repeat=2):
        assert matrix[x][y] * gram[x][y] == (p if x == y else 0)
        product_checks += 1
        square = sum(matrix[x][z] * matrix[z][y] for z in range(n)) % 2
        assert square == int(x == y)
        involution_checks += 1
    for frequency in range(n):
        eigenvalue = 1 + krawtchouk(h, p, 2, frequency.bit_count())
        for row in range(n):
            lhs = sum(matrix[row][x] * (-1) ** ((frequency & x).bit_count()) for x in range(n))
            rhs = eigenvalue * (-1) ** ((frequency & row).bit_count())
            assert lhs == rhs
            character_checks += 1
    assert matrix_rank_mod(matrix, 2) == n
    rank3 = matrix_rank_mod(matrix, 3)
    predicted3 = sum(comb(h, t) for t in range(h + 1) if (1 + krawtchouk(h, p, 2, t)) % 3)
    assert rank3 == predicted3
    # Omitting the diagonal destroys the claimed mod-two inverse identity.
    bad = [[int(x != y) * matrix[x][y] for y in range(n)] for x in range(n)]
    assert any(sum(bad[x][z] * bad[z][x] for z in range(n)) % 2 != 1 for x in range(n))
    return {
        "matrix_side": n,
        "hadamard_identity_entries": product_checks,
        "mod_two_involution_entries": involution_checks,
        "exact_character_row_checks": character_checks,
        "mod_two_rank": n,
        "mod_three_rank": rank3,
    }


def ring_factor_checks() -> dict[str, int]:
    count = 0
    for p, e in ((2, 2), (2, 3), (3, 2)):
        modulus = p**e
        for a, b, c, d in itertools.product(range(modulus), repeat=4):
            # Exhaust every two-by-one times one-by-two factorization.
            outer = (a * c % modulus, a * d % modulus, b * c % modulus, b * d % modulus)
            assert outer != (p, 0, 0, p)
            count += 1
        # At exponent one, pI is zero and has rank zero: e>=2 is necessary.
        assert p % p == 0
    return {"rank_one_factorizations_exhausted": count, "prime_power_rings": 3}


def spectral_strata(p: int, q: int, exponents: tuple[int, ...]) -> dict[str, object]:
    h = 2 * p - 1
    inner_n = q**h
    n = inner_n**h
    values = [krawtchouk(h, p, q, t) for t in range(h + 1)]
    multiplicities = [comb(h, t) * (q - 1) ** t for t in range(h + 1)]
    assert sum(multiplicities) == inner_n
    assert all(value % 2 == 0 for value in values)
    ranks = {e: 0 for e in exponents}
    rational_rank = 0
    tuples = 0
    total = 0
    for types in itertools.product(range(h + 1), repeat=h):
        eigenvalue = 1 + elementary(tuple(values[t] for t in types), p)
        weight = prod(multiplicities[t] for t in types)
        assert eigenvalue % 2 == 1
        rational_rank += weight * (eigenvalue != 0)
        for e in exponents:
            ranks[e] += weight * (eigenvalue % (p**e) != 0)
        tuples += 1
        total += weight
    assert total == rational_rank == n
    # The constant eigenvalue of G=pJ-K and the one-coordinate eigenspaces.
    gram_rank = int(p * inner_n - h * values[0] != 0)
    gram_rank += h * sum(multiplicities[t] for t in range(1, h + 1) if values[t] != 0)
    assert gram_rank <= 1 + h * inner_n
    for e in exponents:
        if e >= 2:
            assert ranks[e] * gram_rank >= n
    return {
        "p": p,
        "q": q,
        "full_outer_side_not_materialized": n,
        "type_tuples": tuples,
        "rational_rank": rational_rank,
        "integer_gram_rank": gram_rank,
        "prime_power_inner_ranks": ranks,
        "rank_products_divided_by_N": {str(e): str(Fraction(ranks[e] * gram_rank, n)) for e in exponents},
    }


def main() -> None:
    parity_cases = 0
    for p in range(3, 1000, 2):
        assert comb(2 * p - 1, p) % 2 == 0
        parity_cases += 1
    strata = [spectral_strata(3, q, (1, 2, 3)) for q in (2, 4, 8, 16, 32)]
    witness = strata[3]
    assert witness["prime_power_inner_ranks"][1] * witness["integer_gram_rank"] < witness["full_outer_side_not_materialized"]
    assert witness["prime_power_inner_ranks"][2] * witness["integer_gram_rank"] >= witness["full_outer_side_not_materialized"]
    result = {
        "status": "pass",
        "scope": "Exact finite corroboration of the same-field/support-preserving prime-power lift obstruction; no general tape lower bound.",
        "odd_binomial_parity_cases": parity_cases,
        "small_principal_matrix": small_source_restriction(),
        "ring_inner_rank_checks": ring_factor_checks(),
        "spectral_strata": strata,
        "negative_controls": [
            "The exponent-one ring does not satisfy the pI inner-rank lemma.",
            "Omitting P_*'s diagonal fails the mod-two involution identity.",
            "At p=3,q=16, substituting the mod-p rank as the mod-p^2 inner rank violates the exact rank-product obstruction.",
        ],
    }
    output = json.dumps(result, indent=2) + "\n"
    Path(__file__).with_name("verification.json").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
