#!/usr/bin/env python3
"""Enumerate native four-isolate/Petersen witnesses on the 95 remaining roles."""
import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

BASE = Path('research/moonshot-005-program')
ROOT_TABLE = BASE / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
REMOVED = {14, 17, 19, 20, 96, 99, 101, 102}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def members(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def later(mask, role):
    return mask >> (role + 1) << (role + 1)


def petersen_labels(roles, neighbours):
    """The five independent four-sets of KG(5,2) are its five stars."""
    stars = [set(group) for group in combinations(roles, 4)
             if all(not (neighbours[i] >> j & 1) for i, j in combinations(group, 2))]
    if len(stars) != 5:
        return None
    labels = [tuple(k for k, star in enumerate(stars) if i in star) for i in roles]
    if set(labels) != set(combinations(range(5), 2)):
        return None
    for a, i in enumerate(roles):
        for b, j in enumerate(roles):
            if bool(neighbours[i] >> j & 1) != set(labels[a]).isdisjoint(labels[b]):
                return None
    return labels


def enumerate_witnesses(roots):
    roles = [i for i in range(8, 111) if i not in REMOVED]
    all_roles = sum(1 << i for i in roles)
    neighbours = {i: sum(1 << j for j in roles if j != i and
                          sum(a * b for a, b in zip(roots[i], roots[j])) == 0) for i in roles}
    apart = {i: all_roles ^ neighbours[i] ^ (1 << i) for i in roles}
    sizes = Counter()
    witnesses = []
    for i in roles:
        for j in members(later(apart[i], i)):
            ij = apart[i] & apart[j]
            for k in members(later(ij, j)):
                ijk = ij & apart[k]
                for ell in members(later(ijk, k)):
                    core = ijk & apart[ell]
                    sizes[core.bit_count()] += 1
                    if core.bit_count() != 10:
                        continue
                    points = list(members(core))
                    labels = petersen_labels(points, neighbours)
                    require(labels is not None, 'ten common roles did not form the Petersen graph')
                    witnesses.append({'isolates': [i, j, k, ell], 'petersen': points, 'pair_labels': labels})
    require(sum(sizes.values()) == 43492 and max(sizes) == 10, 'independent four-set census')
    require(len(witnesses) == 838, 'Petersen witness count')
    sets = [tuple(sorted(w['isolates'] + w['petersen'])) for w in witnesses]
    require(len(set(sets)) == len(sets), 'duplicate witness role set')
    frequencies = Counter(i for group in sets for i in group)
    require(set(frequencies) == set(roles), 'witness family does not cover U')
    return roles, witnesses, sizes, frequencies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--flat-input', type=Path, help='optional exact flat-search input')
    args = parser.parse_args()
    raw = (args.repo / ROOT_TABLE).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == ROOT_SHA, 'wrong native roots')
    roots = json.loads(raw)['native_roots']
    roles, witnesses, sizes, frequencies = enumerate_witnesses(roots)
    masks = [' '.join(map(str, w['isolates'] + w['petersen'])) for w in witnesses]
    result = {'native_sha256': ROOT_SHA, 'remaining_roles': roles, 'independent_four_sets': sum(sizes.values()),
              'common_noncontacts_by_size': dict(sorted(sizes.items())), 'witness_count': len(witnesses),
              'ordered_witness_role_list_sha256': hashlib.sha256(('\n'.join(masks) + '\n').encode()).hexdigest(),
              'witness_frequency_by_role': dict(sorted(frequencies.items())), 'one_witness': witnesses[0],
              'downset_records': '9b', 'private_plus_downset_records': '17b'}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    if args.flat_input:
        args.flat_input.write_text('\n'.join([' '.join(map(str, roles)),
            *(' '.join(map(str, roots[i])) for i in roles), str(len(witnesses)), *masks]) + '\n')
    print(f'{len(witnesses)} certified Petersen-plus-four witnesses on {len(roles)} roles')


if __name__ == '__main__':
    main()
