#!/usr/bin/env python3
"""Independent directed arithmetic review of BIT reversal-rank budgets."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def power(rank, bits=192):
    den = 1 << bits
    target = rank ** 199 * den ** 200
    lo, hi = 0, rank * den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, ("directed 200th root", rank))
    up = lo if lo ** 200 == target else lo + 1
    return F(lo, den), F(up, den)


def price(profile, powers):
    lo = hi = F(0)
    for r, c in profile.items():
        a, b = powers[r]
        if c >= 0:
            lo += c * a
            hi += c * b
        else:
            lo += c * b
            hi += c * a
    return lo, hi


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[1], a[1] - b[0]


def mul_int(k, p):
    return (k * p[0], k * p[1]) if k >= 0 else (k * p[1], k * p[0])


def fmt(pair):
    return {"lower": str(pair[0]), "upper": str(pair[1])}


def main(args):
    repo = args.repo
    if (repo / "programme/research").exists():
        repo = repo / "programme"
    budget_path = repo / "research/moonshot-005-program/results/bit-rank-nine-shared-interface/BUDGET.json"
    raw = budget_path.read_bytes()
    budget = json.loads(raw)
    lim0 = budget["at_t_199_over_200"]["limiting_Q_allowance"]
    ceiling = (F(lim0["exact_lower"]), F(lim0["exact_upper"]))
    powers = {r: power(r) for r in range(1, 9)}
    factor = (powers[8][0] / 8, powers[8][1] / 8)  # 8^(t-1)=8^(-1/200)
    need(all(powers[r][0] > r * factor[1] for r in range(1, 8)), "rank-price lower envelope")
    need(powers[8][0] == 8 * factor[0] and powers[8][1] == 8 * factor[1], "rank-8 baseline identity")

    clean_profile = {1: 289, 2: 244, 7: 111, 8: 9}
    clean_base = price(clean_profile, powers)
    clean_room = sub(ceiling, clean_base)
    clean_u2 = add(clean_base, mul_int(4, factor))
    clean_u3 = add(clean_base, mul_int(6, factor))
    need(clean_u2[1] < ceiling[0], "fixed clean caller U=2 remains below limiting ceiling")
    need(clean_u3[0] > ceiling[1], "fixed clean caller U=3 exceeds limiting ceiling")

    monotone_profile = {7: 222, 8: 9}
    monotone_base = price(monotone_profile, powers)
    mono_u5 = add(monotone_base, mul_int(10, factor))
    mono_u6 = add(monotone_base, mul_int(12, factor))
    need(mono_u5[1] < ceiling[0], "optimistic monotone-X/Y U=5 remains below limit")
    need(mono_u6[0] > ceiling[1], "optimistic monotone-X/Y U=6 exceeds limit")

    # X and Y endpoint nets are each +7 per field; packet endpoint nets are
    # -8 per packet. If R sums every X/Y downward rank plus packet upward rank,
    # total MOVE rank is at least 111*7+111*7+9*8+2R=1626+2R.
    direct_rank_base = (F(1626) * factor[0], F(1626) * factor[1])
    all_r6 = add(direct_rank_base, mul_int(12, factor))
    all_r7 = add(direct_rank_base, mul_int(14, factor))
    need(all_r6[1] < ceiling[0], "optimistic R=6 remains below limit")
    need(all_r7[0] > ceiling[1], "optimistic R=7 exceeds limit")

    local102 = add(monotone_base, (F(102), F(102)))
    local102_deficit = sub(local102, ceiling)
    need(local102_deficit[0] > F("90.45799327294747"), "conditional 102 rank-one arrival deficit")

    root_path = Path("root-work/BIT-REVERSAL-BUDGET.json")
    root = json.loads(root_path.read_text())
    need(root["caller_sha256"] == sha(raw), "root result references same exact limiting caller")
    expected = {
        "clean_fixed_U": 2,
        "arbitrary_monotone_XY_U": 5,
        "all_original_reverse_rank_R": 6,
    }
    observed = {
        "clean_fixed_U": root["fixed_clean_X_minimum_Y_packet_upward_rank"]["necessary_integer_upper"],
        "arbitrary_monotone_XY_U": root["arbitrary_monotone_XY_packet_upward_rank"]["necessary_integer_upper"],
        "all_original_reverse_rank_R": root["all_original_records_total_reverse_rank"]["necessary_integer_upper"],
    }
    need(observed == expected, ("root integer thresholds", observed))

    out = {
        "status": "PASS_INDEPENDENT_EXACT_BIT_REVERSAL_BUDGET_ARITHMETIC",
        "caller_budget_sha256": sha(raw),
        "root_result_sha256": sha(root_path.read_bytes()),
        "t": "199/200",
        "rank_power_intervals": {str(r): fmt(powers[r]) for r in range(1, 9)},
        "per_total_MOVE_rank_factor": fmt(factor),
        "limiting_Q_ceiling": fmt(ceiling),
        "fixed_clean_profile": clean_profile,
        "fixed_clean_direct_base": fmt(clean_base),
        "fixed_clean_remaining_room": fmt(clean_room),
        "fixed_clean_U2_lower_bound": fmt(clean_u2),
        "fixed_clean_U3_lower_bound": fmt(clean_u3),
        "fixed_clean_U3_deficit": fmt(sub(clean_u3, ceiling)),
        "monotone_XY_direct_profile": monotone_profile,
        "monotone_XY_U5_lower_bound": fmt(mono_u5),
        "monotone_XY_U6_lower_bound": fmt(mono_u6),
        "monotone_XY_U6_deficit": fmt(sub(mono_u6, ceiling)),
        "all_original_telescoping": {
            "identity": "total MOVE rank >= 1626+2R; R = X/Y downward rank + packet upward rank",
            "R6_lower_bound": fmt(all_r6),
            "R7_lower_bound": fmt(all_r7),
            "R7_deficit": fmt(sub(all_r7, ceiling)),
        },
        "conditional_102_local_arrival_deficit": fmt(local102_deficit),
        "independent_derivation": "For every integer MOVE rank q in1..8, q^(199/200)/q is decreasing in q, so q^(199/200)>=q*8^(-1/200). Endpoint path variation telescopes; the additional movement ranks are 2U or2R.",
        "scope": "Directed arithmetic only. The 102-arrival count is conditional on its separate event-accounting premise. The U limits are optimistic necessary movement bounds, not constructions or an architecture-wide no-go.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in (
        "status", "fixed_clean_U2_lower_bound", "fixed_clean_U3_deficit",
        "monotone_XY_U6_deficit", "all_original_telescoping", "conditional_102_local_arrival_deficit")}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    main(p.parse_args())
