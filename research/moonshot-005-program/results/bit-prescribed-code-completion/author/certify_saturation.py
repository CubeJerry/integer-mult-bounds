#!/usr/bin/env python3
"""Exact native witnesses for the five-direction prescribed S8 minimum.

This checker is deliberately separate from the exploratory frame solver.
It uses only binary ranks, rational native dot products and explicit rows.
"""
import argparse
import hashlib
import json
from pathlib import Path

SOURCE_PIN = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
SEED_PIN = "71c260d339b216eb010e7410bed02237df20366f1a3bf95fe66e9d5921531cb0"
FRAME = [0, 14, 22, 23, 30, 31, 59, 60]
POINTS = [1, 3, 4, 6, 18, 21, 61, 64, 65, 73, 74, 75, 76, 77, 78, 79, 80]
SOURCE_ROW = int("cc00cc6400097c0033000055", 16)
FUNCTIONAL = (1 << 0) | (1 << 24) | (1 << 32)


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return len(pivots)


def restrict(row, coordinates):
    return sum(((row >> j) & 1) << k for k, j in enumerate(coordinates))


def native_data(repo, seed_path):
    seed_bytes = seed_path.read_bytes()
    assert hashlib.sha256(seed_bytes).hexdigest() == SEED_PIN
    seed = json.loads(seed_bytes)
    native_bytes = (repo / seed["native_source_path"]).read_bytes()
    assert hashlib.sha256(native_bytes).hexdigest() == SOURCE_PIN
    roots = json.loads(native_bytes)["native_roots"]
    rows = [int(v, 16) for v in seed["seed_rows"]]
    dot = lambda i, j: sum(a * b for a, b in zip(roots[i], roots[j]))
    local = [sum(1 << j for j in range(111) if dot(i, j) == 0) for i in range(111)]
    canonical = [local[i] ^ (1 << i) for i in range(111)]
    return seed, roots, rows, dot, local, canonical


def check_witness(rows, dot, local, frame, source_row, functional, points):
    assert len(frame) == len(set(frame)) == 8
    assert all(dot(i, j) != 0 for i in frame for j in frame)
    assert not set(frame).intersection(points)
    assert rank(restrict(row, frame) for row in rows) == 4
    assert source_row in rows
    assert restrict(source_row, frame) == 1
    assert functional & 1
    assert not (functional & local[0])
    assert all((functional & row).bit_count() % 2 == 0 for row in rows)
    assert all(not ((functional >> p) & 1) for p in points)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    seed, roots, rows, dot, local, canonical = native_data(args.repo, args.seed)
    check_witness(rows, dot, local, FRAME, SOURCE_ROW, FUNCTIONAL, POINTS)
    assert rank(rows) == 8 and rank(canonical) == 9
    full_baseline = rows + [1 << p for p in POINTS]
    intersections = [rank(rows) + 9 - rank(rows + canonical),
                     rank(full_baseline) + 9 - rank(full_baseline + canonical)]
    assert intersections == [4, 4]
    negative_controls = []
    cases = [
        ("functional_missing_own_coefficient", FRAME, SOURCE_ROW, FUNCTIONAL ^ 1, POINTS, local),
        ("duplicate_frame_port", FRAME[:-1] + [FRAME[0]], SOURCE_ROW, FUNCTIONAL, POINTS, local),
        ("wrong_baseline_source_row", FRAME, 0, FUNCTIONAL, POINTS, local),
        ("out_of_scope_free_point_24", FRAME, SOURCE_ROW, FUNCTIONAL, POINTS + [24], local),
        ("out_of_scope_local_coordinate_24", FRAME, SOURCE_ROW, FUNCTIONAL, POINTS,
         [local[0] | (1 << 24)] + local[1:]),
    ]
    for name, frame, s, lam, points, loc in cases:
        try:
            check_witness(rows, dot, loc, frame, s, lam, points)
        except AssertionError:
            negative_controls.append(name)
        else:
            raise AssertionError("negative control incorrectly accepted: " + name)
    result = {
        "status": "PASS_EXACT_FIVE_DIRECTION_COMPLETION_MINIMUM",
        "source_sha256": SOURCE_PIN,
        "seed_source_sha256": SEED_PIN,
        "frame": FRAME,
        "frame_gram": [[dot(i, j) for j in FRAME] for i in FRAME],
        "frame_restriction_rank": 4,
        "source_seed_index": rows.index(SOURCE_ROW),
        "source_row": hex(SOURCE_ROW),
        "source_frame_restriction": restrict(SOURCE_ROW, FRAME),
        "functional_support": [0, 24, 32],
        "functional_native_products_with_receiver_0": [dot(0, j) for j in [0, 24, 32]],
        "functional_annihilates_all_seed_rows": True,
        "functional_annihilates_all_17_point_grants": True,
        "canonical_intersection_at_empty_and_full_point_grants": intersections,
        "additional_dimension_lower_and_upper_per_record_width": [5, 5],
        "negative_controls_rejected": negative_controls,
        "quantifiers": "Every characteristic-two field, every positive record width V, arbitrary linear added rows and block operators, any subset of the listed 17 raw point grants",
        "scope": "Prescribed S8 static ground code and geometric foreign-coordinate local information; abstract fitting dimension only; no acquisition, transport or complete kappa claim",
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "SATURATION-CERTIFICATE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "source_seed_index", "additional_dimension_lower_and_upper_per_record_width", "negative_controls_rejected"]}))


if __name__ == "__main__":
    main()
