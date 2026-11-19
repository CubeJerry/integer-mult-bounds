#!/usr/bin/env python3
"""Exact native irreducible target; not a physical-network realization."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def require(value: bool, label: str) -> None:
    if not value:
        raise ValueError(label)


def rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for value in rows:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def transpose(rows: list[int], n: int) -> list[int]:
    out = [0] * n
    for i, value in enumerate(rows):
        while value:
            bit = value & -value
            out[bit.bit_length() - 1] ^= 1 << i
            value ^= bit
    return out


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = []
    for value in left:
        result = 0
        while value:
            bit = value & -value
            result ^= right[bit.bit_length() - 1]
            value ^= bit
        out.append(result)
    return out


def power(rows: list[int], exponent: int) -> list[int]:
    out = [1 << i for i in range(len(rows))]
    base = rows
    while exponent:
        if exponent & 1:
            out = multiply(out, base)
        base = multiply(base, base)
        exponent >>= 1
    return out


def generators(w: int) -> list[list[int]]:
    require(w >= 2, "nontrivial internal bank")
    b = 60 * w
    jordan = [0] * b
    closing = [0] * b
    for k in range(w - 1):
        jordan[k] = 1 << (k + 1)
    closing[w - 1] = 1
    out = [jordan, closing]
    for block in range(1, 60):
        rows = [0] * b
        for k in range(w):
            rows[k] = 1 << (block * w + k)
        out.append(rows)
    return out


def geometry(roots: list[list[int]]) -> tuple[list[set[int]], list[int]]:
    require(len(roots) == 111, "111 original roots")
    neighbors = [
        {j for j, y in enumerate(roots)
         if i != j and sum(u * v for u, v in zip(x, y)) == 0}
        for i, x in enumerate(roots)
    ]
    canonical = [(1 << i) | sum(1 << j for j in neighbors[i]) for i in range(111)]
    require(rank(canonical) == 9, "canonical rank nine")
    require(sum(map(len, neighbors)) == 6470, "all foreign edges")
    seen = {0}
    todo = [0]
    while todo:
        for j in neighbors[todo.pop()] - seen:
            seen.add(j)
            todo.append(j)
    require(len(seen) == 111, "native connectivity")
    a, d = 80, 10
    require(d not in neighbors[a] and a != d, "separated centers")
    require((len(neighbors[a]), len(neighbors[d])) == (62, 61), "actual star degrees")
    all_bits = (1 << 111) - 1
    for support in [neighbors[a] | {d}, {a} | neighbors[d]]:
        complement = all_bits ^ sum(1 << j for j in support)
        require(rank([row & complement for row in canonical]) == 9, "native support separation")
    return neighbors, canonical


def assignment(neighbors: list[set[int]], w: int) -> dict[tuple[int, int], list[int]]:
    g = generators(w)
    b = 60 * w
    out = {(80, j): rows for j, rows in zip(sorted(neighbors[80]), g + [[0] * b])}
    for i, rows in zip(sorted(neighbors[10]), g):
        require((i, 10) not in out, "disjoint block stars")
        out[i, 10] = transpose(rows, b)
    for i, j in out:
        require(j in neighbors[i], "native proper support")
        require((j, i) not in out or not any(out[j, i]), "identity reverse direction")
    return out


def full_native_control(neighbors: list[set[int]], canonical: list[int], w: int) -> dict:
    b = 60 * w
    blocks = assignment(neighbors, w)
    canon_rows = [sum(1 << (j * b + k) for j in range(111) if (canonical[i] >> j) & 1)
                  for i in range(111) for k in range(b)]
    delta = [0] * (111 * b)
    for (i, j), rows in blocks.items():
        for k, row in enumerate(rows):
            delta[i * b + k] ^= row << (j * b)
        require(rank([row ^ (1 << k) for k, row in enumerate(rows)]) == b,
                "every full foreign block invertible")
    fitting = [x ^ y for x, y in zip(canon_rows, delta)]
    require(rank(delta) == 2 * w, "literal perturbation rank")
    require(rank(fitting) == 9 * b + 2 * w, "literal native fitting rank")
    require(rank(canon_rows + delta) == 9 * b + 2 * w, "literal retained quotient rank")
    return {"w": w, "b": b, "h": 2 * w, "q": 9 * b + 2 * w,
            "full_matrix_dimension": 111 * b, "foreign_block_checks": len(blocks)}


def algebra_control(w: int) -> dict:
    b = 60 * w
    g = generators(w)
    identity = [1 << k for k in range(b)]
    J, E = g[:2]
    units = {}
    for r in range(w):
        for s in range(w):
            unit = multiply(multiply(power(J, w - 1 - r), E), power(J, s))
            expected = [0] * b
            expected[r] = 1 << s
            require(unit == expected, "Jordan-closing matrix-unit identity")
            units[r, s] = unit
    transports = [identity] + g[2:]
    transposes = [transpose(t, b) for t in transports]
    count = 0
    for left in range(60):
        for right in range(60):
            for r in range(w):
                for s in range(w):
                    unit = multiply(multiply(transposes[left], units[r, s]), transports[right])
                    expected = [0] * b
                    expected[left * w + r] = 1 << (right * w + s)
                    require(unit == expected, "full bank-to-bank matrix unit")
                    count += 1
    require(count == b * b, "complete matrix-unit coverage")
    require(rank([row for matrix in g for row in matrix]) == b, "zero common right kernel")
    require(rank([row for matrix in g for row in transpose(matrix, b)]) == w,
            "one-sided family retains b-w left covectors")
    # Removing all transposed generators leaves the proper invariant U.
    require(all((row & ((1 << w) - 1)) == 0 for matrix in g for row in matrix[w:]),
            "one-sided proper invariant subspace control")
    # One diagonal term makes I+E singular; nilpotence is essential.
    bad = [0] * b
    bad[0] = 1
    require(rank([bad[k] ^ (1 << k) for k in range(b)]) == b - 1,
            "nonnilpotent mutation rejected")
    return {"w": w, "b": b, "all_matrix_units": count,
            "one_sided_flat_left_dimension": b - w,
            "common_right_kernel_dimension": 0}


def full_width_structure(w: int) -> dict:
    # No 111b-square matrix is materialized. These sparse generator checks
    # instantiate the written factorization for all three actual bank sizes.
    b = 60 * w
    g = generators(w)
    require(len(g) == 61, "61 available generator blocks")
    require(power(g[0], w) == [0] * b, "full-width Jordan nilpotence")
    require(any(power(g[0], w - 1)), "exact Jordan nilpotence index")
    for rows in g[1:]:
        require(multiply(rows, rows) == [0] * b, "full-width square-zero generators")
    require(rank([row for rows in g for row in rows]) == b, "full-width kernel coverage")
    return {"b": b, "w": w, "h": 2 * w, "q": 9 * b + 2 * w,
            "generator_count": 61, "native_block_assignments": 123,
            "nonidentity_foreign_blocks": 122, "excess_ratio": "1/30"}


def budget_check(data: dict) -> dict:
    entry = data["every_r_zero_through_203"][192]
    require(entry["r"] == 192 and entry["first_even_m"] == 870, "inherited exact comparison")
    for name, pair in data["power_enclosures"].items():
        low, high = map(Fraction, pair["rational"])
        value = int(name) ** 199
        require(low ** 200 <= value <= high ** 200, "exact rational power enclosure")
    room = list(map(Fraction, entry["limiting_room"]["rational"]))
    previous = list(map(Fraction, entry["previous_gap"]["rational"]))
    first = list(map(Fraction, entry["first_positive_gap"]["rational"]))
    require(room[0] > 0 and previous[1] < 0 and first[0] > 0, "strict movement sign controls")
    for b in [480, 1920, 5760]:
        require(Fraction(2 * (b // 60), b) == Fraction(192, 5760), "normalized paid ratio")
    return {"first_even_m": 870, "previous_even_m": 868,
            "limiting_room": entry["limiting_room"], "inherited_excess_at_b5760": 192,
            "inherited_budget_only": True, "power_enclosures_checked": len(data["power_enclosures"])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    prog = args.repo / "research/moonshot-005-program"
    source = prog / "sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
    budget = prog / "results/bit-canonical-quotient-repair/author/output/BUDGET.json"
    predecessor = prog / "results/bit-one-star-nilpotent-target/author/PROOF.md"
    two_star = prog / "results/bit-one-star-nilpotent-target/development/two-star188/author/PROOF.md"
    replacement = prog / "results/bit-replacement-return-bank/author/PROOF.md"
    roots = json.loads(source.read_text())["native_roots"]
    neighbors, canonical = geometry(roots)
    full_controls = [full_native_control(neighbors, canonical, w) for w in [2, 3]]
    algebra = [algebra_control(w) for w in [2, 3]]
    structural = [full_width_structure(w) for w in [8, 32, 96]]
    movement = budget_check(json.loads(budget.read_text()))
    pins = [{"path": str(p.relative_to(args.repo)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in [source, budget, predecessor, two_star, replacement]]
    result = {
        "status": "PASS_NATIVE_IRREDUCIBLE_TARGET",
        "scope": "algebraic endpoint target only; no physical source or decoder realization",
        "baseline_programme_sha": "882a135e95d5f3202ab3c20784668b627a26628e",
        "row_center": 80, "column_center": 10,
        "degrees": [62, 61], "foreign_blocks": 6470,
        "theorem_domain": "every characteristic-two field and b=60w, integer w>=2",
        "finite_bank_transport_irreducible": True,
        "body_tensor_irreducible_claimed": False,
        "flat_input_dimension": 0, "flat_output_quotient_dimension": 0,
        "full_native_controls": full_controls, "matrix_algebra_controls": algebra,
        "full_width_structural_instances": structural, "movement": movement,
        "negative_controls": {
            "one_sided_star_retains_left_quotient": True,
            "one_sided_star_has_proper_invariant_bank": True,
            "diagonal_nonnilpotent_mutation_singular": True,
            "adjacent_center_rejected": 42 in neighbors[80],
        },
        "new_complete_kappa": False, "all_five_foundations_retained": True,
        "source_pins": pins,
    }
    require(result["negative_controls"]["adjacent_center_rejected"], "adjacent control geometry")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    assignments = {str(b): {"w": b // 60,
                           "row_neighbors_in_generator_order": sorted(neighbors[80]),
                           "column_neighbors_in_transposed_generator_order": sorted(neighbors[10]),
                           "generators": ["J", "E"] + [f"T_{k}" for k in range(1, 60)],
                           "last_row_neighbor_generator": "zero"}
                   for b in [480, 1920, 5760]}
    (args.out / "ASSIGNMENT.json").write_text(json.dumps(assignments, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "excesses": [16, 64, 192],
                      "full_matrix_units_checked": sum(x["all_matrix_units"] for x in algebra),
                      "first_even_m": movement["first_even_m"]}, sort_keys=True))


if __name__ == "__main__":
    main()
