#!/usr/bin/env python3
"""Exact checks for the published-Gram/count-residue incompatibility.

No outer matrix of dimension 2^((2p-1)^2) is materialized. The proof gives
its rank; one small full-rank principal restriction is also checked modulo
an auxiliary prime, which certifies a rational rank lower bound.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction
from pathlib import Path


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def krawtchouk(h: int, distance: int, weight: int) -> int:
    return sum(
        (-1) ** j * math.comb(weight, j) * math.comb(h - weight, distance - j)
        for j in range(max(0, distance - (h - weight)), min(weight, distance) + 1)
    )


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    rows = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column], -1, prime)
        rows[rank] = [(value * inv) % prime for value in rows[rank]]
        for r in range(rank + 1, len(rows)):
            factor = rows[r][column]
            if factor:
                for c in range(column, len(rows[r])):
                    rows[r][c] = (rows[r][c] - factor * rows[rank][c]) % prime
        rank += 1
        if rank == len(rows):
            break
    return rank


def verify_inner_spectra() -> dict[str, object]:
    coefficients = 0
    rows = []
    for p in range(1, 102):
        h = 2 * p - 1
        for t in range(h + 1):
            value = krawtchouk(h, p, t)
            expected_numerator = (-1) ** ((t + 1) // 2) * math.comb(h, p) * math.comb(p - 1, t // 2)
            assert value * math.comb(h, t) == expected_numerator
            assert value != 0
            coefficients += 1
        if p >= 3 and is_prime(p):
            assert math.comb(h, p) % p == 1
            assert (p * (1 << h) - 2 * h * math.comb(h, p)) % p == 2
            rows.append({"p": p, "h": h, "binary_gram_rank": h * ((1 << h) - 1) + 2})
    character_rows = 0
    for p in (3, 5):
        h = 2 * p - 1
        neighbors = [sum(1 << j for j in bits) for bits in itertools.combinations(range(h), p)]
        for t in range(h + 1):
            character_mask = (1 << t) - 1
            eigenvalue = krawtchouk(h, p, t)
            for x in range(1 << h):
                action = sum((-1) ** (((x ^ y) & character_mask).bit_count()) for y in neighbors)
                expected = eigenvalue * (-1) ** ((x & character_mask).bit_count())
                assert action == expected
                character_rows += 1
    return {"krawtchouk_values_checked": coefficients, "exact_character_row_checks": character_rows, "odd_prime_examples": rows}


def verify_small_outer_rank() -> dict[str, int | str]:
    p = 3
    h = 2 * p - 1
    inner_size = 1 << h
    labels = [(0,) * h]
    for coordinate in range(h):
        for inner_word in range(1, inner_size):
            label = [0] * h
            label[coordinate] = inner_word
            labels.append(tuple(label))
    auxiliary_prime = 101
    two_over_p = 2 * pow(p, -1, auxiliary_prime)
    minus_block = []
    for v in labels:
        row = []
        for w in labels:
            far_count = sum((x ^ y).bit_count() == p for x, y in zip(v, w))
            row.append((1 - two_over_p * far_count) % auxiliary_prime)
        minus_block.append(row)
    rank = rank_mod(minus_block, auxiliary_prime)
    assert rank == 1 + h * (inner_size - 1)
    assert len(labels) == rank
    return {
        "p": p,
        "auxiliary_prime": auxiliary_prime,
        "minus_principal_matrix_side": len(labels),
        "minus_principal_rank": rank,
        "plus_block_rank": 1,
        "certified_total_rank_lower_bound": rank + 1,
        "proof_total_rank_upper_bound": h * (inner_size - 1) + 2,
        "full_outer_label_count_not_materialized": inner_size ** h,
        "interpretation": "nonzero modular minor gives rational rank lower bound; tensor proof gives matching upper bound",
    }


def residue_masses(m: int, p: int) -> list[int]:
    masses = [0] * (2 * p)
    weight = 1
    for k in range(m + 1):
        masses[k % (2 * p)] += weight
        if k < m:
            weight = weight * (m - k) // (k + 1)
    assert sum(masses) == 1 << m
    return masses


def verify_residue_agreement() -> dict[str, object]:
    examples = []
    functions = 0
    for p in (3, 5, 7, 11, 13, 17):
        for m in (p * p, p * p + 1, 2 * p * p, 4 * p * p):
            masses = residue_masses(m, p)
            best_agreement = sum(max(masses[r], masses[r + p]) for r in range(p))
            differences = [masses[r] - masses[r + p] for r in range(p)]
            l1 = sum(abs(d) for d in differences)
            assert 2 * best_agreement == (1 << m) + l1
            assert l1 * l1 <= p * sum(d * d for d in differences)
            failure = Fraction((1 << m) - best_agreement, 1 << m)
            assert failure > Fraction(1, 4)
            if p <= 7:
                best_exhaustive = max(sum(masses[r + p * ((mask >> r) & 1)] for r in range(p)) for mask in range(1 << p))
                assert best_exhaustive == best_agreement
                functions += 1 << p
            examples.append({"p": p, "m": m, "best_failure_decimal": float(failure), "failure_gt_one_quarter": True})
    # Characteristic two is an intentional exclusion: the multiplier is constant.
    assert all(pow(-1, k, 2) == 1 for k in range(100))
    # The integral divided power remembers more than the count's field residue.
    for p in (3, 5, 7, 11):
        assert 0 % p == p % p
        assert math.comb(0, p) % p != math.comb(p, p) % p
    return {"count_residue_functions_exhausted": functions, "examples": examples, "negative_controls": ["characteristic two excluded", "divided powers distinguish equal count residues"]}


def verify_contraction_implications() -> dict[str, int]:
    checks = 0
    feasible = 0
    for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        h = 2 * p - 1
        reserves = h * ((1 << h) - 1)
        assert 2 * reserves >= 2 * h * h > p * p
        for alpha_numerator, alpha_denominator in ((3, 4), (7, 8), (15, 16)):
            for exponent in range(1, 257):
                m = 1 << exponent
                reserve_contracts = (2 * reserves) ** alpha_denominator < (1 << (alpha_numerator * exponent))
                if reserve_contracts:
                    assert m > p * p
                    assert (h * (1 << h)) ** alpha_denominator < (1 << (alpha_numerator * exponent))
                    feasible += 1
                checks += 1
    return {"necessary_budget_cases_checked": checks, "feasible_reserve_cases_checked": feasible}


def main() -> None:
    report = {
        "status": "pass",
        "python": platform.python_version(),
        "scope": "exact finite checks of a source-specific rank and finite-characteristic obstruction; no general multiplication lower bound",
        "inner_spectra": verify_inner_spectra(),
        "outer_rank_certificate": verify_small_outer_rank(),
        "residue_agreement": verify_residue_agreement(),
        "contraction": verify_contraction_implications(),
    }
    path = Path(__file__).with_name("interchange-verification.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "scope": report["scope"],
        "krawtchouk_values_checked": report["inner_spectra"]["krawtchouk_values_checked"],
        "character_row_checks": report["inner_spectra"]["exact_character_row_checks"],
        "outer_rank_certificate": report["outer_rank_certificate"],
        "residue_functions_exhausted": report["residue_agreement"]["count_residue_functions_exhausted"],
        "contraction": report["contraction"],
    }, indent=2))


if __name__ == "__main__":
    main()
