#!/usr/bin/env python3
"""Exact integer/cyclotomic checks for the Bell outer-boundary identities."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent


def sign(x):
    return -1 if x.bit_count() & 1 else 1


def walsh(a):
    return [sum(sign(x & y) * value for x, value in enumerate(a)) for y in range(len(a))]


def encode_numerator(values, q):
    return [walsh([values[z * q + (z ^ u)] for z in range(q)]) for u in range(q)]


def decode_numerator(encoded, q):
    out = [0] * (q * q)
    for u in range(q):
        row = walsh(encoded[u])
        for z in range(q):
            out[z * q + (z ^ u)] = row[z]
    return out


counts = Counter()
for s in range(1, 6):
    q = 1 << s
    for seed in range(12):
        f = [((13 * j + 7 * seed + j * j) % 19) - 9 for j in range(q * q)]
        g = [((11 * j + 3 * seed + 2 * j * j) % 17) - 8 for j in range(q * q)]
        fn = encode_numerator(f, q)
        gn = encode_numerator(g, q)
        hn = encode_numerator([x * y for x, y in zip(f, g)], q)
        assert decode_numerator(fn, q) == [q * x for x in f]
        for u in range(q):
            for v in range(q):
                # Multiplying BO2 by sqrt(q) leaves q Hnum = Fnum*Gnum.
                assert q * hn[u][v] == sum(fn[u][w] * gn[u][v ^ w] for w in range(q))
                counts['exact_product_coordinates'] += 1
        counts['product_arrays'] += 1

        diagonal = [((5 * j + seed + 3 * j * j) % 23) - 11 for j in range(q * q)]
        encoded_input = [[((7 * v + 5 * u + seed) % 13) - 6 for v in range(q)] for u in range(q)]
        physical_num = decode_numerator(encoded_input, q)
        actual_num = encode_numerator([d * x for d, x in zip(diagonal, physical_num)], q)
        for u in range(q):
            kernel_num = walsh([diagonal[z * q + (z ^ u)] for z in range(q)])
            for v in range(q):
                # Both expressions are numerator of E^T D E; denominator q.
                assert actual_num[u][v] == sum(kernel_num[t] * encoded_input[u][v ^ t]
                                               for t in range(q))
                counts['exact_diagonal_coordinates'] += 1
        counts['diagonal_arrays'] += 1


# Literal entire matrix columns for all diagonals in a small family.
for s in range(1, 4):
    q = 1 << s
    for seed in range(4):
        diagonal = [((seed + 3) * j + j * j) % 7 - 3 for j in range(q * q)]
        kernels = [walsh([diagonal[z * q + (z ^ u)] for z in range(q)]) for u in range(q)]
        for u0 in range(q):
            for v0 in range(q):
                basis = [[int(u == u0 and v == v0) for v in range(q)] for u in range(q)]
                physical = decode_numerator(basis, q)
                actual = encode_numerator([d * x for d, x in zip(diagonal, physical)], q)
                expected = [[kernels[u][v ^ v0] if u == u0 else 0 for v in range(q)] for u in range(q)]
                assert actual == expected
                counts['literal_conjugated_matrix_columns'] += 1


# Q(omega), omega^2+omega+1=0, represented by exact rational pairs.
def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qneg(a):
    return (-a[0], -a[1])


def qmul(a, b):
    ac, cross, bd = a[0] * b[0], a[0] * b[1] + a[1] * b[0], a[1] * b[1]
    return (ac - bd, cross - bd)


def qconj(a):
    return (a[0] - a[1], -a[1])


one, zero, omega = (Fraction(1), Fraction(0)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(1))
omega2 = qmul(omega, omega)
assert qadd(qadd(one, omega), omega2) == zero
assert qmul(omega, omega2) == one
a = tuple(x / 2 for x in qadd(one, omega2))
b = tuple(x / 2 for x in qadd(one, qneg(omega2)))
assert a != zero and b != zero
assert a == (Fraction(0), Fraction(-1, 2))
assert b == (Fraction(1), Fraction(1, 2))
assert qadd(qmul(a, qconj(a)), qmul(b, qconj(b))) == one
assert qadd(qmul(a, qconj(b)), qmul(b, qconj(a))) == zero
counts['unitary_third_root_orbit_controls'] += 1


# Incorrect encoded pointwise product: disjoint physical supports.
f = [1, 0, 0, 0]
g = [0, 0, 0, 1]
fn, gn = encode_numerator(f, 2), encode_numerator(g, 2)
assert all(x * y == 0 for x, y in zip(f, g))
assert any(fn[u][v] * gn[u][v] for u in range(2) for v in range(2))
counts['encoded_pointwise_negative_controls'] += 1


# Explicit positive invoice, not a lower bound inferred from an upper bound.
for base in range(1, 9):
    value = Fraction(base)
    for depth in range(21):
        width = 1 << depth
        assert value == base * width
        assert value * value / width == base * base * width
        value *= 2
        counts['exact_full_volume_invoice_steps'] += 1
for A in (4, 16, 64, 256):
    for multiple in range(1, 8):
        b = isqrt(A) * multiple
        assert b * b == A * multiple * multiple
        mass_squared = Fraction((2 * b) ** 2, 2 * A)
        assert mass_squared == 2 * multiple * multiple
        counts['expanded_template_mass_checks'] += 1


proof = ROOT / 'bell-outer-boundary.md'
receipt = {
    'status': 'passed',
    'scope': 'BO2--BO4 exact identities and BO6--BO8 invoice arithmetic only',
    'utc': datetime.now(timezone.utc).isoformat(),
    'proof_sha256': sha256(proof.read_bytes()).hexdigest(),
    'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'counts': dict(sorted(counts.items())),
    'floating_point_fourier_or_spectral_tests': False,
    'missing_supplier': 'No improved Bell boundary, general phase executor, or encoded convolution is supplied.',
}
(ROOT / 'bell-outer-boundary-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
