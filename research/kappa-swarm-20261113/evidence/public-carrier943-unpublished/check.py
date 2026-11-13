#!/usr/bin/env python3
"""Bounded exact one-source/one-ADD carrier gate, not a supplier emitter.

Prepared for CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "reference/pr7481/WORD.json.gz"
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
CUT = 40710
INJECT = 35426


def need(ok, why):
    if not ok:
        raise ValueError(why)


def add(a, b, q):
    for j, v in b.items():
        z = a.get(j, Q(0)) + q*v
        if z:
            a[j] = z
        else:
            a.pop(j, None)


def rank(rows):
    basis = {}
    for original in rows:
        row = original.copy()
        while row:
            p = min(row)
            if p not in basis:
                q = row[p]
                basis[p] = {j: v/q for j, v in row.items()}
                break
            add(row, basis[p], -row[p])
    return len(basis)


def encoded(row):
    return {str(j): str(v) for j, v in sorted(row.items())}


def check():
    raw = SOURCE.read_bytes()
    need(sha256(raw).hexdigest() == PIN, "exact native source pin")
    w = json.loads(gzip.decompress(raw))
    need(w["program"][CUT] == ["MOVE", 885, 3, 189, False], "candidate binding")
    need(w["program"][INJECT] == ["MOVE", 943, 3, 105, False], "latest injection cut")
    n, size = w["public"], w["public"] + w["owned_fields"]
    rows = [{h: Q(1)} for h in range(n)] + [None]*w["owned_fields"]
    frames = list(w["initial"]) + [None]*w["owned_fields"]
    delta = [Q(0)]*size
    bank, delta_moves, first_outward, snapshots = [], [], None, {}
    carrier_moves, touches = [], []

    def observe(event, owner, f, kind):
        if f == 189 and owner != 1459:
            bank.append({"event": event, "owner": owner, "frame": f, "kind": kind,
                         "row": rows[owner].copy(), "injection_coefficient": delta[owner]})

    for owner, f in enumerate(frames[:n]):
        observe(-1, owner, f, "initial")
    for event, e in enumerate(w["program"]):
        if event == INJECT:
            need(frames[943] == frames[885] == 3, "legal scalar injection coframe")
            need(rows[943] == {943: Q(2)}, "carrier original value before first MOVE")
            need(rows[885] == {885: Q(1), 943: Q(1)}, "current source885 value")
            # The one injected source value is s=x885+x943. Delta is its
            # scalar coefficient; no physical new source is emitted here.
            delta[943] += 1
            snapshots["injection"] = {"event": event, "source": encoded(rows[885]),
                                       "carrier": encoded(rows[943])}
        if event == CUT:
            snapshots["candidate"] = {"target": rows[885].copy(),
                                      "delta_target": delta[885],
                                      "delta_fields": {r: v for r, v in enumerate(delta) if v}}
        if e[1] == 943 or e[0] in ("ADD", "COPY") and e[2] == 943:
            touches.append({"event": event, "instruction": e})
        op, a = e[:2]
        if event >= INJECT and first_outward is None and op in ("ADD", "COPY") and e[2] == 943:
            first_outward = {"event": event, "instruction": e}
        if op == "MOVE":
            need(frames[a] == e[2], "MOVE frame")
            if a == 943:
                carrier_moves.append({"event": event, "instruction": e})
            if delta[a]:
                delta_moves.append({"event": event, "owner": a, "source": e[2],
                                    "destination": e[3], "rank": abs(len(w["frames"][e[3]])-len(w["frames"][e[2]])),
                                    "coefficient": str(delta[a])})
            frames[a] = e[3]
            if event < CUT:
                observe(event, a, e[3], "arrival")
        elif op == "INIT":
            frames[a], delta[a] = e[2], Q(0)
            if event < CUT:
                rows[a] = {}
        elif op == "CLEAR":
            frames[a], delta[a] = None, Q(0)
            if event < CUT:
                rows[a] = None
        elif op == "SCALE":
            delta[a] *= Q(e[2])
            if event < CUT:
                rows[a] = {j: Q(e[2])*v for j, v in rows[a].items()}
        elif op in ("ADD", "COPY"):
            b, q = e[2], Q(e[3])
            need(frames[a] == frames[b] == e[-1], "scalar common frame")
            delta[a] = (delta[a] if op == "ADD" else Q(0)) + q*delta[b]
            if event < CUT:
                if op == "COPY":
                    rows[a] = {}
                add(rows[a], rows[b], q)
        else:
            raise ValueError(op)
    h = [o["row"] for o in bank]
    z = snapshots["candidate"]["target"]
    b = {885: Q(1)}
    need(len(h) == rank(h) == 2, "two independent available B observations")
    need(rank(h + [z]) == 3, "old target outside available history")
    need(rank(h + [z, b]) == 4, "pre30780 source also independent modulo history and target")
    need(z == {885: Q(1), 943: Q(1)}, "old target row")
    need(snapshots["candidate"]["delta_target"] == 0, "late injection leaves target unchanged")
    need(first_outward == {"event": 35427, "instruction": ["ADD", 663, 943, "-1/2", 105]},
         "first outward carrier use")
    need(all(o["event"] < CUT for o in bank), "strict historical clock")
    need(not any(1459 in row for row in h + [z]), "demoted entrance not used as backing")
    # Every one-ADD injection before943 leaves frame3 has source either b
    # (before30780) or z (after30780). By linearity every changed row is its
    # old row plus a scalar multiple of that one source. The exact two rank
    # increments prove target nonmembership for every coefficient and time.
    controls = []
    for q in (Q(-2), Q(-1), Q(0), Q(1), Q(2), Q(7, 3)):
        tilted = []
        for o in bank:
            row = o["row"].copy()
            add(row, z, q*o["injection_coefficient"])
            tilted.append(row)
        need(rank(tilted) == 2 and rank(tilted + [z]) == 3, "exact late-injection samples")
    controls.append({"name": "six_exact_coefficients", "passed": True})
    old = [{0: Q(1)}, {0: Q(1)}]
    changed = [{0: Q(1)}, {0: Q(1), 1: Q(1)}]
    need(rank(old) == 1 and rank(changed) == rank(changed + [{1: Q(1)}]) == 2,
         "inconsistent duplicate observations can expose the injected source")
    controls.append({"name": "duplicate_old_history_with_different_encoding_can_enable_cache",
                     "passed": True, "why": "independence/consistent temporal backing is essential"})
    final = [{"owner": r, "frame": frames[r], "dimension": len(w["frames"][frames[r]]),
              "coefficient": str(v)} for r, v in enumerate(delta) if v]
    return {
        "status": "EXACT_ONE_ADD_INJECTION_CACHE_OBSTRUCTION",
        "source_head": "89eaa9d8cae37c1540de98f2d29a3abaabb96a2b",
        "word_sha256": PIN, "candidate_event": CUT,
        "latest_injection_before": INJECT,
        "all_legal_one_ADD_insertion_cuts": [0, INJECT],
        "cut_interval_inclusive": True,
        "coefficients_covered": "all real or complex scalar coefficients by the exact rank argument",
        "available_history_rank": 2, "history_plus_old_target_rank": 3,
        "history_plus_old_target_and_early_source_rank": 4,
        "available_B_history": [{**{k: v for k, v in o.items() if k not in ("row", "injection_coefficient")},
                                 "row": encoded(o["row"]),
                                 "late_injection_coefficient": str(o["injection_coefficient"])} for o in bank],
        "old_target": encoded(z), "early_source": encoded(b),
        "latest_injection_snapshot": snapshots["injection"],
        "latest_candidate_delta_fields": encoded(snapshots["candidate"]["delta_fields"]),
        "first_outward_use": first_outward,
        "carrier943_moves": carrier_moves,
        "carrier943_touches": touches,
        "changed_dependency_MOVEs_before_candidate": [e for e in delta_moves if e["event"] < CUT],
        "changed_dependency_MOVEs_total": len(delta_moves),
        "latest_injection_unrepaired_final_fields": final,
        "latest_injection_unrepaired_final_count": len(final),
        "controls": controls,
        "limits": "One scalar ADD from current885 into943 at a common empty-frame cut, all other pre-cut operations fixed, no new paid import and no free demoted1459 backing. No conclusion about multiple edits, additional histories/imports, endpoint repairs, typed zero reframe or a complete supplier.",
        "new_native_word_emitted": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = check()
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "history_rank": result["available_history_rank"],
                      "rank_with_target_and_early_source": result["history_plus_old_target_and_early_source_rank"],
                      "first_outward_use": result["first_outward_use"],
                      "unrepaired_final_fields": result["latest_injection_unrepaired_final_count"]}))
