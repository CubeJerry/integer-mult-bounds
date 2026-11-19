#!/usr/bin/env python3
"""Independent exact review of the native two-star algebraic target.

No author implementation is imported. Native binary elimination uses ascending
pivots, small controls use a different selector allocation, and movement prices
are recomputed from the retained profiles with authenticated integer powers.
"""
from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import random


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def basis(rows):
    pivots = {}
    for value in rows:
        while value:
            index = (value & -value).bit_length() - 1
            if index in pivots:
                value ^= pivots[index]
            else:
                pivots[index] = value
                break
    return list(pivots.values())


def rank(rows):
    return len(basis(rows))


def image(rows, vector):
    return sum(((row & vector).bit_count() & 1) << i
               for i, row in enumerate(rows))


def independent_selectors(width, neighbors, a=80, b=42, c=8):
    """Use front coordinates and round-robin donor slots, unlike the author."""
    wa = (width + len(neighbors[a]) - 1) // len(neighbors[a])
    wb = (width + len(neighbors[b]) - 1) // len(neighbors[b])
    ua = list(range(wa))
    ub = list(range(wa, wa + wb))
    outside = list(range(wa + wb, width))
    require(len(outside) >= wb - wa, "enough disjoint selector coordinates")

    def allocate(i, omitted, own, first):
        others = sorted(neighbors[i] - {omitted, c}, reverse=True)
        values = {j: [None] * len(own) for j in others}
        values[c] = first
        remaining = [t for t in range(width) if t not in set(own + first)]
        for slot, coordinate in enumerate(remaining):
            values[others[slot % len(others)]][slot // len(others)] = coordinate
        return values

    return ua, ub, allocate(a, b, ua, ub[:wa]), allocate(b, a, ub, ua + outside[:wb-wa])


def validate_selectors(width, neighbors, ua, ub, va, vb, a=80, b=42, c=8):
    require(set(ua).isdisjoint(ub), "disjoint shear images")
    require(len(set(ua)) == len(ua) and len(set(ub)) == len(ub), "injective image columns")
    for receiver, omitted, own, maps in ((a, b, ua, va), (b, a, ub, vb)):
        require(set(maps) == neighbors[receiver] - {omitted}, "literal native selector support")
        require(all(len(row) == len(own) for row in maps.values()), "selector matrix height")
        used = [k for row in maps.values() for k in row if k is not None]
        require(all(0 <= k < width for k in used), "selector coordinate bounds")
        require(set(used).isdisjoint(own), "every shear square is zero")
        require(set(used) == set(range(width)) - set(own), "intersection of selector kernels equals image")
    c_rows = va[c] + vb[c]
    require(None not in c_rows and len(set(c_rows)) == len(ua) + len(ub),
            "common-neighbor row block has full row rank")
    return {"modified_foreign_blocks": len(va) + len(vb),
            "Va_kernel_dimension": len(ua), "Vb_kernel_dimension": len(ub),
            "Vc_row_rank": len(ua) + len(ub)}


def delta_rows(width, ua, ub, va, vb, a=80, b=42):
    rows = [0] * (111 * width)
    for receiver, own, maps in ((a, ua, va), (b, ub, vb)):
        for donor, selected in maps.items():
            for target, source in zip(own, selected):
                if source is not None:
                    rows[receiver * width + target] ^= 1 << (donor * width + source)
    return rows


def tensor(native_rows, width):
    result = []
    for row in native_rows:
        template = sum(1 << (j * width) for j in range(111) if row >> j & 1)
        result.extend(template << k for k in range(width))
    return result


def flat_dimension(width, neighbors, perturbation):
    mask = (1 << width) - 1

    def equations():
        for receiver, donors in enumerate(neighbors):
            for donor in sorted(donors):
                for coordinate in range(width):
                    row = perturbation[receiver * width + coordinate]
                    block = (row >> (donor * width)) & mask
                    yield ((1 << (receiver * width + coordinate))
                           ^ (1 << (donor * width + coordinate))
                           ^ (block << (donor * width)))

    return 111 * width - rank(equations())


def small_control(width, neighbors, native_k):
    ua, ub, va, vb = independent_selectors(width, neighbors)
    validation = validate_selectors(width, neighbors, ua, ub, va, vb)
    change = delta_rows(width, ua, ub, va, vb)
    canonical = tensor(native_k, width)
    fitting = [x ^ y for x, y in zip(canonical, change)]
    h = len(ua) + len(ub)
    require(rank(change) == h, "small complete perturbation rank")
    require(rank(fitting) == 9 * width + h, "small complete fitting rank")
    require(rank(canonical + change) == 9 * width + h, "small complete retained repair rank")
    joint_dimension = flat_dimension(width, neighbors, change) if width <= 7 else None
    if joint_dimension is not None:
        require(joint_dimension == 0, "independent full native gauge solve")
    proper = [row ^ (1 << i) for i, row in enumerate(fitting)]
    rng = random.Random(53021 + width)
    for _ in range(16):
        x, y = rng.getrandbits(111 * width), rng.getrandbits(111 * width)
        endpoint = y ^ image(canonical, x) ^ image(change, x) ^ image(proper, x)
        require(endpoint == y ^ x, "algebraic return-bank endpoint identity")
    # Omitting the noncanonical syndrome fails on an explicit native input.
    input_coordinate = va[8][0]
    x = 1 << (8 * width + input_coordinate)
    require(image(canonical, x) ^ image(proper, x) != x, "missing correction is detected")
    return {"width": width, "image_widths": [len(ua), len(ub)],
            "fitting_rank": 9 * width + h, "retained_repair_rank": h,
            "joint_flat_solution_dimension": joint_dimension, "endpoint_controls": 16,
            "selector_validation": validation}


def negative_controls(neighbors):
    width = 7
    ua, ub, va, vb = independent_selectors(width, neighbors)
    outside = next(i for i in range(width) if i not in ua + ub)
    drop = lambda maps: {j: [None if k == outside else k for k in selected]
                         for j, selected in maps.items()}
    incomplete = delta_rows(width, ua, ub, drop(va), drop(vb))
    require(flat_dimension(width, neighbors, incomplete) == 1,
            "omitting one shared selector coordinate restores a flat line")
    one_star = delta_rows(width, ua, [], va, {})
    require(flat_dimension(width, neighbors, one_star) == len(ua),
            "a single star leaves its image flat")
    bad_shear = [(1 << k) ^ ((1 << ua[0]) if k == ua[0] else 0)
                 for k in range(width)]
    require(rank(bad_shear) == width - 1,
            "dropping the square-zero source restriction may destroy invertibility")
    # Each separation condition in the rank-addition lemma is necessary.
    m = [1, 0]
    column_separated_only = [0, 1]
    row_separated_only = [2, 0]
    require(rank([x ^ y for x, y in zip(m, column_separated_only)]) == 1,
            "column separation alone does not add ranks")
    require(rank([x ^ y for x, y in zip(m, row_separated_only)]) == 1,
            "row separation alone does not add ranks")
    return {"missing_selector_coordinate_restores_flat_dimension": 1,
            "single_star_flat_dimension": len(ua),
            "non_nilpotent_shear_is_singular": True,
            "either_one_sided_rank_separation_is_insufficient": True,
            "omitted_return_syndrome_fails": True}


def commutator_rank(width, ua, ub, va, vb):
    # Sparse basis-column action of the two individual nilpotent parts at c.
    na = {source: 1 << target for target, source in zip(ua, va[8])}
    nb = {source: 1 << target for target, source in zip(ub, vb[8])}
    def apply(mapping, vector):
        answer = 0
        while vector:
            bit = vector & -vector
            answer ^= mapping.get(bit.bit_length() - 1, 0)
            vector ^= bit
        return answer
    return rank(apply(na, nb.get(k, 0)) ^ apply(nb, na.get(k, 0))
                for k in range(width))


def movement():
    scale = 10 ** 36
    cache = {}
    def power(value):
        if value not in cache:
            with localcontext() as context:
                context.prec = 100
                floor = int(Decimal(value) ** (Decimal(199) / 200) * scale)
            target = value ** 199 * scale ** 200
            require(floor ** 200 <= target < (floor + 1) ** 200,
                    "independent exact irrational price enclosure")
            top = floor if floor ** 200 == target else floor + 1
            cache[value] = Fraction(floor, scale), Fraction(top, scale)
        return cache[value]
    def add(profile, gap, coefficient):
        profile[gap] += Fraction(coefficient)
    def interval(profile):
        low = high = Fraction(0)
        for gap, coefficient in profile.items():
            a, b = power(gap)
            low += coefficient * (a if coefficient >= 0 else b)
            high += coefficient * (b if coefficient >= 0 else a)
        return low, high
    n = {1:1386, 2:1253, 3:62, 4:47, 5:9, 6:104, 7:10}
    h = {2:1, 4:25, 6:1, 8:410}
    difference = Counter()
    for gap, coefficient in h.items(): add(difference, gap, 36 * coefficient)
    for gap, coefficient in n.items(): add(difference, gap, -36 * coefficient)
    add(difference, 127, 222)
    add(difference, 1, -444)
    for j in range(1, 10): add(difference, 1 + 7*j, 444)
    for j in range(1, 9): add(difference, 7*j, -444)
    q = {1:Fraction(4451,8), 2:Fraction(7213,16), 4:24,
         8:9 + Fraction(188,5760)}
    limit_profile = Counter({gap: coefficient / 36 for gap, coefficient in difference.items()})
    for gap, coefficient in n.items(): add(limit_profile, gap, coefficient)
    for gap, coefficient in h.items(): add(limit_profile, gap, -coefficient)
    for gap, coefficient in q.items(): add(limit_profile, gap, -coefficient)
    room = interval(limit_profile)
    require(room[0] > 0, "positive limiting movement room at h188")
    def finite(m):
        result = Counter({gap: coefficient * Fraction(m, 2)
                          for gap, coefficient in difference.items()})
        for gap, coefficient in n.items(): add(result, gap, 18*(m-1)*coefficient)
        for gap, coefficient in h.items(): add(result, gap, -18*(m-1)*coefficient)
        for gap, coefficient in q.items(): add(result, gap, -18*(m-1)*coefficient)
        return interval(result)
    previous, first = finite(626), finite(628)
    require(previous[1] < 0 < first[0], "independent finite movement crossing")
    def show(bounds):
        with localcontext() as context:
            context.prec = 50
            decimals = [str(Decimal(v.numerator)/Decimal(v.denominator)) for v in bounds]
        return {"rational": list(map(str, bounds)), "decimal": decimals}
    return {"limiting_room": show(room), "first_even_m": 628,
            "previous_m626_gap": show(previous), "first_m628_gap": show(first),
            "scope": "Movement screen only; no physical realization or full caller invoice"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--author", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = args.repo / "research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
    raw = source.read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e",
            "authenticated native source pin")
    roots = json.loads(raw)["native_roots"]
    require(len(roots) == 111, "111 native roles")
    neighbors = [{j for j, y in enumerate(roots)
                  if i != j and sum(v*w for v,w in zip(x,y)) == 0}
                 for i,x in enumerate(roots)]
    native_k = [sum(1 << j for j in donors) ^ (1 << i)
                for i, donors in enumerate(neighbors)]
    a, b, c = 80, 42, 8
    require(sum(map(len, neighbors)) == 6470, "all native foreign blocks")
    require((len(neighbors[a]),len(neighbors[b])) == (62,61), "native star degrees")
    require(b in neighbors[a] and c in neighbors[a] & neighbors[b], "native adjacent stars and common neighbor")
    canonical_basis = basis(native_k)
    require(len(canonical_basis) == 9, "native canonical rank")
    union = sum(1 << j for j in neighbors[a] | neighbors[b])
    pair = (1 << a) | (1 << b)
    require(rank(row & ~union for row in native_k) == 7, "outside-union rank")
    require(rank(row & ~pair for row in native_k) == 9, "outside-pair rank")
    supported_union = set()
    supported_pair = set()
    for coefficients in range(512):
        word = 0
        for i, row in enumerate(canonical_basis):
            if coefficients >> i & 1: word ^= row
        if word & ~union == 0: supported_union.add(word)
        if word & ~pair == 0: supported_pair.add(word)
    require(supported_union == {0,native_k[a],native_k[b],native_k[a]^native_k[b]},
            "all canonical words supported in the union are exactly the two-row span")
    require(supported_pair == {0}, "no canonical word supported at the two receiver roles")

    selected_path = args.author / "output/SELECTORS.json"
    selected = json.loads(selected_path.read_text())
    require((selected["a"], selected["b"], selected["common_neighbor"], selected["width"])
            == (80,42,8,5760), "submitted full-width construction identity")
    ua, ub = selected["Ua_coordinates"], selected["Ub_coordinates"]
    va = {int(j): row for j,row in selected["Va_selectors"].items()}
    vb = {int(j): row for j,row in selected["Vb_selectors"].items()}
    require((len(ua),len(ub)) == (93,95), "submitted shear widths")
    full = validate_selectors(5760,neighbors,ua,ub,va,vb)
    require(set(ua+ub) == set(range(5572,5760)), "literal common left prefix")
    require(a not in va and b not in va and a not in vb and b not in vb,
            "omitted cross-star columns essential for row separation")
    require(commutator_rank(5760,ua,ub,va,vb) == 186, "full-width additive commutator rank")
    controls = [small_control(width,neighbors,native_k) for width in (5,7,123)]
    negatives = negative_controls(neighbors)
    price = movement()
    author_result = json.loads((args.author / "output/RESULT.json").read_text())
    for key,value in {"excess_rank":188,"fitting_rank":52028,"fixed_bank_repair_rank":188,
                      "maximum_flat_gauge_subsystem_dimension":0,"common_correct_left_rows":5572}.items():
        require(author_result[key] == value, "author recorded value: " + key)
    result = {"status":"PASS_INDEPENDENT_NATIVE_TWO_STAR_REVIEW",
              "native_facts":{"rank_K":9,"outside_union_rank":7,"outside_pair_rank":9,
                              "supported_union_binary_codewords":4,"supported_pair_binary_codewords":1},
              "width":5760,"fitting_rank":52028,"excess_rank":188,"retained_repair_rank":188,
              "flat_gauge_dimension":0,"literal_common_left_rows":5572,"additive_commutator_rank":186,
              "full_selector_checks":full,"small_complete_matrix_controls":controls,
              "negative_controls":negatives,"movement":price,
              "scope":"Accept algebraic target and conditional movement screen only; no physical source realization"}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    files = [source,args.author/"PROOF.md",args.author/"check.py",selected_path,args.author/"output/RESULT.json"]
    (args.out / "REVIEW-PINS.json").write_text(json.dumps(
        [{"path":str(p.resolve()),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],indent=2)+"\n")
    print(result["status"])


if __name__ == "__main__":
    main()
