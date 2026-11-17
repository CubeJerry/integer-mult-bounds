#!/usr/bin/env python3
"""Independent all888-column replay and chronological source comparison."""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

P = Path('research/moonshot-005-program')
NATIVE = P / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
GEOMETRY = P / 'sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py'
LOCAL = P / 'results/bit-shared-facet-mds/author/four-chart-word/WORD.json'
PINS = {
    'native': '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
    'geometry': '41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
    'local': '831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa',
    'word': '59da0681e8267a07358c3015b587c57d0ea4976d91bed795dd74c5c2c92c2f5f',
    'author_proof': 'b5a1f6d9dc6fdad0ec08383dc0bed7b8e3c73f07bab7d5c4795975f89e88a3f8',
    'author_builder': '04a658cd9d7ca51ff3ee652106483583ac902f9ae2e1cd9a9e39e2130b5e9e26',
    'author_lifetimes': '61ee3f0bc2da444cf507de5d431cc3977626b616100373a25f442a001e4dd6b6',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_pinned(path, key):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == PINS[key], 'authenticated ' + key)
    return json.loads(raw)


def binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            k = row.bit_length() - 1
            if k in pivots:
                row ^= pivots[k]
            else:
                pivots[k] = row
                break
    return len(pivots)


def interval(iv):
    with localcontext() as ctx:
        ctx.prec = 60
        return {'rational': [str(x) for x in iv],
                'decimal': [str(Decimal(x.numerator) / Decimal(x.denominator)) for x in iv]}


