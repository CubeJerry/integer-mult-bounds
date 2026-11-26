#!/usr/bin/env python3
"""Exact finite evidence for CR; not an asymptotic proof or a tape run."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent


def rank_mod(matrix, p):
    a = [[x % p for x in row] for row in matrix]
    rank = 0
    for col in range(len(a[0]) if a else 0):
        pivot = next((r for r in range(rank, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = pow(a[rank][col], -1, p)
        a[rank] = [(x * scale) % p for x in a[rank]]
        for r in range(len(a)):
            if r != rank and a[r][col]:
                z = a[r][col]
                a[r] = [(v-z*w) % p for v, w in zip(a[r], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def dot(a, b, q):
    return sum(x*y for x, y in zip(a, b)) % q


def canonical(v, q):
    c = next(x for x in v if x)
    inv = pow(c, -1, q)
    return tuple(x*inv % q for x in v)


def collision_checks():
    rng = random.Random(20261126)
    examples = 0
    scalar_ranks = 0
    block_checks = 0
    symmetric_counts = []
    for q in (2, 3, 5):
        for dim in (1, 2, 3):
            nonzero = [v for v in product(range(q), repeat=dim) if any(v)]
            for _ in range(24):
                n = rng.randrange(2, 13)
                source = [rng.choice(nonzero) for _ in range(n)]
                destination = []
                for v in source:
                    options = [u for u in product(range(q), repeat=dim)
                               if dot(u, v, q) == 1]
                    destination.append(rng.choice(options))
                classes = Counter(canonical(v, q) for v in source)
                largest = max(classes.values())
                assert len(classes) <= (q**dim-1)//(q-1)
                for p in (2, 3, 5, 7):
                    free = [[rng.randrange(p) if dot(destination[i], source[j], q) == 0
                             else 0 for j in range(n)] for i in range(n)]
                    charged = [[int(i == j)-free[i][j] for j in range(n)] for i in range(n)]
                    rank = rank_mod(charged, p)
                    assert rank >= largest
                    assert Fraction(rank, n) >= Fraction(q-1, q**dim-1)
                    for v in classes:
                        ids = [i for i, x in enumerate(source) if canonical(x, q) == v]
                        for i in ids:
                            for j in ids:
                                assert charged[i][j] % p == int(i == j)
                                block_checks += 1
                    scalar_ranks += 1
                examples += 1
    for dim in range(1, 9):
        norm_one = [v for v in product((0, 1), repeat=dim) if dot(v, v, 2) == 1]
        assert len(norm_one) == 2**(dim-1)
        symmetric_counts.append({'dimension': dim, 'norm_one_directions': len(norm_one)})
    equalities = []
    for t in range(1, 17):
        matrix = [[int(i % t == j % t) for j in range(2*t)] for i in range(2*t)]
        for p in (2, 3, 5, 7):
            assert rank_mod(matrix, p) == t
        equalities.append({'D': 2, 'N': 2*t, 'rank': t})
    # Adverse control: a single collision class but target all-ones.
    # It has rank 1, demonstrating why I=P+F is indispensable.
    adverse = [[1]*5 for _ in range(5)]
    assert rank_mod(adverse, 3) == 1 < 5
    return {'random_geometric_instances': examples, 'exact_scalar_rank_checks': scalar_ranks,
            'identity_class_entries': block_checks, 'symmetric_count_checks': symmetric_counts,
            'sharp_binary_examples': equalities, 'all_ones_target_rejected': True}


def pow2(exponent):
    assert isinstance(exponent, int)
    return Fraction(2**exponent) if exponent >= 0 else Fraction(1, 2**(-exponent))


def dp_invoice(max_x, K, B, p):
    """All even y>=2, exact child x-y, fixed even base X=2."""
    cost = {2: Fraction(1)}
    selected = {}
    for x in range(4, max_x+1, 2):
        candidates = [(pow2(K*y-x//2)+B*y**p*cost[x-y], y)
                      for y in range(2, x-1, 2)]
        value, y = min(candidates)
        cost[x] = value
        selected[x] = y
        for candidate, _ in candidates:
            assert value <= candidate
    paths = []
    for start in (32, 64, 128, max_x):
        if start not in cost:
            continue
        x = start
        chain = []
        while x > 2:
            y = selected[x]
            assert 0 < y <= x-2
            chain.append([x, y])
            x -= y
        # Logarithms are intentionally not used to certify the asymptotics.
        f = cost[start]
        paths.append({'x': start, 'depth': len(chain), 'first_y': chain[0][1],
                      'bill_numerator_bits': f.numerator.bit_length(),
                      'bill_denominator_bits': f.denominator.bit_length(),
                      'selected_chain': chain})
    return paths


def invoice_checks():
    families = []
    for K, B, p in ((1, 2, 1), (2, 2, 1), (1, 3, 2)):
        paths = dp_invoice(256, K, B, p)
        families.append({'K': K, 'B': B, 'p': p, 'exact_optimum_samples': paths})
    controls = 0
    for x in range(8, 260, 4):
        y = x-4
        # K=1/4 permits one giant descent with bounded ordinary toll.
        bill = pow2(y//4-x//2) + 2*y
        assert bill <= 2*x+1
        controls += 1
        # Dropping the ordinary toll permits a one-step polynomial bill.
        assert 2*(x-2) <= 2*x
        controls += 1
        # Dropping regular shrink permits y=2 and direct jump to the base.
        arbitrary_jump = pow2(2-x//2)+4
        assert arbitrary_jump <= 5
        controls += 1
    # With child factor exactly 1, constant arity y=2 gives a bounded sum.
    cost = Fraction(1)
    for x in range(4, 258, 2):
        cost = pow2(2-x//2)+cost
        assert cost < 3
        controls += 1
    return {'families': families, 'failed_premise_controls': controls,
            'scope': 'Exact rational finite dynamic programming. No finite grid proves CR10.'}


def main():
    evidence = {'claim': 'CR3-CR7 and finite CR8-CR9 diagnostics',
                'scope': 'Exact algebra/rational invoices; no physical tape timing or full multiplication.',
                'collision': collision_checks(), 'invoice': invoice_checks()}
    evidence['source_sha256'] = {
        name: sha256((HERE/name).read_bytes()).hexdigest()
        for name in ('verify_collision_and_invoice.py', 'collision-rank-and-invoice-floor.md')}
    path = HERE/'collision-invoice-verification.json'
    path.write_text(json.dumps(evidence, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'rank_checks': evidence['collision']['exact_scalar_rank_checks'],
                      'class_entries': evidence['collision']['identity_class_entries'],
                      'controls': evidence['invoice']['failed_premise_controls'],
                      'output': str(path)}, indent=2))


if __name__ == '__main__':
    main()
