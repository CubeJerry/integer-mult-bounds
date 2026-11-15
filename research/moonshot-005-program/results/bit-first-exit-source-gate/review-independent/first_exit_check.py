#!/usr/bin/env python3
"""Independent all-64 orientation check for the singleton first-exit gate."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

SOURCE_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def need(value, label):
    if not value:
        raise ValueError(label)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def bits(indices):
    return sum(1 << i for i in indices)


def basis(rows):
    pivots = {}
    for row in rows:
        while row:
            lead = row.bit_length()-1
            if lead in pivots:
                row ^= pivots[lead]
            else:
                pivots[lead] = row
                break
    return list(pivots.values())


def check(path):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'source hash')
    roots = json.loads(raw)['native_roots']
    selected = [1, 3, 5, 10, 30, 61]
    frame = [0, 1, 2, 4, 8, 14, 30, 59]
    gram = [bits(k for k, j in enumerate(frame) if dot(roots[i], roots[j])//2 % 2) for i in frame]
    need(len(basis(gram)) == 8, 'binary coordinate frame')
    lookup = {tuple((row & x).bit_count()%2 for row in gram): x for x in range(256)}

    def coordinate(root):
        return lookup[tuple(dot(root, roots[j])//2 % 2 for j in frame)]

    masks = sorted({bits(i for i, x in enumerate(r) if x) for r in roots if sum(x != 0 for x in r) == 4})
    full = [[2 if i == j else 0 for i in range(8)] for j in range(8)]
    for mask in masks:
        indices = [i for i in range(8) if mask >> i & 1]
        for signs in range(8):
            row = [0]*8
            row[indices[0]] = 1
            for k in range(1, 4):
                row[indices[k]] = -1 if signs >> (k-1) & 1 else 1
            full.append(row)
    root_by_coordinate = {coordinate(root): root for root in full}
    need(len(root_by_coordinate) == 120, 'full completion')
    h = [(coordinate(root) & 189).bit_count()%2 for root in roots]
    choices = [[roots[i], root_by_coordinate[coordinate(roots[i]) ^ 38]] for i in selected]
    need(all(dot(left, right) == 0 for left, right in choices), 'orthogonal complementary normal pairs')
    need(all((coordinate(root) & 189).bit_count()%2 == 0 for pair in choices for root in pair), 'D8 normal classes')
    omitted_b = [0, 0, 1, 1, 0, 0, 1, -1]
    kb = bits(j for j, root in enumerate(roots) if dot(root, omitted_b) == 0)
    canonical = [bits(j for j, t in enumerate(roots) if i == j or dot(root, t) == 0) for i, root in enumerate(roots)]
    hmask = bits(j for j, value in enumerate(h) if value)
    seeds = [canonical[i] for i in [1, 3, 5, 10, 11, 15, 30]] + [canonical[0] & hmask]
    need(len(basis(seeds)) == 8, 'eight target seeds')
    records = []
    six_clear = []

    def witnesses(normals, mode_rows):
        result = []
        for j in range(111):
            demand = [k for k, row in enumerate(mode_rows) if row >> j & 1]
            if len(demand) < 2:
                continue
            common_originals = [i for i, root in enumerate(roots) if all(dot(root, normals[k]) == 0 for k in demand)]
            need(j in common_originals, 'demanded source lies in every acquisition facet')
            if common_originals == [j]:
                result.append({'source': j, 'demanded_facet_indices': demand, 'common_native_originals': common_originals})
        return result

    for orientation in range(64):
        normals = [choices[k][(orientation >> k) & 1] for k in range(6)]
        modes = [bits(j for j, root in enumerate(roots) if h[j] and dot(root, normal) == 0) for normal in normals]
        unflipped = [canonical[i] & hmask for i in selected]
        need(all(modes[k] == (unflipped[k] ^ hmask if orientation >> k & 1 else unflipped[k]) for k in range(6)), 'exact complementary mode identity')
        need(len(basis(seeds+modes+[kb])) == 15, 'orientation preserves the full target basis')
        six = witnesses(normals, modes)
        seven = witnesses(normals+[omitted_b], modes+[kb])
        if not six:
            six_clear.append(orientation)
        need(bool(seven), 'every full seven-mode orientation has a singleton-source gate')
        records.append({'orientation': orientation, 'six_normals': normals, 'six_mode_witnesses': six, 'seven_mode_witnesses': seven,
                        'full_seed_plus_mode_rank': 15})
    need(six_clear == [26, 28, 41, 47, 53], 'exact five six-mode exceptions')
    need(any(w['source'] == 6 and w['demanded_facet_indices'] == list(range(6)) for w in records[0]['six_mode_witnesses']), 'unflipped X6 singleton witness')
    return {'status': 'PASS_INDEPENDENT_SINGLETON_FIRST_EXIT_GEOMETRY', 'source_sha256': SOURCE_SHA,
            'selected_native_normals': selected, 'seventh_omitted_normal': omitted_b,
            'orientations_checked': 64, 'six_mode_orientations_with_witness': 59,
            'six_mode_orientations_without_witness': six_clear,
            'seven_mode_orientations_with_witness': 64,
            'seven_mode_witness_count_histogram': dict(Counter(len(record['seven_mode_witnesses']) for record in records)),
            'records': records,
            'scope': 'Fixed six complementary mode normals plus fixed omitted-normal K_b; original-X-only monotone preprocessing with stationary caches. No universal acquisition impossibility.',
            'new_complete_kappa': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(check(args.source), indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
