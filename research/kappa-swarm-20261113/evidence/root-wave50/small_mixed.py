#!/usr/bin/env python3
"""Exact-Q root check of eight small mixed helper/cache components.

Research arithmetic only: source reconstruction and global composition are
separately reviewed. Each new cache supplies its own necessary direction.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time
import budget_price as bp

ROOT = Path(__file__).resolve().parent
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
KAPPA = Q(19, 5000)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def decode(row):
    return {int(h): Q(a) for h, a in row.items() if Q(a)}


def axpy(row, other, factor):
    for h, a in other.items():
        z = row.get(h, Q(0)) + factor*a
        if z:
            row[h] = z
        else:
            row.pop(h, None)


def residue(row, basis):
    # All pivots, including those after the first nonpivot coordinate.
    row = row.copy()
    for p in sorted(basis):
        if row.get(p):
            axpy(row, basis[p], -row[p])
    return row


def echelon(rows):
    out = {}
    for row in rows:
        v = residue(row, out)
        if v:
            p = min(v)
            out[p] = {h: a/v[p] for h, a in v.items()}
    return out


def profile(prefix):
    need(prefix[0] == 0, "no zero-price helper columns")
    need(all(a <= b for a, b in zip(prefix, prefix[1:])), "prefix monotonicity")
    return {k: prefix[k]-prefix[k-1] for k in range(1, 10)
            if prefix[k] != prefix[k-1]}


def run():
    start = time.monotonic()
    pins = {}

    def load(name, compressed=False):
        raw = (ROOT/name).read_bytes()
        pins[name] = sha256(raw).hexdigest()
        return json.loads(gzip.decompress(raw) if compressed else raw)

    word = load("reference/pr7481/WORD.json.gz", True)
    need(pins["reference/pr7481/WORD.json.gz"] == PIN, "native bytes")
    independent = load("worker-c/combined-one-relation-review/ARRANGEMENT-REPLAY.json")
    need(independent["source_sha256"] == PIN, "fresh source replay binding")
    rows = load("worker-b/helper-graph/ROWS.json")
    need(rows["source_sha256"] == PIN, "zero source binding")
    arrangement = load("cache-zero-arrangement-exploration.json")
    zero = {r["event"]: r for r in rows["records"]}
    target_rank = {int(h): int(r) for h, r in rows["targets"].items()}
    need(len(target_rank) == 1101, "all original helpers")
    need(residue({1: Q(1), 7: Q(2)}, {7: {7: Q(1), 8: Q(3)}})
         == {1: Q(1), 8: Q(-6)}, "all-pivot quotient negative-control trap")
    sites = independent["site_spaces"]
    selected = [c for c in arrangement["components_with_cache_spaces"]
                if len(c["zero_events"]) <= 4]
    need(len(selected) == 8, "eight assigned components")
    result = []
    gain_sum_lo = gain_sum_hi = Q(0)
    covered = 0
    for component in selected:
        events = sorted(int(s.split(":")[1]) for s in component["cache_sites"])
        zevents = component["zero_events"]
        zr = [decode(zero[e]["row"]) for e in zevents]
        data = {}
        for e in events:
            s = sites[str(e)]
            need(word["program"][e] == ["MOVE", s["owner"], s["source"],
                                       s["destination"], True], "cache literal")
            raw_hist = s["history_basis"]
            raw_l = s["helper_extension_basis"]
            P = echelon(decode(r) for r in (raw_hist.values() if isinstance(raw_hist, dict) else raw_hist))
            L = echelon(decode(r) for r in (raw_l.values() if isinstance(raw_l, dict) else raw_l))
            target = decode(s["target_row"])
            need(len(P) == s["strict_history_rank"] and len(L) == s["helper_extension_dim"], "source space dimensions")
            need(residue(target, P), "unrestricted earlier-history miss")
            need(all(set(r) <= target_rank.keys() for r in L.values()), "L is helper-only")
            data[e] = dict(P=P, L=L, target=target, rank=s["target_rank"])
        cases = []
        subset_records = []
        for mask in range(1 << len(zr)):
            need(time.monotonic()-start < 60, "bounded scope deadline")
            indices = [i for i in range(len(zr)) if mask >> i & 1]
            Z = echelon(zr[i] for i in indices)
            prefix = [len(echelon({h: a for h, a in row.items() if target_rank[h] <= k}
                                  for row in Z.values())) for k in range(10)]
            beta = profile(prefix)
            enabled = [e for e in events if not residue(data[e]["target"], echelon(
                list(data[e]["P"].values()) + list(Z.values())))]
            newable = [e for e in events if e not in enabled]
            individual = {}
            for e in newable:
                L = data[e]["L"]
                union = [len(echelon({h: a for h, a in row.items() if target_rank[h] <= k}
                                     for row in list(Z.values()) + list(L.values())))
                         for k in range(10)]
                need(union[9] > prefix[9], "new cache needs a direction outside Z")
                generic = [min(prefix[k]+1, union[k]) for k in range(10)]
                individual[e] = dict(prefix=generic, debit=profile(generic))
            mask_cases = []
            for nmask in range(1 << len(newable)):
                new = [e for j, e in enumerate(newable) if nmask >> j & 1]
                credits = Counter(zero[zevents[i]]["rank"] for i in indices)
                credits.update(data[e]["rank"] for e in enabled+new)
                obligations = [(None, beta)] if not new else [(e, individual[e]["debit"]) for e in new]
                upper_candidates = []
                for witness, debit in obligations:
                    delta = credits.copy()
                    delta.subtract(debit)
                    delta = {r: a for r, a in delta.items() if a}
                    interval = bp.moment(delta, KAPPA)
                    upper_candidates.append(dict(witness=witness, debit=debit,
                        signed_profile=delta, interval=bp.display(interval)))
                lo = min(Q(c["interval"]["exact"][0]) for c in upper_candidates)
                hi = min(Q(c["interval"]["exact"][1]) for c in upper_candidates)
                best = min(upper_candidates, key=lambda c: Q(c["interval"]["exact"][1]))
                case = dict(mask=mask, enabled=enabled, newly_granted=new,
                    native_bound=bp.display((lo, hi)), binding_obligation=best,
                    all_necessary_obligations=upper_candidates)
                cases.append(case)
                mask_cases.append(case)
            subset_records.append(dict(mask=mask, zeros=[zevents[i] for i in indices],
                prefix=prefix, beta=beta, enabled=enabled, new_obligations=individual,
                cases=mask_cases))
            covered += 1
        lo = max(Q(c["native_bound"]["exact"][0]) for c in cases)
        hi = max(Q(c["native_bound"]["exact"][1]) for c in cases)
        best = max(cases, key=lambda c: Q(c["native_bound"]["exact"][1]))
        gain_sum_lo += lo
        gain_sum_hi += hi
        result.append(dict(cache_events=events, zero_events=zevents,
            subset_count=len(subset_records), case_count=len(cases),
            max_relaxed_native_gain=bp.display((lo, hi)), maximizing_case=best,
            subsets=subset_records))
    out = dict(status="COMPLETE_EIGHT_SMALL_COMPONENT_EXACT_RELAXATIONS",
        source_sha256=PIN, input_sha256=pins, kappa=str(KAPPA),
        covered_subsets=covered, components=result,
        total_native_upper=bp.display((gain_sum_lo, gain_sum_hi)),
        seconds=time.monotonic()-start,
        scope="Arithmetic evidence for arbitrary homogeneous scalar-linear helper constraints with original retained targets; global direct-sum proof and source review separate. No positive profile is asserted realizable, and no kappa is claimed.")
    (ROOT/"small-mixed-result.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status":out["status"], "subsets":covered,
        "components":[{"sites":c["cache_events"], "maximum":c["max_relaxed_native_gain"]["decimal_display_only"],
                       "profile":c["maximizing_case"]["binding_obligation"]["signed_profile"]} for c in result],
        "total":out["total_native_upper"]["decimal_display_only"], "seconds":out["seconds"]}, indent=2))


if __name__ == "__main__":
    run()
