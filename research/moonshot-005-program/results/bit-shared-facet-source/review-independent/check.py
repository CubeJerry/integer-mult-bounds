#!/usr/bin/env python3
"""Independent rational-chart and 222-column replay. No author imports."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

SOURCE_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def need(value, message):
    if not value:
        raise ValueError(message)


def rref(rows):
    matrix = [[Fraction(x) for x in row] for row in rows]
    at = 0
    for column in range(8):
        pivot = next((j for j in range(at, len(matrix)) if matrix[j][column]), None)
        if pivot is None:
            continue
        matrix[at], matrix[pivot] = matrix[pivot], matrix[at]
        scale = matrix[at][column]
        matrix[at] = [x / scale for x in matrix[at]]
        for j in range(len(matrix)):
            if j != at and matrix[j][column]:
                coefficient = matrix[j][column]
                matrix[j] = [x - coefficient*y for x, y in zip(matrix[j], matrix[at])]
        at += 1
    return tuple(tuple(row) for row in matrix[:at])


def kernel(rows):
    matrix = rref(rows)
    pivots = [next(i for i, x in enumerate(row) if x) for row in matrix]
    result = []
    for free in range(8):
        if free not in pivots:
            vector = [Fraction(0)]*8
            vector[free] = 1
            for row, pivot in zip(matrix, pivots):
                vector[pivot] = -row[free]
            result.append(vector)
    return rref(result)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def bits(indices):
    return sum(1 << i for i in indices)


def rank2(rows):
    pivots = {}
    for row in rows:
        while row:
            lead = row.bit_length()-1
            if lead in pivots:
                row ^= pivots[lead]
            else:
                pivots[lead] = row
                break
    return len(pivots)


def nth_root(integer, exponent):
    estimate = 1 << ((integer.bit_length()+exponent-1)//exponent)
    while True:
        update = ((exponent-1)*estimate + integer//estimate**(exponent-1))//exponent
        if update >= estimate:
            break
        estimate = update
    while (estimate+1)**exponent <= integer:
        estimate += 1
    while estimate**exponent > integer:
        estimate -= 1
    return estimate


def price(profile):
    scale = 10**30
    lower = upper = 0
    for rank, count in profile.items():
        integer = rank**199 * scale**200
        root = nth_root(integer, 200)
        need(root**200 <= integer < (root+1)**200, 'exact price bracket')
        lower += count*root
        upper += count*(root if root**200 == integer else root+1)
    return {'scale': str(scale), 'lower_numerator': str(lower), 'upper_numerator': str(upper),
            'decimal_lower': f'{lower//scale}.{lower%scale:030d}',
            'decimal_upper': f'{upper//scale}.{upper%scale:030d}'}


def replay(word, roots):
    charts = {name: rref(spec['rows']) if spec['kind'] == 'span' else kernel(spec['rows'])
              for name, spec in word['charts'].items()}
    need(len(charts['Hub']) == 8 and not charts['zero'], 'Hub/ground identity')
    for i, root in enumerate(roots):
        need(charts[f'L{i}'] == rref([root]), 'source line identity')
        need(charts[f'F{i}'] == kernel([root]), 'receiver facet identity')
    cache = {}

    def contains(outer, inner):
        if (outer, inner) not in cache:
            cache[outer, inner] = len(rref(charts[outer]+charts[inner])) == len(charts[outer])
        return cache[outer, inner]

    omitted = [0, 0, 1, 1, 0, 0, 1, -1]
    h = [((dot(roots[72], root)+dot(omitted, root))//2)%2 for root in roots]
    facets, donors = word['facets'], word['donors']
    need(len(set(facets)) == len(set(donors)) == 2, 'distinct branch facets and donors')
    need(all(not h[i] for i in facets+donors), 'class-zero branches/carriers')
    modes = [{j for j, root in enumerate(roots) if h[j] and dot(roots[i], root) == 0} for i in facets]
    shared = modes[0] & modes[1]
    need(all(dot(roots[d], roots[i]) == 0 for d in donors for i in facets), 'donors in actual common chart')
    need(charts['D'] == kernel([roots[i] for i in facets]), 'common chart identity')
    need(charts['Fa'] == charts[f'F{facets[0]}'] and charts['Fb'] == charts[f'F{facets[1]}'], 'branch chart identities')
    if word['seed_kind'] == 'zero':
        seeds = [set(), set()]
    elif word['seed_kind'] == 'canonical':
        seeds = [{j for j, root in enumerate(roots) if j == i or dot(roots[i], root) == 0} for i in facets]
    else:
        raise ValueError('unknown seed interface')
    moved = sorted(set.union(*modes, *seeds) | set(donors))
    need(word['moved_original_sources'] == moved, 'exact moved-source set')
    expected_owned = {f'R{j}': (f'L{j}', 1 << j) for j in moved}
    expected_owned.update({'Z': ('D', bits(shared)),
                           'Ca': ('Fa', bits(modes[0]) ^ (1 << donors[0])),
                           'Cb': ('Fb', bits(modes[1]) ^ (1 << donors[1])),
                           'Pa': ('zero', bits(seeds[0] ^ modes[0])),
                           'Pb': ('zero', bits(seeds[1] ^ modes[1]))})
    records = {f'X{i}': [f'L{i}', 1 << i, False] for i in range(111)}
    records.update({f'Y{i}': ['zero', 1 << (111+i), False] for i in range(111)})
    counts, profile = Counter(), Counter()
    paths = {'Pa': [], 'Pb': []}
    peak = dirty = 0
    handoff_verified = False
    all_x = (1 << 111)-1
    hmask = bits(i for i, value in enumerate(h) if value)
    canonical = [bits(j for j, t in enumerate(roots) if i == j or dot(root, t) == 0) for i, root in enumerate(roots)]
    wrows = [row & (hmask if h[i] else all_x ^ hmask) for i, row in enumerate(canonical)]
    history, outside = [], []

    def handoff():
        live = {name: (record[0], record[1]) for name, record in records.items() if record[2]}
        need(live == expected_owned, 'independently derived complete handoff')
        for i in range(111):
            need(records[f'X{i}'][:2] == ['Hub' if i in moved else f'L{i}', 1 << i], f'restored original X{i}')
            need(records[f'Y{i}'][:2] == ['zero', 1 << (111+i)], f'unchanged original Y{i}')

    for step, operation in enumerate(word['operations'], 1):
        kind, name, *arguments = operation
        counts[kind] += 1
        if kind == 'INIT':
            need(name not in records and arguments[0] in charts, 'fresh zero INIT')
            records[name] = [arguments[0], 0, True]
            peak = max(peak, sum(record[2] for record in records.values()))
            if name in paths:
                need(not paths[name], 'one continuous packet lifetime')
                paths[name].append(len(charts[arguments[0]]))
                for i in moved:
                    need(records[f'X{i}'][:2] == ['Hub', 1 << i], 'original restoration precedes packet birth')
        elif kind == 'ADD':
            target = arguments[0]
            need(name in records and target in records and name != target, 'live distinct ADD roles')
            need(charts[records[name][0]] == charts[records[target][0]], f'cochart ADD at {step}')
            records[target][1] ^= records[name][1]
        elif kind == 'MOVE':
            need(name in records and arguments[0] in charts, 'live MOVE role/chart')
            old, value, owned = records[name]
            new = arguments[0]
            need(contains(old, new) if owned else contains(new, old), f'monotone nested MOVE at {step}')
            delta = abs(len(charts[new])-len(charts[old]))
            need(delta > 0, 'positive-rank MOVE')
            profile[delta] += 1
            records[name][0] = new
            if name in paths:
                paths[name].append(len(charts[new]))
        elif kind == 'CLEAR':
            if not handoff_verified:
                handoff()
                handoff_verified = True
            need(name in records and records[name][2], 'owned CLEAR')
            dirty += bool(records[name][1])
            del records[name]
        else:
            raise ValueError('unknown operation')
        for packet in paths:
            if packet in records and records[packet][0] != 'Hub':
                row = records[packet][1] & all_x
                history.append(row)
                if rank2(wrows+[row]) > 15 and len(outside) < 6:
                    outside.append({'operation': step, 'packet': packet, 'chart': records[packet][0], 'X_row_hex': hex(row)})
    if not handoff_verified:
        handoff()
    for packet in paths:
        need(paths[packet] == [8, 7, 1, 0], 'packet path 8->7->1->0')
    for i in range(111):
        need(records[f'X{i}'][1] == 1 << i, 'all final X restored')
        need(records[f'Y{i}'][1] == 1 << (111+i), 'all final unserved Y unchanged')
        if word['closed_partial']:
            need(records[f'X{i}'][0] == 'Hub' and charts[records[f'Y{i}'][0]] == charts[f'F{i}'], 'closed original endpoint charts')
    owners = sum(record[2] for record in records.values())
    need(owners == (0 if word['closed_partial'] else len(expected_owned)), 'complete owner accounting')
    history_rank, joint_rank = rank2(history), rank2(wrows+history)
    need(joint_rank == 17, 'two actual outside-W historical directions')
    return {'status': 'PASS_INDEPENDENT_MASKED_FACET_REPLAY', 'facets': facets, 'donors': donors,
            'seed_kind': word['seed_kind'], 'closed_partial': word['closed_partial'],
            'source_supports': {'modes': [len(mode) for mode in modes], 'common': len(shared), 'moved_originals': len(moved)},
            'operations': dict(sorted(counts.items())), 'movement_profile': dict(sorted(profile.items())),
            'movement_rank_length': sum(rank*count for rank, count in profile.items()),
            'movement_moment_199_over_200': price(profile), 'packet_paths': paths,
            'owned_peak': peak, 'owned_remaining': owners, 'dirty_clears_under_retained_contract': dirty,
            'carried_X_history_rank': history_rank, 'history_plus_W_rank': joint_rank,
            'outside_W_dimension': joint_rank-15, 'history_intersection_W_dimension': history_rank+15-joint_rank,
            'outside_W_examples': outside, 'all_222_columns_replayed': True,
            'all_111_X_restored': True, 'all_111_Y_unchanged': True,
            'completed_target_count': 0, 'new_complete_kappa': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--live', type=Path, required=True)
    parser.add_argument('--closed', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.read_bytes()
    need(hashlib.sha256(source).hexdigest() == SOURCE_SHA, 'pinned geometry bytes')
    roots = json.loads(source)['native_roots']
    live, closed = json.loads(args.live.read_text()), json.loads(args.closed.read_text())
    result = {'status': 'PASS_INDEPENDENT_SHARED_FACET_SOURCE_REVIEW', 'author_code_imported': False,
              'source_sha256': SOURCE_SHA, 'live_word_sha256': hashlib.sha256(args.live.read_bytes()).hexdigest(),
              'closed_word_sha256': hashlib.sha256(args.closed.read_bytes()).hexdigest(),
              'live': replay(live, roots), 'closed': replay(closed, roots), 'negative_controls': {}, 'new_complete_kappa': False}

    def reject(label, predicate, replacement=None):
        candidate = copy.deepcopy(live)
        index = next(i for i, operation in enumerate(candidate['operations']) if predicate(operation))
        if replacement is None:
            del candidate['operations'][index]
        else:
            candidate['operations'][index] = replacement(candidate['operations'][index])
        try:
            replay(candidate, roots)
        except (ValueError, KeyError) as error:
            result['negative_controls'][label] = {'rejected': True, 'reason': str(error)}
        else:
            raise ValueError('mutation passed: '+label)

    first_common, donor = min(live['source_sets']['common']), live['donors'][0]
    reject('omit_shared_capture', lambda op: op == ['ADD', f'X{first_common}', 'Z'])
    reject('omit_Hub_original_restoration', lambda op: op == ['ADD', f'X{first_common}', f'X{donor}'])
    reject('read_departed_donor_original', lambda op: op == ['ADD', f'R{donor}', 'Pa'], lambda op: ['ADD', f'X{donor}', 'Pa'])
    reject('omit_mask_cancellation', lambda op: op == ['ADD', f'R{donor}', 'Pa'])
    reject('omit_mask_correction_line_visit', lambda op: op == ['MOVE', 'Pa', f'L{donor}'])
    reject('erase_shared_bank_before_second_donor', lambda op: op == ['ADD', 'Z', f"X{live['donors'][1]}"], lambda op: ['CLEAR', 'Z'])
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
