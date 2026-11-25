#!/usr/bin/env python3
"""Finite exact checks of the sharper parameter majorants and sparse rounding.

No giant template, numerical Fourier layer, or tape machine is constructed.
Rejection of a deliberately weak majorant is not an impossibility theorem.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb


def ceil_log2(n: int) -> int:
    assert n >= 1
    return (n - 1).bit_length()


def majorants(j_capital: int, u: int) -> tuple[Fraction, Fraction]:
    """Conservative rational upper bounds using u < log2(m) < u+1."""
    x_upper = u + 1
    log3x = ceil_log2(3 * x_upper)
    half_log = Fraction(ceil_log2(u + 3), 2)
    interchange = (
        Fraction(3 * x_upper, 100 * j_capital)
        + 4 * (200 * j_capital) ** 2 * log3x
        + half_log + 13
    )
    fourier = (
        Fraction(2 * x_upper, 100 * j_capital)
        + 202 * j_capital * log3x + half_log
        + ceil_log2(606 * j_capital) + 9
    )
    return interchange, fourier


def main() -> None:
    parameter_cases = 0
    negative_controls = 0
    selected_j = list(range(3, 4097)) + [10**k + 1 for k in range(4, 31)]
    for j_capital in selected_j:
        integer_threshold = (1 << 30) * j_capital**3 * ceil_log2(j_capital)
        u = 1 << ceil_log2(integer_threshold)
        interchange, fourier = majorants(j_capital, u)
        target_excess = Fraction(u, 2 * j_capital)
        assert interchange + 1 <= target_excess
        assert fourier + 2 <= target_excess
        address_excess = 4 * (200 * j_capital)**2 * (
            ceil_log2(400 * j_capital) + 2
        )
        assert address_excess <= u
        assert 202 * j_capital <= u
        assert u >= 16  # The proved induction gives 2^u >= 32(u+2).
        parameter_cases += 1

        # Deliberately omit the absolute threshold constant. The invoice
        # must reject this unjustified shortcut, without claiming that no
        # more careful implementation could ever accept those parameters.
        too_small = j_capital**3 * ceil_log2(j_capital)
        bad_interchange, _ = majorants(j_capital, too_small)
        assert bad_interchange + 1 > Fraction(too_small, 2 * j_capital)
        negative_controls += 1

    label_cases = 0
    for prime in (3, 5, 7, 11):
        h = 2 * prime - 1
        cr = (1 + h ** (prime - 1)) ** (prime + 1)
        for u in range(prime, 301, 7):
            m = (1 << u) + 1
            t = max(1, (ceil_log2(cr * m) + prime**2 - 1) // prime**2)
            q = 1 << t
            assert q ** (prime**2) >= cr * m
            if t > 1:
                assert (q // 2) ** (prime**2) < cr * m
            dimension = 2 + h * q**h
            incidence = comb(h, prime)**(prime + 1) * (q - 1)**prime * t**(prime * (prime - 1))
            # A stronger finite sufficient test: upper-round the LHS log
            # while lower-rounding every RHS log and replacing x by u.
            lhs_upper = ceil_log2(dimension * (1 + incidence))
            rhs_lower = Fraction(3 * u, prime) + 4 * prime**2 * ((3 * u).bit_length() - 1)
            assert lhs_upper <= rhs_lower
            label_cases += 1

    sparse_cases = 0
    for profile_constant in (1, 2, 4, 16, 128):
        for log_z in range(16, 81):
            z = 1 << log_z
            h = 0
            while 2 * profile_constant * (1 << (3 * (h + 1))) * log_z <= z:
                h += 1
            if h < 2:
                continue
            j_capital = 1 << h
            assert 2 * profile_constant * j_capital**3 * h <= z
            assert 2 * profile_constant * (2 * j_capital)**3 * log_z > z
            assert j_capital >= 4
            sparse_cases += 1

    print(json.dumps({
        "status": "passed",
        "parameter_and_guard_cases": parameter_cases,
        "negative_controls_missing_threshold_constant": negative_controls,
        "exact_label_majorant_cases": label_cases,
        "sparse_profile_rounding_cases": sparse_cases,
        "scope": "Finite exact inequalities; no full template or tape-machine implementation.",
    }, indent=2))


if __name__ == "__main__":
    main()
