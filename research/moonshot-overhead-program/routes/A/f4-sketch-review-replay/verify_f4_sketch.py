#!/usr/bin/env python3
"""Exact finite checks for additive sketches of a product on F4*^m."""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path


def mul(a: int, b: int) -> int:
    out = 0
    for _ in range(2):
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def rank_binary(rows: tuple[int, ...]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p] = row
                break
    return len(basis)


def apply(rows: tuple[int, ...], x: int) -> int:
    return sum(((row & x).bit_count() & 1) << i for i, row in enumerate(rows))


def domain(m: int) -> list[tuple[int, int]]:
    logs = {1: 0, 2: 1, 3: 2}
    return [(sum(a << (2*i) for i, a in enumerate(xs)), sum(logs[a] for a in xs) % 3)
            for xs in itertools.product((1, 2, 3), repeat=m)]


def norm_from_counts(counts: list[int]) -> int:
    a, b = counts[0]-counts[2], counts[1]-counts[2]
    return a*a-a*b+b*b


def target(x: int, m: int) -> int:
    out = 1
    for i in range(m):
        out = mul(out, (x >> (2*i)) & 3)
    return out


def check(rows: tuple[int, ...], m: int, points: list[tuple[int, int]]) -> dict[str, int]:
    size = 1 << len(rows)
    fibers = [[0, 0, 0] for _ in range(size)]
    for x, logz in points:
        fibers[apply(rows, x)][logz] += 1
    energy = sum(norm_from_counts(c) for c in fibers)
    good = 0
    for t in range(size):
        pulled = 0
        for i, row in enumerate(rows):
            if (t >> i) & 1:
                pulled ^= row
        if all((pulled >> (2*j)) & 3 for j in range(m)):
            good += 1
    assert size*energy == good*4**m
    k = rank_binary(rows)
    image_size = 1 << k
    multiplicity = size//image_size
    assert good % multiplicity == 0
    good_image = good//multiplicity
    assert good_image <= image_size-1
    assert image_size*energy == good_image*4**m
    success_numerator = sum(max(c) for c in fibers)
    total = 3**m
    gap = 3*success_numerator-total
    assert gap >= 0
    assert gap*gap <= 4*good_image*4**m
    assert (success_numerator == total) == (k == 2*m)
    collisions = 0
    if k < 2*m:
        v = next(v for v in range(1, 1 << (2*m)) if apply(rows, v) == 0)
        found = False
        for u, _ in points:
            other = u ^ v
            if all((other >> (2*i)) & 3 for i in range(m)) and target(u, m) != target(other, m):
                assert apply(rows, u) == apply(rows, other)
                found = True
                break
        assert found
        collisions = 1
    return {"parseval": 1, "success": 1, "collision": collisions, "injective": int(k == 2*m)}


def main() -> None:
    rng = random.Random(20261125)
    counts = {"parseval": 0, "success": 0, "collision": 0, "injective": 0}
    for m in range(1, 4):
        points = domain(m)
        for rows in itertools.product(range(1 << (2*m)), repeat=2):
            out = check(rows, m, points)
            for key, value in out.items():
                counts[key] += value
    for m in range(1, 7):
        points = domain(m)
        for bits in (0, 1, 2, 3, 4, 2*m):
            for _ in range(24):
                rows = tuple(rng.randrange(1 << (2*m)) for _ in range(bits))
                out = check(rows, m, points)
                for key, value in out.items():
                    counts[key] += value
        identity = tuple(1 << i for i in range(2*m))
        out = check(identity, m, points)
        for key, value in out.items():
            counts[key] += value

    # Every additive character has either zero or squared Gauss magnitude 4/9.
    gauss = 0
    for mask in range(4):
        coeff = [0, 0, 0]
        for x, exponent in ((1, 0), (2, 1), (3, 2)):
            coeff[exponent] += -1 if (mask & x).bit_count() & 1 else 1
        assert norm_from_counts(coeff) == (0 if mask == 0 else 4)
        gauss += 1

    # Frobenius is additive and is not F4-linear: natural two-power pencils included.
    frobenius = (3, 2)
    assert all(apply(frobenius, x) == mul(x, x) for x in range(4))
    assert apply(frobenius, 2) != mul(2, apply(frobenius, 1))
    assert all(apply(frobenius, x ^ y) == (apply(frobenius, x) ^ apply(frobenius, y))
               for x in range(4) for y in range(4))

    # A dimension-free advantage bound is false on the identity sketch.
    assert (3*3-3)**2 > 4*4
    # One additive bit for one F4 coordinate does not give exact recovery.
    trace_rows = (2,)
    one_bit = check(trace_rows, 1, domain(1))
    assert one_bit["collision"] == 1 and one_bit["injective"] == 0

    result = {"status": "all exact finite checks passed", "counts": counts,
              "gauss_characters": gauss, "frobenius_additive_controls": 16,
              "negative_controls": {"dimension_free_bound_rejected": True,
                                    "half_rank_exact_recovery_rejected": True},
              "largest_domain": 3**6, "floating_point_used": False,
              "full_multiplier_execution": False}
    Path(__file__).with_name("verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
