#!/usr/bin/env python3
"""Independent finite corroboration of the heterogeneous Gaussian proof.

This checker never imports the author's verifier. It uses exact rational
matrix entries q_i**(x_i-y_i)**2 * v_i**(x_i-y_i), not the author's
rational-log-exponent representation or exponential interval routine.
Default operation prints JSON and does not create or overwrite artifacts.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from math import factorial, lcm, prod
from pathlib import Path


PINS = {
    "PROOF.md": "7ce68fdc614b28df6133682ee2e82f661c2d373ceb645f24f4a93d76a9d0955c",
    "verify.py": "18214b9c995512b2ef33ceaaaba6f5fbf23eaae4ed40e77355b6edb3f06dbf51",
    "inputs/GAUGEFREE-INTERIORS.md": "a7fc34302a70f8453f877a6433ffe2776457bf37b5d8bb262afcb6b198a935fc",
    "inputs/FINE-PRIME-PADDING.md": "47d1b1b4df28aadda3cd6bdeb1fbc47290595e9208cd09c1a1f338520d33fdce",
    "inputs/HOMOGENEOUS-ORBIT-SCALE.md": "3d86ae5437c3415c4f8a638dcb7c6fca3c3c332486fe13cff79d845e8fb56077",
}


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def vertices(ns):
    need(bool(ns) and all(type(n) is int and n >= 2 for n in ns), "Nondegenerate integer sides")
    return tuple(product(*(range(n) for n in ns)))


def kernel(ns, qs, vs):
    points = vertices(ns)
    need(len(qs) == len(vs) == len(ns), "Parameter dimensions")
    need(all(0 < q < 1 for q in qs) and all(v > 0 for v in vs), "Positive widths and gauges")
    return tuple(tuple(prod(q ** ((x-y)**2) * v ** (x-y)
                            for x, y, q, v in zip(a, b, qs, vs))
                       for b in points) for a in points)


def all_symmetries(matrix):
    """Try every vertex permutation; no coordinate or metric prefilter."""
    size = len(matrix)
    need(size <= 9, "Bounded complete permutation domain")
    labels = {x: i for i, x in enumerate(set(x for row in matrix for x in row))}
    table = tuple(tuple(labels[x] for x in row) for row in matrix)
    # Diagonals and each ordered off-diagonal entry are all tested.
    pairs = [(i, i) for i in range(size)]
    pairs += [(i, j) for i in range(size) for j in range(size) if i != j]
    answers = set()
    for p in permutations(range(size)):
        if all(table[i][j] == table[p[i]][p[j]] for i, j in pairs):
            answers.add(p)
    return answers


def signed_axis_maps(ns, qs=None, vs=None):
    points = vertices(ns)
    index = {p: i for i, p in enumerate(points)}
    d = len(ns)
    answers = set()
    for dest in permutations(range(d)):
        if any(ns[i] != ns[dest[i]] for i in range(d)):
            continue
        if qs is not None and any(qs[i] != qs[dest[i]] for i in range(d)):
            continue
        for signs in product((-1, 1), repeat=d):
            if vs is not None and any(vs[dest[i]] ** signs[i] != vs[i] for i in range(d)):
                continue
            image = []
            for point in points:
                out = [None] * d
                for i, j in enumerate(dest):
                    out[j] = point[i] if signs[i] == 1 else ns[i] - 1 - point[i]
                image.append(index[tuple(out)])
            answers.add(tuple(image))
    return answers


def reflections(ns):
    points = vertices(ns)
    index = {p: i for i, p in enumerate(points)}
    return {tuple(index[tuple(n-1-x if flip else x for x, n, flip in zip(p, ns, mask))]
                  for p in points) for mask in product((False, True), repeat=len(ns))}


def cycle_data(p):
    todo = set(range(len(p)))
    lengths = []
    while todo:
        first = min(todo)
        i, length = first, 0
        while i in todo:
            todo.remove(i)
            length += 1
            i = p[i]
        need(i == first, "Closed permutation cycle")
        lengths.append(length)
    return len(lengths), lcm(*lengths), lengths.count(1)


def exact_min_cycles(ns, vs):
    total = prod(ns)
    zero = [i for i, v in enumerate(vs) if v == 1]
    if any(ns[i] % 2 == 0 for i in zero):
        return total // 2
    return (total + total // prod(ns[i] for i in zero)) // 2


def nearest_dyadic(x, bits):
    scaled = x * (1 << bits)
    floor = scaled.numerator // scaled.denominator
    return Q(floor + (2 * (scaled.numerator % scaled.denominator) >= scaled.denominator), 1 << bits)


def rounded(matrix, bits):
    return tuple(tuple(nearest_dyadic(x, bits) for x in row) for row in matrix)


def max_error(a, b):
    return max(abs(x-y) for row_a, row_b in zip(a, b) for x, y in zip(row_a, row_b))


def exact_gap(qs):
    levels = [q*q for q in qs]
    edge = min(levels) - max(q**4 for q in qs)
    # For gamma=-log(q), the mean-value theorem gives
    # |gamma_i-gamma_j| >= |q_i-q_j|/max(q).  This supplies a
    # rational lower bound for the theorem's B*, not just observed levels.
    qgap = min((abs(a-b) for i, a in enumerate(qs) for b in qs[i+1:]), default=None)
    color = 2*min(levels)*qgap/max(qs) if qgap is not None else Q(1)
    return min(edge, color)


def guarded_rounding(ns, qs, vs, bits):
    need(all(q <= v <= 1/q for q, v in zip(qs, vs)), "Unit-entry shift regime")
    raw = kernel(ns, qs, vs)
    stored = rounded(raw, bits)
    error = max_error(raw, stored)
    need(4*error + 2*error*error < exact_gap(qs), "Independent exact pair-level gap")
    group = all_symmetries(stored)
    need(group <= reflections(ns), "Rounded symmetry containment")
    need(all(cycle_data(p)[1] <= 2 for p in group), "Rounded order-two bound")
    return raw, stored, group, error


def inverse(matrix):
    size = len(matrix)
    rows = [list(row) + [Q(i == j) for j in range(size)] for i, row in enumerate(matrix)]
    for j in range(size):
        pivot = next((i for i in range(j, size) if rows[i][j]), None)
        need(pivot is not None, "Nonsingular exact kernel")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x/scale for x in rows[j]]
        for i in range(size):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[j])]
    return tuple(tuple(row[size:]) for row in rows)


def run(package):
    source_hashes = {}
    for name, wanted in PINS.items():
        digest = sha256((package/name).read_bytes()).hexdigest()
        need(digest == wanted, "Frozen review input: " + name)
        source_hashes[name] = digest

    fixtures = [
        ("one_axis_two", (2,), (Q(1,2),), (Q(1),)),
        ("one_axis_shifted_three", (3,), (Q(1,2),), (Q(3,2),)),
        ("equal_width_swap", (2,2), (Q(1,2),Q(1,2)), (Q(1),Q(1))),
        ("distinct_widths", (2,2), (Q(1,2),Q(1,3)), (Q(1),Q(1))),
        ("equal_physical_sides_unequal_counts", (2,3), (Q(1,16),Q(1,2)), (Q(1),Q(1))),
        ("equal_width_unequal_counts", (2,3), (Q(1,2),Q(1,2)), (Q(1),Q(1))),
        ("opposite_shifts", (2,2), (Q(1,2),Q(1,2)), (Q(3,2),Q(2,3))),
        ("three_distinct_widths", (2,2,2), (Q(1,2),Q(2,5),Q(1,3)), (Q(1),Q(1),Q(1))),
        ("two_nonzero_shifts", (2,2,2), (Q(1,2),Q(2,5),Q(1,3)), (Q(3,2),Q(1),Q(2))),
        ("mixed_signed_class", (2,2,2), (Q(1,2),Q(1,2),Q(1,3)), (Q(3,2),Q(2,3),Q(1))),
        ("axis_diagonal_metric_coincidence", (2,2,2), (Q(1,2),Q(1,3),Q(1,6)), (Q(1),Q(1),Q(1))),
        ("all_nine_vertices_odd_reflections", (3,3), (Q(1,2),Q(1,3)), (Q(1),Q(1))),
        ("all_nine_vertices_one_zero_shift", (3,3), (Q(1,2),Q(1,3)), (Q(1),Q(3,2))),
    ]
    reports, groups = [], {}
    for name, ns, qs, vs in fixtures:
        matrix = kernel(ns, qs, vs)
        found = all_symmetries(matrix)
        predicted = signed_axis_maps(ns, qs, vs)
        need(found == predicted, "Complete classification: " + name)
        census = [cycle_data(p) for p in found]
        if len(set(qs)) == len(qs):
            need(all(order <= 2 for _, order, _ in census), "Distinct-width involutions")
            need(min(c for c, _, _ in census) == exact_min_cycles(ns, vs), "Exact fixed-point minimum")
            need(all(prod(ns)**2 <= 2*c*prod(ns) <= 2*prod(ns)**2 for c, _, _ in census), "Dense-slot bounds")
        groups[name] = found
        reports.append({"name":name, "sides":ns, "q":list(map(str,qs)), "v":list(map(str,vs)),
                        "permutations_examined":factorial(prod(ns)), "group_size":len(found),
                        "maximum_order":max(o for _, o, _ in census), "minimum_cycles":min(c for c, _, _ in census)})

    # Independent elimination checks the inverse claim on a non-symmetric matrix.
    ns, qs, vs = (2,3), (Q(1,2),Q(1,3)), (Q(3,2),Q(2))
    matrix = kernel(ns, qs, vs)
    inv = inverse(matrix)
    need(all(sum(matrix[i][k]*inv[k][j] for k in range(6)) == (i == j)
             for i in range(6) for j in range(6)), "Literal rational inverse")
    need(all_symmetries(inv) == all_symmetries(matrix), "Inverse symmetry equivalence")

    fine_reports = []
    for name, ns, qs, vs, bits in [
        ("fine_unshifted", (2,2,2), (Q(1,2),Q(2,5),Q(1,3)), (Q(1),Q(1),Q(1)), 12),
        ("fine_shifted", (2,3), (Q(1,2),Q(1,3)), (Q(3,2),Q(2)), 12),
        ("tiny_shift_lost", (2,2), (Q(1,2),Q(1,3)), (Q(1)+Q(1,2**30),Q(1)), 12),
    ]:
        raw, stored, found, error = guarded_rounding(ns, qs, vs, bits)
        original = all_symmetries(raw)
        need(original <= found, "A common deterministic rounding rule preserves symmetry")
        if name == "tiny_shift_lost":
            need(len(found) > len(original), "Tiny nonzero shift can gain reflection")
        fine_reports.append({"name":name, "sides":ns, "bits":bits,
                             "entry_error":str(error), "pair_gap":str(exact_gap(qs)),
                             "ideal_group_size":len(original), "stored_group_size":len(found),
                             "permutations_examined_per_matrix":factorial(prod(ns))})

    controls = {}
    controls["equal_widths_allow_order_four"] = max(cycle_data(p)[1] for p in groups["equal_width_swap"]) == 4
    # In a square physical hull, the midpoint would have nonintegral native x.
    controls["square_hull_midpoint_not_grid"] = (Q(1,2),Q(0)) not in vertices((2,3))
    controls["opposite_shifts_need_signed_swap"] = len(groups["opposite_shifts"]) == 2
    coarse_raw = kernel((2,2), (Q(1,2),Q(1,3)), (Q(1),Q(1)))
    coarse = rounded(coarse_raw, 1)
    coarse_group = all_symmetries(coarse)
    controls["coarse_rounding_merges_axis_levels"] = max(cycle_data(p)[1] for p in coarse_group) == 4
    coarse_error = max_error(coarse_raw, coarse)
    controls["coarse_rounding_fails_gap"] = 4*coarse_error+2*coarse_error**2 >= exact_gap((Q(1,2),Q(1,3)))
    altered = [list(row) for row in coarse_raw]
    eps = Q(1,4096)
    for i in range(4):
        altered[i][i] += eps*Q(i+1,5)
    need(max_error(coarse_raw, altered) <= eps, "Arbitrary perturbation is small")
    need(4*eps+2*eps**2 < exact_gap((Q(1,2),Q(1,3))), "Small perturbation meets guard")
    controls["arbitrary_small_diagonal_errors_destroy_symmetry"] = len(all_symmetries(altered)) == 1
    for name, params in [
        ("zero_width_rejected", ((2,2),(Q(1),Q(1,2)),(Q(1),Q(1)))),
        ("degenerate_axis_rejected", ((1,2),(Q(1,2),Q(1,3)),(Q(1),Q(1)))),
    ]:
        try:
            kernel(*params)
        except ValueError:
            controls[name] = True
        else:
            controls[name] = False
    need(all(controls.values()), "All semantic countercontrols")

    # Exact source-format witness: different dyadic target sizes and odd primes.
    r, p = 64, 2
    targets, primes = (64,32), (59,29)
    eta = Q(1,4*p*p)
    need(all((1-2*eta)*t < s <= (1-eta)*t for t,s in zip(targets,primes)), "Fine-prime interval")
    need(all(s % k for s in primes for k in range(2,s) if k*k <= s), "Direct prime witness")
    ms = tuple(r//t*s for t,s in zip(targets,primes))
    need(ms == (59,58), "Distinct integer numerators across size groups")
    broad = tuple(Q(m,r) for m in ms)
    narrow = tuple(Q(r,m) for m in ms)
    need(abs(broad[0]-broad[1]) == Q(1,r), "Sharp broad gap after scaling b0=1")
    need(abs(narrow[0]-narrow[1]) > Q(1,r), "Strict narrow gap after scaling A=1")

    return {"status":"PASS_INDEPENDENT_HETEROGENEOUS_REVIEW", "source_sha256":source_hashes,
            "independence":"No predecessor executable imported; rational entries and exhaustive vertex permutations.",
            "exact_fixtures":reports, "classification_permutations":sum(x["permutations_examined"] for x in reports),
            "inverse":{"vertices":6,"all_permutations":720,"group_size":1},
            "rounding":fine_reports, "controls":controls,
            "source_format_witness":{"p":p,"r":r,"targets":targets,"primes":primes,"m":ms,
                                     "broad_gap_b0_one":str(abs(broad[0]-broad[1])),
                                     "narrow_gap_A_one":str(abs(narrow[0]-narrow[1]))},
            "scope":"Finite corroboration supplements the universal proof; no runtime, source admission or kappa claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(run(args.package), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
