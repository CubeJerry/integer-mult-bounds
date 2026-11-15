#!/usr/bin/env python3
"""Exact source-bound two-facet acquisition through recoded original carriers.

All values are coefficient bitsets in the 222 independent original columns.
The finite geometry uses rational arithmetic. This is a partial interface;
no unserved Y is called a completed target and no movement margin is admission.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


def rank_q(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    k = 0
    for c in range(8):
        pivot = next((i for i in range(k, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        p = a[k][c]
        a[k] = [x / p for x in a[k]]
        for i in range(k + 1, len(a)):
            p = a[i][c]
            if p:
                a[i] = [x - p * y for x, y in zip(a[i], a[k])]
        k += 1
    return k


def rank_f2(rows):
    basis = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p] = row
                break
    return len(basis)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mask(indices):
    return sum(1 << i for i in indices)


def source_geometry(root):
    recovery = root / "research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
    raw = recovery.read_bytes()
    actual_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if actual_blob != "8eba43d142c819c206dce5df87ea4571aaead287":
        raise ValueError("Recovered native geometry Git blob mismatch")
    geometry = json.loads(raw)
    roots = geometry["native_roots"]
    if len(roots) != 111:
        raise ValueError("Native role count mismatch")
    # The singular pivot is the sum of actual root 72 and this omitted normal.
    # Its characteristic-two functional equals real pairing parity with both.
    omitted = [0, 0, 1, 1, 0, 0, 1, -1]
    h = [((dot(roots[72], r) // 2) + (dot(omitted, r) // 2)) % 2 for r in roots]
    if [h.count(0), h.count(1)] != [52, 59]:
        raise ValueError("Singular partition mismatch")
    return roots, h, {
        "source_recovery_git_blob": actual_blob,
        "source_recovery_sha256": hashlib.sha256(raw).hexdigest(),
        "native_gzip_sha256": geometry["native_source_sha256"],
        "native_gzip_replayed_by_this_checker": False,
    }


def build_word(roots, h, a=1, b=3, seed_kind="zero", closed=False):
    if a == b or h[a] or h[b]:
        raise ValueError("Need two distinct class-zero receiver normals")
    supports = [{j for j, r in enumerate(roots) if h[j] and dot(roots[i], r) == 0} for i in (a, b)]
    common = supports[0] & supports[1]
    exclusive = [supports[i] - common for i in range(2)]
    donors = [j for j, r in enumerate(roots) if not h[j] and dot(roots[a], r) == dot(roots[b], r) == 0]
    if len(donors) < 2 or not common:
        raise ValueError("Missing two disjoint-class original donor carriers")
    donors = donors[:2]
    if rank_q([roots[a], roots[b]]) != 2:
        raise ValueError("Facet normals not independent")
    charts = {"zero": {"kind": "span", "rows": []}, "Hub": {"kind": "ann", "rows": []},
              "D": {"kind": "ann", "rows": [roots[a], roots[b]]},
              "Fa": {"kind": "ann", "rows": [roots[a]]},
              "Fb": {"kind": "ann", "rows": [roots[b]]}}
    for j, r in enumerate(roots):
        charts[f"L{j}"] = {"kind": "span", "rows": [r]}
        charts[f"F{j}"] = {"kind": "ann", "rows": [r]}
    ops = []
    moved = sorted(set.union(*supports) | set(donors))
    # These are real stationary point copies, not an allowance to ascend later.
    for j in moved:
        ops += [["INIT", f"R{j}", f"L{j}"], ["ADD", f"X{j}", f"R{j}"]]
    ops += [["INIT", "Z", "D"], ["INIT", "Ca", "Fa"], ["INIT", "Cb", "Fb"]]
    for j in sorted(common):
        ops += [["MOVE", f"X{j}", "D"], ["ADD", f"X{j}", "Z"], ["MOVE", f"X{j}", "Hub"]]
    # Every original donor is outside the spinor sources, so ZU=0 literally.
    for d in donors:
        ops += [["MOVE", f"X{d}", "D"], ["ADD", "Z", f"X{d}"]]
    for side, donor, private in zip(("a", "b"), donors, exclusive):
        ops += [["MOVE", f"X{donor}", f"F{side}"], ["ADD", f"X{donor}", f"C{side}"], ["MOVE", f"X{donor}", "Hub"]]
        for j in sorted(private):
            ops += [["MOVE", f"X{j}", f"F{side}"], ["ADD", f"X{j}", f"C{side}"], ["MOVE", f"X{j}", "Hub"]]
    acquisition_marker = len(ops)
    # Restore both original carriers by their now actually available pure sources.
    for d in donors:
        for j in sorted(common):
            ops += [["ADD", f"X{j}", f"X{d}"]]
    restored_marker = len(ops)
    seeds = []
    for i in (a, b):
        if seed_kind == "zero":
            seeds.append(set())
        elif seed_kind == "canonical":
            seeds.append({j for j, r in enumerate(roots) if j == i or dot(roots[i], r) == 0})
        else:
            raise ValueError("Unknown seed kind")
    # Additional pure original reads needed by canonical seed rows are paid.
    extra_seed_sources = sorted(set.union(*seeds) - set(moved))
    for j in extra_seed_sources:
        ops += [["INIT", f"R{j}", f"L{j}"], ["ADD", f"X{j}", f"R{j}"], ["MOVE", f"X{j}", "Hub"]]
    moved = sorted(set(moved) | set(extra_seed_sources))
    for side, donor, seed in zip(("a", "b"), donors, seeds):
        ops += [["INIT", f"P{side}", "Hub"]]
        for j in sorted(seed):
            ops += [["ADD", f"X{j}", f"P{side}"]]
        ops += [["MOVE", f"P{side}", f"F{side}"], ["ADD", f"C{side}", f"P{side}"],
                ["MOVE", f"P{side}", f"L{donor}"], ["ADD", f"R{donor}", f"P{side}"],
                ["MOVE", f"P{side}", "zero"]]
    handoff_marker = len(ops)
    live_expected = {"Z": ("D", mask(common)),
                     "Ca": ("Fa", mask(supports[0]) ^ (1 << donors[0])),
                     "Cb": ("Fb", mask(supports[1]) ^ (1 << donors[1])),
                     "Pa": ("zero", mask(seeds[0] ^ supports[0])),
                     "Pb": ("zero", mask(seeds[1] ^ supports[1]))}
    live_expected.update({f"R{j}": (f"L{j}", 1 << j) for j in moved})
    if closed:
        for name in live_expected:
            ops += [["CLEAR", name]]
        for j in range(111):
            if j not in moved:
                ops += [["MOVE", f"X{j}", "Hub"]]
            ops += [["MOVE", f"Y{j}", f"F{j}"]]
    return {"schema": "shared-facet-source-v1", "facets": [a, b], "donors": donors,
            "source_sets": {"common": sorted(common), "exclusive": [sorted(x) for x in exclusive], "modes": [sorted(x) for x in supports]},
            "seed_kind": seed_kind, "seed_sets": [sorted(x) for x in seeds],
            "moved_original_sources": moved, "closed_partial": closed,
            "charts": charts, "operations": ops,
            "markers": {"acquired": acquisition_marker, "restored": restored_marker, "handoff": handoff_marker},
            "expected_owned_at_handoff": {k: {"chart": c, "value_hex": hex(v)} for k, (c, v) in live_expected.items()},
            "completed_targets": [], "new_complete_kappa": False}


def replay(word, roots):
    charts = word["charts"]
    dims = {name: rank_q(c["rows"]) if c["kind"] == "span" else 8 - rank_q(c["rows"]) for name, c in charts.items()}
    def included(a, b):
        ca, cb = charts[a], charts[b]
        if ca["kind"] == cb["kind"] == "ann":
            return rank_q(ca["rows"] + cb["rows"]) == rank_q(ca["rows"])
        if ca["kind"] == cb["kind"] == "span":
            return rank_q(ca["rows"] + cb["rows"]) == rank_q(cb["rows"])
        if ca["kind"] == "span" and cb["kind"] == "ann":
            return all(dot(x, y) == 0 for x in ca["rows"] for y in cb["rows"])
        if ca["kind"] == "ann" and cb["kind"] == "span" and not cb["rows"]:
            return rank_q(ca["rows"]) == 8
        raise ValueError("Unsupported inclusion")
    records = {f"X{i}": {"chart": f"L{i}", "value": 1 << i, "owned": False} for i in range(111)}
    records.update({f"Y{i}": {"chart": "zero", "value": 1 << (111+i), "owned": False} for i in range(111)})
    counts, profile = Counter(), Counter()
    paths = {"Pa": [], "Pb": []}
    carried = []
    peak = 0
    snapshots = {}
    for k, op in enumerate(word["operations"], 1):
        kind, name, *rest = op
        counts[kind] += 1
        if kind == "INIT":
            chart = rest[0]
            if name in records or chart not in charts:
                raise ValueError("Bad INIT")
            records[name] = {"chart": chart, "value": 0, "owned": True}
            peak = max(peak, sum(r["owned"] for r in records.values()))
            if name in paths:
                for j in word["moved_original_sources"]:
                    if records[f"X{j}"]["value"] != 1 << j or records[f"X{j}"]["chart"] != "Hub":
                        raise ValueError("Original not restored before packet birth")
                paths[name].append(dims[chart])
        elif kind == "ADD":
            target = rest[0]
            if name == target or name not in records or target not in records or records[name]["chart"] != records[target]["chart"]:
                raise ValueError(f"Unavailable ADD at {k}")
            records[target]["value"] ^= records[name]["value"]
        elif kind == "MOVE":
            target = rest[0]
            r = records[name]
            source = r["chart"]
            if not (included(target, source) if r["owned"] else included(source, target)):
                raise ValueError(f"Illegal nested MOVE at {k}")
            delta = abs(dims[source] - dims[target])
            if not delta:
                raise ValueError("Zero-rank MOVE")
            profile[delta] += 1
            r["chart"] = target
            if name in paths:
                paths[name].append(dims[target])
        elif kind == "CLEAR":
            if not records[name]["owned"]:
                raise ValueError("Original CLEAR")
            del records[name]
        else:
            raise ValueError("Unknown operation")
        for p in paths:
            if p in records and records[p]["chart"] != "Hub":
                carried.append(records[p]["value"] & ((1 << 111) - 1))
        for label, at in word["markers"].items():
            if at == k:
                snapshots[label] = {"profile": dict(sorted(profile.items())), "counts": dict(counts),
                                    "records": {name: {"chart": r["chart"], "value_hex": hex(r["value"])} for name, r in records.items() if r["owned"]},
                                    "carried_x_rank": rank_f2(carried)}
    if snapshots["handoff"]["records"] != word["expected_owned_at_handoff"]:
        raise ValueError("Handoff cache/packet value mismatch")
    for i in range(111):
        if records[f"X{i}"]["value"] != 1 << i:
            raise ValueError(f"Original X{i} not restored")
        if records[f"Y{i}"]["value"] != 1 << (111+i):
            raise ValueError(f"Unserved Y{i} altered")
        want_x = "Hub" if word["closed_partial"] or i in word["moved_original_sources"] else f"L{i}"
        want_y = f"F{i}" if word["closed_partial"] else "zero"
        if records[f"X{i}"]["chart"] != want_x or records[f"Y{i}"]["chart"] != want_y:
            raise ValueError("Original endpoint chart mismatch")
    live = sum(r["owned"] for r in records.values())
    if live != (0 if word["closed_partial"] else len(word["expected_owned_at_handoff"])):
        raise ValueError("Owner count mismatch")
    for p in paths:
        if paths[p] != [8, 7, 1, 0]:
            raise ValueError("Packet lifetime changed")
    return {"status": "PASS_SHARED_FACET_SOURCE", "all_original_input_columns": 222,
            "facets": word["facets"], "donors": word["donors"], "seed_kind": word["seed_kind"],
            "closed_partial": word["closed_partial"], "counts": dict(counts),
            "movement_profile": dict(sorted(profile.items())), "rank_length": sum(k*v for k,v in profile.items()),
            "owned_peak": peak, "live_owned": live, "carried_x_rank": rank_f2(carried),
            "packet_paths": paths, "snapshots": snapshots, "completed_targets": [], "new_complete_kappa": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    roots, h, pins = source_geometry(args.repo)
    args.output.mkdir(parents=True, exist_ok=True)
    preferred = build_word(roots, h)
    preferred_closed = build_word(roots, h, closed=True)
    canonical = build_word(roots, h, seed_kind="canonical")
    canonical_closed = build_word(roots, h, seed_kind="canonical", closed=True)
    result = {"status": "PASS_SHARED_FACET_SOURCE", "source_pins": pins,
              "preferred": replay(preferred, roots), "preferred_closed": replay(preferred_closed, roots),
              "canonical": replay(canonical, roots), "canonical_closed": replay(canonical_closed, roots),
              "pair_variants": [], "negative_controls": {}}
    modes = [1, 3, 5, 10, 30, 61]
    for ai, a in enumerate(modes):
        for b in modes[ai+1:]:
            for seed in ("zero", "canonical"):
                word = build_word(roots, h, a, b, seed, closed=True)
                receipt = replay(word, roots)
                o = len(word["source_sets"]["common"])
                e = sum(map(len, word["source_sets"]["exclusive"]))
                expected = {1: e+8, 2: o, 5: o+2, 6: e+2, 7: 220-o-e}
                if receipt["movement_profile"] != expected or receipt["rank_length"] != 1570:
                    raise ValueError("Closed pair profile identity failed")
                result["pair_variants"].append({k:v for k,v in receipt.items() if k != "snapshots"})
    import copy
    mutants = {}
    def omit_first(name, predicate):
        w = copy.deepcopy(preferred)
        i = next(i for i,o in enumerate(w["operations"]) if predicate(o))
        del w["operations"][i]
        w["markers"] = {k: v-(v>i) for k,v in w["markers"].items()}
        mutants[name] = w
    omit_first("omit_shared_capture", lambda o: o[0] == "ADD" and o[-1] == "Z")
    omit_first("omit_first_carrier_injection", lambda o: o == ["ADD", "Z", "X5"])
    omit_first("omit_donor_restore", lambda o: o[0] == "ADD" and o[-1] == "X5" and o[1] != "Z")
    omit_first("omit_point_unmask", lambda o: o == ["ADD", "R5", "Pa"])
    omit_first("omit_facet_update", lambda o: o == ["ADD", "Ca", "Pa"])
    omit_first("omit_point_copy", lambda o: o == ["ADD", "X5", "R5"])
    for name, word in mutants.items():
        try:
            replay(word, roots)
        except (ValueError, KeyError) as exc:
            result["negative_controls"][name] = {"rejected": True, "reason": str(exc)}
        else:
            raise ValueError("Accepted mutant " + name)
    # Literal history/W intersection, including the outside-W donor masks.
    full = (1 << 111)-1
    hm = mask(j for j in range(111) if h[j])
    K = [mask(j for j, r in enumerate(roots) if j == i or dot(roots[i], r) == 0) for i in range(111)]
    A = [row & (hm if h[i] else full ^ hm) for i, row in enumerate(K)]
    ma, mb = (mask(s) for s in canonical["source_sets"]["modes"])
    da, db = (1 << i for i in canonical["donors"])
    history = [K[1], K[3], K[1] ^ ma ^ da, K[3] ^ mb ^ db, K[1] ^ ma, K[3] ^ mb]
    rh, rw, rj = rank_f2(history), rank_f2(A), rank_f2(history + A)
    if (rh, rw, rj, rh+rw-rj) != (6, 15, 17, 4):
        raise ValueError("Actual history/W intersection differs")
    if rank_f2([K[1], K[3], ma, mb]) != 4:
        raise ValueError("Two proper modes are not independent innovations")
    result["canonical_history"] = {"dimension": rh, "W_dimension": rw, "joint_dimension": rj,
                                    "intersection_dimension": rh+rw-rj, "outside_W_dimension": rj-rw,
                                    "inside_W_basis": [hex(x) for x in [K[1], K[3], ma, mb]]}
    for name, content in [("WORD.json", preferred), ("CLOSED-WORD.json", preferred_closed),
                          ("CANONICAL-WORD.json", canonical), ("CANONICAL-CLOSED-WORD.json", canonical_closed),
                          ("RESULT.json", result)]:
        (args.output/name).write_text(json.dumps(content, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"status": result["status"], "variants": len(result["pair_variants"]),
                      "negative_controls": len(result["negative_controls"]),
                      "preferred_profile": result["preferred_closed"]["movement_profile"]}, sort_keys=True))


if __name__ == "__main__":
    main()
