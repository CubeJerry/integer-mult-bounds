#!/usr/bin/env python3
"""Optimistic ONE-import gate after the latest943 injection; bounded search.

No word is emitted. Historical backing and every ordinary operation are free.
Prepared for CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys
import time

from check import SOURCE, PIN, CUT, INJECT, need, add, encoded, rank

ROOT = Path(__file__).resolve().parents[2]
COMPILER = ROOT / "worker-a/selected/frozen/clifford_exact.py"
COMPILER_PIN = "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    sys.modules[name] = out
    spec.loader.exec_module(out)
    return out


def space(basis):
    out = {0}
    for v in basis:
        out |= {v ^ u for u in tuple(out)}
    return frozenset(out)


def encoded_relation(records):
    """Return a dependence of old rows with encoded coefficient1, if any."""
    basis = {}
    for i, record in enumerate(records):
        row, d, comb = record["row"].copy(), record["delta"], {i: Q(1)}
        while row:
            p = min(row)
            if p not in basis:
                q = row[p]
                basis[p] = ({j: v/q for j, v in row.items()}, d/q,
                            {j: v/q for j, v in comb.items()})
                break
            old, oldd, oldcomb = basis[p]
            q = row[p]
            add(row, old, -q)
            d -= q*oldd
            add(comb, oldcomb, -q)
        if not row and d:
            return {j: v/d for j, v in comb.items()}, len(basis)
    return None, len(basis)


def run(max_seconds=60):
    start = time.monotonic()
    raw = SOURCE.read_bytes()
    need(sha256(raw).hexdigest() == PIN, "source pin")
    w = json.loads(gzip.decompress(raw))
    need(sha256(COMPILER.read_bytes()).hexdigest() == COMPILER_PIN, "Clifford constructor pin")
    compiler = module("carrier943_clifford", COMPILER)
    destination_op = compiler.canonical_frame(9, w["frames"][189])
    spans = list(map(space, w["frames"]))
    aliases = defaultdict(list)
    for f, s in enumerate(spans):
        aliases[s].append(f)
    n = w["public"]
    rows = [{r: Q(1)} for r in range(n)] + [None]*w["owned_fields"]
    delta = [Q(0)]*len(rows)
    cur = list(w["initial"]) + [None]*w["owned_fields"]
    banks = defaultdict(list)

    def observe(event, owner, frame):
        if owner != 1459:
            banks[spans[frame]].append({"event": event, "owner": owner, "frame": frame,
                                       "row": rows[owner].copy(), "delta": delta[owner]})

    for a, f in enumerate(w["initial"]):
        observe(-1, a, f)
    for event, e in enumerate(w["program"][:CUT]):
        need(time.monotonic()-start < max_seconds, "bounded prefix replay")
        if event == INJECT:
            need(rows[885] == {885: Q(1), 943: Q(1)}, "latest source z")
            delta[943] += 1
        op, a = e[:2]
        if op == "INIT":
            cur[a], rows[a], delta[a] = e[2], {}, Q(0)
        elif op == "CLEAR":
            cur[a], rows[a], delta[a] = None, None, Q(0)
        elif op == "MOVE":
            need(cur[a] == e[2], "native MOVE source")
            cur[a] = e[3]
            observe(event, a, e[3])
        elif op == "SCALE":
            rows[a] = {j: Q(e[2])*v for j, v in rows[a].items()}
            delta[a] *= Q(e[2])
        else:
            need(op in ("ADD", "COPY"), "source opcode")
            b, q = e[2], Q(e[3])
            need(cur[a] == cur[b] == e[-1], "same physical frame scalar contact")
            if op == "COPY":
                rows[a], delta[a] = {}, Q(0)
            add(rows[a], rows[b], q)
            delta[a] += q*delta[b]
    prefix_seconds = time.monotonic()-start
    target = rows[885]
    need(target == {885: Q(1), 943: Q(1)}, "old target z")
    bankB = banks[spans[189]]
    need(len(bankB) == 2 and rank([o["row"] for o in bankB]) == 2, "literal B bank")
    eligible = []
    for s, bank in banks.items():
        f = aliases[s][0]
        dim = len(w["frames"][f])
        intersection_dim = (len(s & spans[189])).bit_length()-1
        child_rank = dim + 8 - 2*intersection_dim
        if 1 <= child_rank <= 3:
            eligible.append((child_rank, len(bank), f, s))
    eligible.sort()
    records, witness = [], None
    for child_rank, count, f, s in eligible:
        if time.monotonic()-start >= max_seconds:
            break
        combined = bankB + banks[s]
        actual = compiler.canonical_frame(9, w["frames"][f]).adjoint().then(destination_op)
        actual_rank = compiler.rank([x for x, z, phase in actual.tab[9:]])
        need(actual_rank == child_rank, "actual physical B-rank equals exact frame distance")
        need(all(885 not in o["row"] for o in combined), "old non-B source observation has no885 dependence")
        weights, rankR = encoded_relation(combined)
        record = {"frame_ids": aliases[s], "rank": child_rank,
                  "dimension": len(w["frames"][f]), "A_history_observations": count,
                  "old_union_rank": rankR, "encoded_dependence": weights is not None,
                  "actual_Clifford_B_rank_checked": actual_rank,
                  "native_nested_MOVE": bool(s < spans[189] or spans[189] < s)}
        records.append(record)
        if weights is not None:
            oldzero, d = {}, Q(0)
            for i, q in weights.items():
                add(oldzero, combined[i]["row"], q)
                d += q*combined[i]["delta"]
            need(not oldzero and d == 1, "exact provider relation")
            witness = {"frame_ids": aliases[s], "rank": child_rank,
                       "coefficient_alpha": "1", "target": encoded(target),
                       "terms": [{"bank": "B" if i < len(bankB) else "A", "weight": str(q),
                                  **{k: v for k, v in combined[i].items() if k not in ("row", "delta")},
                                  "old_row": encoded(combined[i]["row"]),
                                  "injection_coefficient": str(combined[i]["delta"])}
                                 for i, q in sorted(weights.items())],
                       "old_row_sum_zero": True, "injection_coefficient_sum": "1"}
            break
    source_bank = banks[spans[3]]
    initial = {o["owner"]: o["row"] for o in source_bank if o["event"] == -1}
    source_control = initial[885].copy()
    add(source_control, initial[943], Q(1))
    need(source_control == target, "rank8 original-source-frame positive control")
    fixture = [{"row": {0: Q(1)}, "delta": Q(0)},
               {"row": {0: Q(1)}, "delta": Q(1)}]
    control, _ = encoded_relation(fixture)
    need(control is not None and sum(control[i]*fixture[i]["delta"] for i in control) == 1,
         "encoded-dependence positive control")
    fixture = [{"row": {0: Q(1)}, "delta": Q(1)},
               {"row": {0: Q(2)}, "delta": Q(2)}]
    control, _ = encoded_relation(fixture)
    need(control is None, "consistent encoding negative control")
    pricing = module("carrier943_budget", ROOT / "budget_price.py")
    price_raw = pricing.INVOICE.read_bytes()
    need(sha256(price_raw).hexdigest() == pricing.PIN, "complete17-call invoice pin")
    price_input = json.loads(price_raw)
    t, p = price_input["after"]["T"], price_input["after"]["P"]
    signed = {r: t.get(r, 0)-p.get(r, 0) for r in t.keys() | p.keys()}
    budget_records = []
    for text in ("0.003647081039689", "0.0038"):
        kappa = Q(text)
        baseline = pricing.moment(signed, kappa)
        f8 = pricing.price(8, kappa)
        required = (-baseline[1]/17, -baseline[0]/17)
        residual = (f8[0]-1-required[1], f8[1]-1-required[0])
        imports = []
        for r in range(9):
            fr = pricing.price(r, kappa)
            gain = (f8[0]-1-fr[1], f8[1]-1-fr[0])
            full = (baseline[0]+17*gain[0], baseline[1]+17*gain[1])
            imports.append({"rank": r, "net_native_saving": pricing.display(gain),
                            "complete_complex_moment": pricing.display(full)})
        if text == "0.0038":
            need(Q(imports[4]["complete_complex_moment"]["exact"][1]) < 0,
                 "even a sole rank4 import exhausts the.0038 budget")
        budget_records.append({"kappa": text, "baseline": pricing.display(baseline),
                               "remaining_native_new_cost_ceiling": pricing.display(residual),
                               "one_import_no_other_new_service": imports})
    return {
        "status": "CONCRETE_OPTIMISTIC_ONE_IMPORT_WITNESS" if witness else
                  "NO_ONE_IMPORT_WITNESS_IN_COMPLETED_DOMAIN" if len(records) == len(eligible) else "PARTIAL_BOUNDED_IMPORT_GATE",
        "source_sha256": PIN, "compiler_sha256": COMPILER_PIN,
        "complete_invoice_sha256": pricing.PIN,
        "injection_cut": INJECT, "candidate_cut": CUT,
        "available_history_coframes": len(banks), "rank_1_to_3_domains": len(eligible),
        "completed_domains": len(records), "coverage_complete": len(records) == len(eligible),
        "domain_rank_histogram": {str(r): sum(t[0] == r for t in eligible) for r in (1, 2, 3)},
        "records": records, "witness": witness, "prefix_seconds": prefix_seconds,
        "seconds": time.monotonic()-start,
        "rank8_source_frame_positive_control": True,
        "encoded_dependence_positive_control": True,
        "consistent_encoding_negative_control": True,
        "directed_optimistic_budgets": budget_records,
        "limits": "One latest scalar injection and ONE arbitrary same-A strict-history combination imported to189. Complete source histories pooled free; actual canonical child B-rank uses frozen geometry formula, permits nonnested ranks2/3 as an optimistic interface overgrant. No backing/ordinary/precision/zero-retag/endpoint admission; no supplier or kappa claim.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seconds", type=int, default=60)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    result = run(a.seconds)
    a.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "rank_1_to_3_domains", "completed_domains", "coverage_complete", "seconds")}))
