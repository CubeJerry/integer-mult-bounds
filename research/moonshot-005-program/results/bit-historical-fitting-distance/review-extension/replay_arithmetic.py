#!/usr/bin/env python3
"""Independent closed-form audit of the scalar patch-distance extension."""
import argparse
import json
from collections import Counter
from pathlib import Path


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior-review", type=Path, required=True)
    ap.add_argument("--root-package", type=Path, required=True)
    ap.add_argument("--q8-budget", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    prior = json.loads((a.prior_review / "RESULT.json").read_text())
    root = json.loads((a.root_package / "RESULT.json").read_text())
    q8 = json.loads((a.q8_budget / "RESULT.json").read_text())

    support_hist = {int(k): int(v) for k, v in prior["foreign_support_histogram"].items()}
    need(support_hist == {55: 1, 56: 11, 57: 16, 58: 36, 59: 28, 60: 13, 61: 5, 62: 1},
         "prior exact source support histogram changed")
    margins = []
    for support, multiplicity in support_hist.items():
        margins.extend([support - 52] * multiplicity)
    margins.sort()
    need(len(margins) == 111 and min(margins) == 3 and max(margins) == 10,
         "first-marginal range/count")
    need(sum(margins) == 698, "sum of first marginal costs")
    second_marginals = [x + 16 for x in margins]
    need(min(second_marginals) == 19 and min(second_marginals) > max(margins),
         "all first marginals should be cheaper than every second marginal")

    scenarios = [(9, 0), (9, 11), (8, 0), (8, 1), (8, 3)]
    out_cases = []
    for q, e in scenarios:
        saves = 111 - q - e
        need(0 <= saves <= 111, f"invalid saving count {q,e}")
        distance = sum(margins[:saves])
        out_cases.append({"q": q, "extra_arrivals": e, "required_saved_visits": saves,
                          "minimum_changed_entries": distance,
                          "support_valid_rankone_terms_at_area_144": (distance + 143) // 144})

    # Universal ADE/E8 root-flat maxima from the admitted low-rank proof.
    N = {1: 1, 2: 3, 3: 6, 4: 12, 5: 20, 6: 36, 7: 111}
    areas = {(r, s): N[r] * N[s] for r in N for s in N if r + s <= 8}
    max_area = max(areas.values())
    maximizing = [list(pair) for pair, area in sorted(areas.items()) if area == max_area]
    need(max_area == 144 and maximizing == [[4, 4]], "orthogonality rectangle area maximum")
    need(111 * 1 == 111 < 144, "rank-seven trivial bound must remain below max")

    root_cases = {(c["q"], c["extra_arrivals"]): c for c in root["cases"]}
    for c in out_cases:
        rc = root_cases[(c["q"], c["extra_arrivals"])]
        need(c["minimum_changed_entries"] == rc["distance"],
             f"root closed-form receipt mismatch for {(c['q'], c['extra_arrivals'])}")
    m6_extra = q8["m6_affordable_extra_unit_calls"]
    q8_extra_limit = q8["all_finite_m_affordable_extra_unit_calls_at_most"]
    need(q8["status"] == "PASS_EXACT_CONDITIONAL_Q8_UNIT_PATH_TARGET_BUDGET" and
         q8["minimum_q8_unit_path_calls"] == 1618 and q8_extra_limit == 3 and m6_extra == 1,
         "q8 movement extra-arrival allowance changed")
    need(out_cases[4]["minimum_changed_entries"] == 603 and out_cases[4]["support_valid_rankone_terms_at_area_144"] == 5,
         "q8 limiting five-patch conclusion")
    need(out_cases[3]["minimum_changed_entries"] == 619 and out_cases[3]["support_valid_rankone_terms_at_area_144"] == 5,
         "q8 m=6 five-patch conclusion")

    result = {
        "status": "PASS_INDEPENDENT_CLOSED_FORM_PATCH_DISTANCE_EXTENSION",
        "source_histogram_reference": prior["foreign_support_histogram"],
        "first_marginal_cost_histogram": dict(sorted(Counter(margins).items())),
        "second_marginal_cost": 16,
        "max_first_marginal": max(margins),
        "closed_form_cases": out_cases,
        "root_line_counts_by_flat_rank": N,
        "orthogonality_rectangle_max_area": max_area,
        "maximizing_rank_pair": maximizing,
        "movement_allowances": {"q8_limit_all_finite_m": q8_extra_limit,
                                "q8_fixed_m6": m6_extra},
        "scope": "Scalar fitting matrices and sums of individually fitting-preserving rank-one terms only; no unrestricted rank-two decomposition or rank-ten classification.",
    }
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "closed_form_cases": out_cases,
                      "rectangle_max_area": max_area, "allowances": result["movement_allowances"]}, indent=2))


if __name__ == "__main__":
    main()
