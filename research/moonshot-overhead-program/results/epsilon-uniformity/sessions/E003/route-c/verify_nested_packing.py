#!/usr/bin/env python3
"""Check exact occupied layouts; does not simulate finite-field arithmetic."""
import itertools
import json
from pathlib import Path


def main():
    cases = 0
    checked_bits = 0
    for d_parent, d_child, groups, spatial, payload in itertools.product((1, 2, 3, 5), (1, 2, 4), (1, 2), (2, 3, 5), (1, 3)):
        # The parent initially has rows (group, child_basis, parent_basis).
        original = list(itertools.product(range(groups), range(d_child), range(d_parent), range(spatial), range(payload)))
        first = [(g, c2, o, t, c1) for g, c2, c1, o, t in original]
        second = [(g, o, t, c1, c2) for g, c2, o, t, c1 in first]
        assert len(set(original)) == len(set(first)) == len(set(second))
        # A nontrivial deterministic spatial permutation, valid for odd and even sizes.
        permutation = list(reversed(range(spatial)))
        permuted = [(g, permutation[o], t, c1, c2) for g, o, t, c1, c2 in second]
        unpack_child = [(g, c2, o, t, c1) for g, o, t, c1, c2 in permuted]
        unpack_parent = [(g, c2, c1, o, t) for g, c2, o, t, c1 in unpack_child]
        expected = [(g, c2, c1, permutation[o], t) for g, c2, c1, o, t in original]
        assert unpack_parent == expected
        # There is no degree product in volume beyond the already occupied basis rows.
        assert len(original) == groups * d_child * d_parent * spatial * payload
        assert len(second) == groups * spatial * (payload * d_parent * d_child)
        cases += 1
        checked_bits += len(original)
    receipt = {"scope": "Nested occupied coordinate bijections and permutation commutation; not arithmetic or physical tape execution.", "cases": cases, "distinct_symbolic_bit_positions_checked": checked_bits, "maximum_nested_basis_product": 20, "padding_assumed": False}
    Path(__file__).with_name("nested-packing-verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
