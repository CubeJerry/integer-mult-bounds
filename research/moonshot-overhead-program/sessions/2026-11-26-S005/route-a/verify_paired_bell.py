#!/usr/bin/env python3
"""Exact finite Bell/Clifford/table checks, not tape timing or a formal proof."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import random


def parity(x):
    return x.bit_count() & 1


def sign(x):
    return -1 if x & 1 else 1


def xor_sum(values):
    result = 0
    for value in values:
        result ^= value
    return result


def basis(values):
    pivots = {}
    for value in values:
        while value:
            p = value.bit_length() - 1
            if p in pivots:
                value ^= pivots[p]
            else:
                pivots[p] = value
                break
    for p in sorted(pivots):
        for q in pivots:
            if q != p and ((pivots[q] >> p) & 1):
                pivots[q] ^= pivots[p]
    return tuple(pivots[p] for p in sorted(pivots, reverse=True))


def reduce_by(value, b):
    for row in b:
        if (value >> (row.bit_length() - 1)) & 1:
            value ^= row
    return value


def linear(matrix, value):
    return sum(parity(mask & value) << i for i, mask in enumerate(matrix))


def inverse_transpose(matrix):
    a = len(matrix)
    candidates = range(1 << a)
    return tuple(next(v for v in candidates
                      if all(parity(v & matrix[j]) == (i == j)
                             for j in range(a))) for i in range(a))


def columnwise(matrix, value, a, t):
    mask = (1 << a) - 1
    return sum(linear(matrix, (value >> (a*h)) & mask) << (a*h)
               for h in range(t))


def rows(value, a, t):
    return tuple(sum(((value >> (a*h+i)) & 1) << h for h in range(t))
                 for i in range(a))


def fwht(values, bits=None):
    result = list(values)
    if bits is None:
        bits = range((len(result) - 1).bit_length())
    for bit in bits:
        stride = 1 << bit
        for base in range(0, len(result), 2*stride):
            for offset in range(stride):
                i, j = base+offset, base+offset+stride
                x, y = result[i], result[j]
                result[i], result[j] = x+y, x-y
    return result


def bell_column(u, v, s):
    q = 1 << s
    result = [0] * (q*q)
    for z in range(q):
        result[(z << s) | (z ^ u)] = sign(parity(v & z))
    return result


def bell_transpose(values, s):
    q = 1 << s
    result = [0] * (q*q)
    for u in range(q):
        transformed = fwht([values[(z << s) | (z ^ u)] for z in range(q)])
        result[u*q:(u+1)*q] = transformed
    return result


def quadratic(a, constant, linear_mask, pairs):
    def evaluate(x):
        return (constant ^ parity(x & linear_mask)
                ^ (sum(((x >> i) & 1) * ((x >> j) & 1)
                       for i, j in pairs) & 1))
    matrix = tuple(sum((1 << j) for p, q in pairs
                       for j in ([q] if p == i else [p] if q == i else []))
                   for i in range(a))
    return evaluate, matrix


def key_at(x, y, family, a, t):
    mask = (1 << a)-1
    return sum((sum(q((x >> (a*h)) & mask) ^ q((y >> (a*h)) & mask)
                    for h in range(t)) & 1) << j
               for j, (q, _) in enumerate(family))


def subgroup_data(u, family, a, t):
    mask = (1 << a)-1
    deltas = [columnwise(matrix, u, a, t) for _, matrix in family]
    b = basis(deltas)
    points = {xor_sum(b[j] for j in range(len(b)) if (z >> j) & 1): z
              for z in range(1 << len(b))}
    alphas = [points[delta] for delta in deltas]
    eta = [sum(q((u >> (a*h)) & mask) ^ q(0) for h in range(t)) & 1
           for q, _ in family]
    return b, points, alphas, eta


def expected_table_column(u, v, family, a, t, table):
    s = a*t
    b, points, alphas, eta = subgroup_data(u, family, a, t)
    d = len(b)
    spectral = [table(sum((eta[j] ^ parity(alphas[j] & lam)) << j
                          for j in range(len(family))))
                for lam in range(1 << d)]
    convolution = fwht(spectral)
    result = [Fraction(0)] * (1 << (2*s))
    for delta, z in points.items():
        result[(u << s) | (v ^ delta)] = Fraction(convolution[z], 1 << d)
    return result


def physical_table_column(u, v, family, a, t, table):
    s = a*t
    q = 1 << s
    values = bell_column(u, v, s)
    for i, value in enumerate(values):
        if value:
            values[i] = value * table(key_at(i >> s, i & (q-1), family, a, t))
    return [Fraction(value, q) for value in bell_transpose(values, s)]


def check():
    rng = random.Random(26110542)
    counts = dict(bell_orthogonal_columns=0, gl_columns=0, walsh_columns=0,
                  quadratic_generator_columns=0, rational_table_columns=0,
                  complete_cosets=0, dependent_phase_cases=0,
                  orbit_preservation=0, cubic_controls=0, unequal_pair_controls=0)
    for a, t in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (4, 1), (2, 3)]:
        s = a*t
        q = 1 << s
        selected = list(range(q*q)) if q*q <= 256 else rng.sample(range(q*q), 24)
        matrices = [tuple(1 << i for i in range(a))]
        if a >= 2:
            matrices += [tuple((1 << i) ^ ((1 << 1) if i == 0 else 0)
                               for i in range(a)),
                         tuple(1 << ((i+1) % a) for i in range(a))]
        for label in selected:
            u, v = label >> s, label & (q-1)
            original = bell_column(u, v, s)
            recovered = bell_transpose(original, s)
            assert recovered[label] == q and sum(x != 0 for x in recovered) == 1
            counts['bell_orthogonal_columns'] += 1
            for matrix in matrices:
                transformed = [0] * (q*q)
                for i, value in enumerate(original):
                    if value:
                        x = columnwise(matrix, i >> s, a, t)
                        y = columnwise(matrix, i & (q-1), a, t)
                        transformed[(x << s) | y] = value
                result = bell_transpose(transformed, s)
                target_u = columnwise(matrix, u, a, t)
                target_v = columnwise(inverse_transpose(matrix), v, a, t)
                target = (target_u << s) | target_v
                assert result[target] == q and sum(x != 0 for x in result) == 1
                counts['gl_columns'] += 1
            for axis in range(a):
                active = [a*h+axis for h in range(t)]
                transformed = fwht(original, active + [s+b for b in active])
                result = bell_transpose(transformed, s)
                bitmask = sum(1 << b for b in active)
                tu = (u & ~bitmask) | (v & bitmask)
                tv = (v & ~bitmask) | (u & bitmask)
                target = (tu << s) | tv
                assert result[target] == q*(1 << t)*sign(parity(u & v & bitmask))
                assert sum(x != 0 for x in result) == 1
                counts['walsh_columns'] += 1
        pairs = [(i, j) for i in range(a) for j in range(i+1, a)]
        family = [quadratic(a, 0, 0, [p]) for p in pairs]
        family += [quadratic(a, 0, 1, []), quadratic(a, 1, 1, pairs[:1]),
                   quadratic(a, 0, 0, pairs[:1])]
        for label in selected:
            u, v = label >> s, label & (q-1)
            for j, generator in enumerate(family):
                actual = physical_table_column(u, v, [generator], a, t,
                                               lambda k: sign(k))
                expected = expected_table_column(u, v, [generator], a, t,
                                                 lambda k: sign(k))
                assert actual == expected and sum(x != 0 for x in actual) == 1
                counts['quadratic_generator_columns'] += 1
            # Dense, unequal-denominator rational coefficients; no low-degree assumption.
            def table(k):
                return Fraction((17*k*k + 11*k + 3) % 43 - 21, 1 + (5*k % 13))
            assert physical_table_column(u, v, family, a, t, table) == \
                expected_table_column(u, v, family, a, t, table)
            counts['rational_table_columns'] += 1
            b, points, alphas, eta = subgroup_data(u, family, a, t)
            if any(alpha == 0 and e for alpha, e in zip(alphas, eta)):
                counts['dependent_phase_cases'] += 1
        # Exhaustive subgroup partitions, including every deficient rank.
        for u in range(q):
            b, points, _, _ = subgroup_data(u, family, a, t)
            cosets = {}
            for v in range(q):
                bar = reduce_by(v, b)
                w = basis(rows(u, a, t) + rows(v, a, t))
                cosets.setdefault(bar, []).append((v, w))
                for delta in points:
                    assert basis(rows(u, a, t) + rows(v ^ delta, a, t)) == w
                    counts['orbit_preservation'] += 1
            for group in cosets.values():
                assert len(group) == len(points)
                assert len({w for _, w in group}) == 1
                counts['complete_cosets'] += 1
    # The degree and identical-pair hypotheses are substantive.
    a, t, u, v = 3, 1, 7, 0
    cubic = (lambda x: int((x & 7) == 7), (0, 0, 0))
    transformed = physical_table_column(u, v, [cubic], a, t, lambda k: sign(k))
    assert sum(x != 0 for x in transformed) > 1
    counts['cubic_controls'] += 1
    a, s = 2, 2
    q = 1 << s
    original = bell_column(0, 0, s)
    for i, value in enumerate(original):
        x = i >> s
        original[i] = value * sign((x & 1)*((x >> 1) & 1))
    transformed = bell_transpose(original, s)
    assert sum(x != 0 for x in transformed) > 1
    counts['unequal_pair_controls'] += 1
    assert counts['dependent_phase_cases'] > 0
    return counts


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    receipt = {'status': 'passed', 'deterministic_seed': 26110542,
               'exact_arithmetic': 'integers and fractions.Fraction',
               'checks': check(),
               'scope': 'Finite exact algebra, all-rank coset partitions and failure controls; not physical tape timing, a numerical error theorem, or a formal-kernel proof.',
               'files': {name: sha256((root/name).read_bytes()).hexdigest()
                         for name in ['verify_paired_bell.py', 'paired-column-bell-executor.md']}}
    (root/'paired-bell-verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
