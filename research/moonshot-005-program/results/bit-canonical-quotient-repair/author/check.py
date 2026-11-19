#!/usr/bin/env python3
"""Exact finite controls for the fixed-code canonical-quotient repair theorem.

No author implementation is imported. This does not materialize the large
balanced GF(2^30) coefficient assignment.
"""
from __future__ import annotations

from argparse import ArgumentParser
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import gzip
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def elimination(rows: list[int]) -> dict[int, tuple[int, int]]:
    pivots: dict[int, tuple[int, int]] = {}
    for index, original in enumerate(rows):
        value, coefficient = original, 1 << index
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (value, coefficient)
                break
            row, expression = pivots[pivot]
            value ^= row
            coefficient ^= expression
    return pivots


def rank(rows: list[int]) -> int:
    return len(elimination(rows))


def expression(value: int, pivots: dict[int, tuple[int, int]]) -> int | None:
    coefficients = 0
    while value:
        pivot = value.bit_length() - 1
        if pivot not in pivots:
            return None
        row, mask = pivots[pivot]
        value ^= row
        coefficients ^= mask
    return coefficients


def basis(rows: list[int]) -> list[int]:
    return [value for value, _ in elimination(rows).values()]


def span(rows: tuple[int, ...] | list[int]) -> frozenset[int]:
    result = {0}
    for row in rows:
        result |= {value ^ row for value in list(result)}
    return frozenset(result)


def evaluate(rows: list[int], value: int) -> int:
    return sum(((row & value).bit_count() & 1) << i
               for i, row in enumerate(rows))


def linear_combination(mask: int, rows: list[int]) -> int:
    result = 0
    while mask:
        low = mask & -mask
        result ^= rows[low.bit_length() - 1]
        mask ^= low
    return result


def apply_matrix(rows: list[int], vectors: list[int]) -> list[int]:
    return [linear_combination(row, vectors) for row in rows]


def complement(h: list[int], t: list[int]) -> list[int]:
    joint = list(h)
    result = []
    for row in t:
        if expression(row, elimination(joint)) is None:
            result.append(row)
            joint.append(row)
    return result


def small_controls() -> dict:
    subspaces = sorted({span(rows) for size in range(4)
                        for rows in combinations(range(1, 8), size)},
                       key=lambda item: (len(item), sorted(item)))
    require(len(subspaces) == 16, "all sixteen subspaces of F2^3")
    g = [3, 2, 4]  # One nontrivial invertible ground-to-endpoint map.
    require([evaluate(g, evaluate(g, 1 << i)) for i in range(3)]
            == [1, 2, 4], "G inverse is G in the exhaustive control")
    cases, fibres, all_input_pairs = 0, 0, 0
    histogram: Counter[int] = Counter()
    for subspace in subspaces:
        h = basis(list(subspace))
        for target_tuple in product(range(8), repeat=3):
            t = list(target_tuple)
            r = rank(h + t) - len(h)
            ell = complement(h, t)
            require(len(ell) == r, "quotient basis size")
            messages = h + ell
            pivots = elimination(messages)
            decoding = [expression(row, pivots) for row in t]
            require(all(mask is not None for mask in decoding), "target decodes")
            decoded_rows = [linear_combination(int(mask), messages)
                            for mask in decoding]
            require(decoded_rows == t, "every target row from H plus syndrome")
            by_h: dict[int, set[int]] = defaultdict(set)
            b = [row ^ (1 << i) for i, row in enumerate(t)]
            for x in range(8):
                tx = evaluate(t, x)
                by_h[evaluate(h, x)].add(tx)
                mx = evaluate(messages, x)
                decoded = evaluate([int(mask) for mask in decoding], mx)
                require(decoded == tx, "actual message values decode T x")
                for y in range(8):
                    z = evaluate(g, y ^ decoded)
                    endpoint = evaluate(g, z) ^ evaluate(b, x)
                    require(endpoint == y ^ x, "all-input repair identity")
                    all_input_pairs += 1
            require(all(len(values) == 1 << r for values in by_h.values()),
                    "exact target cardinality on every H fibre")
            fibres += len(by_h)
            cases += 1
            histogram[r] += 1
    # A receiver with identical H messages but distinct target values cannot
    # be repaired by a zero-length new message, even nonlinearly.
    h, t = [1], [2, 0, 0]
    require(evaluate(h, 0) == evaluate(h, 2)
            and evaluate(t, 0) != evaluate(t, 2),
            "missing syndrome is detected by an exact H-fibre collision")
    # Failing to undo a nonidentity pure-Y map corrupts arbitrary Y, even X=0.
    require(evaluate(g, 2) != 2,
            "omitted late inverse corrupts an arbitrary original Y")
    return {"binary_input_dimension": 3, "canonical_subspaces": 16,
            "target_maps": 512, "cases": cases, "fibres": fibres,
            "all_X_Y_pairs_checked": all_input_pairs,
            "quotient_rank_histogram": dict(sorted(histogram.items())),
            "negative_controls": ["missing syndrome on fixed H fibre",
                                  "omitted inverse on arbitrary original Y"]}


