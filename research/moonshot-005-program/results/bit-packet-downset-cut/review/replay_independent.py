#!/usr/bin/env python3
"""Independent exact audit of the BIT eight-downset cut and B8 reference."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from fractions import Fraction
from pathlib import Path

NATIVE_SHA = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
WORD_SHA = "820ec11e14ae00d98bc0fdc109d5d8db64f6a6bea7f2cf76f5bc743a5d4abb4c"
FRAMES = [
    [0, 16, 17, 32, 36, 38, 67, 71],
    [0, 16, 17, 32, 36, 39, 68, 72],
    [0, 16, 17, 36, 37, 63, 71, 72],
    [0, 16, 17, 36, 38, 39, 62, 63],
    [1, 8, 9, 30, 37, 46, 73, 77],
    [1, 8, 9, 30, 37, 47, 74, 78],
    [1, 8, 9, 36, 37, 65, 73, 74],
    [1, 8, 9, 37, 46, 47, 64, 65],
    [36, 37, 62, 64, 67, 68, 77, 78],
]


def need(test: bool, msg: str) -> None:
    if not test:
        raise AssertionError(msg)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rank_q(rows):
    """Exact rational row rank, independent of the author's elimination code."""
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        z = a[r][c]
        a[r] = [x / z for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [x - z * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def in_span_q(row, basis):
    return rank_q([*basis, row]) == rank_q(basis)


def rank_f2(rows):
    pivots = {}
    for row in rows:
        z = int(row)
        while z:
            p = z.bit_length() - 1
            if p not in pivots:
                pivots[p] = z
                break
            z ^= pivots[p]
    return len(pivots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--root-package", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()

    native_path = a.repo / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
    native_raw = native_path.read_bytes()
    need(hashlib.sha256(native_raw).hexdigest() == NATIVE_SHA, "pinned BIT native bytes changed")
    native = json.loads(gzip.decompress(native_raw))
    chart = {int(k): v for k, v in native["frames"].items()}
    word_path = a.root_package / "WORD.json.gz"
    word_raw = word_path.read_bytes()
    need(hashlib.sha256(word_raw).hexdigest() == WORD_SHA, "pinned root reference word changed")
    word = json.loads(gzip.decompress(word_raw))
    need(word["frames"] == native["frames"], "reference chart coordinates differ from native")
    need(word["start"] == native["start"][:222], "reference input charts differ from native")
    need(word["final"] == native["final"][:222], "reference endpoint charts differ from native")

    # Build the actual rational real root vectors from the native source charts.
    roots = []
    for i in range(111):
        row = [Fraction(x) for x in chart[native["start"][i]]["B"][0]]
        norm = dot(row, row)
        need(norm in (1, 4), f"unexpected source root norm at {i}: {norm}")
        scale = 2 if norm == 1 else 1
        v = [scale * x for x in row]
        need(all(x.denominator == 1 for x in v) and dot(v, v) == 4, f"nonintegral doubled root {i}")
        roots.append(v)

    # Reconstruct B over F_2 from the actual integer roots.
    b_rows = []
    for i in range(111):
        bits = 0
        for j in range(111):
            d = dot(roots[i], roots[j])
            need(d.denominator == 1 and int(d) % 2 == 0, f"non-even doubled-root dot {i},{j}")
            coefficient = (int(d) // 2) & 1
            need(coefficient == int(i != j and d != 0), f"wrong contact encoding {i},{j}")
            bits |= coefficient << j
        b_rows.append(bits)
    need(rank_f2(b_rows) == 8, "source B matrix rank is not 8")

    # Independently certify each retained eight-frame's strict geometry and B block.
    frame_receipts = []
    for fi, S in enumerate(FRAMES):
        need(len(S) == len(set(S)) == 8, f"frame {fi} has duplicate/missing roles")
        real = [[dot(roots[i], roots[j]) for j in S] for i in S]
        need(all(real[i][j] != 0 for i in range(8) for j in range(8)), f"frame {fi} not nonorthogonal")
        # A source line L_j lies outside U_S iff it is not orthogonal to any selected normal.
        need(all(all(dot(roots[j], roots[i]) != 0 for i in S) for j in S), f"frame {fi} source not outside U")
        # The target facet F_i is exactly the 7-plane orthogonal to root i.
        for i in S:
            target_chart = chart[native["final"][111 + i]]
            need(target_chart["dim"] == 7, f"target {i} is not a 7-facet")
            need(all(dot([Fraction(x) for x in row], roots[i]) == 0 for row in target_chart["B"]),
                 f"target facet {i} not in U")
        b_sub = [sum(((b_rows[i] >> j) & 1) << k for k, j in enumerate(S)) for i in S]
        need(b_sub == [255 ^ (1 << i) for i in range(8)], f"frame {fi} binary Gram is not I+J")
        need(rank_f2(b_sub) == 8, f"frame {fi} Gram is singular")
        frame_receipts.append({"frame_index": fi, "roles": S, "all_64_real_pairs_nonzero": True,
                               "source_lines_outside_union": 8, "target_facets_inside_union": 8,
                               "B_principal_rank_f2": rank_f2(b_sub)})
    coordinate_source_inside_last_frame = [
        any(dot(roots[j], roots[i]) == 0 for i in FRAMES[-1]) for j in range(8)
    ]
    need(all(coordinate_source_inside_last_frame),
         "coordinate bus sources are not all inside the ninth retained-frame downset")

    # Independently replay every operation in the literal partial word over F_2.
    V = 1
    public = word["public"]
    need(public == 222 and word["owned_fields"] == 1, "reference shape mismatch")
    rows = {i: 1 << i for i in range(public)}
    locations = {i: word["start"][i] for i in range(public)}
    life_count = 0
    live_peak = 0
    movement_profile = {}
    counts = {"MOVE": 0, "ADD": 0, "INIT": 0, "CLEAR": 0}
    packet_encoder_forms = []
    for op_index, ins in enumerate(word["program"]):
        op = ins[0]
        counts[op] += 1
        if op == "INIT":
            _, f, c = ins
            need(f not in rows, f"INIT of live field at {op_index}")
            rows[f] = 0
            locations[f] = c
            life_count += 1
            live_peak = max(live_peak, sum(i >= public for i in rows))
        elif op == "ADD":
            _, d, s, c = ins
            need(d in rows and s in rows, f"ADD lifetime error at {op_index}")
            need(locations[d] == locations[s] == c, f"ADD chart mismatch at {op_index}")
            rows[d] ^= rows[s]
            if d >= public:
                packet_encoder_forms.append((op_index, d, s, c, rows[d]))
        elif op == "MOVE":
            _, f, src, dst = ins
            need(f in rows and locations[f] == src, f"MOVE source mismatch at {op_index}")
            src_basis, dst_basis = chart[src]["B"], chart[dst]["B"]
            dimsrc, dimdst = chart[src]["dim"], chart[dst]["dim"]
            if f < 111 or 111 <= f < 222:
                need(all(in_span_q(row, dst_basis) for row in src_basis),
                     f"public move not ascending/nested at {op_index}")
                need(dimsrc <= dimdst, f"public trajectory descends at {op_index}")
            else:
                need(all(in_span_q(row, src_basis) for row in dst_basis),
                     f"packet move not descending/nested at {op_index}")
                need(dimdst <= dimsrc, f"packet trajectory ascends at {op_index}")
            r = abs(dimdst - dimsrc)
            movement_profile[r] = movement_profile.get(r, 0) + 1
            counts["MOVE"] += 0
            locations[f] = dst
        elif op == "CLEAR":
            _, f, c = ins
            need(f in rows and locations[f] == c, f"CLEAR lifetime/chart mismatch at {op_index}")
            del rows[f]
            del locations[f]
        else:
            raise AssertionError(f"unsupported operation {op!r} at {op_index}")
    need(set(rows) == set(range(public)), "owned field not cleared or public field lost")
    need([locations[i] for i in range(public)] == word["final"], "reference endpoints not reached")
    expected_x = [1 << i for i in range(111)]
    expected_y = [(1 << (111 + i)) ^ b_rows[i] for i in range(111)]
    need([rows[i] for i in range(111)] == expected_x, "X endpoints are not restored identities")
    need([rows[111 + i] for i in range(111)] == expected_y, "Y endpoint map is not y+Bx")
    need(all(rows[111 + i] != ((1 << (111 + i)) ^ (1 << i)) for i in range(111)),
         "negative control failed: some full target unexpectedly satisfied")
    need(counts == {"MOVE": 230, "ADD": 824, "INIT": 8, "CLEAR": 8}, f"operation bill mismatch: {counts}")
    need(movement_profile == {7: 222, 8: 8}, f"movement profile mismatch: {movement_profile}")
    need(life_count == 8 and live_peak == 1, "owned lifetimes/peak mismatch")

    # Verify that each of the eight actual encoded packet rows restricts to rank 8
    # on each retained frame, hence all nine first-entry cut tests are saturated.
    enc_rows = []
    p = 0
    while p < len(word["program"]):
        ins = word["program"][p]
        if ins[0] != "INIT":
            p += 1
            continue
        f, c = ins[1], ins[2]
        need(c == native["final"][0], "packet not initialized at Hub")
        mask = 0
        p += 1
        while p < len(word["program"]) and word["program"][p][0] == "ADD":
            _, d, s, at = word["program"][p]
            need(d == f and at == c and 0 <= s < 111, "packet encoder has non-X or wrong-chart input")
            mask ^= 1 << s
            p += 1
        need(word["program"][p] == ["MOVE", f, c, native["start"][111]], "packet first entry is not Hub-to-zero")
        enc_rows.append(mask)
        while p < len(word["program"]) and word["program"][p] != ["CLEAR", f, native["start"][111]]:
            p += 1
        need(p < len(word["program"]), "packet lifetime not cleared")
        p += 1
    need(len(enc_rows) == 8 and rank_f2(enc_rows) == 8, "eight packet encoders not independent")
    for fi, S in enumerate(FRAMES):
        restricted = [sum(((row >> j) & 1) << k for k, j in enumerate(S)) for row in enc_rows]
        need(rank_f2(restricted) == 8, f"frame {fi} first-entry encoder rank deficient")

    result = {
        "status": "PASS_INDEPENDENT_EIGHT_DOWNSET_CUT_AUDIT",
        "pinned_native_sha256": NATIVE_SHA,
        "pinned_root_word_sha256": WORD_SHA,
        "exact_source_geometry": {"source_lines": 111, "rank_B_f2": 8, "frames_checked": frame_receipts},
        "coordinate_bus_negative_control": {
            "source_roles": list(range(8)),
            "inside_union_for_retained_frame_index_8": coordinate_source_inside_last_frame,
            "note": "These source lines do not satisfy the source-outside premise for this cut."
        },
        "partial_word_replay": {"inputs": 222, "x_restored": True, "y_map": "y+B*x",
                                "full_targets_failed": 111, "operation_counts": counts,
                                "movement_profile": movement_profile, "packet_lifetimes": life_count,
                                "peak_owned": live_peak, "encoder_rank": 8,
                                "all_nine_frame_first_entry_ranks": [8] * 9},
        "proof_audit": {
            "status": "SOUND_WITH_EXPLICIT_SCOPE",
            "necessary_hypotheses": [
                "all ordinary public and extra local-copy data trajectories move only to containing charts",
                "every downward/incoming transfer from outside the downset is one of the q counted V-dimensional packet trajectories",
                "owned initializations and stationary caches are zero; no nonzero preloaded cross-chart data",
                "physical trajectory identities persist through whole-(chart,value) role relabelings",
                "retirement/rebirth creates a new counted descending lifetime",
                "finite chronological linear operations over one common field and all endpoints exact",
            ],
            "rank_argument": "For one retained 8-frame, x_S starts outside U_S and all eight requested endpoints lie inside. The map from x_S to the at most q packet crossing vectors has rank <=qV. Every inside output is a linear image of those crossing values, while exact targets contain I_(8V); hence 8V<=qV.",
            "all_volume": "The same cut is applied to V-dimensional vector inputs; each packet crossing contributes at most V dimensions.",
            "role_swaps": "Whole-(chart,value) relabelings do not move a value across the cut. Any subsequently downward physical data trajectory is counted as another packet lifetime; free value-only exchange across distinct charts would invalidate the theorem and is excluded.",
            "saturation": "For q=8, each of the nine listed frame restrictions must have full stacked rank 8V at first packet entries. The exact B8 word meets these cut ranks but fails every diagonal target, so saturation is not sufficient.",
            "limits": ["Does not establish existence or impossibility of a complete q=8 word.",
                      "Does not price rank or prove a full native/compiler/supplier result.",
                      "Does not cover uncounted downward copies, restarts, nonmonotone public routes, or nonzero cross-chart preloads."],
        },
    }
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "rank_B_f2": 8,
                      "all_nine_frame_ranks": [8] * 9,
                      "movement_profile": movement_profile,
                      "packet_lifetimes": life_count,
                      "failed_targets": 111}, indent=2))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Independent exact replay requires assertions")
    main()
