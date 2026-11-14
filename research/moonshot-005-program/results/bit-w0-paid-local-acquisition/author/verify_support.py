#!/usr/bin/env python3
"""Exact support covers for the eight coordinate W0 local forms.

No author-checker imports. The universal subspace quantifier uses the
maximal-parabolic containment argument written in PROOF.md.
"""
import argparse
from collections import deque
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path

NATIVE_PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def line(v):
    v = tuple(v)
    need(any(v), 'nonzero line')
    return v if next(x for x in v if x) > 0 else tuple(-x for x in v)


def rref(rows, width=8):
    a = [[F(x) for x in row] for row in rows]
    need(all(len(row) == width for row in a), 'row width')
    pivots = []
    for c in range(width):
        p = len(pivots)
        k = next((k for k in range(p, len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[p], a[k] = a[k], a[p]
        q = a[p][c]
        a[p] = [x/q for x in a[p]]
        for k in range(len(a)):
            if k != p and a[k][c]:
                q = a[k][c]
                a[k] = [x-q*y for x, y in zip(a[k], a[p])]
        pivots.append(c)
    return tuple(tuple(row) for row in a[:len(pivots)])


def inverse(a):
    n = len(a)
    aug = [[F(x) for x in row] + [F(i == j) for j in range(n)]
           for i, row in enumerate(a)]
    for p in range(n):
        q = next((q for q in range(p, n) if aug[q][p]), None)
        need(q is not None, 'invertible simple-root basis')
        aug[p], aug[q] = aug[q], aug[p]
        q = aug[p][p]
        aug[p] = [x/q for x in aug[p]]
        for j in range(n):
            if j != p:
                q = aug[j][p]
                aug[j] = [x-q*y for x, y in zip(aug[j], aug[p])]
    return [row[n:] for row in aug]


def source(native_path):
    raw = native_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == NATIVE_PIN, 'native source pin')
    native = json.loads(gzip.decompress(raw))
    actual = []
    for i in range(111):
        r = tuple(F(x) for x in native['frames'][str(native['start'][i])]['B'][0])
        q = dot(r, r)
        need(q in (1, 4), 'source normalization')
        rr = tuple(x*(2 if q == 1 else 1) for x in r)
        need(all(x.denominator == 1 for x in rr), 'integral roots')
        actual.append(tuple(int(x) for x in rr))
    need(actual[:8] == [tuple(2*int(i == j) for j in range(8)) for i in range(8)],
         'actual coordinate indices')
    supports = sorted({tuple(j for j, x in enumerate(r) if x)
                       for r in actual if sum(x != 0 for x in r) == 4})
    need(len(supports) == 14, 'four-coordinate supports')
    full = set(actual[:8])
    for support in supports:
        for signs in itertools.product((-1, 1), repeat=3):
            r = [0]*8
            r[support[0]] = 1
            for j, sign in zip(support[1:], signs):
                r[j] = sign
            full.add(tuple(r))
    need(len(full) == 120 and set(actual) <= full, 'full root-line completion')
    return native, actual, full


def geometry(full):
    # Exact root-system premises. The universal chamber argument is in PROOF.
    need(all(dot(v, v) == 4 for v in full), 'equal real root norms')
    for u in full:
        for v in full:
            q = dot(u, v)
            need(q % 2 == 0 and line(tuple(y-q//2*x for x, y in zip(u, v))) in full,
                 'reflection closure')
    roots = sorted(v[1:] for v in full if v[0] == 0)
    need(len(roots) == 63, 'E7 line count')
    generic = tuple(3**j for j in range(7))
    need(all(dot(r, generic) for r in roots), 'regular orientation')
    positive = {r if dot(r, generic) > 0 else tuple(-x for x in r) for r in roots}
    sums = {tuple(x+y for x, y in zip(u, v)) for u in positive for v in positive}
    simple = sorted(positive-sums)
    need(len(simple) == 7 and len(rref(simple, 7)) == 7, 'simple-root basis')
    cartan = [[dot(u, v)//2 for v in simple] for u in simple]
    need(all(cartan[i][j] == 2 if i == j else cartan[i][j] in (0, -1)
             for i in range(7) for j in range(7)), 'simply-laced Cartan matrix')
    inv = inverse([list(x) for x in zip(*simple)])
    coefficients = []
    for r in roots:
        c = tuple(dot(row, r) for row in inv)
        need(all(x.denominator == 1 for x in c), 'integral simple coefficients')
        c = tuple(int(x) for x in c)
        need(all(x >= 0 for x in c) or all(x <= 0 for x in c), 'one-sign simple coefficients')
        coefficients.append(c)
    flats = {}
    orbit_sizes = []
    for k in range(7):
        start = tuple(int(j == k) for j in range(7))
        seen = {start}
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for j in range(7):
                w = line(tuple(v[i]-v[j]*cartan[j][i] for i in range(7)))
                if w not in seen:
                    seen.add(w)
                    queue.append(w)
        orbit_sizes.append(len(seen))
        for v in sorted(seen):
            mask = sum(1 << j for j, c in enumerate(coefficients) if dot(v, c) == 0)
            need(mask not in flats, 'distinct maximal-parabolic support masks')
            flats[mask] = {'node': k, 'normal_simple_pairings': v}
    need(orbit_sizes == [378, 5040, 63, 1008, 288, 2016, 28], 'complete normal orbits')
    need(len(flats) == 8821, 'complete maximal-parabolic count')
    return roots, simple, cartan, coefficients, flats


def best_pair(target, flats):
    # Keep all masks, including small and dominated ones. Bounds only skip
    # pairs whose sum of individual sizes cannot exceed an already seen union.
    restricted = {}
    for m in sorted(flats):
        restricted.setdefault(m & target, m)
    masks = sorted(restricted, key=lambda m: (-m.bit_count(), m))
    maximum = -1
    pair = None
    evaluated = 0
    for i, x in enumerate(masks):
        if x.bit_count()+masks[0].bit_count() <= maximum:
            break
        for y in masks[i:]:
            if x.bit_count()+y.bit_count() <= maximum:
                break
            evaluated += 1
            n = (x | y).bit_count()
            if n > maximum:
                maximum, pair = n, (restricted[x], restricted[y])
    need(pair is not None, 'nonempty pair search')
    return maximum, pair, masks[0].bit_count(), evaluated


def main(args):
    native, actual, full = source(args.native)
    roots, simple, cartan, coeffs, flats = geometry(full)
    # Coordinate xor translations preserve this exact completed root set;
    # this is verified, not inferred from the E8 name.
    results = []
    for p in range(8):
        moved = [line(tuple(r[j ^ p] for j in range(8))) for r in actual]
        need({line(tuple(r[j ^ p] for j in range(8))) for r in full} == full,
             'coordinate translation isometry')
        indices = [i for i, r in enumerate(moved) if i >= 8 and r[0] == 0]
        target = sum(1 << roots.index(moved[i][1:]) for i in indices)
        best, pair, single, evaluated = best_pair(target, flats)
        results.append({'coordinate': p, 'support_indices': indices,
                        'support_size': len(indices), 'target_mask': hex(target),
                        'max_one_proper_subspace': single,
                        'max_two_proper_subspaces': best,
                        'exact_pairs_evaluated_after_safe_cardinality_pruning': evaluated,
                        'sharp_pair': [dict(flats[m], full_mask=hex(m),
                                           selected_actual_indices=[i for i in indices if (m >> roots.index(moved[i][1:])) & 1])
                                       for m in pair]})
    need([x['support_size'] for x in results] == [49, 53, 53, 51, 51, 51, 51, 53], 'eight local forms')
    need([x['max_one_proper_subspace'] for x in results] == [30, 32, 32, 32, 31, 30, 31, 32], 'sharp one-flat maxima')
    need([x['max_two_proper_subspaces'] for x in results] == [44, 47, 47, 45, 45, 45, 45, 47], 'sharp two-flat maxima')
    full_target = sum(1 << i for i, r in enumerate(roots) if sum(x != 0 for x in r) == 4)
    full_best, full_pair, full_single, _ = best_pair(full_target, flats)
    need((full_target.bit_count(), full_single, full_best) == (56, 32, 48), 'full noncoordinate support bound')
    # Deterministic three-flat witness, selected by exact normal pairings.
    triple_normals = [(1, 0, 0, 0, 0, 0, -1), (0, 1, 0, 0, 0, -1, 0), (1, 0, -1, 0, 0, 0, -1)]
    triple_masks = [next(m for m, d in flats.items() if tuple(d['normal_simple_pairings']) == v and d['node'] == 6)
                    for v in triple_normals]
    target0 = int(results[0]['target_mask'], 16)
    union = 0
    for m in triple_masks:
        union |= m
    need(target0 & ~union == 0, 'three E6 flats cover l0')
    groups = []
    remaining = set(results[0]['support_indices'])
    for m in triple_masks:
        group = sorted(i for i in remaining if (m >> roots.index(actual[i][1:])) & 1)
        need(group, 'nonempty acquisition group')
        remaining.difference_update(group)
        basis = rref([[0] + list(r) for j, r in enumerate(roots) if (m >> j) & 1])
        need(len(basis) == 6, 'real E6 acquisition chart dimension')
        groups.append({'indices': group, 'carrier': group[0], 'normal': flats[m],
                       'full_mask': hex(m), 'chart_basis': [[str(x) for x in row] for row in basis]})
    need(not remaining, 'disjoint groups cover exact l0 support')
    need(all(len(g['indices']) > 1 for g in groups), 'nontrivial borrowed carriers')
    # The inherited coarser 52-root theorem cannot establish these 49-line
    # exclusions. Reject a proposed two-flat coverage by its missing columns.
    pair0 = results[0]['sharp_pair']
    covered = int(pair0[0]['full_mask'], 16) | int(pair0[1]['full_mask'], 16)
    missing = [i for i in results[0]['support_indices'] if not ((covered >> roots.index(actual[i][1:])) & 1)]
    need(len(missing) == 5, 'sharp pair misses five actual l0 inputs')
    result = {'status': 'PASS_EXACT_W0_LOCAL_ACQUISITION_SUPPORT_COVERS',
              'native_sha256': NATIVE_PIN, 'all_proper_real_subspaces': True,
              'universal_quantifier_dependency': 'closed Weyl chamber / maximal parabolic containment proof in PROOF.md; exact verified root-system premises',
              'simple_roots': simple, 'cartan': cartan, 'normal_orbit_sizes': [378, 5040, 63, 1008, 288, 2016, 28],
              'maximal_parabolic_root_sets': len(flats), 'coordinate_forms': results,
              'full_56_noncoordinate_root_max_one': full_single,
              'full_56_noncoordinate_root_max_two': full_best,
              'full_56_sharp_pair': [dict(flats[m], full_mask=hex(m)) for m in full_pair],
              'l0_three_arrival_groups': groups,
              'negative_control_sharp_two_flat_claim_missing_inputs': missing,
              'scope': 'Exact support bound and matching three-predecessor support decomposition. Physical word is separate. Nonlocal prior histories are excluded from the pre-Hub local-acquisition corollary. No complete source, supplier, or kappa.'}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'SUPPORT-CERTIFICATE.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': result['status'], 'support_sizes': [r['support_size'] for r in results],
                      'max_pairs': [r['max_two_proper_subspaces'] for r in results],
                      'groups': [g['indices'] for g in groups]}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
