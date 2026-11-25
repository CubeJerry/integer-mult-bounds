#!/usr/bin/env python3
"""Exact formal-polynomial checks of cyclic formula linearization.

Coefficient ring: F_p[z]/Phi_12(z), including nonreduced p=2,3 cases.
The query variable x remains formal; checks compare all its coefficients.
These are finite algebra tests, not asymptotic/physical compiler tests.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class Algebra:
    def __init__(self, prime):
        self.p = prime
        self.degree = 4
        self.phi = (1, 0, -1, 0, 1)
        self.zero = (0, 0, 0, 0)
        self.one = (1, 0, 0, 0)
        self.eta = (0, 1, 0, 0)

    def constant(self, n):
        return (n % self.p, 0, 0, 0)

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def multiply(self, a, b):
        out = [0] * 7
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] += x * y
        for degree in range(6, 3, -1):
            factor = out[degree] % self.p
            for j in range(4):
                out[degree - 4 + j] -= factor * self.phi[j]
        return tuple(x % self.p for x in out[:4])

    def power(self, a, exponent):
        result = self.one
        while exponent:
            if exponent & 1:
                result = self.multiply(result, a)
            a = self.multiply(a, a)
            exponent //= 2
        return result

    def trim(self, coefficients):
        coefficients = list(coefficients)
        while len(coefficients) > 1 and coefficients[-1] == self.zero:
            coefficients.pop()
        return tuple(coefficients)

    def padd(self, a, b):
        out = [self.zero] * max(len(a), len(b))
        for i in range(len(out)):
            out[i] = self.add(a[i] if i < len(a) else self.zero,
                              b[i] if i < len(b) else self.zero)
        return self.trim(out)

    def pmul(self, a, b):
        if a == (self.zero,) or b == (self.zero,):
            return (self.zero,)
        out = [self.zero] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] = self.add(out[i + j], self.multiply(x, y))
        return self.trim(out)

    def affine(self, slope=1, intercept=0):
        return self.trim((self.constant(intercept), self.constant(slope)))

    def matrix(self, size):
        return [[(self.zero,) for _ in range(size)] for _ in range(size)]

    def identity(self, size, scalar=None):
        out = self.matrix(size)
        for i in range(size):
            out[i][i] = scalar if scalar is not None else (self.one,)
        return out

    def mmul(self, a, b):
        out = self.matrix(len(a))
        for i in range(len(a)):
            for k in range(len(a)):
                if a[i][k] == (self.zero,):
                    continue
                for j in range(len(a)):
                    if b[k][j] != (self.zero,):
                        out[i][j] = self.padd(out[i][j], self.pmul(a[i][k], b[k][j]))
        return out

    def kron(self, a, b):
        r, s = len(a), len(b)
        return [[self.pmul(a[i // s][j // s], b[i % s][j % s])
                 for j in range(r * s)] for i in range(r * s)]


@dataclass
class Factorization:
    scalar: tuple
    factors: list
    size: int = 1


def leaf(poly):
    return Factorization(poly, [[[poly]]])


def padded(algebra, value, length):
    if not value.factors:
        factors = [algebra.identity(1, value.scalar)]
        size = 1
    else:
        factors, size = list(value.factors), value.size
    factors += [algebra.identity(size) for _ in range(length - len(factors))]
    return Factorization(value.scalar, factors, size)


def product(algebra, left, right):
    scalar = algebra.pmul(left.scalar, right.scalar)
    if not left.factors and not right.factors:
        return Factorization(scalar, [])
    if not left.factors or not right.factors:
        constant, other = (left, right) if not left.factors else (right, left)
        factors = [[list(row) for row in matrix] for matrix in other.factors]
        factors[0] = [[algebra.pmul(constant.scalar, entry) for entry in row] for row in factors[0]]
        return Factorization(scalar, factors, other.size)
    factors = [algebra.kron(matrix, algebra.identity(right.size)) for matrix in left.factors]
    factors += [algebra.kron(algebra.identity(left.size), matrix) for matrix in right.factors]
    return Factorization(scalar, factors, left.size * right.size)


def addition(algebra, left, right, *, wrong_twist=False, wrong_grade=False):
    scalar = algebra.padd(left.scalar, right.scalar)
    length = max(len(left.factors), len(right.factors))
    if length == 0:
        return Factorization(scalar, [])
    assert 12 % length == 0
    left, right = padded(algebra, left, length), padded(algebra, right, length)
    xi = algebra.one if wrong_twist else algebra.power(algebra.eta, 12 // length)
    block = left.size * right.size
    factors = []
    for grade in range(length):
        matrix = algebra.matrix(length * block)
        for first_grade in range(length):
            xblock = algebra.kron(left.factors[first_grade], algebra.identity(right.size))
            second_grade = (grade + first_grade if wrong_grade else grade - first_grade) % length
            yblock = algebra.kron(algebra.identity(left.size), right.factors[second_grade])
            coefficient = (algebra.power(xi, first_grade),)
            for i in range(block):
                for j in range(block):
                    source = first_grade * block + j
                    target_x = ((first_grade + 1) % length) * block + i
                    target_y = first_grade * block + i
                    matrix[target_x][source] = algebra.padd(matrix[target_x][source], xblock[i][j])
                    matrix[target_y][source] = algebra.padd(matrix[target_y][source], algebra.pmul(coefficient, yblock[i][j]))
        factors.append(matrix)
    return Factorization(scalar, factors, length * block)


def check_all_rotations(algebra, value):
    if not value.factors:
        return 0
    assert all(len(entry) <= 2 for matrix in value.factors for row in matrix for entry in row)
    target = algebra.identity(value.size, value.scalar)
    for first in range(len(value.factors)):
        actual = algebra.identity(value.size)
        for step in range(len(value.factors)):
            actual = algebra.mmul(value.factors[(first + step) % len(value.factors)], actual)
        assert actual == target
    return len(value.factors)


def scalar_product(algebra, length, variant=0, zero=False):
    result = Factorization((algebra.one,), [])
    for j in range(length):
        if zero and j == 0:
            factor = (algebra.zero,)
        elif variant:
            factor = algebra.trim((algebra.power(algebra.eta, j + 1), algebra.constant(j + 2)))
        else:
            factor = algebra.affine(1, j + 1)
        result = product(algebra, result, leaf(factor))
    return result


def rejected(algebra, value):
    try:
        check_all_rotations(algebra, value)
    except AssertionError:
        return True
    return False


def coefficient_formula_stats(length, degree, memo):
    """Counts the unfolded formula, even though numeric statistics are memoized."""
    key = (length, degree)
    if key in memo:
        return memo[key]
    if length == 1:
        result = (1, min(degree, 1) if degree <= 2 else 0)
    else:
        left = length // 2
        terms = []
        for split in range(degree + 1):
            first = coefficient_formula_stats(left, split, memo)
            second = coefficient_formula_stats(length - left, degree - split, memo)
            terms.append((first[0] + second[0] + 1, first[1] + second[1]))
        result = (sum(count for count, _ in terms) + degree,
                  max(syntactic for _, syntactic in terms))
    assert result[1] <= degree
    memo[key] = result
    return result


def run():
    tests, rotations = [], 0
    for prime in (2, 3, 5, 7):
        algebra = Algebra(prime)
        assert algebra.power(algebra.eta, 12) == algebra.one
        for length in (2, 3, 4, 6):
            left = scalar_product(algebra, length)
            right = scalar_product(algebra, length, variant=1)
            summed = addition(algebra, left, right)
            rotations += check_all_rotations(algebra, summed)
            zero = scalar_product(algebra, length, zero=True)
            rotations += check_all_rotations(algebra, addition(algebra, zero, right))
            tests.append(dict(name='formal_sum_and_zero_child', prime=prime,
                              length=length, rows=summed.size, passed=True))
        unequal = addition(algebra, leaf(algebra.affine(2, 1)), scalar_product(algebra, 3, variant=1))
        rotations += check_all_rotations(algebra, unequal)
        first = addition(algebra, scalar_product(algebra, 2), scalar_product(algebra, 2, variant=1))
        second = addition(algebra, scalar_product(algebra, 2, variant=1), leaf(algebra.affine(1, 0)))
        concatenated = product(algebra, first, second)
        rotations += check_all_rotations(algebra, concatenated)
        for constant in (0, 1, 2):
            entry = Factorization((algebra.constant(constant),), [])
            rotations += check_all_rotations(algebra, product(algebra, entry, first))
            rotations += check_all_rotations(algebra, addition(algebra, entry, first))
        tests.append(dict(name='unequal_degrees_products_constants', prime=prime, passed=True))
    algebra = Algebra(2)
    left, right = scalar_product(algebra, 3), scalar_product(algebra, 3, variant=1)
    assert rejected(algebra, addition(algebra, left, right, wrong_twist=True))
    assert rejected(algebra, addition(algebra, left, right, wrong_grade=True))
    e11, e12 = algebra.matrix(2), algebra.matrix(2)
    e11[0][0], e12[0][1] = (algebra.one,), (algebra.one,)
    bad = Factorization((algebra.zero,), [e11, e12], 2)
    assert algebra.mmul(e12, e11) == algebra.matrix(2)
    assert rejected(algebra, bad)
    tests.append(dict(name='negative_controls', wrong_twist=True, wrong_total_grade=True,
                      single_product_without_cyclic_invariant=True, passed=True))
    stats_cases = 0
    for length in (1, 2, 4, 8, 16, 32):
        for cap in range(1, 9):
            memo = {}
            for degree in range(cap + 1):
                size, syntactic = coefficient_formula_stats(length, degree, memo)
                bound = (8 * (cap + 1)) ** ((length - 1).bit_length() + 3)
                assert size <= bound and syntactic <= degree
                stats_cases += 1
    tests.append(dict(name='unfolded_coefficient_formula_size_and_degree', cases=stats_cases, passed=True))
    return dict(status='exact formal-polynomial verification passed',
                coefficient_ring='F_p[z]/(z^4-z^2+1)', includes_nonreduced_specializations=[2, 3],
                cyclic_products_checked=rotations, independent_input_matrix_identity=True,
                asymptotic_or_physical_compiler_verified=False, tests=tests)


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('formula-linearization-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
