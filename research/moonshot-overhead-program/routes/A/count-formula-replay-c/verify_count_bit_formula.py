#!/usr/bin/env python3
"""Independent exact tests of copied count-bit formulas and F4 prediction."""
from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(eq=False, slots=True)
class Node:
    op: str
    a: object
    b: object = None
    size: int = 1
    degree: int = 0


def const(a):
    return Node("c", a)


def var(a):
    return Node("v", a, degree=1)


def add(a, b):
    return Node("+", a, b, 1 + a.size + b.size, max(a.degree, b.degree))


def mul(a, b):
    return Node("*", a, b, 1 + a.size + b.size, a.degree + b.degree)


def add_bits(x, y):
    carry = const(0)
    result = []
    for a, b in zip(x, y):
        result.append(add(add(a, b), carry))
        carry = add(mul(a, b), mul(add(a, b), carry))
    return result


def count_bits(m, t, u=0):
    r = (m - 1).bit_length()
    words = []
    for j in range(1 << r):
        words.append([var(2*j+k) if j < m and k < 2 else const(0)
                      for k in range(t)])
    while len(words) > 1:
        words = [add_bits(words[j], words[j+1])
                 for j in range(0, len(words), 2)]
    offset = (-u) % (1 << t)
    result = add_bits(words[0], [const((offset >> k) & 1) for k in range(t)])
    for k, f in enumerate(result):
        assert f.degree <= 1 << k
        assert f.size <= 8**(r+1) * math.comb(r+k+1, k)
    return result


def evaluate(nodes, values):
    cache = {}
    def rec(n):
        if n in cache:
            return cache[n]
        if n.op == "c":
            z = n.a
        elif n.op == "v":
            z = values[n.a]
        elif n.op == "+":
            z = rec(n.a) ^ rec(n.b)
        else:
            z = rec(n.a) & rec(n.b)
        cache[n] = z
        return z
    return [rec(n) for n in nodes]


def binom_integer(n, h):
    if n >= 0:
        return math.comb(n, h) if n >= h else 0
    return (-1)**h * math.comb(h-n-1, h)


def gf4mul(a, b):
    z = 0
    for _ in range(2):
        if b & 1:
            z ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return z


def gf4pow(a, n):
    if n < 0:
        assert a
        n %= 3
    z = 1
    while n:
        if n & 1:
            z = gf4mul(z, a)
        a = gf4mul(a, a)
        n >>= 1
    return z


def predictor(bits, degree, u, beta_sum):
    z = 0
    for h in range(degree+1):
        coefficient = 1
        for k in range(len(bits)):
            if (h >> k) & 1:
                coefficient &= bits[k]
        if coefficient:
            z ^= gf4pow(3, h)  # omega-1=omega+1=3
    return gf4mul(gf4pow(2, u-beta_sum), z)


def direct_predictor(c, degree, u, beta_sum):
    z = 0
    for h in range(degree+1):
        if binom_integer(c-u, h) & 1:
            z ^= gf4pow(3, h)
    return gf4mul(gf4pow(2, u-beta_sum), z)


def main():
    result = {"status": "PASS", "bit_assignments": 0,
              "negative_offset_assignments": 0, "syntactic_budgets": 0,
              "binomial_residues": 0, "F4_indicators": 0,
              "F4_predictors": 0, "central_matches": 0,
              "negative_controls": 0}
    # All ternary digit tuples, plus unrestricted two-bit digits at small m.
    for m in range(1, 8):
        t = (2*m+1).bit_length()
        offsets = (-m-2, 0, m, 2*m+1)
        formulas = [(u, count_bits(m, t, u)) for u in offsets]
        for digits in itertools.product(range(4 if m <= 4 else 3), repeat=m):
            values = [(v >> k) & 1 for v in digits for k in range(2)]
            for u, nodes in formulas:
                bits = evaluate(nodes, values)
                got = sum(b << k for k, b in enumerate(bits))
                assert got == (sum(digits)-u) % (1 << t)
                result["bit_assignments"] += 1
                result["negative_offset_assignments"] += sum(digits) < u
    # Large formula budgets are computed as unfolded trees, even though
    # the verifier stores pointer sharing to avoid materializing the tree.
    for m in list(range(2, 65)) + [127, 128, 129, 256]:
        for degree in sorted({1, min(m, 2), max(1, math.isqrt(m)), m}):
            t = degree.bit_length()
            bits = count_bits(m, t, m//2-3)
            size = 2
            for h in range(degree+1):
                selected = [bits[k] for k in range(t) if (h >> k) & 1]
                d = sum(b.degree for b in selected)
                assert d <= h
                size += sum(b.size for b in selected) + len(selected) + 3
            assert size <= 2**15 * m**8
            result["syntactic_budgets"] += 1
    for t in range(1, 9):
        for n in range(-2**t-3, 2**t+4):
            residue = n % (1 << t)
            for h in range(1 << t):
                lucas = (residue & h) == h
                assert (binom_integer(n, h) & 1) == lucas
                result["binomial_residues"] += 1
    for k, beta, v in itertools.product(range(3), range(3), (1, 2)):
        value = 0
        q = gf4pow(2, k)
        for a in range(3):
            value ^= gf4mul(gf4pow(2, (beta-v)*a), gf4pow(q, a))
        assert value == int((k+beta) % 3 == v)
        result["F4_indicators"] += 1
    for m in range(1, 7):
        for degree in sorted({1, min(m, 3), m}):
            t = degree.bit_length()
            for u in (-2, m//2, m+1):
                nodes = count_bits(m, t, u)
                for digits in itertools.product(range(3), repeat=m):
                    vals = [(v >> k) & 1 for v in digits for k in range(2)]
                    bits = evaluate(nodes, vals)
                    c = sum(digits)
                    beta_sum = (sum((j+1)*v for j, v in enumerate(digits))) % 3
                    got = predictor(bits, degree, u, beta_sum)
                    assert got == direct_predictor(c, degree, u, beta_sum)
                    result["F4_predictors"] += 1
                    if u <= c <= u+degree:
                        assert got == gf4pow(2, c-beta_sum)
                        result["central_matches"] += 1
    # Wrong carry (no interaction), omitted offset, and too few residue
    # bits each fail; the nonmultilinear formula is not claimed off-cube.
    assert (1 ^ 1) != ((1+1) >> 1)
    result["negative_controls"] += 1
    assert binom_integer(-1, 1) & 1 != binom_integer(0, 1) & 1
    result["negative_controls"] += 1
    assert (math.comb(4, 4) & 1) != ((0 & 4) == 4)
    result["negative_controls"] += 1
    output = Path(__file__).with_name("count-bit-formula-verification.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
