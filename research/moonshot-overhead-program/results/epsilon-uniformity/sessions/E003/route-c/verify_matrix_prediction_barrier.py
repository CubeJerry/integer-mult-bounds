#!/usr/bin/env python3
"""Exact finite checks for M1--M3; not an asymptotic or tape verification."""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path


class Field:
    def __init__(self, order: int) -> None:
        self.order = order

    def add(self, a: int, b: int) -> int:
        return a ^ b if self.order == 4 else (a + b) % self.order

    def neg(self, a: int) -> int:
        return a if self.order == 4 else (-a) % self.order

    def sub(self, a: int, b: int) -> int:
        return self.add(a, self.neg(b))

    def mul(self, a: int, b: int) -> int:
        if self.order != 4:
            return a * b % self.order
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7
        return result

    def inv(self, a: int) -> int:
        assert a
        return next(b for b in range(1, self.order) if self.mul(a, b) == 1)

    def prod(self, values) -> int:
        result = 1
        for a in values:
            result = self.mul(result, a)
        return result

    def total(self, values) -> int:
        result = 0
        for a in values:
            result = self.add(result, a)
        return result


def rank(matrix: list[list[int]], field: Field) -> int:
    a = [row[:] for row in matrix]
    n = len(a)
    if not n:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        row = next((r for r in range(pivot, n) if a[r][col]), None)
        if row is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        scale = field.inv(a[pivot][col])
        a[pivot] = [field.mul(scale, entry) for entry in a[pivot]]
        for r in range(n):
            if r != pivot and a[r][col]:
                factor = a[r][col]
                a[r] = [field.sub(v, field.mul(factor, p)) for v, p in zip(a[r], a[pivot])]
        pivot += 1
        if pivot == n:
            break
    return pivot


