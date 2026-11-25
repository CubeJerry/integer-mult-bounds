#!/usr/bin/env python3
"""Exact finite algebra/layout checks for the two-pass shared pencil.

Random-access lists here are finite audit witnesses, not claimed tape code.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from random import Random


def mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return result


def inverse(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    work = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        reciprocal = next(x for x in range(1, 4) if mul(x, work[column][column]) == 1)
        work[column] = [mul(reciprocal, x) for x in work[column]]
        for row in range(n):
            if row != column and work[row][column]:
                coefficient = work[row][column]
                work[row] = [a ^ mul(coefficient, b) for a, b in zip(work[row], work[column])]
    return [row[n:] for row in work]


def add(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[x ^ y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def zero(rows: int, spatial: int) -> list[list[int]]:
    return [[0] * spatial for _ in range(rows)]


def row_map(matrix: list[list[int]], array: list[list[int]]) -> list[list[int]]:
    spatial = len(array[0])
    out = zero(len(matrix), spatial)
    for i, coefficients in enumerate(matrix):
        for j, coefficient in enumerate(coefficients):
            for position in range(spatial):
                out[i][position] ^= mul(coefficient, array[j][position])
    return out


def push(array: list[list[int]], permutation: list[int]) -> list[list[int]]:
    out = zero(len(array), len(permutation))
    for row, source in zip(out, array):
        for old, destination in enumerate(permutation):
            row[destination] = source[old]
    return out


def inv_perm(permutation: list[int]) -> list[int]:
    out = [0] * len(permutation)
    for old, destination in enumerate(permutation):
        out[destination] = old
    return out


def compose(first: list[int], second: list[int]) -> list[int]:
    return [first[second[i]] for i in range(len(first))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('pencil-schedule-verification.json'))
    args = parser.parse_args()
    random = Random(2026112603)
    counts = {'instances': 0, 'output_field_entries': 0, 'rank_guard_instances': 0,
              'query_layouts': 0, 'rectangle_updates': 0}
    bad = {'omit_lowrank_rejected': 0, 'wrong_destination_layout_rejected': 0,
           'omit_central_inverse_rejected': 0}
    # Odd-weight F2^3 label vectors have self-pairing one. Repeated copies
    # permit mr/N<=1 while retaining a genuinely nontrivial rank-three core.
    seeds = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    for copies in (2, 3, 4):
        labels = seeds * copies
        number = len(labels)
        pstar = [[sum(a * b for a, b in zip(v, w)) % 2 for v in labels] for w in labels]
        basis_rows = [0, 1, 2]
        basis_columns = [3, 1, 2]
        center = [[pstar[i][j] for j in basis_columns] for i in basis_rows]
        center_inverse = inverse(center)
        rectangles = [([v], [w]) for w in range(number) for v in range(number)
                      if w != v and pstar[w][v]]
        for queries in range(1, min(5, number // 3 + 1)):
            for internal in (1, 2, 3):
                for spatial in (2, 3, 5, 7):
                    assert queries * len(basis_rows) <= number
                    counts['rank_guard_instances'] += 1
                    original = [[[random.randrange(4) for _ in range(spatial)]
                                 for _ in range(internal)] for _ in range(number)]
                    a_maps = [[[random.randrange(4) for _ in range(internal)]
                               for _ in range(internal)] for _ in range(queries + 1)]
                    q_maps, s_maps, t_maps = [], [], []
                    for query in range(queries):
                        q = list(range(spatial)); random.shuffle(q)
                        q_maps.append(q)
                        source, destination = [], []
                        for _ in labels:
                            s = list(range(spatial)); random.shuffle(s)
                            source.append(s)
                            destination.append(compose(s, inv_perm(q)))
                            counts['query_layouts'] += 1
                        s_maps.append(source); t_maps.append(destination)
                    expected = [row_map(a_maps[0], array) for array in original]
                    for query in range(queries):
                        for label in range(number):
                            expected[label] = add(expected[label], row_map(a_maps[query + 1], push(original[label], q_maps[query])))
                    # Source singleton terms initialize every query/rank accumulator.
                    ranks = [[push(original[i], s_maps[query][i]) for i in basis_rows]
                             for query in range(queries)]
                    direct = [row_map(a_maps[0], array) for array in original]
                    for sources, destinations in rectangles:
                        for query in range(queries):
                            common = zero(internal, spatial)
                            for source in sources:
                                common = add(common, push(original[source], s_maps[query][source]))
                            for destination in destinations:
                                direct[destination] = add(direct[destination], push(row_map(a_maps[query + 1], common), inv_perm(t_maps[query][destination])))
                            for rank, label in enumerate(basis_rows):
                                if label in destinations:
                                    ranks[query][rank] = add(ranks[query][rank], common)
                            counts['rectangle_updates'] += 1
                    result = [[row[:] for row in array] for array in direct]
                    without_inverse = [[row[:] for row in array] for array in direct]
                    wrong_layout = [[row[:] for row in array] for array in direct]
                    for query in range(queries):
                        processed = []
                        for coefficients in center_inverse:
                            value = zero(internal, spatial)
                            for coefficient, rank_array in zip(coefficients, ranks[query]):
                                value = add(value, [[mul(coefficient, x) for x in row] for row in rank_array])
                            processed.append(row_map(a_maps[query + 1], value))
                        for label in range(number):
                            common = zero(internal, spatial)
                            bad_common = zero(internal, spatial)
                            for rank, basis_label in enumerate(basis_columns):
                                coefficient = pstar[label][basis_label]
                                common = add(common, [[mul(coefficient, x) for x in row] for row in processed[rank]])
                                raw = row_map(a_maps[query + 1], ranks[query][rank])
                                bad_common = add(bad_common, [[mul(coefficient, x) for x in row] for row in raw])
                            result[label] = add(result[label], push(common, inv_perm(t_maps[query][label])))
                            without_inverse[label] = add(without_inverse[label], push(bad_common, inv_perm(t_maps[query][label])))
                            wrong_layout[label] = add(wrong_layout[label], common)
                    assert result == expected
                    bad['omit_lowrank_rejected'] += direct != expected
                    bad['wrong_destination_layout_rejected'] += wrong_layout != expected
                    bad['omit_central_inverse_rejected'] += without_inverse != expected
                    counts['instances'] += 1
                    counts['output_field_entries'] += number * internal * spatial
    assert all(bad.values())
    receipt = {'status': 'passed', 'scope': 'exact F4 two-pass linear-operator and query-layout simulation; no physical tape or actual source geometry execution',
               'counts': counts, 'negative_controls': bad}
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
