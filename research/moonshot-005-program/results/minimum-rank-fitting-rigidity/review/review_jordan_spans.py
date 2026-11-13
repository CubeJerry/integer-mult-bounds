#!/usr/bin/env python3
"""Independent exact modular-minor review of the source Jordan premises.

No author implementation or computed geometry is imported.  Source roots are
rebuilt in Q^9; frames are enumerated by bit-set clique intersection.  Dense
column elimination over a different prime checks the rational spanning claims.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

SOURCE_SHA = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
BASIS = (5, 56, 69, 100, 65, 77, 96, 103)
PRIME = 1009


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact_rank(rows, labels, modulus=PRIME):
    """Column elimination: previous columns vanish in remaining pivot rows."""
    a = np.asarray(rows, dtype=np.int64) % modulus
    n, width = a.shape
    selected = []
    column_labels = list(range(width))
    pivot_products = 1
    rank = 0
    for row in range(n):
        hit = np.flatnonzero(a[row, rank:])
        if not len(hit):
            continue
        col = rank + int(hit[0])
        if col != rank:
            a[:, [rank, col]] = a[:, [col, rank]]
            column_labels[rank], column_labels[col] = column_labels[col], column_labels[rank]
            pivot_products = -pivot_products % modulus
        val = int(a[row, rank])
        pivot_products = pivot_products * val % modulus
        inv = pow(val, -1, modulus)
        # Eliminate the remainder of this pivot row by column operations.  All
        # earlier selected rows have zeros in these remaining columns.
        factors = a[row, rank + 1:] * inv % modulus
        if rank + 1 < width:
            a[:, rank + 1:] = (a[:, rank + 1:] - a[:, rank:rank + 1] * factors) % modulus
        selected.append({'row': labels[row], 'column': column_labels[rank]})
        rank += 1
        if rank == width:
            break
    return {'rank': rank, 'selected': selected, 'pivot_product_mod_prime': int(pivot_products),
            'prime': modulus}


def main(args):
    raw = (args.repo / 'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'Native identity')
    source = json.loads(gzip.decompress(raw))
    hosted = {source['live'][i] for i in source['hosted']['Dports']}
    indices = sorted(hosted if args.count == 96 else source['live'])
    require(len(indices) == args.count and set(BASIS) <= set(indices), 'Source population')
    roots = {}
    for i in indices:
        normal = source['frames'][source['initial'][i]][0]
        ones = [p for p in range(9) if normal & (1 << p)]
        require(len(ones) in (3, 7), 'Root normal')
        if len(ones) == 3:
            roots[i] = tuple(2 if p in ones else -1 for p in range(9))
        else:
            p, q = [p for p in range(9) if p not in ones]
            roots[i] = tuple(3 * ((k == p) - (k == q)) for k in range(9))
    inner = lambda i, j: sum(x * y for x, y in zip(roots[i], roots[j]))
    require(all(inner(i, j) == 18 * (i == j) for i in BASIS for j in BASIS), 'Basis orthogonality')
    # g2 = twice the orthonormal B coordinates, an integral source realization.
    require(all(inner(i, b) % 9 == 0 for i in indices for b in BASIS), 'Dyadic coordinates')
    g2 = {i: [inner(i, b) // 9 for b in BASIS] for i in indices}
    require(all(sum(x * x for x in g2[i]) == 4 for i in indices), 'Coordinate norms')
    require(all(9 * sum(x * y for x, y in zip(g2[i], g2[j])) == 2 * inner(i, j)
                for i in indices for j in indices), 'Source Gram factorization')
    sym = list(itertools.combinations_with_replacement(range(8), 2))
    projectors = {i: [g2[i][p] * g2[i][q] for p, q in sym] for i in indices}
    # These integral rows equal four times the coordinates of S_i=g_i g_i^T.
    projector_result = exact_rank([projectors[i] for i in indices], indices)
    require(projector_result['rank'] == 36, 'Full symmetric projector span')

    n = len(indices)
    neighbours = [sum(1 << j for j in range(n) if j != k and inner(i, indices[j]) == 0)
                  for k, i in enumerate(indices)]
    frames = []

    def visit(chosen, possible):
        need = 8 - len(chosen)
        if not need:
            frames.append(tuple(indices[k] for k in chosen))
            return
        while possible.bit_count() >= need:
            bit = possible & -possible
            possible ^= bit
            k = bit.bit_length() - 1
            visit(chosen + (k,), possible & neighbours[k])

    visit((), (1 << n) - 1)
    require(len(frames) == len(set(frames)) and tuple(sorted(BASIS)) in frames, 'Actual source frames')
    identity4 = [4 * (p == q) for p, q in sym]
    require(all([sum(projectors[i][k] for i in frame) for k in range(36)] == identity4
                for frame in frames), 'Every frame sums to identity')
    reference = set(BASIS)
    difference_rows = [[int(i in frame) - int(i in reference) for i in indices] for frame in frames]
    # Verify the exact relation before using modular rank to prove completeness.
    require(all(all(sum(row[k] * projectors[indices[k]][j] for k in range(n)) == 0
                        for j in range(36)) for row in difference_rows), 'Frame differences are exact relations')
    relation_result = exact_rank(difference_rows, [list(f) for f in frames])
    require(relation_result['rank'] == n - 36, 'All linear relations generated by frames')

    square_coordinates = list(itertools.combinations_with_replacement(range(36), 2))
    pairs = [(i, j) for i, j in itertools.combinations(indices, 2) if inner(i, j) == 0]
    # Orthogonal generators before squares intentionally differ from author order.
    pairs += [(i, i) for i in reversed(indices)]
    tensors = [[projectors[i][p] * projectors[j][q] +
                (projectors[i][q] * projectors[j][p] if p != q else 0)
                for p, q in square_coordinates] for i, j in pairs]
    tensor_result = exact_rank(tensors, [list(p) for p in pairs])
    require(tensor_result['rank'] == 666, 'Full symmetric-square span of Jordan test pairs')
    # Controls: diagonal coordinates alone cannot establish the 36-dimensional
    # first span; idempotence tests alone cannot establish a 666-dimensional
    # bilinear identity (there are fewer than 666 test rows).
    diagonal_rows = [[projectors[i][k] if p == q else 0 for k, (p, q) in enumerate(sym)]
                     for i in indices]
    require(exact_rank(diagonal_rows, indices)['rank'] == 8, 'Offdiagonal deletion control')
    require(len(indices) < 666, 'Squares alone are insufficient')
    output = {'status': 'PASS_ROOT_JORDAN_SOURCE_PREMISES', 'source_pin': SOURCE_SHA,
              'source_count': n, 'source_indices': indices, 'basis': list(BASIS),
              'source_projector_rank': projector_result, 'source_frame_count': len(frames),
              'frame_relation_rank': relation_result, 'Jordan_tensor_generators': len(pairs),
              'Jordan_tensor_rank': tensor_result,
              'proof_of_exactness': 'Integral rows have nonzero minors modulo1009; hence the same minors are nonzero overQ. Exact source identities give the matching relation upper bound. All characteristic-zero extensions preserve these rational ranks.',
              'negative_controls': {'delete_offdiagonal_projector_coordinates_rank': 8,
                                    'idempotence_only_test_count': len(indices)},
              'scope': 'Independent finite premises for an all-volume Jordan proof; no multiplication bound or physical implementation.'}
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'source_count': n, 'frames': len(frames),
                      'ranks': [projector_result['rank'], relation_result['rank'], tensor_result['rank']]}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--count', type=int, choices=[96, 104], required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
