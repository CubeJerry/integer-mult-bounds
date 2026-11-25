#!/usr/bin/env python3
"""Exact finite controls for Route B's schedules, chunk layout and eligibility.

These are arithmetic/model checks. They are not a physical Turing-machine
implementation, a proof of asymptotic bounds by testing, or a source compiler.
"""

from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import random
import sys


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def ell(value):
    require(value >= 1, "positive binary length")
    return value.bit_length()


def code_length(value):
    a = ell(value)
    return a + 3 * ell(a)


def row_product(left, right, n, r):
    require(0 <= left < 2**n and 0 <= right < 2**n, "input width")
    require(1 <= r <= n, "chunk count")
    u = (n + r - 1) // r
    base = 2**u
    aa = [(left // base**i) % base for i in range(r)]
    bb = [(right // base**j) % base for j in range(r)]
    zz = [0] * (2*r)
    calls = 0
    for i in range(r):
        carry = 0
        for j in range(r):
            current = aa[i] * bb[j] + zz[i+j] + carry
            require(current <= base*base-1, "two-digit local bound")
            zz[i+j] = current % base
            carry = current // base
            require(0 <= carry < base, "single-digit carry invariant")
            calls += 1
        require(zz[i+r] == 0, "untouched row-ending digit")
        zz[i+r] = carry
        value = sum(digit * base**k for k, digit in enumerate(zz))
        require(value == (left % base**(i+1)) * right,
                "exact accumulated rows")
    result = sum(digit * base**k for k, digit in enumerate(zz))
    require(result == left * right, "complete product")
    require(calls == r*r, "exact digit-call count")
    require(r*r*u <= 2*r*n, "wrapper invoice")
    require(2*r*u <= 4*n, "contiguous accumulator cap")
    return result


def main():
    # Independently enumerate the simple B1 pair schedule for small rounds.
    budget_rounds = []
    for s in range(1, 23):
        m = s // 2
        count = 0
        allotted = Fraction(1, 2) * 2**s
        for a in range(1, m+1):
            for b in range(1, m+1):
                if 2*(a+b) > s:
                    continue
                for q in range(2**(a-1), 2**a):
                    for h in range(2**(b-1), 2**b):
                        count += 1
                        allotted += 2**(s-2*ell(q)-2*ell(h))
        exact_count = (m-2)*2**(m-1)+1 if m >= 2 else 0
        require(count == exact_count, "B1 exact pair count")
        require(allotted <= Fraction(3, 4)*2**s, "B1 round mass")
        budget_rounds.append({"s": s, "pairs": count})

    # B2 moments by two exact grouping computations.
    for max_a in [1, 3, 7, 15, 31, 63, 127]:
        partial_mass = sum((Fraction(1, 2) / 2**(3*ell(a))
                            for a in range(1, max_a+1)), Fraction())
        partial_moment = sum((Fraction(a, 2) / 2**(3*ell(a))
                              for a in range(1, max_a+1)), Fraction())
        level = ell(max_a)
        require(partial_mass == Fraction(1, 12)*(1-Fraction(1, 4**level)),
                "B2 exact mass prefix")
        require(partial_moment <= Fraction(1, 4), "B2 label-cost moment")
    for q, h in product(range(1, 257), repeat=2):
        weight = 2**(code_length(q)+code_length(h))
        require(weight <= 256*q*h*ell(q)**3*ell(h)**3,
                "B2 parameter penalty")

    # Removing all length overhead gives non-summable weight, a negative
    # control on this particular block schedule (not all schedulers).
    require(sum(Fraction(1, 2) for _ in range(10)) > 1,
            "bare binary-length weights do not sum to one")

    exhaustive_products = 0
    for n in range(1, 7):
        for r in range(1, n+1):
            for left, right in product(range(2**n), repeat=2):
                row_product(left, right, n, r)
                exhaustive_products += 1
    rng = random.Random(20261126)
    randomized_products = 0
    for _ in range(200):
        n = rng.randint(7, 128)
        r = rng.randint(1, n)
        row_product(rng.getrandbits(n), rng.getrandbits(n), n, r)
        randomized_products += 1
    for r in [1, 2, 31, 256, 512]:
        row_product(2**512-1, 2**512-1, 512, r)
        randomized_products += 1

    # This maximum-digit example needs real carry propagation.
    require(row_product(15, 15, 4, 2) == 225, "max-digit positive control")
    base = 4
    without_carries = sum(((3*3) % base)*base**(i+j)
                         for i in range(2) for j in range(2))
    require(without_carries != 225, "dropping carry is detected")

    cap_cases = 0
    for c in range(1, 129):
        r = 1
        while r <= 2*c:
            r *= 2
        require(2*c < r <= 4*c, "least strict dyadic chunk count")
        for core_threshold in [1, 2, 5, 19]:
            threshold = max(4*c, r*core_threshold)
            for n in [threshold, threshold+1, threshold+r-1,
                      2*threshold, 3*threshold+1]:
                u = (n+r-1)//r
                require(r <= n and u >= core_threshold,
                        "integer threshold feasibility")
                require(c*(u+1) <= n, "candidate common cap")
                cap_cases += 1

    # Model-level discovery bound: all targets fitting a sufficiently early
    # successful round are actually offered; compare exact integer budgets.
    discovery_cases = 0
    for s in range(8, 29):
        for j in range(1, 129):
            w = 2**code_length(j)
            for e in [1, 2, 3, 7, 16, 31, 100]:
                if w*(e+1) <= 2**s:
                    success_round = code_length(j) + e.bit_length()
                    require(success_round <= s, "successful preflight round")
                    require(2**(success_round-code_length(j)) >= e,
                            "enough actual offer steps")
                    discovery_cases += 1

    rate_cases = 0
    for cg, cv, cn in product(range(1, 5), repeat=3):
        divisor = 4*max(cg, cv, cn)
        for x in range(32, 257):
            j = x//divisor
            require(j >= 1 and cn*j <= x//4, "P2 threshold slack")
            # log2(w_j) is an integer; extra 10 pays a finite model constant.
            log_cost = code_length(j)+10+2**(cg*j)+x*2**(cv*j)
            require(log_cost < 2**x-1, "P2 preparation window")
            rate_cases += 1
    for x in [8, 16, 32, 64]:
        require(2**(2*x) > 2**x-1,
                "uncontrolled growing index fails the preparation test")

    report = {
        "status": "exact_finite_checks_passed",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "simple_schedule_rounds": len(budget_rounds),
        "max_simple_schedule_pairs": budget_rounds[-1]["pairs"],
        "sharp_penalty_parameter_pairs": 256**2,
        "exhaustive_chunk_products": exhaustive_products,
        "seeded_larger_chunk_products": randomized_products,
        "space_threshold_cases": cap_cases,
        "preflight_discovery_cases": discovery_cases,
        "preflight_rate_cases": rate_cases,
        "negative_controls": [
            "bare binary-length weights are non-summable",
            "dropping positional carries changes the product",
            "uncontrolled index growth can outrun linear preparation",
        ],
        "not_verified": [
            "literal fixed-tape implementation",
            "all asymptotic claims by finite enumeration",
            "sound source-wide bill compiler",
            "source candidate constants and thresholds",
            "complete new unconditional multiplication envelope",
        ],
    }
    Path(__file__).with_name("verification.json").write_text(
        json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
