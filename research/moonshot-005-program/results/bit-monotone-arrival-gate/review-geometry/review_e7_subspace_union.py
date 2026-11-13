#!/usr/bin/env python3
"""Independent E7 two-proper-subspace union review in 8D root coordinates.

The pinned 120-line system is reconstructed from source supports, then a
positive system, simple roots, fundamental weights, and Weyl orbits are built
directly in the ambient rational coordinates. This is independent of the
author's simple-coroot-coordinate orbit implementation.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from pathlib import Path

PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def canon(v):
    v = tuple(F(x) for x in v)
    first = next(x for x in v if x)
    return v if first > 0 else tuple(-x for x in v)


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    p = 0
    for c in range(len(a[0])):
        q = next((i for i in range(p, len(a)) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        z = a[p][c]
        a[p] = [x / z for x in a[p]]
        for i in range(len(a)):
            if i != p and a[i][c]:
                z = a[i][c]
                a[i] = [x - z * y for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def solve_square(a, b):
    """Exact Gauss-Jordan solution to square rational system A x=b."""
    n = len(a)
    m = [[F(x) for x in row] + [F(y)] for row, y in zip(a, b)]
    for c in range(n):
        q = next((i for i in range(c, n) if m[i][c]), None)
        need(q is not None, ("singular simple basis", c))
        m[c], m[q] = m[q], m[c]
        z = m[c][c]
        m[c] = [x / z for x in m[c]]
        for i in range(n):
            if i != c and m[i][c]:
                z = m[i][c]
                m[i] = [x - z * y for x, y in zip(m[i], m[c])]
    return tuple(m[i][-1] for i in range(n))


def reflect(v, alpha):
    q = dot(v, alpha)
    need(q.denominator == 1 and q.numerator % 2 == 0,
         ("reflection coefficient integral", tuple(v), tuple(alpha), q))
    c = q / 2
    return tuple(x - c * y for x, y in zip(v, alpha))


def main(args):
    repo = args.repo
    if (repo / "programme/research").exists():
        repo = repo / "programme"
    raw = (repo / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, "authenticated native hash")
    native = json.loads(gzip.decompress(raw))
    source = []
    for c in native["start"][:111]:
        row = tuple(F(x) for x in native["frames"][str(c)]["B"][0])
        if sum(bool(x) for x in row) == 1:
            row = tuple(2 * x for x in row)
        else:
            need(sum(bool(x) for x in row) == 4, ("source root support", c, row))
        need(dot(row, row) == 4, ("source root norm", c, row))
        source.append(canon(row))
    need(len(set(source)) == 111, "111 distinct source root lines")

    # Reconstruct full root lines from actual weight-four supports plus the
    # eight coordinate root lines, then independently verify reflection
    # closure, rank and transitivity.
    supports = sorted({tuple(i for i, x in enumerate(r) if x) for r in source if sum(bool(x) for x in r) == 4})
    need(len(supports) == 14, ("support blocks", len(supports)))
    roots = {tuple(2 * int(i == j) for j in range(8)) for i in range(8)}
    for supp in supports:
        # Choose first sign positive to quotient opposite roots.
        for signs in itertools.product((-1, 1), repeat=3):
            row = [0] * 8
            row[supp[0]] = 1
            for j, s in zip(supp[1:], signs):
                row[j] = s
            roots.add(canon(row))
    need(len(roots) == 120, ("full root line count", len(roots)))
    roots = sorted(roots)
    need(rank(roots) == 8, "full system spans R8")
    for u in roots:
        need(dot(u, u) == 4, ("root norm", u))
        for v in roots:
            q = dot(u, v)
            need(q % 2 == 0, ("integral Cartan pairing", u, v, q))
            w = canon(tuple(y - (q // 2) * x for x, y in zip(u, v)))
            need(w in set(roots), ("reflection closure", u, v, w))
    need(set(source) <= set(roots), "all actual source lines belong to reconstructed system")
    orbit = {roots[0]}
    todo = deque(orbit)
    while todo:
        v = todo.popleft()
        for alpha in roots:
            q = dot(v, alpha)
            need(q % 2 == 0, "root reflection coefficient")
            w = canon(tuple(y - (q // 2) * x for x, y in zip(alpha, v)))
            if w not in orbit:
                orbit.add(w)
                todo.append(w)
    need(orbit == set(roots), "Weyl group transitive on reconstructed 120 root lines")

    # Fix alpha=2e_0 by transitivity. Its orthogonal E7 subsystem is the 63
    # full root lines whose first coordinate is zero.
    e7 = sorted({tuple(F(x) for x in r) for r in roots if r[0] == 0})
    need(len(e7) == 63 and all(len(r) == 8 for r in e7), "63 E7 root lines")
    actual = [r for r in source if dot(r, (2, 0, 0, 0, 0, 0, 0, 0)) == 0]
    need(len(actual) == 56, ("actual roles in fixed E7 including target root", len(actual)))
    need(len(actual) >= 55, "fixed target has at least55 actual foreign contacts")

    # A generic integer functional selects one half of E7 roots. Its minimal
    # positive elements form a simple system. Search rather than reuse the
    # author's 3^i orientation, and compute weights in the 8D embedding.
    generic = None
    for b in range(2, 20):
        cand = tuple(F(b ** i) for i in range(8))
        if all(dot(cand, r) for r in e7):
            generic = cand
            break
    need(generic is not None, "found a regular E7 orientation")
    positives = {tuple(r) if dot(generic, r) > 0 else tuple(-x for x in r) for r in e7}
    sums = {tuple(u[i] + v[i] for i in range(8)) for u in positives for v in positives}
    simple = sorted(positives - sums)
    need(len(simple) == 7 and rank(simple) == 7, ("simple root basis", len(simple), rank(simple)))
    cartan = [[dot(a, b) // 2 for b in simple] for a in simple]
    need(all(cartan[i][i] == 2 for i in range(7)), "Cartan diagonal")
    need(all(cartan[i][j] in (0, -1) for i in range(7) for j in range(7) if i != j), "simply-laced Cartan off-diagonal")
    need(all(sum(cartan[i][j] != 0 for j in range(7) if j != i) <= 3 for i in range(7)), "finite E7 tree degrees")
    for r in e7:
        coeff = solve_square([[simple[j][i + 1] for j in range(7)] for i in range(7)], list(r[1:]))
        need(all(x.denominator == 1 for x in coeff), ("integral simple coefficients", r, coeff))
        need(all(x >= 0 for x in coeff) or all(x <= 0 for x in coeff), ("positive-root sign", r, coeff))

    # Fundamental weights are solved as ambient rational vectors omega_k in
    # x_0=0 with <omega_k, alpha_j>=2 delta_jk. Weyl orbits are generated by
    # reflecting those vectors in the 8D coordinates, not by Cartan-coordinate
    # updates. This is the independent orbit computation.
    simple7 = [[a[j] for j in range(1, 8)] for a in simple]
    weights = []
    for k in range(7):
        z = solve_square(simple7, [2 * int(j == k) for j in range(7)])
        weights.append(tuple([F(0), *z]))
    orbit_records = []
    all_masks = {}
    roots_by_mask = {}
    root_lines_by_index = e7
    for k, weight in enumerate(weights):
        start = canon(weight)
        reached = {start}
        q = deque([start])
        while q:
            v = q.popleft()
            for alpha in simple:
                w = canon(reflect(v, alpha))
                if w not in reached:
                    reached.add(w)
                    q.append(w)
        masks = {}
        for normal in reached:
            mask = 0
            for j, root in enumerate(root_lines_by_index):
                if dot(normal, root) == 0:
                    mask |= 1 << j
            need(mask not in masks, ("duplicate parabolic root mask within orbit", k, normal))
            masks[mask] = normal
        counts = {m.bit_count() for m in masks}
        need(len(counts) == 1, ("constant root count in orbit", k, counts))
        for mask, normal in masks.items():
            need(mask not in all_masks, ("parabolic masks across orbits disjoint", k, normal))
            all_masks[mask] = (k, normal)
            roots_by_mask[mask] = [root_lines_by_index[j] for j in range(63) if mask >> j & 1]
        orbit_records.append({
            "node": k,
            "fundamental_weight_8d": [[x.numerator, x.denominator] for x in weight],
            "line_orbit_size": len(reached),
            "root_lines_per_hyperplane": next(iter(counts)),
            "distinct_hyperplane_root_masks": len(masks),
        })
    need(len(all_masks) == 8821, ("all maximal parabolic flats", len(all_masks)))

    # For each possible first parabolic orbit representative, search the full
    # second-normal population. Weyl transitivity reduces arbitrary pairs to
    # these seven first representatives.
    by_node = defaultdict(list)
    for mask, (node, normal) in all_masks.items():
        by_node[node].append((mask, normal))
    pair_summaries = []
    for rec in orbit_records:
        node = rec["node"]
        first_mask = next(m for m, (n, _) in all_masks.items() if n == node)
        best = -1
        witnesses = []
        for second_mask, (second_node, second_normal) in all_masks.items():
            union = (first_mask | second_mask).bit_count()
            if union > best:
                best, witnesses = union, [(second_mask, second_node, second_normal)]
            elif union == best:
                witnesses.append((second_mask, second_node, second_normal))
        pair_summaries.append({
            "first_orbit": node,
            "first_mask": hex(first_mask),
            "max_union": best,
            "witness_count": len(witnesses),
            "first_witness": {
                "second_orbit": witnesses[0][1],
                "second_normal_8d": [[x.numerator, x.denominator] for x in witnesses[0][2]],
                "second_mask": hex(witnesses[0][0]),
                "intersection_lines": (first_mask & witnesses[0][0]).bit_count(),
            },
        })
    global_max = max(x["max_union"] for x in pair_summaries)
    need(global_max == 52, ("sharp maximum union", global_max))
    # Check an explicit sharp E6/E6 witness and a rejected 51 threshold.
    sharp = None
    for m1, (n1, v1) in all_masks.items():
        if m1.bit_count() != 36:
            continue
        for m2, (n2, v2) in all_masks.items():
            if m2.bit_count() == 36 and (m1 | m2).bit_count() == 52:
                sharp = (m1, n1, v1, m2, n2, v2)
                break
        if sharp:
            break
    need(sharp is not None, "explicit E6/E6 52-line pair")
    m1, n1, v1, m2, n2, v2 = sharp
    neg51 = {
        "status": "REJECTED",
        "union_size": (m1 | m2).bit_count(),
        "intersection_size": (m1 & m2).bit_count(),
        "first_orbit": n1,
        "second_orbit": n2,
        "first_normal_8d": [[x.numerator, x.denominator] for x in v1],
        "second_normal_8d": [[x.numerator, x.denominator] for x in v2],
        "first_mask": hex(m1),
        "second_mask": hex(m2),
        "union_root_lines_8d": [[[x.numerator, x.denominator] for x in root] for idx, root in enumerate(root_lines_by_index) if ((m1 | m2) >> idx) & 1],
    }

    # Actual source contact counts for all111 outputs in their E7 subsystems.
    contact_counts = []
    for i, r in enumerate(source):
        contacts = sum(1 for j, s in enumerate(source) if i != j and dot(r, s) == 0)
        need(55 <= contacts <= 62, ("actual contact count", i, contacts))
        contact_counts.append(contacts)
    need(min(contact_counts) > global_max, "no two proper subspaces cover actual contacts")

    out = {
        "status": "PASS_INDEPENDENT_8D_E7_ORBIT_AND_TWO_SUBSPACE_REVIEW",
        "native_sha256": PIN,
        "actual_source_line_count": len(source),
        "full_E8_line_count": len(roots),
        "full_E8_reflection_closure_checked": True,
        "full_E8_transitive_line_orbit_checked": len(orbit) == 120,
        "fixed_E7_root_line_count": len(e7),
        "simple_roots_8d": [[int(x) if x.denominator == 1 else str(x) for x in r] for r in simple],
        "cartan": cartan,
        "ambient_fundamental_weight_orbits": orbit_records,
        "all_distinct_parabolic_root_masks": len(all_masks),
        "pair_maxima_by_first_orbit": pair_summaries,
        "maximum_union": global_max,
        "sharp_e6_pair": {
            "first_orbit": n1,
            "second_orbit": n2,
            "first_normal_8d": [[x.numerator, x.denominator] for x in v1],
            "second_normal_8d": [[x.numerator, x.denominator] for x in v2],
            "first_root_count": m1.bit_count(),
            "second_root_count": m2.bit_count(),
            "intersection_count": (m1 & m2).bit_count(),
            "union_count": (m1 | m2).bit_count(),
        },
        "negative_51_control": neg51,
        "actual_contact_count_min_max": [min(contact_counts), max(contact_counts)],
        "independent_scope": "Exact ambient-coordinate reflection/orbit replay. Universal real-subspace reduction is reviewed separately below: every proper subspace has a nonzero normal in E7, Weyl-conjugate it to the closed dominant chamber, and its orthogonal roots lie in a maximal parabolic flat. The finite orbit certificate then bounds arbitrary real subspaces. This is geometry only; no source chronology, event-count theorem, supplier, or kappa is admitted here.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "status": out["status"],
        "orbit_records": orbit_records,
        "all_parabolic_flats": len(all_masks),
        "pair_maxima": [{"orbit": x["first_orbit"], "max_union": x["max_union"]} for x in pair_summaries],
        "sharp_pair": out["sharp_e6_pair"],
        "negative_51": neg51["status"],
        "contact_count_min_max": out["actual_contact_count_min_max"],
    }, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
