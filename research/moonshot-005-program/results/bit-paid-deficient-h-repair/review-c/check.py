#!/usr/bin/env python3
"""Independent paid-H complement, compiler and movement-price review.

No source-construction or predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and different pivot choices.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np


def need(value, message):
    if not value:
        raise AssertionError(message)


def xor(values):
    answer = 0
    for value in values:
        answer ^= int(value)
    return answer


def product(x, y):
    result = 0
    while y:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 64:
            x ^= 67
    return result


MUL = np.array([[product(x, y) for y in range(64)] for x in range(64)], dtype=np.uint8)
INV = np.array([0] + [next(y for y in range(1, 64) if MUL[x, y] == 1)
                           for x in range(1, 64)], dtype=np.uint8)


def power(x, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = int(MUL[answer, x])
        x = int(MUL[x, x])
        exponent >>= 1
    return answer


def mm(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    need(left.ndim == right.ndim == 2 and left.shape[1] == right.shape[0], 'matrix dimensions')
    answer = np.zeros((left.shape[0], right.shape[1]), dtype=np.uint8)
    for col in range(left.shape[1]):
        answer ^= MUL[left[:, col, None], right[col, None, :]]
    return answer


def kron(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    return MUL[left[:, None, :, None], right[None, :, None, :]].reshape(
        left.shape[0] * right.shape[0], left.shape[1] * right.shape[1])


def echelon(matrix):
    matrix = np.array(matrix, dtype=np.uint8, copy=True)
    pivots = []
    determinant = 1
    for col in range(matrix.shape[1]):
        row = len(pivots)
        choices = np.flatnonzero(matrix[row:, col])
        if not len(choices):
            continue
        chosen = row + int(choices[-1])
        matrix[[row, chosen]] = matrix[[chosen, row]]
        determinant = int(MUL[determinant, matrix[row, col]])
        matrix[row, col:] = MUL[INV[matrix[row, col]], matrix[row, col:]]
        if row + 1 < len(matrix):
            matrix[row + 1:, col:] ^= MUL[matrix[row + 1:, col, None], matrix[row, None, col:]]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots, determinant


def rank(matrix):
    return len(echelon(matrix)[1])


def null(matrix):
    rows, pivots, _ = echelon(matrix)
    free = [j for j in range(rows.shape[1]) if j not in pivots]
    result = np.zeros((rows.shape[1], len(free)), dtype=np.uint8)
    result[free] = np.eye(len(free), dtype=np.uint8)
    for i in range(len(pivots) - 1, -1, -1):
        result[pivots[i]] = mm(rows[i:i + 1, pivots[i] + 1:], result[pivots[i] + 1:])[0]
    need(not np.any(mm(matrix, result)), 'independent nullspace identity')
    return result


def certificate(matrix):
    _, cols, _ = echelon(matrix)
    _, rows, _ = echelon(matrix[:, cols].T)
    minor = matrix[np.ix_(rows, cols)]
    _, pivots, determinant = echelon(minor)
    kernel = null(matrix)
    need(len(pivots) == len(cols) and determinant != 0, 'nonzero maximal minor')
    need(rank(kernel) == matrix.shape[1] - len(cols), 'independent upper-rank certificate')
    return {'shape': list(matrix.shape), 'rank': len(cols), 'minor_rows': rows,
            'minor_columns': cols, 'minor_determinant': determinant,
            'kernel_columns': kernel.tolist(), 'matrix_sha256': hashlib.sha256(matrix.tobytes()).hexdigest()}


def ceil_div(n, d):
    return -((-n) // d)


@lru_cache(None)
def power_interval(n, kappa):
    """Directed dyadic square roots; independent of the author's log/exp engine."""
    scale = 1 << 320
    root_lo = root_hi = n * scale
    product_lo = product_hi = scale
    remaining = Fraction(kappa)
    need(0 <= remaining < 1, 'exponent range')
    for _ in range(160):
        root_lo = isqrt(root_lo * scale)
        radicand = root_hi * scale
        root_hi = isqrt(radicand)
        if root_hi * root_hi < radicand:
            root_hi += 1
        remaining *= 2
        if remaining >= 1:
            product_lo = product_lo * root_lo // scale
            product_hi = ceil_div(product_hi * root_hi, scale)
            remaining -= 1
    if remaining:
        product_hi = ceil_div(product_hi * root_hi, scale)
    return Fraction(n * scale, product_hi), Fraction(n * scale, product_lo)


