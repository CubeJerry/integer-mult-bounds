#!/usr/bin/env python3
"""Exact finite checks of the scalar-count aliasing bound; no tape claim."""
from fractions import Fraction
from math import comb
import json
from pathlib import Path


def masses(m, p):
    out = [0] * (2 * p)
    for c in range(m + 1):
        out[c % (2 * p)] += comb(m, c)
    return out


def main():
    cases = []
    total = 0
    for p in [3, 5, 7, 11, 17, 31]:
        for m in [1, 2, 3, 9, 15, 31, 63, 127, 255, 511, 1023]:
            pp = masses(m, p)
            diff = sum(abs(pp[r] - pp[r + p]) for r in range(p))
            best = Fraction(sum(max(pp[r], pp[r + p]) for r in range(p)), 2 ** m)
            assert best == Fraction(1, 2) + Fraction(diff, 2 ** (m + 1))
            # cos^2(pi/(2p)) <= 1-1/p^2, from sin x >= 2x/pi.
            # Rational relaxation of Parseval, checked using integers only.
            assert diff ** 2 * p ** (2 * m) <= p * (p * p - 1) ** m * 4 ** m
            total += 1
            if m in [31, 127, 511, 1023]:
                cases.append({"p": p, "m": m, "best_success": str(best),
                              "best_success_decimal": float(best),
                              "defect_one_sixteenth_impossible": best < Fraction(15, 16)})
    collisions = 0
    for p in [3, 5, 7, 11, 17]:
        for c in range(3 * p):
            assert c % p == (c + p) % p
            assert (-1) ** c != (-1) ** (c + p)
            collisions += 1
    # Exhaust a small shift family against its optimal scalar-count decision.
    m, p = 9, 3
    width = 1 << m.bit_length()
    beta = [sum((((j & t).bit_count() & 1) << (j - 1))
                for j in range(1, m + 1)) for t in range(width)]
    pp = masses(m, p)
    decision = [(-1) ** (r if pp[r] >= pp[r + p] else r + p) for r in range(p)]
    successes = []
    for freq in range(1 << m):
        target = (-1) ** freq.bit_count()
        successes.append(sum((-1) ** b.bit_count() *
                             decision[(b ^ freq).bit_count() % p] == target for b in beta))
    mean = Fraction(sum(successes), width * (1 << m))
    best = Fraction(sum(max(pp[r], pp[r + p]) for r in range(p)), 2 ** m)
    assert mean == best
    assert Fraction(min(successes), width) <= mean
    return {"status": "passed", "scope": "Finite identities; all-m claim proved in note",
            "rational_parseval_cases": total, "count_collisions": collisions,
            "selected_cases": cases, "exhaustive_shift_example": {
                "m": m, "p": p, "rows": width, "tuples": 1 << m,
                "average": str(mean), "worst": str(Fraction(min(successes), width)),
                "worst_tuple": successes.index(min(successes))}}


if __name__ == "__main__":
    result = main()
    Path(__file__).with_name("count-aliasing-verification.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
