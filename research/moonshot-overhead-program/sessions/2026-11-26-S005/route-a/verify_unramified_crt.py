#!/usr/bin/env python3
"""Exact finite ring/CRT/precision/setup checks, not a fast CRT implementation."""
from hashlib import sha256
from pathlib import Path
import json
import random


def gf_rem(value, divisor):
    d = divisor.bit_length()-1
    while value and value.bit_length()-1 >= d:
        value ^= divisor << (value.bit_length()-1-d)
    return value


def gf_mul(a, b, modulus):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return gf_rem(result, modulus)


def irreducibles(d):
    return [f for f in range(1 << d, 1 << (d+1))
            if not any(gf_rem(f, g) == 0
                       for e in range(1, d//2+1)
                       for g in range(1 << e, 1 << (e+1)))]


def coeffs(bits):
    return [(bits >> j) & 1 for j in range(bits.bit_length())]


def poly_mul(a, b, modulus):
    out = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = (out[i+j]+x*y) % modulus
    return out


def poly_rem(a, g, modulus):
    out = [x % modulus for x in a]
    d = len(g)-1
    out += [0] * max(0, d-len(out))
    for j in range(len(out)-1, d-1, -1):
        value = out[j]
        for i in range(d+1):
            out[j-d+i] = (out[j-d+i]-value*g[i]) % modulus
    return out[:d]


def inverse_matrix(a, modulus):
    n = len(a)
    rows = [[x % modulus for x in row] + [int(i == j) for j in range(n)]
            for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j] & 1)
        rows[j], rows[pivot] = rows[pivot], rows[j]
        unit = pow(rows[j][j], -1, modulus)
        rows[j] = [(x*unit) % modulus for x in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                scale = rows[i][j]
                rows[i] = [(x-scale*y) % modulus for x, y in zip(rows[i], rows[j])]
    assert all(rows[i][j] == (i == j) for i in range(n) for j in range(n))
    return [row[n:] for row in rows]


def matvec(a, v, modulus):
    return [sum(x*y for x, y in zip(row, v)) % modulus for row in a]


def factor_list(b):
    return [coeffs(g) for d in range(1, b+1) if b % d == 0
            for g in irreducibles(d)]


def crt_matrix(b, h):
    modulus, q = 1 << h, 1 << b
    factors = factor_list(b)
    columns = [sum((poly_rem([0]*j+[1], g, modulus) for g in factors), [])
               for j in range(q)]
    return [list(row) for row in zip(*columns)]


def residue_product(x, y, factors, modulus):
    out, position = [], 0
    for g in factors:
        d = len(g)-1
        out += poly_rem(poly_mul(x[position:position+d], y[position:position+d], modulus),
                        g, modulus)
        position += d
    return out


def lyndon_up_to(d):
    word = [-1]
    while word:
        word[-1] += 1
        yield tuple(word)
        length = len(word)
        while len(word) < d:
            word.append(word[-length])
        while word and word[-1] == 1:
            word.pop()


def rank_binary(values):
    pivots = {}
    for x in values:
        while x:
            p = x.bit_length()-1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)


def conjugates(gamma, d, modulus):
    out = [gamma]
    for _ in range(1, d):
        out.append(gf_mul(out[-1], out[-1], modulus))
    return out


def field_poly_mul_packed(a, b, d, modulus):
    stride = 2*d-1
    digit = (max(len(a), len(b))*d+1).bit_length()+1
    def pack(values):
        return sum(((value >> j) & 1) << (digit*(i*stride+j))
                   for i, value in enumerate(values) for j in range(d))
    product, mask = pack(a)*pack(b), (1 << digit)-1
    out = []
    for i in range(len(a)+len(b)-1):
        binary = sum(((product >> (digit*(i*stride+j))) & mask & 1) << j
                     for j in range(2*d-1))
        out.append(gf_rem(binary, modulus))
    return out


def field_poly_mul_direct(a, b, modulus):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] ^= gf_mul(x, y, modulus)
    return out


