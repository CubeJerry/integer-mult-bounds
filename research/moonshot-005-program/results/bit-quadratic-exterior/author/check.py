#!/usr/bin/env python3
"""Exact finite premises for the native Schur-square/exterior theorem.

The universal tensor argument and its characteristic-two extension are in
PROOF.md.  This script does not search for an asymptotic algorithm.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

NATIVE = "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
DEPS = ["results/bit-operator-canonical-quotient/author/PROOF.md", "results/bit-monotone-arrival-gate/PROOF.md"]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def basis(rows):
    pivots = {}
    for original in rows:
        row = original
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return list(pivots.values())


def members(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def shortening(rows, allowed):
    """A binary basis of row(rows) supported in allowed."""
    pivots = {}
    out = []
    for original in rows:
        full = original
        restricted = original & ~allowed
        while restricted:
            p = restricted.bit_length() - 1
            if p in pivots:
                a, b = pivots[p]
                restricted ^= a
                full ^= b
            else:
                pivots[p] = (restricted, full)
                break
        if not restricted:
            out.append(full)
    return basis(out)


def binary_solve(rows, target, size):
    augmented = [r | ((b & 1) << size) for r, b in zip(rows, target)]
    at = 0
    for col in range(size):
        found = next((j for j in range(at, len(rows)) if augmented[j] >> col & 1), None)
        if found is None:
            continue
        augmented[at], augmented[found] = augmented[found], augmented[at]
        for j in range(len(rows)):
            if j != at and augmented[j] >> col & 1:
                augmented[j] ^= augmented[at]
        at += 1
    need(at == size, "invertible system")
    return sum((augmented[i] >> size & 1) << i for i in range(size))


def mod_rank(rows, prime):
    a = [[int(x) % prime for x in r] for r in rows]
    ncols = len(a[0]) if a else 0
    at = 0
    for col in range(ncols):
        found = next((j for j in range(at, len(a)) if a[j][col]), None)
        if found is None:
            continue
        a[at], a[found] = a[found], a[at]
        inv = pow(a[at][col], -1, prime)
        a[at] = [inv*x % prime for x in a[at]]
        for j in range(at + 1, len(a)):
            c = a[j][col]
            if c:
                a[j] = [(x-c*y) % prime for x, y in zip(a[j], a[at])]
        at += 1
        if at == ncols:
            break
    return at


def load_native(repo):
    raw = (repo / NATIVE).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, "native source pin")
    native = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        root = list(map(Fraction, native["frames"][str(native["start"][i])]["B"][0]))
        norm = sum(x*x for x in root)
        scale = (2 if norm == 1 else 1)*(1 if next(x for x in root if x) > 0 else -1)
        root = [scale*x for x in root]
        need(all(x.denominator == 1 for x in root) and sum(x*x for x in root) == 4, "integer root normalization")
        roots.append(tuple(map(int, root)))
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    K = [sum(int(i == j or dot(r, s) == 0) << j for j, s in enumerate(roots)) for i, r in enumerate(roots)]
    return roots, K


def finite_geometry(roots, K):
    all_points = (1 << 111)-1
    B = [r ^ all_points for r in K]
    need(len(basis(B)) == 8, "symplectic binary rank eight")
    frame = []
    for i, row in enumerate(B):
        if len(basis([B[j] for j in frame] + [row])) > len(frame):
            frame.append(i)
    need(frame == [0, 1, 2, 4, 8, 14, 30, 59], "deterministic binary coordinate frame")
    gram = [sum(((B[i] >> j) & 1) << c for c, j in enumerate(frame)) for i in frame]
    need(len(basis(gram)) == 8, "nondegenerate principal Gram")
    coordinates = [binary_solve(gram, [(B[i] >> j) & 1 for i in frame], 8) for j in range(111)]
    need(len(set(coordinates)) == 111, "distinct binary points")
    bilinear = lambda x, y: sum(((x >> i) & 1)*(gram[i] & y).bit_count() for i in range(8)) & 1
    pairs = list(itertools.combinations(range(8), 2))
    def quadratic(x):
        return (x.bit_count() + sum(((gram[i] >> j) & 1)*((x >> i) & 1)*((x >> j) & 1) for i, j in pairs)) & 1
    need(all(quadratic(x) == 1 for x in coordinates), "anisotropic native points")
    need(all(bilinear(coordinates[i], coordinates[j]) == ((B[i] >> j) & 1) for i in range(111) for j in range(111)), "all polar pairings")
    anisotropic = {x for x in range(256) if quadratic(x)}
    need(len(anisotropic) == 120, "plus type anisotropic count")
    affine = [all_points] + [sum(((x >> c) & 1) << j for j, x in enumerate(coordinates)) for c in range(8)]
    monomials = affine + [sum((((x >> a) & 1)*((x >> b) & 1)) << j for j, x in enumerate(coordinates)) for a, b in pairs]
    C = basis(K)
    Q = basis(C + [a & b for a, b in itertools.combinations(C, 2)])
    need(len(C) == 9 and len(basis(C + affine)) == 9, "canonical affine code")
    need(len(Q) == 36 and len(basis(Q + monomials)) == 36, "quadratic evaluation rank")
    relation = affine[0]
    for row in affine[1:]:
        relation ^= row
    for p, (a, b) in enumerate(pairs):
        if gram[a] >> b & 1:
            relation ^= monomials[9+p]
    need(relation == 0, "unique degree-two relation q+1")
    need(len(basis(gram)) > 4, "exterior quotient rank margin")
    local = [shortening(Q, row) for row in K]
    need(all(len(L) == 8 for L in local), "all local Schur spaces dimension eight")
    need(all(len(shortening(C, row)) == 1 for row in K), "canonical local rigidity")
    need(all(len(basis([row & c for c in C])) == 8 and len(basis(L + [row & c for c in C])) == 8 for row, L in zip(K, local)), "local Ki times affine identification")
    need(all(len(basis(C+L)) == 16 for L in local), "all local quotient dimensions seven")
    pair_intersections = Counter()
    support_histogram = Counter()
    for i, j in itertools.combinations(range(111), 2):
        qij = K[i] & K[j]
        need(len(basis(C+[qij])) == 10, "pair representative noncanonical")
        need(not(qij & ~K[i]) and not(qij & ~K[j]), "pair representative literal locality")
        common = 14-(len(basis(C+local[i]+local[j]))-9)
        pair_intersections[common] += 1
        need(common == 1, "all pair intersections exactly one")
        acquired = qij & ~((1 << i) | (1 << j))
        supp = list(members(acquired))
        # Orthogonality to two independent roots gives real rank <=6;
        # a nonzero mod101 6-minor gives the opposite inequality.
        need(all(sum(x*y for x, y in zip(roots[t], roots[i])) == 0 and sum(x*y for x, y in zip(roots[t], roots[j])) == 0 for t in supp), "common real flat support")
        need(mod_rank([roots[i], roots[j]], 101) == 2 and mod_rank([roots[t] for t in supp], 101) == 6, "exact real common support rank six")
        support_histogram[(bool(K[i] >> j & 1), len(supp), 6)] += 1
    i, j = 0, 1
    need(K[i] >> j & 1, "orthogonal positive-control pair")
    qij = K[i] & K[j]
    fitting = list(K)
    fitting[i] = fitting[j] = qij
    need(all(row >> a & 1 and not(row & ~K[a]) for a, row in enumerate(fitting)), "native scalar fitting positive control")
    need(len(basis(C+fitting))-9 == 1, "positive-control quotient one")
    need(all(K[a] & ~fitting[a] for a in (i, j)), "two contact-deleting rows")
    need(all(mod_rank([roots[t] for t in members(qij & ~(1 << a))], 101) == 7 for a in (i, j)), "positive-control foreign rank seven")
    return {"source_path": NATIVE, "source_sha256": PIN,
            "binary_frame_indices": frame, "binary_gram_rows": gram,
            "binary_native_points": coordinates,
            "missing_anisotropic_points": sorted(anisotropic-set(coordinates)),
            "anisotropic_count": len(anisotropic),
            "canonical_dimension": len(C), "quadratic_dimension": len(Q),
            "quadratic_quotient_dimension": len(Q)-len(C),
            "local_literal_dimensions": dict(Counter(map(len, local))),
            "pair_quotient_intersections": dict(pair_intersections),
            "common_flat_support_histogram": [{"orthogonal": key[0], "size": key[1], "real_rank": key[2], "pairs": value} for key, value in sorted(support_histogram.items())],
            "pure_tensor_positive_control": {"changed_rows": [i, j], "scalar_quotient_dimension": 1, "block_quotient_dimension": "V", "deleted_rows": 2, "proper_cover_charge": 220}}


def low_rank_negative_control():
    # Wedge coordinates12,13,14,23,24,34 in dimension four.
    omega = (1 << 0) | (1 << 5)
    L1 = [1 << j for j in (0, 1, 2)]
    L3 = [1 << j for j in (1, 3, 5)]
    intersection = 3+3-(len(basis([omega]+L1+L3))-1)
    need(intersection == 2, "rank-four form has two-dimensional local intersection")
    p, q, r, s = 1 << 1, 1 << 0, 1 << 2, 1 << 3
    need(len(basis([omega, p, q, r, s])) == 5, "four independent chain scalars modulo omega")
    need(len(basis([omega]+L1+[p, q, r])) == 4, "first local chain plane")
    need(len(basis([omega]+L3+[p, q, s])) == 4, "second local chain plane")
    return {"ambient_dimension": 4, "polar_rank": 4,
            "pair_intersection_dimension": intersection,
            "omega_wedge_mask": omega,
            "pure_chain": [[r, p], [p, q], [q, s]],
            "scope": "Abstract local geometry; not a native fitting or physical source."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    roots, K = load_native(args.repo)
    result = {"status": "PASS_AUTHOR_QUADRATIC_EXTERIOR_CONTROLS",
              "claim": "In the native quadratic reservoir, a completely entangled canonical quotient of dimension d<2V allows at most one contact-deleting row; chi>=220.",
              "proof_status": "Universal proof in PROOF.md; independent review pending",
              "source": finite_geometry(roots, K),
              "rank_four_negative_control": low_rank_negative_control(),
              "dependencies": [{"path": "research/moonshot-005-program/"+p, "sha256": hashlib.sha256((args.repo/"research/moonshot-005-program"/p).read_bytes()).hexdigest()} for p in DEPS],
              "new_complete_kappa": False, "physical_source_constructed": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "output": str(args.output), "quadratic_dimension": 36, "local_quotient_dimension": 7, "pair_intersections_checked": 6105, "new_complete_kappa": False}))


if __name__ == "__main__":
    main()
