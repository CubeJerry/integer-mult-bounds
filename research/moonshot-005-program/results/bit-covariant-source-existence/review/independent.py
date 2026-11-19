#!/usr/bin/env python3
"""Independent review of S027 full-covariant source certificates.

No code from the author package is imported.  Geometry is reconstructed in
quadratic coordinates, the orbit is generated afresh, and witness ranks are
computed by Gaussian elimination in GF(16), not binary expansion.
@CubeJerry, S028 Worker B, substantial OpenAI assistance. Apache-2.0.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import gzip
import json
from pathlib import Path
import sys
import time

import numpy as np

PROGRAMME = Path("research/moonshot-005-program")
SOURCE = PROGRAMME / "work-in-progress/2026-11-19-S027/covariant-trace-source"


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


def linear_binary(A, vector):
    return np.bitwise_xor.reduce(np.where(A, vector[None, :], 0), axis=1)


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


def direct_trace_source(gamma, plane, donor, vectors):
    """Evaluate [j,[k,C X]]v directly, without author basis re-expansion."""
    other = min(set(plane) - {donor})
    j, k = gamma[donor], gamma[other]
    jk, kj = binary_product(j, k), binary_product(k, j)
    basis = [np.eye(16, dtype=np.uint8), j, k, jk]
    answer = np.zeros((16, 16, 16), dtype=np.uint16)
    for C, raw in zip(basis, vectors):
        v = np.array(raw, dtype=np.uint16)
        terms = [(binary_product(jk, C), v),
                 (binary_product(j, C), linear_binary(k, v)),
                 (binary_product(k, C), linear_binary(j, v)),
                 (C, linear_binary(kj, v))]
        for A, u in terms:
            answer ^= A[:, :, None] * u[None, None, :]
    return answer.reshape(16, 256)


def combine(L, F, table):
    L = np.array(L, dtype=table.dtype)
    out = np.zeros((len(L), F.shape[1]), dtype=table.dtype)
    for k in range(F.shape[0]):
        out ^= table[L[:, k, None], F[k, None, :]]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    source = args.source or args.repo / SOURCE
    resultroot = args.repo / PROGRAMME / "results"
    layoutpath = resultroot / "bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz"
    basispath = resultroot / "bit-clifford-one-evaluation-gate/author/BASIS.json"
    routespath = resultroot / "bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz"
    layout = unpack(layoutpath)
    masks, gamma, adjacency = geometry(layout, unpack(basispath))
    rootindex = {mask: i for i, mask in enumerate(masks)}
    planes = [set(x) for x in layout["A2"]]
    complete = {frozenset([i, j, rootindex[masks[i] ^ masks[j]]])
                for i in range(120) for j in range(i) if polar(masks[i], masks[j])}
    require(set(map(frozenset, planes)) == complete and len(complete) == 1120,
            "complete anisotropic planes")
    permutations = [[rootindex[v ^ (u if polar(u, v) else 0)] for v in masks] for u in masks]
    for ui, perm in enumerate(permutations):
        for i, dest in enumerate(perm):
            require(np.array_equal(binary_product(binary_product(gamma[ui], gamma[i]), gamma[ui]), gamma[dest]),
                    "quadratic transvection is actual Clifford conjugation")
    origin = (5, 77)
    reached = {origin}
    queue = deque([origin])
    while queue:
        i, j = queue.popleft()
        for p in permutations:
            pair = (p[i], p[j])
            if pair not in reached:
                reached.add(pair)
                queue.append(pair)
    expected = {(i, j) for i in range(120) for j in adjacency[i]}
    require(reached == expected and len(reached) == 7560, "independently generated full pair orbit")
    tree = unpack(source / "output/ORBIT.json.gz")
    edges = {(i, j): ((a, b), u) for i, j, a, b, u in tree["edges"]}
    require(len(edges) == 7559 and set(edges) | {origin} == reached, "author tree exact node coverage")
    for child, (parent, u) in edges.items():
        require(tuple(permutations[u][x] for x in parent) == child, "author orbit edge")
    table, inverses = field(19)
    require(rank(np.array([[1, 1], [1, 1]]), table, inverses) == 1, "rank negative control")
    identity = np.eye(16, dtype=np.uint8)
    for H in planes:
        j, k = sorted(H)[:2]
        N, M = gamma[j] ^ identity, gamma[k] ^ identity
        C = [binary_product(N, M), N, M, binary_product(M, N)]
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        want = C[2*a+d] if b == c else np.zeros((16, 16), dtype=np.uint8)
                        require(np.array_equal(binary_product(C[2*a+b], C[2*c+d]), want), "local matrix unit identity")
        require([rank(x, table, inverses) for x in C] == [8]*4, "rank-eight coefficient units")
    pair = unpack(source / "output/PAIR-WITNESS.json")
    visible = [h for h, H in enumerate(planes) if 77 in H and H <= adjacency[5]]
    require(pair["pair"] == [5, 77] and pair["planes"] == visible and len(visible) == 16,
            "actual sixteen visible witness planes")
    F = np.vstack([direct_trace_source(gamma, planes[h], 77, v)
                   for h, v in zip(visible, pair["vectors"])])
    require(F.shape == (256, 256) and rank(F, table, inverses) == 256, "foreign GF16 determinant")
    missing = F.copy(); missing[:16] = 0
    require(rank(missing, table, inverses) == 240, "omitted quotient control")
    routebytes = gzip.decompress(routespath.read_bytes())
    counts = Counter()
    for line in routebytes.splitlines():
        route = json.loads(line)
        if route[0] == "X":
            counts[route[1], route[3]] += 1
    require(Counter(counts.values()) == {15:2675, 30:422, 45:11}, "actual route quota census")
    quota = {key: value*8//15 for key, value in counts.items()}
    require(sum(counts.values()) == 111*480, "all original early owners")
    early = unpack(source / "output/EARLY-WITNESSES.json.gz")
    require([x["donor"] for x in early] == list(range(111)), "complete early donor evidence")
    ranks = []
    negatives = []
    extra_count = 0
    for cert in early:
        j = cert["donor"]
        expectedflags = sorted(h for donor, h in quota if donor == j)
        require([x["plane"] for x in cert["flags"]] == expectedflags, "all genuine early flags")
        matrices = []
        for flag in cert["flags"]:
            h = flag["plane"]; q = quota[j, h]
            L, extra = flag["early_output_rows"], flag["extra_rows"]
            require(len(L) == min(q, 16) and all(len(row) == 16 for row in L), "early frame dimensions")
            require(len(extra) == max(q-16, 0) and all(len(row) == 256 for row in extra), "extra original owner dimensions")
            require(all(0 <= x < 16 for row in L + extra + flag["vectors"] for x in row), "witness alphabet")
            quotient = direct_trace_source(gamma, planes[h], j, flag["vectors"])
            matrices.append(combine(L, quotient, table))
            if extra:
                matrices.append(np.array(extra, dtype=np.uint8))
                extra_count += len(extra)
        M = np.vstack(matrices)
        require(M.shape == (256, 256), "one entire early donor matrix")
        r = rank(M, table, inverses)
        require(r == 256, "early GF16 determinant")
        ranks.append(r)
        if j in (0, 5, 77, 110):
            q = quota[j, expectedflags[0]]
            bad = M.copy(); bad[:q] = 0
            rb = rank(bad, table, inverses)
            require(rb == 256-q, "actual removed early group control")
            negatives.append({"donor":j, "deleted_rows":q, "remaining_rank":rb})
    require(extra_count == 88, "singleton additional early rows")
    j, k = sorted(planes[263])[:2]
    require(j == 0, "fixed noncommutative incidence")
    N, M = gamma[j] ^ identity, gamma[k] ^ identity
    require(np.array_equal(binary_product(N, M) ^ binary_product(M, N), identity), "coefficient commutator witness")
    fanout = max(sum(H <= adjacency[i] for i in range(111)) for H in planes)
    require(fanout == 36, "true source variable foreign-view fanout")
    # Independent irreducibility check: trial divide by every monic polynomial
    # of degrees1..4. A reducible degree-nine polynomial has such a factor.
    p = 529
    trial_divisors = [d for degree in range(1,5) for d in range(1<<degree, 1<<(degree+1))]
    require(all(pmod(p, d) for d in trial_divisors), "GF512 irreducible by exhaustive small-factor exclusion")
    R = 15
    binary_width = 9*256*R
    late_caches = 9*2675*8*R
    invoice = 2*111*(binary_width**2 + 3*binary_width) + late_caches*(binary_width+1)
    require(invoice == 365025125160 and late_caches == 2889000, "independent source invoice")
    inputs = [layoutpath, basispath, routespath, source/"PROOF.md", source/"algebra.py", source/"check.py",
              source/"search.py", source/"output/PAIR-WITNESS.json", source/"output/ORBIT.json.gz",
              source/"output/EARLY-WITNESSES.json.gz"]
    pins = []
    for path in inputs:
        data = path.read_bytes()
        pins.append({"path":str(path.relative_to(args.repo)) if path.is_relative_to(args.repo) else str(path),
                     "sha256":sha256(data).hexdigest(),
                     **({"decompressed_sha256":sha256(gzip.decompress(data)).hexdigest()} if path.suffix == ".gz" else {})})
    result = {"status":"PASS_INDEPENDENT_FULL_COVARIANT_SOURCE_REVIEW",
              "scope":"finite determinants plus reviewed source-existence proof; no H/D/K completion or new kappa",
              "independent_algorithms":["quadratic-coordinate transvection BFS", "direct nested-commutator tensor", "GF16 Gaussian elimination", "degree-nine trial-factor exclusion"],
              "full_orthogonal_pair_orbit":len(reached), "native_foreign_pairs":sum(len(A & set(range(111))) for A in adjacency[:111]),
              "foreign_witness_GF16_rank":256, "early_GF16_rank_histogram":dict(Counter(ranks)),
              "actual_early_quota_histogram":dict(Counter(quota.values())), "extra_early_rows":extra_count,
              "coefficient_rank":8, "full_covariant_parameter_dimension":64,
              "source_variable_degree_bound":8*(fanout+1)+2, "field_size":512, "field_polynomial":p,
              "source_invoice":{"field_bank":3840, "field_bits":9, "ADD_upper_bound":invoice,
                                "INIT":late_caches, "dirty_CLEAR":late_caches, "extra_peak":late_caches, "extra_MOVE":0},
              "negative_controls":{"rank_duplicate_rows":1,"missing_foreign_quotient_rank":240,"missing_early_groups":negatives},
              "source_pins":pins,"global_coefficients_emitted":False,"new_complete_kappa":False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"REVIEW-RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(result["status"], "seconds", round(time.monotonic()-start, 2), flush=True)


if __name__ == "__main__":
    main()