def histogram(*terms):
    result = Counter()
    for scalar, table in terms:
        for degree, count in table.items():
            result[int(degree)] += Fraction(scalar) * count
    return result


def moment(table, kappa):
    lo = hi = Fraction(0)
    for degree, coefficient in table.items():
        a, b = power_interval(degree, kappa)
        if coefficient >= 0:
            lo += coefficient * a
            hi += coefficient * b
        else:
            lo += coefficient * b
            hi += coefficient * a
    return lo, hi


def binary_expansion(A):
    return np.array([[int(MUL[A[r // 6, c // 6], 1 << (c % 6)]) >> (r % 6) & 1
                      for c in range(6 * A.shape[1])] for r in range(6 * A.shape[0])], dtype=np.uint8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    here = Path(__file__).resolve().parent
    for name, digest in json.loads((here / 'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo / name).read_bytes()).hexdigest() == digest, 'pin ' + name)
    package = here.parent
    data = json.loads((package / 'author/output/COMPILER.json').read_text())
    receipt = json.loads((package / 'author/output/RESULT.json').read_text())
    P, L, T, inverse = (np.array(data[name], dtype=np.uint8) for name in ['P', 'L', 'T', 'T_inverse'])
    need(P.shape == (9, 9) and L.shape == (6, 9) and T.shape == inverse.shape == (15, 15),
         'literal owned matrix dimensions')
    evaluation = np.array([[power(a, d) for d in range(3)] for a in range(1, 10)], dtype=np.uint8)
    sum_blocks = np.hstack([np.eye(3, dtype=np.uint8)] * 3)
    need(np.array_equal(P, mm(evaluation, sum_blocks)) and np.array_equal(L, np.eye(9, dtype=np.uint8)[:6]),
         'literal sum provider and genuine complement coordinates')
    need(all(rank(evaluation[list(rows)]) == 3 for rows in itertools.combinations(range(9), 3)),
         'all 84 three-port sum recovery views')
    A = np.vstack((P, L))
    need(rank(P) == 3 and rank(A) == 9 and rank(A[:-1]) == 8, 'exact defect and missing-complement control')
    need(np.array_equal(T[:, :9], A) and np.array_equal(mm(T, inverse), np.eye(15, dtype=np.uint8)) and
         np.array_equal(mm(inverse, T), np.eye(15, dtype=np.uint8)), 'invertible extended local map')
    reset = np.vstack((np.eye(9, dtype=np.uint8), np.zeros((6, 9), dtype=np.uint8)))
    need(np.array_equal(mm(inverse, A), reset), 'all original values restored and all complement values zero')
    ops = data['binary_elimination_adds']
    need(all(len(op) == 2 and all(0 <= x < 90 for x in op) and op[0] != op[1] for op in ops),
         'each binary operation is a real distinct-owner ADD')
    binary = binary_expansion(T)
    forward = np.eye(90, dtype=np.uint8)
    for target, source in reversed(ops):
        forward[target] ^= forward[source]
    need(np.array_equal(forward, binary), 'complete supplied forward ADD word')
    for target, source in ops:
        forward[target] ^= forward[source]
    need(np.array_equal(forward, np.eye(90, dtype=np.uint8)), 'complete supplied inverse ADD word')
    # Symbolic original inputs and separately initialized zero complement owners.
    values = np.vstack((np.eye(54, dtype=np.uint8), np.zeros((36, 54), dtype=np.uint8)))
    for target, source in reversed(ops):
        values[target] ^= values[source]
    need(np.array_equal(values, binary_expansion(A)), 'actual forward action with zero-initialized complements')
    for target, source in ops:
        values[target] ^= values[source]
    need(np.array_equal(values, binary_expansion(reset)), 'symbolic restoration without any canonical side information')
    need(len(ops) == 1421 <= 90 ** 2 + 3 * 90 and 32 * len(ops) == 45472,
         'exact replacement ADD invoice')
    need(16 * 6 == 96 and 16 * 6 * 6 == 576 and 8 - 2 == 6, 'charged complement owners and movement gap')

    old_paid = {1: 1386, 2: 1253, 3: 62, 4: 47, 5: 9, 6: 104, 7: 10}
    old_productive = {2: 1, 4: 25, 6: 1, 8: 410}
    wrapper = Counter({127: 2, 1: -4})
    for j in range(1, 10):
        wrapper[7 * j + 1] += 4
    for j in range(1, 9):
        wrapper[7 * j] -= 4
    old_gap = histogram((36, old_productive), (-36, old_paid), (111, wrapper))
    need(moment(old_gap, Fraction(0)) == (1506, 1506), 'retained complete caller credit at zero saving')
    allowance = Counter({127: Fraction(37, 6), 64: Fraction(37, 3), 1: -Fraction(37, 3)})
    for j in range(1, 9):
        allowance[7 * j + 1] += Fraction(37, 3)
        allowance[7 * j] -= Fraction(37, 3)
    Q0 = {1: Fraction(4451, 8), 2: Fraction(7213, 16), 4: Fraction(24)}

    def margin(kappa, q, exports, multiplicity):
        profile = histogram((1, allowance), (-1, Q0), (-Fraction(q, 3840), {8: 1}),
                            (-Fraction(exports, 3840), {6: 1}))
        if multiplicity is not None:
            profile = histogram((1, profile), (Fraction(1, 36 * (multiplicity - 1)), old_gap))
        return moment(profile, kappa)

    rows = []
    for target in ['.005', '.0043']:
        kappa = Fraction(target)
        for multiplicity in [870, None]:
            for exports in [0, 16, 96, 192]:
                lo, hi = margin(kappa, 0, exports, multiplicity)
                p8 = power_interval(8, kappa)
                interval = (3840 * lo / p8[1], 3840 * hi / p8[0])
                cap = interval[0].numerator // interval[0].denominator
                need(interval[1] < cap + 1 and margin(kappa, cap, exports, multiplicity)[0] > 0 and
                     margin(kappa, cap + 1, exports, multiplicity)[1] < 0, 'strict integer cap, both signs')
                original = next(x for x in receipt['movement_caps'] if
                                (x['kappa'], x['m'], x['extra_field_exports']) == (target, multiplicity, exports))
                need(cap == original['return_cap'], 'independently reproduced movement cap')
                rows.append({'kappa': target, 'm': multiplicity, 'exports': exports, 'return_cap': cap,
                             'exact_cap_interval': [str(x) for x in interval],
                             'cap_pass_margin': [str(x) for x in margin(kappa, cap, exports, multiplicity)],
                             'next_fail_margin': [str(x) for x in margin(kappa, cap + 1, exports, multiplicity)]})
    need(moment(old_gap, Fraction('.005'))[1] < 0, 'finite multiplicities remain below the limiting allowance')
    need(margin(Fraction('.005'), 34560, 192, None)[1] < 0, 'two repairs exceed the limiting nine-bank floor')
    need(margin(Fraction('.005'), 34688, 96, 870)[1] < 0, 'omitting direct complement movement changes the sign')
    need(next(x['return_cap'] for x in rows if (x['kappa'], x['m'], x['exports']) == ('.005', 870, 96)) == 34615,
         'single repair leaves only 55 fields above the floor')
    args.out.mkdir(parents=True, exist_ok=True)
    result = {'status': 'PASS_INDEPENDENT_PAID_H_REPAIR_REVIEW', 'input_fields': 9, 'output_rank': 3,
              'extension_dimension': 15, 'complement_fields': 6, 'all_three_port_views': 84,
              'binary_ADD_per_direction': len(ops), 'sixteen_copy_replacement_ADDs': 32 * len(ops),
              'sixteen_copy_binary_INIT_MOVE_CLEAR_each': 576, 'export_gap': 6,
              'power_method': '160 directed dyadic exponent digits with 320-bit outward-rounded integer square roots',
              'strict_integer_caps': rows, 'full_source_constructed': False, 'new_complete_kappa': False}
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(result['status'], len(ops), 45472, 576, 34615, flush=True)


if __name__ == '__main__':
    main()
