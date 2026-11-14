#!/usr/bin/env python3
"""Native reconstruction and exhaustive finite code-distance review."""
import argparse, collections, gzip, hashlib, json
from fractions import Fraction
from pathlib import Path

NATIVE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def need(value, message):
    if not value:
        raise ValueError(message)

def rank(rows):
    pivots = {}
    for x in rows:
        while x:
            top = x.bit_length() - 1
            if top in pivots:
                x ^= pivots[top]
            else:
                pivots[top] = x
                break
    return len(pivots)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == NATIVE, 'native pin')
    native = json.loads(gzip.decompress(raw))
    roots = [list(map(Fraction, native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
    K = [sum(int(i == j or sum(a*b for a, b in zip(x, y)) == 0) << j
             for j, y in enumerate(roots)) for i, x in enumerate(roots)]
    basis = []
    selected = []
    for i, row in enumerate(K):
        if rank(basis + [row]) > len(basis):
            basis.append(row)
            selected.append(i)
    need(selected == [0, 1, 2, 4, 8, 9, 14, 30, 59], 'independent canonical basis')
    words = [0]
    for row in basis:
        words += [x ^ row for x in words]
    need(len(set(words)) == 512, 'all canonical words')
    mask = (1 << 111) - 1
    census = collections.Counter()
    per_receiver = []
    witnesses = []
    for i, row in enumerate(K):
        forbidden = mask ^ row
        restricted = {x & forbidden for x in words}
        need(len(restricted) == 256 and rank([x & forbidden for x in basis]) == 8, 'forbidden restriction dimension')
        need({x for x in words if not x & forbidden} == {0, row}, 'exact canonical constraint kernel')
        distance = min(x.bit_count() for x in restricted if x)
        census[distance] += 1
        per_receiver.append(distance)
        if distance == 18:
            deletion = min(x for x in restricted if x.bit_count() == 18)
            remaining = forbidden & ~deletion
            need(rank([x & remaining for x in basis]) == 7, 'sharp18 deletion loses one constraint rank')
            # Every proper subset of this support of size17 still preserves rank8.
            for column in range(111):
                if deletion >> column & 1:
                    kept = remaining | (1 << column)
                    need(rank([x & kept for x in basis]) == 8, 'all17 subsets of sharp support retain rank')
            witnesses.append({'receiver': i, 'deletion_columns': [j for j in range(111) if deletion >> j & 1]})
    need(dict(census) == {18:7, 19:24, 20:52, 21:16, 22:11, 23:1}, 'exact distance census')
    degrees = [row.bit_count() - 1 for row in K]
    need(dict(collections.Counter(degrees)) == {55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}, 'native foreign degree census')
    ell_bounds = {str(s): 2*(111-s)-sum(d <= 52+s for d in degrees) for s in range(5)}
    need(list(ell_bounds.values()) == [222,220,218,215,202], 'uniform support lower bounds')
    # Legitimate correction rows at deleted indices are a necessary scope control.
    for i in range(111):
        localized = 1 << i
        need(not localized & (mask ^ K[i]), 'unit row still respects all forbidden positions')
        need(localized != K[i] and rank(basis + [localized]) == 10, 'coordinate innovation not canonical')
    larger_set = [0,1,2,3,4,9,30,8]
    larger_mask = sum(1 << j for j in larger_set)
    example = [(1 << i) if i in larger_set else row & ~larger_mask for i, row in enumerate(K)]
    example_ell = sum(int((row ^ (1 << i)).bit_count() > 36) + int((row ^ (1 << i)).bit_count() > 52)
                      for i, row in enumerate(example))
    need(rank(example) == 17 and example_ell == 183, 'eight-coordinate algebraic escape control')
    output = {'status': 'PASS_INDEPENDENT_NATIVE_COORDINATE_GATE', 'native_sha256': NATIVE,
              'author_code_imported_or_run': False, 'canonical_basis_indices': selected,
              'minimum_forbidden_distances': per_receiver, 'distance_census': dict(census),
              'foreign_degree_census': dict(collections.Counter(degrees)), 'ell_lower_bounds': ell_bounds,
              'sharp18_deletion_witnesses': witnesses, 'scope_control': 'rows inside S may be unit rows',
              'eight_coordinate_control': {'S':larger_set, 'fitting_rank':17, 'ell':example_ell,
                                          'physical_decoder_established':False},
              'reviewed_proof_sha256': hashlib.sha256((args.package/'PROOF.md').read_bytes()).hexdigest(),
              'classification': 'Exact source certificate plus separately reviewed all-subset/all-field/all-width proof. No new kappa.'}
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': output['status'], 'receivers':111, 'words':512, 'sharp_witnesses':len(witnesses)}))

if __name__ == '__main__':
    main()
