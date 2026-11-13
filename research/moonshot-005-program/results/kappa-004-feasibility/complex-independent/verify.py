#!/usr/bin/env python3
"""Independent exact arithmetic for the S010 kappa > .004 assessment.

This does not replay a source word or admit a supplier. With --repo, it also
authenticates the selected full-caller JSON against its inherited source pin.
Every reported power interval is proved by integer exponent comparisons.
Floating point is used only to propose an initial integer root candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

DEN = 1 << 42
HERE = Path(__file__).resolve().parent


def combine(*terms: tuple[int, dict[str, int]]) -> dict[int, int]:
    answer: dict[int, int] = {}
    for scale, profile in terms:
        for rank, multiplicity in profile.items():
            r = int(rank)
            answer[r] = answer.get(r, 0) + scale * multiplicity
    return {r: n for r, n in answer.items() if n}


def power_bounds(ranks: set[int], p: int, q: int) -> dict[int, tuple[int, int]]:
    answer = {}
    scale_power = pow(DEN, q)
    for rank in sorted(ranks):
        if rank == 1:
            answer[rank] = (DEN, DEN)
            continue
        target = pow(rank, p) * scale_power
        z = int(math.floor(rank ** (p / q) * DEN))
        while pow(z, q) > target:
            z -= 1
        while pow(z + 1, q) <= target:
            z += 1
        if not (pow(z, q) <= target < pow(z + 1, q)):
            raise ArithmeticError("Unproved integer root bound")
        answer[rank] = (z, z + 1)
    return answer


def evaluate(profile, bounds, divisor=1):
    lo = hi = 0
    for rank, coefficient in profile.items():
        low, high = bounds[int(rank)]
        if coefficient >= 0:
            lo += coefficient * low
            hi += coefficient * high
        else:
            lo += coefficient * high
            hi += coefficient * low
    return lo, hi, DEN * divisor


def receipt(interval):
    lo, hi, denominator = interval
    with localcontext() as context:
        context.prec = 40
        decimal_interval = [
            str(Decimal(lo) / denominator),
            str(Decimal(hi) / denominator),
        ]
    return {
        "lower_numerator": str(lo),
        "upper_numerator": str(hi),
        "denominator": str(denominator),
        "decimal_interval_illustrative": decimal_interval,
    }


def finite_minimum(d18, surplus18):
    dlo, dhi, _ = d18
    slo, shi, _ = surplus18
    if shi <= 0:
        return None
    if slo <= 0 or dlo <= 0:
        raise ArithmeticError("Minimum multiplicity cannot be certified")
    ratio_lo = Fraction(dlo, shi)
    ratio_hi = Fraction(dhi, slo)
    floor_lo = ratio_lo.numerator // ratio_lo.denominator
    floor_hi = ratio_hi.numerator // ratio_hi.denominator
    if floor_lo != floor_hi:
        raise ArithmeticError("Need narrower integer-root bounds")
    return floor_lo + 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--caller-source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_bytes = (HERE / "INPUT.json").read_bytes()
    data = json.loads(source_bytes)
    profiles = data["profiles"]
    source_authenticated = False
    caller_path = args.caller_source
    if args.repo:
        caller_path = args.repo / data["caller_source"]
    if caller_path is None and (HERE / "inputs" / "FULL-RESULT.json").exists():
        caller_path = HERE / "inputs" / "FULL-RESULT.json"
    if caller_path is not None:
        raw = caller_path.read_bytes()
        actual_hash = hashlib.sha256(raw).hexdigest()
        if actual_hash != data["caller_source_sha256"]:
            raise ValueError("Caller bytes do not match the inherited source pin")
        full = json.loads(raw)
        actual_profiles = {
            "T": full["invoice"]["T"],
            "P": full["invoice"]["P"],
            "N": full["native"]["paid"],
            "H": full["native"]["helpers"],
        }
        for key, value in actual_profiles.items():
            if value != profiles[key]:
                raise ValueError(f"Caller profile mismatch: {key}")
        source_authenticated = True
    T, P, N, H = (profiles[key] for key in ("T", "P", "N", "H"))
    a18 = combine((18, N), (-18, H), (1, T), (-1, P))
    d18 = combine((1, P), (-1, T))
    ranks = {int(r) for profile in profiles.values() for r in profile}
    result = {
        "classification": "Exact recursive-invoice arithmetic; no new kappa",
        "programme_head": data["programme_head"],
        "input_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_byte_pin_authenticated": source_authenticated,
        "scale": str(DEN),
        "theorem": (
            "For every fixed integer m>=2, if Q is an admitted complete rail, "
            "(T_m-P_m)_t = 18(m-1)(A(t)-Q_t)-18d(t), where "
            "A=(N-H)_t+(T-P)_t/18 and d=(P-T)_t/18. "
            "Partial/relaxed profiles do not discharge the premise."
        ),
        "targets": [],
    }
    for p, q, witness_m in [(249, 250, 2), (9959, 10000, 3), (1991, 2000, 6)]:
        bounds = power_bounds(ranks, p, q)
        d_interval = evaluate(d18, bounds, 18)
        if d_interval[0] <= 0:
            raise ArithmeticError("Positive fixed-m penalty not established")
        actual_surplus = combine(
            (1, a18), (-18, profiles["Q_actual"])
        )
        terminal_deficit = combine(
            (1728, {1: 1}), (-1, actual_surplus)
        )
        terminal_interval = evaluate(terminal_deficit, bounds, 18)
        if terminal_interval[0] <= 0:
            raise ArithmeticError("Current-Q terminal obstruction not established")
        proposed_deficit = combine(
            (18, profiles["Q_proposed_completion"]), (-1, a18)
        )
        proposed_interval = evaluate(proposed_deficit, bounds, 18)
        if proposed_interval[0] <= 0:
            raise ArithmeticError("Proposed completion price failure not established")
        target = {
            "kappa": str(Fraction(q - p, q)),
            "t": str(Fraction(p, q)),
            "d": receipt(d_interval),
            "allowance_infinity": receipt(evaluate(a18, bounds, 18)),
            "actual_Q_additional_room_infinity": receipt(
                evaluate(actual_surplus, bounds, 18)
            ),
            "current_Q_terminal_96_deficit_infinity": receipt(terminal_interval),
            "proposed_completion_deficit_infinity": receipt(proposed_interval),
            "relaxations": {},
            "integer_power_bounds": {
                str(r): [str(lo), str(hi)]
                for r, (lo, hi) in sorted(bounds.items())
            },
        }
        for name in (
            "Q_fresh_eight_relaxation",
            "Q_eight_zero_born_relaxation",
            "Q_nine_A2_relaxation",
        ):
            candidate = profiles[name]
            surplus18 = evaluate(
                combine((1, a18), (-18, candidate)), bounds
            )
            least_m = finite_minimum(evaluate(d18, bounds), surplus18)
            candidate_result = {
                "limiting_surplus_per_rail": receipt(
                    (surplus18[0], surplus18[1], 18 * surplus18[2])
                ),
                "least_fixed_m_for_relaxed_moment": least_m,
            }
            if least_m:
                m = least_m
                finite_profile = combine(
                    (18 * (m - 1), N),
                    (-18 * (m - 1), H),
                    (m, T),
                    (-m, P),
                    (-18 * (m - 1), candidate),
                )
                total = evaluate(finite_profile, bounds)
                if total[0] <= 0:
                    raise ArithmeticError("Finite-m witness was not positive")
                candidate_result["finite_m_signed_caller_moment"] = receipt(total)
                candidate_result["finite_m_surplus_per_rail"] = receipt(
                    (total[0], total[1], total[2] * 18 * (m - 1))
                )
            target["relaxations"][name] = candidate_result
        if target["relaxations"]["Q_fresh_eight_relaxation"][
            "least_fixed_m_for_relaxed_moment"
        ] != witness_m:
            raise ArithmeticError("Fresh-eight expected witness changed")

        # Negative control: re-crediting all shared helper targets turns a
        # correctly negative current-Q+96 invoice into a false positive.
        false_overcredit = combine(
            (1, a18), (18, H), (-18, profiles["Q_actual"]), (-1728, {1: 1})
        )
        false_interval = evaluate(false_overcredit, bounds, 18)
        if false_interval[0] <= 0:
            raise ArithmeticError("Helper overcredit control did not discriminate")
        target["negative_controls"] = {
            "omitting_shared_helper_credit_loss_falsely_passes_terminal": receipt(
                false_interval
            ),
            "finite_m_penalty_retained_and_positive": True,
            "terminal96_charge_retained_and_excludes_actual_Q": True,
        }
        result["targets"].append(target)

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
