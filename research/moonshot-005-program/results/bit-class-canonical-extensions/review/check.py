#!/usr/bin/env python3
"""Direct actual-source F2 class/canonical quotient table, algebra only."""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return len(pivots)


def main(a):
    raw = (a.repo / 'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'native pin')
    word = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        r = [F(x) for x in word['frames'][str(word['start'][i])]['B'][0]]
        n = sum(x*x for x in r)
        need(n in (1, 4), 'normalization')
        roots.append([x*(2 if n == 1 else 1) for x in r])
    dot = lambda r, s: sum(x*y for x, y in zip(r, s))
    class_result = (a.workspace / 'root-work/orthogonal-class-fitting/RESULT.json').read_bytes()
    need(hashlib.sha256(class_result).hexdigest() ==
         '7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117', 'class partition pin')
    groups = json.loads(class_result)['groups']
    need(len(groups) == 15 and sorted(i for g in groups for i in g) == list(range(111)), 'partition')
    need(all(dot(roots[i], roots[j]) == 0 for g in groups for i in g for j in g if i != j), 'class contacts')
    U = [sum(1 << i for i in g) for g in groups]
    K = [sum(1 << j for j in range(111) if j == i or dot(roots[i], roots[j]) == 0) for i in range(111)]
    need((rank(U), rank(K), rank(U+K)) == (15, 9, 19), 'code ranks')
    # Disjoint class indicators have distinct pivots; reduction modulo U is exact.
    pivots = sorted(((u.bit_length()-1, u) for u in U), reverse=True)
    def reduce_U(row):
        for p, u in pivots:
            if row >> p & 1:
                row ^= u
        return row
    residue = list(map(reduce_U, K))
    basis, representatives = [], []
    for i, row in enumerate(residue):
        if rank(basis + [row]) > len(basis):
            basis.append(row)
            representatives.append(i)
    need(len(basis) == 4, 'quotient dimension')
    coordinates = {0: 0}
    for k, row in enumerate(basis):
        coordinates.update({v ^ row: m ^ (1 << k) for v, m in list(coordinates.items())})
    need(len(coordinates) == 16, 'all quotient elements')
    class_rows, locals_out = [], []
    for c, g in enumerate(groups):
        cosets = {coordinates[residue[i]] for i in g}
        need(len(cosets) == 1 and 0 not in cosets, 'common nonzero coset')
        label = next(iter(cosets))
        need(rank(U + [K[g[0]]]) == 16, 'minimal W dimension')
        canonical_inside = [i for i in range(111) if rank(U+[K[g[0]], K[i]]) == 16]
        need(canonical_inside == sorted(g), 'exactly own class canonical rows in W')
        weights = []
        for i in g:
            ell = K[i] ^ U[c]
            need(not (ell >> i & 1), 'local diagonal zero')
            support = [j for j in range(111) if ell >> j & 1]
            need(all(dot(roots[i], roots[j]) == 0 for j in support), 'local facet support')
            facet = word['frames'][str(word['final'][111+i])]
            need(facet['dim'] == 7 and all(dot(roots[i], [F(x) for x in r]) == 0 for r in facet['B']), 'actual Fi')
            weights.append(len(support))
            locals_out.append({'i': i, 'class': c, 'l_i_hex': hex(ell), 'support_size': len(support)})
        class_rows.append({'class': c, 'indices': g, 'representative': g[0],
                           'quotient_coordinate': label, 'quotient_binary': format(label, '04b'),
                           'quotient_reduced_row_hex': hex(residue[g[0]]),
                           'W_dimension': 16, 'canonical_rows_in_W': sorted(g),
                           'local_weight_min': min(weights), 'local_weight_max': max(weights)})
    need({r['quotient_coordinate'] for r in class_rows} == set(range(1,16)), 'fifteen distinct nonzero classes')
    table = {'schema': 'actual-BIT-F2-class-canonical-coset-table-v1',
             'source_sha256': PIN, 'U_dimension': 15, 'C_dimension': 9,
             'intersection_dimension': 5, 'union_dimension': 19, 'quotient_dimension': 4,
             'quotient_basis_K_row_indices': representatives,
             'coordinate_convention': 'Bit k is reduced K row at quotient_basis_K_row_indices[k]; reductions use highest bit pivots of disjoint U indicators.',
             'classes': class_rows, 'local_rows': sorted(locals_out, key=lambda x: x['i'])}
    (a.output / 'TABLE.json').write_text(json.dumps(table, indent=2, sort_keys=True)+'\n')
    result = {'status': 'PASS_EXACT_F2_CLASS_COSET_TABLE_AND_LOCAL_IDENTITY',
              'source_sha256': PIN, 'classes_with_one_coset': 15,
              'distinct_nonzero_cosets': 15, 'all111_local_diagonals_zero': True,
              'all111_local_supports_inside_actual_Fi': True,
              'fifteen_distinct_W16_codes': True,
              'physical_local_availability_claimed': False,
              'full_source_or_supplier_claimed': False}
    (a.output / 'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': result['status'], 'basis': representatives,
                      'class_coset_coordinates': [r['quotient_coordinate'] for r in class_rows]}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O')
    p=argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
