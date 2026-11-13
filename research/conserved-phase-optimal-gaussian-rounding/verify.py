#!/usr/bin/env python3
"""Cross-check the frozen integer and root Fraction implementations."""

from __future__ import annotations

from itertools import product
import hashlib
import json
from pathlib import Path
import random
from types import ModuleType


PACKAGE = Path(__file__).resolve().parent


def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def load_exact_source(name: str, path: Path) -> ModuleType:
    """Compile the recorded source bytes directly, independent of .pyc state."""
    source = path.read_bytes()
    module = ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


def flatten(pair):
    return (pair[0][0], pair[0][1], pair[1][0], pair[1][1])


def unflatten(vector):
    return ((vector[0], vector[1]), (vector[2], vector[3]))


def main() -> None:
    integer = load_exact_source("frozen_integer_checker",
                                PACKAGE / "proof" / "check.py")
    root = load_exact_source("root_fraction_checker",
                             PACKAGE / "review" / "root" / "check_candidate.py")

    source_manifest = json.loads((PACKAGE / "SOURCES.json").read_text(encoding="utf-8"))
    local_hashes = {row["path"]: row["sha256"]
                    for row in source_manifest.get("local_artifacts", [])}
    local_paths = (
        "proof/check.py", "proof/RESULT.json",
        "review/root/check_candidate.py", "review/root/RESULT.json",
    )
    local_bytes = {}
    for path in local_paths:
        local_bytes[path] = (PACKAGE / path).read_bytes()
        need(local_hashes.get(path) == hashlib.sha256(local_bytes[path]).hexdigest(),
             f"SOURCES.json local artifact hash mismatch: {path}")
    proof_hash = hashlib.sha256(local_bytes["proof/check.py"]).hexdigest()
    root_hash = hashlib.sha256(local_bytes["review/root/check_candidate.py"]).hexdigest()
    cube_count = 0
    for values in product(range(-4, 5), repeat=4):
        pair = unflatten(values)
        proof_out = integer.check_pair(pair)
        root_out = unflatten(root.check(values))
        need(proof_out == root_out,
             f"cross-implementation forward mismatch at {pair}: {proof_out} != {root_out}")
        proof_back = integer.inverse_pair(proof_out)
        root_back = unflatten(root.transform(flatten(root_out), inverse=True))
        need(proof_back == pair and root_back == pair,
             f"cross-implementation inverse mismatch at {pair}")
        cube_count += 1

    rng = random.Random(20261113)
    large_count = 0
    for digits in (1, 10, 100, 400):
        for _ in range(15):
            values = tuple(rng.randrange(-(10 ** digits), 10 ** digits)
                           for _ in range(4))
            pair = unflatten(values)
            proof_out = integer.check_pair(pair)
            root_out = unflatten(root.check(values))
            need(proof_out == root_out,
                 f"large cross-implementation mismatch at {pair}")
            need(integer.inverse_pair(proof_out) == pair
                 and unflatten(root.transform(flatten(root_out), inverse=True)) == pair,
                 f"large inverse mismatch at {pair}")
            large_count += 1

    power_count = 0
    for exponent in (0, 1, 8, 64, 512):
        n = 1 << exponent
        for pair in (
            ((n, 1), (-n, 0)),
            ((n, 0), (0, n)),
            ((n + 1, n), (0, 1)),
            ((n, n + 1), (1, 0)),
        ):
            proof_out = integer.check_pair(pair)
            root_out = unflatten(root.check(flatten(pair)))
            need(proof_out == root_out,
                 f"power-of-two cross-implementation mismatch at {pair}")
            need(integer.inverse_pair(proof_out) == pair
                 and unflatten(root.transform(flatten(root_out), inverse=True)) == pair,
                 f"power-of-two inverse mismatch at {pair}")
            power_count += 1

    # Exact negative control: the wrong p-dependent type assignment breaks
    # the global-i identity at this finite input.
    mutant_input = ((-2, -2), (-2, -1))
    mutant_out = integer.map_pair(mutant_input, phase_mutant=True)
    mutant_i_out = integer.map_pair(integer.phase_i(mutant_input), phase_mutant=True)
    expected_i_out = integer.phase_i(mutant_out)
    need(mutant_i_out != expected_i_out,
         "phase-assignment mutant unexpectedly passed the global-i identity")
    need(integer.map_pair(integer.phase_i(mutant_input))
         == integer.phase_i(integer.map_pair(mutant_input)),
         "correct phase rule failed at the mutant witness")

    # Exact negative control: this candidate has no F^4 identity.
    fourth_input = ((-2, -2), (-2, 1))
    first = integer.map_pair(fourth_input)
    fourth = fourth_input
    for _ in range(4):
        fourth = integer.map_pair(fourth)
    need(first == ((-1, -1), (-3, 0)), "F^4 control first image changed")
    need(fourth == ((-3, 0), (-1, -1)) and fourth != fourth_input,
         "F^4 counterexample control changed")

    # The n=1 instance of the pinned #6778 theorem: a row/column array made
    # from the exact-sum basis input. This checks the theorem's convention
    # against this map, not a new universal noncommutation proof.
    tensor_input = (
        ((0, -1), (0, 0)),  # row (-i, 0)
        ((1, 0), (0, 0)),   # row (1, 0)
    )

    def apply_rows(array):
        return tuple(integer.map_pair(row) for row in array)

    def apply_columns(array):
        columns = tuple(zip(*array))
        mapped = tuple(integer.map_pair(column) for column in columns)
        return tuple(tuple(row) for row in zip(*mapped))

    row_after_column = apply_rows(apply_columns(tensor_input))
    column_after_row = apply_columns(apply_rows(tensor_input))
    commutator = tuple(
        tuple((left[0] - right[0], left[1] - right[1])
              for left, right in zip(row_left, row_right))
        for row_left, row_right in zip(row_after_column, column_after_row)
    )
    need(row_after_column == (((1, 0), (0, -1)), ((0, 0), (0, 0))),
         "#6778 n=1 row-after-column result changed")
    need(column_after_row == (((0, 0), (1, -1)), ((0, 0), (0, 0))),
         "#6778 n=1 column-after-row result changed")
    need(commutator == (((1, 0), (-1, 0)), ((0, 0), (0, 0))),
         "#6778 exact row/column commutator changed")
    need(integer.map_pair(((1, 0), (0, 0))) == ((0, 0), (1, 0)),
         "#6778 conservative-bijection basis image changed")

    print(json.dumps({
        "status": "PASS_CONSERVED_PHASE_COVARIANT_CROSS_IMPLEMENTATIONS",
        "cube_cases": cube_count,
        "random_large_cases": large_count,
        "power_of_two_large_cases": power_count,
        "largest_random_decimal_digits": 400,
        "largest_power_of_two_exponent": 512,
        "phase_assignment_mutant": {
            "input": mutant_input,
            "mutant_output": mutant_out,
            "mutant_on_i_input": mutant_i_out,
            "i_of_mutant_output": expected_i_out,
            "global_i_identity_fails": True,
        },
        "fourth_power_control": {
            "input": fourth_input,
            "first_image": first,
            "fourth_iterate": fourth,
            "F4_identity_fails": True,
        },
        "pr_6778_n1_row_column_control": {
            "input_rows": tensor_input,
            "row_after_column": row_after_column,
            "column_after_row": column_after_row,
            "commutator": commutator,
            "same_map_tensor_commutation_fails": True,
        },
        "proof_integer_checker_sha256": proof_hash,
        "root_fraction_checker_sha256": root_hash,
        "scope": "finite exact cross-check of two implementations and explicit identity controls; the all-input theorem is proved in proof/PROOF.md",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
