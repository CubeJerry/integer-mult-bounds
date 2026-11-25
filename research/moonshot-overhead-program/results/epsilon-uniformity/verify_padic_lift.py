#!/usr/bin/env python3
"""Exact finite checks for the literal p-adic label-lift obstruction.

These checks support the written proof. They do not construct the full
astronomically sized outer matrix or replay a multiplication implementation.
"""

from datetime import datetime, timezone
from itertools import product
from math import comb
from pathlib import Path
import json
import platform


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def coefficient(factors, degree):
    """Coefficient of z**degree in a product of (1+factor*z)."""
    out = [1] + [0] * degree
    for factor in factors:
        for j in range(degree, 0, -1):
            out[j] += factor * out[j - 1]
    return out[degree]


def inner_eigenvalue(h, distance, weight, q):
    return coefficient([-1] * weight + [q - 1] * (h - weight), distance)


def fwht(values):
    out = list(values)
    width = 1
    while width < len(out):
        for start in range(0, len(out), 2 * width):
            for j in range(start, start + width):
                a, b = out[j], out[j + width]
                out[j], out[j + width] = a + b, a - b
        width *= 2
    return out


def local_ring_invariants(matrix, p):
    """Count unit and p-valued Smith pivots using exact row/column steps."""
    modulus = p * p
    a = [[v % modulus for v in row] for row in matrix]
    n = len(a)
    k = 0
    while k < n:
        pivot = next(((i, j) for i in range(k, n) for j in range(k, n)
                      if a[i][j] % p), None)
        if pivot is None:
            break
        i, j = pivot
        a[k], a[i] = a[i], a[k]
        for row in a:
            row[k], row[j] = row[j], row[k]
        inverse = pow(a[k][k], -1, modulus)
        a[k] = [(v * inverse) % modulus for v in a[k]]
        for i in range(n):
            if i == k:
                continue
            scale = a[i][k]
            a[i] = [(v - scale * w) % modulus for v, w in zip(a[i], a[k])]
        # This column operation clears the pivot row and preserves other rows,
        # since the pivot column is now the k-th unit vector.
        for j in range(n):
            if j != k:
                a[k][j] = 0
        k += 1
    unit_count = k
    tail = [[a[i][j] // p for j in range(k, n)] for i in range(k, n)]
    r = 0
    for col in range(len(tail)):
        pivot = next((i for i in range(r, len(tail)) if tail[i][col] % p), None)
        if pivot is None:
            continue
        tail[r], tail[pivot] = tail[pivot], tail[r]
        inverse = pow(tail[r][col], -1, p)
        tail[r] = [(v * inverse) % p for v in tail[r]]
        for i in range(len(tail)):
            if i != r:
                scale = tail[i][col]
                tail[i] = [(v - scale * w) % p for v, w in zip(tail[i], tail[r])]
        r += 1
    return unit_count, r, n - unit_count - r


def main():
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 43]
    tested = 0
    large_q_cases = 0
    for p in primes:
        h = 2 * p - 1
        c = comb(h, p)
        beta = comb(h - 1, p - 1)
        require((c - 1) % (p * p) == 0, 'central-binomial congruence')
        require(beta % p == 0 and beta % (p * p) != 0, 'one p-adic digit')
        require((2 * p - 1) * beta == p * c, 'exact binomial relation')
        for q in [2, 4, 8, 16, 64, 256, 16384, 65536]:
            low = inner_eigenvalue(h, p, p - 1, q)
            high = inner_eigenvalue(h, p, h, q)
            eigen = 1 + coefficient([low] + [high] * (h - 1), p)
            require(high == -c, 'highest-weight inner eigenvalue')
            require((low + 1 - q**p) % p == 0, 'nonzero low-mode residue')
            require(eigen % p == 0 and eigen % (p * p) != 0, 'outer valuation one')
            require((eigen // p + q**p) % p == 0, 'outer divided residue')
            multiplicity = h * comb(h, p - 1) * (q - 1)**(h*h - p)
            order = q**(h*h)
            require(0 < multiplicity <= order, 'valid eigenspace multiplicity')
            if q >= 2 * h * h:
                require(multiplicity * q**p >= order, 'rank-fraction inequality')
                reserve_floor = (q - 1)**h - 1
                m = 2 * reserve_floor + 1
                # L4 at alpha=1, without floating roots: (m r/N)^h >
                # 2^(-p) m^(h-p), and the weaker exponent 2/5.
                require((m * multiplicity)**h * 2**p > order**h * m**(h-p),
                        'reserve tradeoff at its integer boundary')
                require((2 * m * multiplicity)**5 >= order**5 * m**2,
                        'uniform two-fifths fresh-factor bound')
                large_q_cases += 1
            tested += 1

    binary_spectra = []
    for p in [3, 5, 7]:
        h = 2 * p - 1
        order = 1 << h
        spectrum = fwht([int(v.bit_count() == p) for v in range(order)])
        for frequency, value in enumerate(spectrum):
            require(value == inner_eigenvalue(h, p, frequency.bit_count(), 2),
                    'direct group spectrum agrees with coefficient formula')
        binary_spectra.append({'p': p, 'matrix_order': order, 'eigenvalues_checked': order})

    # Direct matrix elimination over Z/9 independently detects valuations.
    p, h, order = 3, 5, 32
    inner = [[int(i == j or (i ^ j).bit_count() == p)
              for j in range(order)] for i in range(order)]
    invariants = local_ring_invariants(inner, p)
    require(invariants == (16, 15, 1), 'direct inner-matrix ring pivots')

    # Rank-one factorization obstruction over Z/9; determinants alone cannot
    # detect it, because det(3I_2)=0 modulo9.
    factorizations_checked = 0
    for u0, u1, v0, v1 in product(range(9), repeat=4):
        values = (u0*v0 % 9, u0*v1 % 9, u1*v0 % 9, u1*v1 % 9)
        require(values != (3, 0, 0, 3), '3I_2 has no width-one factorization')
        factorizations_checked += 1

    # The polynomial degree gate has an independent exhaustive small case.
    degree_counterexamples = 0
    target = [1, 0, 0, 1, 0, 0]
    for coeffs in product(range(9), repeat=4):
        values = [sum(c * pow(x, i, 9) for i, c in enumerate(coeffs)) % 9
                  for x in range(6)]
        if values == target:
            degree_counterexamples += 1
    require(degree_counterexamples == 0, 'no degree-three indicator modulo9')
    require([(1 - x**2)**2 % 9 for x in range(6)] == target,
            'degree-four indicator attains the bound')
    require([(1 - x**2) % 3 for x in range(6)] == target,
            'modulo3 admits the smaller degree, as intended')

    # A forbidden q divisible by p kills the crucial unit eigenvalue. The
    # hypothesis p not dividing q must not be silently dropped.
    low = inner_eigenvalue(5, 3, 2, 3)
    high = inner_eigenvalue(5, 3, 5, 3)
    require((1 + coefficient([low] + [high] * 4, 3)) % 9 == 0,
            'non-coprime q negative control')

    report = {
        'status': 'exact_finite_checks_passed',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'prime_and_alphabet_parameter_cases': tested,
        'large_alphabet_reserve_cases': large_q_cases,
        'direct_binary_spectra': binary_spectra,
        'direct_inner_matrix_modulus': 9,
        'direct_inner_matrix_order': 32,
        'unit_p_and_zero_pivots': invariants,
        'rank_one_factorizations_excluded': factorizations_checked,
        'degree_three_polynomials_excluded': 9**4,
        'negative_controls': ['modulo-p lower degree', 'non-coprime alphabet',
                              'zero determinant does not certify low factor rank'],
        'not_verified': ['complete outer matrix materialization', 'universal formal proof',
                         'full multiplier implementation', 'new runtime lower bound'],
    }
    Path(__file__).with_name('verification-padic-lift.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
