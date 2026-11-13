#!/usr/bin/env python3
"""Exact arithmetic review of source-bound supplier requirements at kappa .004.

This independently checks thresholds and the published complete BIT histogram.
It does not replay native words, construct a provider, or admit new suppliers.
Run from any directory: python3 -I -B verify.py
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = "3fb13f8072e0d8b2ff9cead7754533cf95fe5079f144857e558da719d3a533f0"
PROGRAMME_SHA = "8533bc2640e0ec002bb16ba85997480ce3c3cac6"
CANONICAL_SHA = "e54523517d0f03e58352e647c403a5af3e525a57"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ratio(value):
    return str(value)


def stage_supremum(covered, previous):
    return covered / (1 + covered - previous)


def covered_threshold(target, previous):
    return target * (1 - previous) / (1 - target)


def power_interval(rank, numerator, denominator, grid):
    """Certified bounds on rank**(numerator/denominator)."""
    target = rank ** numerator * grid ** denominator
    lower, upper = 0, rank * grid + 1
    while upper - lower > 1:
        middle = (lower + upper) // 2
        if middle ** denominator <= target:
            lower = middle
        else:
            upper = middle
    exact = lower ** denominator == target
    high = lower if exact else lower + 1
    require(lower ** denominator <= target, "Bad lower power bound")
    require(exact or high ** denominator > target, "Bad upper power bound")
    return lower, high


def main():
    raw = (HERE / "SOURCE-BIT-RESULT.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256,
            "Changed published histogram fixture")
    source = json.loads(raw)

    b0 = F(12039, 3125000)
    c_selected = F(19262649, 5000000000)
    uniform_complex = F(181502908503, 50000000000000)
    rho = F(1, 250)
    selected_kappa = F(363005817, 100000000000)
    require(0 < uniform_complex < b0 < c_selected < rho < F(1, 2),
            "Selected supplier order mismatch")
    require(selected_kappa < uniform_complex, "Lost selected complex slack")

    thresholds = {}
    for target, expected in [
        (F(1, 250), F(3112961, 778125000)),
        (F(401, 100000), F(1248297361, 311246875000)),
    ]:
        threshold = covered_threshold(target, b0)
        require(threshold == expected, "Covered threshold mismatch")
        require(stage_supremum(threshold, b0) == target,
                "Equality is the unattained supremum")
        eps = F(1, 10**12)
        require(stage_supremum(threshold - eps, b0) < target,
                "Below-threshold negative control")
        require(stage_supremum(threshold + eps, b0) > target,
                "Above-threshold positive control")
        thresholds[ratio(target)] = {
            "covered_must_be_strictly_greater_than": ratio(threshold),
            "equality_supremum_only": True,
            "exact_threshold_controls": "PASS",
        }

    current_supremum = stage_supremum(c_selected, b0)
    require(b0 < current_supremum < c_selected < F(1, 250),
            "Current wrapper cannot reach .004")
    # The general proof gives every finite iterate below C. The checks above
    # corroborate this exact selected one-stage instance, not an induction proof.

    paid = {int(k): v for k, v in source["paid"].items()}
    targets = {int(k): v for k, v in source["targets"].items()}
    require(sum(paid.values()) == 107352, "Paid job count")
    require(sum(targets.values()) == 19950, "Target count")
    require(source["actual_queries"] == 4
            and source["jobs_per_query"] == 111, "QUERY inventory")
    grid = 2**64
    lower = upper = 0
    powers = {}
    for rank in sorted(set(paid) | set(targets)):
        lo, hi = power_interval(rank, 249, 250, grid)
        powers[str(rank)] = [str(lo), str(hi)]
        coefficient = targets.get(rank, 0) - paid.get(rank, 0)
        if coefficient >= 0:
            lower += coefficient * lo
            upper += coefficient * hi
        else:
            lower += coefficient * hi
            upper += coefficient * lo
    require(lower == -1054813698952914390024, "Moment lower mismatch")
    require(upper == -1054813698952914315006, "Moment upper mismatch")
    require(upper + 57 * grid < 0, "57-credit negative control")
    require(lower + 58 * grid > 0, "58-credit positive control")
    require(lower + (111 - 36) * grid > 0,
            "One free QUERY less 36 added jobs passes raw gate")
    require(upper + (111 - 54) * grid < 0,
            "One free QUERY less 54 added jobs fails raw gate")

    # Explicitly hypothetical supplier target, not a constructed algorithm.
    c_hyp = F(403, 100000)
    rho_hyp = F(101, 25000)
    b_hyp = F(201, 50000)
    u_hyp = F(41, 10000)
    k_hyp = F(401, 100000)
    a_wrapper = (1 - rho_hyp) * c_hyp + rho_hyp * b0
    require(b0 < b_hyp < a_wrapper < rho_hyp < 1 - a_wrapper,
            "Hypothetical full strict BIT interface")
    require(a_wrapper == F(1259150881, 312500000000),
            "Hypothetical exact A")
    m_outer = min(u_hyp, b_hyp, F(1, 32))
    d_outer = (m_outer - k_hyp) / 7
    family = {
        "q": k_hyp + 3 * d_outer,
        "a": k_hyp + 4 * d_outer,
        "b": k_hyp + 5 * d_outer,
        "epsilon": 1 - d_outer,
        "beta": 1 - 3 * d_outer,
        "r0": d_outer / 10,
        "stop": d_outer,
        "layout": d_outer,
    }
    old = F("0.001730970419199163702738")
    require(old < k_hyp < m_outer and d_outer == F(1, 700000),
            "Exact outer feasibility and family gap")
    require(k_hyp < family["q"] < family["a"] < family["b"]
            < m_outer and family["epsilon"] * family["q"] > k_hyp,
            "Outer family ordering and main-transform margin")
    hypothetical = {
        "status": "TARGET_SPECIFICATION_ONLY_NO_SUPPLIERS_CONSTRUCTED",
        "kappa": ratio(k_hyp),
        "covered_C": ratio(c_hyp),
        "atom_rho": ratio(rho_hyp),
        "ordinary_B": ratio(b_hyp),
        "uniform_complex_U": ratio(u_hyp),
        "A": ratio(a_wrapper),
        "strict_BIT_gaps": {
            "B_minus_b0": ratio(b_hyp - b0),
            "A_minus_B": ratio(a_wrapper - b_hyp),
            "rho_minus_A": ratio(rho_hyp - a_wrapper),
            "one_minus_A_minus_rho": ratio(1 - a_wrapper - rho_hyp),
        },
        "outer_M": ratio(m_outer),
        "outer_d": ratio(d_outer),
        "outer_family": {key: ratio(value) for key, value in family.items()},
        "outer_validation_scope": "Exact feasibility region and sufficient family by prior proved outer-region theorem. Not a fresh replay of all 58 source expressions.",
    }

    result = {
        "status": "PASS_EXACT_004_SUPPLIER_REQUIREMENTS_AND_RAW_BIT_BUDGET",
        "complete_new_kappa": None,
        "programme_sha": PROGRAMME_SHA,
        "canonical_sha": CANONICAL_SHA,
        "source_fixture_sha256": SOURCE_SHA256,
        "source_path": "research/moonshot-005-program/results/bit-query-budget/RESULT.json",
        "selected": {
            "kappa": ratio(selected_kappa),
            "uniform_complex_U": ratio(uniform_complex),
            "completed_ordinary_BIT_b0": ratio(b0),
            "covered_BIT_C": ratio(c_selected),
            "frozen_atom_rho": ratio(rho),
            "one_stage_supremum_unattained": ratio(current_supremum),
        },
        "one_stage_target_requirements": thresholds,
        "frozen_rho_ceiling": "Strict B < rho = 1/250; follows from retained root term and strict interface.",
        "power_exponent": "249/250",
        "grid_denominator": str(grid),
        "margin_numerators": [str(lower), str(upper)],
        "minimum_integer_rank_one_net_credit": 58,
        "one_free_QUERY_margin_numerators": [
            str(lower + 111 * grid), str(upper + 111 * grid)
        ],
        "controls": {
            "published_fixture_hash_checked": True,
            "threshold_equality_not_attained": True,
            "57_net_credits_fail": True,
            "58_net_credits_pass_raw_only": True,
            "QUERY_credit_less_36_added_passes_raw_only": True,
            "QUERY_credit_less_54_added_fails": True,
        },
        "rank_power_interval_numerators": powers,
        "hypothetical_00401_assembly": hypothetical,
        "scope": "Published histogram arithmetic and exact wrapper thresholds only. No source-word replay, physical provider, new covered/ordinary/complex supplier, or complete multiplication theorem.",
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "RESULT.json").write_text(output, encoding="utf-8")
    print(result["status"])


if __name__ == "__main__":
    main()
