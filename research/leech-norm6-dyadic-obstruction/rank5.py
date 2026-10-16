"""Exact F5 row rank using three Python-integer bit planes.

A column's three bits encode its residue 0..4. plus() forms the binary
sum (0..8), detects sums >=5, and subtracts 5. There are no floating-point
operations, packed-lane carries or external libraries. Proof and scalar
truth-table controls are in PROOF.md / test_verify.py. Apache-2.0.
"""
from __future__ import annotations
from typing import Iterable, Sequence

Planes = tuple[int, int, int]


def plus(a: Planes, b: Planes) -> Planes:
    a0, a1, a2 = a
    b0, b1, b2 = b
    s0, c0 = a0 ^ b0, a0 & b0
    u = a1 ^ b1
    s1, c1 = u ^ c0, (a1 & b1) | (u & c0)
    v = a2 ^ b2
    s2, c2 = v ^ c1, (a2 & b2) | (v & c1)
    reduce = c2 | (s2 & (s1 | s0))
    return s0 ^ reduce, s1 ^ (reduce & ~s0), s2 & ~reduce


def neg(a: Planes) -> Planes:
    a0, a1, a2 = a
    return a2 | (a1 & ~a0), a1, a0 & ~a1


def mul(a: Planes, k: int) -> Planes:
    if type(k) is not int or not 0 <= k < 5:
        raise ValueError("F5 scalar")
    if k == 0:
        return (0, 0, 0)
    if k == 1:
        return a
    if k == 2:
        return plus(a, a)
    if k == 3:
        return neg(plus(a, a))
    return neg(a)


def pack(row: Sequence[int]) -> Planes:
    out = [0, 0, 0]
    for i, v in enumerate(row):
        if type(v) is not int or not 0 <= v < 5:
            raise ValueError("F5 row entry")
        for b in range(3):
            if v >> b & 1:
                out[b] |= 1 << i
    return tuple(out)  # type: ignore[return-value]


def rank(rows: Iterable[Sequence[int]]) -> tuple[int, list[int]]:
    """Return row rank and the indices of a greedily selected row basis."""
    basis: dict[int, list[Planes]] = {}
    selected: list[int] = []
    width = None
    for i, row in enumerate(rows):
        if width is None:
            width = len(row)
        if len(row) != width:
            raise ValueError("ragged matrix")
        a = pack(row)
        while any(a):
            c = (a[0] | a[1] | a[2]).bit_length() - 1
            v = ((a[0] >> c) & 1) + 2 * ((a[1] >> c) & 1) + 4 * ((a[2] >> c) & 1)
            if c not in basis:
                a = mul(a, pow(v, -1, 5))
                basis[c] = [mul(a, k) for k in range(5)]
                selected.append(i)
                break
            a = plus(a, basis[c][5 - v])
    return len(basis), selected
