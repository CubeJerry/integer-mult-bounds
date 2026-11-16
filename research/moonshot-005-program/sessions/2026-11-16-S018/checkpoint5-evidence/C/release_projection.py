#!/usr/bin/env python3
"""Release immutable original routes by a protected source-coordinate projection.

This is an independently implemented finite native-word transformation/replay.
No predecessor checker is imported.  The theorem and scope are in PROOF.md.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

N = 111
PIN = "27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd"
BACKUPS = {
    0: "ZRAW0", 2: "COMMON_RAW2", 8: "ADDED_RAW8", 9: "ADDED_RAW9",
    20: "DIRECT_RAW20", 28: "ZRAW28", 36: "ADDED_RAW36", 37: "ADDED_RAW37",
    44: "ZRAW44", 50: "ADDED_RAW50",
}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def rref(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    k = 0
    pivots = []
    for j in range(8):
        q = next((q for q in range(k, len(a)) if a[q][j]), None)
        if q is None:
            continue
        a[k], a[q] = a[q], a[k]
        z = a[k][j]
        a[k] = [x / z for x in a[k]]
        for q in range(len(a)):
            if q != k and a[q][j]:
                z = a[q][j]
                a[q] = [x - z*y for x, y in zip(a[q], a[k])]
        pivots.append(j)
        k += 1
    return tuple(tuple(r) for r in a[:k]), pivots


def chart(rec):
    a, pivots = rref(rec["rows"])
    if rec["kind"] == "span":
        return a
    require(rec["kind"] == "ann", "chart kind")
    rows = []
    for j in range(8):
        if j in pivots:
            continue
        v = [Fraction(0)] * 8
        v[j] = 1
        for k, p in enumerate(pivots):
            v[p] = -a[k][j]
        rows.append(v)
    return rref(rows)[0]


def binary_basis(rows):
    b = {}
    for row in rows:
        while row:
            p = row.bit_length()-1
            if p in b:
                row ^= b[p]
            else:
                b[p] = row
                break
    return b


def same_span(a, b):
    ra, rb = len(binary_basis(a)), len(binary_basis(b))
    return ra == rb == len(binary_basis(list(a)+list(b)))


def replay(w, *, collect=False):
    charts = {name: chart(rec) for name, rec in w["charts"].items()}
    values = {f"X{i}": 1 << i for i in range(N)}
    values.update({f"Y{i}": 1 << (N+i) for i in range(N)})
    locations = {f"X{i}": f"L{i}" for i in range(N)}
    locations.update({f"Y{i}": "zero" for i in range(N)})
    owned = set()
    ever = set()
    counters, profile = Counter(), Counter()
    dirty = peak = 0
    memo = {}
    trace = []
    live_cut = None

    def sub(a, b):
        key = (a, b)
        if key not in memo:
            memo[key] = len(rref(charts[a]+charts[b])[0]) == len(charts[b])
        return memo[key]

    for step, o in enumerate(w["operations"]):
        op, name, *tail = o
        if collect:
            trace.append((values.copy(), locations.copy()))
        if op == "CLEAR" and live_cut is None:
            live_cut = (step, values.copy(), locations.copy())
        counters[op] += 1
        if op == "INIT":
            require(name not in values and name not in ever, (step, "birth", name))
            values[name], locations[name] = 0, tail[0]
            owned.add(name)
            ever.add(name)
        elif op == "ADD":
            dst = tail[0]
            require(name in values and dst in values, (step, "read alive", o))
            require(sub(locations[name], locations[dst]) and sub(locations[dst], locations[name]),
                    (step, "co-location", o, locations[name], locations[dst]))
            values[dst] ^= values[name]
        elif op == "MOVE":
            require(name in values, (step, "move alive", o))
            old, new = locations[name], tail[0]
            require(sub(new, old) if name in owned else sub(old, new),
                    (step, "move direction", o, old))
            d = abs(len(charts[new])-len(charts[old]))
            require(d > 0, (step, "positive move", o))
            profile[d] += 1
            locations[name] = new
        elif op == "CLEAR":
            require(name in owned, (step, "owned clear", o))
            dirty += bool(values[name])
            owned.remove(name)
            del values[name], locations[name]
        else:
            raise ValueError((step, "opcode", o))
        peak = max(peak, len(owned))
    require(not owned and len(values) == 2*N, "complete lifetimes")
    targets = set(w["targets"])
    for i in range(N):
        require(values[f"X{i}"] == 1 << i and locations[f"X{i}"] == "Hub", ("X endpoint", i))
        require(values[f"Y{i}"] == (1 << (N+i)) ^ ((1 << i) if i in targets else 0),
                ("Y endpoint", i))
        require(locations[f"Y{i}"] == f"F{i}", ("Y final chart", i))
    return {
        "counts": dict(counters), "movement_profile": dict(sorted(profile.items())),
        "dirty_CLEAR": dirty, "peak_owned": peak, "all_222_endpoints": True,
    }, trace, live_cut


def validate_backups(w, backups, release_set=None):
    ds = set(backups) if release_set is None else set(release_set)
    require(set(backups) == ds & set(w["targets"]),
            "exactly released old completed targets need protected backups")
    require(not any(o[0] == "ADD" and o[2] == f"X{d}"
                    for o in w["operations"] for d in ds), "release requires immutable X donors")
    require(not any(o[0] == "ADD" and o[1].startswith("Y") for o in w["operations"]),
            "this concrete compiler requires read-only Y outputs")
    for d, name in backups.items():
        writes = [o for o in w["operations"] if o[0] == "ADD" and o[2] == name]
        require(writes == [["ADD", f"X{d}", name]], ("independent pure backup", d, name))
        births = [o for o in w["operations"] if o[0] == "INIT" and o[1] == name]
        require(births == [["INIT", name, f"L{d}"]], ("native backup birth", d))
        moves = [o for o in w["operations"] if o[0] == "MOVE" and o[1] == name]
        require(moves == [["MOVE", name, "zero"]], ("native backup descent", d))
        require(sum(o == ["CLEAR", name] for o in w["operations"]) == 1, ("backup retirement", d))


def build(w, backups, release_set=None):
    ds = set(backups) if release_set is None else set(release_set)
    validate_backups(w, backups, ds)
    xs = {f"X{d}" for d in ds}
    bs = set(backups.values())
    old_to_new = {}
    removed = []
    inserted = []
    repaired = set()
    new_ops = []
    before_clear = None
    for k, o in enumerate(w["operations"]):
        op, name, *q = o
        if op == "MOVE" and name in xs:
            removed.append({"index": k, "operation": o, "why": "released original route"})
            continue
        if op == "ADD" and name in xs:
            d = int(name[1:])
            if q[0] != backups.get(d):
                removed.append({"index": k, "operation": o, "why": "projected raw donor"})
                continue
        if op == "ADD" and name in bs:
            removed.append({"index": k, "operation": o, "why": "projected protected-backup use"})
            continue
        if op == "MOVE" and name.startswith("Y") and int(name[1:]) in backups:
            d = int(name[1:])
            if d not in repaired:
                x = ["ADD", backups[d], name]
                inserted.append({"index": len(new_ops), "operation": x, "why": "actual ground endpoint repair"})
                new_ops.append(x)
                repaired.add(d)
        if op == "CLEAR" and before_clear is None:
            before_clear = len(new_ops)
            for d in sorted(ds):
                x = ["MOVE", f"X{d}", "Hub"]
                inserted.append({"index": len(new_ops), "operation": x, "why": "closed raw carrier control"})
                new_ops.append(x)
        old_to_new[k] = len(new_ops)
        new_ops.append(o)
    require(repaired == set(backups), "every released old target repaired")
    out = {k: copy.deepcopy(w[k]) for k in ("source_path", "source_sha256", "charts", "targets")}
    out.update({
        "schema": "protected-coordinate-projection-carrier-release-v1",
        "base_word_sha256": PIN,
        "released_carriers": sorted(ds),
        "protected_native_ground_backups": {str(d): backups[d] for d in sorted(backups)},
        "carrier_interface_before_operation": before_clear,
        "operations": new_ops,
        "scope": f"All46 endpoints preserved; {len(ds)} immutable originals are completely detached from old source computation, with independent native backups for the {len(backups)} released old targets. Their actual raw values stay at their native lines until the declared interface; {len(ds)} direct Hub returns close this control. Old higher source rows and histories are projected, not inherited. All original111 X and arbitrary111 Y columns are retained. This is a route-release interface, not a completed supplier or new kappa.",
    })
    return out, old_to_new, removed, inserted


def covariance(old, new, old_to_new, old_trace, new_trace, backups):
    ds = set(new["released_carriers"])
    dm = sum(1 << d for d in ds)
    xs, bs = {f"X{d}" for d in ds}, set(backups.values())
    observed = 0
    for oldk, newk in old_to_new.items():
        ov, oa = old_trace[oldk]
        nv, na = new_trace[newk]
        for name, row in ov.items():
            if name in xs or name in bs:
                continue
            want = row & ~dm
            if name.startswith("Y") and name[1:].isdigit():
                d = int(name[1:])
                if d in backups and na[name] != "zero":
                    want ^= 1 << d
                elif d in backups and new["operations"][newk][0:2] == ["MOVE", name]:
                    # The repair is inserted immediately before this old MOVE.
                    want ^= 1 << d
            require(nv[name] == want, ("covariance value", oldk, newk, name, hex(nv[name]), hex(want)))
            require(na[name] == oa[name], ("covariance chart", oldk, name))
            observed += 1
    return observed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--maximal", action="store_true")
    a = ap.parse_args()
    base = a.repo / "research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json"
    raw = base.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PIN, "pinned base")
    w = json.loads(raw)
    src = a.repo / w["source_path"]
    require(hashlib.sha256(src.read_bytes()).hexdigest() == w["source_sha256"], "pinned native roots")
    old_stats, old_trace, old_live = replay(w, collect=True)
    mutable = {int(o[2][1:]) for o in w["operations"] if o[0] == "ADD" and o[2].startswith("X")}
    ds = set(BACKUPS)
    if a.maximal:
        ds |= set(range(N))-set(w["targets"])-mutable
    new, mapping, removed, inserted = build(w, BACKUPS, ds)
    stats, trace, live = replay(new, collect=True)
    state_checks = covariance(w, new, mapping, old_trace, trace, BACKUPS)
    # Actual carrier interface is before all direct-Hub closure moves.
    cut = new["carrier_interface_before_operation"]
    cv, ca = trace[cut]
    require(all(cv[f"X{d}"] == 1 << d and ca[f"X{d}"] == f"L{d}" for d in ds),
            "all released raw original carriers at native source charts")
    require(all(cv[b] == 1 << d and ca[b] == "zero" for d, b in BACKUPS.items()),
            "ten raw common backups at actual interface")
    require(all(cv[f"X{i}"] == 1 << i and ca[f"X{i}"] == "Hub" for i in set(range(N))-ds),
            "all other originals restored at Hub")
    old_ground = [r for n, r in old_live[1].items() if old_live[2][n] == "zero" and r >> N == 0]
    new_ground = [r for n, r in cv.items() if ca[n] == "zero" and r >> N == 0]
    require(same_span(old_ground, new_ground), "actual common source span unchanged")
    controls = []
    tests = [
        ("omit protected capture", ["ADD", "X50", "ADDED_RAW50"]),
        ("omit actual ground endpoint repair", ["ADD", "ADDED_RAW50", "Y50"]),
        ("omit carrier Hub closure", ["MOVE", "X50", "Hub"]),
        ("omit protected owner retirement", ["CLEAR", "ADDED_RAW50"]),
    ]
    for label, op in tests:
        bad = copy.deepcopy(new)
        bad["operations"].remove(op)
        try:
            replay(bad)
        except (ValueError, KeyError) as e:
            controls.append({"control": label, "rejected": str(e)})
        else:
            raise ValueError(("accepted bad word", label))
    # Retain a now-forbidden old backup use into another output: geometry is
    # legal, but it injects an uncancelled released coordinate.
    extra = next(x for x in removed if x["why"] == "projected protected-backup use"
                 and x["operation"][2] != "Y"+str(next(d for d,b in BACKUPS.items() if b == x["operation"][1])))
    bad = copy.deepcopy(new)
    oldk = extra["index"]
    next_old = min(k for k in mapping if k > oldk)
    bad["operations"].insert(mapping[next_old], extra["operation"])
    try:
        replay(bad)
    except (ValueError, KeyError) as e:
        controls.append({"control": "unprojected old raw-backup reader", "operation": extra["operation"], "rejected": str(e)})
    else:
        raise ValueError("accepted unprojected backup reader")
    try:
        validate_backups(w, {10: "DIRECT_RAW10"})
    except ValueError as e:
        controls.append({"control": "release mutable original X10", "rejected": str(e)})
    else:
        raise ValueError("accepted mutable original")
    # Zero-cost packet/history inheritance is deliberately rejected.
    old_imports = {n: hex(old_live[1][n]) for n in ("IMPORT_E8", "IMPORT_E9", "IMPORT_E36")}
    new_imports = {n: hex(cv[n]) for n in old_imports}
    require(all(int(v,16) for v in old_imports.values()) and set(new_imports.values()) == {"0x0"},
            "actual source contract changes recorded")
    source_cuts = []
    released_names = {f"X{d}" for d in ds}
    for packet in [f"P{i}" for i in range(6)]:
        k = next(k for k,o in enumerate(new["operations"])
                 if o[0] == "ADD" and o[2] == packet and trace[k][1][o[1]] == "Hub")
        vv,ll = trace[k]
        hub_orig = {n:z for n,z in vv.items() if n.startswith("X") and ll[n] == "Hub"}
        held = {n:{"chart":ll[n],"row_hex":hex(z)} for n,z in vv.items()
                if n.startswith("X") and ll[n] != "Hub" and n not in released_names}
        source_cuts.append({"packet":packet,"cut":"before first actual Hub source ADD","new_operation_index":k,
            "actual_Hub_original_count":len(hub_orig),
            "actual_Hub_original_rank":len(binary_basis(hub_orig.values())),
            "actual_Hub_originals_all_raw":all(z == 1 << int(n[1:]) for n,z in hub_orig.items()),
            "held_nonreleased_originals":held,
            "released_originals_still_raw_native":all(vv[f"X{d}"]==1<<d and ll[f"X{d}"]==f"L{d}" for d in ds)})
    cb = {n:chart(rec) for n,rec in new["charts"].items()}
    m1_names = [n for n in cv if cb[ca[n]] == cb["M1"]]
    owned_names = [n for n in cv if not (n[:1] in "XY" and n[1:].isdigit())]
    retained_owned = [cv[n] for n in owned_names]
    retained_nonprotected = [cv[n] for n in owned_names if n not in set(BACKUPS.values())]
    a.out.mkdir(parents=True, exist_ok=True)
    output = (json.dumps(new, indent=2)+"\n").encode()
    (a.out / "WORD.json").write_bytes(output)
    report = {
        "status": "PASS_PROTECTED_PROJECTION_ORIGINAL_CARRIER_RELEASE",
        "base_word_sha256": PIN,
        "word_sha256": hashlib.sha256(output).hexdigest(),
        "native_source_sha256": w["source_sha256"],
        "released_carriers": sorted(ds),
        "protected_backups": {str(d): BACKUPS[d] for d in sorted(BACKUPS)},
        "before": old_stats, "after": stats,
        "target_count": len(new["targets"]),
        "covariant_actual_state_comparisons": state_checks,
        "carrier_interface_before_operation": cut,
        "carrier_interface": {f"X{d}": {"row_hex": hex(cv[f"X{d}"]), "chart": ca[f"X{d}"]} for d in sorted(ds)},
        "other_originals_raw_at_Hub": N-len(ds),
        "all10_protected_backups_raw_at_ground": True,
        "actual_common_source_rank_before": len(binary_basis(old_ground)),
        "actual_common_source_rank_after": len(binary_basis(new_ground)),
        "actual_common_source_rowspace_identical": True,
        "uncompleted_mutable_originals_not_released": sorted((set(range(N))-set(w["targets"]))&mutable),
        "actual_source_cuts":source_cuts,
        "actual_open_interface_M1_fields":{n:hex(cv[n]) for n in m1_names},
        "actual_open_interface_M1_rank":len(binary_basis(cv[n] for n in m1_names)),
        "actual_open_interface_owned_rank":len(binary_basis(retained_owned)),
        "actual_open_interface_nonprotected_owned_rank":len(binary_basis(retained_nonprotected)),
        "old_imports": old_imports, "new_imports": new_imports,
        "removed_operations": removed, "inserted_operations": inserted,
        "negative_controls": controls,
        "scope": new["scope"], "new_complete_kappa": False,
    }
    (a.out / "RESULT.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in ("status", "word_sha256", "before", "after", "actual_common_source_rank_after", "covariant_actual_state_comparisons")}))


if __name__ == "__main__":
    main()
