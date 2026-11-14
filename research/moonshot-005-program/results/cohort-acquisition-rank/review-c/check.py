#!/usr/bin/env python3
"""Independent finite kernel enumeration for the cohort filtration theorem."""
import argparse, hashlib, itertools, json, math, random
from fractions import Fraction
from pathlib import Path

def need(test, message):
    if not test:
        raise ValueError(message)

def act(rows, x):
    return sum(((row & x).bit_count() & 1) << i for i, row in enumerate(rows))

def compose(left, right):
    result = []
    for row in left:
        value = 0
        for j, source in enumerate(right):
            if row >> j & 1:
                value ^= source
        result.append(value)
    return result

def ranges(sizes, width):
    answer = []
    offset = 0
    for size in sizes:
        answer.append(list(range(offset, offset + size * width)))
        offset += size * width
    return answer

def evaluate(targets, acquisitions, width, P, U):
    target_ranges = ranges(targets, width)
    acquisition_ranges = ranges(acquisitions, width)
    N, B = sum(targets) * width, sum(acquisitions) * width
    need(len(P) == B and len(U) == N, 'rectangular dimensions')
    source_masks = [sum(1 << j for j in group) for group in target_ranges]
    acquisition_masks = [sum(1 << j for j in group) for group in acquisition_ranges]
    supports, owners = [], []
    for c, group in enumerate(acquisition_ranges):
        need(all(not (P[j] & source_masks[c]) for j in group), 'own-cohort acquisition forbidden')
        need(all(not (U[j] & ~acquisition_masks[c]) for j in target_ranges[c]), 'local U')
        for first in range(0, len(group), width):
            row = 0
            for j in group[first:first + width]:
                row |= P[j]
            supports.append({d for d, mask in enumerate(source_masks) if row & mask})
            owners.append(c)
    correction = [row ^ (1 << j) for j, row in enumerate(compose(U, P))]
    kernel = [x for x in range(1 << N) if not act(correction, x)]
    need(len(kernel) & (len(kernel) - 1) == 0, 'kernel cardinality is power of two')
    nullity = len(kernel).bit_length() - 1
    rank = N - nullity
    best, steps = 0, 0
    for order in itertools.permutations(range(len(targets))):
        position = {c: i for i, c in enumerate(order)}
        good = [all(position[owner] < position[d] for d in support)
                for owner, support in zip(owners, supports)]
        best = max(best, sum(good))
        mask, previous = 0, 0
        for c in order:
            mask |= source_masks[c]
            count = sum(not (x & ~mask) for x in kernel)
            dimension = count.bit_length() - 1
            bad = sum(owner == c and not g for owner, g in zip(owners, good))
            need(dimension - previous <= bad * width, 'actual filtration increment')
            previous = dimension
            steps += 1
    expectation = sum((Fraction(1, len(s) + 1) for s in supports), Fraction())
    need(best >= math.ceil(expectation), 'order expectation')
    lower = width * (sum(targets) - sum(acquisitions) + best)
    need(rank >= lower, 'rectangular order rank bound')
    return {'rank': rank, 'max_good': best, 'steps': steps, 'singular_U':
            len({act(U, x) for x in range(1 << B)}) < 1 << min(N, B)}

def modular_rank(rows, prime):
    a = [[x % prime for x in row] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col], -1, prime)
        a[rank] = [x * inverse % prime for x in a[rank]]
        for i in range(len(a)):
            if i != rank:
                multiplier = a[i][col]
                a[i] = [(x - multiplier * y) % prime for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    counters = {'cases': 0, 'filtration_steps': 0, 'singular_U_cases': 0}
    for n in (2, 3):
        positions = [(i, j) for i in range(n) for j in range(n) if i != j]
        for bits in range(1 << len(positions)):
            P = [0] * n
            for p, (i, j) in enumerate(positions):
                P[i] |= ((bits >> p) & 1) << j
            for diagonal in range(1 << n):
                U = [((diagonal >> i) & 1) << i for i in range(n)]
                result = evaluate([1] * n, [1] * n, 1, P, U)
                counters['cases'] += 1
                counters['filtration_steps'] += result['steps']
                counters['singular_U_cases'] += result['singular_U']
    rng = random.Random(20261114)
    shapes = [([2, 1, 1], [2, 1, 1], 2), ([1, 1, 1], [0, 2, 1], 2),
              ([1, 2], [3, 0], 2), ([2, 1, 1], [1, 2, 2], 1),
              ([1, 1, 1, 1], [1, 1, 1, 1], 2)]
    for targets, acquisitions, width in shapes:
        tr, ar = ranges(targets, width), ranges(acquisitions, width)
        for unused in range(24):
            P = [0] * (sum(acquisitions) * width)
            U = [0] * (sum(targets) * width)
            for c in range(len(targets)):
                for i in ar[c]:
                    P[i] = sum(rng.randrange(2) << j for d, group in enumerate(tr) if d != c for j in group)
                for i in tr[c]:
                    U[i] = sum(rng.randrange(2) << j for j in ar[c])
            result = evaluate(targets, acquisitions, width, P, U)
            counters['cases'] += 1
            counters['filtration_steps'] += result['steps']
            counters['singular_U_cases'] += result['singular_U']
    sharpness = 0
    for prime in (2, 3, 5):
        for n in range(2, 14):
            for k in range(1, n):
                A = [[int(i // (k + 1) == j // (k + 1)) for j in range(n)] for i in range(n)]
                need(modular_rank(A, prime) == math.ceil(n / (k + 1)), 'all-field grouping sharpness')
                sharpness += 1
    # Removing either physical hypothesis gives rank-zero counterexamples.
    need(compose([2, 1], [2, 1]) == [1, 2], 'free nonlocal inverse counterexample')
    need(compose([1, 2], [1, 2]) == [1, 2], 'own-cohort input counterexample')
    incidence = {str(q): math.ceil(Fraction(111 * 111, q) - 111) for q in (8, 9, 10)}
    need(incidence == {'8': 1430, '9': 1258, '10': 1122}, 'exact native incidence thresholds')
    pins = {name: hashlib.sha256((args.package / name).read_bytes()).hexdigest()
            for name in ('PROOF.md', 'COROLLARIES.md', 'LITERATURE.md')}
    output = {'status': 'PASS_INDEPENDENT_COHORT_FILTRATION_REVIEW',
              'author_code_imported_or_run': False, 'reviewed_pins': pins,
              'enumerated_binary_kernel_cases': counters, 'prime_field_sharpness_cases': sharpness,
              'negative_controls': ['nonlocal_decoder_inverse', 'own_cohort_acquisition'],
              'native_incidence_thresholds': incidence,
              'scope': 'Finite controls support the separately reviewed universal proof; no complete supplier or kappa.'}
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': output['status'], **counters, 'sharpness': sharpness}))

if __name__ == '__main__':
    main()
