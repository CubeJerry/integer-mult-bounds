#!/usr/bin/env python3
"""Small independent source and quotient checks; no author code imported."""
import argparse
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

NATIVE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
AUTHOR = '7d5aa1911bc7a76e36167906d548435372afbd895cffcc5778e84a80b9d584d4'
Y = 'd427cabd4770bdd787f8bf85e77640a16a0848264a6d9b74d4881f28e2a3cd56'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def span(rows):
    out = {0}
    for row in rows:
        out |= {x ^ row for x in out}
    return out


def main(args):
    native = args.repo / 'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
    need(digest(native) == NATIVE, 'native pin')
    author = args.workspace / 'worker-a/next/class-historical-closure'
    need(digest(author / 'MANIFEST.json') == AUTHOR, 'author manifest')
    for item in json.loads((author / 'MANIFEST.json').read_text())['files']:
        need(digest(author / item['path']) == item['sha256'], 'author artifact pin')
    need(digest(args.workspace / 'root-work/y-feedback-normalization/MANIFEST.json') == Y,
         'Y normalization manifest')
    data = json.loads(gzip.decompress(native.read_bytes()))
    roots = []
    for i in range(111):
        row = tuple(Fraction(x) for x in data['frames'][str(data['start'][i])]['B'][0])
        norm = sum(x*x for x in row)
        need(norm in (1, 4), 'root normalization')
        row = tuple(x * (2 if norm == 1 else 1) for x in row)
        roots.append(row)
        need(data['frames'][str(data['start'][111+i])]['dim'] == 0, 'Y birth')
    groups = json.loads((args.workspace / 'root-work/orthogonal-class-fitting/RESULT.json').read_text())['groups']
    need(sorted(x for g in groups for x in g) == list(range(111)), 'partition')
    need(len(groups) == 15, 'fifteen groups')
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    for g in groups:
        need(all(dot(roots[i], roots[j]) == 0 for i, j in itertools.combinations(g, 2)),
             'class orthogonality')
        need(all(dot(roots[i], roots[i]) == 4 for i in g), 'class Gram diagonal')
    full = [g for g in groups if len(g) == 8]
    need(len(full) == 9, 'nine full bases')
    endpoint_coordinates = []
    for g in full:
        i = g[0]
        facet = [tuple(Fraction(x) for x in row)
                 for row in data['frames'][str(data['final'][111+i])]['B']]
        need(len(facet) == 7 and all(dot(roots[i], row) == 0 for row in facet),
             'actual terminal facet')
        need(dot(roots[i], roots[i]) != 0, 'own source outside facet')
        # In each full basis at least one member is outside root_i perpendicular.
        need(all(any(dot(roots[i], roots[j]) != 0 for j in h) for h in full),
             'every full class has an outside-facet witness')
        endpoint_coordinates.append(i)

    # Finite analogue: two full class coordinates, one short coordinate;
    # nested local spaces omit at least one coordinate in each full class.
    # Quotient by the short class is essential to decomposition independence.
    U = span([0b00011, 0b01100, 0b10000])
    T = span([0b10000])
    LC = span([0b00001, 0b10000])
    LD = span([0b00001, 0b00100, 0b10000])
    maps = []
    for local in (LC, LD):
        need(U & local <= T, 'shortened intersection')
        pi = {}
        for u in U:
            quotient = ((u & 1) != 0) + 2 * ((u & 4) != 0)
            for ell in local:
                w = u ^ ell
                need(w not in pi or pi[w] == quotient, 'well-defined quotient')
                pi[w] = quotient
        need(all(pi[a ^ b] == pi[a] ^ pi[b] for a in pi for b in pi), 'linearity')
        maps.append(pi)
    need(all(maps[0][w] == maps[1][w] for w in maps[0]), 'either-direction MOVE')
    # This row genuinely contains a nonclass local remainder.
    w = 0b00011 ^ 0b00001
    need(w not in U and maps[0][w] == maps[1][w] == 1, 'nonclass packet control')
    need(0b10000 in U & LC and 0b10000 != 0, 'omitting T would be ambiguous')
    bad_local = span([0b00001, 0b00010])
    need(0b00011 in U & bad_local and 0b00011 not in T, 'missing full-basis premise control')
    result = {
        'status': 'PASS_INDEPENDENT_CLASS_HISTORICAL_CLOSURE_AND_Y_EXTENSION_REVIEW',
        'author_manifest_sha256': AUTHOR, 'native_sha256': NATIVE,
        'Y_normalization_manifest_sha256': Y,
        'source_classes': len(groups), 'full_real_bases': len(full),
        'class_sizes_sorted': sorted(map(len, groups)),
        'actual_endpoint_representatives': endpoint_coordinates,
        'proper_chart_full_class_intersection': 'Universal from nonzero orthogonal 8-root real bases',
        'quotient_control_space_sizes': list(map(len, maps)),
        'nonclass_MOVE_control': True, 'without_T_control': True,
        'missing_full_basis_premise_control': True,
        'scope': 'Exact specified class fitting and declared historical normalization; all fields and V. No arbitrary rank15 fitting, source construction, or supplier.',
        'X_projection_rank_must_exceed_15V_for_q8': True,
        'scalar_min_rank_Gx': 16, 'scalar_min_sum_kernel_nullity': 8,
        'general_V_min_rank_Gx': '15V+1', 'general_V_min_sum_kernel_nullity': '7V+1',
        'allV_16V_claimed': False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'full_bases': 9, 'quotient_controls': True}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: explicit guarded review mode')
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
