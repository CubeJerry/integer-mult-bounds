#!/usr/bin/env python3
"""Exact source premises and finite algebra controls for PROOF.md.

This does not enumerate native fittings or replace the universal proof.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
NATIVE = "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
DEPS = [
    "results/bit-three-direction-width-two/author/PROOF.md",
    "results/bit-one-extra-coset/author/PROOF.md",
    "results/bit-monotone-arrival-gate/PROOF.md",
    "results/bit-operator-canonical-quotient/author/PROOF.md",
    "results/bit-scalar-proper-cover-fourteen/author/PROOF.md",
    "results/bit-scalar-proper-cover-equality/author/PROOF.md",
    "results/bit-quotient-direction-savings/author/PROOF.md",
    "results/bit-full-halfclass-width-two-gate/author/PROOF.md",
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def bitbasis(rows):
    pivots = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return list(pivots.values())


def members(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


class Field:
    def __init__(self, order):
        need(order in (2, 4), "supported finite control field")
        self.q = order

    def mul(self, a, b):
        if self.q == 2:
            return a & b
        answer = 0
        while b:
            if b & 1:
                answer ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7
        return answer

    def inv(self, a):
        need(a != 0, "nonzero inverse")
        return next(b for b in range(1, self.q) if self.mul(a, b) == 1)

    def dot(self, a, b):
        out = 0
        for x, y in zip(a, b):
            out ^= self.mul(x, y)
        return out

    def solve(self, matrix, target=None):
        """Return rank, one solution (None if inconsistent), and null basis."""
        nr = len(matrix)
        nc = len(matrix[0]) if nr else 0
        a = [list(row) + ([target[i]] if target is not None else []) for i, row in enumerate(matrix)]
        pivots = []
        at = 0
        for col in range(nc):
            row = next((j for j in range(at, nr) if a[j][col]), None)
            if row is None:
                continue
            a[at], a[row] = a[row], a[at]
            inv = self.inv(a[at][col])
            a[at] = [self.mul(inv, x) for x in a[at]]
            for j in range(nr):
                if j != at and a[j][col]:
                    scale = a[j][col]
                    a[j] = [x ^ self.mul(scale, y) for x, y in zip(a[j], a[at])]
            pivots.append(col)
            at += 1
            if at == nr:
                break
        null = []
        for free in range(nc):
            if free not in pivots:
                vector = [0] * nc
                vector[free] = 1
                for i, pivot in enumerate(pivots):
                    vector[pivot] = a[i][free]
                null.append(vector)
        solution = None
        if target is not None and not any(not any(row[:nc]) and row[nc] for row in a):
            solution = [0] * nc
            for i, pivot in enumerate(pivots):
                solution[pivot] = a[i][nc]
        return len(pivots), solution, null


# Each row gives the scalar-index entries of one quotient generator's
# first/second value components. A None entry is zero.
SHAPES = {
    "C1_R2_repeated": ((0, 1), (2, None), (3, None)),
    "C1_R2_Jordan": ((0, 1), (2, None), (3, 2)),
    "C1_R1_R1_distinct": ((0, 1), (2, None), (None, 3)),
    "C2_R1": ((0, 1), (1, 2), (3, None)),
    "C1_C1_R1": ((0, 1), (2, 3), (4, None)),
    "C3": ((0, 1), (1, 2), (2, 3)),
    "C2_C1": ((0, 1), (1, 2), (3, 4)),
    "C1_C1_C1": ((0, 1), (2, 3), (4, 5)),
}
DOMINATORS = {
    "C1_R2_repeated": ((1,),),
    "C1_R2_Jordan": ((2,), (1, 2)),
    "C1_R1_R1_distinct": ((2,), (3,)),
    "C2_R1": ((3,), (1, 2)),
    "C1_C1_R1": ((4,), (1, 3)),
}


def coefficient_map(field, U, shape):
    size = 1 + max(x for pair in shape for x in pair if x is not None)
    phi = [[0] * size for _ in range(4)]
    for generator, pair in enumerate(shape):
        for value_coordinate, scalar_coordinate in enumerate(pair):
            if scalar_coordinate is not None:
                for output in range(2):
                    phi[2 * output + value_coordinate][scalar_coordinate] ^= U[output][generator]
    return phi


def dominates(solution, null, coordinates):
    # A singleton is the fixed h_j code. A pair is h_p+t h_q for a new
    # transcendental; both coordinate functionals must kill the kernel.
    return all(all(v[j] == 0 for j in coordinates) for v in null) and any(solution[j] for j in coordinates)


def algebra_controls(order):
    f = Field(order)
    data = {}
    bad_one_code = None
    for name, codes in DOMINATORS.items():
        histogram = Counter()
        coverage = Counter()
        count = 0
        rank_two = 0
        for flat in itertools.product(range(order), repeat=6):
            U = [list(flat[:3]), list(flat[3:])]
            if f.solve(U)[0] != 2:
                continue
            rank_two += 1
            phi = coefficient_map(f, U, SHAPES[name])
            rank, solution, null = f.solve(phi, [1, 0, 0, 1])
            if solution is None:
                continue
            count += 1
            histogram[len(null)] += 1
            good = [j for j, code in enumerate(codes) if dominates(solution, null, code)]
            need(good, f"scalar domination failure: {order} {name} {U}")
            coverage[tuple(good)] += 1
            if name == "C1_R2_Jordan" and not dominates(solution, null, (1, 2)):
                need(U[0][0] == U[1][0] == 0 and dominates(solution, null, (2,)), "Jordan exceptional control")
                if bad_one_code is None:
                    bad_one_code = {"U": U, "Phi": phi, "identity_preimage": solution, "kernel": null}
            # Recompute every declared solution and null vector directly.
            need([f.dot(row, solution) for row in phi] == [1, 0, 0, 1], "identity replay")
            for vector in null:
                need(not any(f.dot(row, vector) for row in phi), "kernel replay")
        need(rank_two == (order**3 - 1) * (order**3 - order), "complete rank-two selector count")
        data[name] = {"rank_two_selectors": rank_two, "identity_admissible": count,
                      "kernel_dimension_histogram": dict(sorted(histogram.items())),
                      "dominator_index_coverage": {str(key): value for key, value in sorted(coverage.items())}}
    need(bad_one_code is not None, "retain negative control for false one-code Jordan proof")
    entangled = {}
    for name in ("C3", "C2_C1", "C1_C1_C1"):
        shape = SHAPES[name]
        size = 1 + max(x for pair in shape for x in pair)
        checks = 0
        for coefficients in itertools.product(range(order), repeat=3):
            if not any(coefficients):
                continue
            pair = [[0, 0] for _ in range(size)]
            for a, indices in zip(coefficients, shape):
                for j, p in enumerate(indices):
                    pair[p][j] ^= a
            need(f.solve(pair)[0] == 2, "pure chain no-decomposable control")
            checks += 1
        entangled[name] = {"nonzero_vectors_checked": checks, "all_scalar_pair_ranks": 2, "envelope_dimension": size}
    return {"order": order, "regular_family_checks": data,
            "Jordan_one_code_negative_control": bad_one_code,
            "pure_chain_controls": entangled}


def classify_sizes():
    # L_e uses e+1 rows and e columns; its transpose R_e uses e rows and
    # e+1 columns. S_e denotes a regular square block of size e.
    blocks = [(f"C{e}", e + 1, e) for e in range(1, 4)]
    blocks += [(f"D{e}", e, e + 1) for e in range(1, 3)]
    blocks += [(f"R{e}", e, e) for e in range(1, 4)]
    larger = []
    right_cases = []
    for number in range(1, 4):
        for entries in itertools.combinations_with_replacement(blocks, number):
            rows = sum(e[1] for e in entries)
            cols = sum(e[2] for e in entries)
            if cols != 3:
                continue
            names = tuple(e[0] for e in entries)
            if any(name.startswith("D") for name in names):
                need(rows <= 3, "right singular block envelope gate")
                right_cases.append({"blocks": names, "D": rows})
            if rows > 3:
                larger.append({"blocks": names, "D": rows})
    expected = {("C3",), ("C2", "R1"), ("C1", "R2"),
                ("C1", "R1", "R1"), ("C1", "C2"),
                ("C1", "C1", "R1"), ("C1", "C1", "C1")}
    need({tuple(row["blocks"]) for row in larger} == expected, "all high-envelope KCF patterns")
    return {"larger_envelope_patterns": larger, "right_singular_patterns": right_cases}


def source_controls(repo):
    path = repo / NATIVE
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, "native source hash")
    native = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        r = list(map(Fraction, native["frames"][str(native["start"][i])]["B"][0]))
        norm = sum(x*x for x in r)
        scale = (2 if norm == 1 else 1) * (1 if next(x for x in r if x) > 0 else -1)
        r = [scale*x for x in r]
        need(all(x.denominator == 1 for x in r) and sum(x*x for x in r) == 4, "normalized roots")
        roots.append(tuple(map(int, r)))
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    adj = [sum(int(dot(r, s) == 0) << j for j, s in enumerate(roots)) for r in roots]
    K = [a | (1 << i) for i, a in enumerate(adj)]
    basis = bitbasis(K)
    need(len(basis) == 9, "canonical rank")
    code = [0]
    for word in basis:
        code += [x ^ word for x in list(code)]
    distance = min(x.bit_count() for x in code if x)
    forbidden = [min(x.bit_count() for x in {word & ~K[i] for word in code} if x) for i in range(111)]
    need(distance == 48 and min(forbidden) == 18, "global and forbidden distances")
    need(all({word for word in code if not(word & ~K[i])} == {0, K[i]} for i in range(111)), "canonical local rigidity")
    need(min(a.bit_count() for a in adj) == 55, "minimum canonical foreign degree")
    current = [((i,), adj[i]) for i in range(111)]
    counts = {}
    for size in range(1, 9):
        counts[size] = len(current)
        if size == 7:
            for clique, common in current:
                need(common.bit_count() <= 1, "orthogonal seven-set extension count")
                intersection = (1 << 111) - 1
                for i in clique:
                    intersection &= K[i]
                need(intersection == common | sum(1 << i for i in clique), "seven-set gluing support")
        if size < 8:
            current = [(clique+(j,), common & adj[j])
                       for clique, common in current
                       for j in members(common & ~((1 << (clique[-1]+1))-1))]
    need(counts[7] == 9443 and counts[8] == 1094, "complete source clique counts")

    # Credited existing boundary control: dimension four can meet chi194.
    S = [[54, 56, 57, 59, 61, 63, 64], [52, 53, 55, 58, 60, 62, 65]]
    need(not(set(S[0]) & set(S[1])), "disjoint boundary supports")
    fitting = list(K)
    for clique in S:
        need(all(adj[i] >> j & 1 for i, j in itertools.combinations(clique, 2)), "boundary seven-cliques")
        row = sum(1 << i for i in clique)
        for i in clique:
            fitting[i] = row
    need(all(row >> i & 1 and not(row & ~K[i]) for i, row in enumerate(fitting)), "boundary fitting mask")
    # Two coordinate copies of scalar binary rows.
    tensor_rows = lambda rows: [sum(((r >> j) & 1) << (2*j+c) for j in range(111)) for r in rows for c in range(2)]
    canonical_tensor = tensor_rows(basis)
    quotient = len(bitbasis(canonical_tensor+tensor_rows(fitting))) - len(canonical_tensor)
    need(quotient == 4, "dimension-four target boundary")
    return {"native_path": NATIVE, "native_sha256": PIN,
            "canonical_rank": 9, "minimum_global_weight": distance,
            "forbidden_distance_histogram": dict(sorted(Counter(forbidden).items())),
            "foreign_degree_histogram": dict(sorted(Counter(a.bit_count() for a in adj).items())),
            "orthogonal_clique_counts": counts,
            "credited_dimension_four_boundary": {"supports": S, "quotient_dimension": quotient,
                "proper_cover_charge": 194,
                "scope": "Six independent foreign roots at changed rows; inherited canonical chi2 at the other rows. No physical word."}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = args.repo / "research/moonshot-005-program"
    sources = [{"path": "research/moonshot-005-program/"+p,
                "sha256": hashlib.sha256((base/p).read_bytes()).hexdigest()} for p in DEPS]
    result = {"status": "PASS_AUTHOR_KRONECKER_QUOTIENT_CONTROLS",
              "proof_status": "universal proof in PROOF.md; independent review pending",
              "KCF_block_size_classification": classify_sizes(),
              "source": source_controls(args.repo),
              "finite_algebra_controls": [algebra_controls(2), algebra_controls(4)],
              "dependencies": sources,
              "claim": "Every native width2 quotient dim<=3 at chi<=194 is geometrically completely entangled and has pure left-chain type C3, C2+C1, or C1+C1+C1.",
              "new_complete_kappa": False,
              "physical_source_constructed": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "output": str(args.output),
                      "field4_rank_two_selectors_per_family": 3780,
                      "regular_families": 5, "native_seven_cliques": 9443,
                      "new_complete_kappa": False}))


if __name__ == "__main__":
    main()
