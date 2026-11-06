"""Source-sized integer-frame and quotient-syndrome checks, independent of
the combinatorial lower-bound implementation. Stdlib, Python 3.12.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lift

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / "precision-state-frontier" / "FIXTURE.json"
A = 51_008_161
B = 50_979_600
D = 50_983_170


def rounding(numerator: int, denominator: int) -> int:
    sign = 1 if numerator >= 0 else -1
    return sign * ((2 * abs(numerator) + denominator) // (2 * denominator))


def native(vector, rows):
    projection = [sum(vector[i] * rows[i][j] for i in range(112)) for j in range(8)]
    quotient = [rounding(x, 52) for x in projection]
    return [vector[i] - sum(rows[i][j] * quotient[j] for j in range(8))
            for i in range(112)], quotient


def check_full_frames(data):
    rows = data["rows"]
    free = data["free"]
    coefficients = data["coefficients"]
    actual_images = []
    maximum_entry = 0
    for stage, operations in enumerate(data["operations"]):
        # Every input column, rather than selected random vectors, verifies
        # the integer map's mode-preservation and explicit inverse.
        for coordinate in range(112):
            source = [int(i == coordinate) for i in range(112)]
            moved = lift.apply_frame(source, operations, free, coefficients)
            restored = lift.apply_frame(moved, operations, free, coefficients, True)
            lift.require(restored == source, "whole integer frame inverse")
            projection = [sum(rows[i][j] * moved[i] for i in range(112)) for j in range(8)]
            lift.require(projection == rows[coordinate], "whole integer frame preserves M^T")
            maximum_entry = max(maximum_entry, max(abs(x) for x in moved))
        image = []
        for source in data["columns"]:
            moved = lift.apply_frame(source, operations, free, coefficients)
            image.append(sum((moved[i] & 1) << k for k, i in enumerate(free)))
        lift.require(lift.rank(image) == 4, "actual stage dimension four")
        actual_images.append(image)
    lift.require(lift.rank([v for block in actual_images for v in block]) == 104,
                 "actual combined image dimension104")
    return maximum_entry, actual_images


def check_literal_chains(data):
    free, coefficients, rows = data["free"], data["coefficients"], data["rows"]
    operations = data["operations"]
    rng = random.Random(78)
    samples = [[0] * 112]
    samples.extend([[int(i == j) for i in range(112)] for j in range(112)])
    samples.extend([[rng.randrange(-1000, 1001) for _ in range(112)] for _ in range(8)])
    for initial in samples:
        state, first = native([2 * x for x in initial], rows)
        history = [first]
        for j in range(1, 27):
            state = lift.apply_frame(state, operations[j-1], free, coefficients)
            state = lift.apply_frame(state, operations[j], free, coefficients, True)
            state, quotient = native(state, rows)
            history.append(quotient)
        result = lift.apply_frame(state, operations[-1], free, coefficients)
        for j in range(27):
            source = [sum(rows[i][k] * history[j][k] for k in range(8)) for i in range(112)]
            source = lift.apply_frame(source, operations[j], free, coefficients)
            result = [x + y for x, y in zip(result, source)]
        lift.require(result == [2 * x for x in initial], "full 27-stage literal inverse identity")
    return len(samples)


def syndrome_mass(data):
    coordinates = data["source_coefficients"]
    masses = [0] * 16
    for q in range(256):
        syndrome = lift.combine(coordinates, q)
        masses[syndrome] += 7 ** (8-q.bit_count()) * 6 ** q.bit_count()
    expected = [A if s == 0 else (D if s.bit_count() & 1 else B) for s in range(16)]
    lift.require(masses == expected, "literal source quotient weights")
    terms = []
    for u in range(16):
        term = 1
        for mapping in data["maps"]:
            term *= masses[lift.combine(mapping, u)]
        terms.append(term)
    lower = A**27 + 3*A*B**26 + 12*A*A*B**25
    upper = 16*A**27
    lift.require(sum(terms) == lower, "balanced relation exact zero fiber")
    lift.require(sorted(terms[1:]) == sorted([A*B**26]*3 + [A*A*B**25]*12), "all fifteen relation weights")
    lift.require(2**695 < lower <= upper <= 2**696, "sharp696-bit sandwich")
    return masses, lower, upper


def expect_rejection(action, name):
    try:
        action()
    except (ValueError, StopIteration):
        return name
    raise ValueError("fault unexpectedly accepted: " + name)


def controls(data):
    names = []
    bad_rows = [row[:] for row in data["rows"]]
    # This changes a nonpivot source row outside the selected image lattice.
    bad_rows[0][0] += 1
    names.append(expect_rejection(lambda: lift.source_lattice(bad_rows), "nonintegral_image_lattice"))
    bad_maps = [block[:] for block in data["maps"]]
    bad_maps[0] = [0, 0, 0, 0]
    # A changed source equation must fail the advertised zero-fiber receipt,
    # even though some changed code could remain a legitimate construction.
    changed = dict(data, maps=bad_maps)
    names.append(expect_rejection(lambda: syndrome_mass(changed), "changed_relation_receipt"))
    bad_images = [block[:] for block in data["images"]]
    bad_images[1][0] = bad_images[1][1]
    names.append(expect_rejection(lambda: lift.lift_operations(data["images"][0], bad_images[1]),
                                  "dependent_stage_image"))
    names.append(expect_rejection(lambda: lift.quotient_images([[1, 2, 4, 8]]), "single_stage_relation"))
    # Omit an actual nonzero lift gate and demand the original source image.
    stage = next(j for j, op in enumerate(data["operations"]) if op)
    operations = data["operations"][stage]
    found = False
    for omit in range(len(operations)):
        damaged = operations[:omit] + operations[omit+1:]
        for j in data["chosen_indices"]:
            moved = lift.apply_frame(data["columns"][j], damaged, data["free"], data["coefficients"])
            bit = sum((moved[i] & 1) << k for k, i in enumerate(data["free"]))
            expected = lift.combine(data["images"][stage], data["source_coefficients"][j])
            if bit != expected:
                found = True
                break
        if found:
            break
    lift.require(found, "missing lift gate negative control")
    names.append("missing_actual_lift_gate")
    # A sign error has the same binary matrix and must be caught over Z.
    vector = [((7*i + 3) % 19)-9 for i in range(104)]
    moved = lift.apply_kernel_lift(vector, operations)
    wrong = list(moved)
    for kind, i, j in operations:
        if kind == "swap":
            wrong[i], wrong[j] = wrong[j], wrong[i]
        else:
            wrong[i] -= wrong[j]
    lift.require(wrong != vector, "inverse sign fault invisible overF2")
    names.append("integer_inverse_sign")
    lift.require(not (sum(data["maps"][j][0] != 0 for j in range(27)) == 0), "nontrivial relation")
    lift.require(A**27 + 3*A*B**26 + 12*A*A*B**25 > 2**695,
                 "695-bit tag rejected by attained zero fiber")
    names.append("insufficient695_bit_tag")
    return names


def main():
    data = lift.construct(FIXTURE)
    maximum_entry, images = check_full_frames(data)
    samples = check_literal_chains(data)
    masses, lower, upper = syndrome_mass(data)
    faults = controls(data)
    operation_bytes = json.dumps(data["operations"], separators=(",", ":")).encode()
    receipt = {
        "schema": "source-bound-depth27-frame-attainment-v1",
        "source_sha256": lift.FIXTURE_SHA256,
        "lattice_basis_rows": list(lift.LATTICE_ROWS),
        "kernel_dimension": 104,
        "stages": 27,
        "frame_column_checks": 27*112,
        "literal_chain_samples": samples,
        "relation_dimension": 4,
        "relation_kernel_multiplicities": {str(k): 1 if k <= 3 else 2 for k in range(1, 16)},
        "frame_operation_counts": [len(op) for op in data["operations"]],
        "frame_operations_sha256": hashlib.sha256(operation_bytes).hexdigest(),
        "largest_integer_frame_entry": maximum_entry,
        "coset_masses": masses,
        "attained_zero_fiber": str(lower),
        "all_output_upper": str(upper),
        "packed_recovery_bits": 696,
        "negative_controls": faults,
        "scope": "Exact integer frame/zero-fiber attainment and all-output bit sandwich; no physical cost, full worst-fiber cardinality optimum or new kappa."
    }
    print(json.dumps(receipt, sort_keys=True))
    print("PASS_INDEPENDENT_DEPTH27_ATTAINMENT")


if __name__ == "__main__":
    main()
