#!/usr/bin/env python3
"""Finite exact checks; objects share references, sizes count full unfoldings.

Addition lengths are actual padded cyclic-family lengths. No full multiplier
or formal-kernel verification is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json

@dataclass(frozen=True, eq=False)
class Expr:
    op: str
    value: int
    args: tuple[Expr, ...]
    length: int
    size: int

def is_power(n: int, p: int) -> bool:
    if n < 1:
        return False
    while n % p == 0:
        n //= p
    return n == 1

class Formula:
    def __init__(self, p: int):
        self.p = p

    def const(self, value: int) -> Expr:
        return Expr("const", value % self.p, (), 0, 1)

    def var(self, index: int) -> Expr:
        return Expr("var", index, (), 1, 1)

    def scale(self, scalar: int, arg: Expr) -> Expr:
        scalar %= self.p
        if not scalar:
            return self.const(0)
        if arg.op == "const":
            return self.const(scalar * arg.value)
        if scalar == 1:
            return arg
        return Expr("scale", scalar, (arg,), arg.length, arg.size + 2)

    def add(self, args: list[Expr], budget: int) -> Expr:
        assert is_power(budget, self.p), ("non-prime-power", budget, self.p)
        assert all(x.length <= budget for x in args), ("over-budget", budget)
        if all(x.op == "const" for x in args):
            return self.const(sum(x.value for x in args))
        # The flattened sum abbreviates binary gates with the same budget.
        return Expr("add", budget, tuple(args), budget,
                    sum(x.size for x in args) + max(0, len(args) - 1))

    def mul(self, args: list[Expr]) -> Expr:
        scalar = 1
        nonconstant = []
        for arg in args:
            if arg.op == "const":
                scalar = scalar * arg.value % self.p
            else:
                nonconstant.append(arg)
        if not scalar:
            return self.const(0)
        if not nonconstant:
            return self.const(scalar)
        if len(nonconstant) == 1:
            return self.scale(scalar, nonconstant[0])
        expr = Expr("mul", 0, tuple(nonconstant),
                    sum(x.length for x in nonconstant),
                    sum(x.size for x in nonconstant) + len(nonconstant) - 1)
        return self.scale(scalar, expr)

    def binom(self, arg: Expr, a: int, digit_budget: int) -> Expr:
        assert 0 <= a < self.p
        return self.scale(pow(factorial(a), -1, self.p), self.mul([
            self.add([arg, self.const(-r)], digit_budget) for r in range(a)
        ]))

    def add_digits(self, xs: list[Expr], ys: list[Expr]) -> list[Expr]:
        assert len(xs) == len(ys)
        carry = self.const(0)
        answer = []
        for i, (x, y) in enumerate(zip(xs, ys)):
            budget = self.p ** i
            answer.append(self.add([x, y, carry], budget))
            if i + 1 == len(xs):
                break
            g = self.add([
                self.mul([self.binom(x, a, budget),
                          self.binom(y, self.p - a, budget)])
                for a in range(1, self.p)
            ], budget * self.p)
            w = self.add([x, y, self.const(1)], budget)
            propagated = self.mul([w] * (self.p - 1) + [carry])
            carry = self.add([g, carry, self.scale(-1, propagated)],
                             budget * self.p)
        return answer

    def count_digits(self, m: int, t: int) -> list[Expr]:
        count = 1 << (m - 1).bit_length()
        rows = [[self.var(j)] + [self.const(0)] * (t - 1) if j < m
                else [self.const(0)] * t for j in range(count)]
        while len(rows) > 1:
            rows = [self.add_digits(rows[j], rows[j + 1])
                    for j in range(0, len(rows), 2)]
        return rows[0]

    def offset(self, digits: list[Expr], u: int) -> list[Expr]:
        return self.add_digits(digits, [
            self.const((-u // (self.p ** i)) % self.p)
            for i in range(len(digits))
        ])

    def lucas(self, digits: list[Expr], h: int) -> Expr:
        return self.mul([
            self.binom(x, (h // (self.p ** i)) % self.p, self.p ** i)
            for i, x in enumerate(digits)
        ])

    def predictor(self, digits: list[Expr], u: int, degree: int) -> Expr:
        length = 1
        while length < max(1, degree):
            length *= self.p
        phase = -1 if u % 2 else 1
        return self.add([
            self.scale(phase * pow(-2, h), self.lucas(digits, h))
            for h in range(degree + 1)
        ], length)

    def evaluator(self, assignment: tuple[int, ...]):
        @lru_cache(None)
        def evaluate(expr: Expr) -> int:
            if expr.op == "const":
                return expr.value
            if expr.op == "var":
                return assignment[expr.value]
            if expr.op == "scale":
                return expr.value * evaluate(expr.args[0]) % self.p
            values = [evaluate(x) for x in expr.args]
            if expr.op == "add":
                return sum(values) % self.p
            result = 1
            for value in values:
                result = result * value % self.p
            return result
        return evaluate

def generalized_binom(n: int, k: int) -> int:
    value = 1
    for i in range(1, k + 1):
        value = value * (n - i + 1) // i
    return value

def structural_check(root: Expr, p: int, top: int) -> int:
    seen = set()
    stack = [root]
    additions = 0
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        if node.op == "add":
            assert node.length == node.value and is_power(node.length, p)
            assert all(a.length <= node.length for a in node.args)
            assert node.length <= top
            additions += len(node.args) - 1
        if node.op == "mul":
            assert node.length == sum(a.length for a in node.args)
        stack.extend(node.args)
    return additions

def formula_checks() -> dict:
    totals = dict(formulas=0, digit_values=0, offset_values=0,
                  newton_values=0, window_parity_values=0,
                  checked_additions=0, actual_digit_size_bounds=0,
                  largest_unfolded_formula=0)
    profiles = [(p, m, degree) for p in [3, 5, 7, 11]
                for m in range(2, 7) for degree in range(1, m + 1)]
    profiles += [(3, 9, 9), (3, 10, 10), (3, 27, 27), (5, 25, 25)]
    for p, m, degree in profiles:
        t = 1
        while p ** t <= degree:
            t += 1
        algebra = Formula(p)
        digits = algebra.count_digits(m, t)
        r = (m - 1).bit_length()
        a_p = 128 * p * p
        for i, digit in enumerate(digits):
            assert digit.size <= a_p ** r * 2 ** i * comb(r + i, i)
            totals["actual_digit_size_bounds"] += 1
        for u in [-m - 1, -1, 0, 1, m, m + 2]:
            shifted = algebra.offset(digits, u)
            for i, digit in enumerate(shifted):
                assert digit.size <= a_p ** (r + 1) * 2 ** i * comb(r + 1 + i, i)
                totals["actual_digit_size_bounds"] += 1
            root = algebra.predictor(shifted, u, degree)
            totals["formulas"] += 1
            totals["checked_additions"] += structural_check(
                root, p, root.length)
            totals["largest_unfolded_formula"] = max(
                totals["largest_unfolded_formula"], root.size)
            assignments = (product(range(2), repeat=m) if m <= 10 else
                           [tuple(int(j < c) for j in range(m))
                            for c in range(m + 1)] +
                           [tuple((j + phase) % 2 for j in range(m))
                            for phase in range(2)])
            for assignment in assignments:
                evaluate = algebra.evaluator(assignment)
                count = sum(assignment)
                for i in range(t):
                    assert evaluate(digits[i]) == count // p ** i % p
                    assert evaluate(shifted[i]) == (count - u) // p ** i % p
                    totals["digit_values"] += 1
                    totals["offset_values"] += 1
                expected = (-1 if u % 2 else 1) * sum(
                    (-2) ** h * generalized_binom(count - u, h)
                    for h in range(degree + 1))
                assert evaluate(root) == expected % p
                totals["newton_values"] += 1
                if u <= count <= u + degree:
                    assert evaluate(root) == (-1) ** count % p
                    totals["window_parity_values"] += 1
    return totals

def recurrence_checks() -> int:
    count = 0
    for p in [2, 3, 5, 7, 11, 13]:
        bound_constant = 128 * p * p
        previous = [1] * 13
        for r in range(1, 13):
            current = [bound_constant * sum(
                2 ** (k - i) * previous[i] for i in range(k + 1))
                for k in range(13)]
            for k, value in enumerate(current):
                upper = bound_constant ** r * 2 ** k * comb(r + k, k)
                assert value <= upper
                count += 1
            previous = current
    return count

def identity(n: int) -> list[list[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]

def matmul(a: list[list[int]], b: list[list[int]], p: int) -> list[list[int]]:
    n = len(a)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if a[i][j]:
                for k in range(n):
                    out[i][k] = (out[i][k] + a[i][j] * b[j][k]) % p
    return out

def scalar_identity(scalar: int, n: int, p: int) -> list[list[int]]:
    return [[scalar % p if i == j else 0 for j in range(n)] for i in range(n)]

def inverse2(matrix: list[list[int]], p: int) -> list[list[int]]:
    a, b = matrix[0]
    c, d = matrix[1]
    determinant = pow((a * d - b * c) % p, -1, p)
    return [[d * determinant % p, -b * determinant % p],
            [-c * determinant % p, a * determinant % p]]

def cyclic_family(p: int, length: int, scalar: int, seed: int,
                  width: int = 2) -> list[list[list[int]]]:
    if width == 1:
        factors = [[[1]] for _ in range(length)]
        factors[0] = [[scalar % p]]
        return factors
    factors = []
    acc = identity(2)
    for i in range(length - 1):
        a = (i + seed) % p
        b = (i * i + 2 * seed + 1) % p
        factor = [[1, a], [b, (1 + a * b) % p]]
        factors.append(factor)
        acc = matmul(factor, acc, p)
    factors.append(inverse2(acc, p))
    factors[0] = [[scalar * x % p for x in row] for row in factors[0]]
    return factors

def sliced_sum(a: list, b: list, t: int, p: int,
               wrong_mask: bool = False) -> list[list[int]]:
    d = len(a)
    ra, rb = len(a[0]), len(b[0])
    width = ra * rb
    out = [[0] * (d * width) for _ in range(d * width)]
    for grade in range(d):
        second = b[t % d if wrong_mask else (t - grade) % d]
        for ai in range(ra):
            for bi in range(rb):
                column = grade * width + ai * rb + bi
                for ao in range(ra):
                    row = ((grade + 1) % d) * width + ao * rb + bi
                    out[row][column] = (out[row][column] + a[grade][ao][ai]) % p
                for bo in range(rb):
                    row = grade * width + ai * rb + bo
                    out[row][column] = (out[row][column] + second[bo][bi]) % p
    return out

def cyclic_checks() -> dict:
    totals = dict(child_cyclic_products=0, sum_cyclic_products=0,
                  wrong_phase_controls=0, non_prime_power_controls=0)
    for p, d, width in [(3, 3, 2), (5, 5, 2), (7, 7, 2),
                         (3, 9, 1), (2, 8, 1)]:
        for seed in range(3):
            alpha, beta = seed % p, (seed + 1) % p
            a = cyclic_family(p, d, alpha, seed, width)
            b = cyclic_family(p, d, beta, seed + 2, width)
            for family, scalar in [(a, alpha), (b, beta)]:
                for start in range(d):
                    acc = identity(width)
                    for step in range(d):
                        acc = matmul(family[(start + step) % d], acc, p)
                    assert acc == scalar_identity(scalar, width, p)
                    totals["child_cyclic_products"] += 1
            factors = [sliced_sum(a, b, t, p) for t in range(d)]
            target = scalar_identity(alpha + beta, d * width * width, p)
            for start in range(d):
                acc = identity(len(target))
                for step in range(d):
                    acc = matmul(factors[(start + step) % d], acc, p)
                assert acc == target
                totals["sum_cyclic_products"] += 1
            wrong = identity(len(target))
            for t in range(d):
                wrong = matmul(sliced_sum(a, b, t, p, True), wrong, p)
            if wrong != target:
                totals["wrong_phase_controls"] += 1
    assert totals["wrong_phase_controls"] >= 6
    for p, d in [(3, 2), (3, 6), (5, 3), (7, 4)]:
        a = b = [[[1]] for _ in range(d)]
        acc = identity(d)
        for t in range(d):
            acc = matmul(sliced_sum(a, b, t, p), acc, p)
        assert acc != scalar_identity(2, d, p)
        totals["non_prime_power_controls"] += 1
    return totals

def carry_and_budget_checks() -> dict:
    cases, rejected = 0, 0
    for p in [2, 3, 5, 7, 11, 13]:
        for x, y, c in product(range(p), range(p), range(2)):
            g = sum(comb(x, a) * comb(y, p - a)
                    for a in range(1, p)) % p
            next_carry = (g + c - pow(x + y + 1, p - 1, p) * c) % p
            assert next_carry == (x + y + c) // p
            cases += 1
        if p > 2:
            f = Formula(p)
            x, y, c = (f.var(i) for i in range(3))
            w = f.add([x, y, f.const(1)], 1)
            power = f.mul([w] * (p - 1))
            try:
                f.add([f.const(1), f.scale(-1, power)], p - 1)
            except AssertionError:
                rejected += 1
            else:
                raise AssertionError("non-prime-power H budget accepted")
            rounded = f.add([f.const(1), f.scale(-1, power)], p)
            try:
                f.add([f.mul([rounded, c])], p)
            except AssertionError:
                rejected += 1
            else:
                raise AssertionError("rounded H times carry exceeded no budget")
    return dict(digit_carry_cases=cases, rejected_old_budget_controls=rejected)

def poly_add(a: dict, b: dict, p: int) -> dict:
    out = a.copy()
    for key, value in b.items():
        out[key] = (out.get(key, 0) + value) % p
        if not out[key]:
            del out[key]
    return out

def poly_mul(a: dict, b: dict, p: int) -> dict:
    out = {}
    for (i, j), value in a.items():
        for (k, l), other in b.items():
            key = (i + k, j + l)
            out[key] = (out.get(key, 0) + value * other) % p
            if not out[key]:
                del out[key]
    return out

def polynomial_product(a: list, b: list, p: int) -> list:
    n = len(a)
    out = [[{} for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if a[i][j]:
                for k in range(n):
                    if b[j][k]:
                        out[i][k] = poly_add(out[i][k],
                            poly_mul(a[i][j], b[j][k], p), p)
    return out

def formal_cyclic_checks() -> dict:
    cases, entries = 0, 0
    for p, d, width in [(3, 3, 2), (5, 5, 2), (3, 9, 1), (2, 4, 1)]:
        a = cyclic_family(p, d, 1, 1, width)
        b = cyclic_family(p, d, 1, 2, width)
        n = d * width * width
        factors = []
        for t in range(d):
            out = [[{} for _ in range(n)] for _ in range(n)]
            for grade in range(d):
                second_grade = (t - grade) % d
                for ai in range(width):
                    for bi in range(width):
                        column = grade * width * width + ai * width + bi
                        for ao in range(width):
                            value = a[grade][ao][ai]
                            row = ((grade + 1) % d) * width * width + ao * width + bi
                            monomial = (1, 0) if grade == 0 else (0, 0)
                            out[row][column] = poly_add(out[row][column],
                                {monomial: value} if value else {}, p)
                        for bo in range(width):
                            value = b[second_grade][bo][bi]
                            row = grade * width * width + ai * width + bo
                            monomial = (0, 1) if second_grade == 0 else (0, 0)
                            out[row][column] = poly_add(out[row][column],
                                {monomial: value} if value else {}, p)
            factors.append(out)
        target = [[{(1, 0): 1, (0, 1): 1} if i == j else {}
                   for j in range(n)] for i in range(n)]
        for start in range(d):
            acc = [[{(0, 0): 1} if i == j else {} for j in range(n)]
                   for i in range(n)]
            for step in range(d):
                acc = polynomial_product(factors[(start + step) % d], acc, p)
            assert acc == target
            cases += 1
            entries += n * n
    return dict(formal_bivariate_cyclic_products=cases,
                formal_polynomial_matrix_entries=entries)

def main() -> None:
    report = {
        "status": "passed",
        "scope": "Finite formula budgets, carry values, and whole cyclic identities; no full machine or kernel proof.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "formula": formula_checks(),
        "unfolded_size_majorant_cases": recurrence_checks(),
        "carry_and_budget": carry_and_budget_checks(),
        "cyclic": cyclic_checks(),
        "formal_cyclic": formal_cyclic_checks(),
    }
    output = Path(__file__).with_name("p-power-count-compiler-verification.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
