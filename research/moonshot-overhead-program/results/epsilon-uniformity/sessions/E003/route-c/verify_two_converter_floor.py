#!/usr/bin/env python3
"""Exact finite checks of Z1--Z5; not an actual running-time lower bound."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path
import random

from verify_matrix_prediction_barrier import Field, rank


def tails(m: int) -> list[Fraction]:
    cumulative = []
    total = 0
    for j in range(m + 1):
        total += comb(m, j)
        cumulative.append(total)
    answer = []
    for t in range(m + 1):
        cutoff = (m - t - 1) // 2
        answer.append(Fraction(cumulative[cutoff] if cutoff >= 0 else 0, 1 << m))
    return answer


def potential(m: int) -> Fraction:
    mode = Fraction(comb(m, m // 2), 1 << m)
    if m % 2:
        return 1 / (2 * mode)
    previous = Fraction(comb(m, m // 2 - 1), 1 << m)
    return 2 / (mode + 2 * previous)


def main() -> None:
    counts = {}

    def record(key, amount=1):
        counts[key] = counts.get(key, 0) + amount

    for m in range(1, 513):
        delta = tails(m)
        value = potential(m)
        ratios = [Fraction(t, 1) / (1 - 2 * delta[t]) for t in range(1, m + 1)]
        assert value == min(ratios)
        assert ratios[0 if m % 2 else 1] == value
        assert value <= m
        assert value * value >= Fraction(3 * m, 8)
        if not m % 2:
            assert value * value >= Fraction(2 * m, 3)
            assert delta[0] < Fraction(1, 2)
            # Leaving the degree-zero entry unpatched would contract a
            # positive potential at zero cost, contradicting the desired
            # scalar subsolution already after one relaxed step.
            assert 2 * delta[0] * value < value
            record("rejected_unpatched_even_degree_zero")
        patched = delta[:]
        patched[0] = Fraction(1, 2)
        for t, error in enumerate(patched):
            assert t + 2 * value * error >= value
            record("exact_subsolution_inequalities")
        if m % 2 and m >= 3:
            # A unit coefficient in front of sqrt(m) is not a subsolution
            # of this relaxed rank recurrence. The active degree is one.
            assert m * (1 - 2 * delta[1]) ** 2 > 1
            record("rejected_naive_q_two_continuum_potential")
        record("exact_minimum_potentials")

    for m in range(1, 65):
        delta = tails(m)
        delta[0] = Fraction(1, 2)
        value = potential(m)
        bound = Fraction(m)
        fixed_choice = bound
        chosen = 1 if m % 2 else 2
        for depth in range(1, 13):
            next_bound = min(t + 2 * error * bound for t, error in enumerate(delta))
            fixed_choice = chosen + 2 * delta[chosen] * fixed_choice
            assert value <= next_bound <= bound
            assert next_bound <= fixed_choice
            assert fixed_choice == value + (m - value) * (2 * delta[chosen]) ** depth
            bound = next_bound
            record("exact_finite_depth_relaxations")

    rng = random.Random(302605)
    for order in (3, 4, 5, 7):
        field = Field(order)
        for m in range(1, 8):
            for width in range(1, 5):
                for case in range(8):
                    matrix = [[rng.randrange(order) for _ in range(width)] for _ in range(width)]
                    pairs = [rng.sample(range(1, order), 2) for _ in range(m)]
                    total_rank = 0
                    for point in range(0, 1 << m, 2):
                        values = [field.prod(pair[((point + bit) >> i) & 1]
                                             for i, pair in enumerate(pairs)) for bit in (0, 1)]
                        assert values[0] != values[1]
                        paired_ranks = []
                        for value in values:
                            defect = [[field.sub(value if i == j else 0, matrix[i][j])
                                       for j in range(width)] for i in range(width)]
                            paired_ranks.append(rank(defect, field))
                        assert sum(paired_ranks) >= width
                        total_rank += sum(paired_ranks)
                        record("matrix_rank_pairs")
                    assert total_rank >= (1 << (m - 1)) * width
                    record("constant_matrix_targets")

    root = Path(__file__).resolve().parent
    files = [Path(__file__).name, "TWO-CONVERTER-PORT-FLOOR.md", "verify_matrix_prediction_barrier.py"]
    result = {
        "status": "passed exact finite checks",
        "counts": counts,
        "small_potentials": {str(m): str(potential(m)) for m in range(1, 13)},
        "sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in files},
        "scope": [
            "The proof is the finite-tree subsolution and central-mass argument in the note",
            "No finite check proves asymptotics or an actual tape lower bound",
            "Relaxed potential attainment does not construct a predictor attaining the rank bound",
        ],
    }
    (root / "two-converter-floor-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
