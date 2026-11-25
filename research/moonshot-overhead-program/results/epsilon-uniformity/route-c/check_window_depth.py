#!/usr/bin/env python3
"""Exact finite controls for the exact-window depth/resource note.

The asymptotic tradeoff is proved analytically in the Markdown, not here.
"""

from fractions import Fraction
from itertools import product
from math import comb, isqrt, log, sqrt
import json


def generalized_binomial(n, h):
    result = Fraction(1)
    for j in range(h):
        result *= Fraction(n - j, j + 1)
    assert result.denominator == 1
    return result.numerator


def interpolation(count, u, width):
    return (-1) ** u * sum(
        (-2) ** h * generalized_binomial(count - u, h)
        for h in range(width + 1)
    )


def binomial_weights(m):
    weights = [1]
    for c in range(m):
        weights.append(weights[-1] * (m - c) // (c + 1))
    assert sum(weights) == 1 << m
    return weights


def main():
    band_cases = 0
    characteristic_cases = 0
    for m in range(1, 21):
        for u in range(m + 1):
            for v in range(u, m + 1):
                width = v - u
                for count in range(u, v + 1):
                    value = interpolation(count, u, width)
                    assert value == (-1) ** count
                    band_cases += 1
                top = sum(
                    (-1) ** (width - s) * comb(width, s) * (-1) ** (u + s)
                    for s in range(width + 1)
                )
                assert top == (-1) ** u * (-2) ** width
                for p in (3, 5, 7):
                    assert top % p != 0
                    characteristic_cases += 1

    # Degree-lowering characteristic-four control: "characteristic != 2"
    # would be an invalid hypothesis; invertibility of 2 is the right one.
    mod_four_cases = 0
    for bits in product((0, 1), repeat=6):
        assert (1 - 2 * sum(bits)) % 4 == (-1) ** sum(bits) % 4
        mod_four_cases += 1
    assert (-2) % 2 == 0  # In characteristic two parity is constant.

    rows = []
    center_checks = 0
    for m in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        weights = binomial_weights(m)
        prefix = [0]
        for weight in weights:
            prefix.append(prefix[-1] + weight)
        denominator = 1 << m
        best = None
        for width in range(m + 1):
            u = (m - width) // 2
            mass = prefix[u + width + 1] - prefix[u]
            if m <= 64:
                for other in range(m - width + 1):
                    assert mass >= prefix[other + width + 1] - prefix[other]
                    center_checks += 1
            numerator = width * denominator + m * (denominator - mass)
            if best is None or numerator < best[0]:
                best = (numerator, width, u)

        # Exact source window and advertised tail budget.
        r = (2 * m - 1).bit_length()
        radicand = 2 * m * r
        bound = isqrt(radicand)
        if bound * bound != radicand:
            bound += 1
        u_src = max(0, m // 2 - bound)
        v_src = min(m, (m + 1) // 2 + bound)
        tail = denominator - (prefix[v_src + 1] - prefix[u_src])
        assert 2 * m ** 3 * tail <= denominator
        if m >= 32 * r:
            assert u_src > 0 and v_src < m
            assert (v_src - u_src) ** 2 >= 8 * m * r
        value = best[0] / denominator
        rows.append({
            "m": m,
            "optimal_window_width_for_D_plus_m_delta": best[1],
            "source_clamped_window_width": v_src - u_src,
            "source_tail_budget_exactly_checked": True,
            "illustrative_optimum": value,
            "illustrative_optimum_over_sqrt_m_ln_m": value / sqrt(m * log(m)),
        })

    print(json.dumps({
        "scope": "Exact finite interpolation, degree-witness and source-tail controls. Floating values only illustrate the window resource functional; they are not asymptotic evidence or runtime measurements.",
        "band_value_cases": band_cases,
        "odd_characteristic_top_coefficient_cases": characteristic_cases,
        "mod_four_degree_one_negative_controls": mod_four_cases,
        "centered_window_maximum_comparisons": center_checks,
        "resource_functional_examples": rows,
    }, indent=2))


if __name__ == "__main__":
    main()
