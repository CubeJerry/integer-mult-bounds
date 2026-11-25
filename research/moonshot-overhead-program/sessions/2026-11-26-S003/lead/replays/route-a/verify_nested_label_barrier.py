#!/usr/bin/env python3
"""Exact finite checks; not a full multiplier or formal proof."""
from fractions import Fraction
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import json
import platform
import sys
import numpy as np


def rank2(rows):
    basis = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p] = row
                break
    return len(basis)


def multiply2(left, right):
    result = []
    for row in left:
        out = 0
        while row:
            bit = row & -row
            out ^= right[bit.bit_length() - 1]
            row ^= bit
        result.append(out)
    return result


def tensor(previous, d, direct=False):
    n, h = len(previous), 2 * d - 1
    words = list(product(range(n), repeat=h))
    subsets = [set(s) for s in combinations(range(h), d)]
    rows = []
    for i, a in enumerate(words):
        row = 0
        for j, b in enumerate(words):
            if direct:
                changed = [k for k in range(h) if a[k] != b[k]]
                value = i == j or (len(changed) == d and all((previous[a[k]] >> b[k]) & 1 for k in changed))
            else:
                value = sum(all(((previous[a[k]] >> b[k]) & 1) if k in s else a[k] == b[k] for k in range(h)) for s in subsets) % 2
            row |= int(value) << j
        rows.append(row)
    return rows


def rankp(matrix, prime):
    a = matrix.astype(np.int64) % prime
    rank = 0
    for column in range(a.shape[1]):
        options = np.flatnonzero(a[rank:, column])
        if not len(options):
            continue
        pivot = rank + int(options[0])
        a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, column]), -1, prime) % prime
        if rank + 1 < a.shape[0]:
            factors = a[rank + 1:, column].copy()
            a[rank + 1:] = (a[rank + 1:] - factors[:, None] * a[rank][None, :]) % prime
        rank += 1
        if rank == a.shape[0]:
            break
    return rank


def gram(previous, d):
    words = list(product(range(len(previous)), repeat=2 * d - 1))
    out = np.zeros((2 * len(words), 2 * len(words)), dtype=np.int64)
    for i, a in enumerate(words):
        for j, b in enumerate(words):
            k = sum(x != y and ((previous[x] >> y) & 1) for x, y in zip(a, b))
            out[2 * i, 2 * j] = out[2 * i + 1, 2 * j + 1] = d - k
            out[2 * i, 2 * j + 1] = out[2 * i + 1, 2 * j] = k
    return out


def rectangles(q, d):
    h, t = 2 * d - 1, q.bit_length() - 1
    words = list(product(range(q), repeat=h))
    idx = {v: i for i, v in enumerate(words)}
    left_count, right_count = [0] * len(words), [0] * len(words)
    bit_parts = []
    for bit in range(t):
        suffix = t - bit - 1
        for prefix in range(1 << bit):
            zero = tuple((prefix << (suffix + 1)) + k for k in range(1 << suffix))
            one = tuple(k + (1 << suffix) for k in zero)
            bit_parts += [(zero, one), (one, zero)]
    seen, count = set(), 0
    for changed in combinations(range(h), d):
        unchanged = [i for i in range(h) if i not in changed]
        for common in product(range(q), repeat=len(unchanged)):
            for x, y in product(range(q), repeat=2):
                if x == y:
                    continue
                for parts in product(bit_parts, repeat=d - 1):
                    lc, rc = [()] * h, [()] * h
                    for i, v in zip(unchanged, common):
                        lc[i] = rc[i] = (v,)
                    lc[changed[0]], rc[changed[0]] = (x,), (y,)
                    for i, (l, r) in zip(changed[1:], parts):
                        lc[i], rc[i] = l, r
                    ls, rs = list(product(*lc)), list(product(*rc))
                    for side in (ls, rs):
                        assert all(sum(x != y for x, y in zip(v, w)) != d for v in side for w in side)
                    for v in ls:
                        left_count[idx[v]] += 1
                    for v in rs:
                        right_count[idx[v]] += 1
                    for v, w in product(ls, rs):
                        assert sum(x != y for x, y in zip(v, w)) == d
                        pair = idx[v], idx[w]
                        assert pair not in seen
                        seen.add(pair)
                    count += 1
    incidence = comb(h, d) * (q - 1) * t ** (d - 1)
    assert set(left_count) == set(right_count) == {incidence}
    assert len(seen) == len(words) * comb(h, d) * (q - 1) ** d
    return dict(q=q, d=d, rectangles=count, pairs=len(seen), exact_incidence=incidence)


