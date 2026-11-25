#!/usr/bin/env python3
"""Finite rational Gram/probe checks for a scoped basis obstruction."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                scale = a[i][c]
                a[i] = [x - scale * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def distance(a, b):
    return sum(x != y for x, y in zip(a, b))


def check(d, q):
    h = 2 * d - 1
    zero = (0,) * h
    corners = tuple((0,) * (h - 2) + (a, b) for a, b in [(0, 0), (1, 0), (0, 1), (1, 1)])
    outer = tuple((u,) + (zero,) * (h - 1) for u in corners)
    probes = []
    for a, b in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        u = tuple([1] * (d - 2) + [0] * (h - d) + [1 - a, 1 - b])
        assert len(u) == h
        probes.append((u,) + (zero,) * (h - 1))

    def far_count(v, w):
        return sum(distance(a, b) == d for a, b in zip(v, w))

    gram = [[F(1) - F(far_count(v, w), d) for w in probes] for v in outer]
    directions = [[gram[i][j] - gram[0][j] for j in range(4)] for i in [1, 2, 3]]
    assert rank(directions) == 3
    assert [[directions[i][j] for j in [1, 2, 3]] for i in range(3)] == [
        [-F(1, d), 0, 0], [0, -F(1, d), 0], [0, 0, -F(1, d)]]
    edges = [[1, 0, 0], [0, -1, 1], [0, 1, 0], [-1, 0, 1]]
    assert rank(edges) == 3
    assert all(rank([edges[i] for i in subset]) == 3 for subset in combinations(range(4), 3))
    assert [edges[0][i] + edges[3][i] - edges[1][i] - edges[2][i] for i in range(3)] == [0, 0, 0]

    rectangle_checks = 0
    for first, second in [(0, 1), (2, 3), (0, 2), (1, 3)]:
        left = (outer[first], outer[second])
        changed = next(i for i in range(h) if corners[first][i] != corners[second][i])
        selected = [0] + list(range(1, d - 1)) + [changed]
        assert len(set(selected)) == d
        base = list(corners[first])
        for i in selected:
            base[i] = 1
        dest_inner = []
        for value in [2, 3]:
            u = base.copy()
            u[changed] = value
            assert all(0 <= x < q for x in u)
            dest_inner.append(tuple(u))
        singleton_dest = (1,) * d + (0,) * (h - d)
        right = tuple((u,) + (singleton_dest,) * (d - 1) + (zero,) * (h - d) for u in dest_inner)
        assert all(far_count(a, b) == d for a, b in product(left, right))
        assert all(far_count(a, b) == 0 for a, b in product(left, repeat=2))
        assert all(far_count(a, b) == 0 for a, b in product(right, repeat=2))
        rectangle_checks += 1

    # The d-2 probe offset is essential for this chosen diagonal minor.
    bad_probes = []
    for a, b in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        u = tuple([1] * (d - 1) + [0] * (h - d - 1) + [1 - a, 1 - b])
        bad_probes.append((u,) + (zero,) * (h - 1))
    bad_gram = [[F(1) - F(far_count(v, w), d) for w in bad_probes] for v in outer]
    bad_directions = [[bad_gram[i][j] - bad_gram[0][j] for j in range(4)] for i in [1, 2, 3]]
    assert rank(bad_directions) < 3
    return {"d": d, "q": q, "probe_rank": 3, "canonical_sides": rectangle_checks,
            "independent_three_edge_subsets": 4, "wrong_probe_offset_rejected": True}


def main():
    cases = [check(d, q) for d in [2, 3, 4, 8, 16] for q in [4, 8, 16]]
    receipt = {"scope": "Finite exact rational Gram checks; no tape or universal-basis search.",
               "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "cases": cases, "total_canonical_sides": sum(c["canonical_sides"] for c in cases),
               "total_three_edge_rank_checks": 4 * len(cases),
               "wrong_offset_controls": len(cases)}
    Path(__file__).with_name("source-basis-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
