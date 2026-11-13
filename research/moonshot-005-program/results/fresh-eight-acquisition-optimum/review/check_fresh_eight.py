#!/usr/bin/env python3
"""Independent exact geometry check for the fresh-eight line-return gate.

No programme checker or author helper is imported. Uses exact integer roots,
source gzip pinned by SHA-256, and rational elimination over Q.
"""
import argparse, gzip, hashlib, itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

NATIVE_SHA = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
FULL_SHA = "d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7"
CALLER_SHA = "b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248"
CHART_GATE_SHA = "dae0ad585ad8c2d6a1d128dc32b00025388089fec08d17d9f02accae8e7ed6c4"
CHART_REVIEW_SHA = "57fc50cabcba8dc8ca5b6fb7aae03a11be6617e8a7807c04c4aa2a98cd05002f"

def need(test, msg):
    if not test:
        raise ValueError(msg)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def root9(n):
    bits = [j for j in range(9) if (n >> j) & 1]
    if len(bits) == 3:
        return tuple(2 if j in bits else -1 for j in range(9))
    need(len(bits) == 7, f"not a weight-three/seven normal: {n}")
    p, q = [j for j in range(9) if j not in bits]
    return tuple(3 * (int(j == p) - int(j == q)) for j in range(9))

def dot(a, b):
    return sum(x*y for x, y in zip(a,b))

def rank_q(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    nr, nc = len(a), len(a[0])
    p = 0
    for c in range(nc):
        pivot = next((r for r in range(p,nr) if a[r][c]), None)
        if pivot is None:
            continue
        a[p], a[pivot] = a[pivot], a[p]
        v = a[p][c]
        a[p] = [x/v for x in a[p]]
        for r in range(p+1,nr):
            if a[r][c]:
                v = a[r][c]
                a[r] = [x-v*y for x,y in zip(a[r],a[p])]
        p += 1
        if p == nr:
            break
    return p

def power_interval(r, precision=140):
    """Exact dyadic enclosure of r^(199/200), by integer 200th roots."""
    den = 1 << precision
    target = (r ** 199) * (den ** 200)
    lo, hi = 0, r * den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, "exact 200th-root bracket")
    upper = lo if lo ** 200 == target else lo + 1
    return Fraction(lo, den), Fraction(upper, den)

def signed_moment(profile, precision=140):
    """Exact rational lower/upper bounds for sum profile[r] r^(199/200)."""
    low = high = Fraction(0)
    for r, coefficient in profile.items():
        l, h = power_interval(r, precision)
        if coefficient >= 0:
            low += coefficient * l
            high += coefficient * h
        else:
            low += coefficient * h
            high += coefficient * l
    return low, high

