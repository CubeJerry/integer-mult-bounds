#!/usr/bin/env python3
"""Independent exact moment assessment at kappa=1/250 and above.

No finite field or floating-point calculation is used.  Integer qth-root
brackets enclose r**(p/q).  This is a complete-caller arithmetic assessment,
not an endpoint construction, supplier admission, or new kappa certificate.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEAD = "8533bc2640e0ec002bb16ba85997480ce3c3cac6"
FULL_PIN = "d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7"
RECEIPT_PIN = "a816768b8d71fb74755653f4888b673f980e67b8d9cea7d2e7594c5680d39aae"
RAIL_PIN = "90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2"
SCALE = 10**24
RAW = {1: 990, 2: 360, 3: 105, 4: 112, 5: 133, 6: 8, 7: 2}
IDEAL_FRESH8 = {1: 51, 7: 43, 8: 358, 9: 15}
IDEAL_NO_LINE = {1: 8, 8: 400, 9: 16}
SIMPLE_COMPLETE_CANDIDATE = {1: 208, 8: 400}
FORWARD_ENTRY_RAW = {1: 8, 8: 400, 9: 8}
FRESH8_RETURN = {1: 43, 7: 43, 8: -42, 9: 7}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def source(name, expected):
    raw = (HERE / "inputs" / name).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, "Source SHA256: " + name)
    return json.loads(raw)


def hist(values):
    return {int(k): int(v) for k, v in values.items()}


def combine(*terms):
    out = {}
    for coefficient, profile in terms:
        for rank, count in profile.items():
            out[rank] = out.get(rank, 0) + coefficient * count
    return {r: n for r, n in out.items() if n}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def subtract(a, b):
    return a[0] - b[1], a[1] - b[0]


def divide(a, positive):
    need(positive > 0, "Positive interval divisor")
    return a[0] / positive, a[1] / positive


def exact(value):
    return Fraction(value), Fraction(value)


def price_interval(rank, exponent):
    p, q = exponent.numerator, exponent.denominator
    need(rank >= 1 and 0 < p < q, "Price domain")
    if rank == 1:
        return exact(1)
    target = rank**p * SCALE**q
    low, high = 0, rank * SCALE + 1
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**q <= target:
            low = middle
        else:
            high = middle
    need(low**q <= target < (low + 1)**q, "Exact root enclosure")
    upper = low if low**q == target else low + 1
    return Fraction(low, SCALE), Fraction(upper, SCALE)


def moment(profile, prices):
    lo = hi = Fraction(0)
    for rank, count in profile.items():
        a, b = prices[rank]
        if count >= 0:
            lo += count * a
            hi += count * b
        else:
            lo += count * b
            hi += count * a
    return lo, hi


def decimal_bound(value, upper=False, digits=18):
    unit = 10**digits
    numerator = value.numerator * unit
    scaled = -((-numerator) // value.denominator) if upper else numerator // value.denominator
    sign = "-" if scaled < 0 else ""
    whole, part = divmod(abs(scaled), unit)
    return sign + str(whole) + "." + str(part).zfill(digits)


def encode(interval):
    return {
        "lower": str(interval[0]),
        "upper": str(interval[1]),
        "decimal_lower_outward": decimal_bound(interval[0]),
        "decimal_upper_outward": decimal_bound(interval[1], upper=True),
    }


def assess(kappa, T, P, N, H, Q):
    exponent = 1 - kappa
    ranks = set(T) | set(P) | set(N) | set(H) | set(RAW) | set(Q)
    ranks |= set(IDEAL_FRESH8) | set(IDEAL_NO_LINE)
    prices = {r: price_interval(r, exponent) for r in ranks}
    def bill(profile):
        return moment(profile, prices)

    # Complete caller, including loss of duplicated helper-target credits:
    # T_m = m T - 18(m-1)H
    # P_m = m(P-18N) + 18N + 18(m-1)Q.
    d = divide(bill(combine((1, P), (-1, T))), 18)
    Ainf = subtract(bill(combine((1, N), (-1, RAW), (-1, H))), d)
    current_c = bill(combine((1, Q), (-1, RAW)))
    current_limit = subtract(Ainf, current_c)
    terminal_gap = subtract(exact(96), current_limit)
    return_allowance = subtract(Ainf, bill(combine((1, FORWARD_ENTRY_RAW), (-1, RAW))))
    fresh8_cost = bill(FRESH8_RETURN)
    fresh8_limit = subtract(Ainf, bill(combine((1, IDEAL_FRESH8), (-1, RAW))))
    no_line_limit = subtract(Ainf, bill(combine((1, IDEAL_NO_LINE), (-1, RAW))))
    simple_limit = subtract(Ainf, bill(combine((1, SIMPLE_COMPLETE_CANDIDATE), (-1, RAW))))
    fresh8_m2 = subtract(fresh8_limit, d)
    fresh8_m3 = subtract(fresh8_limit, divide(d, 2))
    no_line_m2 = subtract(no_line_limit, d)
    no_line_m3 = subtract(no_line_limit, divide(d, 2))

    need(d[0] > 0, "Positive selected-caller deficit")
    need(terminal_gap[0] > 0, "Actual terminal reverse repair exceeds even limiting allowance")
    need(fresh8_limit[0] > 0, "Optimistic fresh-eight limiting moment is positive")
    need(no_line_limit[0] > 0, "Optimistic no-line limiting moment is positive")
    need(simple_limit[1] < 0, "Simple 208-return profile fails even at limiting multiplicity")
    # Check algebra independently by forming the complete profiles directly.
    for m, candidate, expected in [(2, IDEAL_FRESH8, fresh8_m2),
                                  (3, IDEAL_FRESH8, fresh8_m3),
                                  (3, IDEAL_NO_LINE, no_line_m3)]:
        target = combine((m, T), (-18 * (m - 1), H))
        paid = combine((m, P), (-18 * (m - 1), N), (18 * (m - 1), candidate))
        direct = divide(bill(combine((1, target), (-1, paid))), 18 * (m - 1))
        need(max(direct[0], expected[0]) <= min(direct[1], expected[1]),
             "Direct full-profile identity")

    # Meaningful adverse controls: old target .005 must fail the ideal gate;
    # omitting helper credit loss strictly changes the full caller; terminal
    # 31 paid returns plus 65 new departures must equal the 96 total barrier.
    helper_loss = bill(H)
    need(helper_loss[0] > 0, "Dropped helper loss would create overcredit")
    paid31_gap = subtract(exact(65), subtract(current_limit, exact(31)))
    need(paid31_gap == terminal_gap, "31-return terminal barrier invariance")
    if kappa == Fraction(1, 250):
        need(fresh8_m2[0] > 0, ".004 ideal fresh-eight m2 passes moment")
        need(no_line_m2[1] < 0 and no_line_m3[0] > 0,
             ".004 no-line moment requires at least m3")
    if kappa == Fraction(1, 240):
        need(fresh8_m2[1] < 0 and fresh8_m3[0] > 0,
             "Strictly-above-.004 ideal fresh-eight moment requires m3")

    return {
        "kappa": str(kappa),
        "price_exponent": str(exponent),
        "power_bracket_denominator": str(SCALE),
        "d": encode(d),
        "A_infinity": encode(Ainf),
        "current_Q_extra_moment": encode(current_c),
        "current_Q_remaining_limit": encode(current_limit),
        "current_Q_terminal96_limiting_deficit": encode(terminal_gap),
        "ideal_return_allowance_limit": encode(return_allowance),
        "fresh8_return_cost": encode(fresh8_cost),
        "fresh8_limit_slack": encode(fresh8_limit),
        "fresh8_m2_slack": encode(fresh8_m2),
        "fresh8_m3_slack": encode(fresh8_m3),
        "fresh9_no_line_limit_slack": encode(no_line_limit),
        "fresh9_no_line_m2_slack": encode(no_line_m2),
        "fresh9_no_line_m3_slack": encode(no_line_m3),
        "simple_208_return_limit_slack": encode(simple_limit),
        "helper_loss_overcredit_if_omitted": encode(helper_loss),
        "positive_optimistic_profile_is_supplier": False,
    }


def main():
    full = source("FULL-RESULT.json", FULL_PIN)
    rail = source("PURE-RAIL-RESULT.json", RECEIPT_PIN)
    need(rail["word_sha256"] == RAIL_PIN, "Actual standalone rail identity")
    T, P = [hist(full["invoice"][name]) for name in ("T", "P")]
    N, H = [hist(full["native"][name]) for name in ("paid", "helpers")]
    Q = hist(rail["ordinary_bill"]["moves"])
    need(sum(RAW.values()) == 1710, "Raw profile count")
    need(sum(N.values()) == 6310 and sum(H.values()) == 1080, "Native/helper count")
    need(sum(Q.values()) == 809, "Actual rail move count")
    need(combine((1, FORWARD_ENTRY_RAW), (1, FRESH8_RETURN)) == IDEAL_FRESH8,
         "Fresh-return refinement profile exact")
    rows = [assess(k, T, P, N, H, Q) for k in (Fraction(1, 250), Fraction(1, 240))]
    # .005 is an actual negative control, independently evaluated here.
    ranks = set(T) | set(P) | set(N) | set(H) | set(IDEAL_FRESH8)
    prices = {r: price_interval(r, Fraction(199, 200)) for r in ranks}
    old_gap_profile = combine((18, IDEAL_FRESH8), (-18, N), (18, H), (-1, T), (1, P))
    old_gap = divide(moment(old_gap_profile, prices), 18)
    need(old_gap[0] > 0, "Pinned .005 fresh-eight limiting obstruction reproduced")
    return {
        "status": "PASS_EXACT_004_PROFILE_ASSESSMENT",
        "programme_head": HEAD,
        "full_result_sha256": FULL_PIN,
        "pure_rail_receipt_sha256": RECEIPT_PIN,
        "rail_word_sha256": RAIL_PIN,
        "source_profiles": {"T": T, "P": P, "N": N, "H": H, "R": RAW, "Q": Q},
        "optimistic_profiles": {"fresh8": IDEAL_FRESH8, "no_line": IDEAL_NO_LINE},
        "additional_profile_checked": SIMPLE_COMPLETE_CANDIDATE,
        "rows": rows,
        "negative_control_005_fresh8_limiting_deficit": encode(old_gap),
        "negative_controls": [
            "Restored old .005 fresh-eight limiting failure.",
            "Omitted helper-target credit loss is strictly positive overcredit.",
            "31 already-paid returns plus 65 remaining departures equal 96.",
            "No-line m2 fails at .004 while m3 passes.",
            "Fresh-eight m2 fails at 1/240 while m3 passes.",
        ],
        "scope": "Exact arithmetic of pinned complete conditional moment profiles; no new kappa.",
        "not_proved": [
            "Optimistic full rail endpoint identity L=E.",
            "Complete physical compiler and uniform complex supplier.",
            "Compatible completed ordinary BIT supplier.",
            "Any of the five foundational assumptions.",
            "Universal impossibility outside the terminal source interface.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
