#!/usr/bin/env python3
"""Replay the packed trace transform, physical FS1 order and prime-length Rader kernel."""

from collections import Counter
from pathlib import Path
from random import Random
import json
import runpy

AR = runpy.run_path(str(Path(__file__).with_name('verify-fibre-join.py')))
field_poly = AR['field_poly']
mul = AR['mul']
power = AR['power']
normal = AR['normal']
minpoly = AR['minpoly']
poly_eval = AR['field_poly_eval']
poly_product = AR['xor_product']
poly_div = AR['divmod_binary']


def parity(n):
    return n.bit_count() & 1


def trace(value, c, field):
    acc = 0
    for _ in range(c):
        acc ^= value
        value = mul(value, value, field)
    assert acc in (0, 1)
    return acc


def linear(rows, bits):
    return sum(parity(row & bits) << i for i, row in enumerate(rows))


def inverse(rows):
    n = len(rows)
    aug = [r | 1 << (n + j) for j, r in enumerate(rows)]
    for j in range(n):
        pivot = next(r for r in range(j, n) if (aug[r] >> j) & 1)
        aug[j], aug[pivot] = aug[pivot], aug[j]
        for r in range(n):
            if r != j and (aug[r] >> j) & 1:
                aug[r] ^= aug[j]
    mask = (1 << n) - 1
    assert [(v & mask) for v in aug] == [1 << i for i in range(n)]
    return [v >> n for v in aug]


