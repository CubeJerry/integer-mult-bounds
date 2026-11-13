#!/usr/bin/env python3
"""Independent source reconstruction and scalar support-distance bounds."""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

SRC_PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def directed_power(rank, bits=192):
    den = 1 << bits
    target = rank ** 199 * den ** 200
    lo, hi = 0, rank * den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, ("directed rank power", rank))
    return F(lo, den), F(lo + int(lo ** 200 != target), den)


def fmt_interval(x):
    return {"lower": str(x[0]), "upper": str(x[1])}


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def bit_rank(rows):
    pivots = {}
    for x in rows:
        y = int(x)
        while y:
            p = y.bit_length() - 1
            if p in pivots:
                y ^= pivots[p]
            else:
                pivots[p] = y
                break
    return len(pivots)


def reconstruct_K(native_path):
    raw = native_path.read_bytes()
    need(sha(raw) == SRC_PIN, "authenticated BIT native input pin")
    native = json.loads(gzip.decompress(raw))
    frames = {int(k): v for k, v in native["frames"].items()}
    roots = []
    for i in range(111):
        chart = native["start"][i]
        r = [F(x) for x in frames[chart]["B"][0]]
        norm = dot(r, r)
        need(norm in (1, 4), ("source root norm", i, norm))
        if norm == 1:
            r = [2 * x for x in r]
        need(dot(r, r) == 4, ("doubled root norm", i, r))
        need(all(x.denominator == 1 for x in r), ("integral E8 root", i, r))
        r = [int(x) for x in r]
        first = next(x for x in r if x)
        if first < 0:
            r = [-x for x in r]
        roots.append(r)
    need(len({tuple(r) for r in roots}) == 111, "source lines are distinct projective roots")
    K = []
    for i, a in enumerate(roots):
        row = 0
        for j, b in enumerate(roots):
            z = dot(a, b)
            need(z % 2 == 0, ("doubled-root Gram parity", i, j, z))
            # The actual canonical fitting is diagonal one, foreign one
            # exactly at real orthogonality contacts.
            value = int(i == j or z == 0)
            row |= value << j
            if i != j:
                need(value == int(z == 0), ("foreign contact equivalence", i, j, z))
        K.append(row)
    need(bit_rank(K) == 9, "canonical source fitting rank")
    supports = [row.bit_count() - 1 for row in K]
    need(min(supports) == 55 and max(supports) == 62, ("contact support range", min(supports), max(supports)))
    return native, roots, K, supports, raw


def distance_dp(supports, required_savings):
    """Relaxed minimum changed entries to lower row visit demand enough.

    For row support a, one visit can be saved only after at least a-52
    deletions, and the second only after a-36. These are necessary thresholds
    from the universal root-flat caps 52 and 36. A DP allows arbitrary
    independent entry deletion and ignores fitting constraints, so its cost
    is a rigorous lower bound on Hamming changes.
    """
    inf = 10**9
    dp = [0] + [inf] * 222
    for a in supports:
        c1, c2 = a - 52, a - 36
        ndp = [inf] * 223
        for saved, cost in enumerate(dp):
            if cost == inf:
                continue
            ndp[saved] = min(ndp[saved], cost)
            ndp[saved + 1] = min(ndp[saved + 1], cost + c1)
            ndp[saved + 2] = min(ndp[saved + 2], cost + c2)
        dp = ndp
    return min(dp[required_savings:])


def patch_geometry(supports):
    # In any scalar rank-one fit patch, diagonal preservation implies
    # U∩V=empty. Fitting zeros force every U×V pair to be a canonical contact,
    # so U roots are orthogonal to every V root.
    regimes = {
        "v0": {"max_affected_rows": 0, "max_visit_savings": 0, "minimum_visits_q9": 222},
        "v1": {"max_affected_rows": 62, "max_visit_savings": 0, "minimum_visits_q9": 222},
        "v2": {"max_affected_rows": 36, "max_visit_savings": 0, "minimum_visits_q9": 222},
        "v3_18": {"max_affected_rows": 36, "max_visit_savings": 36, "minimum_visits_q9": 186},
        "v19_plus": {"max_affected_rows": 6, "max_visit_savings": 12, "minimum_visits_q9": 210},
    }
    need(len(supports) == 111, "111 source rows")
    return regimes


