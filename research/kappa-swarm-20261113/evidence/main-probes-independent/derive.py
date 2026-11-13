#!/usr/bin/env python3
"""Independent full-input replay and exact main-only cache separators."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import gzip
import json
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORD_PATH = ROOT / "worker-a/inputs/pr7481-WORD.json.gz"
RESULT_PATH = ROOT / "worker-a/cache-main/RESULT.json"
PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
TIME_CAP = 60.0


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def frame_key(vecs):
    """Canonical GF(2) row RREF, using high-to-low pivots."""
    a = [int(v) for v in vecs if int(v)]
    if not a:
        return ()
    width = max(a).bit_length()
    rank = 0
    for col in range(width - 1, -1, -1):
        hit = next((i for i in range(rank, len(a)) if (a[i] >> col) & 1), None)
        if hit is None:
            continue
        a[rank], a[hit] = a[hit], a[rank]
        pivot = a[rank]
        for i in range(len(a)):
            if i != rank and ((a[i] >> col) & 1):
                a[i] ^= pivot
        rank += 1
    return tuple(sorted(a[:rank]))


def add_sparse(dst, src, scale):
    for k, x in src.items():
        y = dst.get(k, Q(0)) + scale * x
        if y:
            dst[k] = y
        else:
            dst.pop(k, None)


class DenseBasis:
    """Forward echelon basis over Q for 400-coordinate projected rows."""
    def __init__(self, n):
        self.n = n
        self.rows = {}
        self.count = 0

    def insert(self, sparse, coordinate_to_col):
        v = [Q(0)] * self.n
        for coordinate, value in sparse.items():
            j = coordinate_to_col.get(coordinate)
            if j is not None:
                v[j] = value
        for p in range(self.n):
            x = v[p]
            if not x:
                continue
            old = self.rows.get(p)
            if old is None:
                inv = 1 / x
                for j in range(p, self.n):
                    v[j] *= inv
                self.rows[p] = v
                self.count += 1
                return True
            for j in range(p, self.n):
                if old[j]:
                    v[j] -= x * old[j]
        need(not any(v), "basis insertion failed to reduce to zero")
        return False


def project(row, coordinate_to_col, n):
    v = [Q(0)] * n
    for coordinate, value in row.items():
        j = coordinate_to_col.get(coordinate)
        if j is not None:
            v[j] = value
    return v


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def separating_nullvector(basis, target):
    pivots = set(basis.rows)
    free = [j for j in range(basis.n) if j not in pivots]
    for f in free:
        t = [Q(0)] * basis.n
        t[f] = Q(1)
        for p in sorted(pivots, reverse=True):
            row = basis.rows[p]
            t[p] = -sum((row[j] * t[j] for j in range(p + 1, basis.n)), Q(0))
        value = dot(target, t)
        if value:
            denominator = 1
            for x in t:
                denominator = lcm(denominator, x.denominator)
            ints = [int(x * denominator) for x in t]
            common = 0
            for x in ints:
                common = gcd(common, abs(x))
            need(common > 0, "nonzero separator has zero gcd")
            ints = [x // common for x in ints]
            # Fix sign for deterministic certificates.
            first = next(x for x in ints if x)
            if first < 0:
                ints = [-x for x in ints]
            return ints, dot(target, [Q(x) for x in ints])
    return None


def main():
    started = time.monotonic()
    raw = WORD_PATH.read_bytes()
    source_sha = sha256(raw).hexdigest()
    need(source_sha == PIN, "exact source byte hash mismatch")
    word = json.loads(gzip.decompress(raw))
    result_raw = RESULT_PATH.read_bytes()
    a_result = json.loads(result_raw)
    # Deliberately read only A's missed candidate event IDs.
    candidates = [r["event"] for r in a_result["records"] if not r["earlier_B_hit"]]
    need(len(candidates) == 33 and len(set(candidates)) == 33,
         "candidate ID set is not the stated 33 misses")
    events = word["program"]
    need(all(0 <= i < len(events) and events[i][0] == "MOVE" and events[i][4]
             for i in candidates), "candidate ID does not name an owned MOVE")

    mains = (set(word["live"]) | {i + 112 for i in word["live"]} |
             set(word["hosted"]["X2"]) | set(word["hosted"]["Y2"]))
    need(len(mains) == 400 and max(mains) < word["public"], "main set malformed")
    main_order = sorted(mains)
    coordinate_to_col = {coordinate: j for j, coordinate in enumerate(main_order)}
    n = len(main_order)
    frame_keys = [frame_key(f) for f in word["frames"]]

    candidates_by_frame = {}
    candidate_meta = {}
    for event_id in candidates:
        e = events[event_id]
        frame = frame_keys[e[3]]
        candidates_by_frame.setdefault(frame, []).append(event_id)
        candidate_meta[event_id] = {
            "event": event_id,
            "owner": e[1],
            "source_frame": e[2],
            "destination_frame": e[3],
            "destination_key": list(frame),
        }
    for ids in candidates_by_frame.values():
        ids.sort()

    histories = {frame: DenseBasis(n) for frame in candidates_by_frame}
    rows = [{i: Q(1)} for i in range(word["public"])] + [None] * word["owned_fields"]
    chart = word["initial"].copy() + [None] * word["owned_fields"]

    # Initial destination-chart registers are the first observations.
    for owner, frame_id in enumerate(word["initial"]):
        k = frame_keys[frame_id]
        if k in histories:
            histories[k].insert(rows[owner], coordinate_to_col)

    probes = {}
    covered = []
    opcounts = Counter()
    last = -1
    complete = True
    for i, e in enumerate(events):
        last = i
        if i % 128 == 0 and time.monotonic() - started > TIME_CAP:
            complete = False
            break
        op, a = e[:2]
        opcounts[op] += 1
        if op == "MOVE":
            old, new = e[2:4]
            need(rows[a] is not None and chart[a] == old, f"invalid MOVE at {i}")
            new_key = frame_keys[new]
            if i in candidate_meta:
                target = project(rows[a], coordinate_to_col, n)
                answer = separating_nullvector(histories[new_key], target)
                need(answer is not None, f"candidate {i} unexpectedly lies in its main history")
                t, target_dot = answer
                sparse_t = [[main_order[j], x] for j, x in enumerate(t) if x]
                need(all(coordinate in mains for coordinate, _ in sparse_t), "separator escaped main set")
                probes[i] = {
                    **candidate_meta[i],
                    "history_rank": histories[new_key].count,
                    "main_separator": sparse_t,
                    "target_dot": str(target_dot),
                    "history_dot_claim": "zero by exact backsolve",
                }
                covered.append(i)
            chart[a] = new
            if new_key in histories:
                histories[new_key].insert(rows[a], coordinate_to_col)
        elif op == "INIT":
            need(a >= word["public"] and chart[a] is None and rows[a] is None,
                 f"invalid INIT at {i}")
            chart[a], rows[a] = e[2], {}
        elif op == "CLEAR":
            need(a >= word["public"] and chart[a] == e[2] and rows[a] is not None,
                 f"invalid CLEAR at {i}")
            chart[a], rows[a] = None, None
        elif op == "SCALE":
            need(rows[a] is not None and chart[a] == e[-1], f"invalid SCALE at {i}")
            q = Q(e[2])
            need(q != 0, f"zero SCALE at {i}")
            rows[a] = {k: q * v for k, v in rows[a].items() if q * v}
        elif op in ("ADD", "COPY"):
            b = e[2]
            need(a != b and rows[a] is not None and rows[b] is not None and
                 chart[a] == chart[b] == e[-1], f"invalid coframed operation at {i}")
            if op == "COPY":
                need(a >= word["public"] and not rows[a], f"nonfresh COPY at {i}")
            add_sparse(rows[a], rows[b], Q(e[3]))
        else:
            raise ValueError(f"unknown operation {op}")

    need(complete, "full native row replay exceeded 60-second cap")
    need(covered == candidates, "not all 33 candidates were independently separated")
    need(chart == word["final"] + [None] * word["owned_fields"], "final chart mismatch")

    output = {
        "status": "COMPLETE_INDEPENDENT_FULL_NATIVE_REPLAY",
        "source_sha256": source_sha,
        "A_candidate_id_source_sha256": sha256(result_raw).hexdigest(),
        "candidate_event_ids_only_from_A": candidates,
        "main_coordinate_count": len(main_order),
        "main_coordinates_sha256": sha256(json.dumps(main_order, separators=(",", ":")).encode()).hexdigest(),
        "candidate_count": len(probes),
        "candidate_probes": [probes[i] for i in candidates],
        "event_count": len(events),
        "last_event": last,
        "operation_counts": dict(opcounts),
        "construction": "Every native row was replayed over all 1501 public input columns first; each observation was then projected to the independently reconstructed 400-main set. A separate dense exact-Q echelon/backsolve produced integer null vectors.",
        "scope": "33 strict earlier-destination-history nonmembers in the main-only projection; no 14-hit cases or full all-column cache admission examined.",
    }
    (OUT / "PROBES.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "candidate_probes"}, indent=2))
    print("probe supports:", [len(probes[i]["main_separator"]) for i in candidates])
    print("history ranks:", [probes[i]["history_rank"] for i in candidates])
    print("elapsed:", round(time.monotonic() - started, 3))


if __name__ == "__main__":
    main()
