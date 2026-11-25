#!/usr/bin/env python3
"""Exact finite checks for active query volume and rational fractions."""
from __future__ import annotations

from collections import Counter
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import random

from verify_spectral_rank import MUL as F4_MUL


class Field:
    def __init__(self, order):
        self.order = order

    def add(self, x, y):
        return x ^ y if self.order == 4 else (x + y) % self.order

    def neg(self, x):
        return x if self.order == 4 else -x % self.order

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        return F4_MUL[x][y] if self.order == 4 else x * y % self.order

    def power(self, x, n):
        value = 1
        for _ in range(n):
            value = self.mul(value, x)
        return value

    def inv(self, x):
        assert x
        return self.power(x, self.order - 2)


def eye(n, field):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def rank(matrix, field):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0]) if a else 0
    out = 0
    for col in range(cols):
        pivot = next((i for i in range(out, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[out], a[pivot] = a[pivot], a[out]
        inv = field.inv(a[out][col])
        a[out] = [field.mul(x, inv) for x in a[out]]
        for i in range(out + 1, rows):
            c = a[i][col]
            if c:
                a[i] = [field.sub(x, field.mul(c, y)) for x, y in zip(a[i], a[out])]
        out += 1
        if out == rows:
            break
    return out


def multiply(a, b, field):
    out = [[0] * len(b[0]) for _ in a]
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] = field.add(out[i][j], field.mul(x, y))
    return out


def inverse(a, field):
    n = len(a)
    b = [row[:] + eye(n, field)[i] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if b[i][col]), None)
        if pivot is None:
            return None
        b[col], b[pivot] = b[pivot], b[col]
        inv = field.inv(b[col][col])
        b[col] = [field.mul(x, inv) for x in b[col]]
        for i in range(n):
            if i != col and b[i][col]:
                c = b[i][col]
                b[i] = [field.sub(x, field.mul(c, y)) for x, y in zip(b[i], b[col])]
    return [row[n:] for row in b]


def regular(poly, m, r, rows, cols, field):
    monomials = list(product(range(r), repeat=m))
    index = {alpha: i for i, alpha in enumerate(monomials)}
    out = [[0] * (len(monomials) * cols) for _ in range(len(monomials) * rows)]
    for beta in monomials:
        col = index[beta] * cols
        for alpha, mat in poly.items():
            gamma = tuple((x + y) % r for x, y in zip(alpha, beta))
            row = index[gamma] * rows
            for i in range(rows):
                for j in range(cols):
                    out[row + i][col + j] = field.add(out[row + i][col + j], mat[i][j])
    return out


def mask(m, r, rows, k):
    return [int(sum(x != 0 for x in alpha) <= k)
            for alpha in product(range(r), repeat=m) for _ in range(rows)]


def commutator(a, left_mask, right_mask, field):
    return [[field.mul(field.sub(left_mask[i], right_mask[j]), value)
             for j, value in enumerate(row)] for i, row in enumerate(a)]


def layer(m, r, k):
    return comb(m, k) * (r - 1)**k if 0 <= k <= m else 0


def cut_count(m, r, k):
    # Count n_0>=m-k and n_(r-1)<m-k, and double by symmetry.
    threshold = m - k
    total = 0
    for a in range(max(0, threshold), m + 1):
        for b in range(max(0, min(threshold, m - a + 1))):
            c = m - a - b
            total += comb(m, a) * comb(m - a, b) * (r - 2)**c
    return 2 * total


def evaluate(poly, k, root, rows, cols, field):
    out = [[0] * cols for _ in range(rows)]
    for alpha, mat in poly.items():
        weight = field.power(root, sum(a * b for a, b in zip(alpha, k)) % (3 if field.order == 4 else 2))
        for i in range(rows):
            for j in range(cols):
                out[i][j] = field.add(out[i][j], field.mul(weight, mat[i][j]))
    return out


def main():
    rng = random.Random(1414213562)
    counts = Counter()
    examples = []

    for r in (2, 3):
        for m in range(1, 81):
            k = (m - 1) // 2 if r == 2 else 2 * m // 3
            value = cut_count(m, r, k)
            if r == 2:
                expected = 2**m - (comb(m, m // 2) if m % 2 == 0 else 0)
            else:
                balanced = factorial(m) // factorial(m // 3)**3 if m % 3 == 0 else 0
                expected = 2 * (3**m - balanced) // 3
            assert value == expected
            counts["exact_binary_ternary_cut_formulas"] += 1
        for m in range(1, 9):
            for k in range(m + 1):
                enumerated = sum((sum(a != 0 for a in alpha) <= k) !=
                                 (sum((a + 1) % r != 0 for a in alpha) <= k)
                                 for alpha in product(range(r), repeat=m))
                assert enumerated == cut_count(m, r, k)
                counts["enumerated_cut_counts"] += 1

    for r, field, root in [(2, Field(5), 4), (3, Field(4), 2)]:
        for m in range(1, 4):
            zero = (0,) * m
            monomials = [a for a in product(range(r), repeat=m) if sum(x != 0 for x in a) <= 1]
            for rep in range(3):
                # Two noncommuting nilpotent row coefficients ensure that
                # the inverse can have genuinely higher support degree.
                q = {a: [[0] * 3 for _ in range(3)] for a in monomials}
                q[zero] = eye(3, field)
                for alpha in monomials:
                    q[alpha][0][1] = rng.randrange(field.order)
                    q[alpha][1][2] = rng.randrange(field.order)
                reg = regular(q, m, r, 3, 3, field)
                inv = inverse(reg, field)
                assert inv is not None
                assert multiply(reg, inv, field) == eye(len(reg), field)
                counts["exact_affine_inverse_identities"] += 1
                for k in range(m + 1):
                    projection = mask(m, r, 3, k)
                    c = rank(commutator(reg, projection, projection, field), field)
                    c_inv = rank(commutator(inv, projection, projection, field), field)
                    bound = 3 * (layer(m, r, k) + layer(m, r, k + 1))
                    assert c == c_inv and c <= bound
                    counts["inverse_commutator_rank_equalities"] += 1
                # Genuine changing-width network: inject two occupied rows
                # and one zero row, apply inverse then a constant row map.
                injection = {zero: [[1, 0], [0, 1], [0, 0]]}
                output = {zero: [[1, 0, 1], [0, 1, 1]]}
                inj = regular(injection, m, r, 3, 2, field)
                out = regular(output, m, r, 2, 3, field)
                network = multiply(out, multiply(inv, inj, field), field)
                target = regular({(1,) * m: eye(2, field)}, m, r, 2, 2, field)
                error = [[field.sub(x, y) for x, y in zip(a, b)] for a, b in zip(network, target)]
                error_rank = rank(error, field)
                for k in range(m + 1):
                    assert 2 * cut_count(m, r, k) <= 3 * (layer(m, r, k) + layer(m, r, k + 1)) + 2 * error_rank
                    counts["changing_width_network_invoices"] += 1

    # One-fraction rare-error bound over F5, with noncommuting A,B.
    field = Field(5)
    for m in range(2, 9):
        zero = (0,) * m
        allowed = [a for a in product(range(2), repeat=m) if sum(a) <= 1]
        for rep in range(4):
            a = {alpha: [[rng.randrange(5) for _ in range(3)] for _ in range(3)] for alpha in allowed}
            b = {alpha: [[0] * 3 for _ in range(3)] for alpha in allowed}
            b[zero] = eye(3, field)
            for alpha in allowed:
                b[alpha][0][1] = rng.randrange(5)
                b[alpha][1][2] = rng.randrange(5)
            totals = [0, 0]
            noncommuting = False
            for point in product(range(2), repeat=m):
                av = evaluate(a, point, 4, 3, 3, field)
                bv = evaluate(b, point, 4, 3, 3, field)
                inv = inverse(bv, field)
                assert inv is not None
                noncommuting |= multiply(av, bv, field) != multiply(bv, av, field)
                chi = 4 if sum(point) % 2 else 1
                for index, p in enumerate([multiply(av, inv, field), multiply(inv, av, field)]):
                    error = [[field.sub(chi if i == j else 0, p[i][j]) for j in range(3)] for i in range(3)]
                    totals[index] += rank(error, field)
            threshold = (m + 2) // 2
            lower = 3 * sum(comb(m, k) for k in range(threshold + 1, m + 1))
            assert min(totals) >= lower
            assert noncommuting
            counts["noncommuting_one_fraction_cases"] += 2
            counts["one_fraction_spectral_ranks"] += 2**(m + 1)
            if rep == 0:
                examples.append({"m": m, "width": 3, "a": 1, "b": 1,
                                 "left_and_right_rank_sums": totals, "lower_rank_sum": lower})

    # Counterexample to counting inverse gates rather than their active rows:
    # inverse of the (m+1)-row lower-bidiagonal matrix has chi in its
    # bottom-left entry, by the unique product path. Its one gate uses m+1
    # active rows. The wrong q=1 bill violates the exact cut bound.
    m = 9
    k = 4
    assert 2 * comb(m, k) < 2**m
    assert (m + 1) * 2 * comb(m, k) >= 2**m
    negative = [
        {"omission": "active row volume", "example": "one inverse on m+1 path rows, input/output width 1",
         "m": m, "invalid_gate_count": 1, "correct_active_volume": m + 1},
        {"omission": "singular denominator defect", "example": "A=B=0, P=chi I",
         "apparent_error": 0, "denominator_nullity_fraction": 1},
        {"omission": "affine query contract", "example": "chi I declared one affine gate for m=9",
         "actual_support_degree": 9},
    ]
    result = {"status": "passed", "arithmetic": "exact F4, F5 and integers",
              "seed": 1414213562, "counts": dict(counts), "examples": examples,
              "negative_controls": negative,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "helper_sha256": hashlib.sha256(Path(__file__).with_name("verify_spectral_rank.py").read_bytes()).hexdigest(),
              "scope": "Exact finite rank/count/inverse tests; no tape runtime or asymptotic verification by enumeration"}
    Path(__file__).with_name("inverse-query-commutator-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
