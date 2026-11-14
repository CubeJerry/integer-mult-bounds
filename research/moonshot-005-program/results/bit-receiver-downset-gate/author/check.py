#!/usr/bin/env python3
"""Exact receiver shortenings of U+C and all canonical extension subcodes."""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PARTITION = '7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def basis(rows):
    pivots, selected = {}, []
    for original in rows:
        v = original
        while v:
            p = v.bit_length()-1
            if p not in pivots:
                pivots[p] = v
                selected.append(original)
                break
            v ^= pivots[p]
    return selected


def coordinates(row, independent):
    table = {}
    for i, v in enumerate(independent):
        c = 1 << i
        while v:
            p = v.bit_length()-1
            if p not in table:
                table[p] = (v, c)
                break
            old, coeff = table[p]
            v ^= old
            c ^= coeff
        need(v != 0, 'independent coordinate basis')
    result = 0
    while row:
        p = row.bit_length()-1
        need(p in table, 'row belongs to code')
        v, c = table[p]
        row ^= v
        result ^= c
    return result


def real_rank(rows):
    a = [[F(x) for x in row] for row in rows]
    k = 0
    for j in range(8):
        p = next((i for i in range(k, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[k], a[p] = a[p], a[k]
        q = a[k][j]
        a[k] = [x/q for x in a[k]]
        for i in range(k+1, len(a)):
            q = a[i][j]
            if q:
                a[i] = [x-q*y for x, y in zip(a[i], a[k])]
        k += 1
    return k


def all_subspaces():
    zero = frozenset([0])
    found = {zero}
    queue = [zero]
    while queue:
        h = queue.pop()
        for v in range(1, 16):
            if v in h:
                continue
            k = h | frozenset(x ^ v for x in h)
            if k not in found:
                found.add(k)
                queue.append(k)
    need(len(found) == 67, 'all binary four-space subspaces')
    return sorted(found, key=lambda h: (len(h), tuple(sorted(h))))


def main(args):
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'native source pin')
    part = args.partition.read_bytes()
    need(hashlib.sha256(part).hexdigest() == PARTITION, 'class partition pin')
    groups = json.loads(part)['groups']
    need(len(groups) == 15 and sorted(itertools.chain.from_iterable(groups)) == list(range(111)), 'exact fifteen-class partition')
    cls = {i: c for c, g in enumerate(groups) for i in g}
    s = json.loads(gzip.decompress(raw))
    roots = [[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]] for i in range(111)]
    dot = lambda x, y: sum(a*b for a, b in zip(x, y))
    for c, group in enumerate(groups):
        need(all(dot(roots[i], roots[j]) == 0 for i, j in itertools.combinations(group, 2)), 'within-class actual orthogonality')
    U = [sum(1 << i for i in group) for group in groups]
    K = [sum(1 << j for j in range(111) if i == j or dot(roots[i], roots[j]) == 0) for i in range(111)]
    W = basis(U+K)
    need(len(basis(U)) == 15 and len(basis(K)) == 9 and len(W) == 19, 'code ranks15/9/19')
    need(W[:15] == U, 'class-first quotient basis')
    quotients = [coordinates(k, W) >> 15 for k in K]
    by_class = [quotients[g[0]] for g in groups]
    need(set(by_class) == set(range(1, 16)), 'fifteen nonzero canonical quotient classes')
    need(all(quotients[i] == by_class[cls[i]] for i in range(111)), 'quotient constant exactly on class')
    all_inputs = (1 << 111)-1
    rows = []
    for i in range(111):
        contacts = K[i] ^ (1 << i)
        forbidden = all_inputs ^ contacts
        facet = s['frames'][str(s['final'][111+i])]
        need(facet['dim'] == 7 and real_rank(facet['B']) == 7, 'actual terminal facet rank')
        need(all(dot(roots[i], list(map(F, row))) == 0 for row in facet['B']), 'actual facet is root perpendicular')
        local = K[i] ^ U[cls[i]]
        need(local and local & forbidden == 0, 'actual nonzero local repair support')
        need(real_rank([roots[j] for j in range(111) if local >> j & 1]) == 7, 'local repair spans the entire actual facet')
        need(len(basis([u & forbidden for u in U])) == 15, 'class code has zero shortening at receiver')
        need(len(basis([w & forbidden for w in W])) == 18, 'U+C receiver shortening is exactly one dimension')
        c_dims = []
        for c in range(15):
            code = U + [K[groups[c][0]]]
            need(len(basis(code)) == 16, 'canonical one-direction extension dimension')
            d = 16-len(basis([v & forbidden for v in code]))
            need(d == int(cls[i] == c), 'all15 receiver-shortening gates')
            c_dims.append(d)
        rows.append({'receiver': i, 'class': cls[i], 'canonical_quotient': quotients[i],
                     'actual_facet': s['final'][111+i], 'forbidden_mask': hex(forbidden),
                     'local_repair_hex': hex(local), 'local_repair_support_rank': 7,
                     'U_forbidden_rank': 15, 'U_plus_C_forbidden_rank': 18,
                     'canonical_extension_shortening_dimensions': c_dims})
    subspaces = []
    for h in all_subspaces():
        hb = basis(sorted(h))
        lift = []
        for v in hb:
            row = 0
            for j in range(4):
                if v >> j & 1:
                    row ^= W[15+j]
            lift.append(row)
        code = U + lift
        d = len(hb)
        need(len(basis(code)) == 15+d, 'extension dimension')
        for i, record in enumerate(rows):
            forbidden = int(record['forbidden_mask'], 16)
            actual_d = 15+d-len(basis([v & forbidden for v in code]))
            need(actual_d == int(quotients[i] in h), 'all canonical-subcode shortenings')
        invisible = [c for c in range(15) if by_class[c] not in h]
        need(len(invisible) == 16-2**d, 'exact invisible-class count')
        subspaces.append({'dimension': d, 'vectors': sorted(h), 'basis': hb,
                          'invisible_classes': invisible, 'necessary_packet_count': len(invisible)})
    # Controls distinguish support from arbitrary chosen code dimension.
    need(all(int(r['local_repair_hex'], 16) & int(r['forbidden_mask'], 16) == 0 for r in rows), 'actual shortening witnesses')
    need(all((int(r['local_repair_hex'], 16) ^ (1 << r['receiver'])) & int(r['forbidden_mask'], 16)
             for r in rows), 'own-coordinate contamination rejected')
    result = {'status': 'PASS_EXACT_RECEIVER_DOWNSET_CANONICAL_EXTENSION_GATE',
              'native_sha256': PIN, 'partition_sha256': PARTITION,
              'U_basis_hex': [hex(x) for x in U], 'U_plus_C_basis_hex': [hex(x) for x in W],
              'canonical_quotient_by_class': by_class, 'receiver_rows': rows,
              'canonical_subspaces': subspaces,
              'packet_lower_bounds_by_added_canonical_dimension': {'0':15, '1':14, '2':12, '3':8, '4':0},
              'controls': {'contaminated_own_coordinate_rejected_for_all111': True,
                           'actual_one_dimensional_local_kernel_retained_in_own_class': True},
              'scope': 'Exact binary source premises. Universal chronological first-entry theorem and field/block quantifiers are in PROOF.md. No general q8 impossibility or complete kappa.'}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'CERTIFICATE.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': result['status'], 'receiver_rows': len(rows), 'canonical_subspaces': len(subspaces),
                      'one_direction_packet_floor':14, 'two_direction_packet_floor':12}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--partition', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
