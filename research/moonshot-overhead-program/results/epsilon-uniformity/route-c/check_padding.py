#!/usr/bin/env python3
"""Finite exact witnesses for SOURCE-PADDING-BARRIER.md; not a universal proof."""

from fractions import Fraction
from pathlib import Path
import json
from math import isqrt


def padding_ratio(radix: int, width: int) -> Fraction:
    target = 1 << width
    padded = 1
    while padded < target:
        padded *= radix
    return Fraction(padded, target)


def is_prime(value: int) -> bool:
    return value >= 2 and all(value % p for p in range(2, isqrt(value) + 1))


def next_prime(value: int) -> int:
    value += 1
    while not is_prime(value):
        value += 1
    return value


def maximum_padding(radix: int, start: int, end: int):
    target = 1 << start
    padded = 1
    exponent = 0
    best = (start, Fraction(0), 0)
    for width in range(start, end + 1):
        while padded < target:
            padded *= radix
            exponent += 1
        ratio = Fraction(padded, target)
        if ratio > best[1]:
            best = (width, ratio, exponent)
        target <<= 1
    return best


def main():
    interval_cases = 0
    for radix in [2, 3, 4, 5, 7, 8, 11, 17, 31, 37, 67, 257, 1021]:
        for start in range(0, 40):
            for diameter in [0, 1, 2, 3, 5, 10, 25, 50]:
                maximum = max(padding_ratio(radix, u) for u in range(start, start + diameter + 1))
                assert maximum >= min(Fraction(1 << diameter), Fraction(radix, 2))
                interval_cases += 1

    witnesses = []
    for root_degree in [2, 3, 4]:
        for m in range(2, 12):
            radix = next_prime(1 << m)
            assert radix > (1 << m)
            start = m**root_degree
            end = (m + 1)**root_degree - 1
            witness, ratio, radix_exponent = maximum_padding(radix, start, end)
            inflation = ratio * ratio
            assert inflation >= 4 ** (m - 1)
            witnesses.append({
                "root_degree": root_degree,
                "m": m,
                "radix_prime": radix,
                "interval_start": start,
                "interval_end": end,
                "witness_width": witness,
                "volume_inflation_exact": {"numerator": f"{radix}^{2 * radix_exponent}", "denominator": f"2^{2 * witness}"},
                "volume_inflation_illustration": float(inflation),
                "proved_threshold": str(4 ** (m - 1)),
            })

    # Negative control: radix two has zero binary padding cost at all widths,
    # and does not satisfy the source's b > W >= 2^m premise for m >= 2.
    assert all(padding_ratio(2, u) == 1 for u in range(100))

    output = {
        "status": "finite_exact_checks_passed",
        "scope": "Lemma P1 on finite intervals; prime-radix witnesses for P2; bounded-radix negative control",
        "interval_cases": interval_cases,
        "witness_cases": len(witnesses),
        "universal_proof": "SOURCE-PADDING-BARRIER.md, Lemma P1 and Theorem P2",
        "not_claimed": ["lower bound on arbitrary interchangers", "lower bound on multiplication", "actual source implementation replay"],
        "witnesses": witnesses,
    }
    serialized = json.dumps(output, indent=2) + "\n"
    Path(__file__).with_name("padding-verification.json").write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
