#!/usr/bin/env python3
"""Bounded all-MOVE information screen using exact coordinate separators.

Missing support is a proved history exclusion. A surviving support test is
only an unresolved candidate for exact row-space membership, never a cache.
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


def need(ok, why):
    if not ok:
        raise ValueError(why)


def span(frame):
    out = {0}
    for x in frame:
        need(x not in out and 0 < x < 512, "independent frame basis")
        out |= {v ^ x for v in out}
    return tuple(sorted(out))


def add(a, b, q):
    for h, x in b.items():
        z = a.get(h, Q(0))+q*x
        if z:
            a[h] = z
        else:
            a.pop(h, None)


def run():
    start = time.monotonic()
    raw = (ROOT/"reference/pr7481/WORD.json.gz").read_bytes()
    need(sha256(raw).hexdigest() == PIN, "exact source bytes")
    w = json.loads(gzip.decompress(raw))
    frames = list(map(span, w["frames"]))
    n = w["public"]
    rows = [{h: Q(1)} for h in range(n)]+[None]*w["owned_fields"]
    current = w["initial"].copy()+[None]*w["owned_fields"]
    support = {f: 0 for f in frames}
    for h, f in enumerate(w["initial"]):
        support[frames[f]] |= 1 << h
    exclusions = []
    survivors = []
    ops = Counter()
    for event, ins in enumerate(w["program"]):
        need(time.monotonic()-start < 60, "bounded source screen")
        op, a = ins[:2]
        ops[op] += 1
        if op == "MOVE":
            old, new, owned = ins[2:]
            need(current[a] == old and rows[a] is not None and owned == (a >= n),
                 "MOVE owner/source binding")
            fa, fb = set(frames[old]), set(frames[new])
            need(fa < fb or owned and fb < fa, "actual nested MOVE rank")
            mask = sum(1 << h for h in rows[a])
            missing = mask & ~support[frames[new]]
            rec = dict(event=event, literal=ins, rank=abs(len(w["frames"][old])-len(w["frames"][new])),
                       owned=owned, target_support=len(rows[a]), earlier_support=support[frames[new]].bit_count())
            if missing:
                h = (missing & -missing).bit_length()-1
                rec.update(probe_coordinate=h, target_value=str(rows[a][h]))
                exclusions.append(rec)
            else:
                rec["target"] = {str(h): str(v) for h, v in rows[a].items()}
                survivors.append(rec)
            # The querying MOVE must not contribute its own arrival to its history.
            support[frames[new]] |= mask
            current[a] = new
        elif op == "INIT":
            need(a >= n and current[a] is None and rows[a] is None, "owned INIT")
            current[a], rows[a] = ins[2], {}
        elif op == "CLEAR":
            need(a >= n and current[a] == ins[2] and rows[a] is not None, "owned CLEAR")
            current[a], rows[a] = None, None
        elif op == "SCALE":
            need(current[a] == ins[3] and rows[a] is not None, "SCALE coframe")
            q = Q(ins[2]); need(q, "nonzero scale")
            rows[a] = {h: q*x for h, x in rows[a].items()}
        elif op in ("ADD", "COPY"):
            b = ins[2]
            need(a != b and current[a] == current[b] == ins[4], "ordinary coframe")
            if op == "COPY":
                need(a >= n and not rows[a], "COPY into owned zero")
            add(rows[a], rows[b], Q(ins[3]))
        else:
            raise ValueError("unknown instruction")
    need(current == w["final"]+[None]*w["owned_fields"], "final frames/lifecycles")
    need(len(exclusions)+len(survivors) == ops["MOVE"] == 6279, "complete MOVE coverage")
    out = dict(status="COMPLETE_COORDINATE_SEPARATOR_SCREEN_ONLY", source_sha256=PIN,
        events=len(w["program"]), moves=6279, exclusions=len(exclusions), survivors=len(survivors),
        surviving_public=sum(not x["owned"] for x in survivors),
        surviving_owned=sum(x["owned"] for x in survivors),
        survivor_rank_histogram=dict(sorted(Counter(x["rank"] for x in survivors).items())),
        survivor_destination_classes=len({frames[x["literal"][3]] for x in survivors}),
        excluded=exclusions, candidates=survivors, seconds=time.monotonic()-start,
        scope="All original inputs arbitrary. Exact coordinate annihilators exclude listed cuts. Remaining cuts have no established history membership or physical cache implementation.")
    (ROOT/"all-move-support-result.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in ("excluded", "candidates")}, indent=2))


if __name__ == "__main__":
    run()
