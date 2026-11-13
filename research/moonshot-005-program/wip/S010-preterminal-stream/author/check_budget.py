#!/usr/bin/env python3
"""Conditional stream tariff and inherited clean-chart support receipts.

This file constructs no rank-eight current-row source or observation word.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
FULL = "d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7"
PARENT = "a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc"
FOUR = "20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f"
EXTRACT = "7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372"
DEPENDENCIES = {
    "research/moonshot-005-program/results/standalone-cyclic-rail/PROOF.md":
        "1d016a8958c035a3251d5c87256835ccdcd8f6aa4573818053728bb3dd35e9d9",
    "research/moonshot-005-program/results/standalone-cyclic-rail/ADMISSION.md":
        "587cc548b9fc2c6bebbd953114757dd17ded78ea12a9082cf819c2dbd85ebfd4",
    "research/moonshot-005-program/results/nine-packet-no-line-gate/PROOF.md":
        "15f8ff31d3f103f9fbea45a36842b8635f6dcd7c02e87d6479751e0af49eac9c",
    "research/moonshot-005-program/results/nine-packet-no-line-gate/review-root/REVIEW.md":
        "cf99298b5f0b6e717fd45f94676b07dddceb20c4df763063d0db8fbb67146d4c",
    "research/moonshot-005-program/results/nine-packet-no-line-gate/review-root/RESULT.json":
        "7def61d54916bd6953a0bc4163c7470f8c343b03f0ce7e1d1bb6396eae759760",
    "research/moonshot-005-program/results/unchanged-donor-contact-bound/PROOF.md":
        "8893207a0abf978062c76bac2ffd46da757df0757360332b99fc8a0fd97e4026",
    "research/moonshot-005-program/results/unchanged-donor-contact-bound/DISCOVERY-REVIEW.json":
        "8a5f12db177cd6c3d95e30237d36ccafc2eb36e749ee34069b1fe351b951d0b3",
    "research/moonshot-005-program/results/hosted-gram-distance42/PROOF.md":
        "77c996ff9233f087a0e024c107b552f022adeca51cf5540c2487ef80cb2a2506",
    "research/moonshot-005-program/results/hosted-gram-distance42/review/REVIEW.md":
        "243dd13d54ef1a69f801bb264903dbdce5a557d022f303b53b9eedb4ab0a3846",
    "research/moonshot-005-program/results/s008-recovered-cut-and-entry/TRANSPORT-GATES.md":
        "2620d9e1be37873d59b1da99e41deb59b83b29791fd084635d888de2395e927f",
}


def need(test, message):
    if not test:
        raise ValueError(message)


def read(path, pin):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == pin, f"Source pin: {path}")
    return raw


def iroot(a, n):
    lo, hi = 0, 1 << ((a.bit_length() + n - 1) // n)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**n <= a:
            lo = mid
        else:
            hi = mid
    need(lo**n <= a < (lo + 1)**n, "Integer root enclosure")
    return lo


POWERS = {}


def power(r):
    if r not in POWERS:
        den = 10**40
        target = r**199 * den**200
        z = iroot(target, 200)
        POWERS[r] = (F(z, den), F(z if z**200 == target else z + 1, den))
    return POWERS[r]


def moment(profile):
    low = high = F(0)
    for r, c in profile.items():
        a, b = power(r)
        low += c * (a if c >= 0 else b)
        high += c * (b if c >= 0 else a)
    return low, high


def add(*profiles):
    result = Counter()
    for profile in profiles:
        for r, c in profile.items():
            result[r] += c
    return {r: c for r, c in result.items() if c}


def mul(c, profile):
    return {r: c * v for r, v in profile.items()}


def bill(word):
    return dict(Counter(abs(len(word["frames"][op[2]]) - len(word["frames"][op[3]]))
                        for op in word["program"] if op[0] == "MOVE"))


def clean(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


def span(rows):
    values = {0}
    for r in rows:
        values |= {x ^ r for x in values}
    return values


def rank(rows):
    pivots = {}
    for raw in rows:
        row = list(raw)
        for p, old in sorted(pivots.items()):
            if row[p]:
                scale = row[p]
                row = [x - scale*y for x, y in zip(row, old)]
        p = next((i for i, x in enumerate(row) if x), None)
        if p is not None:
            scale = row[p]
            pivots[p] = [x/scale for x in row]
    return len(pivots)


def main(args):
    for path, pin in DEPENDENCIES.items():
        read(args.repo / path, pin)
    source = json.loads(gzip.decompress(read(
        args.repo / "research/shared-wire-split-composition/data/final.json.gz", SOURCE)))
    full = json.loads(read(
        args.repo / "research/shared-wire-split-composition/FULL-RESULT.json", FULL))
    parent = json.loads(gzip.decompress(read(HERE / "source-evidence/rail-consumer.json.gz", PARENT)))
    four = json.loads(gzip.decompress(read(HERE / "source-evidence/rail-cross-four.json.gz", FOUR)))
    q, q4 = bill(parent), bill(four)
    ferry = {1: 16, 7: 8, 9: -8}
    need(add(q4, mul(-1, q)) == ferry, "Actual frozen four-ferry debit")
    need(sum(r*c for r, c in ferry.items()) == 0, "Ferries do not lower rank mass")
    need(len(parent["consumer"]["selected_return_ports"]) == 31, "Old coordinate-return count")
    extract_path = HERE / "source-evidence/extract_rail.py"
    read(extract_path, EXTRACT)
    spec = importlib.util.spec_from_file_location("stream_cost_source_corroboration", extract_path)
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    host = {source["live"][k]: (x, y) for k, x, y in zip(
        source["hosted"]["Dports"], source["hosted"]["X2"], source["hosted"]["Y2"])}
    roles = {int(k): v for k, v in parent["source_role_map"].items()}
    stripped_receipts = {}
    stripped_rows = {}
    for label, word, expected_rank in [("parent_without31", parent, 82),
                                       ("four_ferries_without31", four, 82)]:
        if label == "parent_without31":
            ops = word["program"][:parent["consumer"]["begin"]]
        else:
            need(len(word["parent_event_of_output"]) == len(word["program"]), "Literal old-event itinerary")
            ops = [op for op, old in zip(word["program"], word["parent_event_of_output"])
                   if old is None or old < parent["consumer"]["begin"]]
        rows, loc, ordinary = engine.run(
            ops, word["initial"], 400, word["owned_fields"],
            list(map(engine.span, word["frames"])), {i: {i: F(1)} for i in range(400)})
        matrix = [[rows[roles[host[h][0]]].get(roles[host[j][1]], F(0)) + F(h == j)
                   for j in host] for h in host]
        actual_rank = rank(matrix)
        need(actual_rank == expected_rank,
             f"Deleting paid observations restores their source debt: {label} rank {actual_rank}")
        need(sum(ordinary["moves"].values()) == sum(q.values()) - 31 + (16 if label.startswith("four") else 0),
             "Literal deletion agrees with cost skeleton")
        stripped_receipts[label] = {"reverse_rank": actual_rank, "ordinary_bill": ordinary,
                                    "residual_matrix_sha256": hashlib.sha256(
                                        json.dumps(clean(matrix), separators=(",", ":")).encode()).hexdigest(),
                                    "complete_source": False}
        stripped_rows[label] = rows
    expected = {i: dict(row) for i, row in stripped_rows["parent_without31"].items()}
    for i, j, coefficient in [(1, 106, -1), (2, 4, 1), (11, 15, 1), (23, 24, 1)]:
        for target, donor in [(i, j), (j, i)]:
            row = expected[roles[host[target][0]]]
            key = roles[host[donor][1]]
            row[key] = row.get(key, F(0)) + coefficient
            if not row[key]:
                del row[key]
    need(expected == stripped_rows["four_ferries_without31"], "All400 stripped outputs and exact eight B changes")

    T, P = [{int(k): v for k, v in full["invoice"][key].items()} for key in ("T", "P")]
    H, N = [{int(k): v for k, v in full["native"][key].items()} for key in ("helpers", "paid")]
    slope = mul(F(1, 18), add(T, mul(-1, P)))
    d = moment(mul(-1, slope))
    need(d[0] > 0, "Strict selected-caller deficit")
    # All paid parent terms stay charged except the explicitly removed 31 returns.
    limit_parent = add(slope, N, mul(-1, H), mul(-1, q))
    envelope_q = add(q, {1: -31, 7: 8})
    envelope_four = add(envelope_q, ferry)
    variants = {}
    for label, candidate, expected in [
        ("no_ferry_debit", envelope_q, 21),
        ("retain_actual_four_ferries", envelope_four, 24),
    ]:
        need(all(c >= 0 for c in candidate.values()), "Nonnegative hypothetical Q profile")
        limit = add(slope, N, mul(-1, H), mul(-1, candidate))
        limit_bounds = moment(limit)
        need(limit_bounds[0] > 0, "Positive limiting envelope")
        threshold = (d[0] / limit_bounds[1], d[1] / limit_bounds[0])
        need(expected - 2 < threshold[0] <= threshold[1] < expected - 1,
             "Exact adjacent integer threshold")
        rows = []
        for m in [2, 3, expected - 1, expected, 32, 64]:
            target = add(mul(m, T), mul(-18*(m-1), H))
            paid = add(mul(m, P), mul(-18*(m-1), N), mul(18*(m-1), candidate))
            need(all(c >= 0 for c in target.values()) and all(c >= 0 for c in paid.values()),
                 "Whole conditional caller profiles nonnegative")
            signed = mul(F(1, 18*(m-1)), add(target, mul(-1, paid)))
            need(signed == add(limit, mul(F(1, m-1), slope)), "Whole invoice identity")
            bounds = moment(signed)
            if m == expected - 1:
                need(bounds[1] < 0, "Previous fixed m strictly fails")
            if m == expected:
                need(bounds[0] > 0, "First fixed m strictly passes this envelope")
            rows.append({"fixed_copies": m, "normalized_moment_bounds": bounds,
                         "display": float(bounds[0]),
                         "target_profile": target, "paid_profile": paid})
        variants[label] = {"hypothetical_Q_profile": candidate,
                           "limiting_room_bounds": limit_bounds,
                           "limiting_room_display": float(limit_bounds[0]),
                           "threshold_d_over_room_bounds": threshold,
                           "least_fixed_m_for_strict_positive_envelope": expected,
                           "finite_rows": rows}

    # This is an inherited census, independently recomputed for the local warning.
    hosted = sorted(source["live"][k] for k in source["hosted"]["Dports"])
    normals = {h: source["frames"][source["initial"][h]][0] for h in hosted}
    d_roles = {source["live"][k]: d for k, d in
               zip(source["hosted"]["Dports"], source["hosted"]["Y2"])}
    for h in hosted:
        need(normals[h].bit_count() % 2 == 1, "Odd source normal")
        need(span(source["frames"][source["final"][d_roles[h]]]) ==
             {v for v in range(512) if not ((v & normals[h]).bit_count() % 2)},
             "Actual original D polar facet")
    masks = {v: sum(1 << k for k, h in enumerate(hosted)
                    if not ((v & normals[h]).bit_count() % 2)) for v in range(1, 512)}
    histogram = Counter()
    joint = Counter()
    witness = None
    positive_b_max = {}
    for a in range(1, 512):
        for b in range(a + 1, 512):
            c = a ^ b
            if b >= c:
                continue
            dmask = masks[a] & masks[b]
            bmask = sum(1 << k for k, h in enumerate(hosted) if normals[h] in (a, b, c))
            need(not (bmask & dmask), "Clean B and D supports disjoint")
            db, bb = dmask.bit_count(), bmask.bit_count()
            histogram[db] += 1
            joint[bb, db] += 1
            positive_b_max[bb] = max(positive_b_max.get(bb, 0), db)
            if witness is None or bb + db > witness["combined_support"]:
                witness = {"chart_nonzero_vectors": [a, b, c], "clean_B": bb,
                           "clean_D": db, "combined_support": bb + db}
    reviewed = json.loads((args.repo /
        "research/moonshot-005-program/results/nine-packet-no-line-gate/review-root/RESULT.json").read_text())
    old2 = reviewed["chart_census"]["2"]
    need(sum(histogram.values()) == old2["count"] == 43435, "Inherited all-C2 count")
    need(dict(histogram) == {int(k): v for k, v in old2["support_count_histogram"].items()},
         "Exact inherited D-population histogram")
    need(witness["combined_support"] == max(histogram) == 35, "Inherited clean support cap corollary")

    controls = {}
    for label, replacement in [("keep_old31_returns", {7: 8}),
                               ("rank8_returns_instead_of_rank7", {1: -31, 8: 8})]:
        candidate = add(q, replacement)
        bounds = moment(add(slope, N, mul(-1, H), mul(-1, candidate)))
        need(bounds[1] < 0, "Negative budget control")
        controls[label] = {"limiting_room_bounds": bounds, "strictly_negative": True}

    result = {
        "status": "PASS_CONDITIONAL_ARITHMETIC_AND_INHERITED_GEOMETRY_RECEIPTS_ONLY",
        "construction_status": "UNVERIFIED_WIP_NO_COMPATIBLE_RANK8_SOURCE_OR_STREAM_WORD",
        "native_sha256": SOURCE, "complete_caller_sha256": FULL,
        "parent_rail_sha256": PARENT, "actual_four_ferry_word_sha256": FOUR,
        "source_corroboration_engine_sha256": EXTRACT,
        "literal_source_after_deleting_old31_returns": stripped_receipts,
        "stripped_four_retains_only_the_same_eight_B_changes": True,
        "deleting_old31_does_not_preserve_rank54_or_its_four_row_dependencies": True,
        "inherited_dependencies": DEPENDENCIES,
        "whole_invoice_formulas": {
            "T_m": "m*T-18*(m-1)*H",
            "P_m": "m*P-18*(m-1)*N+18*(m-1)*Q_hypothetical",
            "normalized_margin": "L-d/(m-1), normalized by18*(m-1)",
        },
        "selected_caller_deficit_d_bounds": d,
        "parent_limiting_allowance_bounds": moment(limit_parent),
        "old31_returns_removed": 31, "new_rank7_calls": 8,
        "limiting_allowance_after_removing_old31_bounds": moment(add(limit_parent, {1: 31})),
        "eight_rank7_price_bounds": moment({7: 8}),
        "actual_four_ferry_debit_profile": ferry,
        "actual_four_ferry_debit_bounds": moment(ferry),
        "variants": variants,
        "clean_chart_corroboration": {
            "not_new_geometry": True, "all_binary2planes": 43435,
            "D_histogram_equals_inherited_root_review": True,
            "maximum_D_population_by_clean_B_population": positive_b_max,
            "maximum_combined_B_D_support": 35, "maximum_witness": witness,
            "Gram_distance42_inherited": True,
            "minimum_extra_distinct_hosted_positions_in_P_plus_Q_under_hypothetical_G_minus_I": 7,
            "no_universal_message_or_MOVEs_lower_bound_from_this_seven": True,
        },
        "controls": controls,
        "all_source_and_forward_costs_still_owed": True,
        "no_growing_m": True,
        "scope": "Finite fixed-m moment feasibility for an explicitly hypothetical paid profile. Actual rank54 is not rank8. No C2 innovation, streaming decoder, full forward completion, lifetime schedule or supplier is provided. Additional acquisition/refinement/endpoint work must fit the strict remaining room and may invalidate the envelope. The clean-source Gram warning assumes actual Hub graph G-I; it grants no such source.",
    }
    args.output.write_text(json.dumps(clean(result), sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "least_fixed_m_without_ferry_debit": 21,
                      "least_fixed_m_with_four_ferry_debit": 24,
                      "clean_source_support_bound_is_inherited": True}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "BUDGET.json")
    main(parser.parse_args())
