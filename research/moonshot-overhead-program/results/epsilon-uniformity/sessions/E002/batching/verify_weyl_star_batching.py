#!/usr/bin/env python3
"""Exact finite checks of WB1--WB5 and its complete occupied coset layout.

No asymptotic tape-runtime simulation is claimed. Complex arithmetic uses
pairs of integers. Inverse Hadamard denominators are accumulated as one
known power of two and checked without rounding.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path

Z = tuple[int, int]
ZERO: Z = (0, 0)

def add(a: Z, b: Z) -> Z:
    return a[0] + b[0], a[1] + b[1]

def sub(a: Z, b: Z) -> Z:
    return a[0] - b[0], a[1] - b[1]

def scale(a: Z, c: int) -> Z:
    return c * a[0], c * a[1]

def iphase(a: Z, exponent: int) -> Z:
    exponent %= 4
    if exponent == 0:
        return a
    if exponent == 1:
        return -a[1], a[0]
    if exponent == 2:
        return -a[0], -a[1]
    return a[1], -a[0]

def parity(n: int) -> int:
    return n.bit_count() & 1

def split(addr: int, m: int, f: int) -> tuple[int, ...]:
    mask = (1 << f) - 1
    return tuple((addr >> (j * f)) & mask for j in range(m))

def join(xs: tuple[int, ...] | list[int], f: int) -> int:
    return sum(x << (j * f) for j, x in enumerate(xs))

def coset_word(x: int, s: int, f: int) -> int:
    if s == 0:
        return x
    t = (s & -s).bit_length() - 1
    shift = f - 1 - t
    epsilon = (x >> t) & 1
    u = x ^ (epsilon * s)
    result = epsilon << (f - 1)
    for old in range(f):
        if old != t:
            result |= ((u >> old) & 1) << ((old + shift) % f)
    return result

def uncoset_word(y: int, s: int, f: int) -> int:
    if s == 0:
        return y
    t = (s & -s).bit_length() - 1
    shift = f - 1 - t
    epsilon = (y >> (f - 1)) & 1
    u = 0
    for old in range(f):
        if old != t:
            u |= ((y >> ((old + shift) % f)) & 1) << old
    return u ^ (epsilon * s)

def coset_array(values: list[Z], s: int, m: int, f: int) -> list[Z]:
    out = [ZERO] * len(values)
    for old, val in enumerate(values):
        new = join(tuple(coset_word(x, s, f) for x in split(old, m, f)), f)
        out[new] = val
    return out

def uncoset_array(values: list[Z], s: int, m: int, f: int) -> list[Z]:
    out = [ZERO] * len(values)
    for new, val in enumerate(values):
        old = join(tuple(uncoset_word(y, s, f) for y in split(new, m, f)), f)
        out[old] = val
    return out

def hadamard(values: list[Z], pos: int) -> list[Z]:
    out = values.copy()
    bit = 1 << pos
    for addr in range(len(values)):
        if not addr & bit:
            out[addr] = add(values[addr], values[addr | bit])
            out[addr | bit] = sub(values[addr], values[addr | bit])
    return out

def diag_phase(values: list[Z], pos: int, exponent: int) -> list[Z]:
    return [iphase(val, exponent if (addr >> pos) & 1 else 0)
            for addr, val in enumerate(values)]

def direct(values: list[Z], s: int, xi: int, m: int, f: int,
           coeffs: tuple[int, ...], const: int) -> list[Z]:
    out = []
    for addr, val in enumerate(values):
        total = scale(val, const)
        xs = split(addr, m, f)
        for j, c in enumerate(coeffs):
            other = addr ^ (s << (j * f))
            sign = -1 if parity(xi & xs[j]) else 1
            total = add(total, scale(values[other], c * sign))
        out.append(total)
    return out

def batched(values: list[Z], s: int, xi: int, m: int, f: int,
            coeffs: tuple[int, ...], const: int,
            wrong_delta: bool = False, omit_coset: bool = False) -> tuple[list[Z], int]:
    if s == 0:
        out = []
        for addr, val in enumerate(values):
            xs = split(addr, m, f)
            c = const + sum(c * (-1 if parity(xi & xs[j]) else 1)
                            for j, c in enumerate(coeffs))
            out.append(scale(val, c))
        return out, 1
    delta = parity(xi & s)
    used_delta = 0 if wrong_delta else delta
    state = values.copy() if omit_coset else coset_array(values, s, m, f)
    # Unnormalized inverse G: H D^{-1}; true denominator is 2 per query.
    for j in range(m):
        pos = (j + 1) * f - 1
        state = diag_phase(state, pos, -used_delta)
        state = hadamard(state, pos)
    mixed = []
    for addr, val in enumerate(state):
        total = scale(val, const)
        for j, c in enumerate(coeffs):
            y = split(addr, m, f)[j]
            b = (y >> (f - 1)) & 1
            # Remove the spectral epsilon bit to recover the coset u.
            u = uncoset_word(y & ((1 << (f - 1)) - 1), s, f)
            sign = -1 if parity(xi & u) ^ b else 1
            total = add(total, scale(iphase(val, used_delta), c * sign))
        mixed.append(total)
    state = mixed
    # Forward G: D H.
    for j in range(m):
        pos = (j + 1) * f - 1
        state = hadamard(state, pos)
        state = diag_phase(state, pos, used_delta)
    if not omit_coset:
        state = uncoset_array(state, s, m, f)
    return state, 1 << m


def reused_sequence(values: list[Z], s: int, xi: int, m: int, f: int,
                    stages: tuple[tuple[tuple[int, ...], int], ...]) -> tuple[list[Z], int]:
    """Apply all stage diagonals between only one pair of common bases."""
    if s == 0:
        state = values.copy()
        for coeffs, const in stages:
            state = direct(state, s, xi, m, f, coeffs, const)
        return state, 1
    delta = parity(xi & s)
    state = coset_array(values, s, m, f)
    for j in range(m):
        pos = (j + 1) * f - 1
        state = diag_phase(state, pos, -delta)
        state = hadamard(state, pos)
    for coeffs, const in stages:
        mixed = []
        for addr, val in enumerate(state):
            total = scale(val, const)
            for j, c in enumerate(coeffs):
                y = split(addr, m, f)[j]
                b = (y >> (f - 1)) & 1
                u = uncoset_word(y & ((1 << (f - 1)) - 1), s, f)
                sign = -1 if parity(xi & u) ^ b else 1
                total = add(total, scale(iphase(val, delta), c * sign))
            mixed.append(total)
        state = mixed
    for j in range(m):
        pos = (j + 1) * f - 1
        state = hadamard(state, pos)
        state = diag_phase(state, pos, delta)
    return uncoset_array(state, s, m, f), 1 << m


def main() -> None:
    counts = {"one_word_bijections": 0, "full_layout_positions": 0,
              "local_conjugacy_cases": 0, "weighted_pencil_cases": 0,
              "weighted_pencil_entries": 0, "zero_parameter_cases": 0,
              "wrong_delta_rejections": 0, "omitted_coset_rejections": 0,
              "shared_basis_two_stage_cases": 0,
              "star_swap_noncommuting_cases": 0}
    for f in range(1, 5):
        q = 1 << f
        for s in range(q):
            images = [coset_word(x, s, f) for x in range(q)]
            assert sorted(images) == list(range(q))
            assert all(uncoset_word(images[x], s, f) == x for x in range(q))
            counts["one_word_bijections"] += 1
            if s:
                for xi in range(q):
                    delta = parity(xi & s)
                    for x in range(q):
                        y = coset_word(x, s, f)
                        yp = coset_word(x ^ s, s, f)
                        assert yp == y ^ (1 << (f-1))
                        eps = (y >> (f-1)) & 1
                        u = x ^ (eps * s)
                        assert parity(xi & x) == (parity(xi & u) ^ (delta * eps))
                        counts["local_conjugacy_cases"] += 1
    for f, m in [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]:
        q, n = 1 << f, 1 << (m*f)
        coeffs = tuple((-1 if j & 1 else 1) * (j + 1) for j in range(m))
        vals = [((37*x + 5) % 23 - 11, (19*x + 1) % 13 - 6) for x in range(n)]
        for s in range(q):
            layout = coset_array(vals, s, m, f)
            assert uncoset_array(layout, s, m, f) == vals
            counts["full_layout_positions"] += n
            for xi in range(q):
                wanted = direct(vals, s, xi, m, f, coeffs, 2)
                actual, denominator = batched(vals, s, xi, m, f, coeffs, 2)
                assert actual == [scale(v, denominator) for v in wanted], (m,f,s,xi)
                counts["weighted_pencil_cases"] += 1
                counts["weighted_pencil_entries"] += n
                if s == 0:
                    counts["zero_parameter_cases"] += 1
                elif parity(s & xi):
                    bad, den = batched(vals, s, xi, m, f, coeffs, 2, wrong_delta=True)
                    if bad != [scale(v, den) for v in wanted]:
                        counts["wrong_delta_rejections"] += 1
                if s and coset_array(vals, s, m, f) != vals:
                    bad, den = batched(vals, s, xi, m, f, coeffs, 2, omit_coset=True)
                    if bad != [scale(v, den) for v in wanted]:
                        counts["omitted_coset_rejections"] += 1
                # Composition uses exactly the same basis. Algebraically compare
                # two differing weighted pencils, including their full output.
                coeffs2 = tuple(j + 2 for j in range(m))
                after = direct(wanted, s, xi, m, f, coeffs2, -3)
                second, den2 = reused_sequence(vals, s, xi, m, f,
                                                ((coeffs, 2), (coeffs2, -3)))
                assert second == [scale(v, den2) for v in after]
                counts["shared_basis_two_stage_cases"] += 1
    # Actual swap families are not covered by a simultaneous Weyl diagonalizer.
    for q in (2, 4, 8):
        def swap(t, j):
            t = list(t); t[0], t[j] = t[j], t[0]; return tuple(t)
        witness = (0, 1, 0)
        assert swap(swap(witness, 1), 2) != swap(swap(witness, 2), 1)
        counts["star_swap_noncommuting_cases"] += 1
    assert counts["wrong_delta_rejections"] > 0
    assert counts["omitted_coset_rejections"] > 0
    output = {"status": "PASS_FINITE_WEYL_STAR_COMPONENTS", "counts": counts,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Exact finite bijections, conjugacy, signed Gaussian-integer pencils, composition and negative controls. Not source-middle-map classification, tape runtime, a global bound or formal verification."}
    Path("weyl-star-verification.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