def native_controls(layout: dict) -> dict:
    roots = layout["root_table"][:111]
    o = [sum(1 << j for j, right in enumerate(roots)
             if sum(a * b for a, b in zip(left, right)) == 0)
         for left in roots]
    k = [row ^ (1 << i) for i, row in enumerate(o)]
    h = basis(k)
    require(rank(o) == 108 and len(h) == 9, "native O and K ranks")
    full = (1 << 111) - 1
    outside = [rank([row & (full ^ neighbours) for row in h])
               for neighbours in o]
    require(outside == [9] * 111, "canonical restriction injective at every F_i")
    require(sum(row.bit_count() for row in o) == 6470, "all native foreign edges")
    require(o[0] & 2 and o[1] & 1, "roles zero and one are orthogonal")

    def tensor_row(row: int, lane: int) -> int:
        return sum(1 << (2 * j + lane) for j in range(111) if row >> j & 1)

    ot = [tensor_row(row, lane) for row in o for lane in range(2)]
    kt = [tensor_row(row, lane) for row in k for lane in range(2)]
    ht = [tensor_row(row, lane) for row in h for lane in range(2)]
    e = [0] * 222
    e[1] = tensor_row(o[0], 0)
    e[3] = 1  # Donor0, first internal coordinate.
    b = [x ^ y for x, y in zip(ot, e)]
    ell = [1]
    require(rank(e) == 2 and rank(ht + e) - len(ht) == 1,
            "rank(E)=2 while the canonical quotient rank is one")
    require(rank(ht + ell) == len(ht) + 1, "new syndrome not in canonical span")
    for i in range(111):
        for j in range(111):
            block = [(b[2 * i + lane] >> (2 * j)) & 3 for lane in range(2)]
            if o[i] >> j & 1:
                require(rank(block) == 2 and block[0] == 1,
                        "every foreign block is invertible with one common row")
            else:
                require(block == [0, 0], "no nonproper block in native control")

    # The fixture has actual native incidence, but the chosen B is an algebraic
    # control, not asserted to be realized by balanced interior coefficients.
    pivots = elimination(ht + ell)
    coeff = [expression(row, pivots) for row in e]
    require(all(value is not None for value in coeff), "native defect decomposes")
    canonical_part = [linear_combination(int(c) & ((1 << len(ht)) - 1), ht)
                      for c in coeff]
    corrected_error = [linear_combination(int(c), ht + ell) for c in coeff]
    require(corrected_error == e, "canonical-plus-syndrome native defect")

    # These whole-bank shears define an explicit invertible G. Their reverse
    # order gives its inverse, without using a floating matrix library.
    operations = [(2, 1), (4, 3), (8, 2), (5, 4)]
    operations += [(10 + 3 * i, 11 + 3 * i) for i in range(40)]
    g = [1 << i for i in range(222)]
    gi = list(g)
    for target, source in operations:
        g[target] ^= g[source]
    for target, source in reversed(operations):
        gi[target] ^= gi[source]
    require(apply_matrix(g, gi) == [1 << i for i in range(222)], "G inverse")

    # Every mask below records all 444 independent original X and Y columns.
    x = [1 << i for i in range(222)]
    y = [1 << (222 + i) for i in range(222)]
    base = apply_matrix(gi, [yy ^ kk for yy, kk in zip(y, kt)])
    corrected = [aa ^ bb for aa, bb in zip(base, apply_matrix(gi, corrected_error))]
    endpoint = [aa ^ bb for aa, bb in zip(apply_matrix(g, corrected), b)]
    require(endpoint == [xx ^ yy for xx, yy in zip(x, y)],
            "native repaired map equals X+Y on all 444 columns")
    missing = [aa ^ bb for aa, bb in zip(base, apply_matrix(gi, canonical_part))]
    omitted_syndrome = [aa ^ bb for aa, bb in zip(apply_matrix(g, missing), b)]
    missing_inverse = [aa ^ bb for aa, bb in zip(base, corrected_error)]
    bad_endpoint = [aa ^ bb for aa, bb in zip(apply_matrix(g, missing_inverse), b)]
    target = [xx ^ yy for xx, yy in zip(x, y)]
    require(omitted_syndrome != target and bad_endpoint != target,
            "both native negative controls fail")
    degrees = [row.bit_count() for row in o]
    return {"roles": 111, "foreign_edges": sum(degrees), "rank_O": 108,
            "rank_K": 9, "all_111_outside_restriction_ranks": outside,
            "degree_range": [min(degrees), max(degrees)],
            "rank_E_control": 2, "canonical_quotient_rank_control": 1,
            "control_bank_width": 2, "control_original_columns": 444,
            "control_late_G_ADDs": len(operations),
            "control_is_balanced_network_realization": False,
            "control_every_foreign_block_invertible": True,
            "negative_omitted_syndrome_output_rows": sum(a != z for a, z in zip(omitted_syndrome, target)),
            "negative_omitted_inverse_output_rows": sum(a != z for a, z in zip(bad_endpoint, target)),
            "max_source_polynomial_degree": max(5760+d*(2*5760-70) for d in degrees),
            "joint_source_polynomial_degree": 111*5760+sum(degrees)*(2*5760-70)}


