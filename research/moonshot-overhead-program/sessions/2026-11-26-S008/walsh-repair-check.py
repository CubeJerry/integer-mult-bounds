#!/usr/bin/env python3
"""Compare the integer repair compiler against independent rational-Vandermonde elimination."""

from fractions import Fraction
from itertools import combinations
from math import comb, factorial, isqrt
from pathlib import Path
import json
import random
import subprocess


def newton(count, low, degree):
    coefficient = 1
    total = 1
    power = 1
    for h in range(1, degree + 1):
        coefficient, remainder = divmod(coefficient * (count - low - h + 1), h)
        assert remainder == 0
        power *= -2
        total += coefficient * power
    return total


def independent_newton(count, low, degree):
    n = count - low
    return sum((-2)**h * (comb(n, h) if n >= h else
               0 if n >= 0 else (-1)**h * comb(h-n-1, h))
               for h in range(degree + 1))


def template(y):
    W = 1 << y
    m = W - 1
    radius = isqrt(4*m-1)+1
    low = m // 2 - radius
    degree = 2*radius + 1
    values = [newton(c, low, degree) for c in range(W)]
    assert values == [independent_newton(c, low, degree) for c in range(W)]
    gap_product = 1
    for p in values:
        for gamma in (1, -1):
            for z in (1, -1):
                gap_product *= abs(gamma*p-z) or 1
    F = factorial(m)
    vandermonde_denom = F * F * gap_product
    v = (y+1).bit_length()  # ceil(log2(y+2))
    b = 1
    while b*b*v < y:
        b += 1
    t = b
    common_multiple = 2 * (2**t * factorial(t)) * (2*factorial(degree)) * W**(W//16) * vandermonde_denom
    Wbits = 8*W*W*(y+2)
    assert common_multiple.bit_length() <= 5*W*W*(y+2)
    masks = [sum(((t & i).bit_count() % 2) << (i-1) for i in range(1, W))
             for t in range(W)]
    return degree, low, values, gap_product, F, vandermonde_denom, common_multiple, Wbits, masks


def actual_defects(key, masks, low, values):
    z = -1 if key.bit_count() % 2 else 1
    rows, gaps = [], []
    for i, mask in enumerate(masks):
        gamma = -1 if (low-mask.bit_count()) % 2 else 1
        gap = gamma*values[(key ^ mask).bit_count()] - z
        if gap:
            rows.append(i)
            gaps.append(gap)
    return rows, gaps


def scaled_rows(W, indices):
    F = factorial(W-1)
    result = []
    for i in indices:
        coefs = [1]
        divisor = 1
        for j in indices:
            if i == j:
                continue
            divisor *= i-j
            coefs = [-j*c + W*d for c,d in zip(coefs+[0], [0]+coefs)]
        assert F % divisor == 0
        result.append([c*(F//divisor) for c in coefs])
    return result


def integer_matrix(W, indices, gaps, gap_product):
    rows = scaled_rows(W, indices)
    for g in gaps:
        assert gap_product % g == 0
    return [[sum(row[r]*row[s]*(gap_product//g) for row,g in zip(rows, gaps))
             for s in range(len(rows))] for r in range(len(rows))]


def invert_raw(A):
    n = len(A)
    matrix = [a[:] + [Fraction(i == j) for j in range(n)] for i,a in enumerate(A)]
    for c in range(n):
        pivot = next(i for i in range(c, n) if matrix[i][c])
        matrix[c], matrix[pivot] = matrix[pivot], matrix[c]
        z = matrix[c][c]
        matrix[c] = [v/z for v in matrix[c]]
        for i in range(n):
            if i != c:
                f = matrix[i][c]
                matrix[i] = [a-f*b for a,b in zip(matrix[i], matrix[c])]
    return [row[n:] for row in matrix]


def verify():
    rng = random.Random(2037)
    counts = {'keys': 0, 'empty': 0, 'nonempty': 0, 'max_actual_defects': 0,
              'exact_table_entries': 0, 'exact_lagrange_entries': 0,
              'arbitrary_sets': 0, 'physical_real_coefficients': 0}
    physical = []
    for y in (6, 7, 8):
        W = 1 << y
        m = W-1
        degree, low, values, G, F, scale, D, width, masks = template(y)
        # Select actual keys at the center of a few mutually separated shift words.
        keys = {0, (1 << m)-1, *masks[:5]}
        for t,u in combinations(range(7), 2):
            diff = masks[t] ^ masks[u]
            bits = [i for i in range(m) if (diff >> i) & 1]
            keys.add(masks[t] ^ sum(1 << i for i in bits[::2]))
            for _ in range(3):
                keys.add(masks[t] ^ sum(1 << i for i in rng.sample(bits, len(bits)//2)))
        for _ in range(12):
            keys.add(rng.getrandbits(m))
        for key in sorted(keys):
            J, gaps = actual_defects(key, masks, low, values)
            n = len(J)
            assert n <= W//16
            counts['keys'] += 1
            counts['empty' if not n else 'nonempty'] += 1
            counts['max_actual_defects'] = max(counts['max_actual_defects'], n)
            if not n:
                continue
            scaled = scaled_rows(W, J)
            V = [[Fraction(i, W)**r for i in J] for r in range(n)]
            H = invert_raw(V)
            assert scaled == [[F*c for c in row] for row in H]
            counts['exact_lagrange_entries'] += n*n
            mat = integer_matrix(W, J, gaps, G)
            assert sum(1 for _ in mat) == n
            for r in range(n):
                for s in range(n):
                    target = sum(H[i][r]*H[i][s]/gaps[i] for i in range(n))
                    assert Fraction(mat[r][s], scale) == target
                    assert D % target.denominator == 0
                    assert abs(mat[r][s]).bit_length() < width
                    counts['exact_table_entries'] += 1
                    # Price the real missing-prime case on the actual larger common modulus.
                    if y == 6 and key == 0 and r == s == 0:
                        assert target.denominator % 73 == 0
                        M = 1 + (1 << 104) * (2*D)
                        physical.append([hex(M-1), str(target.numerator), str(target.denominator),
                                         hex(M), M.bit_length(), max(1, abs(target.numerator).bit_length(),
                                                                   target.denominator.bit_length())])
        # Exercise factorial divisibility independently of the active small shift geometry.
        for n in (1, 2, 3, W//16):
            for _ in range(3):
                J = sorted(rng.sample(range(W), n))
                H = invert_raw([[Fraction(i,W)**r for i in J] for r in range(n)])
                assert scaled_rows(W,J) == [[F*c for c in row] for row in H]
                counts['arbitrary_sets'] += 1
    here = Path(__file__).resolve().parent
    check_module = (here / 'walsh-aligned-scalar.mjs').as_uri()
    child = 'import {checkScalar} from ' + json.dumps(check_module) + ';\n'
    child += '''import {readFileSync} from "node:fs";
for (const [x,a,b,M,K,B] of JSON.parse(readFileSync(0,"utf8"))) {
  checkScalar(BigInt(x),BigInt(a),BigInt(b),BigInt(M),K,B);
}'''
    subprocess.run(['node', '--input-type=module', '-e', child],
                   input=json.dumps(physical), text=True, check=True)
    counts['physical_real_coefficients'] = len(physical)
    counts['physical_modulus_bits'] = [case[4] for case in physical]
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    verify()
