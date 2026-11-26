#!/usr/bin/env python3
"""Finite exact source geometry, SWAP expansion, and occupied-row bridge checks."""
from __future__ import annotations
from collections import defaultdict
from itertools import product
import hashlib
import json
from pathlib import Path


def parity(x: int) -> int:
    return x.bit_count() & 1


def swap_tuple(xs: tuple[int, ...], j: int) -> tuple[int, ...]:
    ys = list(xs)
    ys[0], ys[j] = ys[j], ys[0]
    return tuple(ys)


def main() -> None:
    counts = {"weyl_swap_columns": 0, "fourier_conjugated_blocks": 0,
              "fourier_block_columns": 0, "nonzero_cross_row_columns": 0,
              "wrong_inverse_phase_rejections": 0,
              "character_orthogonality_entries": 0,
              "gram_basis_pairings": 0, "gram_span_rows": 0,
              "relative_swap_noncommuting_cases": 0,
              "star_sum_kernel_cases": 0,
              "lift_involution_commutator_checks": 0,
              "full_two_half_composite_swap_checks": 0}
    for f in (1, 2, 3):
        Q = 1 << f
        for z, x in product(range(Q), repeat=2):
            column = defaultdict(int)
            wrong = defaultdict(int)
            for s, xi in product(range(Q), repeat=2):
                sign = -1 if parity(xi & (s ^ z ^ x)) else 1
                column[(z ^ s, x ^ s)] += sign
                wrong[(z ^ s, x ^ s)] += -1 if parity(xi & (z ^ x)) else 1
            column = {k: v for k, v in column.items() if v}
            assert column == {(x, z): Q}
            counts["weyl_swap_columns"] += 1
            if {k: v for k, v in wrong.items() if v} != {(x, z): Q}:
                counts["wrong_inverse_phase_rejections"] += 1
        for alpha, beta in product(range(Q), repeat=2):
            counts["fourier_conjugated_blocks"] += 1
            for z, x in product(range(Q), repeat=2):
                column = defaultdict(int)
                for s, xi in product(range(Q), repeat=2):
                    p = parity(alpha & s) ^ parity(beta & xi) ^ parity(xi & (s ^ z ^ x))
                    column[(z ^ s, x ^ s)] += -1 if p else 1
                column = {k: v for k, v in column.items() if v}
                sign = -1 if parity(alpha & (z ^ x ^ beta)) else 1
                assert column == {(x ^ beta, z ^ beta): Q * sign}
                counts["fourier_block_columns"] += 1
                if alpha or beta:
                    counts["nonzero_cross_row_columns"] += 1
        r = Q * Q
        for u, v in product(range(r), repeat=2):
            inner = sum(-1 if parity(p & (u ^ v)) else 1 for p in range(r))
            assert inner == (r if u == v else 0)
            counts["character_orthogonality_entries"] += 1
        v = {(1,1,0,0): 1, (1,0,1,0): -1,
             (0,0,1,1): 1, (0,1,0,1): -1}
        out = defaultdict(int)
        for addr, c in v.items():
            for j in (1, 2, 3):
                out[swap_tuple(addr, j)] += c
        assert all(c == 0 for c in out.values())
        counts["star_sum_kernel_cases"] += 1
        witness = (1,0,0,0)
        def relative(addr, j):
            return swap_tuple(swap_tuple(addr, 1), j)
        left = relative(relative(witness, 3), 2)
        right = relative(relative(witness, 2), 3)
        assert left == (0,0,1,0) and right == (0,0,0,1)
        counts["relative_swap_noncommuting_cases"] += 1
    # Exact physical two-half map: cross-swap X_j with Z_b and Z_j
    # with X_b. The auxiliary composite order is reversed once.
    for physical in product(range(2), repeat=8):
        def composite(t):
            return (t[4]+2*t[0],) + tuple(t[j]+2*t[4+j] for j in (1,2,3))
        for j in (1,2,3):
            out=list(physical)
            out[j],out[4]=out[4],out[j]
            out[4+j],out[0]=out[0],out[4+j]
            assert composite(out)==swap_tuple(composite(physical),j)
            counts["full_two_half_composite_swap_checks"] += 1
    # Actual q=4,L=2 quotient: represent vectors by their 16 Gram-row bits.
    labels = list(product(range(4), repeat=2))
    def gamma(v, w):
        return (1 + sum(a != b for a,b in zip(v,w))) % 2
    rows = [sum(gamma(v,w) << j for j,w in enumerate(labels)) for v in labels]
    def idx(v): return labels.index(v)
    es = [1 << idx((a,0)) for a in range(4)]
    p = (1 << idx((0,1))) ^ es[1] ^ es[2] ^ es[3]
    q = (1 << idx((0,2))) ^ es[1] ^ es[2] ^ es[3]
    basis = es + [p,q]
    def row_of(v):
        ans = 0
        for i,r in enumerate(rows):
            if (v >> i) & 1: ans ^= r
        return ans
    def pair(v,w): return parity(row_of(v) & w)
    for i,v in enumerate(basis):
        for j,w in enumerate(basis):
            wanted = int((i == j and i < 4) or (i,j) in ((4,5),(5,4)))
            assert pair(v,w) == wanted
            counts["gram_basis_pairings"] += 1
    basis_rows = [row_of(v) for v in basis]
    span = set()
    for mask in range(64):
        v = 0
        for i,b in enumerate(basis_rows):
            if (mask >> i) & 1: v ^= b
        span.add(v)
    assert len(span) == 64
    assert all(r in span for r in rows)
    counts["gram_span_rows"] = len(rows)
    assert all(gamma(v,w) == 0 for v in ((0,0),(1,0)) for w in ((2,0),(3,0)))
    # For f=1, verify every signed lifted A_(p,j) squares to I and all
    # pairwise products commute on every basis vector. Odd sum invertibility
    # then follows from exact simultaneous diagonalization of involutions.
    for s,xi in product(range(2), repeat=2):
        def act(addr,j):
            x=list(addr)
            sign=-1 if (xi & (s ^ x[0] ^ x[j])) else 1
            x[0]^=s; x[j]^=s
            return tuple(x),sign
        for addr in product(range(2), repeat=4):
            for j in (1,2,3):
                b,c=act(addr,j); d,e=act(b,j)
                assert d==addr and c*e==1
                counts["lift_involution_commutator_checks"] += 1
            for j,k in ((1,2),(1,3),(2,3)):
                b,c=act(addr,j); d,e=act(b,k)
                bb,cc=act(addr,k); dd,ee=act(bb,j)
                assert d==dd and c*e==cc*ee
                counts["lift_involution_commutator_checks"] += 1
    out={"status":"PASS_FINITE_SWAP_WEYL_BRIDGE", "counts":counts,
         "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         "scope":"Exact finite Weyl/SWAP identities, complete cross-row blocks, rank-falsifier components and actual small source Gram geometry. Not a physical lower bound, asymptotic multiplier run, or formal proof."}
    Path('swap-weyl-bridge-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
