#!/usr/bin/env python3
"""Finite affine difference-set partition search; no asymptotic conclusion."""
from pathlib import Path
from itertools import product
import argparse
import json
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


def points(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def shift(mask, value):
    return sum(1 << (x ^ value) for x in points(mask))


def subspaces(n):
    layers = [{1}]
    for dim in range(n):
        following = set()
        for mask in layers[-1]:
            for x in range(1 << n):
                if not ((mask >> x) & 1):
                    following.add(mask | shift(mask, x))
        layers.append(following)
    return [mask for layer in layers for mask in layer]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=3)
    ap.add_argument('--k', type=int, default=2)
    ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    t, k = args.t, args.k
    n, q = t * k, 1 << t
    assert n <= 6, 'this complete enumerator is intentionally bounded'
    target = sum(1 << x for x in range(1 << n)
                 if all((x >> (i * t)) & (q - 1) for i in range(k)))
    support = list(points(target))
    index = {x: i for i, x in enumerate(support)}
    linear = subspaces(n)
    affine = []
    for direction in linear:
        seen = 0
        for x in range(1 << n):
            if (seen >> x) & 1:
                continue
            coset = shift(direction, x)
            seen |= coset
            if coset & ~target == 0:
                affine.append((coset, direction, x))
    rows, columns = [], []
    for j, (coset, _, _) in enumerate(affine):
        for x in points(coset):
            rows.append(index[x])
            columns.append(j)
    matrix = coo_matrix((np.ones(len(rows)), (rows, columns)),
                        shape=(len(support), len(affine))).tocsc()
    result = milp(np.ones(len(affine)), integrality=np.ones(len(affine)),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, 1, 1),
                  options={'time_limit': args.seconds, 'mip_rel_gap': 0.0})
    certificate = None
    if result.x is not None:
        chosen = [affine[j] for j, value in enumerate(result.x) if value > 0.5]
        covered = 0
        for coset, direction, representative in chosen:
            assert covered & coset == 0
            assert shift(direction, representative) == coset
            covered |= coset
        assert covered == target
        vertex_count = 1 << n
        adjacency = [sum(1 << y for y in range(vertex_count) if (target >> (x ^ y)) & 1)
                     for x in range(vertex_count)]
        actual = [0] * vertex_count
        left_load, right_load = [0] * vertex_count, [0] * vertex_count
        rectangle_count = nonproduct_sides = 0
        for _, direction, representative in chosen:
            seen = 0
            for x in range(vertex_count):
                if (seen >> x) & 1:
                    continue
                a = shift(direction, x)
                b = shift(a, representative)
                seen |= a
                rectangle_count += 1
                for source in points(a):
                    assert actual[source] & b == 0
                    actual[source] |= b
                    left_load[source] += 1
                for destination in points(b):
                    right_load[destination] += 1
                for side in (a, b):
                    hull = 1
                    for i in range(k):
                        hull *= len({(z >> (i * t)) & (q - 1) for z in points(side)})
                    nonproduct_sides += hull != side.bit_count()
        assert actual == adjacency
        assert set(left_load + right_load) == {len(chosen)}
        certificate = {'affine_parts': [{'points': list(points(coset)),
                                         'direction': list(points(direction)),
                                         'representative': representative}
                                        for coset, direction, representative in chosen],
                       'part_count_and_common_load': len(chosen),
                       'rectangle_count': rectangle_count,
                       'nonproduct_rectangle_sides': nonproduct_sides,
                       'exact_integer_validation': 'passed'}
    record = {'t': t, 'k': k, 'q': q, 'target_points': len(support),
              'linear_subspaces_enumerated': len(linear),
              'candidate_affine_parts': len(affine),
              'solver_status': int(result.status), 'solver_message': result.message,
              'solver_dual_bound': float(result.mip_dual_bound) if result.x is not None else None,
              'time_limit_seconds': args.seconds, 'certificate': certificate,
              'scope': 'Finite affine difference-set model; solver bound is not a general JR lower bound.'}
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({key: value for key, value in record.items() if key != 'certificate'}))
    if certificate:
        print('EXACT_CERTIFICATE', certificate['part_count_and_common_load'],
              certificate['rectangle_count'], certificate['nonproduct_rectangle_sides'])


if __name__ == '__main__':
    main()
