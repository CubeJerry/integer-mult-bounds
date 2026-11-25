#!/usr/bin/env python3
"""Exact finite checks for the reviewed composite-radix and digit-move lemmas.

These are arithmetic/permutation checks, not a multitape implementation or
an experimental proof of the asymptotic time/space statements.
"""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
COUNTS = {
    "radix_selection": 0,
    "combined_padding": 0,
    "previous_congruence_rejected": 0,
    "selected_b_with_small_divisor": 0,
    "composite_matrix_specialization": 0,
    "short_digit_forward_inverse": 0,
}


def height(q: int, w: int, u: int) -> int:
    return q.bit_length() + w.bit_length() + 2 * (u + 1).bit_length() + 4


def root_ceil(u: int, e: int) -> int:
    target = 1 << u
    low, high = 1, 1 << ((u + e - 1) // e)
    while low < high:
        mid = (low + high) // 2
        if mid ** e >= target:
            high = mid
        else:
            low = mid + 1
    return low


def check_radix(q: int, w: int, u: int) -> None:
    h = height(q, w, u)
    assert u >= 2 * h
    e = u // h
    a = root_ceil(u, e)
    b = 1 + q * ((a - 1 + q - 1) // q)
    rpower = b ** e
    target = 1 << u
    s = u + 1
    batch = w * ((b + w - 1) // w)
    assert b % 2 == 1 and gcd(b, q) == 1 and b > w
    assert b.bit_length() <= 2 * h + 2
    assert a ** e >= target and (a - 1) ** e < target
    assert target <= rpower
    assert 4 * s * rpower <= (4 * s + 1) * target
    assert b <= batch
    assert 16 * s * s * batch < (16 * s * s + 1) * b
    assert s * rpower * rpower * batch <= (s + 1) * target * target * b
    assert b - q >= 1 and (b - q) ** e < target
    COUNTS["radix_selection"] += 1
    COUNTS["combined_padding"] += 1
    COUNTS["previous_congruence_rejected"] += 1
    if any(b > p and b % p == 0 for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)):
        COUNTS["selected_b_with_small_divisor"] += 1


def rational_mod(x: Fraction, modulus: int) -> int:
    return (x.numerator * pow(x.denominator, -1, modulus)) % modulus


def matrix_product(a: list[list[int]], b: list[list[int]], modulus: int) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(2)) % modulus
             for j in range(2)] for i in range(2)]


def swap_bit_gap(data: list[object], prefix: int, gap: int, tail: int) -> list[object]:
    assert len(data) == prefix * 2 * gap * tail
    return [data[(((p * 2 + bit) * gap + g) * tail) + t]
            for p in range(prefix) for g in range(gap)
            for bit in range(2) for t in range(tail)]


def unswap_bit_gap(data: list[object], prefix: int, gap: int, tail: int) -> list[object]:
    assert len(data) == prefix * gap * 2 * tail
    return [data[(((p * gap + g) * 2 + bit) * tail) + t]
            for p in range(prefix) for bit in range(2)
            for g in range(gap) for t in range(tail)]


def check_digit(p: int, b: int, g: int, t: int) -> None:
    a = 1 << (b - 1).bit_length()
    volume = p * b * g * t
    initial = [(i, digit, gap, tail) if digit < b else None
               for i in range(p) for digit in range(a)
               for gap in range(g) for tail in range(t)]
    assert len(initial) < 2 * volume
    current = initial
    remaining, moved = a, 1
    history = []
    while remaining > 1:
        prefix, tail = p * (remaining // 2), moved * t
        history.append((prefix, g, tail))
        current = swap_bit_gap(current, prefix, g, tail)
        remaining //= 2
        moved *= 2
    stripped = [current[(((i * g + gap) * a + digit) * t) + tail]
                for i in range(p) for gap in range(g)
                for digit in range(b) for tail in range(t)]
    expected = [(i, digit, gap, tail) for i in range(p)
                for gap in range(g) for digit in range(b) for tail in range(t)]
    assert stripped == expected
    for dims in reversed(history):
        current = unswap_bit_gap(current, *dims)
    assert current == initial
    COUNTS["short_digit_forward_inverse"] += 1


def main() -> None:
    for q in (2, 6, 30, 210, 2310, 30030, 510510, 9699690,
              200560490130, 614889782588491410):
        for w in (1, 2, 3, 17, 1000, 1000001):
            minimum = 1
            while minimum < 2 * height(q, w, minimum):
                minimum += 1
            widths = {minimum + j for j in range(7)}
            widths.update((2 * minimum - 1, 2 * minimum, 2 * minimum + 1,
                           4 * minimum, 8 * minimum, 16 * minimum, 4096, 8192))
            for u in sorted(widths):
                if u >= 2 * height(q, w, u):
                    check_radix(q, w, u)
    left = [[Fraction(3, 5), Fraction(0)], [Fraction(2, 7), Fraction(5, 3)]]
    inverse = [[Fraction(5, 3), Fraction(0)], [Fraction(-2, 7), Fraction(3, 5)]]
    for b in (841, 1681, 5041, 19321):
        assert b % 210 == 1
        for f in range(1, 5):
            modulus = b ** f
            lm = [[rational_mod(x, modulus) for x in row] for row in left]
            im = [[rational_mod(x, modulus) for x in row] for row in inverse]
            assert matrix_product(lm, im, modulus) == [[1, 0], [0, 1]]
            assert matrix_product(im, lm, modulus) == [[1, 0], [0, 1]]
            COUNTS["composite_matrix_specialization"] += 1
    for p in range(1, 4):
        for b in range(2, 26):
            for g in range(1, 9):
                for t in range(1, 4):
                    check_digit(p, b, g, t)
    reviewed = ROOT.parent / "e002-route-b/composite-radix-padding.md"
    report = {
        "status": "PASS",
        "counts": COUNTS,
        "reviewed_sha256": sha256(reviewed.read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "limits": "Exact finite identities only; no physical tape execution or asymptotic verification.",
    }
    (ROOT / "composite-radix-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
