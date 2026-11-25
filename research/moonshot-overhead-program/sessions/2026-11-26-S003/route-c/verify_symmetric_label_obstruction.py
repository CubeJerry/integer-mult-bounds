#!/usr/bin/env python3
"""Exact finite checks for the scoped symmetric-label invoice obstruction.

No floating-point arithmetic, external dependencies, or full multiplier claim.
Run from any directory; the result is written beside this source file.
"""

from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json


def rank_binary(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)


def multiply_binary(a, b):
    out = []
    for row in a:
        value = 0
        while row:
            bit = row & -row
            value ^= b[bit.bit_length() - 1]
            row ^= bit
        out.append(value)
    return out


def bit(row, column):
    return (row >> column) & 1


def inner_direct(q, d):
    h = 2*d - 1
    words = list(product(range(q), repeat=h))
    rows = []
    for u in words:
        row = 0
        for i, v in enumerate(words):
            if sum(a != b for a, b in zip(u, v)) in (0, d):
                row |= 1 << i
        rows.append(row)
    return words, rows


def inner_tensor_entry(u, v, d):
    # e_d(J_i): a selected J coordinate imposes no condition; every
    # unselected coordinate has the identity constraint u_i=v_i.
    h = len(u)
    out = 0
    for active in combinations(range(h), d):
        active = set(active)
        out ^= all(u[i] == v[i] for i in range(h) if i not in active)
    return int(out)


def outer_direct(words, b, d):
    h = 2*d - 1
    outer = list(product(range(len(words)), repeat=h))
    rows = []
    for u in outer:
        row = 0
        for j, v in enumerate(outer):
            changed = [i for i in range(h) if u[i] != v[i]]
            if not changed or (
                len(changed) == d
                and all(bit(b[u[i]], v[i]) for i in changed)
            ):
                row |= 1 << j
        rows.append(row)
    return outer, rows


def outer_tensor_entry(u, v, b, d):
    out = 0
    for active in combinations(range(len(u)), d):
        active = set(active)
        out ^= all(
            bit(b[u[i]], v[i]) if i in active else u[i] == v[i]
            for i in range(len(u))
        )
    return int(out)


def inner_rectangles(q, d):
    """Enumerate actual directed rectangles for the source partition."""
    assert q > 1 and q & (q-1) == 0
    t = q.bit_length()-1
    h = 2*d-1
    words = list(product(range(q), repeat=h))
    index = {word: i for i, word in enumerate(words)}
    rectangles = []
    for differing in combinations(range(h), d):
        fixed_positions = [i for i in range(h) if i not in differing]
        for fixed in product(range(q), repeat=len(fixed_positions)):
            for first_left in range(q):
                for first_right in range(q):
                    if first_left == first_right:
                        continue
                    for positions in product(range(t), repeat=d-1):
                        # At first differing bit k (counting from MSB),
                        # choose a shared prefix and an oriented split.
                        choices = [
                            list(product(range(1 << k), range(2)))
                            for k in positions
                        ]
                        for splits in product(*choices):
                            side_values = [[first_left], [first_right]]
                            left_values = [[first_left]]
                            right_values = [[first_right]]
                            for k, (prefix, left_bit) in zip(positions, splits):
                                shift = t-k-1
                                left_values.append([
                                    (prefix << (shift+1)) | (left_bit << shift) | tail
                                    for tail in range(1 << shift)
                                ])
                                right_values.append([
                                    (prefix << (shift+1)) | ((1-left_bit) << shift) | tail
                                    for tail in range(1 << shift)
                                ])
                            sides = []
                            for values in (left_values, right_values):
                                members = []
                                for varying in product(*values):
                                    word = [0]*h
                                    for i, value in zip(fixed_positions, fixed):
                                        word[i] = value
                                    for i, value in zip(differing, varying):
                                        word[i] = value
                                    members.append(index[tuple(word)])
                                sides.append(tuple(members))
                            rectangles.append(tuple(sides))
    return words, rectangles


counts = {
    "inner_matrix_entries": 0,
    "outer_matrix_entries": 0,
    "selector_coefficient_cases": 0,
    "exact_rank_cases": [],
    "rectangle_cases": [],
    "integer_invoice_majorant_cases": 0,
    "negative_controls_rejected": 0,
}

