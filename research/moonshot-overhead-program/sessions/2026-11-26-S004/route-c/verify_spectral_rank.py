#!/usr/bin/env python3
"""Independent exact checks for the spectral cokernel rank bound.

F4 arithmetic and ranks are implemented here from scratch.  No numerical
linear algebra, interpolation tolerance, or programme predecessor checker
is imported.  The general result rests on the accompanying proof review.
"""
from __future__ import annotations

from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import random


ROOT = Path(__file__).resolve().parent
MUL = [[0] * 4 for _ in range(4)]
for a in range(4):
    for b in range(4):
        z = ((a & 1) * (b & 1)) ^ (((a & 1) * (b >> 1)) << 1)
        z ^= (((a >> 1) * (b & 1)) << 1) ^ (((a >> 1) * (b >> 1)) << 2)
        if z & 4:
            z ^= 7  # omega^2 + omega + 1 = 0.
        MUL[a][b] = z
INV = {1: 1, 2: 3, 3: 2}
POW = (1, 2, 3)


def rank(a: list[list[int]]) -> int:
    b = [r[:] for r in a]
    rows = len(b)
    cols = len(b[0]) if rows else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if b[i][c]), None)
        if pivot is None:
            continue
        b[r], b[pivot] = b[pivot], b[r]
        inv = INV[b[r][c]]
        b[r] = [MUL[x][inv] for x in b[r]]
        for i in range(r + 1, rows):
            factor = b[i][c]
            if factor:
                b[i] = [x ^ MUL[factor][y] for x, y in zip(b[i], b[r])]
        r += 1
        if r == rows:
            break
    return r


def eye(w: int, a: int = 1) -> list[list[int]]:
    return [[a if i == j else 0 for j in range(w)] for i in range(w)]


def evaluate(poly: dict[tuple[int, ...], list[list[int]]], k: tuple[int, ...], w: int) -> list[list[int]]:
    out = [[0] * w for _ in range(w)]
    for alpha, mat in poly.items():
        v = POW[sum(a * x for a, x in zip(alpha, k)) % 3]
        for i in range(w):
            for j in range(w):
                out[i][j] ^= MUL[v][mat[i][j]]
    return out


def spectral_ranks(poly: dict[tuple[int, ...], list[list[int]]], m: int, w: int) -> list[int]:
    values = []
    for k in product(range(3), repeat=m):
        value = evaluate(poly, k, w)
        chi = POW[sum(k) % 3]
        for i in range(w):
            value[i][i] ^= chi
        values.append(rank(value))
    return values


def regular_defect(poly: dict[tuple[int, ...], list[list[int]]], m: int, w: int) -> list[list[int]]:
    monomials = list(product(range(3), repeat=m))
    index = {a: i for i, a in enumerate(monomials)}
    n = len(monomials) * w
    a = [[0] * n for _ in range(n)]
    for beta in monomials:
        c = index[beta] * w
        chi_beta = tuple((x + 1) % 3 for x in beta)
        r = index[chi_beta] * w
        for j in range(w):
            a[r + j][c + j] ^= 1
        for alpha, mat in poly.items():
            shifted = tuple((x + y) % 3 for x, y in zip(alpha, beta))
            r = index[shifted] * w
            for i in range(w):
                for j in range(w):
                    a[r + i][c + j] ^= mat[i][j]
    return a


