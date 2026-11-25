#!/usr/bin/env python3
"""Exact finite tests of the q=2 parity-corrected repair invoice."""
from fractions import Fraction
from math import comb, pi, sqrt
from pathlib import Path
import hashlib
import json


def tail(n, t):
    if t >= n:
        return Fraction(0)
    cutoff = (n - t - 1) // 2
    return Fraction(sum(comb(n, j) for j in range(cutoff + 1)), 2**n)


def main():
    counts = {"parity_corrected_tails": 0, "finite_local_potentials": 0,
              "finite_six_fifths_bounds": 0, "relaxed_trees": 0,
              "degree_one_equalities": 0}
    for m in range(1, 301):
        v = m // 2
        atom = Fraction(comb(2*v, v), 4**v)
        potential = 1 / atom
        assert potential <= m
        for t in range(m):
            n = m if (m-t) % 2 else m-1
            assert 0 <= t < n <= m and (n-t) % 2
            d = tail(n, t)
            assert d >= Fraction(1, 2) - t*atom/2
            assert t + 2*potential*d >= potential
            counts["parity_corrected_tails"] += 1
            counts["finite_local_potentials"] += 1
        if m >= 25:
            assert potential**2 >= Fraction(36, 25)*m
            counts["finite_six_fifths_bounds"] += 1
        if m >= 2:
            n = m if m % 2 == 0 else m-1
            assert tail(n, 1) == (1-atom)/2
            counts["degree_one_equalities"] += 1
            mass = 1-atom
            for depth in (0, 1, 2, 4, 8):
                direct = sum((mass**j for j in range(depth)), Fraction(0)) + m*mass**depth
                closed = potential + (m-potential)*mass**depth
                assert direct == closed and direct >= potential
                counts["relaxed_trees"] += 1
    # The original even-m t=0 tail admits a false contracting zero-stage tree.
    m = 8
    atom = Fraction(comb(m, m//2), 2**m)
    naive_mass = 2*tail(m, 0)
    true_tail = tail(m-1, 0)
    assert naive_mass == 1-atom < 1 and true_tail == Fraction(1, 2)
    naive_cost = m*naive_mass**20
    assert naive_cost < 1/atom
    diagnostics = []
    for diagnostic_m in (25, 100, 1000, 10000):
        v = diagnostic_m//2
        scaled = float(Fraction(4**v, comb(2*v, v))) / sqrt(diagnostic_m)
        diagnostics.append({"m": diagnostic_m, "exact_potential_over_sqrt_m": scaled,
                            "limit": sqrt(pi/2)})
    result = {"status": "passed", "arithmetic": "exact rational and integer",
              "counts": counts, "negative_control": {
                  "omission": "one-coordinate parity restriction", "m": m,
                  "naive_two_child_mass": str(naive_mass),
                  "correct_zero_stage_two_child_mass": str(2*true_tail),
                  "depth_20_naive_cost_less_than_true_floor": True},
              "asymptotic_diagnostics": diagnostics,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Finite invoice inequalities and relaxed trees; no physical algorithm or general runtime lower bound"}
    Path("two-converter-floor-verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
