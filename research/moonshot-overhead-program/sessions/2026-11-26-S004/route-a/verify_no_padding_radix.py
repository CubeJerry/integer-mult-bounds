#!/usr/bin/env python3
"""Exact finite checks for the no-padding radix wrapper; no tape-time claim."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def ceil_log(n: int, b: int) -> int:
    e, p = 0, 1
    while p < n:
        p *= b
        e += 1
    return e


def blocks(m: int, b: int):
    u = (m - 1).bit_length()
    digits = []
    x = m
    while x:
        digits.append(x % b)
        x //= b
    e = len(digits) - 1
    q = min(e + 1, 1 + ceil_log(u + 1, b))
    retained = []
    start = 0
    for p in range(e, e - q, -1):
        for _ in range(digits[p]):
            stop = start + b**p
            retained.append((start, stop, p))
            start = stop
    return u, e, q, digits, retained, start


def rectangular_source(p: int, q: int, b: int, gap: int):
    """Decomposition: one equal-field swap and a charged small-field move."""
    values = [(x, g, y) for x in range(b**p) for g in range(gap) for y in range(b**q)]
    if p >= q:
        lo = b**q
        # After R_b(q), h remains the outer spectator, then move h across y,g.
        stage = sorted(values, key=lambda t: (t[0] // lo, t[2], t[1], t[0] % lo))
        output = sorted(stage, key=lambda t: (t[2], t[1], t[0] // lo, t[0] % lo))
    else:
        lo = b**p
        # Move y-high to the outer spectator, then swap x with y-low.
        stage = sorted(values, key=lambda t: (t[2] // lo, t[0], t[1], t[2] % lo))
        output = sorted(stage, key=lambda t: (t[2] // lo, t[2] % lo, t[1], t[0]))
    expected = [(x, g, y) for y in range(b**q) for g in range(gap) for x in range(b**p)]
    assert output == expected
    return len(values), stage != expected


def wrapper_permutation(m: int, b: int, gap: int):
    u, e, q, digits, leading, tail_start = blocks(m, b)
    output = {}
    for start_x, stop_x, p in leading:
        for start_y, stop_y, q0 in leading:
            payload = [(x, g, y) for x in range(start_x, stop_x) for g in range(gap) for y in range(start_y, stop_y)]
            returned = sorted(payload, key=lambda t: (t[2], t[1], t[0]))
            for x, g, y in returned:
                assert (y, g, x) not in output
                output[y, g, x] = (x, g, y)
    # Two disjoint tail rectangles, with exact generic transpose.
    for xs, xe, ys, ye in [(tail_start, m, 0, m), (0, tail_start, tail_start, m)]:
        payload = [(x, g, y) for x in range(xs, xe) for g in range(gap) for y in range(ys, ye)]
        for x, g, y in sorted(payload, key=lambda t: (t[2], t[1], t[0])):
            assert (y, g, x) not in output
            output[y, g, x] = (x, g, y)
    actual = [output[y, g, x] for y in range(m) for g in range(gap) for x in range(m)]
    expected = [(x, g, y) for y in range(m) for g in range(gap) for x in range(m)]
    assert actual == expected and len(output) == m * m * gap
    return m * m * gap


def main():
    profile_cases = 0
    tail_cases = 0
    worst_correction_ratio = Fraction(0)
    for m in range(2, 2049):
        for b in range(2, min(m, 33) + 1):
            u, e, q, digits, leading, end = blocks(m, b)
            r = m - end
            assert all(lo < hi and hi - lo == b**p for lo, hi, p in leading)
            assert sum(hi - lo for lo, hi, _ in leading) == end
            assert len(leading) <= (b - 1) * q
            assert r * (u + 1) <= m
            if r:
                tail_cases += 1
                assert r < b ** (e - q + 1)
            volume = m * m
            weighted = 0
            for p in range(e - q + 1, e + 1):
                for q0 in range(e - q + 1, e + 1):
                    v = digits[p] * digits[q0] * b ** (p + q0)
                    term = b ** abs(p - q0) * v
                    assert term <= b * volume
                    weighted += term
            assert weighted <= b * q * q * volume
            worst_correction_ratio = max(worst_correction_ratio, Fraction(weighted, volume))
            profile_cases += 1

    rectangle_cases = 0
    rectangle_symbols = 0
    negative_controls = 0
    for b in range(2, 7):
        for p in range(5):
            for q in range(5):
                if b ** (p + q) > 20000:
                    continue
                for gap in (1, 2):
                    n, nontrivial = rectangular_source(p, q, b, gap)
                    rectangle_symbols += n
                    rectangle_cases += 1
                    if p > q and q > 0 and nontrivial:
                        negative_controls += 1
    assert negative_controls > 0

    permutations = 0
    permutation_symbols = 0
    for m in range(2, 96):
        for b in range(2, min(m, 11) + 1):
            for gap in (1, 2):
                permutation_symbols += wrapper_permutation(m, b, gap)
                permutations += 1

    result = {
        "status": "passed",
        "profile_cases": profile_cases,
        "nonempty_tail_cases": tail_cases,
        "exact_rectangular_decomposition_cases": rectangle_cases,
        "rectangular_symbols": rectangle_symbols,
        "full_wrapper_permutation_cases": permutations,
        "full_wrapper_symbols": permutation_symbols,
        "negative_controls_omitting_unequal_field_move_rejected": negative_controls,
        "max_observed_weighted_correction_over_volume": str(worst_correction_ratio),
        "arithmetic": "exact integer and Fraction",
        "scope": "finite combinatorial identities and invoices, not a tape implementation or asymptotic proof",
    }
    path = Path(__file__).with_name("no-padding-radix-verification.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
