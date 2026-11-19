#!/usr/bin/env python3
"""Separate geometry and alphabet review; no author module is imported."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

EXPECTED = {
    "layout": "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72",
    "partition": "2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25",
}


def require(value, label):
    if not value:
        raise ValueError(label)


def bitset(values):
    result = 0
    for value in values:
        result |= 1 << value
    return result


def bits(value):
    while value:
        bit = value & -value
        yield bit.bit_length() - 1
        value ^= bit


def rational_rank(rows):
    basis = {}
    for row in rows:
        r = [Fraction(x) for x in row]
        for pivot in sorted(basis):
            if r[pivot]:
                factor = r[pivot]
                r = [x - factor * y for x, y in zip(r, basis[pivot])]
        pivot = next((i for i, x in enumerate(r) if x), None)
        if pivot is not None:
            factor = r[pivot]
            basis[pivot] = [x / factor for x in r]
    return len(basis)


def load(path, kind):
    raw = gzip.decompress(path.read_bytes())
    require(sha256(raw).hexdigest() == EXPECTED[kind], f"{kind} pin")
    return json.loads(raw)


def algebra_controls():
    # Two donors each carry four independent bits. The selected middle
    # sees donor A's first two and donor B's last two coordinates. With
    # all other boundary coordinates fixed, every four-bit target occurs.
    images = set()
    for x0, x1, y2, y3 in product(range(2), repeat=4):
        images.add((x0, x1, y2, y3))
    require(len(images) == 16 > 2 ** 2, "nonlinear alphabet contradiction")
    # Equal class profiles alone do not align subspaces.
    first = {0, 3}
    second = {1, 4}
    class_mask = [set(range(3)), set(range(3, 6))]
    p = [len(first & c) for c in class_mask]
    q = [len(second & c) for c in class_mask]
    require(p == q == [1, 1], "same count profile")
    require(len(first | second) == 4 > 2, "matching counts not sufficient")
    # A different donor coordinate identification can align those same
    # geometric column sets; thus independent donor gauges are not ruled out.
    permutation = [1, 0, 2, 4, 3, 5]
    require({permutation[x] for x in second} == first, "changed-gauge escape control")
    return {"target_images_on_fixed_other_boundary": 16, "two_bit_message_alphabet": 4,
            "matching_profiles_union_dimension": 4, "matching_profiles_each_dimension": 2,
            "changed_donor_gauge_can_align": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--author", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    results = args.repo / "research/moonshot-005-program/results"
    layout = load(results / "bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz", "layout")
    part = load(results / "bit-native-nine-port-modules/author/output/PARTITIONS.json.gz", "partition")
    vectors = layout["root_table"]
    require(len(vectors) == 120 and all(sum(x*x for x in v) == 4 for v in vectors), "root table")
    hsets = [bitset(h) for h in layout["A2"]]
    dsets = [bitset(d) for d in layout["D4"]]
    require(len(set(hsets)) == 1120 and len(set(dsets)) == 3150, "chart identifiers")
    # Reconstruct exact orthogonality; supplied dual labels are not consumed.
    ortho = [bitset(j for j, y in enumerate(vectors) if sum(a*b for a,b in zip(x,y)) == 0)
             for x in vectors]
    dlookup = {mask: i for i, mask in enumerate(dsets)}
    dual = []
    for d in dsets:
        mask = (1 << 120) - 1
        for j in bits(d):
            mask &= ortho[j]
        require(mask in dlookup and not mask & d, "geometric perpendicular D chart")
        dual.append(dlookup[mask])
    # Independently verify each listed chart's rational dimension.
    require(all(rational_rank([vectors[j] for j in bits(h)]) == 2 for h in hsets), "A2 ranks")
    require(all(rational_rank([vectors[j] for j in bits(d)]) == 4 for d in dsets), "D4 ranks")
    h_by_d = [[h for h, hm in enumerate(hsets) if hm & dm == hm] for dm in dsets]
    require(all(len(hs) == 16 for hs in h_by_d), "16 A2 charts per D")
    d_by_h = defaultdict(set)
    for d, hs in enumerate(h_by_d):
        for h in hs:
            d_by_h[h].add(d)
    color = {}
    for h in range(1120):
        classes = part["classes"][str(h)]
        require(len(classes) == 5 and all(len(c) == 9 for c in classes), "five nine-port classes")
        flat = [d for c in classes for d in c]
        require(len(set(flat)) == 45 and set(flat) == d_by_h[h], "actual port partition")
        for c, ds in enumerate(classes):
            for d in ds:
                color[h, d] = c
        for i in range(120):
            if hsets[h] & ortho[i] == hsets[h]:
                require(all(sum(dsets[d] & ortho[i] == dsets[d] for d in ds) == 3
                            for ds in classes), "three visible ports in each class")
    profile = {}
    for d, hs in enumerate(h_by_d):
        counts = {j: [0]*5 for j in bits(dsets[d]) if j < 111}
        for h in hs:
            for j in bits(hsets[h]):
                if j < 111:
                    counts[j][color[h,d]] += 1
        require(all(sum(p) == 4 for p in counts.values()), "four actual donor ports")
        profile[d] = counts
    tight = {}
    native = (1 << 111) - 1
    foreign = 0
    for i in range(111):
        for j in bits(ortho[i] & native):
            foreign += 1
            visible = [h for h, hm in enumerate(hsets) if (hm >> j)&1 and hm & ortho[i] == hm]
            require(len(visible) == 16, "sixteen visible source planes")
            tight[i,j] = all((hsets[h] & native).bit_count() >= 2 for h in visible)
    require(foreign == 6470 and sum(tight.values()) == 6110, "native tight pairs")
    by_receiver = defaultdict(list)
    all_rows = []
    triangle_rows = []
    for d, dm in enumerate(dsets):
        for i in bits(dsets[dual[d]] & native):
            require(dm & ortho[i] == dm, "middle lies in actual receiver facet")
            right = [h for h in h_by_d[dual[d]] if (hsets[h] >> i)&1]
            require(len(right) == 4, "actual four K flags")
            active = [j for j in profile[d] if tight[i,j]]
            require(active, "nonempty tight donor set")
            lower = sum(max(profile[d][j][c] for j in active) for c in range(5))
            row = {"receiver": i, "middle": d, "lower": lower,
                   "profiles": {str(j): profile[d][j] for j in sorted(active)}, "right": right}
            all_rows.append(row)
            by_receiver[i].append(row)
            if i in [10,33,80,95]:
                selected = [j for j in [29,36,77] if (dm >> j)&1]
                if len(selected) >= 2:
                    require(all(tight[i,j] for j in selected), "triangle tight source")
                    triangle_rows.append({**row,
                        "lower": sum(max(profile[d][j][c] for j in selected) for c in range(5)),
                        "profiles": {str(j): profile[d][j] for j in selected}})
    hist = Counter(r["lower"] for r in all_rows)
    tri_hist = {i: dict(sorted(Counter(r["lower"] for r in triangle_rows if r["receiver"] == i).items()))
                for i in [10,33,80,95]}
    require(len(all_rows) == 34965 and sum(x > 4 for x in [r["lower"] for r in all_rows]) == 34425,
            "independent complete census")
    require(len(triangle_rows) == 156 and sum(r["lower"] > 4 for r in triangle_rows) == 151,
            "independent triangle census")
    witness = next(r for r in triangle_rows if r["receiver"] == 10 and r["middle"] == 81)
    require(witness["profiles"] == {"29": [0,2,0,2,0], "36": [0,2,0,0,2]}, "explicit profiles")
    require(witness["lower"] == 6 and witness["right"] == [424,605,674,916], "native witness cut")
    require(tri_hist[10] == {6:39}, "all39 receiver10 cuts fail")
    author_result = json.loads((args.author / "output/RESULT.json").read_text())
    require({str(k):v for k,v in sorted(hist.items())} == author_result["all_native"]["histogram"],
            "author census agrees with independent reconstruction")
    author_cuts = json.loads(gzip.decompress((args.author / "output/CUTS.json.gz").read_bytes()))
    original = {(r["receiver"],r["middle"]): r for r in author_cuts["all_native"]}
    for row in all_rows:
        other = original[row["receiver"],row["middle"]]
        require(row["profiles"] == other["profiles"] and row["lower"] == other["dimension_lower"]
                and row["right"] == other["right_planes"], "every independently reconstructed cut agrees")
    controls = algebra_controls()
    report = {"status": "PASS_INDEPENDENT_NATIVE_CLASS_GATE_REVIEW", "author_code_imported": False,
              "rational_A2_ranks_checked": 1120, "rational_D4_ranks_checked": 3150,
              "reconstructed_all_cuts": len(all_rows), "failures": 34425,
              "histogram": dict(sorted(hist.items())), "triangle_cuts": 156, "triangle_failures":151,
              "triangle_histograms": tri_hist, "witness": witness, "controls": controls,
              "pins": EXPECTED,
              "scope": "exact class-separated proper sum only; no arbitrary B or return-rank conclusion"}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    pins = {str(p.relative_to(args.author)): sha256(p.read_bytes()).hexdigest()
            for p in [args.author/"PROOF.md",args.author/"check.py",args.author/"output/RESULT.json"]}
    (args.out / "REVIEW-PINS.json").write_text(json.dumps(pins,indent=2,sort_keys=True)+"\n")
    print(report["status"])
    print(json.dumps({"cuts":len(all_rows),"failures":34425,"triangle_failures":151},sort_keys=True))


if __name__ == "__main__":
    main()
