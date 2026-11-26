#!/usr/bin/env python3
"""Exact controls for the explicitly shaped tall-Hankel repair interface."""
from fractions import Fraction
from itertools import product
from pathlib import Path
from random import Random
import hashlib
import json


def kernel_vector(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivots = []
    for j in range(cols):
        k = len(pivots)
        p = next((i for i in range(k, rows) if a[i][j]), None)
        if p is None:
            continue
        a[k], a[p] = a[p], a[k]
        z = a[k][j]
        a[k] = [v/z for v in a[k]]
        for i in range(rows):
            if i != k and a[i][j]:
                z = a[i][j]
                a[i] = [v-z*w for v, w in zip(a[i], a[k])]
        pivots.append(j)
    if len(pivots) == cols:
        return None
    free = next(j for j in range(cols) if j not in pivots)
    q = [Fraction(0)]*cols
    q[free] = 1
    for i, j in enumerate(pivots):
        q[j] = -a[i][free]
    assert all(sum(x*y for x, y in zip(row, q)) == 0 for row in matrix)
    return q


def convolution(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def main():
    counts = {"sequences_examined": 0, "promised_sequences": 0,
              "prefix_recurrence_identities": 0, "zero_prefix_suffix_injectivity": 0,
              "reversed_product_tails": 0, "terminal_impulse_controls": 0,
              "unpromised_hidden_middle_controls": 0}
    for d in range(3, 9):
        for s in range(1, d//3+1):
            for seq in product((-1, 0, 1), repeat=d):
                counts["sequences_examined"] += 1
                q = kernel_vector([[seq[i+j] for j in range(s+1)] for i in range(d-s)])
                if q is None:
                    continue
                counts["promised_sequences"] += 1
                r = max(j for j, x in enumerate(q) if x)
                if r == 0:
                    assert not any(seq[:d-s])
                else:
                    extension = [Fraction(x) for x in seq[:r]]
                    while len(extension) < d-s:
                        i = len(extension)-r
                        extension.append(-sum(q[j]*extension[i+j] for j in range(r))/q[r])
                    assert extension == list(seq[:d-s])
                    counts["prefix_recurrence_identities"] += d-s-r
                if not any(seq[:s]) and not any(seq[-s:]):
                    assert not any(seq)
                    counts["zero_prefix_suffix_injectivity"] += 1
            terminal = [0]*(d-1)+[1]
            assert kernel_vector([[terminal[i+j] for j in range(s+1)] for i in range(d-s)]) is not None
            assert not any(terminal[:2*s]) and terminal[-1]
            counts["terminal_impulse_controls"] += 1
            if d > 3*s:
                hidden = [0]*d
                hidden[2*s] = 1
                assert not any(hidden[:2*s]) and not any(hidden[-s:])
                assert kernel_vector([[hidden[i+j] for j in range(s+1)] for i in range(d-s)]) is None
                counts["unpromised_hidden_middle_controls"] += 1
    rng = Random(2026112613)
    for h in range(2, 19):
        for s in range(1, 2*h//3+1):
            a, b = ([rng.randrange(32) for _ in range(h)] for _ in range(2))
            full = convolution(a, b)+[0]
            reversed_prefix = convolution(list(reversed(a))[:s], list(reversed(b))[:s])
            tail = [reversed_prefix[2*h-2-i] if i <= 2*h-2 else 0 for i in range(2*h-s, 2*h)]
            assert tail == full[-s:]
            counts["reversed_product_tails"] += 1
    result = {"status": "passed", "arithmetic": "exact rationals and integers",
              "counts": counts, "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Tall-Hankel prefix implication and exact tail indexing; not an arbitrary Hankel promise or tape simulation"}
    Path(__file__).with_name("tall-hankel-verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
