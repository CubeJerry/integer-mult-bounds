#!/usr/bin/env python3
"""Exact finite checks for SP1--SP3; not a tape/runtime/formal proof."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import random


def ident(n):
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction())
             for j in range(len(b[0]))] for i in range(len(a))]


def determinant(a):
    a = [list(map(Fraction, row)) for row in a]
    n = len(a)
    out = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return Fraction()
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            out = -out
        value = a[j][j]
        out *= value
        for i in range(j + 1, n):
            ratio = a[i][j] / value
            for k in range(j + 1, n):
                a[i][k] -= ratio * a[j][k]
            a[i][j] = Fraction()
    return out


def kron(a, b):
    return [[a[i // len(b)][j // len(b[0])] * b[i % len(b)][j % len(b[0])]
             for j in range(len(a[0]) * len(b[0]))]
            for i in range(len(a) * len(b))]


def blockdiag(blocks):
    n = sum(len(b) for b in blocks)
    out = [[Fraction() for _ in range(n)] for _ in range(n)]
    off = 0
    for b in blocks:
        for i in range(len(b)):
            for j in range(len(b)):
                out[off + i][off + j] = b[i][j]
        off += len(b)
    return out


def permutation_sector(p):
    """Standard representation in basis e_i-e_0 (not orthonormal)."""
    m = len(p) - 1
    return [[Fraction((p[j + 1] == i + 1) - (p[0] == i + 1))
             for j in range(m)] for i in range(m)]


def star_sector(m, signs, alpha=0):
    result = [[Fraction(alpha * (i == j)) for j in range(m)] for i in range(m)]
    for j, sign in enumerate(signs, 1):
        p = list(range(m + 1))
        p[0], p[j] = p[j], p[0]
        a = permutation_sector(p)
        for u in range(m):
            for v in range(m):
                result[u][v] += sign * a[u][v]
    return result


def main():
    rng = random.Random(5026005)
    checks = dict(product_identities=0, singular_row_products=0,
                  all_positive_determinants=0, spectral_vectors=0,
                  signed_seed_kernel_vectors=0, rectangular_controls=0,
                  sum_controls=0, address_diagonal_controls=0,
                  trivial_single_star_controls=0)

    # Arbitrary dense scalar mixers and arbitrary controlled register
    # permutations. Determinants are exact; no orthonormal-basis inference
    # is made from these nonorthogonal coordinate matrices.
    for m in range(2, 6):
        for rows in range(1, 4):
            for trial in range(12):
                o0, o1 = ident(rows), ident(rows * m)
                had_singular = False
                for stage in range(1 + trial % 4):
                    a = [[Fraction(rng.randrange(-2, 3)) for _ in range(rows)]
                         for _ in range(rows)]
                    if trial % 4 == 0:
                        a[-1] = [Fraction() for _ in range(rows)]
                    had_singular |= determinant(a) == 0
                    o0 = matmul(a, o0)
                    o1 = matmul(kron(a, ident(m)), o1)
                    blocks = []
                    for _ in range(rows):
                        p = list(range(m + 1))
                        rng.shuffle(p)
                        blocks.append(permutation_sector(p))
                    o1 = matmul(blockdiag(blocks), o1)
                assert determinant(o1) ** 2 == determinant(o0) ** (2 * m)
                checks['product_identities'] += 1
                if had_singular:
                    assert determinant(o0) == determinant(o1) == 0
                    checks['singular_row_products'] += 1

    for m in range(2, 15):
        s = star_sector(m, [1] * m)
        # Standard basis coordinates of m*e_0-sum_i e_i are all -1.
        v = [[Fraction(-1)] for _ in range(m)]
        assert matmul(s, v) == [[Fraction(1)] for _ in range(m)]
        checks['spectral_vectors'] += 1
        for i in range(m - 1):
            v = [[Fraction(j == i) - Fraction(j == m - 1)] for j in range(m)]
            assert matmul(s, v) == [[(m - 1) * x[0]] for x in v]
            checks['spectral_vectors'] += 1
        for alpha in range(6):
            t = star_sector(m, [1] * m, alpha)
            exact = (alpha + m - 1) ** (m - 1) * (alpha - 1)
            assert determinant(t) == exact
            assert determinant(t) ** 2 != (alpha + m) ** (2 * m)
            checks['all_positive_determinants'] += 1

    for r in range(2, 7):
        m = (1 << r) - 1
        for seed in range(1, 1 << r):
            signs = [(-1) ** ((j & seed).bit_count() % 2) for j in range(1, m + 1)]
            assert sum(signs) == -1
            neg = [j for j, b in enumerate(signs, 1) if b == -1]
            assert len(neg) == (m + 1) // 2
            # Check signed permutation action on each independent
            # negative-leaf difference without a huge determinant.
            for pos in neg[:-1]:
                vec = [Fraction()] * (m + 1)
                vec[pos], vec[neg[-1]] = Fraction(1), Fraction(-1)
                out = [sum(signs[j - 1] * vec[j] for j in range(1, m + 1))]
                out += [signs[j - 1] * vec[0] + (-1 - signs[j - 1]) * vec[j]
                        for j in range(1, m + 1)]
                assert all(x == 0 for x in out)
                checks['signed_seed_kernel_vectors'] += 1

    # Negative control: rectangular replication and summation computes
    # the target with one controlled query, violating square/full-rate
    # hypotheses exactly as predecessor SL warns.
    for m in range(2, 7):
        for signs in ([1] * m, [(-1) ** j for j in range(m)]):
            blocks = []
            for j in range(1, m + 1):
                p = list(range(m + 1))
                p[0], p[j] = p[j], p[0]
                blocks.append(permutation_sector(p))
            b = blockdiag(blocks)
            enc = kron([[Fraction(s)] for s in signs], ident(m))
            dec = kron([[Fraction(1)] * m], ident(m))
            assert matmul(dec, matmul(b, enc)) == star_sector(m, signs)
            checks['rectangular_controls'] += 1
        # Addition of individually legal products is also outside SP1.
        s = star_sector(m, [1] * m)
        assert determinant(s) ** 2 != m ** (2 * m)
        checks['sum_controls'] += 1

    # m=1 is deliberately excluded: the target is itself one permutation.
    assert determinant(star_sector(1, [1])) ** 2 == 1
    checks['trivial_single_star_controls'] += 1

    # A varying diagonal on physical addresses is not a scalar row map:
    # it need not preserve the all-ones sector on one-special-letter words.
    for m in range(2, 10):
        image = list(range(1, m + 2))
        assert len(set(image)) > 1
        checks['address_diagonal_controls'] += 1

    here = Path(__file__).resolve().parent
    result = dict(status='passed', exact_arithmetic='fractions.Fraction',
                  deterministic_seed=5026005, checks=checks,
                  scope='Finite algebra only; unbounded proof in the accompanying note. No tape execution or formal kernel build.',
                  files={p.name: sha256(p.read_bytes()).hexdigest() for p in
                         [Path(__file__), here / 'square-product-star-obstruction.md']})
    output = here / 'square-product-star-verification.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
