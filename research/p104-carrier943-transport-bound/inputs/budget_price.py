#!/usr/bin/env python3
"""Directed rational optimistic budget for the exact unselected #7481 invoice.

This is a research aid, not a compiler, source admission or kappa proposal.
No floating-point operation influences an interval or sign decision.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
INVOICE = ROOT / "reference/pr7481/producer54/validation_signed/adapted/CURRENT-PRICE.json"
PIN = "86f71ccbc923db5d7a6753aa971c3a9c8a572680534498ed17be072cfa2aae6b"
DEN = 10**50


def need(ok, why):
    if not ok:
        raise ValueError(why)


def down(x):
    return Q((x.numerator * DEN) // x.denominator, DEN)


def up(x):
    return -down(-x)


def log_series(x, terms=64):
    """For 1 <= x <= 2, positive atanh series and a geometric tail bound."""
    need(1 <= x <= 2, "log range reduction")
    z = (x-1)/(x+1)
    z2, power, s = z*z, z, Q(0)
    for j in range(terms):
        s += 2*power/(2*j+1)
        power *= z2
    # Remaining denominators are >=2*terms+1.
    error = 2*power / ((2*terms+1)*(1-z2))
    return down(s), up(s+error)


@lru_cache(None)
def log_interval(r):
    need(isinstance(r, int) and r >= 1, "positive integral rank")
    a = r.bit_length()-1
    lo2, hi2 = log_series(Q(2))
    lo, hi = log_series(Q(r, 1 << a))
    return down(a*lo2+lo), up(a*hi2+hi)


def exponential_minus(x, degree):
    """Finite Taylor polynomial; odd lower and even upper for x>=0."""
    need(x >= 0, "nonnegative exponential argument")
    term = total = Q(1)
    for k in range(1, degree+1):
        term *= -x/k
        total += term
    return total


@lru_cache(None)
def price(r, kappa):
    if r == 0:
        return Q(0), Q(0)
    need(1 <= r <= 137 and 0 <= kappa <= Q(1, 100), "declared pricing domain")
    lo, hi = log_interval(r)
    # exp(-x) decreases. Taylor's signed remainder bounds hold for all x>=0.
    low = r*exponential_minus(kappa*hi, 35)
    high = r*exponential_minus(kappa*lo, 36)
    return down(low), up(high)


def moment(signed, kappa):
    lo = hi = Q(0)
    for r, count in signed.items():
        a, b = price(int(r), kappa)
        lo += count*(a if count >= 0 else b)
        hi += count*(b if count >= 0 else a)
    return lo, hi


def display(interval):
    with localcontext() as ctx:
        ctx.prec = 35
        approximate = [str(Decimal(x.numerator)/Decimal(x.denominator)) for x in interval]
    return {"exact": list(map(str, interval)), "decimal_display_only": approximate}


def run():
    raw = INVOICE.read_bytes()
    need(sha256(raw).hexdigest() == PIN, "exact invoice pin")
    x = json.loads(raw)
    target, paid = x["after"]["T"], x["after"]["P"]
    signed = {r: target.get(r, 0)-paid.get(r, 0) for r in target.keys() | paid.keys()}
    need(sum(int(r)*c for r,c in signed.items()) == 1424, "linear surplus")
    need(price(0, Q(0)) == (0, 0) and price(1, Q(1,100)) == (1,1), "exact boundary controls")
    need(moment(signed, Q(0)) == (1424, 1424), "linear moment control")
    claim = Q(x["gate"]["claim"])
    need(moment(signed, claim)[0] > 0, "published raw invoice margin positive")
    left, right = map(Q, x["gate"]["raw_bracket"])
    need(moment(signed, left)[0] > 0, "independent left crossing bracket")
    need(moment(signed, right)[1] < 0, "independent right crossing bracket")
    records = []
    for kappa in (Q(38,10000), Q(4,1000), Q(1,100)):
        baseline = moment(signed, kappa)
        need(baseline[1] < 0, "optimistic unmodified complex budget fails")
        trials = {}
        for rank in range(1,10):
            lo,hi = price(rank,kappa)
            trials[str(rank)] = display((baseline[0]+17*lo, baseline[1]+17*hi))
        feasible = [r for r in range(1,10) if Q(trials[str(r)]["exact"][0]) > 0]
        records.append({"kappa": str(kappa), "complete_complex_moment": display(baseline),
                        "required_net_native_saving": display((-baseline[1]/17, -baseline[0]/17)),
                        "one_removed_native_MOVE_with_no_target_loss": trials,
                        "first_optimistically_sufficient_single_rank": min(feasible) if feasible else None})
    result = {
        "status": "PASS_DIRECTED_OPTIMISTIC_COMPLEX_BUDGET",
        "invoice_sha256": PIN, "current_native_calls": 17,
        "selected_complete_kappa": "363005817/100000000000",
        "selected_completed_BIT_saving": "0.00385248",
        "selected_tested_complex_BIT_premise": "0.00376669",
        "records": records,
        "limits": "Complex moment only. Helper debit, cache/setup/ordinary cost, exact-grid/catalogue, compiler constants, new BIT/outer gate checks and all five foundations are additional obligations. No changed source or new complete kappa.",
    }
    (ROOT / "budget-price-result.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status":result["status"], "records":[{
        "kappa":r["kappa"], "complex_moment":r["complete_complex_moment"]["decimal_display_only"],
        "net_native_needed":r["required_net_native_saving"]["decimal_display_only"],
        "first_single_rank":r["first_optimistically_sufficient_single_rank"]} for r in records]}, indent=2))


if __name__ == "__main__":
    run()