def main(args):
    source_path = args.repo / "research/shared-wire-split-composition/data/final.json.gz"
    raw = source_path.read_bytes()
    need(sha(raw) == NATIVE_SHA, "native source pin mismatch")
    s = json.loads(gzip.decompress(raw))
    dports = s["hosted"]["Dports"]
    hosted_values = [s["live"][k] for k in dports]
    need(len(hosted_values) == 96, "expected 96 D ports")
    normals = [s["frames"][s["initial"][h]][0] for h in hosted_values]
    need(len(set(normals)) == 96, "hosted D normals not distinct")
    need(all(n.bit_count() in (3,7) for n in normals), "unexpected source root weight")
    all_roots = {n for n in range(512) if n.bit_count() in (3,7)}
    omitted = sorted(all_roots - set(normals))
    need(len(omitted) == 24, "expected 24 omitted root normals")

    # These exact predecessor pins own the all-511 shortened-rank theorem;
    # this run repeats it only as a consistency check for the new support data.
    chart_gate = args.repo / "research/moonshot-005-program/results/reverse-gram-packet-chart-gate/REVERSE-PACKET-CHART-GATE.md"
    chart_review = args.repo / "research/moonshot-005-program/results/reverse-gram-packet-chart-gate/review/REVIEW.md"
    need(sha(chart_gate.read_bytes()) == CHART_GATE_SHA, "predecessor chart-gate proof pin")
    need(sha(chart_review.read_bytes()) == CHART_REVIEW_SHA, "predecessor chart-gate review pin")

    # For every chart direction, independently check the shortened-source rank.
    line_ranks = Counter()
    exceptional = []
    rank_rows = []
    source_roots = [root9(n) for n in normals]
    for c in range(1,512):
        forbidden = [source_roots[j] for j,n in enumerate(normals) if ((c & n).bit_count() & 1)]
        r = rank_q(forbidden)
        line_ranks[r] += 1
        if c in omitted:
            need(r == 7, f"exceptional c={c} forbidden rank {r}, not 7")
            rc = root9(c)
            need(all(dot(rc, v) == 0 for v in forbidden), f"r(c) does not annihilate forbidden roots c={c}")
            exceptional.append(c)
        else:
            need(r == 8, f"ordinary c={c} forbidden rank {r}, not 8")
        rank_rows.append({"c": c, "rank_forbidden": r, "count_forbidden": len(forbidden)})
    need(dict(line_ranks) == {7:24, 8:487}, f"unexpected line rank distribution {line_ranks}")
    need(exceptional == omitted, "exceptional line list differs from omitted root normals")

    # At an exceptional line c, the unique shortened Gram functional is the
    # inner-product row r(c) against hosted source roots. Check support against
    # the actual root-pair values and the facet-incidence parity description.
    supports = {}
    for c in exceptional:
        rc = root9(c)
        coeffs = [dot(rc, v) for v in source_roots]
        S_gram = {j for j,x in enumerate(coeffs) if x != 0}
        S_facet = {j for j,n in enumerate(normals) if ((c & n).bit_count() & 1) == 0}
        need(S_gram == S_facet, f"Gram support and actual line incidence differ at c={c}")
        need(all(x in (-18,-9,0,9,18) for x in coeffs), "unexpected root inner product scale")
        # Nonzero entries have the same coordinate support for any full-field
        # invertible basis of the one-dimensional shortened code.
        supports[c] = S_gram

    sizes = {str(c): len(S) for c,S in supports.items()}
    min_size = min(sizes.values())
    min_lines = sorted(c for c,S in supports.items() if len(S) == min_size)
    need(min_size == 43 and min_lines == [81], f"support minimum not unique at 81: {min_size}, {min_lines}")

    intersections = []
    min_intersection = 96
    min_pairs = []
    for c,d in itertools.combinations(exceptional,2):
        overlap = len(supports[c] & supports[d])
        intersections.append({"c": c, "d": d, "overlap": overlap})
        if overlap < min_intersection:
            min_intersection = overlap
            min_pairs = [(c,d)]
        elif overlap == min_intersection:
            min_pairs.append((c,d))
    need(len(intersections) == 276 and min_intersection >= 15, f"pair overlap floor failed: {min_intersection}")

    # Negative controls: a hosted root is not an eligible line, and line81's
    # support must really be 43 (not merely the 37 all-row theorem floor).
    included = set(normals)
    bad_c = min(included)
    need(bad_c not in supports, "included hosted normal was accidentally treated as exceptional")
    need(len(supports[81]) == 43, "line81 support control failed")

    # Independently rebuild the exact fixed-m complete-caller comparison for
    # the fresh-eight candidate. The full caller and H4 invoice are pinned.
    full_path = args.repo / "research/shared-wire-split-composition/FULL-RESULT.json"
    caller_path = args.repo / "research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json"
    full_bytes, caller_bytes = full_path.read_bytes(), caller_path.read_bytes()
    need(sha(full_bytes) == FULL_SHA and sha(caller_bytes) == CALLER_SHA, "complete-caller profile pins")
    full, caller = json.loads(full_bytes), json.loads(caller_bytes)
    T = {int(k): int(v) for k,v in full["invoice"]["T"].items()}
    P = {int(k): int(v) for k,v in full["invoice"]["P"].items()}
    N = {int(k): int(v) for k,v in full["native"]["paid"].items()}
    H = {int(k): int(v) for k,v in full["native"]["helpers"].items()}
    # 400 direct raw paths, with the 43 paths required at line81 split 1+7;
    # eight forward rank-nine packets, eight rank-one entry calls, and seven
    # rank-nine plus one rank-eight returns.
    q_best = {1: 51, 7: 43, 8: 358, 9: 15}
    need(sum(q_best.values()) == 467, "fresh-eight schedule MOVE count")
    need(q_best == {1: 43+8, 7: 43, 8: 357+1, 9: 8+7}, "fresh-eight schedule tariff decomposition")

    signed_gap = {r: 18*q_best.get(r,0)-18*N.get(r,0)+18*H.get(r,0)-T.get(r,0)+P.get(r,0)
                  for r in set(q_best)|set(N)|set(H)|set(T)|set(P)}
    gap_lo, gap_hi = signed_moment(signed_gap)
    gap_lo /= 18; gap_hi /= 18
    need(gap_lo > 0, "limiting fresh-eight deficit is not strictly positive")
    tp = {r: T.get(r,0)-P.get(r,0) for r in set(T)|set(P)}
    d_lo, d_hi = signed_moment(tp)
    d_lo, d_hi = -d_hi/18, -d_lo/18
    need(d_lo > 0, "finite-m correction d is not strictly positive")

    # Rebuild the exact return/refinement-only split and the m->infinity
    # allowance after raw-direct, forward, and entry calls are paid.
    t = Fraction(199,200)
    p1l,p1h = power_interval(1);p7l,p7h = power_interval(7)
    p8l,p8h = power_interval(8);p9l,p9h = power_interval(9)
    j8_lo = 7*p9l+p8l+43*(p1l+p7l-p8h)
    j8_hi = 7*p9h+p8h+43*(p1h+p7h-p8l)
    other = {r: N.get(r,0)-H.get(r,0) for r in set(N)|set(H)}
    other.update({r: other.get(r,0)+(T.get(r,0)-P.get(r,0))/18 for r in set(T)|set(P)})
    # Use a denominator of 18 throughout to avoid Fraction profile truncation.
    allowance_numer = {r: 18*(N.get(r,0)-H.get(r,0)) + T.get(r,0)-P.get(r,0)
                       for r in set(N)|set(H)|set(T)|set(P)}
    allowance_numer[8] = allowance_numer.get(8,0)-18*400
    allowance_numer[9] = allowance_numer.get(9,0)-18*8
    allowance_numer[1] = allowance_numer.get(1,0)-18*8
    allow_lo, allow_hi = signed_moment(allowance_numer)
    allow_lo /= 18; allow_hi /= 18
    jgap_lo, jgap_hi = j8_lo-allow_hi, j8_hi-allow_lo
    need(jgap_lo > 0, "J8 does not exceed the optimistic fixed-m allowance")

    # k>=2 line births can be priced even if raw-source branching is allowed
    # and fully billed. One primary visit for each source in the union costs
    # at least the 1+7^t subdivision. For each additional line, overlap with
    # the first is >=15; each repeated source must be independently moved from
    # the common zero chart to that incomparable line, costing >=1.
    delta_lo, delta_hi = p9l-p8h, p9h-p8l
    need(Fraction(15) > delta_hi, "15 MOVE branch penalty does not exceed packet saving")
    all_zero_lo, all_zero_hi = 8*p9l, 8*p9h
    need(all_zero_lo > j8_hi, "zero-line architecture unexpectedly cheaper than J8")

    result = {
        "status": "PASS_INDEPENDENT_FRESH_EIGHT_LINE_GEOMETRY",
        "native_sha256": NATIVE_SHA,
        "hosted_D_count": len(normals),
        "omitted_normals": omitted,
        "line_rank_counts": dict(sorted(line_ranks.items())),
        "exceptional_lines": exceptional,
        "support_sizes": sizes,
        "minimum_support_size": min_size,
        "minimum_support_lines": min_lines,
        "pair_count": len(intersections),
        "minimum_pair_intersection": min_intersection,
        "minimum_intersection_pairs": min_pairs,
        "support_identity": "nonzero inner products dot(r(c),r(n_i)) exactly equal source facets containing c",
        "predecessor_chart_gate_sha256": CHART_GATE_SHA,
        "predecessor_chart_review_sha256": CHART_REVIEW_SHA,
        "complete_caller_sha256": FULL_SHA,
        "H4_invoice_sha256": CALLER_SHA,
        "fresh_eight_paid_profile": {str(k):v for k,v in sorted(q_best.items())},
        "fresh_eight_limiting_gap_bounds": [str(gap_lo), str(gap_hi)],
        "finite_m_penalty_d_bounds": [str(d_lo), str(d_hi)],
        "return_refinement_J8_bounds": [str(j8_lo), str(j8_hi)],
        "optimistic_remaining_return_refinement_allowance_bounds": [str(allow_lo), str(allow_hi)],
        "J8_minus_allowance_bounds": [str(jgap_lo), str(jgap_hi)],
        "all_zero_return_price_bounds": [str(all_zero_lo), str(all_zero_hi)],
        "extra_branch_price_argument": "For k>=2 distinct line births, each j>1 shares at least15 source indices with line1. Per source, one primary route serving endpoint+one line costs excess >=1+7^t-8^t; every additional incomparable line needs another rank>=1 raw MOVE. Thus candidate price exceeds k=1 by at least (k-1)(15-(9^t-8^t))>0, even when these branches are allowed and billed.",
        "negative_controls": {"included_hosted_normal_rejected": bad_c, "line81_support_is_43": True},
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "FRESH-EIGHT-GEOMETRY.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (args.output / "FRESH-EIGHT-LINE-RANKS.json").write_text(json.dumps(rank_rows, indent=2, sort_keys=True) + "\n")
    (args.output / "FRESH-EIGHT-PAIR-INTERSECTIONS.json").write_text(json.dumps(intersections, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
