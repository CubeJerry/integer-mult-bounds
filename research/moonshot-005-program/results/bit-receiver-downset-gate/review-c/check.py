#!/usr/bin/env python3
"""Independent native reconstruction of all class-extension locality kernels."""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rref_bits(rows):
    basis = {}
    for row in rows:
        while row:
            p = row.bit_length()-1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p] = row
                break
    return basis


def in_span(row, basis):
    while row:
        p = row.bit_length()-1
        if p not in basis:
            return False
        row ^= basis[p]
    return True


def verify(raw):
    require(hashlib.sha256(raw).hexdigest() == PIN, 'source pin')
    src = json.loads(gzip.decompress(raw))
    frames = {int(k): v for k, v in src['frames'].items()}
    roots = [list(map(F, frames[src['start'][i]]['B'][0])) for i in range(111)]
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    groups = {}
    for i, root in enumerate(roots):
        support = tuple(j for j, x in enumerate(root) if x)
        require(len(support) in (1, 4), 'native root shape')
        sign = 1 if root[support[0]] > 0 else -1
        parity = sum(x*sign < 0 for x in root) % 2
        complement = tuple(j for j in range(8) if j not in support)
        key = ('coordinate', 0) if len(support) == 1 else (min(support, complement), parity)
        groups.setdefault(key, []).append(i)
        facet = frames[src['final'][111+i]]
        require(facet['dim'] == 7 and all(dot(root, list(map(F, b))) == 0 for b in facet['B']), 'actual facet')
    classes = list(groups.values())
    require(len(classes) == 15, 'fifteen parity/complement classes')
    for group in classes:
        require(all(dot(roots[i], roots[j]) == 0 for i in group for j in group if i != j), 'class orthogonality')
    owner = {i: c for c, group in enumerate(classes) for i in group}
    k = [sum(int(i == j or dot(a, b) == 0) << j for j, b in enumerate(roots))
         for i, a in enumerate(roots)]
    u = [sum(1 << i for i in group) for group in classes]
    require(len(rref_bits(u)) == 15, 'class independence')
    all_columns = (1 << 111)-1
    checks = []
    for c, group in enumerate(classes):
        w = u + [k[group[0]]]
        basis = rref_bits(w)
        require(len(basis) == 16, 'class canonical extension dimension')
        nullities = []
        for j in range(111):
            local_mask = k[j] ^ (1 << j)
            forbidden = all_columns ^ local_mask
            nullity = 16-len(rref_bits([row & forbidden for row in w]))
            require(nullity == int(owner[j] == c), 'exact local intersection dimension')
            if owner[j] == c:
                ell = k[j] ^ u[c]
                require(ell != 0 and ell & forbidden == 0 and in_span(ell, basis), 'one-dimensional local generator')
            else:
                require(((1 << j) ^ u[owner[j]]) & forbidden == 0, 'target class projection remainder local')
            nullities.append(nullity)
        checks.append({'class_by_minimum_member': min(group), 'members': group,
                       'dimension': 16, 'local_intersection_dimensions_by_port': nullities,
                       'independent_required_classes_outside': 14})
    # A zero-local-intersection premise is load-bearing: each own class has
    # an actual nonzero local vector, so the forbidden downset may not include it.
    require(any(value for row in checks for value in row['local_intersection_dimensions_by_port']), 'own-class counterpremise present')
    return {'classes': classes, 'nullity_tests': len(checks)*111, 'extensions': checks,
            'class_index_convention': 'order of first actual port, may differ from predecessor numbering',
            'universal_scope': 'binary matrices transfer to every characteristic-two field; tensor width by proof'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--native', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    data = verify(args.native.read_bytes())
    try:
        verify(args.native.read_bytes()+b'x')
    except ValueError:
        pass
    else:
        raise ValueError('source corruption accepted')
    result = {'status': 'PASS_INDEPENDENT_CLASS_EXTENSION_LOCALITY', 'native_sha256': PIN,
              'source_reconstruction': data, 'source_byte_control': 'rejected',
              'author_checker_imported': False, 'proof_review': 'REVIEW.md', 'new_kappa': None}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'locality_nullities': data['nullity_tests'],
                      'candidate_spaces': 15, 'required_packet_lower_bound': 14}))


if __name__ == '__main__':
    main()
