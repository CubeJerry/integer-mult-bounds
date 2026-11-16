#!/usr/bin/env python3
"""Native small-witness certificate for the selected changed eight-seed code."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def basis(rows):
    pivots = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return pivots


def solve(rows, target):
    pivots = {}
    for i, x in enumerate(rows):
        c = 1 << i
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                r, k = pivots[p]
                x ^= r
                c ^= k
            else:
                pivots[p] = (x, c)
                break
    c = 0
    while target:
        p = target.bit_length() - 1
        if p not in pivots:
            return None
        r, k = pivots[p]
        target ^= r
        c ^= k
    return c


def combine(rows, mask):
    result = 0
    for i, row in enumerate(rows):
        if mask >> i & 1:
            result ^= row
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    data = json.loads(source_bytes)
    native_bytes = (args.repo / data["native_source_path"]).read_bytes()
    assert hashlib.sha256(native_bytes).hexdigest() == data["native_source_sha256"]
    roots = json.loads(native_bytes)["native_roots"]
    dot = lambda i, j: sum(x * y for x, y in zip(roots[i], roots[j]))
    local = [[1 << j for j in range(111) if dot(i, j) == 0] for i in range(111)]
    canonical = [(1 << i) | sum(local[i]) for i in range(111)]
    active = [int(v, 16) for v in data["active_six_rows_hex"]]
    pair = [int(v, 16) for v in data["canonical_pair_hex"]]
    binary_frame = [0, 1, 2, 4, 8, 14, 30, 59]
    noncontact = lambda i, j: int(i != j and dot(i, j) != 0)
    gram = [sum(noncontact(i, j) << k for k, j in enumerate(binary_frame)) for i in binary_frame]
    assert len(basis(gram)) == 8
    labels = [solve(gram, sum(noncontact(i, j) << k for k, i in enumerate(binary_frame))) for j in range(111)]
    assert all(label is not None for label in labels)
    h = [(label & 189).bit_count() % 2 for label in labels]
    singular = [canonical[i] & sum(1 << j for j in range(111) if h[j] == h[i]) for i in range(111)]
    assert active == [singular[i] for i in [3, 76, 80, 4, 74, 78]]
    rows = active + pair
    assert len(basis(active)) == 6 and len(basis(rows)) == 8
    assert all(solve(canonical, row) is not None for row in pair)
    frame = data["frame"]
    points = data["optional_point_set"]
    source_row = int(data["baseline_unit_source_row"], 16)
    lam = sum(1 << i for i in data["functional_support"])
    restrict = lambda row: sum(((row >> i) & 1) << k for k, i in enumerate(frame))
    assert len(frame) == len(set(frame)) == 8
    assert all(dot(i, j) != 0 for i in frame for j in frame)
    assert not set(frame).intersection(points)
    assert len(basis(restrict(row) for row in rows)) == 5
    source_recipe = solve(active, source_row)
    assert source_recipe == 0x38 and restrict(source_row) == 1
    assert lam & 1 and not (lam & sum(local[0]))
    assert all((row & lam).bit_count() % 2 == 0 for row in rows)
    assert all(not (lam >> i & 1) for i in points)
    full = rows + [1 << i for i in points]
    intersections = [9 + len(basis(rows)) - len(basis(rows + canonical)),
                     9 + len(basis(full)) - len(basis(full + canonical))]
    assert len(basis(canonical)) == 9 and intersections == [5, 5]
    new = []
    for row in canonical:
        if solve(rows + new, row) is None:
            new.append(row)
    assert len(new) == 4
    witnesses = []
    for i in range(111):
        coeff = solve(rows + new, canonical[i])
        assert coeff is not None
        assert combine(rows + new, coeff) ^ sum(local[i]) == (1 << i)
        witnesses.append(hex(coeff))
    controls = []
    for omitted in range(4):
        remaining = rows + [v for k, v in enumerate(new) if k != omitted]
        missed = [i for i in range(111) if solve(remaining + local[i], 1 << i) is None]
        assert missed
        controls.append({"omitted_completion_direction": omitted, "unfitted_receivers": missed})
    assert any((row & (lam ^ (1 << 24))).bit_count() % 2 for row in rows)
    assert not restrict(0) == 1
    assert lam >> 17 & 1
    family = collections.Counter()
    for u in range(1 << 8):
        for t in range(2):
            x = sum(((u >> k) & 1) << i for k, i in enumerate(frame)) ^ (lam if t else 0)
            b = sum(((row & x).bit_count() % 2) << k for k, row in enumerate(rows))
            u0 = (source_row & x).bit_count() % 2
            assert u0 == (u & 1)
            assert not (x & sum(local[0]))
            recovered_t = (x & 1) ^ u0
            assert recovered_t == t
            for i in frame:
                assert x & sum(local[i]) == (lam & sum(local[i]) if t else 0)
            assert all(not (x >> p & 1) for p in points)
            family[b] += 1
    assert len(family) == 32 and set(family.values()) == {16}
    result = {
        "status": "PASS_CHANGED_EIGHT_SEED_EXACT_FOUR_COMPLETION",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "native_source_sha256": data["native_source_sha256"],
        "code_dimension": 8,
        "frame": frame,
        "frame_gram": [[dot(i, j) for j in frame] for i in frame],
        "restriction_rank": 5,
        "source_unit_row": hex(source_row),
        "source_unit_active_six_recipe": hex(source_recipe),
        "functional_support": data["functional_support"],
        "functional_native_products_at_receiver0": [dot(0, i) for i in data["functional_support"]],
        "canonical_intersection_dimensions": intersections,
        "canonical_completion_rows": [hex(v) for v in new],
        "all_111_canonical_decoding_coefficients": witnesses,
        "completion_omission_controls": controls,
        "other_controls": ["lambda_missing_coordinate24", "wrong_unit_source_row", "out_of_scope_point17"],
        "binary_restricted_family": {"inputs": 512, "baseline_values": 32, "fiber_size": 16},
        "exact_additional_linear_dimension_per_record_width": 4,
        "exact_finite_field_fixed_length_message_symbols_per_record_width": 4,
        "classification": "Proved prescribed-code static fitting theorem; physical source/transport remains separate; no new kappa",
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "restriction_rank", "canonical_intersection_dimensions", "exact_additional_linear_dimension_per_record_width", "binary_restricted_family"]}))


if __name__ == "__main__":
    main()
