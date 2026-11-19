"""Exact finite-field helpers from S028 Worker B review.
Used by the coefficient selector; this reuse is not an independent review
of the selected coefficients. @CubeJerry, OpenAI assistance, Apache-2.0.
"""

from __future__ import annotations

from fractions import Fraction

import gzip

import json

from pathlib import Path

import numpy as np

PROGRAMME = Path("research/moonshot-005-program")

def require(value, message):
    if not value:
        raise ValueError(message)

def unpack(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)

def pmod(value, modulus):
    while value and value.bit_length() >= modulus.bit_length():
        value ^= modulus << (value.bit_length() - modulus.bit_length())
    return value

def product(x, y, modulus):
    value = 0
    while y:
        if y & 1:
            value ^= x
        x <<= 1
        y >>= 1
    return pmod(value, modulus)

def field(modulus):
    size = 1 << (modulus.bit_length() - 1)
    dtype = np.uint8 if size <= 256 else np.uint16
    table = np.array([[product(x, y, modulus) for y in range(size)]
                      for x in range(size)], dtype=dtype)
    inverses = np.zeros(size, dtype=dtype)
    for x in range(1, size):
        candidates = np.flatnonzero(table[x] == 1)
        require(len(candidates) == 1, "field multiplication inverse")
        inverses[x] = candidates[0]
    return table, inverses

def rank(M, table, inverses):
    """Forward finite-field elimination, independent of author's bit ranks."""
    M = np.array(M, dtype=table.dtype, copy=True)
    rows, cols = M.shape
    pivot = 0
    for col in range(cols):
        candidates = np.flatnonzero(M[pivot:, col])
        if not len(candidates):
            continue
        pos = pivot + int(candidates[0])
        M[[pivot, pos]] = M[[pos, pivot]]
        M[pivot, col:] = table[inverses[M[pivot, col]], M[pivot, col:]]
        if pivot + 1 < rows:
            factors = M[pivot + 1:, col].copy()
            M[pivot + 1:, col:] ^= table[factors[:, None], M[pivot, col:][None, :]]
        pivot += 1
        if pivot == rows:
            break
    return pivot

def rational_inverse(M):
    n = len(M)
    A = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(M)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if A[i][col])
        A[col], A[pivot] = A[pivot], A[col]
        d = A[col][col]
        A[col] = [x / d for x in A[col]]
        for i in range(n):
            if i != col:
                d = A[i][col]
                A[i] = [x - d * y for x, y in zip(A[i], A[col])]
    return [row[n:] for row in A]

def quadratic(x):
    return sum(((x >> (2*k)) & 1) * ((x >> (2*k+1)) & 1) for k in range(4)) % 2

def polar(x, y):
    return quadratic(x ^ y) ^ quadratic(x) ^ quadratic(y)

def binary_product(A, B):
    return (A.astype(np.int16) @ B.astype(np.int16) % 2).astype(np.uint8)

def geometry(layout, basis):
    columns = basis["lattice_basis_columns"]
    inverse = rational_inverse([[columns[c][r] for c in range(8)] for r in range(8)])
    coordinates = {}
    for mask in range(256):
        original = 0
        for k, column in enumerate(basis["hyperbolic_basis_masks"]):
            if mask & (1 << k):
                original ^= column
        require(original not in coordinates, "hyperbolic basis independent")
        coordinates[original] = mask
    roots = layout["root_table"]
    masks = []
    for root in roots:
        c = [sum(a*b for a, b in zip(row, root)) for row in inverse]
        require(all(x.denominator == 1 for x in c), "integral native lattice coordinates")
        masks.append(coordinates[sum((int(x) & 1) << i for i, x in enumerate(c))])
    require(len(set(masks)) == 120 and set(masks) == {x for x in range(256) if quadratic(x)},
            "complete nonsingular quadratic root set")
    primitives = []
    for k in range(4):
        C = np.zeros((16, 16), dtype=np.uint8)
        D = C.copy()
        for s in range(16):
            if s & (1 << k):
                D[s ^ (1 << k), s] = 1
            else:
                C[s | (1 << k), s] = 1
        primitives.extend([C, D])
    gamma = []
    for mask in masks:
        G = np.zeros((16, 16), dtype=np.uint8)
        for k in range(8):
            if mask & (1 << k):
                G ^= primitives[k]
        require(np.array_equal(binary_product(G, G), np.eye(16, dtype=np.uint8)),
                "all root gamma squares")
        gamma.append(G)
    adjacency = []
    for i, x in enumerate(roots):
        A = {j for j, y in enumerate(roots) if i != j and sum(a*b for a, b in zip(x, y)) == 0}
        require(A == {j for j in range(120) if i != j and not polar(masks[i], masks[j])},
                "real orthogonality matches quadratic polar form")
        adjacency.append(A)
    return masks, gamma, adjacency

def combine(L, F, table):
    L = np.array(L, dtype=table.dtype)
    out = np.zeros((len(L), F.shape[1]), dtype=table.dtype)
    for k in range(F.shape[0]):
        out ^= table[L[:, k, None], F[k, None, :]]
    return out
