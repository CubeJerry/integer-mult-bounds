#!/usr/bin/env python3
"""Independent finite receipt for the nonlinear restricted-family argument."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

SOURCE_PIN = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
SEED_PIN = "71c260d339b216eb010e7410bed02237df20366f1a3bf95fe66e9d5921531cb0"
FRAME = [0, 14, 22, 23, 30, 31, 59, 60]
POINTS = [1, 3, 4, 6, 18, 21, 61, 64, 65, 73, 74, 75, 76, 77, 78, 79, 80]
SUPPORT = FRAME + [24, 32]


def xor(values):
    result = 0
    for value in values:
        result ^= value
    return result


def matrix_rank(rows):
    rows = list(rows)
    rank = 0
    for col in range(111):
        pivot = next((j for j in range(rank, len(rows)) if rows[j] >> col & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for j in range(len(rows)):
            if j != rank and rows[j] >> col & 1:
                rows[j] ^= rows[rank]
        rank += 1
    return rank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    seed_bytes = args.seed.read_bytes()
    assert hashlib.sha256(seed_bytes).hexdigest() == SEED_PIN
    seed = json.loads(seed_bytes)
    native_bytes = (args.repo / seed["native_source_path"]).read_bytes()
    assert hashlib.sha256(native_bytes).hexdigest() == SOURCE_PIN
    roots = json.loads(native_bytes)["native_roots"]
    seed_rows = [int(row, 16) for row in seed["seed_rows"]]
    dot = lambda i, j: sum(a * b for a, b in zip(roots[i], roots[j]))
    source_index = seed_rows.index(int("cc00cc6400097c0033000055", 16))
    row_columns = [[k for k, j in enumerate(SUPPORT) if row >> j & 1] for row in seed_rows]
    local_columns = [[k for k, j in enumerate(SUPPORT) if dot(i, j) == 0] for i in FRAME]
    assert local_columns[0] == []
    assert all(all(k >= 8 for k in cols) for cols in local_columns)
    assert not set(SUPPORT).intersection(POINTS)
    frame_mask = sum(1 << i for i in FRAME)
    assert matrix_rank(row & frame_mask for row in seed_rows) == 4
    # The nonlinear proof needs the *availability* of u0, not a named slot.
    assert matrix_rank([row & frame_mask for row in seed_rows] + [1]) == 4
    seed_without_u0 = [row for row in seed_rows if not (row & 1)]
    assert matrix_rank([row & frame_mask for row in seed_without_u0] + [1]) > matrix_rank(row & frame_mask for row in seed_without_u0)
    results = []
    for q in [2, 4]:
        baseline_fibers = collections.Counter()
        tuples = 0
        for u in itertools.product(range(q), repeat=8):
            for t in range(q):
                values = [u[0] ^ t] + list(u[1:]) + [t, t]
                baseline = tuple(xor(values[k] for k in cols) for cols in row_columns)
                assert baseline[source_index] == u[0]
                expected = tuple(xor(u[k] for k, j in enumerate(FRAME) if row >> j & 1) for row in seed_rows)
                assert baseline == expected
                recovered_t = values[0] ^ baseline[source_index]
                assert recovered_t == t
                for cols in local_columns:
                    assert [values[k] for k in cols] == [recovered_t] * len(cols)
                reconstructed = [baseline[source_index]] + values[1:8]
                assert tuple(reconstructed) == u
                assert values[8] == t and values[9] == t
                baseline_fibers[baseline] += 1
                tuples += 1
        assert tuples == q ** 9
        assert len(baseline_fibers) == q ** 4
        assert set(baseline_fibers.values()) == {q ** 5}
        results.append({"field_cardinality": q, "record_width": 1, "parameter_tuples": tuples,
                        "baseline_values": len(baseline_fibers), "fiber_size": q ** 5,
                        "all_receiver_local_inputs_verified": True})
    lam = (1 << 0) | (1 << 24) | (1 << 32)
    assert any((row & (lam ^ (1 << 32))).bit_count() % 2 for row in seed_rows)
    assert 8 not in local_columns[0]
    controls = ["removing_lambda_coordinate_32_breaks_baseline_annihilation",
                "granting_coordinate_24_breaks_receiver_0_zero_local_premise",
                "removing_all_measurements_with_nonzero_column_0_loses_u0"]
    result = {"status": "PASS_NONLINEAR_RESTRICTED_FAMILY_RECEIPT", "source_sha256": SOURCE_PIN,
              "seed_source_sha256": SEED_PIN, "frame": FRAME,
              "actual_local_support_indices_within_family": [[SUPPORT[k] for k in cols] for cols in local_columns],
              "source_seed_index_revealing_u0": source_index, "enumerations": results,
              "negative_controls": controls,
              "proof_scope": "Exact deterministic fixed-length nonlinear common broadcasts over finite characteristic-two fields, unchanged S8 plus any subset of T17 raw grants, and geometric foreign raw local data",
              "universal_result": "The written injection/cardinality argument proves q >= 5V; the finite enumeration is only a native witness receipt"}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "NONLINEAR-RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "enumerations": results, "negative_controls": controls}))


if __name__ == "__main__":
    main()