def movement_price(args):
    budget_raw = args.budget.read_bytes()
    q8_raw = args.q8_result.read_bytes()
    budget = json.loads(budget_raw)
    q8 = json.loads(q8_raw)
    limit_data = budget["limiting_Q_allowance"]
    limit = (F(limit_data["lower"]), F(limit_data["upper"]))
    powers = {r: directed_power(r) for r in (7, 8)}
    base_q9 = (222 * powers[7][0] + 9 * powers[8][0],
               222 * powers[7][1] + 9 * powers[8][1])
    room_q9 = (limit[0] - base_q9[1], limit[1] - base_q9[0])
    q8_base = (F(1618), F(1618))
    room_q8 = (limit[0] - q8_base[1], limit[1] - q8_base[0])
    q8_pin = q8["limiting_perrail_margin"]
    q8_pinned_room = (F(q8_pin["lower"]), F(q8_pin["upper"]))
    need(q8_pinned_room[0] <= room_q8[0] <= room_q8[1] <= q8_pinned_room[1],
         ("q8 limiting-room pin", room_q8, q8_pinned_room))
    q8_m6_data = q8["fixed_even_cases"]["6"]["perrail_margin"]
    q8_m6_room = (F(q8_m6_data["lower"]), F(q8_m6_data["upper"]))
    need(room_q9[0] > 11 and room_q9[1] < 12, ("q9 extra-call ceiling", room_q9))
    need(room_q8[0] > 3 and room_q8[1] < 4, ("q8 extra-call ceiling", room_q8))
    q9_regime_calls = {"v1_2": 102, "v3_18": 66, "v19_plus": 90}
    q8_regime_calls = {"v1_2": 103, "v3_18": 67, "v19_plus": 91}
    q9_deficits, q8_deficits, q8_m6_deficits = {}, {}, {}
    for name, calls in q9_regime_calls.items():
        q9_deficits[name] = fmt_interval((base_q9[0] + calls - limit[1],
                                          base_q9[1] + calls - limit[0]))
    for name, calls in q8_regime_calls.items():
        q8_deficits[name] = fmt_interval((F(calls) - room_q8[1], F(calls) - room_q8[0]))
        q8_m6_deficits[name] = fmt_interval((F(calls) - q8_m6_room[1], F(calls) - q8_m6_room[0]))
    return {
        "budget_result_sha256": sha(budget_raw),
        "q8_target_result_sha256": sha(q8_raw),
        "t": "199/200",
        "rank_power_intervals": {str(k): fmt_interval(v) for k, v in powers.items()},
        "complete_limiting_allowance": fmt_interval(limit),
        "q9_optimistic_direct_path_base": fmt_interval(base_q9),
        "q9_remaining_room": fmt_interval(room_q9),
        "q9_max_extra_unit_arrivals": 11,
        "q9_one_patch_arrival_deficits_lower_intervals": q9_deficits,
        "q8_all_unit_route_base": 1618,
        "q8_remaining_room": fmt_interval(room_q8),
        "q8_max_extra_unit_arrivals_at_limit": 3,
        "q8_one_patch_arrival_deficits_lower_intervals": q8_deficits,
        "q8_m6_remaining_room": fmt_interval(q8_m6_room),
        "q8_m6_max_extra_unit_arrivals": 1,
        "q8_m6_one_patch_arrival_deficits_lower_intervals": q8_m6_deficits,
        "scope": "Optimistic movement-only lower charges: each additional positive-rank MOVE costs at least one. Ordinary work and path-refinement overhead are omitted. Every deficit is directed and conditional on the corresponding one-patch visit lower bound.",
    }


