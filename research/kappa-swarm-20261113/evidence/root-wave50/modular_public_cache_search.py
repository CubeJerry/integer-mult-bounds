#!/usr/bin/env python3
"""Finite-field discovery only, followed by exact verification for any hit.

A modular miss is NOT reported as rational nonmembership: history rank may
drop modulo a prime. No negative theorem follows from an empty hit list.
"""
from collections import Counter
from hashlib import sha256
from fractions import Fraction
from pathlib import Path
from math import isqrt
import gzip
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
PRIME = 1000003
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def add(row, other, q):
    for h, a in other.items():
        v = (row.get(h, 0)+q*a) % PRIME
        if v:
            row[h] = v
        else:
            row.pop(h, None)


def reduce(row, basis):
    row = row.copy()
    while row:
        p = min(row)
        if p not in basis:
            break
        add(row, basis[p], -row[p])
    return row


def insert(row, basis):
    v = reduce(row, basis)
    if v:
        p = min(v)
        q = pow(v[p], -1, PRIME)
        basis[p] = {h: q*a % PRIME for h, a in v.items()}


def frame_key(f):
    s = {0}
    for v in f:
        s |= {u ^ v for u in s}
    return tuple(sorted(s))


def run():
    start = time.monotonic()
    need(all(PRIME % d for d in range(2, isqrt(PRIME)+1)), "prime modulus")
    raw = (ROOT/"reference/pr7481/WORD.json.gz").read_bytes()
    need(sha256(raw).hexdigest() == PIN, "native source pin")
    w = json.loads(gzip.decompress(raw))
    screen = json.loads((ROOT/"all-move-support-result.json").read_text())
    need(screen["source_sha256"] == PIN and screen["moves"] == 6279, "coordinate-screen source")
    neutral_mode = "--neutral" in sys.argv
    full_mode = "--full" in sys.argv or neutral_mode
    all_queries = "--all" in sys.argv or full_mode
    queries = {r["event"]: r for r in screen["candidates"]
               if all_queries or not r["owned"] and r["rank"] >= 4}
    if full_mode:
        queries = {i: dict(event=i, literal=e,
                          rank=abs(len(w["frames"][e[2]])-len(w["frames"][e[3]])))
                   for i, e in enumerate(w["program"]) if e[0] == "MOVE"}
    frames = list(map(frame_key, w["frames"]))
    banks = {frames[r["literal"][3]]: {} for r in queries.values()}
    generator_count = {f: 0 for f in banks}
    n = w["public"]
    neutral = set()
    exact_zero_events = set()
    zero_record_pin = None
    if neutral_mode:
        nd = json.loads((ROOT/"worker-a/cold-compose/JOINT72-ZERO-CONTACTS.json").read_text())
        need(nd["source_sha256"] == PIN, "neutral-set source")
        neutral = set(nd["cold_helpers"])
        need(len(neutral) == 72, "exact neutral set")
        zr_raw = (ROOT/"worker-b/helper-graph/ROWS.json").read_bytes()
        zero_record_pin = sha256(zr_raw).hexdigest()
        need(zero_record_pin == "15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834",
             "independently reconstructed exact zero-row receipt")
        zr = json.loads(zr_raw)
        need(zr["source_sha256"] == PIN, "zero-row native binding")
        removed = [r for r in zr["records"] if set(map(int, r["row"])) <= neutral]
        need(len(removed) == 72 and all(len(r["row"]) == 1 for r in removed), "72 singleton zero rows")
        need({int(h) for r in removed for h in r["row"]} == neutral, "bijection of zero rows and neutral helpers")
        need(all(r["rank"] == zr["targets"][next(iter(r["row"]))] for r in removed),
             "each lost target exactly cancels its zero MOVE price")
        exact_zero_events = {r["event"] for r in removed}
    rows = [{h: 1} if h not in neutral else {} for h in range(n)]+[None]*w["owned_fields"]
    current = w["initial"].copy()+[None]*w["owned_fields"]
    for h, f in enumerate(w["initial"]):
        if frames[f] in banks:
            insert(rows[h], banks[frames[f]])
            generator_count[frames[f]] += bool(rows[h])
    scalars = {}
    done = []
    hits = []
    controls = 0
    complete = True
    for event, ins in enumerate(w["program"]):
        if time.monotonic()-start > 45:
            complete = False
            break
        op, a = ins[:2]
        if op == "MOVE":
            old, new = ins[2:4]
            need(current[a] == old and rows[a] is not None, "MOVE source")
            if event in queries:
                bank = banks[frames[new]]
                if event in exact_zero_events:
                    need(not rows[a], "exact zero event reduces to zero")
                hit = not reduce(rows[a], bank)
                record = dict(event=event, literal=ins, rank=queries[event]["rank"],
                              history_rank_mod_prime=len(bank), hit_mod_prime=hit,
                              original_history_generator_count=generator_count[frames[new]],
                              rational_nonmembership_certified=(not hit and len(bank) == generator_count[frames[new]]),
                              zero_mod_prime=not rows[a])
                done.append(record)
                if hit:
                    hits.append(record)
            current[a] = new
            if frames[new] in banks:
                insert(rows[a], banks[frames[new]])
                generator_count[frames[new]] += event not in exact_zero_events
                if event in queries:
                    need(not reduce(rows[a], banks[frames[new]]), "inserted-arrival control")
                    controls += 1
        elif op == "INIT":
            need(a >= n and current[a] is None and rows[a] is None, "INIT")
            current[a], rows[a] = ins[2], {}
        elif op == "CLEAR":
            need(a >= n and current[a] == ins[2] and rows[a] is not None, "CLEAR")
            current[a], rows[a] = None, None
        else:
            value = ins[2] if op == "SCALE" else ins[3]
            if value not in scalars:
                q = Fraction(value)
                need(q.denominator % PRIME and q.numerator % PRIME, "valid nonzero scalar reduction")
                scalars[value] = q.numerator*pow(q.denominator, -1, PRIME) % PRIME
            q = scalars[value]
            if op == "SCALE":
                need(current[a] == ins[3], "SCALE chart")
                rows[a] = {h: q*x % PRIME for h, x in rows[a].items()}
            elif op in ("ADD", "COPY"):
                b = ins[2]
                need(a != b and current[a] == current[b] == ins[4], "ordinary chart")
                if op == "COPY":
                    need(a >= n and not rows[a], "COPY zero destination")
                add(rows[a], rows[b], q)
            else:
                raise ValueError("unknown instruction")
    if complete:
        need(current == w["final"]+[None]*w["owned_fields"], "complete final map")
        need(len(done) == len(queries), "all selected queries completed")
    out = dict(status="COMPLETE_MODULAR_DISCOVERY_ONLY" if complete else "PARTIAL_MODULAR_DISCOVERY_ONLY",
        source_sha256=PIN, prime=PRIME, chosen_query_count=len(queries),
        chosen_destination_classes=len(banks), completed_queries=len(done),
        completed_through_event=event, full_source_replay=complete,
        inserted_arrival_controls=controls, hits=hits, queries=done,
        neutral_helpers=sorted(neutral), nonzero_hits=sum(not x["zero_mod_prime"] for x in hits),
        exact_zero_events=sorted(exact_zero_events), zero_record_sha256=zero_record_pin,
        rational_nonmembership_certified=sum(x["rational_nonmembership_certified"] for x in done),
        unresolved_queries=sum(not x["rational_nonmembership_certified"] for x in done),
        seconds=time.monotonic()-start,
        scope="Original arbitrary inputs; coordinate-screen survivors. A modular miss proves rational nonmembership ONLY when the history rank reaches its original generator-count upper bound. Other misses remain unresolved; hits need exact membership. No new kappa.")
    output = ("modular-neutral72-cache-result.json" if neutral_mode else
              "modular-full-cache-result.json" if full_mode else
              "modular-all-cache-result.json" if all_queries else "modular-public-cache-result.json")
    (ROOT/output).write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in ("queries", "hits", "neutral_helpers", "exact_zero_events")}
                     | {"hit_count":len(hits), "exact_zero_count":len(exact_zero_events)}, indent=2))


if __name__ == "__main__":
    run()
