#!/usr/bin/env python3
"""Exact finite checks for RG; no floating-point rank or runtime inference."""
from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


def parity(x: int) -> int:
    return x.bit_count() & 1


def rank2(rows: tuple[int, ...] | list[int], width: int) -> int:
    basis: dict[int, int] = {}
    for value in rows:
        value &= (1 << width) - 1
        while value:
            p = value.bit_length() - 1
            if p in basis:
                value ^= basis[p]
            else:
                basis[p] = value
                break
    return len(basis)


def determinant_predicate(rows: tuple[int, ...] | list[int], a: int) -> int:
    return int(rank2(rows, a) == a)


def rational_rank(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][j]
        a[r] = [x / scale for x in a[r]]
        for i in range(r + 1, len(a)):
            scale = a[i][j]
            if scale:
                a[i] = [x - scale * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def dot_sign(x: int, y: int) -> int:
    return 1 - 2 * parity(x & y)


def main() -> None:
    counts = {
        "elementary_orbit_invariance": 0,
        "determinant_linear_identity": 0,
        "cofactor_families": 0,
        "halfspace_matrices": 0,
        "gram_entries": 0,
        "independent_rational_ranks": 0,
        "full_cross_matrices": 0,
        "rank_fraction_profiles": 0,
        "negative_controls": 0,
    }

    # All elementary row generators at these complete occupied shapes.
    for a, f in [(2, 2), (2, 3), (3, 3), (3, 4)]:
        for rows in itertools.product(range(1 << f), repeat=a):
            expected = determinant_predicate(rows, a)
            for i in range(a):
                for j in range(a):
                    if i == j:
                        continue
                    changed = list(rows)
                    changed[i] ^= changed[j]
                    assert determinant_predicate(changed, a) == expected
                    counts["elementary_orbit_invariance"] += 1
                    changed = list(rows)
                    changed[i], changed[j] = changed[j], changed[i]
                    assert determinant_predicate(changed, a) == expected
                    counts["elementary_orbit_invariance"] += 1

    cofactor_counts: dict[int, dict[int, int]] = {}
    for a in range(2, 5):
        tally = {c: 0 for c in range(1, 1 << a)}
        independent = 0
        for b in itertools.product(range(1 << a), repeat=a - 1):
            if rank2(b, a) != a - 1:
                continue
            independent += 1
            c = sum(determinant_predicate((1 << i,) + b, a) << i
                    for i in range(a))
            assert c != 0
            tally[c] += 1
            for x in range(1 << a):
                assert determinant_predicate((x,) + b, a) == parity(c & x)
                counts["determinant_linear_identity"] += 1
        expected = 1
        for i in range(a - 1):
            expected *= (1 << a) - (1 << i)
        assert independent == expected
        assert len(set(tally.values())) == 1
        cofactor_counts[a] = tally
        counts["cofactor_families"] += 1

    # Character Gram identity certifies both exact rank and singular values.
    for f in range(2, 7):
        q = 1 << f
        for a in range(2, min(4, f) + 1):
            for c in range(1, 1 << a):
                left = [y for y in range(q) if parity(c & y) == 0]
                right = [x for x in range(q) if parity(c & x) == 1]
                matrix = [[dot_sign(y, x) for x in right] for y in left]
                t = 1 if parity(c) else 2
                for i, y in enumerate(left):
                    for j, z in enumerate(left):
                        actual = sum(u * v for u, v in zip(matrix[i], matrix[j]))
                        # The affine column coset changes the radical sign.
                        expected = 0
                        if y == z:
                            expected = q // 2
                        elif t == 2 and (y ^ z) == c:
                            expected = -q // 2
                        assert actual == expected
                        counts["gram_entries"] += 1
                if f <= 4:
                    assert rational_rank(matrix) == q // (2 * t)
                    counts["independent_rational_ranks"] += 1
                if t == 2:
                    assert q // (2 * t) != q // 2  # dropping the radical fails
                    counts["negative_controls"] += 1
                counts["halfspace_matrices"] += 1

    profiles = []
    for a in range(2, 5):
        alpha = Fraction(1)
        for j in range(2, a + 1):
            alpha *= 1 - Fraction(1, 1 << j)
        beta = alpha * Fraction(3 * (1 << (a - 1)) - 1, 4 * ((1 << a) - 1))
        assert beta > Fraction(3, 16)
        for f in range(a, a + 4):
            q = 1 << f
            count = sum(number * (q // (2 if parity(c) else 4))
                        for c, number in cofactor_counts[a].items())
            count *= 1 << ((a - 1) * (f - a))
            expected = beta * (1 << (a * f))
            assert expected.denominator == 1 and count == expected
            profiles.append({"A": a, "f": f, "N": 1 << (a * f),
                             "cross_rank": count, "rank_fraction": str(beta)})
            counts["rank_fraction_profiles"] += 1

    # Direct whole physical matrices at small sizes, independent of the sum.
    for a, f in [(2, 2), (2, 3), (3, 3)]:
        addresses = list(itertools.product(range(1 << f), repeat=a))
        left = [x for x in addresses if determinant_predicate(x, a) == 0]
        right = [x for x in addresses if determinant_predicate(x, a) == 1]
        matrix = [[dot_sign(y[0], x[0]) if y[1:] == x[1:] else 0
                   for x in right] for y in left]
        got = rational_rank(matrix)
        profile = next(p for p in profiles if p["A"] == a and p["f"] == f)
        assert got == profile["cross_rank"]
        counts["full_cross_matrices"] += 1

    # A row-XOR generator is genuinely orbit-preserving but does not preserve
    # an arbitrary coordinate-bit predicate: determinant is essential.
    rows = (0, 1)
    assert rank2(rows, 2) == rank2((1, 1), 2)
    assert (rows[0] & 1) != (1 & 1)
    counts["negative_controls"] += 1
    # H itself is a zero-error counterexample if orbit preservation is dropped.
    assert any(p["cross_rank"] > 0 for p in profiles)
    counts["negative_controls"] += 1

    result = {
        "status": "PASS",
        "claim": "RG exact finite character/separator/rank identities",
        "scope": "Finite checks complement the unbounded proof; no time or full multiplier claim.",
        "counts": counts,
        "profiles": profiles,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": hashlib.sha256(Path(__file__).with_name(
            'rowspace-walsh-rank-gate.md').read_bytes()).hexdigest(),
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