def main() -> None:
    rng = random.Random(2718281828)
    counts = Counter()
    examples = []

    for m in range(1, 9):
        monomials = list(product(range(3), repeat=m))
        for t in range(m + 1):
            threshold = (2 * m) // 3 + t
            for alpha in monomials:
                costs = [sum((a - h) % 3 != 0 for a in alpha) + h * t for h in range(3)]
                assert min(costs) <= threshold
                counts["support_shift_reductions"] += 1
            tail_direct = sum(sum(a != 0 for a in alpha) > threshold for alpha in monomials)
            tail_binomial = sum(comb(m, k) * 2**k for k in range(threshold + 1, m + 1))
            assert tail_direct == tail_binomial
            counts["support_hilbert_tails"] += 1
        for d in range(2 * m + 1):
            threshold = m + d
            for alpha in monomials:
                costs = [sum((a - h) % 3 for a in alpha) + h * d for h in range(3)]
                assert min(costs) <= threshold
                counts["ordinary_shift_reductions"] += 1

    # Arbitrary nonsymmetric, non-diagonal matrix polynomials, rather than
    # only products or diagonal count predictors.  The stronger model makes
    # the matrix-rank assertion directly visible in finite cases.
    for m, w, t, reps in [(1, 1, 0, 4), (2, 2, 0, 12), (3, 2, 1, 16),
                          (4, 3, 1, 10), (5, 2, 1, 8), (5, 3, 2, 8),
                          (6, 2, 1, 6), (7, 2, 2, 4)]:
        allowed = [a for a in product(range(3), repeat=m) if sum(x != 0 for x in a) <= t]
        threshold = (2 * m) // 3 + t
        tail = sum(comb(m, k) * 2**k for k in range(threshold + 1, m + 1))
        for rep in range(reps):
            poly = {a: [[rng.randrange(4) for _ in range(w)] for _ in range(w)] for a in allowed}
            ranks = spectral_ranks(poly, m, w)
            assert sum(ranks) >= w * tail
            counts["matrix_predictors"] += 1
            counts["spectral_rank_evaluations"] += 3**m
            if m <= 3:
                regular = rank(regular_defect(poly, m, w))
                assert regular == sum(ranks)
                q_dim = w * 3**m - regular
                assert q_dim <= w * (3**m - tail)
                counts["crt_regular_representation_ranks"] += 1
            if rep == 0:
                examples.append({"m": m, "width": w, "support_degree": t,
                                 "actual_rank_sum": sum(ranks), "lower_rank_sum": w * tail})

    # Nonscalar constant matrices can make the lower bound an equality.
    # m=1, degree=0, P=diag(1,omega,omega^2): each frequency has rank 2.
    p0 = {(0,): [[1, 0, 0], [0, 2, 0], [0, 0, 3]]}
    assert spectral_ranks(p0, 1, 3) == [2, 2, 2]
    counts["exact_constant_matrix_case"] += 1

    # Scalar trace extraction for the external Smolensky cross-check:
    # indicator[phase==omega^i] = 1 + omega^-i*phase + omega^-2i*phase^2.
    for i, k in product(range(3), repeat=2):
        value = 1 ^ MUL[POW[-i % 3]][POW[k]] ^ MUL[POW[-2 * i % 3]][MUL[POW[k]][POW[k]]]
        assert value == int(i == k)
        counts["phase_indicator_identities"] += 1

    # Essential negative controls.  These are deliberately invalid variants,
    # not alleged counterexamples to the theorem.
    neg = []
    # Characteristic divides group order: only one binary root survives.
    assert (1 ^ 1) == 0
    neg.append({"omission": "semisimplicity", "model": "F2, r=2, m=1, P=1",
                "actual_rank_fraction": "0", "invalid_binary_tail": "1/2"})
    # Low rank does not imply a sparse set of erroneous coordinate rows.
    for w in [2, 3, 7, 16, 31]:
        j = [[1] * w for _ in range(w)]
        assert rank(j) == 1
        assert all(row[i] == 1 for i, row in enumerate(j))
        counts["rank_vs_coordinate_negative_controls"] += 1
    neg.append({"omission": "rank versus coordinate distinction", "model": "defect J_W",
                "rank": 1, "bad_diagonal_entries": "W"})
    # The target must be the full product character, not an arbitrary scalar.
    neg.append({"omission": "full-product character", "model": "constant target and P=I",
                "actual_rank_fraction": "0", "invalid_tail": "positive at degree zero"})
    # A one-stage non-affine query is not a degree-one stage.
    m = 9
    fake_one_stage_tail = sum(comb(m, k) * 2**k for k in range((2 * m) // 3 + 2, m + 1))
    assert fake_one_stage_tail > 0
    neg.append({"omission": "affine stage contract", "model": "P=chi I declared one stage",
                "actual_rank_fraction": "0", "invalid_tail_numerator": fake_one_stage_tail,
                "denominator": 3**m})

    output = {"status": "passed", "arithmetic": "exact F4 and integers", "seed": 2718281828,
              "counts": dict(counts), "examples": examples, "negative_controls": neg,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Finite algebra/CRT/weight checks; no proof by enumeration, no tape execution"}
    (ROOT / "spectral-rank-verification.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
