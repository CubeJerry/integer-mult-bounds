#!/usr/bin/env python3
"""Directed rational checks for the covariant target's single-grade BIT tariff."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
from collections import Counter
from fractions import Fraction as F
from functools import cache
from pathlib import Path


SCALE = 10**32
TARGET = F(1, 200)
RAW = TARGET + F(5, 10**10)
UNIFORM = TARGET + F(4, 10**10)
COVERED = TARGET + F(3, 10**10)
ORDINARY = TARGET + F(2, 10**10)
RHO = F(1, 128)
OLD_SEED = F(385248, 10**8)
NATIVE_PATH = "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
NATIVE_SHA = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
COVARIANT = "research/moonshot-005-program/results/bit-two-sided-covariant-target/author"
COVARIANT_RESULT_SHA = "4151df493670c7912ef613e8d6de490bcb2af9b1f95d9dc065e05594da2ef4c1"
BASELINE = "914097a04bb93f730b805e9d4f036b46707c8675"


def require(value, message):
    if not value:
        raise ValueError(message)


def enclosure(a, b):
    """Round outwards so repeated operations stay small."""
    return (F((a * SCALE).__floor__(), SCALE), F((b * SCALE).__ceil__(), SCALE))


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(c, x):
    if c < 0:
        return c * x[1], c * x[0]
    return c * x[0], c * x[1]


def times(x, y):
    values = [a * b for a in x for b in y]
    return enclosure(min(values), max(values))


def log_unit(value):
    """log(value) for 1 <= value <= 2 via the atanh series."""
    require(1 <= value <= 2, "log range")
    z = (value - 1) / (value + 1)
    total = 2 * sum(z ** (2*j + 1) / (2*j + 1) for j in range(43))
    tail = 2 * z**87 / (87 * (1 - z*z))
    return enclosure(total, total + tail)


@cache
def log_int(rank):
    shift = rank.bit_length() - 1
    return add(scale(shift, log_unit(F(2))), log_unit(F(rank, 2**shift)))


def exp_minus(x):
    """Bounds exp(-x) on [0,1] by alternating partial sums."""
    require(0 <= x <= 1, "exponential range")
    term = total = F(1)
    for k in range(1, 20):
        term *= -x / k
        total += term
    return enclosure(total, total - term * x / 20)


@cache
def power(rank, saving):
    if saving == 0:
        return F(rank), F(rank)
    if saving == 1:
        return F(1), F(1)
    a, b = scale(saving, log_int(rank))
    return enclosure(rank * exp_minus(b)[0], rank * exp_minus(a)[1])


def read_source(repo, name):
    path = repo / name
    if path.is_file():
        return path.read_bytes()
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{BASELINE}:{name}"])


def ordered_profiles(repo):
    data = read_source(repo, NATIVE_PATH)
    require(hashlib.sha256(data).hexdigest() == NATIVE_SHA, "native digest")
    native = json.loads(gzip.decompress(data))
    ranks = {int(label): row["dim"] for label, row in native["frames"].items()}
    paid = Counter(abs(ranks[e[2]] - ranks[e[3]]) for e in native["program"] if e[0] == "MOVE")
    targets = Counter(ranks[native["final"][j]] - ranks[native["start"][j]] for j in range(222, 659))
    require(paid == {1:1386, 2:1253, 3:62, 4:47, 5:9, 6:104, 7:10}, "native paid")
    require(targets == {2:1, 4:25, 6:1, 8:410}, "native helpers")
    data = read_source(repo, COVARIANT + "/output/RESULT.json")
    require(hashlib.sha256(data).hexdigest() == COVARIANT_RESULT_SHA, "target digest")
    result = json.loads(data)
    ratio = F(result["retained_repair_rank"], result["bank"])
    require(ratio == F(1, 30) and result["return_rank"] == 34688, "target rank")
    source = {1:F(4451, 8), 2:F(7213, 16), 4:F(24), 8:9 + ratio}
    return paid, targets, source


def histograms(source, m):
    native_paid, helpers, source_paid = source
    # m=None is the coefficient of m after expansion, not another caller.
    slope, intercept = (1, 0) if m is None else (m, 1)
    paid = Counter({r:18*intercept*n for r,n in native_paid.items()})
    target = Counter({r:18*intercept*n for r,n in helpers.items()})
    paid[1] += 222*slope
    target[127] += 111*slope
    for j in range(1, 9):
        paid[7*j] += 222*slope
    for j in range(1, 10):
        target[1+7*j] += 222*slope
    for r, n in source_paid.items():
        paid[r] += 18*(slope-intercept)*n
    return +paid, +target


def moment(histogram, saving):
    total = F(0), F(0)
    for r, quantity in histogram.items():
        total = add(total, scale(quantity, power(r, saving)))
    return total


def raw_gap(profiles, saving):
    paid, target = profiles
    signed = target.copy()
    signed.subtract(paid)
    return moment(signed, saving)


def centered_log(histogram, saving, comparison_rank):
    scaled_sum = F(0), F(0)
    for rank, count in histogram.items():
        centered = add(log_int(rank), scale(-1, log_int(comparison_rank)))
        scaled_sum = add(scaled_sum, scale(count, times(power(rank, saving), centered)))
    return scaled_sum


def json_interval(interval):
    return [str(endpoint) for endpoint in enclosure(*interval)]


def mode(weights, v):
    total = sum(weights.values())
    counts = {r:(v*w/total).__floor__() for r,w in weights.items()}
    for _ in range(v - sum(counts.values())):
        r = max(weights, key=lambda k:(weights[k] / (counts[k]+1), -k))
        counts[r] += 1
    require(sum(counts.values()) == v, "type length")
    # Swapping any chosen occurrence for any next candidate cannot improve the mode.
    require(min(weights[r]/n for r,n in counts.items() if n) >=
            max(weights[r]/(n+1) for r,n in counts.items()), "exact modal exchange condition")
    return counts


def single_grade(profiles):
    paid, target = profiles
    lanes = 3840 * 6
    require(all((F(c)*lanes).denominator == 1 for h in profiles for c in h.values()),
            "paid record and productive counts must both be integral")
    paid = {k:int(lanes*z) for k,z in paid.items()}
    target = {k:int(lanes*z) for k,z in target.items()}
    weights = {k:c*power(k, RAW)[0] for k,c in target.items()}
    total = sum(weights.values())
    paid_t = moment(paid, RAW)[1]
    # lower bound on 13^RAW uses exp(-RAW log 13)=13^(1-RAW)/13.
    inv_cutoff_power = power(13, RAW)[1]/13
    slack = min(1 - paid_t/total, 1 - sum(k*c for k,c in paid.items()) * inv_cutoff_power/total)
    require(slack > 0, "two modal funding ratios")
    d = len(weights)
    for exponent in range(1, 70):
        v = 2**exponent
        if v*slack >= d*(exponent+1) + 3:
            break
    else:
        raise ValueError("no type bound in the witness range")
    counts = mode(weights, v)
    grade = F(0), F(0)
    for r, n in counts.items():
        grade = add(grade, scale(n, add(log_int(r), scale(-1, log_int(49)))))
    require(grade[0] > 0, "modal grade K >= 49^v")
    require(49**19 >= 13**19*sum(target.values()), "degree 19")
    require(49**18 < 13**18*sum(target.values()), "degree 18 not justified by this bound")
    return {
        "binary_lanes_in_Galois_degree_six_specialization":lanes,
        "productive_slots":sum(target.values()), "paid_slots":sum(paid.values()),
        "productive_histogram":target, "paid_histogram":paid,
        "type_length":v, "log2_type_length":exponent, "distinct_target_ranks":d,
        "type_counts":counts, "v_times_funding_slack_lower":str(v*slack),
        "required_logarithmic_toll_upper":d*(exponent+1) + 3,
        "log_grade_over_49_power":json_interval(grade),
        "split_base":13, "retained_grade_lower_base":49, "ratio_upper":"3/8",
        "productive_polynomial_exponent":19,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = ordered_profiles(args.repo)
    profiles = {m:histograms(source,m) for m in (2,4,868,870,872,1000,None)}
    slopes = {}
    for m,cutoff in [(2,9),(4,13),(None,13)]:
        paid, target = profiles[m]
        low = centered_log(target, F(1), cutoff)
        high = centered_log(paid, F(0), cutoff)
        require(low[0] > 0 and high[1] < 0, "all-price target/paid separation")
        slopes["slope" if m is None else str(m)] = {
            "cutoff":cutoff, "T_prime_0_minus_T0_log_cutoff":json_interval(low),
            "P_prime_1_minus_P1_log_cutoff":json_interval(high),
        }
    brackets = {}
    for m, left, right in [
        (870,".00500000060450",".00500000060451"),
        (None,".00500220831285",".00500220831286"),
    ]:
        a = raw_gap(profiles[m], F(left))
        b = raw_gap(profiles[m], F(right))
        require(a[0] > 0 and b[1] < 0, "crossing endpoints")
        brackets["infinite_m_slope" if m is None else str(m)] = {
            "strict_bounds":[left,right],"gap_at_lower":json_interval(a),"gap_at_upper":json_interval(b),
        }
    require(raw_gap(profiles[2], TARGET)[1] < 0 and raw_gap(profiles[None], TARGET)[0] > 0,
            "m=2 failure and strictly increasing target gap in m")
    require(raw_gap(profiles[868], TARGET)[1] < 0 < raw_gap(profiles[870], RAW)[0],
            "first even feasible m at target and chosen strict price")
    legacy_threshold = TARGET*(1-OLD_SEED)/(1-TARGET)
    require(legacy_threshold == F(3112961,621875000), "one-stage threshold")
    require(F(brackets["infinite_m_slope"]["strict_bounds"][1]) < legacy_threshold, "all-m exclusion")
    require(TARGET < ORDINARY < COVERED < UNIFORM < RAW < RHO < 1-COVERED,
            "strict recurrence and stock exponents")
    stages = [OLD_SEED]
    for _ in range(4):
        stages.append(COVERED/(1+COVERED-stages[-1]))
    require(stages[2] < TARGET < stages[3] < ORDINARY < stages[4],
            "optimal acyclic depths at the target and offered price")
    require(F(1,250) < TARGET, "selected atom floor excludes target")
    # Independent integer control: raw endpoint advantages need not imply a single grade in other words.
    require(70+16 > 18*4 and 70+256 > 18*16 and 70+64 < 18*8,
            "raw-only chord failure control from PR 7828")
    require(raw_gap(profiles[870], F(".0050000007"))[1] < 0,
            "overpriced m=870")
    result = {
        "status":"PASS_COVARIANT_SINGLE_GRADE_AND_SELF_HOSTED_BUDGET",
        "scope":"Exact source-tariff theorem and explicit modal type. Physical source, full caller and strict suppliers remain open.",
        "slope_separation":slopes,"crossings":brackets,
        "covered_one_stage_minimum_strictly_above":str(legacy_threshold),
        "prices":{k:str(v) for k,v in zip(["target","raw","uniform","covered","offered_ordinary","atom"],
                                           [TARGET,RAW,UNIFORM,COVERED,ORDINARY,RHO])},
        "normalized_gap_870_at_raw":json_interval(raw_gap(profiles[870],RAW)),
        "finite_stage_suprema_at_chosen_covered":[str(x) for x in stages],
        "grade_witness":single_grade(profiles[870]),
        "negative_controls":["m=868 at target", "m=870 at .0050000007", "all m below one-stage threshold",
                             "source atom 1/250", "foreign histogram with interior chord failure",
                             "GF64-lane exponent 18 fails the chosen width estimate"],
        "foundations_retained":True, "new_complete_kappa":False,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(result["status"])
    print("raw crossings", brackets["870"]["strict_bounds"], brackets["infinite_m_slope"]["strict_bounds"])
    print("modal power", result["grade_witness"]["type_length"], "degree", result["grade_witness"]["productive_polynomial_exponent"])


if __name__ == "__main__":
    main()
