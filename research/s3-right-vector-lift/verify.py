#!/usr/bin/env python3
"""Exact F2[S3] lift and geometric two-factor obstruction.

Prepared for @CubeJerry with substantial OpenAI Codex assistance.
Apache-2.0. No external packages; checks remain active under python -O.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PERMS = tuple(itertools.permutations(range(3)))
INDEX = {p: i for i, p in enumerate(PERMS)}
ONE = 1 << INDEX[(0, 1, 2)]
TABLE = tuple(tuple(INDEX[tuple(p[q[k]] for k in range(3))] for q in PERMS)
              for p in PERMS)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def mul(a: int, b: int) -> int:
    """Convolution in the formal group basis, not a nonfaithful action."""
    out = 0
    for i in range(6):
        if a >> i & 1:
            for j in range(6):
                if b >> j & 1:
                    out ^= 1 << TABLE[i][j]
    return out


def mm(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(mul(a[2*i], b[j]) ^ mul(a[2*i+1], b[2+j])
                 for i in range(2) for j in range(2))


IDENTITY = (ONE, 0, 0, ONE)


def f2mm(a: int, b: int) -> int:
    out = 0
    for i, j, k in itertools.product(range(2), repeat=3):
        out ^= (((a >> (2*i+k)) & 1) & ((b >> (2*k+j)) & 1)) << (2*i+j)
    return out


def natural(p: tuple[int, ...]) -> int:
    # Nonzero vectors (1,0), (0,1), (1,1), encoded 1,2,3.
    columns = (p[0] + 1, p[1] + 1)
    return sum(((columns[j] >> i) & 1) << (2*i+j)
               for i in range(2) for j in range(2))


RHO = tuple(natural(p) for p in PERMS)
PARITY = tuple(sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)) % 2
               for p in PERMS)


def rho(a: int) -> int:
    out = 0
    for i in range(6):
        if a >> i & 1:
            out ^= RHO[i]
    return out


def pi(a: int) -> int:
    """Quotient S3 -> C2, with e and the transposition encoded 1 and 2."""
    out = 0
    for i in range(6):
        if a >> i & 1:
            out ^= 1 << PARITY[i]
    return out


def c2mul(a: int, b: int) -> int:
    return ((a & 1) & (b & 1)) ^ (((a >> 1) & (b >> 1)) & 1) ^ (
        (((a & 1) & (b >> 1)) ^ ((a >> 1) & (b & 1))) << 1)


def rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for v in vectors:
        while v:
            k = v.bit_length() - 1
            if k in pivots:
                v ^= pivots[k]
            else:
                pivots[k] = v
                break
    return len(pivots)


def span(vectors: tuple[int, ...]) -> set[int]:
    out = {0}
    for v in vectors:
        out |= {x ^ v for x in out}
    return out


def apply4(rows: tuple[int, ...], v: int) -> int:
    return sum(((r & v).bit_count() & 1) << i for i, r in enumerate(rows))


def ring_matrix_columns(m: tuple[int, ...]) -> list[int]:
    return [m[j] | (m[j+2] << 6) for j in range(2)]


def regular_columns(m: tuple[int, ...]) -> list[int]:
    return [mul(m[j], 1 << k) | (mul(m[2+j], 1 << k) << 6)
            for j in range(2) for k in range(6)]


def make_certificate() -> dict:
    # Complete 64-element algebra check of the explicit product decomposition.
    images = {(pi(a), rho(a)) for a in range(64)}
    require(len(images) == 64, "product map is not injective")
    for a, b in itertools.product(range(64), repeat=2):
        require(rho(mul(a, b)) == f2mm(rho(a), rho(b)), "rho is not multiplicative")
        require(pi(mul(a, b)) == c2mul(pi(a), pi(b)), "pi is not multiplicative")
    lift = {rho(a): a for a in range(64) if pi(a) == 0}
    require(len(lift) == 16, "matrix block has wrong dimension")
    units = [lift[1 << k] for k in range(4)]
    for i, j, k, l in itertools.product(range(2), repeat=4):
        require(mul(units[2*i+j], units[2*k+l]) == (units[2*i+l] if j == k else 0),
                "matrix-unit multiplication failed")
    a_cycle = 1 << INDEX[(1, 2, 0)]
    central_e = ONE ^ a_cycle ^ mul(a_cycle, a_cycle)
    central_f = ONE ^ central_e
    require(mul(central_e, central_e) == central_e, "e is not idempotent")
    require(mul(central_f, central_f) == central_f, "f is not idempotent")
    require(mul(central_e, central_f) == 0, "blocks are not orthogonal")
    require(lift[9] == central_f and pi(central_e) == 1 and rho(central_e) == 0,
            "wrong block identities")
    for x in range(64):
        require(mul(central_e, x) == mul(x, central_e), "e is not central")

    a, b = units[1], units[2]
    first = (ONE, a, 0, ONE)
    second = (ONE, 0, b, ONE)
    target = (central_e ^ units[3], a, b, central_e ^ units[0])
    product = mm(mm(first, second), first)
    require(product == target, "three-factor lift fails")
    require(mm(target, target) == IDENTITY, "full target is not an involution")
    require(mm(first, first) == IDENTITY and mm(second, second) == IDENTITY,
            "paid factors do not return under repetition")
    require(tuple(pi(x) for x in target) == (1, 0, 0, 1), "C2 component is not preserved")
    require(tuple(rho(x) for x in target) == (8, 2, 4, 1), "wrong quotient target")

    # Every free GL2(F2) map, with entries in the central base field.
    gl2 = [bits for bits in itertools.product((0, ONE), repeat=4)
           if rank([bits[0] | bits[2] << 1, bits[1] | bits[3] << 1]) == 2]
    require(len(gl2) == 6, "wrong GL2 size")
    dims = [rank(ring_matrix_columns(tuple(x ^ y for x, y in zip(mm(target, t), IDENTITY))))
            for t in gl2]
    require(dims == [2] * 6, "column-bound minimum is not two")

    # Written proof uses these three kernels; this is its complete tiny table.
    planes = [span(v) for v in ((1, 2), (4, 8), (5, 10))]
    p_rows = (8, 2, 4, 1)  # transposition of coordinates 0 and 3
    intersections = []
    for h in planes:
        row = []
        for k in planes:
            common = h & {apply4(p_rows, v) for v in k}
            require(len(common) == 2, "target does not exchange the two plane families")
            row.append(next(v for v in common if v))
        intersections.append(row)
    require(all(len(h & k) in (1, 4) for h in planes for k in planes),
            "kernel planes are not equal or complementary")
    for t in gl2:
        rows = (t[0] | t[1] << 2, t[0] << 1 | t[1] << 3,
                t[2] | t[3] << 2, t[2] << 1 | t[3] << 3)
        require({frozenset(apply4(rows, v) for v in h) for h in planes}
                == {frozenset(h) for h in planes}, "free map fails to permute kernel planes")

    # Controls target distinct ways to lose a component or underprice the word.
    omitted = [mm(second, first), mm(first, first), mm(first, second)]
    require(all(m != target for m in omitted), "an omitted factor was undetected")
    missing_e = (units[3], a, b, units[0])
    require(tuple(rho(x) for x in missing_e) == tuple(rho(x) for x in target),
            "hidden-component control must pass the quotient")
    require(tuple(pi(x) for x in missing_e) == (0, 0, 0, 0)
            and rank(regular_columns(missing_e)) == 8, "hidden-component control not rejected")
    require(rank(regular_columns(target)) == 12, "full regular action is not invertible")
    require(mm(mm(second, first), first) != target, "wrong chronology was undetected")
    wrong_a = a ^ ONE
    wrong_first = (ONE, wrong_a, 0, ONE)
    require(mm(mm(wrong_first, second), wrong_first) != target, "coefficient mutation undetected")
    free_swap = (0, ONE, ONE, 0)
    raw = rank(ring_matrix_columns(tuple(x ^ y for x, y in zip(free_swap, IDENTITY))))
    free_dims = [rank(ring_matrix_columns(tuple(x ^ y for x, y in zip(mm(free_swap, t), IDENTITY))))
                 for t in gl2]
    require(raw == 1 and min(free_dims) == 0, "free-map normalization control failed")
    require([x for x in range(64) if rho(x) == 0] == [0, central_e, 63 ^ central_e, 63],
            "unexpected hidden component")
    return {
        "schema_version": 1,
        "claim": "One explicit F2[S3] target has paid right-vector cost 3 and free-basis column bound 2.",
        "base_commit": "12fa8c5c844be21bfefb38a19503fbd867a11244",
        "assignment_seed": 1,
        "group_basis": [list(p) for p in PERMS],
        "composition": "p*q means apply q first, then p; mask bit i is coefficient of group_basis[i]",
        "rho_basis_row_major_masks": list(RHO),
        "parity_basis": list(PARITY),
        "central_e": central_e,
        "central_f": central_f,
        "matrix_units_row_major": units,
        "matrix_lift_masks_0_to_15": [lift[k] for k in range(16)],
        "target_row_major": list(target),
        "chronological_factors": [list(first), list(second), list(first)],
        "right_vector_parameters": [
            {"u": [a, 0], "y": [0, 1]},
            {"u": [0, b], "y": [1, 0]},
            {"u": [a, 0], "y": [0, 1]},
        ],
        "free_maps_row_major": [list(t) for t in gl2],
        "column_dimensions": dims,
        "kernel_planes_nonzero_masks": [sorted(h - {0}) for h in planes],
        "intersection_nonzero_vectors_rows_H_columns_P_H": intersections,
        "regular_target_columns": regular_columns(target),
        "checks": {"product_algebra_elements": 64, "multiplication_pairs": 4096,
                   "matrix_unit_products": 16, "free_bases": 6, "plane_intersections": 9,
                   "regular_action_rank": 12, "hidden_component_control_rank": 8},
        "controls": ["each_of_three_omissions", "quotient_only_missing_central_component",
                     "wrong_chronology", "one_coefficient_mutation", "free_map_normalization"],
        "cost_ledger": {"paid_factors": 3, "free_basis_changes": 0, "registers": 2,
                        "auxiliary_registers": 0, "terminal_restoration_factors": 0,
                        "native_supplier_cost": "not instantiated; no native or recursive admission claimed"},
        "no_new_kappa": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-certificate", action="store_true", help="regenerate only this package's certificate")
    args = parser.parse_args()
    sources = json.loads((HERE / "SOURCES.json").read_text(encoding="utf-8"))
    for source in sources["external_predecessors"]:
        raw = (HERE / source["retained_path"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == source["sha256"], "retained predecessor SHA256 mismatch")
        blob = b"blob " + str(len(raw)).encode() + b"\0" + raw
        require(hashlib.sha1(blob).hexdigest() == source["git_blob"], "retained predecessor Git blob mismatch")
    result = make_certificate()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = HERE / "CERTIFICATE.json"
    if args.write_certificate:
        path.write_text(encoded, encoding="utf-8")
    else:
        require(json.loads(path.read_text(encoding="utf-8")) == result, "committed certificate differs")
    print("PASS_S3_RIGHT_VECTOR_LIFT cost=3 column_bound=2 algebra_pairs=4096 "
          "free_bases=6 plane_intersections=9 no_new_kappa "
          "certificate_sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
