#!/usr/bin/env python3
"""Exact finite checks for SF1--SF10; no claim to establish FC."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent


def parity(x):
    return x.bit_count() & 1


def rref(rows, f):
    a = list(rows)
    rank = 0
    for p in range(f):
        pivot = next((j for j in range(rank, len(a)) if (a[j] >> p) & 1), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for j in range(len(a)):
            if j != rank and ((a[j] >> p) & 1):
                a[j] ^= a[rank]
        rank += 1
    return tuple(a[:rank])


def choose_q2(f, r):
    value = Fraction(1)
    for j in range(r):
        value *= Fraction((1 << f) - (1 << j), (1 << r) - (1 << j))
    assert value.denominator == 1
    return value.numerator


def h(t, r):
    ans = 1
    for j in range(r):
        ans *= (1 << t) - (1 << j)
    return ans


def coordinates(basis, f):
    pivots = [((v & -v).bit_length() - 1) for v in basis]
    nonpivots = [j for j in range(f) if j not in pivots]
    r, s = len(pivots), len(nonpivots)

    def compose(alpha, beta):
        out = 0
        for i, u in enumerate(basis):
            if (alpha >> i) & 1:
                out ^= u
        for i, j in enumerate(nonpivots):
            if (beta >> i) & 1:
                out ^= 1 << j
        return out

    def primal(x):
        alpha = sum(((x >> p) & 1) << i for i, p in enumerate(pivots))
        rest = x ^ compose(alpha, 0)
        beta = sum(((rest >> p) & 1) << i for i, p in enumerate(nonpivots))
        return alpha, beta

    def dual(y):
        gamma = sum(parity(u & y) << i for i, u in enumerate(basis))
        delta = sum(((y >> p) & 1) << i for i, p in enumerate(nonpivots))
        return gamma, delta

    def dual_compose(gamma, delta):
        out = compose(0, delta)
        for i, p in enumerate(pivots):
            if ((gamma >> i) & 1) ^ parity(basis[i] & out):
                out ^= 1 << p
        return out

    return r, s, compose, primal, dual, dual_compose


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def signed(t):
    return -1 if parity(t) else 1


counts = Counter()
strata = []
subspaces = {}
for A in range(1, 5):
    for f in range(1, 5):
        n = 1 << f
        rank_counts = Counter()
        frames_per_space = Counter()
        for code, B in enumerate(product(range(n), repeat=A - 1)):
            basis = rref(B, f)
            r, s, compose, primal, dual, dual_compose = coordinates(basis, f)
            rank_counts[r] += 1
            frames_per_space[basis] += 1
            subspaces[(f, basis)] = True
            counts['ordered_spectator_fibres'] += 1
            values = [((7 * x + 3 * code + A) % 11) - 5 for x in range(n)]
            direct = [sum(signed(x & y) * values[x] for x in range(n)) for y in range(n)]
            G = [[sum(signed(alpha & gamma) * values[compose(alpha, beta)]
                       for alpha in range(1 << r))
                  for beta in range(1 << s)] for gamma in range(1 << r)]
            Z = [[sum(signed(beta & delta) * G[gamma][beta] for beta in range(1 << s))
                  for delta in range(1 << s)] for gamma in range(1 << r)]
            assert r + s == f  # normalized factors multiply to 2^(-f/2)
            orbit_groups = {}
            for beta in range(1 << s):
                group = {rref((compose(alpha, beta),) + B, f) for alpha in range(1 << r)}
                assert len(group) == 1
                orbit = group.pop()
                assert len(orbit) == r + (beta != 0)
                orbit_groups[beta] = orbit
            assert len(set(orbit_groups.values())) == 1 << s
            for x in range(n):
                alpha, beta = primal(x)
                assert compose(alpha, beta) == x
                for y in range(n):
                    gamma, delta = dual(y)
                    assert dual_compose(gamma, delta) == y
                    assert parity(x & y) == (parity(alpha & gamma) ^ parity(beta & delta))
                    counts['exact_character_entries'] += 1
            for y in range(n):
                gamma, delta = dual(y)
                assert Z[gamma][delta] == direct[y]
                counts['exact_transformed_entries'] += 1
            if r == 0:
                counts['rank_zero_fibres'] += 1
            if r < min(A - 1, f):
                counts['deficient_spectator_fibres'] += 1
        for r in range(min(A - 1, f) + 1):
            expected = choose_q2(f, r) * h(A - 1, r)
            assert rank_counts[r] == expected
            for basis, num in frames_per_space.items():
                if len(basis) == r:
                    assert num == h(A - 1, r)
            strata.append({'A': A, 'f': f, 'r': r, 'frames': expected})
        assert sum(rank_counts.values()) * n == 1 << (A * f)


for f, basis in subspaces:
    r, s, compose, _, _, _ = coordinates(basis, f)
    restricted_rows = [sum(parity(u & v) << j for j, v in enumerate(basis)) for u in basis]
    t = len(rref(restricted_rows, r))
    d = r - t
    eigenvalue = 1 << (r + d)
    expected_rank = 1 << t
    for beta_in in range(1 << s):
        for beta_out in range(1 << s):
            kernel = [[signed(compose(alpha, beta_in) & compose(gamma, beta_out))
                       for alpha in range(1 << r)] for gamma in range(1 << r)]
            gram = matmul(kernel, [list(col) for col in zip(*kernel)])
            squared = matmul(gram, gram)
            assert squared == [[eigenvalue * v for v in row] for row in gram]
            assert sum(gram[i][i] for i in range(1 << r)) == expected_rank * eigenvalue
            # Gram is positive semidefinite; G^2=lambda G and its trace certify
            # rank and equal nonzero singular values exactly over R.
            counts['exact_coset_gram_blocks'] += 1
            if d:
                counts['degenerate_coset_gram_blocks'] += 1
            else:
                counts['nondegenerate_coset_gram_blocks'] += 1


# Adverse control: delta is a dual coordinate, not a primal orbit label.
r, s, compose, primal, dual, dual_compose = coordinates((3,), 2)
assert dual_compose(1, 0) == 1
assert primal(1) == (1, 1)
assert rref((1, 3), 2) != (3,)
counts['dual_orbit_negative_controls'] += 1

# Adverse control: gamma=0 alone erases independent within-coset data.
values = [1, 0, 0, -1]
G = [[sum(signed(alpha & gamma) * values[compose(alpha, beta)] for alpha in range(2))
      for beta in range(2)] for gamma in range(2)]
assert G[0] == [0, 0] and G[1] == [2, 0]
assert any(sum(signed(x & y) * values[x] for x in range(4)) for y in range(4))
counts['scalar_channel_negative_controls'] += 1

proof = ROOT / 'spectator-span-fourier-lift.md'
receipt = {
    'status': 'passed',
    'scope': 'exact finite algebra SF1--SF10 only; FC and asymptotic machine unproved',
    'utc': datetime.now(timezone.utc).isoformat(),
    'proof_sha256': sha256(proof.read_bytes()).hexdigest(),
    'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'counts': dict(sorted(counts.items())),
    'rank_strata': strata,
    'floating_point_spectra': False,
}
(ROOT / 'spectator-span-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'rank_strata'}, indent=2))
