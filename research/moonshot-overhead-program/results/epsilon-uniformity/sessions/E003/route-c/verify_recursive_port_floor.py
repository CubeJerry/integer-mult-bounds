#!/usr/bin/env python3
"""Exact arithmetic checks of R2--R4; Gaussian decimals are diagnostics."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def tails(m: int) -> list[int]:
    result, running = [], 0
    for i in range(m + 1):
        running += math.comb(m, i)
        result.append(running)
    return result


def delta_numerator(m: int, t: int, cumulative: list[int]) -> int:
    return 0 if t >= m else cumulative[(m - t - 1) // 2]


def main() -> None:
    mode_checks = tail_checks = 0
    for m in range(1, 257):
        denominator = 1 << m
        mode = math.comb(m, m // 2)
        assert 3 * m * mode * mode <= 2 * denominator * denominator
        mode_checks += 1
        cumulative = tails(m)
        for t in range(m + 1):
            numerator = delta_numerator(m, t, cumulative)
            missing = denominator - 2 * numerator
            if missing > 0:
                assert 6 * m * missing * missing <= 4 * denominator * denominator * (t + 1)**2
            tail_checks += 1
    subsolution_cases = []
    for m in (4096, 4097, 4225, 8192, 16384):
        denominator = 1 << m
        cumulative = tails(m)
        count = 0
        # Above this cutoff the t term alone proves R4.
        for t in range(math.isqrt(36 * m // 25) + 2):
            numerator = delta_numerator(m, t, cumulative)
            remaining = denominator - 4 * numerator
            if remaining > 0:
                assert 25 * t * t * denominator * denominator >= 36 * m * remaining * remaining
            count += 1
        subsolution_cases.append({"m": m, "exact_integer_subsolution_checks": count})
    # The exact constant used in the finite proof, not a decimal estimate.
    assert 389**2 < 6 * 160**2
    finite_potentials = []
    for m in (16, 32, 64, 128, 256):
        denominator = 1 << m
        cumulative = tails(m)
        candidates = []
        for t in range(m + 1):
            fraction = Fraction(delta_numerator(m, t, cumulative), denominator)
            if 4 * fraction < 1:
                candidates.append((Fraction(t, 1) / (1 - 4 * fraction), t))
        potential, degree = min(candidates)
        current = Fraction(m, 1)
        for _ in range(8):
            current = min(Fraction(m, 1), min(Fraction(t, 1) + 4 * Fraction(delta_numerator(m, t, cumulative), denominator) * current for t in range(m)))
            assert current >= potential
        finite_potentials.append({"m": m, "optimal_rank_bound_potential_degree": degree, "potential_over_sqrt_m_diagnostic": float(potential) / math.sqrt(m), "eight_level_relaxed_invoice_over_sqrt_m_diagnostic": float(current) / math.sqrt(m)})
    gaussian = []
    for q in (3, 4, 8):
        lo, hi = 0.0, 10.0
        for _ in range(80):
            c = (lo + hi) / 2
            density = math.exp(-c * c / 2) / math.sqrt(2 * math.pi)
            tail = math.erfc(c / math.sqrt(2)) / 2
            if q * (tail + c * density) > 1:
                lo = c
            else:
                hi = c
        c = (lo + hi) / 2
        density = math.exp(-c * c / 2) / math.sqrt(2 * math.pi)
        gaussian.append({"q": q, "c_q_diagnostic": c, "Lambda_q_diagnostic": 1 / (q * density)})
    receipt = {
        "scope": "Finite exact integer inequalities and rational relaxed-invoice dynamics; no tape-runtime lower bound or asymptotic proof by sampling.",
        "central_mass_inequalities": mode_checks,
        "binomial_tail_inequalities": tail_checks,
        "finite_subsolution_checks": subsolution_cases,
        "exact_cutoff_constant": "389^2 < 6*160^2",
        "relaxed_finite_potential_diagnostics": finite_potentials,
        "gaussian_constants_diagnostics_only": gaussian,
    }
    Path(__file__).with_name("recursive-port-floor-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
