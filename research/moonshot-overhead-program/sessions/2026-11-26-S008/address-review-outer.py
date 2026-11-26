#!/usr/bin/env python3
"""Independent finite replay of the occupied Fourier lift and the exact integer caller."""
from __future__ import annotations

import cmath
import math
from random import Random


def root(turns):
    return cmath.exp(2j * math.pi * turns)


def identity(size):
    return [[float(i == j) for j in range(size)] for i in range(size)]


def diagonal(values):
    size = len(values)
    return [[value if i == j else 0.0 for j in range(size)] for i, value in enumerate(values)]


def multiply(left, right):
    columns = tuple(zip(*right))
    return [[sum(x * y for x, y in zip(row, column)) for column in columns] for row in left]


def adjoint(matrix):
    return [[z.conjugate() for z in row] for row in zip(*matrix)]


def act(matrix, vector):
    return [sum(z * x for z, x in zip(row, vector)) for row in matrix]


def distance(left, right):
    return max(sum(abs(x - y) for x, y in zip(a, b)) for a, b in zip(left, right))


def fourier(size):
    return [[root((i * j % size) / size) / math.sqrt(size) for j in range(size)] for i in range(size)]


def radix_matrix(size):
    q = size.bit_length() - 1
    bit_reversal = [int(format(i, f"0{q}b")[::-1], 2) for i in range(size)]
    rows = [identity(size)[j] for j in bit_reversal]
    scale = 1 / math.sqrt(2)
    for level in range(1, q + 1):
        m = 1 << level
        half = m // 2
        twiddled = [list(row) for row in rows]
        for i in range(size):
            if i % m >= half:
                phase = root((i % half) / m)
                twiddled[i] = [phase * z for z in rows[i]]
        for base in range(0, size, m):
            for j in range(half):
                i = base + j
                left, right = twiddled[i], twiddled[i + half]
                rows[i] = [scale * (u + v) for u, v in zip(left, right)]
                rows[i + half] = [scale * (u - v) for u, v in zip(left, right)]
    return rows


def extend(matrix, size):
    result = identity(size)
    for i, row in enumerate(matrix):
        result[i][:len(row)] = row
    return result


def three_hadamards(lift):
    scale = 1 / math.sqrt(2)
    hadamard = [[scale, scale], [scale, -scale]]
    q = multiply(hadamard, lift)
    c, s = abs(q[0][0]), abs(q[0][1])
    g = q[0][0] / c
    din = diagonal([1., q[0][1] / (1j * s * g)])
    dout = diagonal([g, q[1][0] / (1j * s)])
    dmid = diagonal([c + 1j * s, c - 1j * s])
    actual = din
    for matrix in [hadamard, dmid, hadamard, dout, hadamard]:
        actual = multiply(matrix, actual)
    return distance(lift, actual)


def lifted_axis(a):
    r = 1 << ((2 * a - 2).bit_length())
    size = 2 * r
    q = math.sin(math.pi / 258)
    ur = extend(fourier(r), size)
    ua = fourier(a)
    lift = identity(size)
    smallest_denominator = 1.
    worst_pair = 0.
    for xi in range(r):
        lam = sum(root((-h * h * r + 2 * a * xi * h) % (2 * a * r) /
                       (2 * a * r)) for h in range(1 - a, a)) / math.sqrt(a)
        z = q * lam
        assert abs(z) < 0.5
        s = math.sqrt(1 - abs(z) ** 2)
        lift[xi][xi] = z
        lift[xi][r + xi] = lift[r + xi][xi] = s
        lift[r + xi][r + xi] = -z.conjugate()
        smallest_denominator = min(smallest_denominator, abs((z + s) / math.sqrt(2)),
                                   abs((s - z.conjugate()) / math.sqrt(2)))
        local = [[z, s], [s, -z.conjugate()]]
        worst_pair = max(worst_pair, three_hadamards(local), three_hadamards(adjoint(local)),
                         three_hadamards(identity(2)))
    d = diagonal([root(((j * j) % (2 * a)) / (2 * a)) if j < a else 1. for j in range(size)])
    v = multiply(d, multiply(adjoint(ur), multiply(lift, multiply(ur, d))))
    compression = [[v[i][j] for j in range(a)] for i in range(a)]
    assert distance(compression, [[q * z for z in row] for row in ua]) < 5e-13
    first = diagonal([-1. if j < a else 1. for j in range(size)])
    second = diagonal([1. if j < a else -1. for j in range(size)])
    rotation = multiply(v, multiply(second, multiply(adjoint(v), first)))
    for _ in range(6):
        rotation = multiply(rotation, rotation)
    b = multiply(rotation, v)
    leak = max(sum(abs(b[i][j]) for j in range(size) if (i < a) != (j < a)) for i in range(size))
    btop = [[b[i][j] for j in range(a)] for i in range(a)]
    assert distance(btop, ua) < 2e-11 and leak < 2e-11

    def chi(j):
        return root((j * j + (a % 2) * j) % (2 * a) / (2 * a))

    spectral = [sum(chi(h).conjugate() * root(xi * h % a / a) for h in range(a))
                / math.sqrt(a) for xi in range(a)]
    assert max(abs(abs(z) - 1) for z in spectral) < 4e-15
    din = diagonal([chi(-j) if j < a else 1. for j in range(size)])
    dout = diagonal([chi(j) if j < a else 1. for j in range(size)])
    ds = diagonal(spectral + [1.] * (size - a))
    restored = multiply(dout, multiply(adjoint(b), multiply(ds, multiply(b, din))))
    error = distance(restored, extend(ua, size))
    assert error < 3e-11 and worst_pair < 3e-15 and smallest_denominator > 0.25
    return restored, error, leak, worst_pair


