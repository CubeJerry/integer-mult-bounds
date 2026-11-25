#!/usr/bin/env python3
"""Exact finite checks for the nonstationary recursion note.

These checks validate integer boundaries, unfolding and negative controls.
They do not prove the infinite asymptotic bounds or implement interchange.
Run from any directory: python3 -B path/to/check_recurrence.py
"""

from fractions import Fraction
from math import isqrt, sqrt
import json
from pathlib import Path
import random


def integer_root(n: int, degree: int) -> int:
    """Return floor(n ** (1/degree)) using integers only."""
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + degree - 1) // degree)
    while True:
        y = ((degree - 1) * x + n // (x ** (degree - 1))) // degree
        if y >= x:
            while x**degree > n:
                x -= 1
            while (x + 1) ** degree <= n:
                x += 1
            return x
        x = y


def chain(e: int, r: int = 4, terminal: int = 1 << 32):
    """Use square arity floor(e^(1/(2r)))^2 and exact ceil division."""
    nodes = []
    while e > terminal:
        q = integer_root(e, 2 * r)
        m = q * q
        f = (e + m - 1) // m
        assert q ** (2 * r) <= e < (q + 1) ** (2 * r)
        assert 2 <= m and 1 <= f < e
        assert e <= m * f < e + m
        assert m**r <= e < (4 * m) ** r
        nodes.append((e, m, f, q))
        e = f
    return nodes, e


def excess(m: int, kind: str) -> Fraction:
    rank = max(1, m.bit_length().bit_length())
    if kind == "none":
        return Fraction(0)
    if kind == "summable":
        return Fraction(1, rank * rank)
    if kind == "borderline":
        return Fraction(1, rank)
    if kind == "constant":
        return Fraction(1, 8)
    raise ValueError(kind)


def bill(e: int, kind: str, critical_toll: bool = False):
    nodes, last = chain(e)
    terminal_bill = Fraction(isqrt(last) + 1)
    raw = terminal_bill
    for width, m, child, q in reversed(nodes):
        toll = isqrt(width) if critical_toll else m
        raw = toll + q * (1 + excess(m, kind)) * raw

    # Independently accumulate the forward unrolling and exact squared
    # normalized rounding product. No floating arithmetic enters assertions.
    factor = Fraction(1)
    forward = Fraction(0)
    rounding_squared = Fraction(1)
    arity_product = 1
    excess_sum = Fraction(0)
    for width, m, child, q in nodes:
        toll = isqrt(width) if critical_toll else m
        forward += factor * toll
        factor *= q * (1 + excess(m, kind))
        rounding_squared *= Fraction(m * child, width)
        arity_product *= m
        excess_sum += excess(m, kind)
    forward += factor * terminal_bill
    assert forward == raw
    assert rounding_squared == Fraction(arity_product * last, e)
    assert rounding_squared >= 1
    normalized_squared = raw * raw / e

    depth = len(nodes)
    if critical_toll and kind == "none":
        # sqrt(width)/2 <= floor(sqrt(width)) <= sqrt(width), while
        # the terminal normalized bill is between 1 and 2.
        assert normalized_squared >= Fraction((depth + 1) ** 2, 4)
        assert normalized_squared <= rounding_squared * (depth + 2) ** 2
    if kind == "constant":
        # A positive fixed mass excess cannot be removed by a cheap toll.
        assert normalized_squared >= Fraction(9, 8) ** (2 * depth)

    return {
        "depth": depth,
        "normalized_bill_illustration": sqrt(float(normalized_squared)),
        "rounding_product_squared": str(rounding_squared),
        "excess_sum_illustration": float(excess_sum),
    }


def main():
    rng = random.Random(20261126)
    root_cases = 0
    for degree in [2, 3, 4, 8, 12]:
        for base in range(2, 100):
            for delta in [-1, 0, 1]:
                n = base**degree + delta
                got = integer_root(n, degree)
                assert got**degree <= n < (got + 1) ** degree
                if degree == 2:
                    assert got == isqrt(n)
                root_cases += 1
        for _ in range(100):
            n = rng.getrandbits(rng.randrange(2, 2048))
            got = integer_root(n, degree)
            assert got**degree <= n < (got + 1) ** degree
            root_cases += 1

    rows = []
    for exponent in [40, 64, 96, 128, 256, 512, 1024, 2048, 4096]:
        e = 1 << exponent
        for delta in [-1, 0, 1]:
            for kind in ["none", "summable", "borderline", "constant"]:
                bill(e + delta, kind)
            bill(e + delta, "none", critical_toll=True)
        row = {"active_width": f"2^{exponent}"}
        for kind in ["summable", "borderline", "constant"]:
            result = bill(e, kind)
            # Keep the output compact; the exact fraction is checked above.
            result.pop("rounding_product_squared")
            row[kind] = result
        critical = bill(e, "none", critical_toll=True)
        critical.pop("rounding_product_squared")
        row["critical_toll_negative_control"] = critical
        rows.append(row)

    output = {
        "status": "finite_exact_checks_passed",
        "scope": "integer roots, ceiling boundaries, exact recurrence unfolding, rounding telescoping, critical-toll and fixed-excess negative controls",
        "not_verified": ["asymptotic theorem by computation", "one-level interchange family", "multiplication algorithm", "Lean formalization"],
        "integer_root_cases": root_cases,
        "recurrence_boundary_cases": 9 * 3 * 5,
        "illustrations": rows,
    }
    target = Path(__file__).with_name("verification.json")
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "illustrations"}, indent=2))


if __name__ == "__main__":
    main()
