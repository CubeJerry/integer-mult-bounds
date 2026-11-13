#!/usr/bin/env python3
"""Independent exact past/future coframe history check at every owned MOVE.

Research checkpoint, not a new supplier. Only the400main coordinates are propagated; helpers project to zero.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

ROOT = Path("/workspace/scratch/19b21bdb3d72")
OUT = Path(__file__).resolve().parent
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
    cuts = {i: e for i, e in enumerate(events) if e[0] == "MOVE" and e[4]}
    need(len(cuts) == 47, "complete owned-MOVE set")
    past = {frames[e[3]]: {} for e in cuts.values()}
    future = {frames[e[2]]: {} for e in cuts.values()}
    public = word["public"]
    mains=set(word["live"])|{i+112 for i in word["live"]}|set(word["hosted"]["X2"])|set(word["hosted"]["Y2"])
    need(len(mains)==400,"exact main-coordinate set")
    rows = [{i: Q(1)} if i in mains else {} for i in range(public)] + [None] * word["owned_fields"]
    chart = word["initial"].copy() + [None] * word["owned_fields"]
    departures = []
    answers = {}
    counts = Counter()
    past_controls = 0

    for owner, f in enumerate(word["initial"]):
        if frames[f] in past:
            put(past[frames[f]], rows[owner])

    complete=True
    last=-1
    for i, e in enumerate(events):
        last=i
        if i % 128 == 0:
            if time.monotonic()-start>=60:
                complete=False
                break
        op, a = e[:2]
        counts[op] += 1
        if op == "MOVE":
            old, new = e[2:4]
            need(chart[a] == old and rows[a] is not None, "MOVE live source")
            if i == 48865:
                need(e == ["MOVE", 1343, 252, 127, False], "public zero occurrence")
                need(rows[a] == {}, "helper-only public row projects to zero")
            if i in cuts:
                h = past[frames[new]]
                remainder = reduce(rows[a], h)
                trial = {p: r.copy() for p, r in h.items()}
                if remainder:
                    need(put(trial, rows[a]), "inserted target raises rank")
                need(not reduce(rows[a], trial), "inserted target becomes member")
                need(not h or not reduce(h[min(h)], h), "existing history member")
                past_controls += 1
                answers[i] = {
                    "event": i, "owner": a, "source": old, "destination": new,
                    "rank": abs(len(word["frames"][old]) - len(word["frames"][new])),
                    "target": rows[a].copy(), "earlier_B_hit": not remainder,
                    "earlier_B_rank": len(h), "main_target_zero":not rows[a],
                    "main_remainder":remainder.copy(),
                    "basis_at_cut":{p:r.copy() for p,r in h.items()},
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
    if complete:need(chart==word['final']+[None]*word['owned_fields'],'all endpoints')
    for rec in answers.values():
        rec['target']={str(k):str(v)for k,v in sorted(rec['target'].items())}
        rec['main_remainder']={str(k):str(v)for k,v in sorted(rec['main_remainder'].items())}
        rec['basis_at_cut']={str(p):{str(k):str(v)for k,v in sorted(row.items())}for p,row in rec['basis_at_cut'].items()}
    survivors=[{'event':r['event'],'owner':r['owner'],'rank':r['rank'],'main_target_zero':r['main_target_zero']}for r in answers.values()if r['earlier_B_hit']]
    result={'status':'COMPLETE_EXACT_MAIN_PROJECTION_FILTER'if complete else 'PARTIAL_MAIN_PROJECTION_TIME_CAP','source_sha256':PIN,'expected_owned_cuts':47,'covered_owned_cuts':len(answers),'last_event':last,'main_coordinates':sorted(mains),'main_projection_survivors':survivors,'survivor_count':len(survivors),'obstructed_count':sum(not r['earlier_B_hit']for r in answers.values()),'self_insertion_controls':past_controls,'seconds':time.monotonic()-start,'records':list(answers.values()),'scope':'Strictly earlier pooled destination histories projected onto400arbitrary mains. Helper-only input restrictions cannot repair a main-projection nonspan. Survivors are only necessary candidates; no cache provider/source/kappa.'}
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in('records','main_coordinates')},indent=2))


if __name__ == "__main__":
    run()
