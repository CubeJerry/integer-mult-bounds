#!/usr/bin/env python3
"""Exact finite support controls; the circuit theorem has an unbounded proof."""
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path
import json
import platform

ROOT = Path(__file__).resolve().parent


def swap(word, i, j):
    result = list(word)
    result[i], result[j] = result[j], result[i]
    return tuple(result)


def overlap_witness(words, generators):
    neighborhoods = {
        word: {swap(word, i, j) for i, j in generators} for word in words
    }
    for left, right in combinations(words, 2):
        common = neighborhoods[left] & neighborhoods[right]
        if len(common) >= 2:
            return {"left": left, "right": right, "common": sorted(common)}
    raise AssertionError("Expected a four-cycle outside the theorem's hypotheses")


def main():
    orbits = []
    vertex_checks = edge_checks = input_pair_checks = weighted_checks = 0
    for size in range(3, 8):
        words = list(permutations(range(size)))
        index = {word: i for i, word in enumerate(words)}
        pair_owner = {}
        arity = size - 1
        for row_index, word in enumerate(words):
            neighbors = [index[swap(word, 0, j)] for j in range(1, size)]
            assert len(set(neighbors)) == arity
            for pair in combinations(sorted(neighbors), 2):
                assert pair not in pair_owner
                pair_owner[pair] = row_index
                input_pair_checks += 1
            for weights in ([1] * arity, [(-1) ** j for j in range(arity)]):
                coefficients = {source: weight for source, weight in zip(neighbors, weights)}
                assert len(coefficients) == arity and all(coefficients.values())
                weighted_checks += 1
        assert len(words) == factorial(size)
        vertex_checks += len(words)
        edge_checks += len(words) * arity
        orbits.append({"m": arity, "vertices": len(words),
                       "degree": arity, "shared_input_pairs": len(pair_owner),
                       "proved_addition_lower_bound": (arity - 1) * len(words)})

    density_checks = 0
    for arity in range(2, 65):
        for alphabet in (arity * (arity + 1), 1 << (2 * arity.bit_length())):
            density = Fraction(1)
            for used in range(arity + 1):
                density *= Fraction(alphabet - used, alphabet)
            union_bound = 1 - Fraction(arity * (arity + 1), 2 * alphabet)
            assert density >= union_bound >= Fraction(1, 2)
            density_checks += 1

    repeated_letters = overlap_witness(list(product(range(2), repeat=4)),
                                       [(0, 1), (0, 2), (0, 3)])
    nonhub_generator = overlap_witness(list(permutations(range(3))),
                                      [(0, 1), (0, 2), (1, 2)])
    word = (0, 1, 2, 3)
    nonzero_sources = {swap(word, 0, j): weight
                       for j, weight in enumerate([1, 1, 0], start=1) if weight}
    assert len(nonzero_sources) == 2 < 3

    files = [Path(__file__), ROOT / "STAR-SHARED-SUM-OBSTRUCTION.md",
             ROOT.parent / "route-a" / "ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md"]
    receipt = {
        "status": "passed",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "orbit_cases": orbits,
        "vertex_checks": vertex_checks,
        "edge_checks": edge_checks,
        "unique_two_input_support_checks": input_pair_checks,
        "weighted_support_checks": weighted_checks,
        "exact_density_checks": density_checks,
        "negative_controls": {"repeated_letters": repeated_letters,
                              "nonhub_generator": nonhub_generator,
                              "zero_weight_support": len(nonzero_sources)},
        "sha256": {str(path.relative_to(ROOT.parent)): sha256(path.read_bytes()).hexdigest()
                   for path in files},
        "scope": "Finite exact support/density controls; no circuit enumeration, bit-runtime claim, or multiplier execution."
    }
    (ROOT / "star-shared-sums-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