def main(args):
    native, roots, K, supports, source_raw = reconstruct_K(args.native)
    dist_q9 = distance_dp(supports, 102)
    dist_q8 = distance_dp(supports, 103)
    dist_q9_extra = {str(m): distance_dp(supports, 102 - m) for m in range(0, 13)}
    dist_q8_extra = {str(m): distance_dp(supports, 103 - m) for m in range(0, 5)}

    # Independently check the frozen rank-ten algebraic rectangle example.
    example = json.loads(args.patch_result.read_text())["rank10_rectangle_example"]
    Aset, Bset = set(example["A"]), set(example["B"])
    mask_v = sum(1 << j for j in Bset)
    patched = [row ^ (mask_v if i in Aset else 0) for i, row in enumerate(K)]
    changed = sum((K[i] ^ patched[i]).bit_count() for i in range(111))
    need(not Aset.intersection(Bset), "diagonal-safe rectangle sets")
    need(all(dot(roots[i], roots[j]) == 0 for i in Aset for j in Bset), "rectangle support-valid cross contacts")
    need(bit_rank(patched) == 10, "rank-ten rectangle example")
    need(changed == example["deleted_foreign_coefficients"] == 144, "rectangle changed-entry count")
    need(all((patched[i] >> i) & 1 for i in range(111)), "patched diagonal remains one")

    hist = Counter(supports)
    out = {
        "status": "PASS_INDEPENDENT_SCALAR_PATCH_GEOMETRY_AND_FITTING_DISTANCE",
        "source_sha256": sha(source_raw),
        "canonical_fitting_rank": bit_rank(K),
        "foreign_support_min_max": [min(supports), max(supports)],
        "foreign_support_histogram": {str(k): v for k, v in sorted(hist.items())},
        "one_rank_patch_arrival_regimes_q9": patch_geometry(supports),
        "one_rank_patch_required_extra_arrivals": {
            "v0_1_2": 102,
            "v3_18": 66,
            "v19_plus": 90,
        },
        "generic_hamming_distance_lower_bounds": {
            "q9_original_paths_only_visits120": dist_q9,
            "q8_original_paths_only_visits119": dist_q8,
            "q9_extra_arrivals_M_to_minimum_changed_entries": dist_q9_extra,
            "q8_extra_arrivals_M_to_minimum_changed_entries": dist_q8_extra,
            "interpretation": "For any scalar fitting A in this interface, measured against any fixed vertex-gauge K^g with the same contact support, the number of changed matrix positions is at least the DP value needed to reduce visit demand to the available total. The DP relaxes by allowing each changed position to delete one contact and ignores fit/algebra constraints.",
        },
        "rank10_rectangle_negative_control": {
            "rank": bit_rank(patched),
            "changed_contact_entries": changed,
            "support_valid": True,
            "physical_word": False,
            "warning": "This algebraic example does not imply every rank-ten fitting is a one-patch perturbation or physically realizable.",
        },
        "geometry_dependencies": {
            "E7_universal_proper_subspace_max": 36,
            "E7_universal_two_proper_union_max": 52,
            "E8_rank4_root_flat_max": 12,
            "E8_rank3_root_flat_max": 6,
        },
        "movement_price": movement_price(args),
        "scope": "Scalar characteristic-two fittings under the stated monotone no-Y-feedback path interface. Geometry caps are separately admitted dependencies. No unrestricted rank-two patch decomposition, arbitrary rank-ten classification, or construction is claimed.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "status": out["status"],
        "support_range": out["foreign_support_min_max"],
        "support_histogram": out["foreign_support_histogram"],
        "one_patch_extra_arrivals": out["one_rank_patch_required_extra_arrivals"],
        "q9_distance_no_extra_copies": dist_q9,
        "q9_distance_after11_extra_arrivals": dist_q9_extra["11"],
        "q8_distance_after3_extra_arrivals": dist_q8_extra["3"],
        "rank10_rectangle": out["rank10_rectangle_negative_control"],
    }, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--native", type=Path, required=True)
    p.add_argument("--patch-result", type=Path, required=True)
    p.add_argument("--budget", type=Path, required=True)
    p.add_argument("--q8-result", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