# The finite range includes d=4, which is not visible in the old outer toy.
for q, d in [(2, 2), (4, 2), (2, 4)]:
    words, b = inner_direct(q, d)
    n0 = len(words)
    for i, u in enumerate(words):
        for j, v in enumerate(words):
            assert bit(b[i], j) == inner_tensor_entry(u, v, d)
            counts["inner_matrix_entries"] += 1
    assert all(v == 0 for v in multiply_binary(b, b))
    r = rank_binary(b)
    assert q**(d-1) <= r <= n0//2
    witness = [i for i, u in enumerate(words) if all(x == 0 for x in u[d-1:])]
    assert len(witness) == q**(d-1)
    assert all(bit(b[i], j) == (i == j) for i in witness for j in witness)
    counts["exact_rank_cases"].append({"q": q, "d": d, "dimension": n0, "rank": r})

    if (q, d) == (2, 2):
        outer, pstar = outer_direct(words, b, d)
        for i, u in enumerate(outer):
            for j, v in enumerate(outer):
                assert bit(pstar[i], j) == outer_tensor_entry(u, v, b, d)
                counts["outer_matrix_entries"] += 1
        rank_outer = rank_binary(pstar)
        n = len(outer)
        assert rank_outer >= r**d * (n0-r)**(d-1)
        assert rank_outer * 2**(d-1) * q**(d*d) >= n
        counts["exact_rank_cases"].append({"q": q, "d": d, "dimension": n, "rank": rank_outer, "outer": True})

for d in [2, 4, 8, 16, 32, 64]:
    h = 2*d-1
    for a in range(d):
        c = sum(comb(h-a, s-a) for s in range(a, d)) % 2
        assert c == (a == d-1)
        counts["selector_coefficient_cases"] += 1

# Literal incidence and unique edge coverage are checked from actual sets.
for q, d in [(2, 2), (4, 2)]:
    words, rectangles = inner_rectangles(q, d)
    t = q.bit_length()-1
    incidence_left = [0]*len(words)
    incidence_right = [0]*len(words)
    covered = {}
    for left, right in rectangles:
        for i in left:
            incidence_left[i] += 1
        for j in right:
            incidence_right[j] += 1
        for i in left:
            for j in right:
                assert sum(a != b for a, b in zip(words[i], words[j])) == d
                covered[i, j] = covered.get((i, j), 0)+1
    expected = comb(2*d-1,d)*(q-1)*t**(d-1)
    assert set(incidence_left) == set(incidence_right) == {expected}
    expected_edges = len(words)*comb(2*d-1,d)*(q-1)**d
    assert len(covered) == expected_edges and set(covered.values()) == {1}
    counts["rectangle_cases"].append({"q": q, "d": d, "rectangles": len(rectangles), "incidence_per_side": expected, "directed_edges": expected_edges})

# L11 can be checked without logs by squaring and exponentiating.
for d in [2, 4, 8, 16, 32]:
    for t in range(1, 65):
        lam = comb(2*d-1,d)**(d+1) * (2**t-1)**d * t**(d*(d-1))
        assert lam*lam >= 2**(d*t) * (t+1)**(d*d)
        counts["integer_invoice_majorant_cases"] += 1

# The power-of-two requirement is substantive: d=3 violates L3.
words, wrong_b = inner_direct(2, 3)
assert any(
    bit(wrong_b[i], j) != inner_tensor_entry(u, v, 3)
    for i, u in enumerate(words) for j, v in enumerate(words)
)
counts["negative_controls_rejected"] += 1

# Replacing the outer e_d by e_(d-1) is detected on actual selector rows.
words, b = inner_direct(2, 2)
outer, pstar = outer_direct(words, b, 2)
assert any(
    bit(pstar[i], j) != outer_tensor_entry(u, v, b, 1)
    for i, u in enumerate(outer) for j, v in enumerate(outer)
)
counts["negative_controls_rejected"] += 1

# Omitting first-differing-bit multiplicity is a false literal invoice.
q, d, t = 4, 2, 2
correct = comb(2*d-1,d)**(d+1) * (q-1)**d * t**(d*(d-1))
wrong = comb(2*d-1,d)**(d+1) * (q-1)**d
assert correct != wrong
counts["negative_controls_rejected"] += 1

result = {
    "status": "passed",
    "arithmetic": "exact integers and binary matrices",
    "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "counts": counts,
    "scope": "Finite selector, rank-witness, literal rectangle and invoice checks. Does not prove the unbounded analytic theorem or execute physical tape routing.",
}
output = Path(__file__).with_name("symmetric-label-obstruction-verification.json")
output.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
