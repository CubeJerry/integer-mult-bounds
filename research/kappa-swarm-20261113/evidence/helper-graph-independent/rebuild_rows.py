#!/usr/bin/env python3
"""Rebuild exact helper-only MOVE rows from the pinned native word."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORD_PATH = ROOT / "worker-a/inputs/pr7481-WORD.json.gz"
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
B_ROWS_PATH = ROOT / "worker-b/helper-graph/ROWS.json"
B_ROWS_PIN = "15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834"
TIME_CAP = 60.0


def need(ok, label):
    if not ok:
        raise AssertionError(label)


def guard(actual, expected):
    if actual != expected:
        raise ValueError("source pin mismatch")


def add(dst, src, q):
    for k, v in src.items():
        z = dst.get(k, Q(0)) + q * v
        if z:
            dst[k] = z
        else:
            dst.pop(k, None)


def gf2_rank(vectors):
    basis = {}
    for raw in vectors:
        x = int(raw)
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def main():
    start = time.monotonic()
    raw = WORD_PATH.read_bytes()
    source_sha = sha256(raw).hexdigest()
    guard(source_sha, PIN)
    w = json.loads(gzip.decompress(raw))
    n = w["public"]
    need(all(gf2_rank(frame) == len(frame) for frame in w["frames"]),
         "frame list contains a dependent basis")
    mains = (set(w["live"]) | {i + 112 for i in w["live"]} |
             set(w["hosted"]["X2"]) | set(w["hosted"]["Y2"]))
    need(len(mains) == 400, "main-coordinate count")
    helpers = set(range(n)) - mains
    need(len(helpers) == 1101, "helper-coordinate count")
    targets = {h: len(w["frames"][w["final"][h]]) -
               len(w["frames"][w["initial"][h]]) for h in helpers}
    need(all(r > 0 for r in targets.values()), "positive original helper target rank")

    # Unlike the main-projection audit, keep all 1501 latent input columns.
    rows = [{i: Q(1)} for i in range(n)] + [None] * w["owned_fields"]
    charts = w["initial"].copy() + [None] * w["owned_fields"]
    fresh = set()
    records = []
    other_moves = 0
    opcounts = Counter()
    for event, e in enumerate(w["program"]):
        if event % 128 == 0 and time.monotonic() - start > TIME_CAP:
            raise TimeoutError("full native row replay exceeded 60-second cap")
        op, a = e[:2]
        opcounts[op] += 1
        if op == "MOVE":
            old, new = e[2:4]
            need(rows[a] is not None and charts[a] == old, f"invalid MOVE {event}")
            need(bool(e[4]) == (a >= n), f"owner flag mismatch {event}")
            need(rows[a], f"zero-support MOVE {event}")
            if not (set(rows[a]) & mains):
                need(set(rows[a]) <= helpers, "main-free row has non-helper support")
                paid = abs(len(w["frames"][old]) - len(w["frames"][new]))
                records.append({
                    "event": event,
                    "owner": a,
                    "owned": bool(e[4]),
                    "rank": paid,
                    "row": {str(h): str(v) for h, v in sorted(rows[a].items())},
                })
            else:
                need(any(h in mains and q for h, q in rows[a].items()),
                     f"excluded row has no nonzero main coefficient {event}")
                other_moves += 1
            charts[a] = new
            fresh.discard(a)
        elif op == "INIT":
            need(a >= n and charts[a] is None and rows[a] is None, f"invalid INIT {event}")
            charts[a], rows[a] = e[2], {}
            fresh.add(a)
        elif op == "CLEAR":
            need(a >= n and charts[a] == e[2] and rows[a] is not None, f"invalid CLEAR {event}")
            charts[a], rows[a] = None, None
            fresh.discard(a)
        elif op == "SCALE":
            need(rows[a] is not None and charts[a] == e[-1], f"invalid SCALE {event}")
            q = Q(e[2])
            need(q != 0, f"zero SCALE {event}")
            rows[a] = {h: q * v for h, v in rows[a].items() if q * v}
            fresh.discard(a)
        elif op in ("ADD", "COPY"):
            b = e[2]
            need(a != b and rows[a] is not None and rows[b] is not None and
                 charts[a] == charts[b] == e[-1], f"invalid {op} {event}")
            if op == "COPY":
                need(a >= n and a in fresh and not rows[a], f"COPY not into fresh zero {event}")
            add(rows[a], rows[b], Q(e[3]))
            fresh.discard(a)
        else:
            raise ValueError(f"unknown operation {op}")

    need(charts == w["final"] + [None] * w["owned_fields"], "final chart/lifetime mismatch")
    need(all(rows[h] == {h: Q(1)} for h in helpers), "helper endpoint is not its original input")
    need(all(not (set(rows[m]) & helpers) for m in mains), "main endpoint depends on helper inputs")
    need(len(records) == 468 and other_moves == 5811, "source MOVE partition mismatch")
    used = sorted({int(h) for rec in records for h in rec["row"]})
    need(len(used) == 806, "used helper support width mismatch")
    target_by_helper = {str(h): targets[h] for h in used}
    for rec in records:
        hs = [int(h) for h in rec["row"]]
        need(hs and rec["rank"] <= min(targets[h] for h in hs),
             f"support target rank fails paid rank at MOVE {rec['event']}")

    # Independent extraction is complete. Compare to B's frozen JSON only as a
    # final consistency check; the coefficients used above came from replay.
    braw = B_ROWS_PATH.read_bytes()
    guard(sha256(braw).hexdigest(), B_ROWS_PIN)
    bdoc = json.loads(braw)
    b_records = [{k: r[k] for k in ("event", "owner", "owned", "rank", "row")}
                 for r in bdoc["records"]]
    need(records == b_records, "replayed native rows differ from frozen B rows")
    need({str(h): targets[h] for h in helpers} == bdoc["targets"],
         "replayed helper target ranks differ from B mapping")

    # A specific executed source-mismatch negative control.
    source_mismatch_rejected = False
    try:
        guard(source_sha, "0" * 64)
    except ValueError as exc:
        source_mismatch_rejected = str(exc) == "source pin mismatch"
    need(source_mismatch_rejected, "wrong source pin was not rejected")

    out = {
        "status": "PASS_INDEPENDENT_EXACT_NATIVE_ROW_REBUILD",
        "source_sha256": source_sha,
        "b_rows_sha256": sha256(braw).hexdigest(),
        "public_inputs": n,
        "main_count": len(mains),
        "helper_count": len(helpers),
        "main_free_move_rows": len(records),
        "nonzero_main_move_rows": other_moves,
        "used_helper_columns": len(used),
        "helper_targets": target_by_helper,
        "records": records,
        "operation_counts": dict(opcounts),
        "owner_lifetimes_and_all_input_endpoints_checked": True,
        "all_frame_lists_confirmed_independent_GF2_bases": True,
        "all_468_paid_ranks_le_support_target_ranks": True,
        "replayed_records_match_frozen_b_output": True,
        "controls": {"source_mismatch_rejected_by_executed_guard": source_mismatch_rejected},
        "scope": "Exact original #7481 helper-only MOVE rows; no changed source or physical construction.",
    }
    (OUT / "REBUILT-ROWS.json").write_text(json.dumps(out, indent=2) + "\n")
    compact = {k: v for k, v in out.items() if k not in ("records", "helper_targets")}
    print(json.dumps(compact, indent=2))
    print("elapsed_seconds:", round(time.monotonic() - start, 3))


if __name__ == "__main__":
    main()
