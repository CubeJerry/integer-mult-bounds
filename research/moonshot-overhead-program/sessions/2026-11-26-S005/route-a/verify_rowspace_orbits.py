#!/usr/bin/env python3
"""Exact codec, orbit and Fourier-block checks; no tape timing claims."""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product, combinations
from math import prod
from pathlib import Path
import json
import random


def basis(rows):
    piv = {}
    for value in rows:
        while value:
            p = value.bit_length() - 1
            if p in piv:
                value ^= piv[p]
            else:
                piv[p] = value
                break
    for p in sorted(piv):
        for q in piv:
            if q != p and (piv[q] >> p) & 1:
                piv[q] ^= piv[p]
    return tuple(piv[p] for p in sorted(piv, reverse=True))


def in_span(value, rows):
    for row in basis(rows):
        if (value >> (row.bit_length() - 1)) & 1:
            value ^= row
    return value == 0


def span(rows):
    result = [0]
    for row in rows:
        result += [x ^ row for x in result]
    return set(result)


def orbit_size(a, r):
    return prod((1 << a) - (1 << j) for j in range(r))


def prefix_count(a, previous, prefix, length):
    projected = [x >> (a - length) for x in previous]
    rho = len(basis(projected))
    excluded = (1 << (len(previous) - rho)) if in_span(prefix, projected) else 0
    return (1 << (a - length)) - excluded


def rank_columns(a, cols):
    rank = 0
    previous = []
    r = len(cols)
    for j, value in enumerate(cols):
        assert not in_span(value, previous)
        later = prod((1 << a) - (1 << v) for v in range(j + 1, r))
        prefix = 0
        for t in range(1, a + 1):
            bit = (value >> (a - t)) & 1
            if bit:
                rank += prefix_count(a, previous, prefix << 1, t) * later
            prefix = (prefix << 1) | bit
        previous.append(value)
    return rank


def unrank_columns(a, r, ordinal):
    assert 0 <= ordinal < orbit_size(a, r)
    cols = []
    for j in range(r):
        later = prod((1 << a) - (1 << v) for v in range(j + 1, r))
        prefix = 0
        for t in range(1, a + 1):
            count = prefix_count(a, cols, prefix << 1, t) * later
            if ordinal < count:
                prefix <<= 1
            else:
                ordinal -= count
                prefix = (prefix << 1) | 1
        assert not in_span(prefix, cols)
        cols.append(prefix)
    assert ordinal == 0
    return tuple(cols)


def coordinates(rows):
    b = basis(rows)
    pivots = [x.bit_length() - 1 for x in b]
    cols = tuple(sum(((row >> p) & 1) << i for i, row in enumerate(rows))
                 for p in pivots)
    return b, cols


def reconstruct(b, cols, a):
    return tuple(xor_sum(v for j, v in enumerate(b) if (cols[j] >> i) & 1)
                 for i in range(a))


def xor_sum(values):
    out = 0
    for value in values:
        out ^= value
    return out


def linear_rows(matrix, rows):
    return tuple(xor_sum(x for j, x in enumerate(rows) if (mask >> j) & 1)
                 for mask in matrix)


def linear_column(matrix, value):
    return sum(((mask & value).bit_count() & 1) << i
               for i, mask in enumerate(matrix))


def rational_rank_sparse(rows):
    pivots = {}
    for source in rows:
        row = {k: Fraction(v) for k, v in source.items() if v}
        while row:
            p = min(row)
            if p not in pivots:
                scale = row[p]
                pivots[p] = {j: value / scale for j, value in row.items()}
                break
            scale = row[p]
            for j, value in pivots[p].items():
                row[j] = row.get(j, Fraction()) - scale * value
                if row[j] == 0:
                    del row[j]
    return len(pivots)


def gram_rank(b):
    gram = [sum(((u & v).bit_count() & 1) << j for j, v in enumerate(b)) for u in b]
    return len(basis(gram))