def axis_fibres(shape, dim):
    step = math.prod(shape[:dim])
    width = shape[dim]
    for start in range(0, math.prod(shape), step * width):
        for low in range(step):
            yield [start + j * step + low for j in range(width)]


def borrowed(vector, shape, axis, a, lifted):
    fibres = list(axis_fibres(shape, axis))
    assert len(shape) in range(4, 8) and len(fibres) % 8 == 0
    v = len(fibres) // 8
    size = len(lifted)
    answer = list(vector)
    for start in range(0, len(fibres), v):
        active = fibres[start:start + v]
        donors = [i for fibre in fibres[:start] + fibres[start + v:] for i in fibre]
        assert len(donors) >= v * (size - a)
        for i, fibre in enumerate(active):
            extra = donors[i * (size - a):(i + 1) * (size - a)]
            indices = fibre[:a] + extra
            values = act(lifted, [answer[j] for j in indices])
            for j, value in zip(indices, values):
                answer[j] = value
    return answer


def exact_axis(vector, shape, axis, a):
    answer = list(vector)
    ua = fourier(a)
    for fibre in axis_fibres(shape, axis):
        indices = fibre[:a]
        for j, value in zip(indices, act(ua, [vector[t] for t in indices])):
            answer[j] = value
    return answer


def test_integer(lifts):
    axes = [3, 4, 5, 7]
    shape = [1 << ((a - 1).bit_length()) for a in axes]
    strides = [math.prod(shape[:i]) for i in range(len(shape))]
    p = [math.prod(axes[:i]) for i in range(len(axes))]
    mu = [pow(q, -1, a) for q, a in zip(p, axes)]
    volume, size = math.prod(shape), math.prod(axes)
    cyclic_addresses = [sum(s * (m * t % a) for s, m, a in zip(strides, mu, axes)) for t in range(size)]
    assert len(set(cyclic_addresses)) == size
    width = 6
    count = 73
    rand = Random(2026112608)
    terms = [[rand.randrange(2**width) for _ in range(count)] for _ in range(2)]
    expected = [sum(terms[0][j] * terms[1][t - j] for j in range(count) if 0 <= t - j < count)
                for t in range(size)]
    spectra = []
    for coefficients in terms:
        x = [0.] * volume
        for index, value in zip(cyclic_addresses, coefficients):
            x[index] = value
        for i, a in enumerate(axes):
            x = borrowed(x, shape, i, a, lifts[a])
        spectra.append(x)
    output = [x * y for x, y in zip(*spectra)]
    for i in reversed(range(len(axes))):
        a = axes[i]
        output = borrowed(output, shape, i, a, adjoint(lifts[a]))
    output = [math.sqrt(size) * z for z in output]
    maximum = max(abs(output[i] - true) for i, true in zip(cyclic_addresses, expected))
    assert maximum < 1e-6
    assert max(abs(output[i]) for i in set(range(volume)) - set(cyclic_addresses)) < 1e-7
    carry = 0
    out_digits = []
    for i in cyclic_addresses:
        coefficient = round(output[i].real)
        carry, digit = divmod(carry + coefficient, 2**width)
        out_digits.append(digit)
    assert carry == 0
    as_int = lambda ds: sum(z << (width * i) for i, z in enumerate(ds))
    assert as_int(out_digits) == as_int(terms[0]) * as_int(terms[1])
    return volume, size, maximum


def main():
    lifts = {}
    stats = []
    radix_error = max(distance(radix_matrix(n), fourier(n)) for n in (1, 2, 4, 8, 16, 32, 64))
    assert radix_error < 2e-13
    for a in [1, 2, 3, 4, 5, 7, 8, 9]:
        lifted, err, leak, pairerr = lifted_axis(a)
        stats.append((err, leak, pairerr))
        lifts[a] = lifted
    rand = Random(123)
    cases = 0
    occupied_error = 0.
    for a, shape, axis in [(2, [2, 2, 2, 2], 1), (3, [4, 4, 2, 2], 0),
                          (5, [2, 8, 2, 2, 2], 1), (7, [2, 2, 2, 2, 8, 2], 4),
                          (3, [2, 2, 2, 4, 2, 2, 2], 3)]:
        vec = [complex(rand.uniform(-1, 1), rand.uniform(-1, 1)) for _ in range(math.prod(shape))]
        target = exact_axis(vec, shape, axis, a)
        got = borrowed(vec, shape, axis, a, lifts[a])
        occupied_error = max(occupied_error, max(abs(x-y) for x, y in zip(got, target)))
        cases += 1
    assert occupied_error < 3e-11
    volume, size, integer_error = test_integer(lifts)
    print("eight axis lengths 1,2,3,4,5,7,8,9; maximum row-sum axis error %.3g, "
          "off-block leakage %.3g, three-H pair error %.3g" % tuple(map(max, zip(*stats))))
    print("seven explicit radix-two twiddle/H/bit-reversal transforms; maximum row-sum error %.3g" % radix_error)
    print("%d arbitrary occupied 4-7-axis blocks; maximum coordinate error %.3g" % (cases, occupied_error))
    print("%d padded records, %d valid points; independent convolution/carry product exact; "
          "maximum valid error %.3g" % (volume, size, integer_error))


if __name__ == "__main__":
    main()
