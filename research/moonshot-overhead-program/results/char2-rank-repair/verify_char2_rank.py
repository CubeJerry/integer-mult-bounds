#!/usr/bin/env python3
"""Exact finite controls for characteristic-two rank-error truncation.
No physical routing or multiplier timing is tested.
"""
from __future__ import annotations
import json
from math import comb
from pathlib import Path
from random import Random


def terms(poly):
    while poly:
        bit = poly & -poly
        yield bit.bit_length() - 1
        poly ^= bit


def mul(a, b):
    out = 0
    for s in terms(a):
        for t in terms(b):
            if not s & t:
                out ^= 1 << (s | t)
    return out


def elementary(m, d):
    return sum(1 << s for s in range(1 << m) if s.bit_count() == d)


def multiplication_rank(m, poly):
    pivots = {}
    for s in range(1 << m):
        v = 0
        for t in terms(poly):
            if not s & t:
                v ^= 1 << (s | t)
        while v:
            pivot = v.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = v
                break
            v ^= pivots[pivot]
    return len(pivots)


def elementary_in_values(values, d):
    coefficients = [1] + [0] * d
    for value in values:
        for degree in range(d, 0, -1):
            coefficients[degree] ^= mul(coefficients[degree - 1], value)
    return coefficients[d]


def main():
    counts = {"elementary_products": 0, "triangular_monomial_basis": 0,
              "automorphism_coefficient_identities": 0, "unit_factor_identities": 0,
              "rank_equalities": 0, "general_degree_cut_cases": 0}
    negative = {"omitted_prefix_failures": 0, "predictor_is_low_rank_failures": 0}
    samples = []
    for m in range(1, 9):
        es = [elementary(m, d) for d in range(m + 1)]
        for a in range(m + 1):
            for b in range(m + 1):
                expected = es[a + b] if a + b <= m and comb(a + b, a) % 2 else 0
                assert mul(es[a], es[b]) == expected
                counts["elementary_products"] += 1
        ys = []
        prefix = 1
        for i in range(m):
            x = 1 << (1 << i)
            ys.append(mul(x, prefix))
            prefix = mul(prefix, 1 ^ x)
        # The image of each monomial has its original degree component;
        # every additional monomial has strictly larger degree.
        for s in range(1 << m):
            image = 1
            for i in range(m):
                if s >> i & 1:
                    image = mul(image, ys[i])
            assert image >> s & 1
            assert all(t == s or t.bit_count() > s.bit_count() for t in terms(image))
            counts["triangular_monomial_basis"] += 1
        d = 1
        while d <= m:
            image = elementary_in_values(ys, d)
            if d == 1:
                expected = sum(es[1:])
            else:
                a = d // 2
                expected = sum(es[h] for h in range(d, m + 1) if comb(h - a - 1, a - 1) % 2)
            assert image == expected
            counts["automorphism_coefficient_identities"] += 1
            predictor = sum(es[:d])
            error = sum(es[d:])
            vd = sum(es[h] for h in range(d, m + 1, d))
            assert mul(predictor, vd) == error
            assert mul(predictor, predictor) == 1
            if d > 1:
                assert mul(1 ^ es[d // 2], vd) == image
            counts["unit_factor_identities"] += 1
            if image != es[d]:
                negative["omitted_prefix_failures"] += 1
            d *= 2
    for m in range(1, 13):
        for d in (1, 2, 4, 8):
            if d > m:
                continue
            error = sum(1 << s for s in range(1 << m) if s.bit_count() >= d)
            r_error = multiplication_rank(m, error)
            r_homogeneous = multiplication_rank(m, elementary(m, d))
            assert r_error == r_homogeneous
            bound = 2 * sum(comb(m, k) for k in range((m - d) // 2 + 1))
            assert r_error <= bound
            counts["rank_equalities"] += 1
            if bound < 1 << m:
                negative["predictor_is_low_rank_failures"] += 1
            if m in (4, 8, 12):
                samples.append({"m": m, "d": d, "error_rank": r_error,
                                "dimension": 1 << m, "degree_cut_bound": bound})
    rng = Random(20261125)
    for m in range(2, 9):
        for d in range(1, m + 1):
            choices = [s for s in range(1 << m) if s.bit_count() >= d]
            for _ in range(5):
                poly = sum(1 << s for s in choices if rng.randrange(2))
                rank = multiplication_rank(m, poly)
                t = (m - d) // 2
                lo = sum(comb(m, k) for k in range(t + 1))
                hi = sum(comb(m, k) for k in range(t + d + 1, m + 1))
                assert rank <= lo + hi <= 2 * lo
                # Check the claimed projection decomposition on every basis vector.
                for s in range(1 << m):
                    out = mul(poly, 1 << s)
                    if s.bit_count() > t:
                        assert all(v.bit_count() >= t + d + 1 for v in terms(out))
                counts["general_degree_cut_cases"] += 1
    assert all(negative.values())
    result = {"status": "PASS", "field": "F_2", "exact_arithmetic": True,
              "scope": "finite rank and algebra checks; no physical correction implementation",
              "counts": counts, "negative_controls": negative, "samples": samples}
    Path(__file__).with_name("verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
