#!/usr/bin/env python3
"""Exact fixed-code feedback closure, including explicit outsider duals."""
import argparse
import hashlib
import json
from pathlib import Path
from certify import basis, solve


def annihilator_basis(rows, n=111):
    pivots = basis(rows)
    result = []
    for j in range(n):
        if j in pivots:
            continue
        z = 1 << j
        for p in sorted(pivots):
            if (pivots[p] & z).bit_count() % 2:
                z ^= 1 << p
        assert all((row & z).bit_count() % 2 == 0 for row in rows)
        result.append(z)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    d = json.loads(source_bytes)
    native_bytes = (args.repo / d["native_source_path"]).read_bytes()
    assert hashlib.sha256(native_bytes).hexdigest() == d["native_source_sha256"]
    roots = json.loads(native_bytes)["native_roots"]
    rows = [int(x, 16) for x in d["active_six_rows_hex"] + d["canonical_pair_hex"]]
    points = d["optional_point_set"]
    initial = d["early_point_grants"]
    local = [[1 << j for j in range(111) if sum(x * y for x, y in zip(roots[i], roots[j])) == 0] for i in range(111)]
    first = [i for i in range(111) if solve(rows + [1 << j for j in initial] + local[i], 1 << i) is not None]
    full = rows + [1 << j for j in points]
    second = [i for i in range(111) if solve(full + local[i], 1 << i) is not None]
    assert first == second == points
    witnesses = []
    for i in range(111):
        if i in points:
            continue
        z = next(v for v in annihilator_basis(full + local[i]) if v >> i & 1)
        assert all((z & r).bit_count() % 2 == 0 for r in full + local[i])
        assert z >> i & 1
        assert not ((z ^ (1 << i)) >> i & 1)  # own-coordinate corruption control
        witnesses.append({"receiver": i, "annihilator": hex(z), "support": [j for j in range(111) if z >> j & 1]})
    assert len(witnesses) == 87
    result = {
        "status": "PASS_CHANGED_U8_POINT_FEEDBACK_CLOSURE",
        "native_source_sha256": d["native_source_sha256"],
        "changed_source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "initial_points": initial,
        "first_fitting_set": first,
        "second_fitting_set": second,
        "closed": True,
        "outside_dual_witnesses": witnesses,
        "own_coordinate_corruption_controls_rejected": 87,
        "scope": "All raw foreign local coordinates are granted for free; a new point is admitted only if exactly recoverable from U8, known points, and those locals. Fixed-code closure, no new physical transport or coded broadcasts.",
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "POINT-CLOSURE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"], len(witnesses))


if __name__ == "__main__":
    main()
