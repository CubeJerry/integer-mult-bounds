#!/usr/bin/env python3
"""Exact controls for the scoped two-stage characteristic-two theorem."""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path


def add(*matrices):
    result = [0] * len(matrices[0])
    for matrix in matrices:
        for i, value in enumerate(matrix):
            result[i] ^= value
    return tuple(result)


def mul(a, b):
    result = []
    for row in a:
        value = 0
        while row:
            low = row & -row
            value ^= b[low.bit_length() - 1]
            row ^= low
        result.append(value)
    return tuple(result)


def comm(a, b):
    return add(mul(a, b), mul(b, a))


def construct(m, omit_linear=False, omit_extra_identity=False):
    r = (m - 1) // 2
    width = 1 << r
    identity = tuple(1 << i for i in range(width))
    zero = (0,) * width
    pairs = []
    for i in range(r):
        bit = 1 << i
        u = tuple((1 << (row | bit)) if not row & bit else 0 for row in range(width))
        v = tuple((1 << (row ^ bit)) if row & bit else 0 for row in range(width))
        pairs.append((u, v))
    e = []
    prefix = zero
    a0 = zero
    for u, v in pairs:
        e.extend((add(prefix, u), add(prefix, v)))
        prefix = add(prefix, u, v)
        a0 = add(a0, mul(u, v)) if omit_linear else add(a0, mul(u, v), u, v)
    if m % 2 == 0:
        e.append(add(zero if omit_extra_identity else identity, *e))
    a = [add(a0, value) for value in e] + [a0]
    b = [add(identity, value) for value in a]
    return identity, e, a, b


def main():
    coefficient_pairs = commutators = block_pairs = 0
    samples = []
    negatives = {"omitted_linear_terms": 0, "omitted_even_identity": 0}
    for m in range(1, 17):
        identity, es, a, b = construct(m)
        assert len(a) == len(b) == m
        assert all(add(x, y) == identity for x, y in zip(a, b))
        for i, j in combinations(range(m), 2):
            assert add(mul(b[i], a[j]), mul(b[j], a[i])) == identity
            assert add(mul(a[i], b[j]), mul(a[j], b[i])) == identity
            coefficient_pairs += 1
            block_pairs += 1
        for x, y in combinations(es, 2):
            assert comm(x, y) == identity
            commutators += 1
        if m in (1, 2, 3, 4, 8, 12, 16):
            samples.append({"m": m, "constructed_width": len(identity),
                            "proved_minimum_two_stage_width": 1 << ((m - 1) // 2)})
        if m >= 3:
            ident, _, aa, bb = construct(m, omit_linear=True)
            assert any(add(mul(bb[i], aa[j]), mul(bb[j], aa[i])) != ident
                       for i, j in combinations(range(m), 2))
            negatives["omitted_linear_terms"] += 1
        if m % 2 == 0:
            ident, _, aa, bb = construct(m, omit_extra_identity=True)
            assert any(add(mul(bb[i], aa[j]), mul(bb[j], aa[i])) != ident
                       for i, j in combinations(range(m), 2))
            negatives["omitted_even_identity"] += 1

    graph_cases = []
    for width in (1, 2):
        matrices = [tuple((value >> (width * i)) & ((1 << width) - 1)
                          for i in range(width))
                    for value in range(1 << (width * width))]
        identity = tuple(1 << i for i in range(width))
        adjacency = [sum(1 << j for j, y in enumerate(matrices)
                         if add(comm(x, y), x, y) == identity)
                     for x in matrices]
        counts = []
        for size in range(1, 2 * width + 2):
            count = sum(all((adjacency[i] >> j) & 1 for i, j in combinations(indices, 2))
                        for indices in combinations(range(len(matrices)), size))
            counts.append(count)
        maximum = max(i + 1 for i, count in enumerate(counts) if count)
        assert maximum == 2 * width
        assert counts[-1] == 0
        graph_cases.append({"width": width, "all_coefficient_matrices": len(matrices),
                            "clique_counts_by_m": counts, "maximum_m": maximum})

    result = {"status": "PASS", "field": "F_2", "scope": "full-rate square affine identities; no physical algorithm",
              "constructed_m_values": 16, "quadratic_coefficient_pairs": coefficient_pairs,
              "commutator_pairs": commutators, "reverse_product_pairs": block_pairs,
              "exhaustive_small_width_graphs": graph_cases,
              "negative_controls": negatives, "samples": samples}
    Path(__file__).with_name("char2-full-rate-width-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
