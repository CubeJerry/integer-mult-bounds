#!/usr/bin/env python3
"""Independent finite controls for A's bounded original-source extraction.

These check finite algebra identities and conservative logarithmic invoices,
not an executed enormous template or a physical tape compiler.
"""
from __future__ import annotations

import json
from math import gcd, isqrt
from pathlib import Path


class Cyclo:
    def __init__(self, order: int, prime: int | None = None):
        assert order >= 2 and order & (order - 1) == 0
        self.order, self.d, self.p = order, order // 2, prime
        self.zero = (0,) * self.d
        self.one = (1,) + (0,) * (self.d - 1)

    def scalar(self, a):
        return ((a % self.p if self.p else a),) + (0,) * (self.d - 1)

    def add(self, a, b):
        v = tuple(x + y for x, y in zip(a, b))
        return tuple(x % self.p for x in v) if self.p else v

    def neg(self, a):
        return tuple((-x) % self.p if self.p else -x for x in a)

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        v = [0] * self.d
        for i, x in enumerate(a):
            if not x:
                continue
            for j, y in enumerate(b):
                if y:
                    k = i + j
                    v[k % self.d] += x * y * (1 if k < self.d else -1)
        return tuple(x % self.p for x in v) if self.p else tuple(v)

    def eta(self, exponent):
        exponent %= self.order
        v = [0] * self.d
        v[exponent % self.d] = 1 if exponent < self.d else -1
        return tuple(x % self.p for x in v) if self.p else tuple(v)

    def inverse_numerator(self, delta):
        delta %= self.order
        assert delta
        order = self.order // gcd(self.order, delta)
        value = self.one
        for exponent in range(3, order, 2):
            value = self.mul(value, self.sub(self.one, self.eta(delta * exponent)))
        return value

    def inverse_difference(self, a, b):
        assert self.p is not None and self.p != 2
        numerator = self.inverse_numerator(b - a)
        return self.mul(self.eta(-a), self.mul(self.scalar(pow(2, -1, self.p)), numerator))


