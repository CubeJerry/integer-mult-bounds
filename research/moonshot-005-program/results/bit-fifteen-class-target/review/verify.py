#!/usr/bin/env python3
"""Independent source/partition/F2 check of the fifteen-class target.

No author code is imported or executed. This is not a physical-code check.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path

SOURCE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
MANIFEST = '407ecc76c7a4a3b8dd4d88cc4743b63df51be244842f268b7c42f3a27d38d864'
GATE = 'd291d6e58a256f9e173af921c02147f51506335c657fefb041e129a4d608d6c9'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rank(matrix, binary=False):
    a = [[int(x) % 2 if binary else F(x) for x in row] for row in matrix]
    rows, columns = len(a), len(a[0]) if a else 0
    pivot = 0
    for j in range(columns):
        k = next((k for k in range(pivot, rows) if a[k][j]), None)
        if k is None:
            continue
        a[pivot], a[k] = a[k], a[pivot]
        if not binary:
            scale = a[pivot][j]
            a[pivot] = [x / scale for x in a[pivot]]
        for k in range(pivot + 1, rows):
            if a[k][j]:
                if binary:
                    a[k] = [x ^ y for x, y in zip(a[k], a[pivot])]
                else:
                    scale = a[k][j]
                    a[k] = [x - scale*y for x, y in zip(a[k], a[pivot])]
        pivot += 1
        if pivot == rows:
            break
    return pivot


def main(args):
    manifest_raw = (args.author / 'MANIFEST.json').read_bytes()
    assert sha(manifest_raw) == MANIFEST
    manifest = json.loads(manifest_raw)
    for name, pin in manifest['artifacts'].items():
        assert sha((args.author / name).read_bytes()) == pin
    gate_raw = (args.author / 'GATE-MANIFEST.json').read_bytes()
    assert sha(gate_raw) == GATE
    for name, pin in json.loads(gate_raw)['artifacts'].items():
        assert sha((args.author / name).read_bytes()) == pin
    claimed = json.loads((args.author / 'RESULT.json').read_text())
    raw = (args.repo / 'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    assert sha(raw) == SOURCE
    word = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        assert word['frames'][str(word['final'][i])]['dim'] == 8
        assert word['frames'][str(word['start'][111+i])]['dim'] == 0
        first = [F(x) for x in word['frames'][str(word['start'][i])]['B'][0]]
        norm = sum(x*x for x in first)
        assert norm in (1, 4)
        first = [x*(2 if norm == 1 else 1) for x in first]
        if next(x for x in first if x) < 0:
            first = [-x for x in first]
        assert all(x.denominator == 1 for x in first)
        roots.append(tuple(int(x) for x in first))
    assert len(set(roots)) == 111 and all(sum(x*x for x in r) == 4 for r in roots)
    support = lambda r: sum((1 << j) for j, x in enumerate(r) if x)
    patterns = {support(r) for r in roots if support(r).bit_count() == 4}
    assert len(patterns) == 14 and all((255 ^ mask) in patterns for mask in patterns)
    assert sorted(Counter(support(r).bit_count() for r in roots).items()) == [(1, 8), (4, 103)]
    classification = defaultdict(list)
    for i, r in enumerate(roots):
        mask = support(r)
        key = ('coordinate',) if mask.bit_count() == 1 else (
            'pair', min(mask, mask ^ 255), sum(x < 0 for x in r) % 2)
        classification[key].append(i)
    groups = sorted(classification.values(), key=lambda g: min(g))
    assert {tuple(g) for g in groups} == {tuple(g) for g in claimed['groups']}
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    assert len(groups) == 15 and all(dot(roots[i], roots[j]) == 0
        for g in groups for i, j in itertools.combinations(g, 2))

    completion = {tuple(2 * int(j == k) for j in range(8)) for k in range(8)}
    for mask in patterns:
        positions = [j for j in range(8) if mask >> j & 1]
        for bits in range(8):
            r = [0]*8
            r[positions[0]] = 1
            for k, j in enumerate(positions[1:]):
                r[j] = 1 if bits >> k & 1 else -1
            completion.add(tuple(r))
    assert len(completion) == 120 and set(roots) <= completion
    full_classes = defaultdict(list)
    for r in completion:
        mask = support(r)
        key = ('coordinate',) if mask.bit_count() == 1 else (
            'pair', min(mask, mask ^ 255), sum(x < 0 for x in r) % 2)
        full_classes[key].append(r)
    assert len(full_classes) == 15 and all(len(g) == rank(g) == 8 for g in full_classes.values())
    assert all(dot(r, t) == 0 for g in full_classes.values() for r, t in itertools.combinations(g, 2))

    membership = {i: k for k, group in enumerate(groups) for i in group}
    A = [[int(membership[i] == membership[j]) for j in range(111)] for i in range(111)]
    K = [[int(i == j or dot(roots[i], roots[j]) == 0) for j in range(111)] for i in range(111)]
    assert all(A[i][i] == 1 and all(not A[i][j] or K[i][j] for j in range(111)) for i in range(111))
    rA, rK, stacked = [rank(x, True) for x in (A, K, A + K)]
    assert (rA, rK, stacked) == (15, 9, 19)
    basis = []
    for row in K:
        if rank(basis + [row], True) > len(basis):
            basis.append(row)
    code = []
    for bits in range(512):
        row = [sum(basis[k][j] for k in range(9) if bits >> k & 1) % 2 for j in range(111)]
        code.append(row)
    assert len({tuple(row) for row in code}) == 512
    constant = [row for row in code if all(len({row[i] for i in g}) == 1 for g in groups)]
    assert len(constant) == 32 and rank(constant, True) == 5
    for h in claimed['intersection_basis_hex']:
        row = [int(h, 16) >> i & 1 for i in range(111)]
        assert row in constant
    assert rank([[int(h, 16) >> i & 1 for i in range(111)]
                 for h in claimed['intersection_basis_hex']], True) == 5

    foreign_rank = []
    for i in range(111):
        final = word['frames'][str(word['final'][111 + i])]['B']
        facet = [[F(x) for x in row] for row in final]
        assert len(facet) == rank(facet) == 7
        assert all(dot(roots[i], row) == 0 for row in facet)
        foreign = [roots[j] for j in groups[membership[i]] if j != i]
        assert all(dot(roots[i], r) == 0 for r in foreign)
        assert rank(foreign) == len(foreign)
        foreign_rank.append(len(foreign))
    assert foreign_rank.count(7) == 72 and max(foreign_rank) == 7
    changed = sum(A[i][j] != K[i][j] for i in range(111) for j in range(111))
    assert changed == 5748
    canonical_foreign = sum(sum(row) - 1 for row in K)
    fitting_foreign = sum(sum(row) - 1 for row in A)
    assert (canonical_foreign, fitting_foreign) == (6470, 722)
    # A different parity on just one member makes a false orthogonal class.
    wrong_parity_witness = next((i, j) for i, j in itertools.combinations(range(111), 2)
        if support(roots[i]) == support(roots[j]) and
        (sum(x < 0 for x in roots[i]) - sum(x < 0 for x in roots[j])) % 2 and
        dot(roots[i], roots[j]) != 0)
    result = {
        'status': 'PASS_INDEPENDENT_EXACT_CLASS_TARGET_GEOMETRY_AND_F2_ALGEBRA',
        'reviewed_manifest_sha256': MANIFEST, 'native_sha256': SOURCE,
        'reviewed_compiler_gate_manifest_sha256': GATE,
        'method': 'Direct native rational roots/facets; support-mask parity classes; dense low-column F2 elimination; all512 codewords. No author code or helper imported or executed.',
        'full_completion_roots': 120, 'full_completion_orthogonal_bases': 15,
        'actual_class_size_multiset': sorted(map(len, groups)),
        'all_actual_groups_equal_author_partition': True,
        'fitting_rank_every_field': 15, 'binary_canonical_rank': rK,
        'binary_union_rank': stacked, 'binary_intersection_rank': 5,
        'binary_quotient_rank': 10, 'constant_codewords': len(constant),
        'canonical_foreign_coefficients': canonical_foreign,
        'fitting_foreign_coefficients': fitting_foreign,
        'changed_coefficients': changed,
        'foreign_rank_histogram': dict(sorted(Counter(foreign_rank).items())),
        'rows_whose_foreign_roots_span_actual_terminal_facet': 72,
        'arrival_count_interpretation_requires_proper_local_support_premise': True,
        'rank15_implies_at_least7_historical_kernel_dimensions_if_admitted_q8_count_applies': True,
        'wrong_parity_nonorthogonal_control': list(wrong_parity_witness),
        'physical_source_verified': False,
        'scope': 'Algebraic target only. The72 statistic verifies exact facet-span geometry; converting it to an arrival lower bound uses the stated local-support arrival model. No dirty current-row source/cache, timing, q8 word, ordinary/erasure/precision compiler, or complete kappa is supplied. Inherited historical-mode and prior14-bus price gates are cited, not re-proved here.',
    }
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'binary_union_rank', 'binary_intersection_rank',
        'binary_quotient_rank', 'rows_whose_foreign_roots_span_actual_terminal_facet', 'physical_source_verified']}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--author', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
