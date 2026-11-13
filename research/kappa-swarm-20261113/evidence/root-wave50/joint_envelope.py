#!/usr/bin/env python3
"""Rigorous upper envelopes for the fixed-history helper/cache mechanism.

An upper envelope is not an attainable supplier or a new kappa. Local source
and algebraic proofs are separate obligations. This script binds their exact
finite price profiles and checks the interval arithmetic used in the proof.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import json
import time
import budget_price as bp
from small_mixed import echelon, decode

ROOT = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


@lru_cache(None)
def whole_interval_price(r, kappa):
    """Taylor remainder signs hold on this larger declared interval too."""
    need(1 <= r <= 137 and 0 <= kappa <= 1, "declared whole power range")
    if kappa == 0:
        return Q(r), Q(r)
    if kappa == 1:
        return Q(1), Q(1)
    a, b = bp.log_interval(r)
    low = bp.down(r*bp.exponential_minus(kappa*b, 35))
    high = bp.up(r*bp.exponential_minus(kappa*a, 36))
    need(0 < low <= high, "positive directed power bracket")
    return low, high


def derivative(profile, left=Q(0), right=Q(1, 100)):
    lo = hi = Q(0)
    for r, n in profile.items():
        loglo, loghi = bp.log_interval(r)
        fmin, fmax = bp.price(r, right)[0], bp.price(r, left)[1]
        a, b = -loghi*fmax, -loglo*fmin
        lo += n*(a if n >= 0 else b)
        hi += n*(b if n >= 0 else a)
    return lo, hi


def run():
    start = time.monotonic()
    pins = {}

    def load(name):
        raw = (ROOT/name).read_bytes()
        pins[name] = sha256(raw).hexdigest()
        return json.loads(raw)

    small = load("small-mixed-result.json")
    rows = load("worker-b/helper-graph/ROWS.json")
    replay = load("worker-c/combined-one-relation-review/ARRANGEMENT-REPLAY.json")
    caller = load("reference/pr7481/CALLER-EXACT.json")
    need(pins["reference/pr7481/CALLER-EXACT.json"] ==
         "255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc", "exact caller pin")
    calls = sum(e[0] == "J" for e in caller["events"])
    need(calls == caller["stages"] == 17, "actual seventeen native calls")
    invoice_name = str(bp.INVOICE.relative_to(ROOT))
    invoice = load(invoice_name)
    need(pins[invoice_name] == bp.PIN, "exact complete invoice")
    T = {int(r): n for r, n in invoice["after"]["T"].items()}
    P = {int(r): n for r, n in invoice["after"]["P"].items()}
    base = Counter(T)
    base.subtract(P)
    base = {r: n for r, n in base.items() if n}
    need(sum(r*n for r, n in base.items()) == 1424, "invoice linear surplus")
    ceilings = {(39875, 39884): {5: 1, 1: 1, 6: -1},
                (42500,): {1: 1, 3: 1, 4: -1},
                (41646,): {6: 1, 4: -1}}
    certificates = []
    total = Counter()
    for block in small["components"]:
        ceiling = ceilings.get(tuple(block["cache_events"]), {})
        total.update(ceiling)
        for subset in block["subsets"]:
            for case in subset["cases"]:
                accepted = []
                for ob in case["all_necessary_obligations"]:
                    difference = Counter({int(r): n for r, n in ob["signed_profile"].items()})
                    difference.subtract(ceiling)
                    difference = {r: n for r, n in difference.items() if n}
                    at_zero = sum(r*n for r, n in difference.items())
                    dlow, dhigh = derivative(difference)
                    # d(k)<=d(0)+k sup d'; this also covers endpoint ties.
                    upper = at_zero + Q(1, 100)*max(Q(0), dhigh)
                    if upper <= 0:
                        accepted.append(dict(witness=ob["witness"],
                            difference=difference, at_zero=at_zero,
                            derivative_upper=str(dhigh), uniform_upper=str(upper)))
                need(accepted, "every small case has a uniform necessary debit")
                certificates.append(dict(sites=block["cache_events"], mask=case["mask"],
                    new=case["newly_granted"], certificate=accepted[0]))
    need(len(certificates) == 89, "all eight small-component cases covered")
    total = {r: n for r, n in total.items() if n}
    need(total == {5: 1, 1: 2, 4: -2, 3: 1}, "telescoped native ceiling")
    envelope = Counter(base)
    envelope.update({r: calls*n for r, n in total.items()})
    envelope = {r: n for r, n in envelope.items() if n}
    slope = derivative(envelope)
    need(slope[1] < 0, "strictly decreasing fine upper envelope")
    at_goal = bp.moment(envelope, Q(19, 5000))
    need(at_goal[1] < -Q(252581, 10000), "fine envelope excludes .0038")
    left = Q("0.0037347911502843961")
    right = Q("0.0037347911502843965")
    need(bp.moment(envelope, left)[0] > 0, "upper-envelope crossing left bracket")
    need(bp.moment(envelope, right)[1] < 0, "upper-envelope crossing right bracket")
    # Coarse funding works without linearity of the helper promise.
    R = {int(h): int(r) for h, r in rows["targets"].items()}
    zero_rows = [decode(r["row"]) for r in rows["records"]]
    rank = len(echelon(zero_rows))
    need(len(zero_rows) == 468 and rank == 463, "independent exact zero-row rank")
    need(all(r["rank"] <= R[int(h)] for r in rows["records"] for h in r["row"]),
         "support matching funds every independent subset")
    rmax = max(r["rank"] for r in rows["records"])
    cache_rank_sum = sum(s["target_rank"] for s in replay["site_spaces"].values())
    need(rmax == 8 and len(replay["site_spaces"]) == 14 and cache_rank_sum == 32,
         "coarse zero/cache inventory")
    cap = (len(zero_rows)-rank)*rmax + cache_rank_sum
    need(cap == 72, "coarse native cap")
    intervals = []
    queue = [(Q(1, 100), Q(1), 0)]
    while queue:
        need(time.monotonic()-start < 60, "bounded envelope verification")
        a, b, depth = queue.pop()
        upper = Q(calls*cap)
        for r, n in base.items():
            # Positive powers decrease with kappa. Collapse equal-rank terms first.
            upper += n*(whole_interval_price(r, a)[1] if n > 0
                        else whole_interval_price(r, b)[0])
        if upper < 0:
            intervals.append(dict(left=str(a), right=str(b), upper=str(upper)))
        else:
            need(depth < 14, "finite interval partition is sufficient")
            m = (a+b)/2
            queue.extend([(m, b, depth+1), (a, m, depth+1)])
    intervals.sort(key=lambda x: Q(x["left"]))
    need(Q(intervals[0]["left"]) == Q(1, 100) and Q(intervals[-1]["right"]) == 1,
         "coarse interval endpoints")
    need(all(x["right"] == y["left"] for x, y in zip(intervals, intervals[1:])),
         "gap-free coarse interval coverage")
    out = dict(status="PASS_JOINT_FUNDING_POWER_ENVELOPES_NO_NEW_KAPPA",
        source_sha256=rows["source_sha256"], input_sha256=pins, native_calls=calls,
        fine_scope="Homogeneous scalar-linear helper promises; individual local bounds require independent source and geometric verification.",
        fine_interval=["0", "1/100"], native_ceiling=total,
        small_case_count=len(certificates), small_case_certificates=certificates,
        full_envelope_at_0038=bp.display(at_goal), full_envelope_derivative=bp.display(slope),
        upper_envelope_crossing=bp.display((left, right)),
        coarse_scope="Any nonempty main-independent helper promise surjective onto retained original coordinates, original histories only;33excluded cache probes separately verified.",
        coarse_inventory=dict(zero_rows=468, rank=rank, nullity=5, max_zero_rank=8,
            possible_cache_sites=14, cache_rank_sum=32, native_cap=cap),
        coarse_interval=["1/100", "1"], coarse_partition=intervals,
        coarse_worst_upper=bp.display((max(Q(i["upper"]) for i in intervals),)*2),
        seconds=time.monotonic()-start,
        limitation="Only necessary budget bounds. No constructive supplier, physical provider, attained kappa or discharge of a foundational assumption is asserted.")
    (ROOT/"joint-envelope-result.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status":out["status"], "fine_cases":len(certificates),
        "at_0038":out["full_envelope_at_0038"]["decimal_display_only"],
        "upper_crossing":out["upper_envelope_crossing"]["decimal_display_only"],
        "coarse_intervals":len(intervals), "coarse_worst_upper":out["coarse_worst_upper"]["decimal_display_only"],
        "seconds":out["seconds"]}, indent=2))


if __name__ == "__main__":
    run()