def mm(c, a, b):
    n = len(a)
    out = [[c.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == c.zero:
                continue
            for j in range(n):
                if b[k][j] != c.zero:
                    out[i][j] = c.add(out[i][j], c.mul(a[i][k], b[k][j]))
    return out


def matrix_root_controls():
    count = 0
    for b in (2, 4):
        for p in (3, 5, 7, 17):
            c = Cyclo(b, p)
            for x, y in ((0, 0), (1, 1), (2, 1), (1, 2), (2, 2), (p - 1, 2)):
                factors_0 = ([x, y] if b == 2 else [x, x, y, 1])
                factors_1 = ([y, y] if b == 2 else [x, y, y, y])
                scalar_0 = scalar_1 = 1
                for a in factors_0:
                    scalar_0 = scalar_0 * a % p
                for a in factors_1:
                    scalar_1 = scalar_1 * a % p
                n = b * b
                pencil = [[c.zero for _ in range(n)] for _ in range(n)]
                for r in range(b):
                    for s in range(b):
                        source = r * b + s
                        dest_0 = ((r + 1) % b) * b + s
                        dest_1 = r * b + ((s + 1) % b)
                        pencil[dest_0][source] = c.add(pencil[dest_0][source], c.scalar(factors_0[r]))
                        term = c.mul(c.eta(r), c.scalar(factors_1[s]))
                        pencil[dest_1][source] = c.add(pencil[dest_1][source], term)
                value = [[c.one if i == j else c.zero for j in range(n)] for i in range(n)]
                for _ in range(b):
                    value = mm(c, value, pencil)
                target = c.scalar(scalar_0 + scalar_1)
                assert all(value[i][j] == (target if i == j else c.zero) for i in range(n) for j in range(n))
                count += 1
    return count


def cyclotomic_controls():
    exact_count = reduction_count = vandermonde_count = 0
    for order in (2, 4, 8, 16, 32, 64):
        c = Cyclo(order)
        for delta in range(1, order):
            numerator = c.inverse_numerator(delta)
            assert c.mul(c.sub(c.one, c.eta(delta)), numerator) == c.scalar(2)
            assert sum(abs(v) for v in numerator) <= 2 ** (c.d - 1)
            exact_count += 1
        for prime in (3, 5, 7, 17):
            f = Cyclo(order, prime)
            for delta in range(1, order):
                inverse = f.inverse_difference(0, delta)
                assert f.mul(f.sub(f.one, f.eta(delta)), inverse) == f.one
                reduction_count += 1
    for prime in (3, 5, 7, 17):
        c = Cyclo(16, prime)
        for indices in ((0,), (0, 1), (0, 2, 7), (0, 1, 3, 7), (1, 4, 8, 12)):
            nodes = [c.eta(i) for i in indices]
            rows = []
            for j, exponent in enumerate(indices):
                coeff = [c.one]
                denominator_inverse = c.one
                for k, other in enumerate(indices):
                    if k == j:
                        continue
                    new = [c.zero] * (len(coeff) + 1)
                    for r, value in enumerate(coeff):
                        new[r] = c.sub(new[r], c.mul(value, nodes[k]))
                        new[r + 1] = c.add(new[r + 1], value)
                    coeff = new
                    denominator_inverse = c.mul(denominator_inverse, c.inverse_difference(exponent, other))
                rows.append([c.mul(value, denominator_inverse) for value in coeff])
            for j, row in enumerate(rows):
                for k, node in enumerate(nodes):
                    value = c.zero
                    for coefficient in reversed(row):
                        value = c.add(c.mul(value, node), coefficient)
                    assert value == (c.one if j == k else c.zero)
                    vandermonde_count += 1
    return exact_count, reduction_count, vandermonde_count


def ceil_log2(n):
    assert n > 0
    return (n - 1).bit_length()


def first_prime_above(n):
    for candidate in range(n + 1, 2 * n + 1):
        if all(candidate % d for d in range(2, isqrt(candidate) + 1)):
            return candidate
    raise AssertionError("Bertrand search failed")


def parameter_controls():
    samples = []
    for target_j in range(0, 257):
        J = target_j + 2
        p = first_prime_above(100 * J)
        h = 2 * p - 1
        L = 100 * J
        u = 1 << ceil_log2((1 << 30) * J ** 6)
        log_cr = (p + 1) * (1 + (p - 1) * ceil_log2(h))
        t_i = max(1, (u + 1 + log_cr + p * p - 1) // (p * p))
        log_d_i = 1 + ceil_log2(h) + h * t_i
        log_lambda_i = (p + 1) * h + p * t_i + p * (p - 1) * ceil_log2(t_i)
        # 64 D(1+lambda) per pencil, <=40 sqrt(m(u+2)) stages;
        # factor 4 covers repair, split padding, and occupied reserves.
        log_contraction_i = u // 2 + ceil_log2(u + 2) + 8 + 6 + log_d_i + 1 + log_lambda_i + 2
        assert 2 * J * log_contraction_i <= (J + 1) * u - 2 * J
        t_f = (2 * (u + 1) + L - 1) // L
        log_d_f = 1 + ceil_log2(L) + t_f
        log_calls_f = u // 2 + ceil_log2(u + 2) + 8 + 4 + log_d_f + L * ceil_log2(t_f + 2) + 1
        assert 2 * J * log_calls_f <= (J + 1) * (u + 1) - 2 * J
        assert h * h * t_i <= 5 * u
        assert L * t_f <= 3 * u
        if target_j in (0, 1, 2, 8, 32, 128, 256):
            samples.append({"j": target_j, "p": p, "L": L, "u": u,
                            "interchange_margin_log2_lower": ((J + 1) * u - 2 * J * log_contraction_i) // (2 * J),
                            "fourier_margin_log2_lower": ((J + 1) * (u + 1) - 2 * J * log_calls_f) // (2 * J)})
    return 257, samples


def main():
    exact, reductions, vandermonde = cyclotomic_controls()
    root = matrix_root_controls()
    parameter_count, samples = parameter_controls()
    report = {"status": "PASS", "scope": "finite algebra and conservative local-call invoices; no physical compiler test",
              "integer_cyclotomic_inverse_products": exact,
              "odd_characteristic_inverse_checks": reductions,
              "vandermonde_inverse_entries_checked": vandermonde,
              "specialized_matrix_root_instances": root,
              "target_parameter_invoices": parameter_count,
              "parameter_samples": samples}
    path = Path(__file__).with_name("scalar-generator-review-verification.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
