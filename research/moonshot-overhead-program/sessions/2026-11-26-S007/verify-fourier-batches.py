#!/usr/bin/env python3
"""Exact finite specialization and independent-row tests for the ternary repair.

The test uses actual primitive ninth and twenty-seventh roots over GF(4).
The small W, s and axis counts are examples of the general written proof.
"""

import itertools
import json
import random
from functools import cache, reduce
from operator import xor


class CyclotomicField:
    """F4[t]/(t^e - omega), base coefficients in increasing degree."""

    def __init__(self, degree):
        self.degree = degree
        self.size = 4**degree
        self.even_mask = sum(1 << (2 * i) for i in range(degree))
        self.mask = self.size - 1

    def times_omega(self, a):
        low = a & self.even_mask
        high = (a >> 1) & self.even_mask
        return high | ((low ^ high) << 1)

    def scale(self, a, base_scalar):
        if base_scalar < 2:
            return a if base_scalar else 0
        result = self.times_omega(a)
        return result ^ a if base_scalar == 3 else result

    def mul(self, a, b):
        if a < 4:
            return self.scale(b, a)
        if b < 4:
            return self.scale(a, b)
        out = 0
        while b:
            out ^= self.scale(a, b & 3)
            b >>= 2
            leading = a >> (2 * (self.degree - 1))
            a = ((a << 2) & self.mask) ^ self.times_omega(leading)
        return out

    def power(self, a, k):
        value = 1
        while k:
            if k & 1:
                value = self.mul(value, a)
            a = self.mul(a, a)
            k //= 2
        return value

    @cache
    def inverse(self, a):
        assert a
        result = self.power(a, self.size - 2)
        assert self.mul(a, result) == 1
        return result

    def dot(self, coefficients, values):
        return reduce(xor, (self.mul(c, v) for c, v in zip(coefficients, values, strict=True)), 0)

    def inverse_matrix(self, matrix):
        n = len(matrix)
        table = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
        for j in range(n):
            pivot = next(i for i in range(j, n) if table[i][j])
            table[j], table[pivot] = table[pivot], table[j]
            factor = self.inverse(table[j][j])
            table[j] = [self.mul(x, factor) for x in table[j]]
            for i in range(n):
                if i != j and table[i][j]:
                    factor = table[i][j]
                    table[i] = [a ^ self.mul(factor, b) for a, b in zip(table[i], table[j], strict=True)]
        return [row[n:] for row in table]


def transpose(rows):
    return list(map(list, zip(*rows, strict=True)))


class Repair:
    def __init__(self, field, width, support_limit):
        self.field = field
        self.width = width
        self.limit = support_limit
        self.nodes = [field.power(4, i) for i in range(width)]
        assert len(set(self.nodes)) == width
        self.checks = [[field.power(node, i) for node in self.nodes] for i in range(support_limit)]
        self.checks_transposed = transpose(self.checks)

    @cache
    def inverse_minor(self, support):
        size = len(support)
        assert size <= self.limit
        return self.field.inverse_matrix([[self.checks[i][j] for j in support] for i in range(size)])

    def table(self, support, p, z, errors, wrong_right_inverse=False):
        size = len(support)
        if not size:
            return [0] * self.limit
        field = self.field
        inv = self.inverse_minor(support)
        error_values = [field.dot(row, errors[:size]) for row in inv]
        # g(y) = y^4 and (g(y)-z)/(y-z)^2 = (y-z)^2 in characteristic two.
        target = [field.mul(field.power(p[j] ^ z, 2), e) for j, e in zip(support, error_values, strict=True)]
        right = inv if wrong_right_inverse else transpose(inv)
        return [field.dot(row, target) for row in right] + [0] * (self.limit - size)

    def on_frequency(self, support, p, z, data, wrong_right_inverse=False):
        field = self.field
        predicted = [field.mul(a, x) for a, x in zip(p, data, strict=True)]
        errors = [field.dot(h, predicted) ^ field.mul(z, field.dot(h, data)) for h in self.checks]
        a = self.table(support, p, z, errors, wrong_right_inverse)
        correction = [field.dot(h, a) for h in self.checks_transposed]
        return [field.mul(field.power(pi, 4), x) ^ field.mul(pi ^ z, v)
                for pi, x, v in zip(p, data, correction, strict=True)]


def trits(x, digits):
    out = []
    for _ in range(digits):
        x, digit = divmod(x, 3)
        out.append(digit)
    return out


def fourier_matrix(digits, sign):
    labels = [trits(i, digits) for i in range(3**digits)]
    roots = [1, 2, 3]
    return [[roots[(sign * sum(a*b for a,b in zip(i,j,strict=True))) % 3] for j in labels] for i in labels]