POWERS: dict[int, tuple[Fraction, Fraction]] = {}


def power_interval(value: int) -> tuple[Fraction, Fraction]:
    if value not in POWERS:
        scale = 10 ** 42
        with localcontext() as context:
            context.prec = 100
            estimate = int((Decimal(value) ** (Decimal(199) / 200)) * scale)
        exact = value ** 199 * scale ** 200
        require(estimate ** 200 <= exact < (estimate + 1) ** 200,
                "integer powers authenticate each irrational enclosure")
        upper = estimate if estimate ** 200 == exact else estimate + 1
        POWERS[value] = (Fraction(estimate, scale), Fraction(upper, scale))
    return POWERS[value]


def profile_sum(*terms: tuple[Fraction | int, dict[int, Fraction | int]]) -> dict[int, Fraction]:
    result: Counter[int] = Counter()
    for factor, profile in terms:
        for gap, count in profile.items():
            result[gap] += Fraction(factor) * count
    return {gap: Fraction(count) for gap, count in result.items() if count}


def interval(profile: dict[int, Fraction | int]) -> tuple[Fraction, Fraction]:
    lower = upper = Fraction(0)
    for gap, coefficient in profile.items():
        low, high = power_interval(gap)
        lower += coefficient * (low if coefficient >= 0 else high)
        upper += coefficient * (high if coefficient >= 0 else low)
    return lower, upper


def display(bounds: tuple[Fraction, Fraction]) -> dict:
    with localcontext() as context:
        context.prec = 70
        decimals = [str(Decimal(value.numerator) / Decimal(value.denominator))
                    for value in bounds]
    return {"rational": [str(value) for value in bounds], "decimal": decimals}


