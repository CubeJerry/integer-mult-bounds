#!/usr/bin/env python3
"""Exact finite checks of canonical rectangle incidence, not a tape test."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json


def first_bit_rectangles(q):
    t = q.bit_length() - 1
    assert q == 1 << t
    rectangles = []
    for j in range(t):
        remaining = t - j - 1
        for prefix in range(1 << j):
            for orientation in range(2):
                left_start = ((prefix << 1) | orientation) << remaining
                right_start = ((prefix << 1) | (1 - orientation)) << remaining
                width = 1 << remaining
                rectangles.append((tuple(range(left_start, left_start + width)),
                                   tuple(range(right_start, right_start + width))))
    return rectangles


def encode(word, base):
    value = 0
    for digit in word:
        value = base * value + digit
    return value


def distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def inner_rectangles(d, q):
    h = 2 * d - 1
    elementary = first_bit_rectangles(q)
    for changed in combinations(range(h), d):
        fixed = tuple(i for i in range(h) if i not in changed)
        for common in product(range(q), repeat=len(fixed)):
            for left_first in range(q):
                for right_first in range(q):
                    if left_first == right_first:
                        continue
                    for choices in product(elementary, repeat=d - 1):
                        left = [None] * h
                        right = [None] * h
                        for position, value in zip(fixed, common):
                            left[position] = right[position] = (value,)
                        left[changed[0]] = (left_first,)
                        right[changed[0]] = (right_first,)
                        for position, pair in zip(changed[1:], choices):
                            left[position], right[position] = pair
                        yield tuple(product(*left)), tuple(product(*right))


def check_inner(d, q):
    h = 2 * d - 1
    t = q.bit_length() - 1
    words = tuple(product(range(q), repeat=h))
    source = Counter()
    destination = Counter()
    edges = set()
    rectangles = []
    for left, right in inner_rectangles(d, q):
        assert left and right
        assert all(distance(a, b) < d for a in left for b in left)
        assert all(distance(a, b) < d for a in right for b in right)
        left_ids = tuple(encode(word, q) for word in left)
        right_ids = tuple(encode(word, q) for word in right)
        rectangles.append((left_ids, right_ids))
        source.update(left_ids)
        destination.update(right_ids)
        for a, aid in zip(left, left_ids):
            for b, bid in zip(right, right_ids):
                assert distance(a, b) == d
                assert (aid, bid) not in edges
                edges.add((aid, bid))
    expected_edges = set()
    for aid, a in enumerate(words):
        for changed in combinations(range(h), d):
            alternatives = [tuple(v for v in range(q) if v != a[j]) for j in changed]
            for values in product(*alternatives):
                b = list(a)
                for j, value in zip(changed, values):
                    b[j] = value
                expected_edges.add((aid, encode(b, q)))
    assert edges == expected_edges
    alpha = comb(h, d) * (q - 1) * t ** (d - 1)
    count = comb(h, d) * 2 ** (d - 1) * (q * (q - 1)) ** d
    assert len(rectangles) == count
    assert set(source.values()) == {alpha}
    assert set(destination.values()) == {alpha}
    assert len(source) == len(destination) == q ** h
    average = Fraction(sum(source.values()), count)
    assert average == Fraction(q * t, 2 * (q - 1)) ** (d - 1)
    negative = 0
    if t > 1:
        wrong = comb(h, d) * (q - 1) * (t - 1) ** (d - 1)
        assert all(source[i] != wrong for i in range(q ** h))
        negative += q ** h
    # Omitting one nonempty rectangle destroys regular incidence/coverage.
    omitted_left, omitted_right = rectangles[0]
    damaged = source.copy()
    damaged.subtract(omitted_left)
    assert any(damaged[i] != alpha for i in range(q ** h))
    negative += 1
    # Replacing the pinned first position by another broad bit rectangle
    # makes a side contain a distance-d pair when q>=4.
    if q >= 4:
        assert distance((0,) * d, (1,) * d) == d
        assert all(v < q // 2 for v in (0, 1))
        negative += 1
    return {
        "d": d, "q": q, "words": q ** h, "rectangles": count,
        "edges": len(edges), "source_incidence": alpha,
        "destination_incidence": alpha,
        "average_side_size": str(average), "negative_controls": negative,
    }, rectangles


def check_full_outer_binary_d2(inner):
    d, h, n0 = 2, 3, 8
    source = Counter()
    destination = Counter()
    edges = set()
    count = 0
    for changed in combinations(range(h), d):
        fixed = next(i for i in range(h) if i not in changed)
        for common in range(n0):
            for selected in product(inner, repeat=d):
                left = [None] * h
                right = [None] * h
                left[fixed] = right[fixed] = (common,)
                for j, (a, b) in zip(changed, selected):
                    left[j], right[j] = a, b
                left_ids = tuple(encode(w, n0) for w in product(*left))
                right_ids = tuple(encode(w, n0) for w in product(*right))
                source.update(left_ids)
                destination.update(right_ids)
                count += 1
                for a, b in product(left_ids, right_ids):
                    assert (a, b) not in edges
                    edges.add((a, b))
    inner_words = tuple(product(range(2), repeat=3))
    outer_words = tuple(product(range(n0), repeat=h))
    expected = set()
    for a_id, a in enumerate(outer_words):
        for b_id, b in enumerate(outer_words):
            changed = [i for i in range(h) if a[i] != b[i]]
            if len(changed) == d and all(distance(inner_words[a[i]], inner_words[b[i]]) == d for i in changed):
                expected.add((a_id, b_id))
    assert edges == expected
    lam = comb(h, d) ** (d + 1)
    assert set(source.values()) == set(destination.values()) == {lam}
    assert len(source) == len(destination) == n0 ** h
    assert count == comb(h, d) * n0 ** (h - d) * len(inner) ** d
    return {"d": 2, "q": 2, "labels": n0 ** h, "rectangles": count,
            "edges": len(edges), "regular_source_and_destination_incidence": lam}


def main():
    cases = []
    binary_inner = None
    for d, q in [(2, 2), (2, 4), (2, 8), (3, 2), (3, 4), (4, 2)]:
        result, rectangles = check_inner(d, q)
        cases.append(result)
        if (d, q) == (2, 2):
            binary_inner = rectangles
    outer = check_full_outer_binary_d2(binary_inner)
    receipt = {
        "scope": "Exact finite combinatorial partition checks; no tape or asymptotic execution.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "inner_cases": cases, "full_outer_case": outer,
        "totals": {
            "inner_rectangles": sum(c["rectangles"] for c in cases),
            "inner_edges": sum(c["edges"] for c in cases),
            "inner_words": sum(c["words"] for c in cases),
            "negative_controls": sum(c["negative_controls"] for c in cases),
        },
    }
    output = Path(__file__).with_name("canonical-incidence-verification.json")
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
