#!/usr/bin/env python3
"""Independent literal-polynomial and circuit-carry checks of KC1--KC5."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def rem(poly, divisor):
    out = list(poly)
    while len(out) >= len(divisor):
        offset, lead = len(out) - len(divisor), out[-1]
        for j, coeff in enumerate(divisor): out[offset + j] -= lead * coeff
        while out and out[-1] == 0: out.pop()
    return out + [0] * (len(divisor) - 1 - len(out))


factors = ((0, 1), (1, 1), (1, 1, 1))
columns = [sum((rem([0] * j + [1], g) for g in factors), []) for j in range(4)]
A = [list(row) for row in zip(*columns)]
assert A == [[1, 0, 0, 0], [1, -1, 1, -1], [1, 0, -1, 1], [0, 1, -1, 0]]
E = [[v % 2 for v in row] for row in A]
D = [[((a - e) // 2) % 2 for a, e in zip(row_a, row_e)] for row_a, row_e in zip(A, E)]


def linear(matrix, x):
    return [sum(a * b for a, b in zip(row, x)) % 2 for row in matrix]


def carry(matrix, x):
    return [(sum(a * b for a, b in zip(row, x)) % 4) // 2 for row in matrix]


def quadratic(x):
    return [(sum(D[r][j] * x[j] for j in range(4)) +
             sum(E[r][i] * E[r][j] * x[i] * x[j] for i in range(4) for j in range(i + 1, 4))) % 2
            for r in range(4)]


def kc5(x):
    x0, x1, x2, x3 = x
    return [0, (x1 + x3 + sum(x[i] * x[j] for i in range(4) for j in range(i + 1, 4))) % 2,
            (x2 + x0 * x2 + x0 * x3 + x2 * x3) % 2, (x2 + x1 * x2) % 2]


counts = Counter()
bits = list(product((0, 1), repeat=4))
for x in bits:
    assert carry(A, x) == quadratic(x) == kc5(x)
    counts['literal_input_vectors'] += 1
for u, v in product(bits, repeat=2):
    uv, both = [a ^ b for a, b in zip(u, v)], [a * b for a, b in zip(u, v)]
    ku, kv, kuv = carry(A, u), carry(A, v), carry(A, uv)
    eu, ev, eboth = linear(E, u), linear(E, v), linear(E, both)
    assert [a ^ b ^ c for a, b, c in zip(kuv, ku, kv)] == [a * b ^ c for a, b, c in zip(eu, ev, eboth)]
    counts['polarization_pairs'] += 1

for variant in range(3):
    C = [[E[r][j] + 2 * variant * int((r + j) % 3 == 0) for j in range(4)] for r in range(4)]
    correction = [[((A[r][j] - C[r][j]) // 2) % 2 for j in range(4)] for r in range(4)]
    for x in bits:
        low, high = [], []
        for row in C:
            lo, hi = 0, 0
            for j, coefficient in enumerate(row):
                for _ in range(coefficient):
                    hi ^= lo * x[j]
                    lo ^= x[j]
            low.append(lo)
            high.append(hi)
        assert low == linear(E, x) and high == carry(C, x)
        assert carry(A, x) == [a ^ b for a, b in zip(high, linear(correction, x))]
        counts['literal_lifted_circuit_inputs'] += 1
for x in ((0, 1, 0, 0), (1, 1, 0, 0)):
    assert carry(A, x) != carry(E, x)
    counts['uncorrected_lift_negative_controls'] += 1

proof = ROOT.parent / 'lead/carry-remainder-interface.md'
receipt = {'status': 'passed', 'utc': datetime.now(timezone.utc).isoformat(),
           'scope': 'KC1--KC5 finite b=2 checks; KC6--KC7 and UC4--UC6 separately reviewed algebraically',
           'proof_sha256': sha256(proof.read_bytes()).hexdigest(),
           'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
           'caller_sha256': sha256((ROOT.parent / 'route-a/unramified-polynomial-crt-caller.md').read_bytes()).hexdigest(),
           'review_sha256': sha256((ROOT / 'REVIEW-CRT-CALLER-AND-CARRY.md').read_bytes()).hexdigest(),
           'counts': dict(sorted(counts.items())), 'integer_remainder_matrix': A,
           'high_coefficient_matrix': D}
(ROOT / 'carry-remainder-independent-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
