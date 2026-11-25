#!/usr/bin/env python3
"""Sparse rational Gram checks for the scoped common-preparation obstruction."""
from fractions import Fraction
from itertools import product, combinations
import json
from pathlib import Path


def word(c, d):
    return (c,) * d + (0,) * (d - 1)


def vector(a, d, wrong=False):
    h = 2 * d - 1
    out = {('z',): -1 if wrong else -2}
    for i in range(h):
        for u in (word(0, d), word(a[i] if i < d else 0, d)):
            key = (i, u)
            out[key] = out.get(key, 0) - 1
    return out


def inner(x, y, d):
    ans = Fraction(0)
    for i, xi in x.items():
        for j, yj in y.items():
            if i == j == ('z',):
                ans += 2 * xi * yj
            elif i != ('z',) and j != ('z',) and i[0] == j[0]:
                if sum(a != b for a, b in zip(i[1], j[1])) == d:
                    ans += Fraction(-4 * xi * yj, d)
    return ans


def check():
    stats = dict(complete_families=0, isotropic_vectors=0,
                 nonorthogonal_pairs=0, identical_source_pairs=0,
                 nonzero_radix3_pairings=0, rejected_wrong_vectors=0)
    cases = []
    for d, q in ((2, 2), (2, 4), (2, 8), (4, 2), (4, 4), (8, 2)):
        tuples = list(product(range(1, q), repeat=d))
        vectors = [vector(a, d) for a in tuples]
        modulus = 3
        while modulus <= d:
            modulus *= 3
        for a, v in zip(tuples, vectors):
            assert inner(v, v, d) == 0
            stats['isotropic_vectors'] += 1
            bad = vector(a, d, wrong=True)
            assert inner(bad, bad, d) != 0
            stats['rejected_wrong_vectors'] += 1
        high_pairs = 0
        for i, j in combinations(range(len(tuples)), 2):
            a, b = tuples[i], tuples[j]
            dist = sum(x != y for x, y in zip(a, b))
            actual = inner(vectors[i], vectors[j], d)
            assert actual == Fraction(-4 * dist, d) != 0
            stats['nonorthogonal_pairs'] += 1
            reduced = actual.numerator * pow(actual.denominator, -1, modulus) % modulus
            assert reduced != 0
            stats['nonzero_radix3_pairings'] += 1
            if all(x >= q // 2 for x in a + b):
                # Each chosen anchor lies in K0; the source side condition is identical.
                for x in a + b:
                    u = word(x, d)
                    assert u[0] == x and all(y >= q // 2 for y in u[1:d])
                    assert all(y == 0 for y in u[d:])
                high_pairs += 1
        high_count = (q // 2) ** d
        assert high_pairs == high_count * (high_count - 1) // 2
        stats['identical_source_pairs'] += high_pairs
        stats['complete_families'] += 1
        cases.append(dict(d=d, q=q, anchor_count=len(tuples),
                          identical_source_anchor_count=high_count,
                          tested_modulus=modulus))
    return dict(status='pass', scope='common totally isotropic preparation only',
                counts=stats, cases=cases)


if __name__ == '__main__':
    out = check()
    Path(__file__).with_name('isotropic-preparation-verification.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))