def movement_controls() -> dict:
    n = {1: 1386, 2: 1253, 3: 62, 4: 47, 5: 9, 6: 104, 7: 10}
    h = {2: 1, 4: 25, 6: 1, 8: 410}
    p2 = profile_sum((36, n), (1, {1: 444}), (1, {7*j: 444 for j in range(1, 9)}))
    t2 = profile_sum((36, h), (1, {127: 222}), (1, {1+7*j: 444 for j in range(1, 10)}))
    limit = profile_sum((Fraction(1, 36), t2), (Fraction(-1, 36), p2), (1, n), (-1, h))
    q0 = {1: Fraction(4451, 8), 2: Fraction(7213, 16), 4: Fraction(24), 8: Fraction(9)}
    initial_room = interval(profile_sum((1, limit), (-1, q0)))
    eighth = power_interval(8)
    threshold = (5760 * initial_room[0] / eighth[1],
                 5760 * initial_room[1] / eighth[0])
    require(202 < threshold[0] <= threshold[1] < 203, "exact integer repair ceiling")
    scaled = {}
    for multiplicity in (1, 2, 3, 4, 30, 100):
        low, high = (value * multiplicity for value in threshold)
        floor_low = low.numerator // low.denominator
        floor_high = high.numerator // high.denominator
        require(floor_low == floor_high and low > floor_low,
                "strict scaled integer ceiling certified by rational interval")
        scaled[str(multiplicity)] = floor_low
    require(scaled["4"] == 809, "the202 ceiling is not universal after replication")
    rows = []
    for r in range(204):
        q = profile_sum((1, q0), (Fraction(r, 5760), {8: 1}))
        room = interval(profile_sum((1, limit), (-1, q)))
        slope = profile_sum((Fraction(1, 2), t2), (Fraction(-1, 2), p2),
                            (18, n), (-18, h), (-18, q))
        require(profile_sum((1, slope), (-18, profile_sum((1, limit), (-1, q)))) == {},
                "finite gap slope equals eighteen times the limiting room")

        def delta(m: int) -> tuple[Fraction, Fraction]:
            return interval(profile_sum((Fraction(m, 2), t2), (Fraction(-m, 2), p2),
                                        (18*(m-1), n), (-18*(m-1), h),
                                        (-18*(m-1), q)))

        entry = {"r": r, "limiting_room": display(room)}
        if room[0] > 0:
            offset = interval(profile_sum((-18, n), (18, h), (18, q)))
            with localcontext() as context:
                context.prec = 80
                boundary = Decimal((-offset[0]).numerator) / Decimal((-offset[0]).denominator)
                divisor = Decimal((18*room[0]).numerator) / Decimal((18*room[0]).denominator)
                candidate = max(2, (int(boundary / divisor) // 2 + 1) * 2)
            require(delta(candidate)[0] > 0, "first passing finite movement gap")
            require(candidate == 2 or delta(candidate-2)[1] < 0,
                    "immediately previous even m fails")
            entry.update({"first_even_m": candidate,
                          "previous_gap": display(delta(candidate-2)) if candidate > 2 else None,
                          "first_positive_gap": display(delta(candidate))})
        else:
            require(room[1] < 0 and delta(2)[1] < 0,
                    "negative slope and initial gap exclude every m>=2")
            entry.update({"first_even_m": None, "initial_gap": display(delta(2)),
                          "all_m_ge_2_excluded": True})
        rows.append(entry)
    expected = {0: 46, 1: 46, 70: 70, 100: 90, 200: 3854, 202: 27218, 203: None}
    require({r: rows[r]["first_even_m"] for r in expected} == expected,
            "reported exact finite thresholds")
    generic_extra = interval({8: Fraction(5690, 5760)})
    generic_room = interval(profile_sum((1, limit), (-1, q0), (Fraction(-5690, 5760), {8: 1})))
    require(generic_room[1] < 0, "maximal foreign defect cannot fit repair budget")
    return {"t": "199/200", "bank_width": 5760, "base_Q": display(interval(q0)),
            "B_infinity": display(interval(limit)), "base_room": display(initial_room),
            "real_valued_rank_ceiling": display(threshold), "maximum_integer_r": 202,
            "scaled_bank_maximum_integer_r": scaled,
            "every_r_zero_through_203": rows,
            "r_5690_minimum_extra_movement": display(generic_extra),
            "r_5690_upper_bound_remaining_room": display(generic_room),
            "power_enclosures": {str(value): display(bounds) for value, bounds in sorted(POWERS.items())}}


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    pins = json.loads(Path(__file__).with_name("SOURCE-PINS.json").read_text())
    sources = {}
    for item in pins["sources"]:
        raw = (args.repo / item["path"]).read_bytes()
        if item["uncompressed"]:
            raw = gzip.decompress(raw)
        require(sha256(raw).hexdigest() == item["sha256"], f"source hash: {item['path']}")
        sources[item["path"]] = raw
    layout_name = next(path for path in sources if path.endswith("LAYOUT.json.gz"))
    native = native_controls(json.loads(sources[layout_name]))
    small = small_controls()
    movement = movement_controls()
    m, c, r_binary = 111*5760*30, 9*5760*30, 202*30
    result = {"status": "PASS_CANONICAL_QUOTIENT_GROUND_REPAIR_CONTROLS",
              "baseline": pins["baseline"], "native": native, "small_controls": small,
              "repair_ceiling": movement["maximum_integer_r"],
              "first_even_m_at_r_202": 27218,
              "r_202_incremental_binary_invoice": {
                  "ADD_bound": m*(c+2*r_binary), "INIT": r_binary,
                  "dirty_CLEAR": r_binary, "extra_owned_peak_bound": r_binary,
                  "MOVE_gap_8": r_binary},
              "generic_maximum_defect_per_edge": 5690,
              "generic_field_size": 2**30,
              "global_balanced_coefficient_table_materialized": False,
              "low_rank_balanced_source_constructed": False,
              "full_supplier_admitted": False, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (args.out / "BUDGET.json").write_text(json.dumps(movement, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print(json.dumps({"finite_cases": small["cases"], "all_input_pairs": small["all_X_Y_pairs_checked"],
                      "repair_ceiling": 202, "first_even_m_r202": 27218,
                      "native_control_original_columns": 444,
                      "generic_max_source_polynomial_degree": native["max_source_polynomial_degree"]}))


if __name__ == "__main__":
    main()
