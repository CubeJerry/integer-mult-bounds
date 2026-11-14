#!/usr/bin/env python3
"""Independent source-premise reconstruction for saturated star rigidity.

No worker-C checker is imported or executed. The nine-bit factor is recovered
from the diagonal of the binary rank-one Schur residual, not a pivot search.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path

NATIVE_PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAME = [0, 16, 17, 32, 36, 38, 67, 71]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rank_rows(rows):
    pivots = {}
    chosen = []
    for i, original in enumerate(rows):
        row = original
        while row:
            p = row.bit_length()-1
            if p not in pivots:
                pivots[p] = row
                chosen.append(i)
                break
            row ^= pivots[p]
    return len(pivots), chosen


def source_check(raw):
    need(hashlib.sha256(raw).hexdigest() == NATIVE_PIN, 'source bytes')
    native = json.loads(gzip.decompress(raw))
    roots = [tuple(F(x) for x in native['frames'][str(native['start'][i])]['B'][0])
             for i in range(111)]
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    K = [[int(i == j or dot(roots[i], roots[j]) == 0) for j in range(111)]
         for i in range(111)]
    need(all(K[i][j] == int(i == j) for i in FRAME for j in FRAME), 'actual independent point frame')
    first = [[K[i][j] for j in FRAME] for i in range(111)]
    residual = [[K[i][j] ^ (sum(x*y for x, y in zip(first[i], first[j])) % 2)
                 for j in range(111)] for i in range(111)]
    last = [residual[i][i] for i in range(111)]
    need(any(last), 'nonzero rank-one residual')
    need(all(residual[i][j] == last[i]*last[j] for i in range(111) for j in range(111)),
         'rank-one symmetric residual equals its diagonal outer product')
    vectors = [sum(v << j for j, v in enumerate(first[i])) | last[i] << 8 for i in range(111)]
    need(all((vectors[i] & vectors[j]).bit_count() % 2 == K[i][j]
             for i in range(111) for j in range(111)), 'all12321 exact factor products')
    need([vectors[i] for i in FRAME] == [1 << j for j in range(8)], 'point coordinate factors')
    edge_roles = {i: tuple(j for j in range(8) if first[i][j]) for i in range(111)
                  if last[i] and sum(first[i]) == 2}
    expected_edges = set(itertools.combinations(range(8), 2)) - {(0, 4)}
    need(len(edge_roles) == 27 and set(edge_roles.values()) == expected_edges, '27-edge sparse seed')
    degree = Counter(a for e in edge_roles.values() for a in e)
    need(sorted(degree.values()) == [6, 6, 7, 7, 7, 7, 7, 7], 'strict degree greater than4')
    for e, f in itertools.permutations(edge_roles, 2):
        need(K[e][f] == int(set(edge_roles[e]).isdisjoint(edge_roles[f])), 'all ordered edge mask constraints')
    seed = sorted(set(FRAME) | set(edge_roles))
    anchors = []
    for i in range(111):
        if i in seed:
            continue
        available = [j for j in seed if K[i][j] == 0]
        r, choices = rank_rows([vectors[j] for j in available])
        need(r == 8, 'rank-eight binary anchor equations')
        picked = [available[j] for j in choices]
        annihilators = [v for v in range(1, 512) if all((v & vectors[j]).bit_count() % 2 == 0 for j in picked)]
        need(annihilators == [vectors[i]], 'unique nonzero annihilator vector')
        need(vectors[i].bit_count() % 2 == 1, 'annihilator unit self pairing')
        need(rank_rows([vectors[j] for j in picked[:-1]])[0] == 7, 'seven-anchor negative control')
        anchors.append({'role': i, 'anchors': picked, 'unique_annihilator': vectors[i]})
    bitrows = [sum(v << j for j, v in enumerate(row)) for row in K]
    ranks = [rank_rows(bitrows)[0], rank_rows([row ^ (1 << i) for i, row in enumerate(bitrows)])[0]]
    need(ranks == [9, 108], 'canonical and residual ranks')
    need(sum(sum(row) for row in K)-111 == 6470 and len(anchors) == 76, 'complete source counts')
    return {'frame': FRAME, 'edge_roles': edge_roles, 'degrees': dict(degree),
            'anchors': anchors, 'factor_vectors': vectors, 'rank_K': 9,
            'rank_K_minus_I': 108, 'foreign_allowed_blocks': 6470}


def small_degree_control():
    edges = list(itertools.combinations(range(4), 2))
    assignment = {(0, 1): 1, (0, 2): 0, (0, 3): 4, (1, 2): 4, (1, 3): 3, (2, 3): 2}
    labels = list(range(4)) + edges
    used_coordinate = list(range(4)) + [assignment[e] for e in edges]
    matrix = [[int(a == b) for b in used_coordinate] for a in used_coordinate]
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            if i == j:
                need(matrix[i][j] == 1, 'degree-three identity diagonal')
            elif isinstance(a, int) and isinstance(b, int):
                need(matrix[i][j] == 0, 'distinct points are noncontacts')
            elif isinstance(a, int):
                need(a in b or matrix[i][j] == 0, 'point-edge noncontact')
            elif isinstance(b, int):
                need(b in a or matrix[i][j] == 0, 'edge-point noncontact')
            elif set(a) & set(b):
                need(matrix[i][j] == 0, 'incident-edge noncontact')
    r = rank_rows([sum(x << j for j, x in enumerate(row)) for row in matrix])[0]
    need(r == 5, 'rank-five degree-three fitting')
    schur = [int(assignment[e] == 4) for e in edges]
    need(schur.count(0) == 4 and schur.count(1) == 2, 'singular Schur counterexample')
    # The rows are standard coordinate units: all products/ranks above have
    # the same interpretation over every field, not only the binary checker.
    return {'graph': 'K4', 'rank': 5, 'schur_diagonals': schur,
            'field_scope': 'all fields, by the displayed coordinate-unit factorization'}


def noncommuting_control():
    def mul(a, b):
        return [[sum(a[i][k]*b[k][j] for k in range(2)) % 2 for j in range(2)] for i in range(2)]
    I = [[1, 0], [0, 1]]
    A = [[1, 1], [0, 1]]
    B = [[1, 0], [1, 1]]
    need(mul(A, B) != mul(B, A), 'noncommuting matrices')
    U, Uinv = mul(A, B), mul(B, A)
    need(mul(U, Uinv) == mul(Uinv, U) == I, 'ordered inverse')
    # A normalized saturated endpoint round-trip is I. An incorrect
    # same-order rather than inverse gauge changes its diagonal.
    need(mul(U, U) != I, 'wrong gauge order negative control')
    return {'noncommuting': True, 'correct_inverse_passes': True, 'same_order_mutant_rejected': True}


def main(args):
    raw = args.native.read_bytes()
    source = source_check(raw)
    try:
        source_check(raw+b' ')
    except ValueError:
        source_mutant = True
    else:
        raise ValueError('source byte mutant passed')
    control = small_degree_control()
    out = {'status': 'PASS_INDEPENDENT_SATURATED_STAR_SOURCE_REVIEW',
           'native_sha256': NATIVE_PIN, 'source': source,
           'controls': {'source_byte_mutant_rejected': source_mutant,
                        'degree_three': control, 'noncommuting_order': noncommuting_control()},
           'author_checker_imported_or_run': False,
           'scope': 'Independent finite source-premise reconstruction and control checks. Universal LR, saturation, ordered gauge and all-width conclusions are independently reviewed in REVIEW.md; not inferred from tests.'}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': out['status'], 'seed_edges': len(source['edge_roles']),
                      'anchors': len(source['anchors']), 'ranks': [9, 108]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
