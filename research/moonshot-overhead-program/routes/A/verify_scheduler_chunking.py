#!/usr/bin/env python3
"""Exact arithmetic checks for A1--A4; not a tape-machine or complexity proof."""

from fractions import Fraction
from math import isqrt
import json
import random


def ceil_log2(value: int) -> int:
    assert value >= 1
    return (value - 1).bit_length()


def code_length(index: int) -> int:
    assert index >= 1
    bucket = index.bit_length() - 1
    return bucket + 2 * ceil_log2(bucket + 1) + 3


def pair_index(h: int, k: int) -> int:
    assert h >= 2 and k >= 0
    diagonal = h - 1 + k
    return 2 + diagonal * (diagonal - 1) // 2 + k


def decode_pair(index: int) -> tuple[int, int]:
    assert index >= 2
    offset = index - 2
    diagonal = (1 + isqrt(1 + 8 * offset)) // 2
    while diagonal * (diagonal - 1) // 2 > offset:
        diagonal -= 1
    while (diagonal + 1) * diagonal // 2 <= offset:
        diagonal += 1
    k = offset - diagonal * (diagonal - 1) // 2
    return diagonal - k + 1, k


def assembled_product(x: int, y: int, n: int, r: int) -> int:
    """Exact diagonal assembly with a candidate simulated by Python multiply."""
    assert 0 <= x < 1 << n and 0 <= y < 1 << n
    assert 1 <= r <= n
    width = (n + r - 1) // r
    base = 1 << width
    mask = base - 1
    x_chunks = [(x >> (a * width)) & mask for a in range(r)]
    y_chunks = [(y >> (b * width)) & mask for b in range(r)]
    carry = 0
    result = 0
    product_count = 0
    for diagonal in range(2 * r):
        accumulator = carry
        for a in range(max(0, diagonal - r + 1), min(r - 1, diagonal) + 1):
            b = diagonal - a
            if b >= r:
                continue
            accumulator += x_chunks[a] * y_chunks[b]
            product_count += 1
            assert accumulator < r * base * base
        digit = accumulator & mask
        carry = accumulator >> width
        assert carry <= r * (base - 1)
        result |= digit << (diagonal * width)
    assert product_count == r * r
    assert carry == 0
    assert result < 1 << (2 * n)
    return result


def verify_schedule() -> dict:
    mass = Fraction(0)
    for bucket in range(4096):
        mass += Fraction(1, 1 << (2 * ceil_log2(bucket + 1) + 3))
    assert mass < Fraction(3, 16)
    assert Fraction(3, 16) - mass == Fraction(1, 1 << 16)
    worst_control_ratio = Fraction(0)
    for round_index in range(1, 1025):
        eligible = [
            bucket for bucket in range(round_index + 1)
            if bucket + 2 * ceil_log2(bucket + 1) + 3 <= round_index
        ]
        if not eligible:
            continue
        count = (1 << (eligible[-1] + 1)) - 1
        work = sum(
            1 << (round_index - 2 * ceil_log2(bucket + 1) - 3)
            for bucket in eligible
        )
        assert 16 * work <= 3 * (1 << round_index)
        control_ratio = Fraction(count * (round_index + 1) ** 2, 1 << round_index)
        worst_control_ratio = max(worst_control_ratio, control_ratio)
        assert control_ratio <= 32
    for index in range(1, 20000):
        length = code_length(index)
        bucket = index.bit_length() - 1
        assert (1 << length) <= 32 * index * (bucket + 1) ** 2
        for completion in (0, 1, 2, 3, 7, 16, 100, 10000):
            success_round = length + ceil_log2(completion + 1)
            assert 1 << (success_round - length) >= completion
            assert 1 << success_round <= (1 << (length + 1)) * (completion + 1)
    for index in range(2, 20000):
        h, k = decode_pair(index)
        assert pair_index(h, k) == index
        assert index <= (h + k) ** 2
    return {
        "rounds_checked": 1024,
        "indices_checked": 19999,
        "partial_kraft_mass": str(mass),
        "proved_infinite_kraft_mass": "3/16 (see proof, not inferred from scan)",
        "maximum_checked_control_ratio": str(worst_control_ratio),
    }


def verify_assembly() -> dict:
    checks = 0
    for n in range(1, 8):
        for r in range(1, n + 1):
            for x in range(1 << n):
                for y in range(1 << n):
                    assert assembled_product(x, y, n, r) == x * y
                    checks += 1
    rng = random.Random(20261126)
    larger = 0
    for n in (8, 9, 17, 31, 64, 127, 256):
        counts = sorted({1, 2, max(1, n // 2), max(1, n - 1), n})
        for r in counts:
            edge = (0, 1, (1 << n) - 1, 1 << (n - 1))
            for x in edge:
                for y in edge:
                    assert assembled_product(x, y, n, r) == x * y
                    larger += 1
            for _ in range(12):
                x, y = rng.getrandbits(n), rng.getrandbits(n)
                assert assembled_product(x, y, n, r) == x * y
                larger += 1
    # Negative control: dropping incoming carries is wrong even at one bit/chunk.
    n, r, x, y = 2, 2, 3, 3
    wrong_no_carry = 1 | (0 << 1) | (1 << 2)
    assert wrong_no_carry != x * y
    assert assembled_product(x, y, n, r) == 9
    return {"exhaustive_cases": checks, "larger_cases": larger,
            "negative_control_detected": "omitting cross-diagonal carry"}


def verify_cap() -> dict:
    cases = 0
    for c in range(1, 65):
        r = 1 << ceil_log2(4 * c)
        assert 4 * c <= r < 8 * c
        for fixed_space in (1, c, 1000 * c):
            for cutoff in (1, 2, 3, 7, 101):
                threshold = max(8 * c, 4 * (c + fixed_space), r * cutoff)
                for n in (threshold, threshold + 1, threshold + r - 1, 2 * threshold):
                    width = (n + r - 1) // r
                    assert 1 <= r <= n and width >= cutoff
                    assert 2 * (c * width + fixed_space) <= n
                    assert r * r * width <= 2 * n * r
                    cases += 1
    return {"boundary_cases": cases}


def verify_thresholds() -> dict:
    polynomial = 0
    for degree in range(17):
        for log_constant in range(17):
            q = degree + log_constant + 1
            for k in (64 * q * q, 64 * q * q + 1, 256 * q * q):
                lhs = (1 << log_constant) * (1 + k) ** degree
                assert lhs <= (1 << (k // 4))
                polynomial += 1
    logarithmic = 0
    # Exact checks of the coarse consequence (1+s)^b <= (4b/epsilon)^b 2^(epsilon s).
    for degree in range(1, 9):
        for inverse_slack in range(1, 17):
            for s in (0, 1, 2, 4, 16, 64, 256, 1024):
                assert (1 + s) ** (degree * inverse_slack) <= (
                    (4 * degree * inverse_slack) ** (degree * inverse_slack) * (1 << s)
                )
                logarithmic += 1
    for arity in range(3, 17):
        for calls in range(2, 33):
            for depth in range(12):
                nodes = (arity - 1) * sum(sum(calls ** level for level in range(j + 1))
                                          for j in range(depth + 1))
                assert nodes <= 4 * arity * calls ** depth
    return {"polynomial_threshold_cases": polynomial,
            "exact_log_slack_cases": logarithmic, "node_count_cases": 14 * 31 * 12}


if __name__ == "__main__":
    print(json.dumps({"status": "passed", "scope": "exact arithmetic only",
                      "schedule": verify_schedule(), "assembly": verify_assembly(),
                      "cap": verify_cap(), "thresholds": verify_thresholds()}, indent=2))
