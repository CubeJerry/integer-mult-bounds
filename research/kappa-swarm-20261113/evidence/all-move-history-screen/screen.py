#!/usr/bin/env python3
"""Independent exact past/future coframe history check at every owned MOVE.

Research checkpoint, not a new supplier. Exactly72 specified helpers are zero; all other public input rows remain arbitrary.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

ROOT = Path(__file__).resolve().parent
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"


def need(ok, label):
    if not ok:
        raise ValueError(label)


def add(a, b, c):
    need(a is not b, "row alias")
    for k, x in b.items():
        y = a.get(k, 0) + c * x
        if y:
            a[k] = y
        else:
            a.pop(k, None)


def key(frame):
    # Enumerating at most 512 addresses gives an independent canonical key.
    span = {0}
    for v in frame:
        span |= {x ^ v for x in span}
    return tuple(sorted(span))


def reduce(row, basis):
    row = row.copy()
    while row:
        pivot = min(row)
        if pivot not in basis:
            return row
        add(row, basis[pivot], -row[pivot])
    return row


def put(basis, row):
    row = reduce(row, basis)
    if not row:
        return False
    p = min(row)
    a = row[p]
    basis[p] = {k: v / a for k, v in row.items()}
    return True


def run():
    start = time.monotonic()
    raw = (ROOT / "reference/pr7481/WORD.json.gz").read_bytes()
    need(sha256(raw).hexdigest() == PIN, "source byte pin")
    word = json.loads(gzip.decompress(raw))
    frames = list(map(key, word["frames"]))
    events = word["program"]
    cuts = {i: e for i, e in enumerate(events) if e[0] == "MOVE"}
    need(len(cuts) == 6279, "complete MOVE set")
    past = {frames[e[3]]: {} for e in cuts.values()}
    future = {}
    public = word["public"]
    mains = set(word["live"]) | {i+112 for i in word["live"]} | set(word["hosted"]["X2"]) | set(word["hosted"]["Y2"])
    need(len(mains) == 400, "main partition")
    neutral_doc = json.loads((ROOT / 'worker-a/cold-compose/JOINT72-ZERO-CONTACTS.json').read_text())
    need(neutral_doc['source_sha256'] == PIN, 'neutral source pin')
    neutral = set(neutral_doc['cold_helpers']) if '--neutral' in __import__('sys').argv else set()
    need(len(neutral) in (0,72) and not neutral & mains, 'helper-only restrictions')
    rows = [{i: Q(1)} if i not in neutral else {} for i in range(public)] + [None] * word["owned_fields"]
    chart = word["initial"].copy() + [None] * word["owned_fields"]
    departures = []
    answers = {}
    counts = Counter()
    past_controls = 0
    zero_paid = Counter()

    for owner, f in enumerate(word["initial"]):
        if frames[f] in past:
            put(past[frames[f]], rows[owner])

    for i, e in enumerate(events):
        if i % 128 == 0:
            need(time.monotonic() - start < 60, "bounded first-stage runtime")
        op, a = e[:2]
        counts[op] += 1
        if op == "MOVE":
            old, new = e[2:4]
            if not rows[a]: zero_paid[abs(len(word["frames"][old])-len(word["frames"][new]))] += 1
            need(chart[a] == old and rows[a] is not None, "MOVE live source")
            if i in cuts:
                h = past[frames[new]]
                remainder = reduce(rows[a], h)
                past_controls += 1
                if not remainder and rows[a]:
                    answers[i] = {
                    "event": i, "owner": a, "source": old, "destination": new, "owned": e[4],
                    "rank": abs(len(word["frames"][old]) - len(word["frames"][new])),
                    "target": rows[a].copy(), "earlier_B_hit": not remainder,
                    "earlier_B_rank": len(h),
                }
            if frames[old] in future:
                departures.append((i, frames[old], rows[a].copy()))
            chart[a] = new
            if frames[new] in past:
                put(past[frames[new]], rows[a])
        elif op == "INIT":
            need(a >= public and chart[a] is None and rows[a] is None, "owned INIT")
            chart[a], rows[a] = e[2], {}
        elif op == "CLEAR":
            need(a >= public and chart[a] == e[2], "owned CLEAR")
            if frames[e[2]] in future:
                departures.append((i, frames[e[2]], rows[a].copy()))
            chart[a], rows[a] = None, None
        elif op == "SCALE":
            need(chart[a] == e[-1], "scalar chart")
            q = Q(e[2])
            need(q, "nonzero scale")
            rows[a] = {k: q * v for k, v in rows[a].items()}
        elif op in ("ADD", "COPY"):
            b = e[2]
            need(a != b and chart[a] == chart[b] == e[-1], "coframed contact")
            if op == "COPY":
                need(a >= public and not rows[a], "fresh zero COPY")
            add(rows[a], rows[b], Q(e[3]))
        else:
            raise ValueError(op)
    need(chart == word["final"] + [None] * word["owned_fields"], "all endpoints")
    for rec in answers.values():
        rec['target'] = {str(k):str(v) for k,v in sorted(rec['target'].items())}
    lost = Counter(abs(len(word['frames'][word['initial'][h]])-len(word['frames'][word['final'][h]])) for h in neutral)
    need(lost == zero_paid and sum(zero_paid.values()) == len(neutral), 'complete neutral tariff cancellation')
    future_controls = None
    out = {
        "status": "EXACT_ALL_MOVE_HISTORY_DISCOVERY_SCREEN",
        "source_sha256": PIN, "instructions": len(events), "checked_MOVEs": len(cuts),
        "earlier_hits": sum(r["earlier_B_hit"] for r in answers.values()),
        "hits_by_kind": dict(Counter("owned" if r["owned"] else "public" for r in answers.values())), "hits_by_rank": dict(Counter(r["rank"] for r in answers.values())), "main_coordinates": len(mains),
        "strict_history_queries": past_controls, "past_subspaces": len(past),
        "future_subspaces": len(future), "event_counts": dict(counts),
        "seconds": time.monotonic()-start, "records": list(answers.values()),
        "scope": "All original native MOVEs with specified helper zeros; every other public input arbitrary. Strict prior history test. Public destructive replacement/erasure interface unproved. No supplier or kappa.",
        "zero_helpers": sorted(neutral), "lost_targets": dict(lost), "zero_paid": dict(zero_paid),
    }
    (ROOT / ("all-move-history-neutral72.json" if neutral else "all-move-history-original.json")).write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="records"}, indent=2))
    print("first20hits", [(r["event"],r["rank"],r["owned"]) for r in list(answers.values())[:20]])


if __name__ == "__main__":
    run()
