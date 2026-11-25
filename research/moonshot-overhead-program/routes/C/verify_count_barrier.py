#!/usr/bin/env python3
"""Exact finite checks for COUNT-PREDICTION-BARRIER.md; standard library only.

These checks complement the proof. They do not prove an asymptotic bound or
establish a tape algorithm. Output JSON is deterministic except Python version.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction
from pathlib import Path


def binomial_weights(n: int) -> list[int]:
    weights = [1]
    for k in range(n):
        weights.append(weights[-1] * (n - k) // (k + 1))
    return weights


def heavy_sum(weights: list[int], count: int) -> int:
    return sum(sorted(weights, reverse=True)[:count])


def variation_failure(m: int, degree: int) -> Fraction:
    return Fraction((1 << (m - 1)) - heavy_sum(binomial_weights(m - 1), degree), 1 << m)


def root_failure(m: int, degree: int) -> Fraction:
    return min(Fraction(1, 2), Fraction((1 << m) - heavy_sum(binomial_weights(m), 2 * degree), 1 << m))


def fraction_json(value: Fraction) -> dict[str, int | float]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": float(value)}


def verify_prefix_identity() -> int:
    checks = 0
    for m in range(1, 257):
        previous = binomial_weights(m - 1)
        cumulative = 0
        for k, weight in enumerate(binomial_weights(m)):
            cumulative += (-1 if k % 2 else 1) * weight
            expected = 0 if k == m else (-1 if k % 2 else 1) * previous[k]
            assert cumulative == expected, (m, k, cumulative, expected)
            checks += 1
    return checks


def verify_threshold_optima() -> tuple[int, list[dict[str, int]]]:
    """Exhaust every sign sequence, not an implementation of a greedy rule."""
    patterns = 0
    cases = []
    for m in range(1, 13):
        weights = binomial_weights(m)
        by_changes = [-1] * (m + 1)
        for mask in range(1 << (m + 1)):
            agreement = sum(weight for k, weight in enumerate(weights) if ((mask >> k) & 1) == (k & 1))
            changes = sum(((mask >> k) ^ (mask >> (k + 1))) & 1 for k in range(m))
            by_changes[changes] = max(by_changes[changes], agreement)
            patterns += 1
        cumulative_best = -1
        for degree in range(m + 1):
            cumulative_best = max(cumulative_best, by_changes[degree])
            expected = (1 << (m - 1)) + heavy_sum(binomial_weights(m - 1), degree)
            assert cumulative_best == expected, (m, degree, cumulative_best, expected)
        cases.append({"m": m, "degree_caps_checked": m + 1})
    return patterns, cases


def interpolated_values(nodes: tuple[int, ...], m: int) -> list[Fraction]:
    """Lagrange interpolation evaluated exactly at every integer count."""
    values = [Fraction(0) for _ in range(m + 1)]
    for i, node in enumerate(nodes):
        denominator = math.prod(node - other for j, other in enumerate(nodes) if j != i)
        sign = -1 if node % 2 else 1
        for k in range(m + 1):
            numerator = math.prod(k - other for j, other in enumerate(nodes) if j != i)
            values[k] += Fraction(sign * numerator, denominator)
    return values


def verify_exact_interpolants() -> tuple[int, list[dict[str, object]]]:
    """Enumerate all possible optimal equality-agreement polynomials at small m.

    An optimum can be taken to agree at at least d+1 counts: extend any smaller
    agreement set to d+1 nodes and interpolate, preserving all earlier matches.
    Thus enumerating d+1-node interpolants also covers complex coefficients.
    """
    checked = 0
    cases = []
    for m in range(1, 10):
        weights = binomial_weights(m)
        for degree in range(min(4, m) + 1):
            best_weight = -1
            best_nodes: tuple[int, ...] = ()
            for nodes in itertools.combinations(range(m + 1), degree + 1):
                values = interpolated_values(nodes, m)
                agreement = sum(weights[k] for k, value in enumerate(values) if value == (-1 if k % 2 else 1))
                if agreement > best_weight:
                    best_weight, best_nodes = agreement, nodes
                checked += 1
            failure = 1 - Fraction(best_weight, 1 << m)
            assert failure >= variation_failure(m, degree), (m, degree, "variation")
            assert failure >= root_failure(m, degree), (m, degree, "root")
            if degree == 0:
                assert failure == Fraction(1, 2)
            if degree == m:
                assert failure == 0
            cases.append({"m": m, "degree": degree, "minimum_failure": fraction_json(failure), "witness_nodes": best_nodes})
    return checked, cases


def verify_shift_averaging() -> int:
    """All shifts have the same count histogram, also under unequal row weights."""
    checks = 0
    for m in range(1, 9):
        expected = binomial_weights(m)
        weighted = [0] * (m + 1)
        total_weight = 0
        for shift in range(1 << m):
            counts = [0] * (m + 1)
            for frequency in range(1 << m):
                counts[(frequency ^ shift).bit_count()] += 1
            assert counts == expected
            row_weight = shift + 1
            for k, count in enumerate(counts):
                weighted[k] += row_weight * count
            total_weight += row_weight
            checks += 1
        assert weighted == [total_weight * count for count in expected]
    return checks


def finite_characteristic_controls() -> dict[str, object]:
    assert all(pow(-1, k, 2) == 1 for k in range(100))
    m = 36
    agreement = sum(math.comb(m, k) for k in range(m + 1) if (1 + k * k) % 3 == pow(-1, k, 3))
    actual = Fraction(agreement, 1 << m)
    assert actual == Fraction(17309009347, 34359738368)
    assert actual > 1 - root_failure(m, 2)
    assert math.comb(0, 3) % 3 != math.comb(3, 3) % 3
    return {
        "characteristic_two_constant_predictor": "exact parity multiplier is constant",
        "characteristic_three_root_bound_counterexample": {
            "m": m,
            "degree": 2,
            "polynomial": "1+c^2 over F_3",
            "agreement": fraction_json(actual),
            "invalid_characteristic_zero_root_bound": fraction_json(1 - root_failure(m, 2)),
            "scope": "counterexample to C4 extension, not a claim refuting C1 over every odd field",
        },
        "divided_power_not_count_residue_function": {"binom_0_3_mod_3": 0, "binom_3_3_mod_3": 1},
    }


def exact_invoice_diagnostics() -> list[dict[str, object]]:
    """Optimize d + m*(C1 lower bound) exactly with a common denominator.

    This optimizes a lower-bound relaxation, not actual equality predictors.
    Decimal ratios are diagnostic output, not proof of limiting constants.
    """
    results = []
    for m in (16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        weights = sorted(binomial_weights(m - 1), reverse=True)
        denominator = 1 << m
        remaining = 1 << (m - 1)
        best = (m * remaining, 0)
        for degree in range(1, m + 1):
            remaining -= weights[degree - 1]
            score = degree * denominator + m * remaining
            best = min(best, (score, degree))
        value = Fraction(best[0], denominator)
        results.append({
            "m": m,
            "minimizing_degree": best[1],
            "invoice_decimal": float(value),
            "ratio_to_sqrt_m_ln_m": float(value) / math.sqrt(m * math.log(m)),
            "optimization_arithmetic": "exact integers; displayed value and ratio rounded",
        })
    return results


def main() -> None:
    prefix_checks = verify_prefix_identity()
    threshold_patterns, threshold_cases = verify_threshold_optima()
    interpolants, exact_cases = verify_exact_interpolants()
    shifts = verify_shift_averaging()
    report = {
        "status": "pass",
        "scope": "finite exact checks of scoped count-prediction lemmas; no formal kernel or tape-time theorem",
        "python": platform.python_version(),
        "prefix_identity_checks": prefix_checks,
        "threshold_patterns_exhausted": threshold_patterns,
        "threshold_cases": threshold_cases,
        "exact_interpolants_checked": interpolants,
        "exact_prediction_cases": exact_cases,
        "shift_histograms_checked": shifts,
        "negative_controls": finite_characteristic_controls(),
        "invoice_diagnostics": exact_invoice_diagnostics(),
    }
    path = Path(__file__).with_name("verification.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in (
        "status", "scope", "python", "prefix_identity_checks", "threshold_patterns_exhausted",
        "exact_interpolants_checked", "shift_histograms_checked", "invoice_diagnostics"
    )}, indent=2))


if __name__ == "__main__":
    main()