def main():
    rng = random.Random(261105)
    checks = dict(codec_ranks=0, large_codec_samples=0, address_roundtrips=0,
                  orbit_sizes=0, gl_action_identities=0, child_support_cases=0,
                  fourier_blocks=0, zero_blocks=0, degenerate_controls=0,
                  nondegenerate_blocks=0)
    for a in range(1, 5):
        for r in range(a + 1):
            count = 0
            for cols in product(range(1 << a), repeat=r):
                if len(basis(cols)) != r:
                    continue
                assert rank_columns(a, cols) == count
                assert unrank_columns(a, r, count) == cols
                count += 1
                checks['codec_ranks'] += 1
            assert count == orbit_size(a, r)

    for a in (5, 7, 11, 17):
        for r in (0, 1, a // 2, a):
            h = orbit_size(a, r)
            for ordinal in {0, h - 1, h // 2, *(rng.randrange(h) for _ in range(8))}:
                cols = unrank_columns(a, r, ordinal)
                assert rank_columns(a, cols) == ordinal
                checks['large_codec_samples'] += 1

    orbit_cache = {}
    for a, f in ((1, 4), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4)):
        groups = defaultdict(list)
        gl = [tuple(1 << i for i in range(a))]
        while len(gl) < 4:
            matrix = tuple(rng.randrange(1 << a) for _ in range(a))
            if len(basis(matrix)) == a:
                gl.append(matrix)
        for rows in product(range(1 << f), repeat=a):
            b, cols = coordinates(rows)
            assert reconstruct(b, cols, a) == rows
            assert unrank_columns(a, len(b), rank_columns(a, cols)) == cols
            groups[b].append(rows)
            checks['address_roundtrips'] += 1
            for matrix in gl:
                changed = linear_rows(matrix, rows)
                b2, cols2 = coordinates(changed)
                assert b2 == b
                assert cols2 == tuple(linear_column(matrix, c) for c in cols)
                checks['gl_action_identities'] += 1
        for b, members in groups.items():
            assert len(members) == orbit_size(a, len(b))
            checks['orbit_sizes'] += 1
        orbit_cache[(a, f)] = groups

    for a in (1, 2, 4):
        for f in range(1, 11):
            reached = {basis((y,) + (0,) * (a - 1)) for y in range(1 << f)}
            assert len(reached) == 1 << f
            checks['child_support_cases'] += 1

    for a, f in ((2, 3), (2, 4), (3, 4)):
        groups = orbit_cache[(a, f)]
        spaces = [b for b in groups if len(b) == a]
        pairs = list(combinations(spaces, 2))
        if a == 3:
            rng.shuffle(pairs)
            pairs = pairs[:18]
        for w, z in pairs:
            inter = basis(span(w) & span(z))
            inputs, outputs = groups[w], groups[z]
            matrix = []
            for target in outputs:
                row = {}
                for j, source in enumerate(inputs):
                    if target[1:] == source[1:]:
                        row[j] = (-1) ** ((target[0] & source[0]).bit_count() & 1)
                matrix.append(row)
            rank = rational_rank_sparse(matrix)
            if len(inter) < a - 1:
                assert rank == 0
                checks['zero_blocks'] += 1
            else:
                t = gram_rank(inter)
                expected = (1 << t) * orbit_size(a - 1, a - 1)
                assert rank == expected
                if t == a - 1:
                    assert rank * ((1 << a) - 1) == orbit_size(a, a)
                    checks['nondegenerate_blocks'] += 1
                else:
                    assert rank * ((1 << a) - 1) < orbit_size(a, a)
                    checks['degenerate_controls'] += 1
            checks['fourier_blocks'] += 1

    here = Path(__file__).resolve().parent
    result = dict(status='passed', deterministic_seed=261105, checks=checks,
                  scope='Exact finite algebra/codecs and sparse rational matrix ranks, not physical tape execution, asymptotic timing or a formal-kernel proof.',
                  files={p.name: sha256(p.read_bytes()).hexdigest() for p in
                         (Path(__file__), here / 'rowspace-orbit-compiler.md')})
    (here / 'rowspace-orbit-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
