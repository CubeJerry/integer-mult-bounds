#!/usr/bin/env python3
"""Exact finite SR1--SR4 checks. Not a physical-machine or asymptotic proof."""
import itertools
import json
import math
from pathlib import Path
import random

MOD = 0b10011  # x^4+x+1, irreducible over F2 (checked below).
def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= MOD
    return out

def power(a, k):
    out = 1
    while k:
        if k & 1:
            out = mul(out, a)
        a = mul(a, a)
        k >>= 1
    return out

def inv(a):
    assert a
    return power(a, 14)

def add(xs):
    out = 0
    for x in xs:
        out ^= x
    return out

def matvec(a, x):
    return [add(mul(v, w) for v, w in zip(row, x)) for row in a]

def transpose(a):
    return [list(row) for row in zip(*a)]

def inverse(a):
    n = len(a)
    aug = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = inv(aug[col][col])
        aug[col] = [mul(scale, x) for x in aug[col]]
        for i in range(n):
            if i != col and aug[i][col]:
                q = aug[i][col]
                aug[i] = [x ^ mul(q, y) for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug]

def binomial(a, h):
    if a >= 0:
        return math.comb(a, h) if h <= a else 0
    return (-1) ** h * math.comb(h-a-1, h)


def repair(h, p, z, jset, x, wrong_transpose=False, wrong_gap=False):
    ell = len(jset)
    y = [0] * len(h)
    if ell:
        v = [[row[j] for j in jset] for row in h[:ell]]
        a = matvec(h, x)
        b = matvec(h, [mul(pi, xi) for pi, xi in zip(p, x)])
        delta = [bi ^ mul(z, ai) for ai, bi in zip(a[:ell], b[:ell])]
        e = matvec(inverse(v), delta)
        w = [mul(1 if wrong_gap else power(p[j] ^ z, 2), ei) for j, ei in zip(jset, e)]
        y[:ell] = matvec(inverse(v if wrong_transpose else transpose(v)), w)
    zz = matvec(transpose(h), y)
    return [mul(pi, xi) ^ mul(pi, zi) ^ mul(z, zi) for pi, xi, zi in zip(p, x, zz)]


def main():
    assert all(mul(a, inv(a)) == 1 for a in range(1, 16))
    omega = next(a for a in range(2, 16) if power(a, 2) ^ a ^ 1 == 0)
    small = [0, 1, omega, power(omega, 2)]
    counts = dict(field_unit_checks=15, signed_truncations=0,
                  all_count_phase_cases=0, full_basis_repairs=0,
                  zero_gap_supersets=0, wrong_transpose_rejections=0,
                  wrong_gap_rejections=0, outside_F4_rejections=0)
    for t in range(1, 7):
        width = 1 << t
        for a in range(-192, 193):
            value = add(power(omega ^ 1, h) for h in range(width) if binomial(a, h) & 1)
            assert value == power(omega, (a % width) % 3)
            counts['signed_truncations'] += 1
            for phase in range(3):
                assert mul(power(omega, phase), value) == power(omega, (phase + a % width) % 3)
                counts['all_count_phase_cases'] += 1
    rng = random.Random(20261126)
    for bsize, s in [(3, 1), (5, 2), (8, 3), (16, 4)]:
        h = [[power(node, i) for node in range(bsize)] for i in range(s)]
        cases = [(ell, tuple(js)) for ell in range(s+1)
                 for js in itertools.islice(itertools.combinations(range(bsize), ell), 24)]
        for ell, js in cases:
            for z in small[1:]:
                for trial in range(4):
                    p = [z] * bsize
                    for j in js:
                        p[j] = small[(trial+j) % 4]
                    if any(p[j] == z for j in js):
                        counts['zero_gap_supersets'] += 1
                    for col in range(bsize):
                        x = [int(i == col) for i in range(bsize)]
                        target = [mul(z, xi) for xi in x]
                        assert repair(h, p, z, js, x) == target
                        counts['full_basis_repairs'] += 1
                        if ell >= 2 and repair(h, p, z, js, x, wrong_transpose=True) != target:
                            counts['wrong_transpose_rejections'] += 1
                        if repair(h, p, z, js, x, wrong_gap=True) != target:
                            counts['wrong_gap_rejections'] += 1
        for _ in range(24):
            z = rng.choice(small[1:]); j = rng.randrange(bsize)
            p = [z] * bsize
            p[j] = rng.choice([a for a in range(16) if a not in small])
            x = [int(i == j) for i in range(bsize)]
            assert repair(h, p, z, [j], x) != [mul(z, xi) for xi in x]
            counts['outside_F4_rejections'] += 1
    assert counts['wrong_transpose_rejections'] > 0
    assert counts['wrong_gap_rejections'] > 0
    result = {'status':'PASS_EXACT_FINITE_SR_IDENTITIES', 'counts':counts,
              'field_modulus':MOD, 'omega':omega,
              'scope':'Finite signed-count formulas and full-basis small repair matrices over F16, including containing zero-gap sets and negative controls. Not Turing-machine execution, asymptotic proof, or formal verification.'}
    Path(__file__).with_name('spectral-repair-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
