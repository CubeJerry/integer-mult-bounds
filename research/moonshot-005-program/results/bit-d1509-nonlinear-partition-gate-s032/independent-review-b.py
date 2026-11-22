#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fresh GF64 ranks and pairwise partition tests; imports no author helper."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse, gzip, json
import numpy as np


def product(a, b):
    polynomial = 0
    for i in range(6):
        if a & (1 << i):
            for j in range(6):
                if b & (1 << j):
                    polynomial ^= 1 << (i + j)
    for degree in range(10, 5, -1):
        if polynomial & (1 << degree):
            polynomial ^= 0x43 << (degree - 6)
    return polynomial


MUL = np.array([[product(a, b) for b in range(64)] for a in range(64)], dtype=np.uint8)
INV = np.array([0] + [next(b for b in range(1, 64) if product(a, b) == 1) for a in range(1, 64)], dtype=np.uint8)


def rank(a):
    a = np.array(a, dtype=np.uint8, copy=True)
    r = 0
    for j in range(a.shape[1]):
        pivots = np.flatnonzero(a[r:, j])
        if not len(pivots):
            continue
        p = r + int(pivots[0])
        a[[r, p]] = a[[p, r]]
        a[r] = MUL[INV[a[r, j]], a[r]]
        for q in np.flatnonzero(a[r + 1:, j]) + r + 1:
            a[q] ^= MUL[a[q, j], a[r]]
        r += 1
        if r == a.shape[0]:
            break
    return r


def same_relations(n, g, generators_a, generators_b):
    for a, b in zip(generators_a, generators_b):
        for x in range(1 << n):
            for y in range(1 << n):
                if ((x ^ y) in (0, a)) != ((g[x] ^ g[y]) in (0, b)):
                    return False
    return True


def join_sizes(n, generators):
    unseen = set(range(1 << n))
    sizes = []
    while unseen:
        first = min(unseen)
        reached, todo = {first}, [first]
        while todo:
            x = todo.pop()
            for a in generators:
                y = x ^ a
                if y not in reached:
                    reached.add(y)
                    todo.append(y)
        unseen -= reached
        sizes.append(len(reached))
    return sorted(sizes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    predecessor = here.parent / 'bit-simultaneous-d1509-s032-independent'
    frame_path = predecessor / 'output/FRAMES.json.gz'
    witness_path = predecessor / 'candidate-output/FIVE-RECEIVER-WITNESSES.json.gz'
    assert sha256(frame_path.read_bytes()).hexdigest() == '3968f31bb756ae4d31977f830068619257b36502f0066b5bc873d053ccadd075'
    assert sha256(witness_path.read_bytes()).hexdigest() == '1393957a807720d744ddf4961c78516c4e230b80aa39c666195feca44d51a495'
    frames = json.loads(gzip.decompress(frame_path.read_bytes()))
    witnesses = json.loads(gzip.decompress(witness_path.read_bytes()))
    native = sorted(int(r) for r in frames['0'] if int(r) < 111)
    assert len(native) == 11
    assert sorted(tuple(w['receivers']) for w in witnesses) == list(combinations(native, 5))
    counts, ranks = Counter(), Counter()
    for w in witnesses:
        actual = []
        for donor in w['donor_pair']:
            matrix = np.concatenate([np.array(frames[str(donor)][str(r)], dtype=np.uint8) for r in w['receivers']], axis=1)
            assert matrix.shape == (96, 40)
            actual.append(rank(matrix))
        assert actual == w['ranks'] and actual[0] != actual[1]
        counts[w['donor_pair'][1]] += 1
        ranks[tuple(actual)] += 1
    assert dict(counts) == {45: 399, 61: 63}
    zero_only = list(range(8)); zero_only[3], zero_only[4] = 4, 3
    assert [set(zero_only[x] for x in (0, a)) for a in [1, 2, 3]] == [{0, 1}, {0, 2}, {0, 4}]
    assert not same_relations(3, zero_only, [1, 2, 3], [1, 2, 4])
    assert (2 ^ 3) == 1 and (zero_only[2] ^ zero_only[3]) == 6
    trials = 0
    for rem in permutations([3, 5, 6, 7]):
        g = [0, 1, 2, 4, *rem]
        assert len(set(g)) == 8 and not same_relations(3, g, [1, 2, 3], [1, 2, 4])
        trials += 1
    assert trials == 24 and join_sizes(3, [1, 2, 3]) == [4, 4] and join_sizes(3, [1, 2, 4]) == [8]
    positive = [x ^ (((x >> 2) & 1) * ((x >> 3) & 1)) for x in range(16)]
    assert len(set(positive)) == 16 and all(positive[positive[x]] == x for x in range(16))
    assert positive[4] ^ positive[8] != positive[12]
    assert same_relations(4, positive, [1, 2], [1, 2]) and join_sizes(4, [1, 2]) == [4, 4, 4, 4]
    result = dict(status='PASS_INDEPENDENT_B_NONLINEAR_PARTITION_REVIEW',
                  author_code_imported=False, fresh_field_reduction='polynomial product modulo x^6+x+1',
                  fresh_join_ranks=924, five_sets=462, donor_witness_counts=dict(counts),
                  rank_pair_counts={str(k): v for k, v in ranks.items()},
                  zero_only_bijections_checked=trials, nonlinear_positive_control=True,
                  physical_frame_reconstruction='Inherited pinned independent S032 frame reconstruction, not newly reexecuted here.',
                  accepted_scope='All-baseline common fibre partitions over finite coefficient fields and fixed identity lane repeats; arbitrary donor-wise bijections.',
                  arbitrary_nonlinear_suppliers_excluded=False, new_kappa=False)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], '924 fresh ranks;462 five-sets;24 zero-only controls;nonlinear positive accepted')


if __name__ == '__main__':
    main()
