#!/usr/bin/env python3
"""Exact ramified specialization and Hermite-node controls.

No huge formula template or physical multiplier is constructed.
"""
from __future__ import annotations

import json
from math import gcd
from pathlib import Path
from random import Random


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def exact_divide(a, b):
    a = a[:]
    assert b[-1] == 1
    out = [0] * (len(a) - len(b) + 1)
    for k in range(len(out) - 1, -1, -1):
        coefficient = a[k + len(b) - 1]
        out[k] = coefficient
        for j, value in enumerate(b):
            a[k + j] -= coefficient * value
    assert not any(a)
    return trim(out)


def cyclotomics(cap):
    values = {}
    for n in range(1, cap + 1):
        polynomial = [-1] + [0] * (n - 1) + [1]
        for d in range(1, n):
            if n % d == 0:
                polynomial = exact_divide(polynomial, values[d])
        values[n] = polynomial
        assert sum(abs(v) for v in polynomial) <= 2 ** (len(polynomial) - 1)
    return values


class Ring:
    def __init__(self, polynomial, prime=None):
        self.polynomial = tuple(polynomial)
        self.degree = len(polynomial) - 1
        self.p = prime
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)

    def scalar(self, a):
        return ((a % self.p if self.p else a),) + (0,) * (self.degree - 1)

    def add(self, a, b):
        return tuple((x + y) % self.p if self.p else x + y for x, y in zip(a, b))

    def neg(self, a):
        return tuple((-x) % self.p if self.p else -x for x in a)

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        n = self.degree
        out = [0] * (2 * n - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    out[i + j] += x * y
        for k in range(2 * n - 2, n - 1, -1):
            coefficient = out[k]
            if coefficient:
                for j in range(n):
                    out[k - n + j] -= coefficient * self.polynomial[j]
        return tuple(v % self.p for v in out[:n]) if self.p else tuple(out[:n])

    def power(self, a, exponent):
        out = self.one
        while exponent:
            if exponent & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            exponent //= 2
        return out

    def eta(self):
        if self.degree == 1:
            return self.scalar(-self.polynomial[0])
        return (0, 1) + (0,) * (self.degree - 2)


def matrix_mul(ring, a, b):
    n = len(a)
    out = [[ring.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] != ring.zero:
                for j in range(n):
                    if b[k][j] != ring.zero:
                        out[i][j] = ring.add(out[i][j], ring.mul(a[i][k], b[k][j]))
    return out


def gaussian_row(ring, root, n):
    powers = [ring.power(root, k) for k in range(n + 1)]
    row = [ring.one]
    for width in range(1, n + 1):
        new = [ring.one] + [ring.zero] * (width - 1) + [ring.one]
        for k in range(1, width):
            new[k] = ring.add(row[k - 1], ring.mul(powers[k], row[k]))
        row = new
    return row


def check_sum_cycles(ring, root, a, b):
    d = len(a)
    factors = []
    for grade in range(d):
        matrix = [[ring.zero for _ in range(d)] for _ in range(d)]
        for i in range(d):
            matrix[(i + 1) % d][i] = ring.add(matrix[(i + 1) % d][i], a[i])
            matrix[i][i] = ring.add(matrix[i][i], ring.mul(ring.power(root, i), b[(grade - i) % d]))
        factors.append(matrix)
    va = vb = ring.one
    for x, y in zip(a, b):
        va, vb = ring.mul(va, x), ring.mul(vb, y)
    target = ring.add(va, vb)
    for start in range(d):
        result = [[ring.one if i == j else ring.zero for j in range(d)] for i in range(d)]
        for step in range(d):
            result = matrix_mul(ring, factors[(start + step) % d], result)
        assert all(result[i][j] == (target if i == j else ring.zero) for i in range(d) for j in range(d))
    return d


def main():
    phis = cyclotomics(120)
    integer_products = node_reductions = gaussian_coefficients = 0
    cycle_products = ramified_coefficients = 0
    rng = Random(20261125)
    for conductor in (6, 12, 20, 24, 30, 60, 120):
        tau = conductor & -conductor
        integer_ring = Ring(phis[conductor])
        eta = integer_ring.eta()
        assert integer_ring.power(eta, conductor) == integer_ring.one
        zeta = integer_ring.power(eta, conductor // tau)
        for delta in range(1, tau):
            order = tau // gcd(tau, delta)
            rho = integer_ring.power(zeta, delta)
            numerator = integer_ring.one
            for v in range(3, order, 2):
                numerator = integer_ring.mul(numerator, integer_ring.sub(integer_ring.one, integer_ring.power(rho, v)))
            assert integer_ring.mul(integer_ring.sub(integer_ring.one, rho), numerator) == integer_ring.scalar(2)
            integer_products += 1
            for prime in (3, 5, 7):
                field_ring = Ring(phis[conductor], prime)
                ff_rho = tuple(v % prime for v in rho)
                ff_num = tuple(v % prime for v in numerator)
                inverse = field_ring.mul(field_ring.scalar(pow(2, -1, prime)), ff_num)
                assert field_ring.mul(field_ring.sub(field_ring.one, ff_rho), inverse) == field_ring.one
                node_reductions += 1
        for prime in (3, 5, 7):
            ring = Ring(phis[conductor], prime)
            eta = ring.eta()
            for d in range(2, min(conductor, 12) + 1):
                if conductor % d:
                    continue
                root = ring.power(eta, conductor // d)
                row = gaussian_row(ring, root, d)
                assert all(value == ring.zero for value in row[1:-1])
                gaussian_coefficients += d - 1
                if d % prime == 0:
                    ramified_coefficients += d - 1

    # This ring is F3[epsilon]/epsilon^2 in cyclotomic coordinates.
    # eta=-1+epsilon. For d=6, 1+eta is a nonzero square-zero partial
    # geometric sum, so a distinguished-root/unit-denominator shortcut
    # would not justify the identity.
    ring = Ring(phis[6], 3)
    eta = ring.eta()
    epsilon = ring.add(eta, ring.one)
    assert epsilon != ring.zero and ring.mul(epsilon, epsilon) == ring.zero
    for d in (3, 6):
        root = ring.power(eta, 6 // d)
        for trial in range(24):
            a = [tuple(rng.randrange(3) for _ in range(ring.degree)) for _ in range(d)]
            b = [tuple(rng.randrange(3) for _ in range(ring.degree)) for _ in range(d)]
            if trial % 3 == 0:
                a[trial % d] = ring.zero
            if trial % 5 == 0:
                b[trial % d] = ring.zero
            cycle_products += check_sum_cycles(ring, root, a, b)

    bad = Ring(phis[6], 5)
    wrong_row = gaussian_row(bad, bad.one, 3)
    assert any(value != bad.zero for value in wrong_row[1:-1])
    result = {
        "status": "PASS",
        "scope": "finite cyclotomic identities, including ramified odd-characteristic reductions; no huge template or tape implementation",
        "integer_cyclotomic_polynomials_and_height_checks": len(phis),
        "integer_power_two_node_inverse_products": integer_products,
        "odd_characteristic_node_inverse_checks": node_reductions,
        "vanishing_gaussian_coefficients": gaussian_coefficients,
        "ramified_gaussian_coefficients": ramified_coefficients,
        "all_rotated_sum_products_over_F3_epsilon_squared": cycle_products,
        "ramified_sum_instances": 48,
        "negative_controls": {
            "degree_six_partial_sum_nonzero_square_zero": True,
            "wrong_noncyclotomic_root_rejected": True,
        },
    }
    Path(__file__).with_name("formula-cyclotomic-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