def prime_divisors(n):
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
        while n % p == 0:
            n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def unit_generator_prime(p):
    fac = prime_divisors(p - 1)
    for a in range(1, p):
        if all(pow(a, (p - 1) // l, p) != 1 for l in fac):
            return a
    raise AssertionError(p)


def field_setup(c):
    field = field_poly(c)
    m = (1 << c) - 1
    primes = prime_divisors(m)
    zeta = next(a for a in range(1, 1 << c)
                if all(power(a, m // l, field) != 1 for l in primes))
    z = [1]
    for _ in range(1, m):
        z.append(mul(z[-1], zeta, field))
    assert sorted(z) == list(range(1, 1 << c))
    gamma = normal(c)[0]
    pairing = [sum(trace(mul(w, 1 << i, field), c, field) << i for i in range(c))
               for w in normal(c)]
    delta = linear(inverse(pairing), 1)
    assert [trace(mul(delta, w, field), c, field) for w in normal(c)] == [1] + [0] * (c - 1)
    assert trace(gamma, c, field) == trace(delta, c, field) == 1
    t = [trace(mul(gamma, v, field), c, field) for v in z]
    u = [trace(mul(delta, z[(-a) % m], field), c, field) for a in range(m)]
    return field, zeta, z, gamma, delta, t, u


def trace_rows(kernel):
    m = len(kernel)
    return [sum(kernel[(a * i) % m] << i for i in range(m)) for a in range(m)]


def selected_rows(rows, data):
    out = []
    for selectors in rows:
        value = 0
        while selectors:
            bit = selectors & -selectors
            value ^= data[bit.bit_length() - 1]
            selectors ^= bit
        out.append(value)
    return out


def rank_basis(c, alternate):
    if not alternate:
        return normal(c)
    field = field_poly(c)
    for a in reversed(range(1, 1 << c)):
        orbit = AR['orbit'](a, field)
        if len(orbit) == c and len(AR['basis_pivots'](orbit)) == c:
            return orbit
    raise AssertionError(c)


def duval_length(d):
    word = [-1]
    while word:
        word[-1] += 1
        size = len(word)
        if size == d:
            yield tuple(word)
        while len(word) < d:
            word.append(word[len(word) - size])
        while word and word[-1] == 1:
            word.pop()


def fs1(c, alternate):
    entries = []
    for d in range(1, c + 1):
        if c % d:
            continue
        basis = rank_basis(d, alternate)
        for word in duval_length(d):
            anchor = 0
            for bit, w in zip(word, basis):
                if bit:
                    anchor ^= w
            poly = minpoly(anchor, field_poly(d))
            entries.append(poly)
    assert len(entries) == len(set(entries))
    assert sum(p.bit_length() - 1 for p in entries) == 1 << c
    return entries


def directory(c, field, z, gamma, fs):
    m = len(z)
    by_poly = {2: (None, None, None)}
    for a0 in range(m):
        orbit = [a0]
        a = 2 * a0 % m
        while a != a0:
            orbit.append(a)
            a = 2 * a % m
        if a0 != min(orbit):
            continue
        d = len(orbit)
        poly = minpoly(z[a0], field)
        rows = [sum(trace(mul(gamma, power(z[a], i, field), field), c, field) << i
                    for i in range(d)) for a in orbit]
        assert poly not in by_poly and poly.bit_length() - 1 == d
        by_poly[poly] = orbit, rows, inverse(rows)
    assert set(by_poly) == set(fs)
    return [(poly, *by_poly[poly]) for poly in fs]


def forward(blocks, trace_matrix, fs):
    y = selected_rows(trace_matrix, [blocks[0] ^ blocks[-1], *blocks[1:-1]])
    payload = []
    for _, orbit, _, backward in fs:
        if orbit is None:
            payload.append([blocks[0]])
        else:
            payload.append(selected_rows(backward, [y[a] for a in orbit]))
    return payload


def backward(payload, inv_matrix, fs):
    m = len(inv_matrix)
    y = [None] * m
    zero = None
    for coeffs, (_, orbit, matrix, _) in zip(payload, fs):
        if orbit is None:
            zero = coeffs[0]
        else:
            for a, plane in zip(orbit, selected_rows(matrix, coeffs)):
                assert y[a] is None
                y[a] = plane
    assert zero is not None and all(v is not None for v in y)
    x = selected_rows(inv_matrix, y)
    return [zero, *x[1:], x[0] ^ zero]


def inverse_mod(a, h):
    b, x, y = h, 1, 0
    while b:
        q, r = poly_div(a, b)
        a, b, x, y = b, r, y, x ^ poly_product(q, y)
    assert a == 1
    return poly_div(x, h)[1]


def crt_idempotents(moduli, n):
    root_poly = (1 << n) | 2
    out = []
    for h in moduli:
        q, remainder = poly_div(root_poly, h)
        assert remainder == 0
        out.append(poly_product(q, inverse_mod(poly_div(q, h)[1], h)))
    return out


def lane(planes, l):
    return sum(((v >> l) & 1) << i for i, v in enumerate(planes))


def cyclic_conv(a, b, length):
    raw = poly_product(a, b)
    return (raw & ((1 << length) - 1)) ^ (raw >> length)


def rader(x, t, rho):
    m = len(t)
    length = m - 1
    seq = [pow(rho, j, m) for j in range(length)]
    assert sorted(seq) == list(range(1, m))
    coeffs = sum(((x >> seq[-j % length]) & 1) << j for j in range(length))
    kernel = sum(t[a] << j for j, a in enumerate(seq))
    circ = cyclic_conv(coeffs, kernel, length)
    out = parity(x) * t[0]
    for j, a in enumerate(seq):
        out |= (((circ >> j) & 1) ^ ((x & 1) * t[0])) << a
    return out


def main():
    rng = Random(0x51A70D)
    count = Counter()
    normal_directory_pairs = []
    for c in range(1, 10):
        n, m = 1 << c, (1 << c) - 1
        field, _, z, gamma, delta, t, u = field_setup(c)
        fwd, inv = trace_rows(t), trace_rows(u)
        for j in range(m):
            assert linear(inv, linear(fwd, 1 << j)) == (1 << j)
            assert linear(fwd, linear(inv, 1 << j)) == (1 << j)
            count['paired_trace_basis_columns_both_orders'] += 1
        if fwd != inv:
            assert any(linear(fwd, linear(fwd, 1 << j)) != (1 << j) for j in range(m))
            count['wrong_ordinary_self_inverse_control'] += 1
        for alternate in [False, True]:
            moduli = fs1(c, alternate)
            if not alternate:
                first_order = moduli
                assert moduli == AR['fs_order'](c)
            else:
                normal_directory_pairs.append(moduli != first_order)
            fs = directory(c, field, z, gamma, moduli)
            idems = crt_idempotents(moduli, n)
            width = n * n if c <= 5 else 11
            blocks = [rng.getrandbits(width) for _ in range(n)]
            payload = forward(blocks, fwd, fs)
            assert backward(payload, inv, fs) == blocks
            independent = [[rng.getrandbits(width) for _ in coeffs] for coeffs in payload]
            recovered = backward(independent, inv, fs)
            assert forward(recovered, fwd, fs) == independent
            for l in range(width):
                f = lane(blocks, l)
                direct = 0
                for h, coeffs, arbitrary, basis in zip(moduli, payload, independent, idems):
                    assert lane(coeffs, l) == poly_div(f, h)[1]
                    direct ^= poly_product(lane(arbitrary, l), basis)
                    count['literal_F2_remainder_words'] += 1
                assert lane(recovered, l) == poly_div(direct, (1 << n) | 2)[1]
                count['independent_idempotent_CRT_inversions'] += 1
            count['full_directory_forward_inverse_batches'] += 1
            count['full_H_equals_N_squared_batches'] += int(width == n * n)
            count['proper_nonzero_orbits'] += sum(orbit is not None and len(orbit) < c for _, orbit, _, _ in fs)
        if m > 1 and prime_divisors(m) == [m]:
            gen = unit_generator_prime(m)
            for test in [1 << i for i in range(m)] + [rng.getrandbits(m) for _ in range(7)]:
                assert rader(test, t, gen) == linear(fwd, test)
                assert rader(test, u, gen) == linear(inv, test)
                count['prime_Rader_each_direction'] += 1
    # A larger Mersenne prime checks both projected kernels against independent
    # field Horner at selected roots and checks all 8191 bits after inversion.
    c, m = 13, (1 << 13) - 1
    field, _, z, gamma, _, t, u = field_setup(c)
    gen = unit_generator_prime(m)
    x = rng.getrandbits(m)
    y = rader(x, t, gen)
    assert rader(y, u, gen) == x
    for a in [0, 1, m - 1] + [rng.randrange(m) for _ in range(18)]:
        assert (y >> a) & 1 == trace(mul(gamma, poly_eval(x, z[a], field), field), c, field)
        count['degree_13_prime_Rader_direct_Horner_probes'] += 1
    count['degree_13_prime_Rader_roundtrip_bits'] = m
    count['FS1_directory_pairs_with_different_order'] = sum(normal_directory_pairs)
    assert count['FS1_directory_pairs_with_different_order'] > 0
    print(json.dumps({'seed': '0x51a70d', 'full_degrees': list(range(1, 10)),
                      'prime_degrees': [2, 3, 5, 7, 13], 'counts': dict(sorted(count.items()))}, indent=2))


if __name__ == '__main__':
    main()
