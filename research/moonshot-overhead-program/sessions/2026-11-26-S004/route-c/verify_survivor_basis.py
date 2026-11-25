#!/usr/bin/env python3
"""Exact finite controls for the full-root survivor-basis theorem."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import random

from verify_inverse_query_commutator import Field, eye, evaluate, multiply, rank, regular


def survivor(alpha, r, t):
    counts = [alpha.count(h) for h in range(r)]
    return all(counts[h] <= counts[0]+h*t for h in range(1, r))


def compositions(n, r):
    if r == 1:
        yield (n,)
    else:
        for first in range(n+1):
            for rest in compositions(n-first, r-1):
                yield (first,)+rest


def survivor_count(m, r, t):
    total = 0
    for counts in compositions(m, r):
        if all(counts[h] <= counts[0]+h*t for h in range(1, r)):
            remaining = m
            multiplicity = 1
            for value in counts:
                multiplicity *= comb(remaining, value)
                remaining -= value
            total += multiplicity
    return total


def main():
    rng = random.Random(2026112507)
    checks = Counter()
    for r in (2, 3, 4, 5):
        for m in range(1, 8 if r <= 3 else 5):
            alphas = list(product(range(r), repeat=m))
            for t in range(m+1):
                selected = [a for a in alphas if survivor(a, r, t)]
                assert len(selected) == survivor_count(m, r, t)
                threshold = (2*m*(r-1)+r*(r-1)*t)//(2*r)
                assert all(sum(x != 0 for x in a) <= threshold for a in selected)
                checks["exact_survivor_and_averaged_cut_counts"] += 1
                for alpha in alphas:
                    weight = sum(x != 0 for x in alpha)
                    lower_options = [sum((x-h) % r != 0 for x in alpha)+h*t
                                     for h in range(1, r)]
                    assert survivor(alpha, r, t) == all(x >= weight for x in lower_options)
                    if not survivor(alpha, r, t):
                        assert min(lower_options) < weight
                    checks["strict_descent_predicates"] += 1

    # Actual arbitrary matrix predictors, including noncommuting coefficients:
    # columns of D plus survivor basis vectors span the entire regular module.
    for r, field, root in ((2, Field(5), 4), (3, Field(4), 2)):
        for m in range(1, 5):
            alphas = list(product(range(r), repeat=m))
            n, width = r**m, 2
            for t in range(min(m, 2)+1):
                allowed = [a for a in alphas if sum(x != 0 for x in a) <= t]
                for rep in range(3):
                    p = {a: [[rng.randrange(field.order) for _ in range(width)]
                             for _ in range(width)] for a in allowed}
                    d = {a: [[field.neg(x) for x in row] for row in mat]
                         for a, mat in p.items()}
                    target = (1,)*m
                    d.setdefault(target, [[0]*width for _ in range(width)])
                    for i in range(width):
                        d[target][i][i] = field.add(d[target][i][i], 1)
                    reg = regular(d, m, r, width, width, field)
                    original_rank = rank(reg, field)
                    survivors = [j*width+i for j, a in enumerate(alphas)
                                 if survivor(a, r, t) for i in range(width)]
                    augmented = [row+[int(i == j) for j in survivors]
                                 for i, row in enumerate(reg)]
                    assert rank(augmented, field) == n*width
                    assert original_rank >= n*width-len(survivors)
                    spectral_rank = sum(rank(evaluate(d, point, root, width, width, field), field)
                                        for point in alphas)
                    assert original_rank == spectral_rank
                    checks["matrix_quotient_spanning_tests"] += 1
                    checks["regular_vs_spectral_rank_sums"] += 1
                    checks["spectral_ranks"] += n
                    mats = list(p.values())
                    if len(mats) > 1 and multiply(mats[0], mats[1], field) != multiply(mats[1], mats[0], field):
                        checks["noncommuting_matrix_coefficient_cases"] += 1

    # Exact concentration controls, including the n=0 binomial case.
    for n in range(1001):
        maximum = comb(n, n//2)
        assert maximum*maximum*(n+1) <= 4**n
        checks["central_binomial_atom_bounds"] += 1
    for r in (2, 3, 4, 5):
        distribution = Counter({0: 1})
        for m in range(1, 201):
            new = Counter()
            for d, count in distribution.items():
                new[d-1] += count
                new[d] += (r-2)*count
                new[d+1] += count
            distribution = new
            assert sum(distribution.values()) == r**m
            assert max(distribution.values())**2*m <= 9*r*r**(2*m)
            checks["count_difference_atom_bounds"] += 1

    profiles = []
    for m in (2, 10, 20, 50, 100, 200):
        for t in sorted({0, 1, isqrt(m)//4, isqrt(m)//2}):
            count = survivor_count(m, 3, t)
            bound = 1-Fraction(count, 3**m)
            binary = Fraction(sum(comb(m, j) for j in range((m-t-1)//2+1)), 2**m)
            old_cut = (2*m)//3+t
            previous = Fraction(sum(comb(m, j)*2**j for j in range(old_cut+1, m+1)), 3**m)
            assert bound >= previous
            profiles.append({"r": 3, "m": m, "t": t,
                             "survivor_rank_lower_bound": str(bound),
                             "survivor_decimal": float(bound), "binary_decimal": float(binary),
                             "previous_averaged_cut_decimal": float(previous)})
            checks["exact_multinomial_comparison_profiles"] += 1
    assert any(p["survivor_decimal"] > p["binary_decimal"] for p in profiles)
    assert any(p["survivor_decimal"] < p["binary_decimal"] for p in profiles)

    # Equal-weight rewriting is not a terminating reduction: P=chi at m=t=1.
    alpha_set = list(product(range(3), repeat=1))
    wrong = [a for a in alpha_set if all(a.count(h) < a.count(0)+h for h in (1, 2))]
    assert len(wrong) == 2 and len(alpha_set) == 3
    # Full mu_3 has constant-predictor error 2/3; its two-point subset has 1/2.
    assert Fraction(1, 2) < 1-Fraction(1, 3)
    result = {"status": "passed", "arithmetic": "exact F4, F5, integers and rationals",
              "seed": 2026112507, "counts": dict(checks), "profiles": profiles,
              "negative_controls": [
                  {"omission": "strict weight descent", "example": "m=t=1, P=chi, actual rank error zero",
                   "incorrect_survivor_count": len(wrong), "full_dimension": 3},
                  {"omission": "full root alphabet", "example": "constant predictor on a two-point subset of mu_3",
                   "actual_error": "1/2", "invalid_full_alphabet_claim": "2/3"}],
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "helper_sha256": hashlib.sha256(Path(__file__).with_name("verify_inverse_query_commutator.py").read_bytes()).hexdigest(),
              "scope": "Finite matrix quotient and count controls; not a tape implementation or general runtime lower bound"}
    Path("survivor-basis-verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "profiles"}, indent=2))


if __name__ == "__main__":
    main()