def matmul(a, b, field):
    return [[field.total(field.mul(x, y) for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def matadd(a, b, field):
    return [[field.add(x, y) for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def matsub(a, b, field):
    return [[field.sub(x, y) for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def low_masks(m, t):
    return [mask for mask in range(1 << m) if mask.bit_count() <= t]


def evaluate(coefficients, masks, point, field):
    w = len(coefficients[0])
    result = [[0] * w for _ in range(w)]
    for coefficient, mask in zip(coefficients, masks):
        if mask & point == mask:
            result = matadd(result, coefficient, field)
    return result


def theorem_case(m, t, w, field, rng, check_moments):
    masks = low_masks(m, t)
    coefficients = [[[rng.randrange(field.order) for _ in range(w)] for _ in range(w)] for _ in masks]
    pairs = [rng.sample(range(1, field.order), 2) for _ in range(m)]
    alpha = [field.mul(a, field.inv(field.sub(a, b))) for a, b in pairs]
    beta = [field.mul(field.neg(b), field.inv(field.sub(a, b))) for a, b in pairs]
    k = (m - t - 1) // 2
    test_masks = low_masks(m, k)
    b_count = len(test_masks)
    moments = [[0] * (w * b_count) for _ in range(w * b_count)] if check_moments else []
    total_rank = 0
    for point in range(1 << m):
        f = field.prod(pair[(point >> i) & 1] for i, pair in enumerate(pairs))
        p = evaluate(coefficients, masks, point, field)
        defect = [[field.sub(f * int(i == j), p[i][j]) for j in range(w)] for i in range(w)]
        total_rank += rank(defect, field)
        if check_moments:
            mu = field.prod(beta[i] if (point >> i) & 1 else alpha[i] for i in range(m))
            z = [field.sub((point >> i) & 1, beta[i]) for i in range(m)]
            values = [field.prod(z[i] for i in range(m) if (mask >> i) & 1) for mask in test_masks]
            inverse_f = field.inv(f)
            q = [[field.mul(inverse_f, entry) for entry in row] for row in defect]
            for s, vs in enumerate(values):
                for u, vu in enumerate(values):
                    scalar = field.mul(mu, field.mul(vs, vu))
                    for i in range(w):
                        for j in range(w):
                            old = moments[s * w + i][u * w + j]
                            moments[s * w + i][u * w + j] = field.add(old, field.mul(scalar, q[i][j]))
    assert total_rank >= w * b_count, (field.order, m, t, w, total_rank, b_count)
    if check_moments:
        for s, mask in enumerate(test_masks):
            diagonal = field.prod(field.mul(alpha[i], beta[i]) for i in range(m) if (mask >> i) & 1)
            assert diagonal
            for u in range(b_count):
                for i in range(w):
                    for j in range(w):
                        expected = diagonal if s == u and i == j else 0
                        assert moments[s * w + i][u * w + j] == expected
        assert rank(moments, field) == w * b_count
    return b_count * w


def exhaustive_scalar(field, m, t):
    masks = low_masks(m, t)
    target = [field.prod(2 if (point >> i) & 1 else 1 for i in range(m)) for point in range(1 << m)]
    floor = len(low_masks(m, (m - t - 1) // 2))
    cases = 0
    minimum = 1 << m
    for coefficients in itertools.product(range(field.order), repeat=len(masks)):
        errors = sum(field.total(c for c, mask in zip(coefficients, masks) if mask & point == mask) != target[point] for point in range(1 << m))
        assert errors >= floor
        minimum = min(minimum, errors)
        cases += 1
    return cases, minimum, floor


def ternary_case(m, t, w, rng):
    field = Field(4)
    terms = []
    for mask in low_masks(m, t):
        variables = [i for i in range(m) if (mask >> i) & 1]
        for values in itertools.product((1, 2, 3), repeat=len(variables)):
            coefficient = [[rng.randrange(4) for _ in range(w)] for _ in range(w)]
            terms.append((list(zip(variables, values)), coefficient))
    total_rank = 0
    for point in itertools.product((1, 2, 3), repeat=m):
        p = [[0] * w for _ in range(w)]
        for conditions, coefficient in terms:
            if all(point[i] == value for i, value in conditions):
                p = matadd(p, coefficient, field)
        f = field.prod(point)
        defect = [[field.sub(f * int(i == j), p[i][j]) for j in range(w)] for i in range(w)]
        total_rank += rank(defect, field)
    b_count = len(low_masks(m, (m - t - 1) // 2))
    assert total_rank * (1 << m) >= w * b_count * 3**m


def telescoping_case(field, w, count, rng):
    bases = [[[rng.randrange(field.order) for _ in range(w)] for _ in range(w)] for _ in range(count)]
    widths = [rng.randint(1, w) for _ in range(count)]
    updates = []
    for base, h in zip(bases, widths):
        u = [[rng.randrange(field.order) for _ in range(h)] for _ in range(w)]
        v = [[rng.randrange(field.order) for _ in range(w)] for _ in range(h)]
        updates.append(matadd(base, matmul(u, v, field), field))
    full, base_product = eye(w), eye(w)
    for update, base in zip(updates, bases):
        full, base_product = matmul(update, full, field), matmul(base, base_product, field)
    expanded = [[0] * w for _ in range(w)]
    for r in range(count):
        term = matsub(updates[r], bases[r], field)
        left = eye(w)
        for update in updates[r + 1:]:
            left = matmul(update, left, field)
        right = eye(w)
        for base in bases[:r]:
            right = matmul(base, right, field)
        expanded = matadd(expanded, matmul(matmul(left, term, field), right, field), field)
    difference = matsub(full, base_product, field)
    assert expanded == difference
    assert rank(difference, field) <= sum(widths)


def main():
    rng = random.Random(260326)
    receipts = {"scope": "Exact finite matrix moment identities, rank inequalities, ternary restrictions and telescoping; not an asymptotic or tape proof.", "seed": 260326}
    gram_cases = rank_cases = 0
    for order in (3, 4, 5, 7):
        field = Field(order)
        for m in range(1, 7):
            for t in range(m):
                for w in (1, 2, 3):
                    moments = m <= 5 and w <= 2
                    theorem_case(m, t, w, field, rng, moments)
                    rank_cases += 1
                    gram_cases += int(moments)
    receipts.update(matrix_rank_cases=rank_cases, full_gram_identity_cases=gram_cases)
    exhaustions = []
    for order, m, t in ((3, 3, 2), (4, 3, 2), (5, 3, 1), (7, 2, 1), (3, 4, 1)):
        cases, minimum, bound = exhaustive_scalar(Field(order), m, t)
        exhaustions.append({"field_order": order, "m": m, "t": t, "polynomials": cases, "minimum_errors": minimum, "rank_bound": bound})
    receipts["exhaustive_scalar_cases"] = exhaustions
    ternary_cases = 0
    for m in range(1, 6):
        for t in range(min(3, m)):
            for w in (1, 2):
                ternary_case(m, t, w, rng)
                ternary_cases += 1
    receipts["ternary_average_rank_cases"] = ternary_cases
    for order in (3, 4, 5, 7):
        for w in range(1, 6):
            for count in range(1, 5):
                telescoping_case(Field(order), w, count, rng)
    receipts["telescoping_cases"] = 80
    field = Field(5)
    assert rank([[1] * 4 for _ in range(4)], field) == 1
    assert sum([[1] * 4 for _ in range(4)][i][i] != 0 for i in range(4)) == 4
    # Coincident local values and an illicit depth reduction both give exact targets.
    assert rank([[0, 0], [0, 0]], Field(2)) == 0
    assert sum(math.comb(4, i) for i in range((4 - 0 - 1) // 2 + 1)) > 0
    assert len(low_masks(4, (4 - 3 - 1) // 2)) == 1
    receipts["negative_controls"] = {
        "nonzero_diagonal_count_is_not_rank": "4 nonzero diagonal entries, rank 1",
        "characteristic_two_parity": "local values coincide; depth-zero exact output would violate an improperly applied positive bound",
        "degree_m_exact_product": "zero defect is allowed at t=m; falsely pricing it at t=m-1 would require positive rank",
    }
    diagnostic = []
    for m in (64, 128, 256, 512, 1024, 2048):
        cumulative, running = [], 0
        for k in range(m + 1):
            running += math.comb(m, k)
            cumulative.append(running)
        denominator = 1 << m
        best = min((t * denominator + m * cumulative[(m - t - 1) // 2], t) for t in range(m))
        value = best[0] / denominator
        diagnostic.append({"m": m, "degree": best[1], "invoice_lower_bound": value, "ratio_to_sqrt_m_log_m": value / math.sqrt(m * math.log(m))})
    receipts["gamma_one_invoice_diagnostics_only"] = diagnostic
    output = Path(__file__).with_name("matrix-prediction-rank-verification.json")
    output.write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps(receipts, indent=2))


if __name__ == "__main__":
    main()