def transform(row, field, matrix):
    return [field.dot(weights, row) for weights in matrix]


def compose_rows(checks, rows, field):
    values = transpose(rows)
    return [[field.dot(check, column) for column in values] for check in checks]


def test_field(degree, width, digits, seed):
    field = CyclotomicField(degree)
    order = 3 * degree
    assert field.power(4, degree) == 2 and field.power(4, order) == 1
    assert all((4**i - 1) % order for i in range(1, degree))
    assert (4**degree - 1) % order == 0
    repair = Repair(field, width, 2)
    rng = random.Random(seed)
    support_sets = [s for size in range(3) for s in itertools.combinations(range(width), size)]
    e_columns = packed_columns = negative_transpose = 0
    for serial, support in enumerate(support_sets):
        z = [1, 2, 3][serial % 3]
        p = [z] * width
        for j in support:
            p[j] = rng.randrange(4, field.size)
        for i in range(width):
            basis = [0] * width
            basis[i] = 1
            result = repair.on_frequency(support, p, z, basis)
            assert result == [field.mul(z, v) for v in basis]
            e_columns += 1
            if len(support) == 2:
                negative_transpose += repair.on_frequency(support, p, z, basis, True) != result
        if support == (0, 1):
            for i, power, base_bit in itertools.product(range(width), range(degree), [1, 2]):
                basis = [0] * width
                basis[i] = base_bit << (2 * power)
                assert repair.on_frequency(support, p, z, basis) == [field.mul(z, v) for v in basis]
                packed_columns += 1
    assert negative_transpose > 0
    data = [1] + [0] * (width-1)
    assert repair.on_frequency((), [4] + [1] * (width-1), 1, data) != data

    n = 3**digits
    forward = fourier_matrix(digits, 1)
    backward = fourier_matrix(digits, -1)
    z = [[1, 2, 3][(i + sum(trits(i, digits))) % 3] for i in range(n)]
    supports = [tuple(sorted(rng.sample(range(width), i % 3))) for i in range(n)]
    predictors = [[rng.randrange(4, field.size) if j in supports[i] else z[i] for i in range(n)] for j in range(width)]
    base_rows = [[rng.randrange(4) for _ in range(n)] for _ in range(width * degree)]
    x = [[sum(base_rows[j*degree + h][i] << (2*h) for h in range(degree)) for i in range(n)] for j in range(width)]

    def prediction(rows):
        result = []
        for p, row in zip(predictors, rows, strict=True):
            spectral = transform(row, field, forward)
            result.append(transform([field.mul(a, b) for a, b in zip(p, spectral, strict=True)], field, backward))
        return result

    px = prediction(x)
    hx = [transform(row, field, forward) for row in compose_rows(repair.checks, x, field)]
    hpx = [transform(row, field, forward) for row in compose_rows(repair.checks, px, field)]
    spectral_a = [[0] * n for _ in range(repair.limit)]
    for i in range(n):
        error = [hpx[j][i] ^ field.mul(z[i], hx[j][i]) for j in range(repair.limit)]
        a = repair.table(supports[i], [p[i] for p in predictors], z[i], error)
        for j, value in enumerate(a):
            spectral_a[j][i] = value
    a_time = [transform(row, field, backward) for row in spectral_a]
    za_time = [transform([field.mul(zi, ai) for zi, ai in zip(z, row, strict=True)], field, backward) for row in spectral_a]
    z_rows = compose_rows(repair.checks_transposed, a_time, field)
    fz_rows = compose_rows(repair.checks_transposed, za_time, field)
    fourth_power = prediction(prediction(prediction(px)))
    pz = prediction(z_rows)
    answer = [[a ^ b ^ c for a,b,c in zip(u,v,w,strict=True)] for u,v,w in zip(fourth_power,pz,fz_rows,strict=True)]
    for j, row in enumerate(base_rows):
        spectral = transform(row, field, forward)
        expected = transform([field.mul(a,b) for a,b in zip(spectral,z,strict=True)], field, backward)
        packed_row, power = divmod(j, degree)
        actual = [(v >> (power*2)) & 3 for v in answer[packed_row]]
        assert expected == actual
    return dict(extension_degree=degree, primitive_root_order=order, extension_rows=width, base_rows=width*degree,
                support_sets=len(support_sets), extension_unit_columns=e_columns, independent_binary_columns=packed_columns,
                wrong_right_inverse_detected=negative_transpose, missing_support_detected=True,
                trit_axis_digits=digits, independently_transformed_base_entries=width*degree*n)


if __name__ == '__main__':
    print(json.dumps([test_field(3, 7, 2, 1714), test_field(9, 10, 3, 7183)], indent=2))
