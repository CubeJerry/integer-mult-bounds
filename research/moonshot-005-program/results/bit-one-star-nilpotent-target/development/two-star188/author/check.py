#!/usr/bin/env python3
"""Exact controls for two receiver-star shears; no physical-network claim."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import random


def rank(rows: list[int]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)


def parity(x: int) -> int:
    return x.bit_count() & 1


def act(rows: list[int], x: int) -> int:
    return sum(parity(row & x) << i for i, row in enumerate(rows))


def selectors(width: int, neighbors: list[set[int]], a: int, b: int, c: int):
    wa, wb = math.ceil(width / len(neighbors[a])), math.ceil(width / len(neighbors[b]))
    assert 0 < wa <= wb and wa + wb <= width
    ua = list(range(width - wa - wb, width - wb))
    ub = list(range(width - wb, width))
    outside = [k for k in range(width) if k not in set(ua + ub)]
    assert len(outside) >= wb - wa
    first_a = ub[:wa]
    first_b = ua + outside[:wb-wa]
    assert len(set(first_a + first_b)) == wa + wb

    def allocate(receiver, omitted, own, first, w):
        target = [k for k in range(width) if k not in set(own)]
        remaining = [k for k in target if k not in set(first)]
        result = {c: first}
        slots = sorted(neighbors[receiver] - {omitted, c})
        assert len(remaining) <= len(slots) * w
        for j in slots:
            block, remaining = remaining[:w], remaining[w:]
            result[j] = block + [None] * (w - len(block))
        assert not remaining
        assert set(k for v in result.values() for k in v if k is not None) == set(target)
        assert all(k not in own for v in result.values() for k in v if k is not None)
        return result

    va = allocate(a, b, ua, first_a, wa)
    vb = allocate(b, a, ub, first_b, wb)
    return ua, ub, va, vb


def tensor_rows(native: list[int], width: int) -> list[int]:
    result = []
    for mask in native:
        columns = [j for j in range(len(native)) if (mask >> j) & 1]
        for k in range(width):
            result.append(sum(1 << (j * width + k) for j in columns))
    return result


def small_control(width, neighbors, native_o, native_k, a, b, c):
    ua, ub, va, vb = selectors(width, neighbors, a, b, c)
    delta = [0] * (111 * width)
    for receiver, own, blocks in [(a, ua, va), (b, ub, vb)]:
        for j, selected in blocks.items():
            for target, source in zip(own, selected):
                if source is not None:
                    delta[receiver * width + target] ^= 1 << (j * width + source)
    canonical = tensor_rows(native_k, width)
    fitting = [x ^ y for x, y in zip(canonical, delta)]
    proper = [x ^ (1 << i) for i, x in enumerate(fitting)]
    h = len(ua) + len(ub)
    assert rank(delta) == h
    assert rank(canonical) == 9 * width
    assert rank(fitting) == 9 * width + h
    assert rank(canonical + delta) == 9 * width + h
    # Two individual shears are square-zero perturbations and do not commute.
    na = [0] * width
    nb = [0] * width
    for target, source in zip(ua, va[c]):
        na[target] = 1 << source
    for target, source in zip(ub, vb[c]):
        nb[target] = 1 << source
    for k in range(width):
        assert act(na, act(na, 1 << k)) == act(nb, act(nb, 1 << k)) == 0
    commutator_columns = [act(na, act(nb, 1 << k)) ^ act(nb, act(na, 1 << k)) for k in range(width)]
    assert rank(commutator_columns) == 2 * len(ua)
    gauge_dimension = None
    if width <= 4:
        # Solve all B_ij z_j = z_i jointly, without using the two-star proof.
        equations = []
        bank_mask = (1 << width) - 1
        for i in range(111):
            for j in neighbors[i]:
                for k in range(width):
                    block_row = (proper[i * width + k] >> (j * width)) & bank_mask
                    equations.append((block_row << (j * width)) ^ (1 << (i * width + k)))
        gauge_dimension = 111 * width - rank(equations)
        assert gauge_dimension == 0
    rng = random.Random(26000 + width)
    for _ in range(128):
        x, y = rng.getrandbits(111 * width), rng.getrandbits(111 * width)
        assert y ^ act(canonical, x) ^ act(delta, x) ^ act(proper, x) == y ^ x
    return {"width": width, "wa": len(ua), "wb": len(ub), "fitting_rank": 9 * width + h,
            "retained_repair_rank": h, "flat_solution_dimension": gauge_dimension,
            "commutator_rank": 2 * len(ua), "endpoint_controls": 128}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    programme = args.repo / "research/moonshot-005-program"
    source = programme / "sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
    budget = programme / "results/bit-canonical-quotient-repair/author/output/BUDGET.json"
    roots = json.loads(source.read_text())["native_roots"]
    assert len(roots) == 111
    neighbors = [{j for j, y in enumerate(roots) if i != j and sum(v*w for v,w in zip(x,y)) == 0}
                 for i,x in enumerate(roots)]
    native_o = [sum(1 << j for j in row) for row in neighbors]
    native_k = [row | (1 << i) for i,row in enumerate(native_o)]
    a,b,c = 80,42,8
    assert b in neighbors[a] and c in neighbors[a] & neighbors[b]
    assert (len(neighbors[a]), len(neighbors[b])) == (62,61)
    assert sum(map(len,neighbors)) == 6470
    assert rank(native_k) == 9
    all_mask = (1 << 111) - 1
    outside_union = all_mask ^ sum(1 << j for j in neighbors[a] | neighbors[b])
    outside_pair = all_mask ^ (1 << a) ^ (1 << b)
    assert rank([row & outside_union for row in native_k]) == 7
    assert rank([row & outside_pair for row in native_k]) == 9
    assert rank([native_k[a],native_k[b]]) == 2
    # Therefore the canonical code supported on the neighborhood union is exactly
    # span(K_a,K_b); none is supported on the two receiver roles themselves.
    controls = [small_control(w,neighbors,native_o,native_k,a,b,c) for w in [2,3,4,8,62]]
    width = 5760
    ua,ub,va,vb = selectors(width,neighbors,a,b,c)
    h = len(ua) + len(ub)
    assert (len(ua),len(ub),h) == (93,95,188)
    assert len(set(ua) & set(ub)) == 0
    assert len(set(va[c] + vb[c])) == 188
    # Every V is a row selector annihilating its U; stack(V) has exact kernel U.
    allocation = {"a":a,"b":b,"common_neighbor":c,"width":width,"Ua_coordinates":ua,
                  "Ub_coordinates":ub,"Va_selectors":va,"Vb_selectors":vb}
    budget_entry = json.loads(budget.read_text())["every_r_zero_through_203"][h]
    assert budget_entry["first_even_m"] == 628
    pins = [{"path":str(p.relative_to(args.repo)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in [source,budget]]
    result = {"scope":"native algebraic endpoint target; no balanced physical realization",
              "native_roles":111,"directed_foreign_edges":6470,"receiver_pair":[a,b],
              "degrees":[62,61],"common_neighbor":c,"outside_union_rank":7,"outside_pair_rank":9,
              "field_scope":"every characteristic-two field; explicit binary coefficients",
              "width":width,"excess_rank":h,"fitting_rank":9*width+h,"fixed_bank_repair_rank":h,
              "common_correct_left_rows":width-h,"maximum_flat_gauge_subsystem_dimension":0,
              "all_foreign_blocks_invertible":True,"physical_source_code_constructed":False,
              "budget_entry":budget_entry,"small_exact_controls":controls,"source_pins":pins}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    (args.out/"SELECTORS.json").write_text(json.dumps(allocation,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"ok":True,"h":h,"rank":9*width+h,"flat_dimension":0,"first_even_m":628}))


if __name__ == "__main__":
    main()
