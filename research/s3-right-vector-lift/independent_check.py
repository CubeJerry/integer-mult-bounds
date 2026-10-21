#!/usr/bin/env python3
"""Separate binary-matrix exclusion and literal six-address bank execution.

No imports from verify.py or predecessor research code. Prepared for @CubeJerry
with substantial OpenAI Codex assistance; Apache-2.0. Not human review.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def check(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def encode(columns: tuple[int, ...]) -> int:
    return sum(v << (4*j) for j, v in enumerate(columns))


def columns(code: int) -> tuple[int, ...]:
    return tuple((code >> (4*j)) & 15 for j in range(4))


def lookup(code: int) -> list[int]:
    c = columns(code)
    return [c[0] * (v & 1) ^ c[1] * ((v >> 1) & 1)
            ^ c[2] * ((v >> 2) & 1) ^ c[3] * ((v >> 3) & 1)
            for v in range(16)]


def compose(a: int, b: int) -> int:
    table = lookup(a)
    return encode(tuple(table[v] for v in columns(b)))


def quotient_census() -> dict:
    ident = encode((1, 2, 4, 8))
    target = encode((8, 2, 4, 1))
    # All U in M_(4x2)(F2), all three nonzero y in F2^2.
    # This includes singular factors and the identity, so no invertibility
    # prefilter can silently exclude a short word.
    factors = set()
    for u0, u1, y in itertools.product(range(16), range(16), (1, 2, 3)):
        c = [1, 2, 4, 8]
        for bank in range(2):
            if y & (1 << bank):
                c[2*bank] ^= u0
                c[2*bank+1] ^= u1
        factors.add(encode(tuple(c)))
    check(len(factors) == 766, "wrong full right-vector alphabet")
    free = []
    for a, b in itertools.permutations((1, 2, 3), 2):
        free.append(encode((a & 1 | (a & 2) << 1,
                            (a & 1) << 1 | (a & 2) << 2,
                            b & 1 | (b & 2) << 1,
                            (b & 1) << 1 | (b & 2) << 2)))
    check(len(set(free)) == 6, "wrong free alphabet")
    targets = {compose(target, s) for s in free}
    two = set()
    decoded = [columns(f) for f in factors]
    for f in factors:
        action = lookup(f)
        two.update(encode(tuple(action[v] for v in c)) for c in decoded)
    check(not (targets & two), "one of the six free-normalized targets has length <= 2")
    check(ident in two and set(free) <= two, "zero-cost positive controls missing")
    # Three literal coordinate XORs swap coordinates 0 and 3.
    a, b = encode((1, 2, 4, 9)), encode((9, 2, 4, 8))
    check(a in factors and b in factors, "upper-bound factors outside alphabet")
    check(compose(a, compose(b, a)) == target, "three-factor positive control fails")
    check(compose(a, b) in two and compose(b, a) in two, "two-factor positive controls missing")
    # Recompute the column image dimension by enumerating its four elements,
    # without Gaussian elimination or the group-algebra verifier's encoding.
    dims = []
    for s in free:
        c = columns(compose(target, s) ^ ident)
        v0, v1 = c[0] | c[1] << 4, c[2] | c[3] << 4
        size = len({0, v0, v1, v0 ^ v1})
        dims.append({1: 0, 2: 1, 4: 2}[size])
    check(dims == [2]*6, "quotient column dimensions differ")
    return {"factors": len(factors), "ordered_pairs": len(factors)**2,
            "two_factor_products": len(two), "free_normalized_targets": len(targets),
            "target_hits": 0, "quotient_column_dimensions": dims}


def literal_bank_replay(cert: dict) -> dict:
    # Build the regular action directly on addresses labelled by permutations.
    # Ring elements here are sets of permutation triples, not integer masks.
    group = tuple(itertools.permutations((0, 1, 2)))
    check(cert["group_basis"] == [list(g) for g in group], "certificate basis mismatch")
    identity = (0, 1, 2)
    labels = tuple("".join(map(str, g)) for g in group)
    a = frozenset({(1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)})
    b = frozenset({(0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1)})
    d0 = frozenset({(0, 2, 1), (1, 2, 0), (2, 1, 0)})
    d1 = frozenset({(0, 2, 1), (2, 0, 1), (2, 1, 0)})
    expected_coefficients = (d0, a, b, d1)
    masks = [sum(1 << group.index(g) for g in s) for s in expected_coefficients]
    check(masks == cert["target_row_major"], "explicit target differs from certificate")
    gates = [(0, 1, a), (1, 0, b), (0, 1, a)]
    check(cert["right_vector_parameters"] == [
        {"u": [60, 0], "y": [0, 1]}, {"u": [0, 30], "y": [1, 0]},
        {"u": [60, 0], "y": [0, 1]}], "certificate paid-factor parameters differ")

    def permute(bits: tuple[int, ...], g: tuple[int, ...], right: bool = False) -> tuple[int, ...]:
        out = [0]*6
        for j, h in enumerate(group):
            product = tuple(h[g[k]] if right else g[h[k]] for k in range(3))
            out[group.index(product)] = bits[j]
        return tuple(out)

    def linear(coeff: frozenset, bits: tuple[int, ...]) -> tuple[int, ...]:
        out = [0]*6
        for g in coeff:
            translated = permute(bits, g)
            out = [x ^ y for x, y in zip(out, translated)]
        return tuple(out)

    schedules: dict[tuple, tuple] = {}

    def run(values: tuple[tuple[int, ...], ...], word: list, right: bool = False) -> tuple:
        key = (tuple(word), right)
        if key not in schedules:
            schedule = []
            for dst, src, coeff in word:
                check(dst != src, "literal XOR schedule aliases its source bank")
                for g in sorted(coeff):
                    for i, h in enumerate(group):
                        product = tuple(h[g[k]] if right else g[h[k]] for k in range(3))
                        schedule.append((6*dst + group.index(product), 6*src + i))
            schedules[key] = tuple(schedule)
        # Actual chronological in-place scalar XORs, with no bank temporary.
        bits = list(values[0] + values[1])
        for dst, src in schedules[key]:
            bits[dst] ^= bits[src]
        return (tuple(bits[:6]), tuple(bits[6:]))

    def wanted(values: tuple[tuple[int, ...], ...]) -> tuple:
        x, y = values
        return (tuple(i ^ j for i, j in zip(linear(d0, x), linear(a, y))),
                tuple(i ^ j for i, j in zip(linear(b, x), linear(d1, y))))

    def packed(values: tuple[tuple[int, ...], ...]) -> int:
        return sum(v << i for i, v in enumerate(values[0] + values[1]))

    variants = {
        "omit_first": gates[1:], "omit_middle": [gates[0], gates[2]],
        "omit_last": gates[:2], "wrong_order": [gates[1], gates[0], gates[2]],
        "wrong_coefficient": [(0, 1, a ^ {identity}), gates[1], (0, 1, a ^ {identity})],
    }
    failures = {name: {"count": 0, "first_input": None} for name in variants}
    failures["right_action_instead_of_left"] = {"count": 0, "first_input": None}
    basis_columns = []
    for value in range(4096):
        bits = tuple((value >> i) & 1 for i in range(12))
        entering = (bits[:6], bits[6:])
        expected = wanted(entering)
        observed = run(entering, gates)
        check(observed == expected, "literal group-address word fails on input " + str(value))
        check(run(observed, gates) == entering, "full involution does not return dirty input")
        if value and value & (value-1) == 0:
            basis_columns.append(packed(observed))
        for name, word in variants.items():
            if run(entering, word) != expected:
                item = failures[name]
                item["count"] += 1
                if item["first_input"] is None:
                    item["first_input"] = value
        if run(entering, gates, right=True) != expected:
            item = failures["right_action_instead_of_left"]
            item["count"] += 1
            if item["first_input"] is None:
                item["first_input"] = value
    check(basis_columns == cert["regular_target_columns"], "regular columns differ")
    check(all(item["count"] > 0 for item in failures.values()), "a negative control did not fail")
    check(len(schedules[(tuple(gates), False)]) == 72, "wrong literal scalar invoice")
    return {"all_dirty_inputs": 4096, "involution_returns": 4096,
            "regular_basis_columns": 12, "translated_bank_xors": sum(len(c) for _, _, c in gates),
            "scalar_xors": 6*sum(len(c) for _, _, c in gates),
            "source_bit_reads": 72, "destination_bit_reads": 72, "destination_bit_writes": 72,
            "auxiliary_banks": 0, "controls": failures, "address_labels": labels}


def main() -> None:
    cert = json.loads((HERE / "CERTIFICATE.json").read_text())
    result = {"quotient_census": quotient_census(), "literal_banks": literal_bank_replay(cert)}
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS_S3_RIGHT_VECTOR_INDEPENDENT factors=766 pairs=586756 target_hits=0 "
          "dirty_inputs=4096 scalar_xors=72 no_new_kappa receipt_sha256=" + hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