def replay(word, roots, geo, target_complete, omit=None):
    charts = {name: geo.chart(spec) for name, spec in word['charts'].items()}
    for i, row in enumerate(roots):
        need(charts[f'L{i}'] == geo.basis((tuple(row),)), 'actual native line')
        need(charts[f'F{i}'] == geo.kernel((tuple(row),)), 'actual native facet')
    for c, other in enumerate([76, 81, 91, 96]):
        need(charts[f'C{c}'] == geo.kernel((tuple(roots[3]), tuple(roots[other]))), 'actual shared facet intersection')
        need(len(charts[f'C{c}']) == 6, 'rank-six proper source chart')
    xnames = {f'X{i}_{c}': (i, c) for i in range(111) for c in range(4)}
    ynames = {f'Y{i}_{c}': (i, c) for i in range(111) for c in range(4)}
    initial = {name: 1 << (4*i+c) for name, (i, c) in xnames.items()}
    initial.update({name: 1 << (444+4*i+c) for name, (i, c) in ynames.items()})
    values = initial.copy()
    locations = {name: f'L{i}' for name, (i, _) in xnames.items()}
    locations.update({name: 'zero' for name in ynames})
    owned, ever_born = set(), set()
    counts, movement, directions = Counter(), Counter(), Counter()
    snapshots, cross_reads, captures, cache_reads, lives = {}, [], [], [], {}
    x_subsequence, y_subsequence = [], []
    xx_prefix, dirty, peak = 0, 0, 0
    K = [sum(1 << j for j in range(111) if i == j or sum(a*b for a, b in zip(roots[i], roots[j])) == 0)
         for i in range(111)]
    for step, operation in enumerate(word['operations']):
        if step == omit:
            continue
        op, name, *rest = operation
        counts[op] += 1
        if op == 'INIT':
            need(name not in values and name not in ever_born, 'fresh owner')
            values[name], locations[name] = 0, rest[0]
            owned.add(name)
            ever_born.add(name)
            lives[name] = {'birth': step, 'chart': rest[0], 'captures': [], 'reads': [], 'moves': []}
        elif op == 'ADD':
            dest = rest[0]
            need(name in values and dest in values and name != dest, 'live distinct ADD endpoints')
            need(charts[locations[name]] == charts[locations[dest]], 'cocharted actual ADD at ' + str(step))
            record = {'operation': step, 'source': name, 'target': dest, 'chart': locations[name],
                      'source_row_hex': hex(values[name]), 'X_subsequence_prefix': xx_prefix}
            if name in xnames and dest in ynames:
                cross_reads.append(record)
            if dest in lives:
                lives[dest]['captures'].append(record)
                if dest.startswith(('ANCHOR_', 'TERMINAL_')):
                    captures.append(record)
            if name in lives:
                lives[name]['reads'].append(record)
                if name.startswith(('ANCHOR_', 'TERMINAL_')):
                    cache_reads.append(record)
            if name in xnames and dest in xnames:
                x_subsequence.append(operation)
                xx_prefix += 1
            if dest in ynames:
                y_subsequence.append(operation)
            need(not (name in ynames and dest in xnames), 'no Y-to-X dependence')
            values[dest] ^= values[name]
        elif op == 'MOVE':
            need(name in values, 'live moved field')
            source, dest = charts[locations[name]], charts[rest[0]]
            delta = len(dest) - len(source)
            need(delta != 0, 'positive MOVE')
            if name in owned:
                need(delta < 0 and geo.contained(dest, source), 'owned source control strictly downward')
                lives[name]['moves'].append({'operation': step, 'from': locations[name], 'to': rest[0], 'gap': -delta})
                directions['owned_down'] += 1
            else:
                need(delta > 0 and geo.contained(source, dest), 'public source control strictly upward')
                directions['public_up'] += 1
            movement[abs(delta)] += 1
            locations[name] = rest[0]
            if name in xnames:
                x_subsequence.append(operation)
                xx_prefix += 1
            if name in ynames:
                y_subsequence.append(operation)
        elif op == 'CLEAR':
            need(name in owned, 'owned retirement')
            lives[name]['retirement'] = step
            lives[name]['retired_row_hex'] = hex(values[name])
            lives[name]['retired_chart'] = locations[name]
            dirty += bool(values[name])
            del values[name], locations[name]
            owned.remove(name)
        else:
            raise ValueError('unknown primitive')
        peak = max(peak, len(owned))
        for label, cut in word.get('milestones', {}).items():
            if step + 1 != cut:
                continue
            snapshots[label] = {'operations_completed': cut, 'live_fields': len(values), 'owners': len(owned),
                                'all_X_raw_at_Hub': all(values[n] == initial[n] and locations[n] == 'Hub' for n in xnames),
                                'all_Y_pure_at_ground': all(values[n] == initial[n] and locations[n] == 'zero' for n in ynames)}
            if label in ['all_X_restored_before_canonical', 'canonical36_at_ground_before_any_Y_move']:
                need(snapshots[label]['all_X_raw_at_Hub'] and snapshots[label]['all_Y_pure_at_ground'], 'actual full-input milestone')
            if label == 'canonical36_at_ground_before_any_Y_move':
                rows = []
                for c in range(4):
                    for i in [0, 1, 2, 4, 8, 9, 14, 30, 59]:
                        n = f'CANONICAL_{i}_{c}'
                        wanted = sum(1 << (4*j+c) for j in range(111) if (K[i] >> j) & 1)
                        need(values[n] == wanted and locations[n] == 'zero', 'actual canonical source row at ground')
                        rows.append(values[n])
                need(binary_rank(rows) == 36, 'actual independent 36-record canonical space')
                snapshots[label]['canonical_row_rank'] = 36
    need(not owned and len(values) == 888, 'all owners retired')
    for n in xnames:
        need(values[n] == initial[n] and locations[n] == 'Hub', 'all original X restored')
    for n, (i, c) in ynames.items():
        correction = 0
        if i == 3:
            correction = (1 << (4*i+c)) if target_complete else sum(1 << (4*j+c) for j in range(111)
                             if sum(a*b for a, b in zip(roots[i], roots[j])) == 0)
        need(values[n] == initial[n] ^ correction and locations[n] == f'F{i}', 'all arbitrary original Y final rows')
    return {'counts': dict(counts), 'movement_profile': dict(sorted(movement.items())),
            'directions': dict(directions), 'dirty_CLEAR': dirty, 'peak_owned': peak,
            'snapshots': snapshots, 'cross_reads': cross_reads, 'captures': captures,
            'cache_reads': cache_reads, 'lives': lives,
            'X_subsequence': x_subsequence, 'Y_subsequence': y_subsequence,
            'all_final_rows': {n: hex(v) for n, v in values.items()}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--author', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    roots = read_pinned(a.repo / NATIVE, 'native')['native_roots']
    old = read_pinned(a.repo / LOCAL, 'local')
    new = read_pinned(a.author / 'output/WORD.json', 'word')
    for file, key in [('PROOF.md', 'author_proof'), ('build.py', 'author_builder')]:
        need(sha256((a.author / file).read_bytes()).hexdigest() == PINS[key], 'author frozen ' + key)
    need(sha256((a.repo / GEOMETRY).read_bytes()).hexdigest() == PINS['geometry'], 'independent Fraction geometry')
    spec = importlib.util.spec_from_file_location('cache_review_fraction_geometry', a.repo / GEOMETRY)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    before, after = replay(old, roots, g, False), replay(new, roots, g, True)
    need(before['X_subsequence'] == after['X_subsequence'], 'identical chronological X computation and restoration')
    need(before['counts'] == {'ADD': 1050, 'MOVE': 1128}, 'complete predecessor invoice')
    need(after['counts'] == {'ADD': 3210, 'MOVE': 1164, 'INIT': 44, 'CLEAR': 44}, 'complete new invoice')
    need(after['movement_profile'] == {1: 12, 2: 228, 5: 232, 6: 4, 7: 652, 8: 36}, 'complete movement profile')
    need(after['dirty_CLEAR'] == after['peak_owned'] == 44, 'dirty retirement and peak memory')
    caches = {n: life for n, life in after['lives'].items() if n.startswith(('ANCHOR_', 'TERMINAL_'))}
    need(len(caches) == 8 and all(not l['moves'] for l in caches.values()), 'eight genuinely stationary caches')
    author_lifetimes = read_pinned(a.author / 'output/CACHE-LIFETIMES.json', 'author_lifetimes')
    need(author_lifetimes['word_sha256'] == PINS['word'], 'lifetime word binding')
    need(set(author_lifetimes['fields']) == set(caches), 'complete author cache inventory')
    for name, actual in caches.items():
        reported = author_lifetimes['fields'][name]
        need((reported['birth'], reported['chart'], reported['clear'], reported['row_hex']) ==
             (actual['birth'], actual['chart'], actual['retirement'], actual['retired_row_hex']), 'exact cache lifetime endpoints')
        need(reported['captures'] == [{'operation': r['operation'], 'source': r['source'],
                                       'source_row_hex': r['source_row_hex']} for r in actual['captures']], 'all author cache capture rows')
        need(reported['reads'] == [{'operation': r['operation'], 'target': r['target'],
                                    'stored_row_hex': r['source_row_hex']} for r in actual['reads']], 'all author deferred read rows')
        need(reported['stationary'] and actual['retired_chart'] == actual['chart'], 'actual stationary retirement')
    expected_captures, expected_reads, used_anchors, used_terminal = [], [], set(), {}
    old_cross_by_operation = {r['operation']: r for r in before['cross_reads']}
    anchor_cross_indices = {}
    for step, operation in enumerate(old['operations']):
        op, n, *rest = operation
        if step in old_cross_by_operation:
            r = old_cross_by_operation[step]
            if r['chart'] in ['C0', 'C1']:
                cache = 'ANCHOR_' + r['target']
                expected_captures.append((n, cache, r['chart'], r['source_row_hex'], r['X_subsequence_prefix']))
                anchor_cross_indices.setdefault(r['target'], []).append(step)
                if cache not in used_anchors:
                    used_anchors.add(cache)
                    expected_reads.append(['ADD', cache, r['target']])
            else:
                need(r['chart'] == 'F3', 'actual terminal chart')
                cache = 'TERMINAL_' + n
                if cache not in used_terminal:
                    used_terminal[cache] = r['source_row_hex']
                    expected_captures.append((n, cache, r['chart'], r['source_row_hex'], r['X_subsequence_prefix']))
                need(used_terminal[cache] == r['source_row_hex'], 'unchanged terminal pivot reused')
                expected_reads.append(['ADD', cache, r['target']])
        elif (op == 'MOVE' and n.startswith('Y')) or (op == 'ADD' and rest[0].startswith('Y')):
            expected_reads.append(operation)
    got_captures = [(r['source'], r['target'], r['chart'], r['source_row_hex'], r['X_subsequence_prefix'])
                    for r in after['captures']]
    need(got_captures == expected_captures, 'every cache captures its exact original chronological source row')
    for target, indices in anchor_cross_indices.items():
        for step in range(indices[0], indices[-1]+1):
            op, src, *rest = old['operations'][step]
            touches = src == target or (op == 'ADD' and rest[0] == target)
            if touches:
                need(step in indices, 'no intervening use/change/movement of a consolidated anchor Y')
    preloads = [['ADD', f'CANONICAL_{i}_{c}', f'Y3_{c}'] for c in range(4) for i in [0, 1, 2]]
    need(after['Y_subsequence'] == preloads + expected_reads, 'exact deferred Y order after actual canonical preload')
    K = [sum(1 << j for j in range(111) if i == j or sum(x*y for x, y in zip(roots[i], roots[j])) == 0)
         for i in range(111)]
    need(binary_rank(K) == 9 and binary_rank([K[i] for i in [0,1,2,4,8,9,14,30,59]]) == 9, 'full native canonical basis')
    need(K[3] == K[0] ^ K[1] ^ K[2], 'actual K3 preload identity')
    profile = {gap: Fraction(count, 4) for gap, count in after['movement_profile'].items()}
    price = g.moment(profile)
    ceiling_profile = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        ceiling_profile[1+7*j] = ceiling_profile.get(1+7*j, 0) + 74
        ceiling_profile[7*j] = ceiling_profile.get(7*j, 0) - 74
    ceiling = tuple(x/6 for x in g.moment(ceiling_profile))
    room = ceiling[0]-price[1], ceiling[1]-price[0]
    # Targeted actual-source omissions, checked by the independent interpreter.
    mutations = {
        'terminal capture': next(r['operation'] for r in after['captures'] if r['target'].startswith('TERMINAL_')),
        'terminal facet visit': next(i for i, op in enumerate(new['operations']) if op == ['MOVE','X1_2','F3']),
        'X restoration': max(i for i, op in enumerate(new['operations']) if op[0] == 'ADD' and op[1].startswith('X') and op[2].startswith('X')),
        'canonical supply descent': next(i for i, op in enumerate(new['operations']) if op[0] == 'MOVE' and op[1].startswith('CANONICAL_')),
        'canonical preload': new['milestones']['canonical36_at_ground_before_any_Y_move'],
        'terminal retirement': next(i for i, op in enumerate(new['operations']) if op[0] == 'CLEAR' and op[1].startswith('TERMINAL_')),
    }
    rejected = []
    for label, step in mutations.items():
        try:
            replay(new, roots, g, True, omit=step)
        except (ValueError, KeyError) as error:
            rejected.append({'mutation': label, 'omitted_operation': step, 'reason': str(error)})
        else:
            raise ValueError('bad omission accepted: ' + label)
    result = {
        'status': 'PASS_INDEPENDENT_ALL888_AND_CHRONOLOGY_REVIEW',
        'pins': PINS, 'all_original_columns': 888,
        'counts': after['counts'], 'movement_profile': after['movement_profile'],
        'directions': after['directions'], 'dirty_CLEAR': after['dirty_CLEAR'], 'peak_owned': after['peak_owned'],
        'milestones': after['snapshots'], 'stationary_cache_count': len(caches),
        'original_cross_read_count': len(before['cross_reads']),
        'actual_cache_capture_count': len(after['captures']),
        'actual_deferred_cache_read_count': len(after['cache_reads']),
        'identical_X_subsequence': True, 'all_capture_rows_and_X_prefixes_match': True,
        'exact_deferred_Y_subsequence': True, 'anchor_consolidation_no_intervening_use': True,
        'full_native_canonical_rank': 9, 'actual_ground_canonical_rank': 36,
        'completed_native_roles_per_copy': [3], 'all_other_Y_exactly_unchanged': True,
        'normalized_movement_moment': interval(price), 'normalized_optimistic_remaining_room': interval(room),
        'independent_negative_controls': rejected,
        'scope': 'Generic source rescheduling lemma under X-only computation and stationary cache permissions; literal one receiver in four separately paid banks. No simultaneous all111 source network, complete supplier, caller construction, or new kappa.',
    }
    a.out.mkdir(parents=True, exist_ok=True)
    for name, data in [('RESULT.json', result), ('INDEPENDENT-CACHE-LIFETIMES.json', caches),
                       ('ALL888-FINAL-ROWS.json', after['all_final_rows'])]:
        (a.out/name).write_text(json.dumps(data, indent=2) + '\n')
    print(result['status'])
    print('counts', result['counts'], 'profile', result['movement_profile'])
    print('captures', result['actual_cache_capture_count'], 'reads', result['actual_deferred_cache_read_count'])
    print('Q', result['normalized_movement_moment']['decimal'][0])
    print('room', result['normalized_optimistic_remaining_room']['decimal'][0])


if __name__ == '__main__':
    main()
