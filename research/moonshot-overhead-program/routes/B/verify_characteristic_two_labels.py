#!/usr/bin/env python3
"""Exact finite checks of power-of-two distance labels; not a tape test."""
import itertools
import json
from math import comb
from pathlib import Path


def rank_binary(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = row
                break
            row ^= pivots[pivot]
    return len(pivots)


def distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def letter_rectangles(q):
    bits = q.bit_length() - 1
    result = []
    for length in range(bits):
        free = 1 << (bits - length - 1)
        for prefix in range(1 << length):
            for orientation in (0, 1):
                left = tuple(prefix * 2 * free + orientation * free + j for j in range(free))
                right = tuple(prefix * 2 * free + (1 - orientation) * free + j for j in range(free))
                result.append((left, right))
    return result


def check_inner_rectangles():
    q, d, h = 4, 2, 3
    words = tuple(itertools.product(range(q), repeat=h))
    index = {word: i for i, word in enumerate(words)}
    coverage, incidence, rectangles = {}, [0] * len(words), 0
    for different in itertools.combinations(range(h), d):
        fixed = next(i for i in range(h) if i not in different)
        for common, a, b in itertools.product(range(q), repeat=3):
            if a == b:
                continue
            for ll, rr in letter_rectangles(q):
                sides = []
                for first, letters in ((a, ll), (b, rr)):
                    side = []
                    for letter in letters:
                        word = [0] * h
                        word[fixed], word[different[0]], word[different[1]] = common, first, letter
                        side.append(tuple(word))
                    sides.append(side)
                left, right = sides
                for side in sides:
                    assert all(distance(x, y) < d for x in side for y in side)
                for x in left:
                    incidence[index[x]] += 1
                    for y in right:
                        assert distance(x, y) == d
                        pair = (index[x], index[y])
                        coverage[pair] = coverage.get(pair, 0) + 1
                rectangles += 1
    expected = {(i, j) for i, x in enumerate(words) for j, y in enumerate(words) if distance(x, y) == d}
    assert set(coverage) == expected and set(coverage.values()) == {1}
    bound = comb(h, d) * (q - 1) * (q.bit_length() - 1) ** (d - 1)
    assert max(incidence) <= bound
    return dict(rectangles=rectangles, far_pairs=len(expected), maximum_incidence=max(incidence), bound=bound)


def run():
    selector_cases = 0
    for d in (2, 4, 8, 16, 32, 64, 128):
        for c in range(2 * d):
            value = sum(comb(c, s) for s in range(min(c, d - 1) + 1)) % 2
            assert value == int(c in (0, d))
            selector_cases += 1
    inner_ranks = []
    for d, q in ((2, 2), (2, 4), (2, 8), (4, 2)):
        h = 2 * d - 1
        words = tuple(itertools.product(range(q), repeat=h))
        rows = [sum(1 << j for j, y in enumerate(words) if distance(x, y) in (0, d)) for x in words]
        rank = rank_binary(rows)
        bound = (1 << (h - 1)) * q ** (d - 1)
        assert rank <= bound
        inner_ranks.append(dict(d=d, q=q, labels=len(words), rank=rank, bound=bound))
    support = []
    for difference in range(512):
        inner = [(difference >> (3 * j)) & 7 for j in range(3)]
        if difference == 0 or (sum(x != 0 for x in inner) == 2 and all(x == 0 or x.bit_count() == 2 for x in inner)):
            support.append(difference)
    rows = [sum(1 << (i ^ difference) for difference in support) for i in range(512)]
    assert all(row >> i & 1 for i, row in enumerate(rows))
    for row in rows:
        product = 0
        while row:
            bit = row & -row
            product ^= rows[bit.bit_length() - 1]
            row ^= bit
        assert product == 0
    outer_rank = rank_binary(rows)
    assert outer_rank <= 256
    return dict(status='exact finite checks passed', selector_cases=selector_cases,
                inner_ranks=inner_ranks, inner_rectangles=check_inner_rectangles(),
                outer_example=dict(d=2, q=2, labels=512, rank=outer_rank,
                                   row_support=len(support), square_zero=True),
                full_tape_or_repair_verification=False)


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('characteristic-two-label-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
