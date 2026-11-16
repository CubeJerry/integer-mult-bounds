#!/usr/bin/env python3
"""Exchange three Q descents for three real Extra6 imports, preserving41 outputs.

The stationary Q copies are built from the same actual original values as their
parents. No old donor, source-cut metadata, or deleted history is inherited.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json

from source_loader import load

BASE = '6c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9'
Q_COPIES = {'Q1': ('C1', 'F74', 'Q1_F74'),
            'Q3': ('C3', 'F4', 'Q3_F4'),
            'Q4': ('C4', 'F78', 'Q4_F78')}
RECEIVERS = {'Y4': ('C1', 'Q1', 'F4', 'Q3_F4'),
             'Y74': ('C4', 'Q4', 'F74', 'Q1_F74'),
             'Y78': ('C3', 'Q3', 'F78', 'Q4_F78')}
IMPORTS = [8, 9, 36]
CUT = ['ADD', 'CAP46', 'P3']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(old):
    w = copy.deepcopy(old)
    cohorts = {q: [o[1] for o in old['operations']
                   if o[0] == 'ADD' and o[2] == q]
               for q in Q_COPIES}
    source_copy = {}
    for q, sources in cohorts.items():
        assert all(n.startswith('X') for n in sources)
        for n in sources:
            assert n not in source_copy
            source_copy[n] = q
    ops = [['INIT', field, facet] for _, facet, field in Q_COPIES.values()]
    ops += [['INIT', f'IMPORT_E{i}', 'Extra6'] for i in IMPORTS]
    relocated_reads = []
    for o in old['operations']:
        op, n, *args = o
        if op == 'MOVE' and n in Q_COPIES and args == ['M1']:
            continue
        if op == 'ADD' and n in Q_COPIES and args[0] in RECEIVERS:
            relocated_reads.append(o)
            continue
        if op == 'MOVE' and n in source_copy and args == ['Hub']:
            _, facet, field = Q_COPIES[source_copy[n]]
            ops += [['MOVE', n, facet], ['ADD', n, field]]
        if op == 'MOVE' and n in [f'X{i}' for i in IMPORTS] and args == ['Hub']:
            field = f'IMPORT_E{n[1:]}'
            ops += [['MOVE', n, 'Extra6'], ['ADD', n, field],
                    ['MOVE', field, 'M1']]
        if op == 'MOVE' and n in RECEIVERS and args == [RECEIVERS[n][2]]:
            chart, q, _, field = RECEIVERS[n]
            ops += [['MOVE', n, chart], ['ADD', q, n], o,
                    ['ADD', field, n]]
        else:
            ops.append(o)
    assert len(relocated_reads) == 6
    ops += [['CLEAR', field] for _, _, field in Q_COPIES.values()]
    ops += [['CLEAR', f'IMPORT_E{i}'] for i in IMPORTS]
    w['operations'] = ops
    w['base_word_sha256'] = BASE
    w['schema'] = 'cyclic-stationary-cache-three-imports-native-word-v1'
    w['cyclic_cache_acquisition'] = {
        'cache_source_cohorts': cohorts,
        'stationary_copies': Q_COPIES,
        'receiver_paths': RECEIVERS,
        'imports': IMPORTS,
        'source_cut_before_operation': CUT,
        'new_complete_outputs': 0,
        'lost_M1_cache_fields': sorted(Q_COPIES),
        'net_added_owned_MOVEs': 0,
    }
    w['scope'] = ('Same41 exact endpoints and restored arbitrary original inputs; '
                  'three actual independent Extra6-to-M1 imports replace three '
                  'old Q descents after a cyclic higher-cache receiver repair. '
                  'All changed source inventories are recomputed; no complete '
                  'E decoder,111-output supplier, or new kappa is asserted.')
    return w


def observe(word, C):
    v = {f'X{i}': 1 << i for i in range(111)}
    v.update({f'Y{i}': 1 << (111+i) for i in range(111)})
    at = {f'X{i}': f'L{i}' for i in range(111)}
    at.update({f'Y{i}': 'zero' for i in range(111)})
    capture_events = []
    cut = None
    copies = {r[2] for r in Q_COPIES.values()}
    fields = copies | {f'IMPORT_E{i}' for i in IMPORTS}
    for step, o in enumerate(word['operations'], 1):
        if o == CUT:
            cut = {'step': step, 'values': v.copy(), 'charts': at.copy(),
                   'M1': {n: r for n, r in v.items()
                          if n != 'P3' and not (r >> 111) and C[at[n]] == C['M1']}}
        op, n, *q = o
        if op == 'INIT':
            v[n] = 0
            at[n] = q[0]
        elif op == 'MOVE':
            at[n] = q[0]
        elif op == 'ADD':
            if q[0] in fields:
                capture_events.append({'step': step, 'operation': o,
                                       'source_row_hex': hex(v[n]),
                                       'source_chart': at[n], 'target_chart': at[q[0]]})
            v[q[0]] ^= v[n]
        elif op == 'CLEAR':
            del v[n], at[n]
    assert cut is not None
    return cut, capture_events


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--engine', type=Path, required=True)
    p.add_argument('--price-engine', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    assert sha(a.base) == BASE
    old = json.loads(a.base.read_text())
    native = a.repo / old['source_path']
    assert sha(native) == old['source_sha256']
    roots = json.loads(native.read_text())['native_roots']
    e = load(a.engine, 'cyclic_import_geometry')
    price = load(a.price_engine, 'cyclic_import_price')
    OC, _, prior_report = e.replay(old, roots)
    old_cut, _ = observe(old, OC)
    w = build(old)
    C, H, report = e.replay(w, roots)
    cut, captures = observe(w, C)
    assert cut['values']['P3'] == 0 and cut['charts']['P3'] == 'M1'
    for q, (chart, facet, field) in Q_COPIES.items():
        assert e.sub(C[chart], C[facet])
        assert len(C[chart]) == 6 and len(C[facet]) == 7
        assert cut['values'][field] == cut['values'][q] == old_cut['values'][q]
        assert cut['charts'][q] == chart and cut['charts'][field] == facet
        assert q not in cut['M1'] and old_cut['charts'][q] == 'M1'
    for y, (chart, q, facet, field) in RECEIVERS.items():
        assert e.sub(C['M1'], C[chart]) and e.sub(C[chart], C[facet])
    for i in IMPORTS:
        assert cut['M1'][f'IMPORT_E{i}'] == 1 << i
        assert e.sub(C[f'L{i}'], C['Extra6'])
    assert e.sub(C['M1'], C['Extra6'])
    E = sum(1 << i for i in [8, 9, 36, 37])
    prior_E = [r & E for r in old_cut['M1'].values()]
    new_E = [r & E for r in cut['M1'].values()]
    assert len(e.bb(prior_E)) == 0 and len(e.bb(new_E)) == 3
    assert len(captures) == 30
    assert report['counts'] == {'INIT': 124, 'ADD': 828, 'MOVE': 483, 'CLEAR': 124}
    assert report['dirty_CLEAR'] == 124
    delta = {1: 60, 2: -27, 5: 3, 7: -3}
    profile = prior_report['movement_profile'].copy()
    for rank, n in delta.items():
        profile[rank] = profile.get(rank, 0) + n
    assert report['movement_profile'] == dict(sorted(profile.items()))
    owned = {o[1] for o in w['operations'] if o[0] == 'INIT'}
    old_owned = {o[1] for o in old['operations'] if o[0] == 'INIT'}
    old_owned_moves = [o for o in old['operations'] if o[0] == 'MOVE' and o[1] in old_owned]
    new_owned_moves = [o for o in w['operations'] if o[0] == 'MOVE' and o[1] in owned]
    assert len(old_owned_moves) == len(new_owned_moves)
    tests = [['MOVE', 'Y4', 'C1'], ['ADD', 'Q1', 'Y4'],
             ['ADD', 'Q3_F4', 'Y4'], ['MOVE', 'Y74', 'C4'],
             ['ADD', 'Q1_F74', 'Y74'], ['MOVE', 'Y78', 'C3'],
             ['ADD', 'Q4_F78', 'Y78'], ['ADD', 'X60', 'Q1_F74'],
             ['ADD', 'X59', 'Q3_F4'], ['ADD', 'X13', 'Q4_F78'],
             ['MOVE', 'X60', 'F74'], ['MOVE', 'X59', 'F4'],
             ['MOVE', 'X13', 'F78'], ['CLEAR', 'Q1_F74']]
    rejected = []
    for op in tests:
        bad = copy.deepcopy(w)
        bad['operations'].remove(op)
        try:
            e.replay(bad, roots)
        except (AssertionError, KeyError) as ex:
            rejected.append({'removed': op, 'failure': str(ex)})
        else:
            raise AssertionError(('accepted endpoint/geometry omission', op))
    interface_controls = []
    for i in IMPORTS:
        field = f'IMPORT_E{i}'
        for op in [['ADD', f'X{i}', field], ['MOVE', field, 'M1']]:
            bad = copy.deepcopy(w)
            bad['operations'].remove(op)
            e.replay(bad, roots)
            bad_cut, _ = observe(bad, C)
            assert field not in bad_cut['M1'] or bad_cut['M1'][field] == 0
            interface_controls.append({'removed': op, 'old41_endpoints_still_hold': True,
                                       'claimed_actual_M1_import_fails': True})
        probe = copy.deepcopy(w)
        ix = probe['operations'].index(CUT)
        probe['operations'][ix:ix] = [['ADD', field, 'P3'], ['ADD', field, 'P3']]
        e.replay(probe, roots)
    Q = price.moment(report['movement_profile'])
    budget = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        budget[1+7*j] = budget.get(1+7*j, 0) + 74
        budget[7*j] = budget.get(7*j, 0) - 74
    allowance = tuple(x/6 for x in price.moment(budget))
    room = allowance[0]-Q[1], allowance[1]-Q[0]
    a.out.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(w, indent=2)+'\n').encode()
    (a.out/'WORD.json').write_bytes(encoded)
    result = {
        'status': 'PASS_ACTUAL_CYCLIC_CACHE_THREE_IMPORTS_PRESERVE41',
        'word_sha256': hashlib.sha256(encoded).hexdigest(),
        'base_word_sha256': BASE,
        'native_source_sha256': old['source_sha256'],
        'dependency_sha256': {'geometry_engine': sha(a.engine), 'price_engine': sha(a.price_engine)},
        'before': prior_report, 'after': report,
        'source_cut_before_operation': CUT,
        'source_capture_events': captures,
        'old_actual_M1_inventory_hex': {n: hex(r) for n, r in old_cut['M1'].items()},
        'actual_M1_inventory_hex': {n: hex(r) for n, r in cut['M1'].items()},
        'M1_rank_before': len(e.bb(old_cut['M1'].values())),
        'M1_rank_after': len(e.bb(cut['M1'].values())),
        'M1_E_projection_rank_before': 0, 'M1_E_projection_rank_after': 3,
        'removed_M1_fields': sorted(Q_COPIES),
        'identical_Q_rows_at_new_stationary_copies': {
            field: {'row_hex': hex(cut['values'][field]), 'chart': facet,
                    'original_field': q, 'original_retained_chart': chart}
            for q, (chart, facet, field) in Q_COPIES.items()},
        'all_old41_endpoints_and_originals_preserved': True,
        'new_complete_outputs': 0,
        'owned_MOVE_count_before': len(old_owned_moves),
        'owned_MOVE_count_after': len(new_owned_moves),
        'exact_movement_increment': '60[1]-27[2]+3[5]-3[7]',
        'signed_movement_profile_increment': delta,
        'zero_linear_rank_volume_increment': sum(k*v for k, v in delta.items()) == 0,
        'price': {'moment': price.display(Q), 'limiting_allowance': price.display(allowance),
                  'limiting_room': price.display(room), 'increment': price.display(price.moment(delta))},
        'endpoint_or_geometry_omissions_rejected': rejected,
        'source_interface_controls': interface_controls,
        'all_three_actual_M1_read_then_unread_probes_pass': True,
        'scope': w['scope'],
    }
    (a.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'word_sha256', 'after',
                                           'M1_rank_before', 'M1_rank_after', 'price']}))


if __name__ == '__main__':
    main()
