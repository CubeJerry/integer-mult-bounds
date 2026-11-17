#!/usr/bin/env python3
"""Defer all public-Y work using stationary proper and terminal caches."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, importlib.util, json

BASE = 'research/moonshot-005-program'
NATIVE = BASE + '/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
NATIVE_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
LOCAL = BASE + '/results/bit-shared-facet-mds/author/four-chart-word/WORD.json'
LOCAL_SHA = '831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa'
GEO = BASE + '/results/bit-leaf-capacity-quotient/author/check.py'
PRICE = BASE + '/sessions/2026-11-17-S019/checkpoint3-evidence/A/build_common_carrier_fanout.py'
BASIS = [0, 1, 2, 4, 8, 9, 14, 30, 59]

def module(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')

def replay(w, R, g, mutation=None):
    charts = {n: g.chart(c) for n, c in w['charts'].items()}
    X = {f'X{j}_{k}': (j, k) for j in range(111) for k in range(4)}
    Y = {f'Y{j}_{k}': (j, k) for j in range(111) for k in range(4)}
    v = {n: 1 << (4*j+k) for n, (j, k) in X.items()}
    v.update({n: 1 << (444+4*j+k) for n, (j, k) in Y.items()})
    loc = {n: f'L{j}' for n, (j, _) in X.items()} | {n: 'zero' for n in Y}
    own = set(); born = set(); counts = Counter(); moves = Counter()
    dirty = peak = 0; snapshots = {}
    for step, o in enumerate(w['operations']):
        op, src, *a = o
        if mutation == step:
            continue
        counts[op] += 1
        if op == 'INIT':
            assert src not in v and src not in born
            v[src] = 0; loc[src] = a[0]; own.add(src); born.add(src)
        elif op == 'ADD':
            dst = a[0]
            assert src != dst and src in v and dst in v
            assert charts[loc[src]] == charts[loc[dst]], (step, o, loc[src], loc[dst])
            v[dst] ^= v[src]
        elif op == 'MOVE':
            to = a[0]; before = charts[loc[src]]; after = charts[to]
            assert len(before) != len(after)
            assert g.sub(after, before) if src in own else g.sub(before, after)
            moves[abs(len(before)-len(after))] += 1; loc[src] = to
        elif op == 'CLEAR':
            assert src in own
            dirty += bool(v[src]); own.remove(src); del v[src], loc[src]
        else:
            raise AssertionError(op)
        peak = max(peak, len(own))
        for label, cut in w['milestones'].items():
            if step+1 != cut:
                continue
            if label in ['all_X_restored_before_canonical', 'canonical36_at_ground_before_any_Y_move']:
                assert all(loc[n] == 'Hub' and v[n] == 1 << (4*j+k) for n, (j, k) in X.items())
                assert all(loc[n] == 'zero' and v[n] == 1 << (444+4*j+k) for n, (j, k) in Y.items())
            if label == 'canonical36_at_ground_before_any_Y_move':
                for seed in w['canonical_seeds']:
                    assert loc[seed['packet']] == 'zero' and v[seed['packet']] == int(seed['row_hex'], 16)
            snapshots[label] = {'live_fields': len(v), 'owners': len(own),
                'all_X_raw_at_Hub': all(loc[n] == 'Hub' and v[n] == 1 << (4*j+k) for n, (j, k) in X.items()),
                'all_Y_pure_at_ground': all(loc[n] == 'zero' and v[n] == 1 << (444+4*j+k) for n, (j, k) in Y.items())}
    assert not own and len(v) == 888
    for n, (j, k) in X.items():
        assert loc[n] == 'Hub' and v[n] == 1 << (4*j+k)
    for n, (j, k) in Y.items():
        wanted = (1 << (444+4*j+k)) ^ ((1 << (4*j+k)) if j == 3 else 0)
        assert loc[n] == f'F{j}' and v[n] == wanted, ('output', n)
    return {'all_original_columns': 888, 'counts': dict(counts), 'movement_profile': dict(sorted(moves.items())),
        'dirty_CLEAR': dirty, 'peak_owned': peak, 'milestones': snapshots,
        'completed_roles_each_copy': [3], 'all_other_Y_unchanged': True}

def main():
    p = argparse.ArgumentParser(); p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True); a = p.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
    native = (a.repo / NATIVE).read_bytes(); assert hashlib.sha256(native).hexdigest() == NATIVE_SHA
    R = json.loads(native)['native_roots']; raw = (a.repo / LOCAL).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == LOCAL_SHA; old = json.loads(raw)
    g = module(a.repo / GEO, 'deferred_cache_geometry'); h = module(a.repo / PRICE, 'deferred_cache_price')
    X = {f'X{j}_{k}': (j, k) for j in range(111) for k in range(4)}
    loc = {n: f'L{j}' for n, (j, _) in X.items()}
    val = {n: 1 << (4*j+k) for n, (j, k) in X.items()}
    ops = []; yops = []; sem = {}; owners = []; anchors = {}; terminal = {}; records = []
    def emit(o, key):
        sem.setdefault(key, []).append(len(ops)); ops.append(o)
    def cache(name, chart, kind):
        owners.append(name); emit(['INIT', name, chart], kind + '_INIT')
    for step, o in enumerate(old['operations']):
        op, src, *q = o
        if op == 'MOVE' and src.startswith('X'):
            emit(o, 'original_X_MOVE'); loc[src] = q[0]
        elif op == 'ADD' and src.startswith('X') and q[0].startswith('X'):
            emit(o, 'original_X_ADD'); val[q[0]] ^= val[src]
        elif op == 'ADD' and src.startswith('X') and q[0].startswith('Y'):
            dst = q[0]; chart = loc[src]
            if chart in ['C0', 'C1']:
                if dst not in anchors:
                    name = 'ANCHOR_' + dst; anchors[dst] = name
                    cache(name, chart, 'anchor_cache')
                    yops.append(['ADD', name, dst])
                    records.append({'name': name, 'kind': 'proper_anchor', 'chart': chart, 'source_Y': dst})
                emit(['ADD', src, anchors[dst]], 'anchor_capture_ADD')
            else:
                assert chart == 'F3'
                key = (src, chart)
                if key not in terminal:
                    name = 'TERMINAL_' + src; terminal[key] = (name, val[src])
                    cache(name, chart, 'terminal_cache')
                    emit(['ADD', src, name], 'terminal_capture_ADD')
                    records.append({'name': name, 'kind': 'terminal_pivot', 'chart': chart,
                        'source_X': src, 'row_hex': hex(val[src]), 'first_original_read': step})
                name, stored = terminal[key]; assert stored == val[src]
                yops.append(['ADD', name, dst])
        elif op == 'MOVE' and src.startswith('Y'):
            yops.append(o)
        elif op == 'ADD' and src.startswith('Y') and q[0].startswith('Y'):
            yops.append(o)
        else:
            raise AssertionError(('nonseparable original word', step, o))
    assert len(anchors) == len(terminal) == 4
    assert all(loc[n] == 'Hub' and val[n] == 1 << (4*j+k) for n, (j, k) in X.items())
    milestones = {'all_X_restored_before_canonical': len(ops)}
    K = [sum(1 << j for j in range(111) if j == i or sum(x*y for x, y in zip(R[i], R[j])) == 0) for i in range(111)]
    assert K[3] == K[0] ^ K[1] ^ K[2]
    echelon = {}
    for row in [K[i] for i in BASIS]:
        while row:
            pivot = row.bit_length()-1
            if pivot in echelon: row ^= echelon[pivot]
            else: echelon[pivot] = row; break
    assert len(echelon) == 9
    for row in K:
        while row:
            pivot = row.bit_length()-1
            assert pivot in echelon
            row ^= echelon[pivot]
    seeds = []
    for k in range(4):
        for i in BASIS:
            name = f'CANONICAL_{i}_{k}'; cache(name, 'Hub', 'canonical')
            sources = [f'X{j}_{k}' for j in range(111) if K[i] >> j & 1]
            for src in sources: emit(['ADD', src, name], 'canonical_source_ADD')
            emit(['MOVE', name, 'zero'], 'canonical_direct_descent')
            row = sum(1 << (4*j+k) for j in range(111) if K[i] >> j & 1)
            seeds.append({'packet': name, 'basis_role': i, 'copy': k, 'row_hex': hex(row), 'source_reads': sources})
    milestones['canonical36_at_ground_before_any_Y_move'] = len(ops)
    for k in range(4):
        for i in [0, 1, 2]: emit(['ADD', f'CANONICAL_{i}_{k}', f'Y3_{k}'], 'canonical_Y_preload_ADD')
    for o in yops: emit(o, 'deferred_Y_' + o[0])
    milestones['all_public_endpoints_complete'] = len(ops)
    for name in owners: emit(['CLEAR', name], 'owned_retirement')
    w = {'schema': 'stationary-terminal-cache-canonical-chronology-v1',
        'native_path': NATIVE, 'native_sha256': NATIVE_SHA, 'original_local_word_path': LOCAL,
        'original_local_word_sha256': LOCAL_SHA, 'physical_binary_copies': 4, 'charts': old['charts'],
        'operations': ops, 'semantic_operation_indices': sem, 'milestones': milestones,
        'cache_inventory': records, 'canonical_seeds': seeds, 'completed_roles_each_copy': [3],
        'new_complete_kappa': False, 'global_source_network_constructed': False}
    save(a.out / 'WORD.json', w); receipt = replay(w, R, g)
    # A complete lifetime log records the actual row at each capture and read.
    vals = {f'X{j}_{k}': 1 << (4*j+k) for j in range(111) for k in range(4)}
    vals.update({f'Y{j}_{k}': 1 << (444+4*j+k) for j in range(111) for k in range(4)})
    places = {f'X{j}_{k}': f'L{j}' for j in range(111) for k in range(4)}
    places.update({f'Y{j}_{k}': 'zero' for j in range(111) for k in range(4)})
    life = {}
    for step, (op, n, *q) in enumerate(ops):
        if op == 'INIT':
            vals[n] = 0; places[n] = q[0]
            if n.startswith(('ANCHOR_', 'TERMINAL_')):
                life[n] = {'chart': q[0], 'birth': step, 'captures': [], 'reads': []}
        elif op == 'ADD':
            d = q[0]
            if d in life: life[d]['captures'].append({'operation': step, 'source': n, 'source_row_hex': hex(vals[n])})
            if n in life: life[n]['reads'].append({'operation': step, 'target': d, 'stored_row_hex': hex(vals[n])})
            vals[d] ^= vals[n]
        elif op == 'MOVE': places[n] = q[0]
        elif op == 'CLEAR':
            if n in life: life[n].update({'clear': step, 'row_hex': hex(vals[n]), 'stationary': places[n] == life[n]['chart']})
            del vals[n], places[n]
    save(a.out/'CACHE-LIFETIMES.json', {'word_sha256': hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(), 'fields': life})
    controls = []
    for name, index in [('anchor_capture', sem['anchor_capture_ADD'][0]),
                        ('terminal_capture', sem['terminal_capture_ADD'][0]),
                        ('terminal_retirement', next(s for s in sem['owned_retirement'] if ops[s][1].startswith('TERMINAL_'))),
                        ('actual_terminal_facet_visit', next(s for s in sem['original_X_MOVE'] if ops[s] == ['MOVE', 'X1_2', 'F3'])),
                        ('original_X_restore', sem['original_X_ADD'][-1]),
                        ('canonical_source', sem['canonical_source_ADD'][0]),
                        ('canonical_descent', sem['canonical_direct_descent'][0]),
                        ('Y_preload', sem['canonical_Y_preload_ADD'][0])]:
        try: replay(w, R, g, mutation=index)
        except (AssertionError, KeyError): controls.append({'control': name, 'rejected': True, 'omitted_step': index})
        else: raise AssertionError(('negative control accepted', name))
    from fractions import Fraction
    profile = {d: Fraction(n, 4) for d, n in receipt['movement_profile'].items()}
    q = h.moment(profile); cap = h.moment({127: 37, 64: 74, 1: -74})
    for j in range(1, 9):
        v = h.moment({1+7*j: 74, 7*j: -74}); cap = (cap[0]+v[0], cap[1]+v[1])
    cap = (cap[0]/6, cap[1]/6); room = (cap[0]-q[1], cap[1]-q[0])
    result = {'status': 'PASS_LITERAL_DEFERRED_TERMINAL_CACHE_CHRONOLOGY',
        'word_sha256': hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),
        'original_word_sha256': LOCAL_SHA, **receipt, 'stationary_anchor_owners': 4,
        'stationary_terminal_owners': 4, 'canonical_owners': 36,
        'additional_noncanonical_MOVEs': 0,
        'ordinary_ADD_breakdown': {key: len(indices) for key, indices in sem.items() if key.endswith('_ADD')},
        'normalized_movement_profile': {d: str(n) for d, n in profile.items()},
        'normalized_moment': h.record(q), 'normalized_necessary_limiting_room': h.record(room),
        'negative_controls': controls, 'global_source_network_constructed': False,
        'complete_supplier': False, 'new_complete_kappa': False}
    save(a.out/'RESULT.json', result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