def run():
    rng = random.Random(26110577)
    counts = dict(factor_degree_identities=0, full_ring_inverses=0,
                  arbitrary_payload_roundtrips=0, quotient_products=0,
                  forward_precision_lifts=0, inverse_precision_lifts=0,
                  omitted_carry_failures=0, literal_lift_controls=0,
                  integer_products=0, lyndon_factors=0, packed_field_products=0)
    cache = {}
    def matrices(b, h):
        key = (b, h)
        if key not in cache:
            a = crt_matrix(b, h)
            cache[key] = a, inverse_matrix(a, 1 << h)
        return cache[key]
    for b in range(1, 6):
        q = 1 << b
        factors = factor_list(b)
        assert sum(len(g)-1 for g in factors) == q
        product2 = [1]
        for g in factors:
            product2 = poly_mul(product2, g, 2)
        expected = [0]*(q+1)
        expected[1] = expected[q] = 1
        assert product2 == expected
        counts['factor_degree_identities'] += 1
        for h in [1, 2, 3, 4, 8]:
            mod = 1 << h
            a, inv = matrices(b, h)
            for j in range(q):
                unit = [int(i == j) for i in range(q)]
                assert matvec(inv, matvec(a, unit, mod), mod) == unit
            counts['full_ring_inverses'] += 1
            p = [1]
            for g in factors:
                p = poly_mul(p, g, mod)
            if b >= 2 and h >= 2:
                binomial = [0]*(q+1)
                binomial[1], binomial[q] = mod-1, 1
                assert p != binomial
                counts['literal_lift_controls'] += 1
            for _ in range(8):
                x = [rng.randrange(mod) for _ in range(q)]
                y = [rng.randrange(mod) for _ in range(q)]
                rx, ry = matvec(a, x, mod), matvec(a, y, mod)
                assert matvec(inv, rx, mod) == x
                assert matvec(a, matvec(inv, y, mod), mod) == y
                counts['arbitrary_payload_roundtrips'] += 2
                actual = matvec(inv, residue_product(rx, ry, factors, mod), mod)
                assert actual == poly_rem(poly_mul(x, y, mod), p, mod)
                counts['quotient_products'] += 1
        for t in [1, 2, 4]:
            mod, mod2 = 1 << t, 1 << (2*t)
            a, inv = matrices(b, t)
            a2, inv2 = matrices(b, 2*t)
            for _ in range(12):
                f0 = [rng.randrange(mod) for _ in range(q)]
                f1 = [rng.randrange(mod) for _ in range(q)]
                low, whole0 = matvec(a, f0, mod), matvec(a2, f0, mod2)
                carry = [x // mod for x in whole0]
                assert [x % mod for x in whole0] == low
                other = matvec(a, f1, mod)
                predicted = [x+mod*((c+y) % mod) for x, c, y in zip(low, carry, other)]
                full = [x+mod*y for x, y in zip(f0, f1)]
                assert predicted == matvec(a2, full, mod2)
                counts['forward_precision_lifts'] += 1
                y = [rng.randrange(mod2) for _ in range(q)]
                y0, y1 = [x % mod for x in y], [x // mod for x in y]
                z0 = matvec(inv, y0, mod)
                zcarry = [x // mod for x in matvec(a2, z0, mod2)]
                z1 = matvec(inv, [(x-c) % mod for x, c in zip(y1, zcarry)], mod)
                recovered = [x+mod*z for x, z in zip(z0, z1)]
                assert recovered == matvec(inv2, y, mod2)
                counts['inverse_precision_lifts'] += 1
                wrong1 = matvec(inv, y1, mod)
                if [x+mod*z for x, z in zip(z0, wrong1)] != recovered:
                    counts['omitted_carry_failures'] += 1
    for n in [2, 3, 7, 15, 31, 63, 127, 255]:
        digit = (n+1).bit_length()
        length = (n+digit-1)//digit
        b = (2*length-1).bit_length()
        q = 1 << b
        h0 = 2*digit + length.bit_length()+2
        h = 1 << (h0-1).bit_length()
        mod = 1 << h
        a, inv = matrices(b, h)
        factors = factor_list(b)
        for _ in range(12):
            x, y = rng.randrange(1 << n), rng.randrange(1 << n)
            xc = [(x >> (digit*j)) & ((1 << digit)-1) for j in range(q)]
            yc = [(y >> (digit*j)) & ((1 << digit)-1) for j in range(q)]
            rx, ry = matvec(a, xc, mod), matvec(a, yc, mod)
            z = matvec(inv, residue_product(rx, ry, factors, mod), mod)
            assert sum(c << (digit*j) for j, c in enumerate(z)) == x*y
            counts['integer_products'] += 1
    for d in range(1, 8):
        target = set(irreducibles(d))
        field = min(target)
        alpha = next(x for x in range(1 << d)
                     if rank_binary(conjugates(x, d, field)) == d)
        normal = conjugates(alpha, d, field)
        generated = set()
        for word in lyndon_up_to(d):
            if len(word) != d:
                continue
            gamma = 0
            for bit, vector in zip(word, normal):
                if bit:
                    gamma ^= vector
            orbit = conjugates(gamma, d, field)
            assert len(set(orbit)) == d
            level = [[root, 1] for root in orbit]
            while len(level) > 1:
                next_level = []
                for j in range(0, len(level), 2):
                    if j+1 == len(level):
                        next_level.append(level[j])
                    else:
                        packed = field_poly_mul_packed(level[j], level[j+1], d, field)
                        assert packed == field_poly_mul_direct(level[j], level[j+1], field)
                        counts['packed_field_products'] += 1
                        next_level.append(packed)
                level = next_level
            assert all(x in [0, 1] for x in level[0])
            polynomial = sum(x << j for j, x in enumerate(level[0]))
            assert polynomial not in generated
            generated.add(polynomial)
            counts['lyndon_factors'] += 1
        assert generated == target
    assert counts['omitted_carry_failures'] > 0
    return counts


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    receipt = {'status': 'passed', 'deterministic_seed': 26110577,
               'exact_arithmetic': 'integers modulo powers of two and GF(2) polynomials',
               'checks': run(),
               'scope': 'Finite exact CRT, full-dimensional inverses, precision carry, integer recovery and factor-generation identities. Brute-force setup and dense CRT are test oracles, not the claimed fast suppliers, tape timing or a formal proof.',
               'files': {name: sha256((root/name).read_bytes()).hexdigest()
                         for name in ['verify_unramified_crt.py',
                                      'unramified-polynomial-crt-caller.md',
                                      'binary-factor-stream-compiler.md']}}
    (root/'unramified-crt-verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