def main():
    result = {"scope": "Finite exact support, actual-rank, Gram, incidence and integer-invoice checks; no full multiplier or formal proof.",
              "python": sys.version.split()[0], "numpy": np.__version__, "platform": platform.platform(),
              "source_openai_math": "3344da59991ed94f9ba711217b29c1d760badfa6",
              "programme_start": "0607d044d1d09489580da0e5828588820e1a6775"}
    count = 0
    for d in (2, 4, 8, 16, 32, 64, 128):
        for k in range(2 * d):
            coefficient = comb(2 * d - 1 - k, d - k) % 2 if k <= d else 0
            assert coefficient == int(k in (0, d))
            count += 1
    result["selector_cases"] = count
    cache, matrix_cases = {}, []
    for q, ds in ((2, (2,)), (4, (2,)), (2, (4,)), (2, (2, 2))):
        previous = [(1 << q) - 1] * q
        for d in ds:
            n, r = len(previous), rank2(previous)
            current = tensor(previous, d, direct=True)
            assert current == tensor(previous, d)
            assert not any(multiply2(current, current))
            assert rank2(current) >= r ** d * (n - r) ** (d - 1)
            adjacent = [row ^ (1 << i) for i, row in enumerate(current)]
            assert rank2(adjacent) == len(current)
            degrees = {row.bit_count() for row in adjacent}
            assert len(degrees) == 1 and next(iter(degrees)) % 2 == 1
            previous = current
        p, t = prod(ds), q.bit_length() - 1
        assert Fraction(rank2(previous), len(previous)) >= Fraction(1, 1 << (p * (t + 1) - 1))
        cache[q, ds] = previous
        matrix_cases.append(dict(q=q, distances=ds, size=len(previous), rank=rank2(previous)))
    result["actual_matrix_cases"] = matrix_cases
    square_zero_cases = []
    for n in range(2, 7):
        for r in range(1, n // 2 + 1):
            previous = [(1 << (r + i)) if i < r else 0 for i in range(n)]
            change = [1 << i for i in range(n)]
            change[0] ^= 1 << (n - 1)
            previous = multiply2(multiply2(change, previous), change)
            assert not any(multiply2(previous, previous))
            current = tensor(previous, 2)
            assert rank2(current) >= r ** 2 * (n - r)
            square_zero_cases.append(dict(n=n, rank=r, tensor_rank=rank2(current), lower=r ** 2 * (n - r)))
    result["arbitrary_square_zero_cases"] = square_zero_cases
    gram_cases = []
    for previous, name in (([3, 3], "base_two"), ([15] * 4, "base_four"), (cache[2, (2,)], "actual_two_level")):
        matrix = gram(previous, 2)
        expected = 2 + 3 * (len(previous) - 1)
        ranks = {p: rankp(matrix, p) for p in (101, 103)}
        assert set(ranks.values()) == {expected}
        gram_cases.append(dict(name=name, size=int(matrix.shape[0]), expected_rank=expected, ranks=ranks))
    result["gram_cases"] = gram_cases
    result["rectangle_cases"] = [rectangles(2, 2), rectangles(4, 2), rectangles(2, 4)]
    count = 0
    for depth in range(2, 7):
        for ds in product((2, 4, 8), repeat=depth):
            assert sum((d - 1) * prod(ds[i + 1:]) for i, d in enumerate(ds)) == prod(ds) - 1
            count += 1
    result["uniform_depth_telescoping_cases"] = count
    growth = []
    for j in (64, 128, 256):
        logj, t = j.bit_length() - 1, j * j
        logt = t.bit_length() - 1
        for depth in (2, 3, 4):
            ds = (16 * j,) + (2,) * (depth - 2) + (16 * j * (1 << (depth - 2)),)
            hs, p = tuple(2 * d - 1 for d in ds), prod(ds)
            x = p * t - (2 * p - 2)
            bound_lambda = comb(hs[0], ds[0]).bit_length() + t + (ds[0] - 1) * logt
            for h, d in zip(hs[1:], ds[1:]):
                bound_lambda = comb(h, d).bit_length() + d * bound_lambda
            bound_d = 1 + hs[-1].bit_length() + prod(hs[:-1]) * t
            bound_invoice = bound_d + bound_lambda + 2
            assert j * bound_invoice <= x
            assert 128 * x >= (1 << (depth - 2)) * j ** 3 * logj
            growth.append(dict(J=j, depth=depth, distances=ds, t=t, log2_m=x, upper_log_invoice=bound_invoice))
    result["positive_integer_invoice_cases"] = growth
    wrong = [comb(5 - k, 3 - k) % 2 for k in range(4)]
    assert wrong != [1, 0, 0, 1]
    actual = Fraction(rank2(cache[2, (2, 2)]), len(cache[2, (2, 2)]))
    j, x, d_address, incidence = 64, 640, 23, 27
    assert d_address * (1 + incidence) <= 1 << (x // j)
    assert 128 * x < j ** 3 * (j.bit_length() - 1)
    assert d_address * (1 + incidence) * (1 + (1 << x) * actual) > 1 << (x // j)
    result["negative_controls"] = {"non_power_two_distance_selector": wrong,
                                   "omitting_rank_term": dict(J=j, log2_m=x, D=d_address, incidence=incidence, actual_rank_fraction=str(actual))}
    result["passed"] = True
    path = Path(__file__).with_name("nested-label-verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"passed": True, "matrix_cases": len(matrix_cases), "arbitrary_square_zero_cases": len(square_zero_cases),
                      "gram_cases": len(gram_cases), "uniform_depth_cases": count, "positive_invoice_cases": len(growth),
                      "output": str(path)}, indent=2))


if __name__ == "__main__":
    main()
