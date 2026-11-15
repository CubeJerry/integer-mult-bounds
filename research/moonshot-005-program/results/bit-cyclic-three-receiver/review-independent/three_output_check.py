#!/usr/bin/env python3
"""Independent all-column replay of the eight-packet, three-output source."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

from check import SOURCE_SHA, bits, dot, kernel, need, price, rank2, rref
from eight_check import binary_basis


def replay(word, roots):
    charts = {name: rref(spec['rows']) if spec['kind'] == 'span' else kernel(spec['rows'])
              for name, spec in word['charts'].items()}
    for j, root in enumerate(roots):
        need(charts[f'L{j}'] == rref([root]), 'native source line')
        need(charts[f'F{j}'] == kernel([root]), 'native receiver facet')
    facets, donors = [1, 3, 5], [7, 15, 16]
    need(word['facets'] == facets and word['donors'] == donors, 'preferred literal source')
    need(len(charts['Hub']) == 8 and not charts['zero'], 'Hub and ground charts')
    need(charts['D'] == kernel([roots[i] for i in facets]), 'actual triple intersection')
    for i in range(3):
        need(charts[f'T{i}'] == charts[f'F{facets[i]}'], 'packet facet chart')
        need(charts[f'E{i}'] == kernel([roots[facets[i]], roots[facets[(i+1)%3]]]), 'actual pair intersection')
    omitted = [0, 0, 1, 1, 0, 0, 1, -1]
    h = [((dot(roots[72], r)+dot(omitted, r))//2) % 2 for r in roots]
    groups = [{k: set() for k in range(1, 8)} for _ in range(2)]
    for j, root in enumerate(roots):
        signature = sum((dot(root, roots[f]) == 0) << i for i, f in enumerate(facets))
        if signature:
            groups[h[j]][signature].add(j)
    d8, spinor = groups
    need(set(donors) <= d8[7], 'old donor masks are D8 triple-group inputs')
    all_x = (1 << 111)-1
    hmask = bits(j for j, value in enumerate(h) if value)
    canonical = [bits(j for j, other in enumerate(roots) if i == j or dot(root, other) == 0)
                 for i, root in enumerate(roots)]
    split = [row & (hmask if h[i] else all_x ^ hmask) for i, row in enumerate(canonical)]
    seeds = [canonical[i] for i in [1, 3, 5, 10, 11, 15, 30]] + [canonical[0] & hmask]
    expected = {f'R{j}': (f'L{j}', 1 << j) for j in range(111)}
    expected.update({'Zt': ('D', bits(spinor[7])), 'DT': ('D', bits(d8[7]))})
    pairs = [3, 6, 5]
    for i in range(3):
        incoming = (i-1) % 3
        expected[f'Z{i}'] = (f'E{i}', bits(spinor[pairs[i]]))
        expected[f'M{i}'] = ('D', 1 << donors[incoming])
        expected[f'C{i}'] = (f'T{i}', bits(spinor[1 << i]) ^ bits(spinor[pairs[incoming]]) ^ (1 << donors[incoming]))
        expected[f'DZ{i}'] = (f'E{i}', bits(d8[pairs[i]]))
        expected[f'DC{i}'] = (f'F{facets[i]}', bits(d8[1 << i]) ^ bits(d8[pairs[incoming]]))
    for i, seed in enumerate(seeds):
        expected[f'P{i}'] = ('zero', split[facets[i]] if i < 3 else seed)
    records = {f'X{j}': [f'L{j}', 1 << j, False] for j in range(111)}
    records.update({f'Y{j}': ['zero', 1 << (111+j), False] for j in range(111)})
    counts, profile = Counter(), Counter()
    packet_paths = {f'P{i}': [] for i in range(8)}
    y_paths = {f'Y{j}': [0] for j in range(111)}
    history = []
    peak = dirty = 0
    checked_handoff = False
    inclusion = {}

    def contains(outer, inner):
        if (outer, inner) not in inclusion:
            inclusion[outer, inner] = len(rref(charts[outer]+charts[inner])) == len(charts[outer])
        return inclusion[outer, inner]

    def handoff():
        actual = {name: (rec[0], rec[1]) for name, rec in records.items() if rec[2]}
        need(actual == expected, 'independently derived complete owned handoff')
        for j in range(111):
            need(records[f'X{j}'][:2] == ['Hub', 1 << j], 'restored original X handoff')
            target = (1 << (111+j)) ^ ((1 << j) if j in facets else 0)
            chart = f'F{j}' if j in facets else 'zero'
            need(records[f'Y{j}'][:2] == [chart, target], 'three exact Y targets; all other Y unchanged')

    for step, operation in enumerate(word['operations'], 1):
        kind, name, *arguments = operation
        counts[kind] += 1
        if kind == 'INIT':
            need(name not in records and arguments[0] in charts, 'fresh owned birth')
            records[name] = [arguments[0], 0, True]
            peak = max(peak, sum(rec[2] for rec in records.values()))
            if name in packet_paths:
                need(not packet_paths[name], 'one continuous packet lifetime')
                packet_paths[name].append(len(charts[arguments[0]]))
                for j in range(111):
                    need(records[f'X{j}'][:2] == ['Hub', 1 << j], 'all sources restored before every packet birth')
        elif kind == 'ADD':
            target = arguments[0]
            need(name in records and target in records and name != target, 'live distinct ADD roles')
            need(charts[records[name][0]] == charts[records[target][0]], f'literal cochart read at operation {step}')
            records[target][1] ^= records[name][1]
        elif kind == 'MOVE':
            need(name in records and arguments[0] in charts, 'live MOVE role and chart')
            old, value, owned = records[name]
            new = arguments[0]
            need(contains(old, new) if owned else contains(new, old), f'monotone nested MOVE at operation {step}')
            delta = abs(len(charts[old])-len(charts[new]))
            need(delta > 0, 'positive movement rank')
            profile[delta] += 1
            records[name][0] = new
            if name in packet_paths:
                packet_paths[name].append(len(charts[new]))
            if name in y_paths:
                y_paths[name].append(len(charts[new]))
        elif kind == 'CLEAR':
            if not checked_handoff:
                handoff()
                checked_handoff = True
            need(name in records and records[name][2], 'owned erasure only')
            dirty += bool(records[name][1])
            del records[name]
        else:
            raise ValueError('unknown operation')
        for packet in packet_paths:
            if packet in records and records[packet][0] != 'Hub':
                history.append(records[packet][1] & all_x)
    if not checked_handoff:
        handoff()
    for i in range(8):
        need(packet_paths[f'P{i}'] == ([8, 7, 6, 5, 0] if i < 3 else [8, 0]), 'eight packet routes')
    for j in range(111):
        need(records[f'X{j}'][:2] == ['Hub', 1 << j], 'restored final X')
        target = (1 << (111+j)) ^ ((1 << j) if j in facets else 0)
        need(records[f'Y{j}'][1] == target, 'all 222 final coefficient columns')
        expected_path = [0, 5, 6, 7] if j in facets else ([0, 7] if word['closed_partial'] else [0])
        need(y_paths[f'Y{j}'] == expected_path, 'literal receiver path')
        final = f'F{j}' if j in facets or word['closed_partial'] else 'zero'
        need(records[f'Y{j}'][0] == final, 'exact final receiver chart')
    live = sum(rec[2] for rec in records.values())
    need(live == (0 if word['closed_partial'] else 136), 'all live owners accounted')
    if word['closed_partial']:
        old = Counter({1:41, 2:21, 3:8, 4:11, 5:24, 6:23, 7:167, 8:5})
        old.update(Counter({1:34, 2:22, 3:2, 4:2, 5:28, 6:22, 7:-52}))
        need(dict(profile) == dict(old), 'independent split-path movement profile')
    rh, rjoint = rank2(history), rank2(history+split)
    need((rh, rjoint) == (18, 22), 'unchanged actual packet history and W trace')
    return {'status': 'PASS_INDEPENDENT_THREE_OUTPUT_SOURCE', 'all_222_columns_replayed': True,
            'completed_targets': facets, 'remaining_unserved_targets': 108,
            'closed_partial': word['closed_partial'], 'operations': dict(sorted(counts.items())),
            'movement_profile': dict(sorted(profile.items())),
            'rank_length': sum(rank*count for rank, count in profile.items()), 'moment': price(profile),
            'peak_owned': peak, 'live_owned': live, 'dirty_clears_under_retained_contract': dirty,
            'all_original_X_restored_before_packet_birth': True, 'other_108_Y_unchanged': True,
            'packet_paths': packet_paths, 'served_Y_paths': {f'Y{j}':y_paths[f'Y{j}'] for j in facets},
            'history_rank': rh, 'history_W_intersection': rh+15-rjoint, 'outside_W_dimension': rjoint-15,
            'D8_incidence_counts': {str(k):len(v) for k,v in d8.items()},
            'history_basis': [hex(row) for row in binary_basis(history)], 'new_complete_kappa': False}


def negative_controls(base, roots):
    tests = {}
    mutations = {
        'remove_reused_mask': lambda op: op == ['ADD', 'M0', 'DT'],
        'remove_D8_pair_read': lambda op: op == ['ADD', 'DZ0', 'Y1'],
        'remove_D8_facet_read': lambda op: op == ['ADD', 'DC0', 'Y1'],
        'remove_D8_triple_read': lambda op: op == ['ADD', 'DT', 'Y1'],
        'remove_ground_packet_read': lambda op: op == ['ADD', 'P0', 'Y1'],
        'remove_D8_pair_cache_deposit': lambda op: op == ['ADD', 'X5', 'DZ0'],
        'remove_D8_pair_carrier_restoration': lambda op: op == ['ADD', 'X38', 'X5'],
    }
    for label, select in mutations.items():
        word = copy.deepcopy(base)
        index = next(i for i, op in enumerate(word['operations']) if select(op))
        del word['operations'][index]
        try:
            replay(word, roots)
        except (ValueError, KeyError) as error:
            tests[label] = {'rejected': True, 'reason': str(error)}
        else:
            raise ValueError('independent checker accepted semantic mutant '+label)
    word = copy.deepcopy(base)
    index = next(i for i, op in enumerate(word['operations']) if op == ['MOVE', 'Y1', 'D'])
    word['operations'][index][-1] = 'F1'
    try:
        replay(word, roots)
    except (ValueError, KeyError) as error:
        tests['skip_required_receiver_meeting'] = {'rejected': True, 'reason': str(error)}
    else:
        raise ValueError('independent checker accepted unavailable receiver read')
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--words', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'source SHA256 pin')
    roots = json.loads(raw)['native_roots']
    names = ['WORD.json', 'CLOSED-WORD.json']
    words = {name:json.loads((args.words/name).read_text()) for name in names}
    result = {'status': 'PASS_INDEPENDENT_EIGHT_PACKET_THREE_OUTPUT_REVIEW',
              'source_sha256': SOURCE_SHA, 'author_code_imported': False,
              'word_sha256': {name:hashlib.sha256((args.words/name).read_bytes()).hexdigest() for name in names},
              'variants': {name:replay(word, roots) for name, word in words.items()},
              'negative_controls': negative_controls(words['WORD.json'], roots),
              'new_complete_kappa': False}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
