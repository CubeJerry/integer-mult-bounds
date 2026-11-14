#!/usr/bin/env python3
"""Joint pre-Hub L0/L1 acquisition with one charged outward copy.

Extends frozen builder cf783adafb7fcb724ec4ea37e769e1003ea83fe1076cbec10dcb47ddb07dd4d8.
All X restored; Y0/Y1 completed; one owned upward rank-one MOVE is charged.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def rref(rows):
    a = [[F(x) for x in r] for r in rows]
    p = 0
    for c in range(8):
        q = next((i for i in range(p, len(a)) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        scale = a[p][c]
        a[p] = [x/scale for x in a[p]]
        for j in range(len(a)):
            if j != p:
                scale = a[j][c]
                a[j] = [x-scale*y for x, y in zip(a[j], a[p])]
        p += 1
    return tuple(tuple(row) for row in a[:p])


def perpendicular(basis):
    b = rref(basis)
    pivots = [next(i for i, x in enumerate(row) if x) for row in b]
    out = []
    for f in range(8):
        if f in pivots:
            continue
        v = [F(0)]*8
        v[f] = 1
        for p, row in zip(pivots, b):
            v[p] = -row[f]
        out.append(v)
    return rref(out)


def included(a, b):
    return len(rref(list(a)+list(b))) == len(b)


def encode_basis(basis):
    return [[int(x) if x.denominator == 1 else str(x) for x in row] for row in basis]


def replay(word):
    frames = {int(c): f for c, f in word['frames'].items()}
    spaces = {c: rref(f['B']) for c, f in frames.items()}
    for c, f in frames.items():
        need(len(spaces[c]) == f['dim'], ('chart rank', c))
        a = rref(f['A'])
        need(len(a)+len(spaces[c]) == 8 and all(dot(x, y) == 0 for x in a for y in spaces[c]),
             ('chart orthogonal complement', c))
    where = dict(enumerate(word['start']))
    rows = {i: 1 << i for i in range(222)}
    counts = Counter()
    paid = Counter()
    lifetimes = peak = 0
    clears = []
    snapshots = {}
    selected = set(word.get('snapshot_indices', []))
    move_pairs = set()
    routes = {i: [where[i]] for i in rows}
    for n, op in enumerate(word['program']):
        kind, a = op[:2]
        counts[kind] += 1
        if kind == 'INIT':
            need(a >= 222 and a not in rows, ('zero-born owned field', n, op))
            rows[a], where[a] = 0, op[2]
            routes[a] = [op[2]]
            lifetimes += 1
            peak = max(peak, len(rows)-222)
        elif kind == 'ADD':
            _, a, b, c = op
            need(a != b and a in rows and b in rows and where[a] == where[b] == c,
                 ('cocharted active ADD', n, op))
            rows[a] ^= rows[b]
        elif kind == 'MOVE':
            _, a, c, d = op
            need(a in rows and where[a] == c, ('MOVE source', n, op))
            dc, dd = len(spaces[c]), len(spaces[d])
            need(abs(dc-dd) == 1, ('unit-rank MOVE', n, op))
            small, large = (spaces[c], spaces[d]) if dc < dd else (spaces[d], spaces[c])
            need(included(small, large), ('real chart inclusion', n, op))
            direction = word['directions'].get(str(a), 'up' if a < 222 else 'stationary')
            need((dd > dc if direction == 'up' else dd < dc if direction == 'down' else False), ('declared monotone direction', n, op))
            where[a] = d
            routes[a].append(d)
            paid[abs(dc-dd)] += 1
            move_pairs.add((c, d))
        elif kind == 'CLEAR':
            _, a, c = op
            need(a >= 222 and a in rows and where[a] == c, ('owned CLEAR', n, op))
            clears.append({'operation': n, 'field': a, 'chart': c, 'row_hex': hex(rows[a])})
            del rows[a]
            del where[a]
        else:
            raise ValueError(('unsupported operation', n, op))
        if n in selected:
            snapshots[str(n)] = {'rows': {str(i): hex(rows[i]) for i in (111, 112, 222, 223, 224, 225) if i in rows},
                                 'all_X_restored_at_Hub': all(rows[i] == 1 << i and where[i] == word['hub'] for i in range(111))}
    need(set(rows) == set(range(222)), 'all owned lifetimes retired')
    need([where[i] for i in range(222)] == word['final'], 'all public endpoint charts')
    return {'rows': [rows[i] for i in range(222)], 'counts': dict(counts),
            'paid_profile': dict(sorted(paid.items())), 'owned_lifetimes': lifetimes,
            'peak_owned': peak, 'clear_rows': clears, 'snapshots': snapshots,
            'routes': routes, 'exact_nested_move_pairs': len(move_pairs)}


def emit(native):
    frames = {int(c): f for c, f in native['frames'].items()}
    spaces = {c: rref(f['B']) for c, f in frames.items()}
    key_to_id = {b: c for c, b in spaces.items()}
    for c in native['start'][:222]+native['final'][:222]:
        key_to_id[spaces[c]] = c
    created = []
    eye = [tuple(F(i == j) for j in range(8)) for i in range(8)]
    hub, zero, f0 = native['final'][0], native['start'][111], native['final'][111]
    need((len(spaces[hub]), len(spaces[zero]), len(spaces[f0])) == (8, 0, 7), 'actual endpoint dimensions')

    def chart(basis):
        b = rref(basis)
        if b in key_to_id:
            return key_to_id[b]
        c = max(frames)+1
        frames[c] = {'dim': len(b), 'B': encode_basis(b), 'A': encode_basis(perpendicular(b))}
        spaces[c] = b
        key_to_id[b] = c
        created.append(c)
        return c

    ops = []
    where = dict(enumerate(native['start'][:222]))

    def unit_move(i, target, preferred=None):
        current = where[i]
        if current == target:
            return
        small, large = spaces[current], spaces[target]
        need(len(small) != len(large), ('no alias-only route', i, current, target))
        if len(small) < len(large):
            need(included(small, large), ('ascending route inclusion', i, current, target))
            candidates = ([preferred] if preferred is not None else [])+list(large)
            basis = small
            for v in candidates:
                nb = rref(list(basis)+[v])
                if len(nb) == len(basis):
                    continue
                need(included(nb, large), 'intermediate flag inside destination')
                nxt = target if len(nb) == len(large) else chart(nb)
                ops.append(['MOVE', i, current, nxt])
                current, basis = nxt, nb
            need(current == target, 'ascending flag completed')
        else:
            need(included(large, small), ('descending route inclusion', i, current, target))
            # Build the same increasing subspace flag and traverse it backward.
            basis = large
            ids = [target]
            for v in small:
                nb = rref(list(basis)+[v])
                if len(nb) == len(basis):
                    continue
                nxt = current if len(nb) == len(small) else chart(nb)
                ids.append(nxt)
                basis = nb
            need(ids[-1] == current, 'descending flag constructed')
            for nxt in reversed(ids[:-1]):
                ops.append(['MOVE', i, current, nxt])
                current = nxt
        where[i] = target

    def add(a, b, c):
        need(where.get(a) == where.get(b) == c and a != b, ('author cochart', a, b, c))
        ops.append(['ADD', a, b, c])
        return len(ops)-1

    def init(i, c):
        need(i not in where, 'new owned lifetime')
        ops.append(['INIT', i, c])
        where[i] = c
        return len(ops)-1

    def clear(i, c):
        need(where.get(i) == c, 'clear cochart')
        ops.append(['CLEAR', i, c])
        del where[i]

    cache0, cache1, packet0, packet1 = 222, 223, 224, 225
    f1 = native['final'][112]
    common_chart = chart(eye[2:8])
    bridge = tuple(eye[0][j]+eye[1][j] for j in range(8))
    roots = [[F(x) for x in native['frames'][str(native['start'][i])]['B'][0]] for i in range(111)]
    common = [i for i in range(8, 111) if roots[i][0] == roots[i][1] == 0]
    exclusive = [[i for i in range(8, 111) if roots[i][p] == 0 and roots[i][1-p] != 0] for p in (0, 1)]
    need([len(common)]+[len(v) for v in exclusive] == [22, 27, 31], 'joint partition sizes')
    group_data = []
    for p in (0, 1):
        first = [i for i in exclusive[p] if roots[i][2] == 0]
        second = [i for i in exclusive[p] if roots[i][2] != 0]
        need(first and second and all(roots[i][3] == 0 for i in second), 'two coordinate predecessor cover')
        group_data.append([(first, chart([v for j, v in enumerate(eye) if j not in (p, 2)])),
                           (second, chart([v for j, v in enumerate(eye) if j not in (p, 3)]))])
    init(cache0, f0)
    # Both unknown-Y records carry their own independent y column.
    for y in (111, 112):
        unit_move(y, common_chart)
    preloads = []
    for i in range(2, 8):
        unit_move(i, common_chart)
        preloads.append(add(111, i, common_chart))
        preloads.append(add(112, i, common_chart))
        unit_move(i, hub, preferred=bridge)
    unit_move(111, f0)
    unit_move(112, f1)
    for i, y, facet in [(1, 111, f0), (0, 112, f1)]:
        unit_move(i, facet)
        preloads.append(add(y, i, facet))
        unit_move(i, hub)
    # One common aggregate; no source is restarted for the second receiver.
    carrier = common[0]
    unit_move(carrier, common_chart)
    for i in common[1:]:
        unit_move(i, common_chart)
        add(carrier, i, common_chart)
        unit_move(i, hub, preferred=bridge)
    copy_birth = init(cache1, common_chart)
    copy_value = add(cache1, carrier, common_chart)
    copy_move = len(ops)
    unit_move(cache1, f1)
    need(len(ops) == copy_move+1, 'one charged rank-one upward copy')
    unit_move(carrier, f0)
    common_deposit = add(cache0, carrier, f0)
    unit_move(carrier, hub)
    common_restore = [add(carrier, i, hub) for i in common[1:]]
    acquired = [{'kind': 'common', 'carrier': carrier, 'group': common,
                 'chart': common_chart, 'deposit_operation': common_deposit,
                 'restoration_operations': common_restore}]
    for p in (0, 1):
        facet, cache = ((f0, cache0), (f1, cache1))[p]
        for indices, c in group_data[p]:
            carrier = indices[0]
            need(len(spaces[c]) == 6 and included(spaces[c], spaces[facet]), 'rank-six exclusive chart')
            need(all(included(spaces[native['start'][i]], spaces[c]) for i in indices), 'exclusive source availability')
            unit_move(carrier, c)
            for i in indices[1:]:
                unit_move(i, c)
                add(carrier, i, c)
                unit_move(i, hub, preferred=eye[p])
            unit_move(carrier, facet)
            deposit = add(cache, carrier, facet)
            unit_move(carrier, hub)
            restores = [add(carrier, i, hub) for i in indices[1:]]
            acquired.append({'kind': 'exclusive'+str(p), 'carrier': carrier,
                             'group': indices, 'chart': c, 'deposit_operation': deposit,
                             'restoration_operations': restores})
    for i in range(111):
        unit_move(i, hub, preferred=bridge)
    prefix = len(ops)-1
    handoffs = []
    snapshots = [copy_value, copy_move, prefix]
    for p, facet, cache, packet in [(0, f0, cache0, packet0), (1, f1, cache1, packet1)]:
        local = [i for i in range(8, 111) if roots[i][p] == 0]
        canonical = list(range(8))+local
        birth = init(packet, hub)
        for i in canonical:
            add(packet, i, hub)
        packet_ready = len(ops)-1
        unit_move(packet, facet)
        make_u = add(cache, packet, facet)
        reload_l = add(packet, cache, facet)
        complete_y = add(111+p, cache, facet)
        retain_k = add(cache, packet, facet)
        clear(cache, facet)
        unit_move(packet, zero)
        ground = len(ops)-1
        clear(packet, zero)
        snapshots.extend([birth, packet_ready, make_u, reload_l, complete_y, retain_k, ground])
        handoffs.append({'coordinate': p, 'cache': cache, 'packet': packet, 'facet': facet,
                         'packet_birth_operation': birth, 'packet_ready_snapshot': packet_ready,
                         'make_u_operation': make_u, 'reload_l_operation': reload_l,
                         'complete_Y_operation': complete_y, 'retain_K_operation': retain_k,
                         'packet_ground_snapshot': ground,
                         'local_row_hex': hex(sum(1 << i for i in local)),
                         'canonical_row_hex': hex(sum(1 << i for i in canonical))})
    for i in range(2, 111):
        unit_move(111+i, native['final'][111+i])
    used = set(native['start'][:222]+native['final'][:222])
    for e in ops:
        used.update(e[-2:] if e[0] == 'MOVE' else [e[-1]])
    word = {'schema': 'BIT-joint-L0-L1-acquisition-one-outward-copy-v1',
            'public': 222, 'owned_fields': 4, 'hub': hub,
            'start': native['start'][:222], 'final': native['final'][:222],
            'frames': {c: frames[c] for c in sorted(used)}, 'program': ops,
            'directions': {str(cache0): 'stationary', str(cache1): 'up',
                           str(packet0): 'down', str(packet1): 'down'},
            'snapshot_indices': snapshots,
            'scope': 'Actual scalar-F2 partial source. L0 and L1 jointly acquired before packets; all111 original X restored; Y0/Y1 complete, other109 Y unchanged. One additional upward rank-one owned MOVE charged. No complete source or kappa.'}
    meta = {'facets': [f0, f1], 'common_chart': common_chart,
            'groups': acquired, 'Y_preload_operations': preloads,
            'copy_birth_operation': copy_birth, 'copy_value_operation': copy_value,
            'extra_copy_MOVE_operation': copy_move,
            'both_local_caches_and_restored_X_snapshot': prefix,
            'handoffs': handoffs, 'new_charts': [c for c in created if c in used],
            'common_support_indices': common,
            'common_row_hex': hex(sum(1 << i for i in common))}
    return word, meta


def main(args):
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'native exact source')
    native = json.loads(gzip.decompress(raw))
    word, metadata = emit(native)
    receipt = replay(word)
    expected = [1 << i for i in range(222)]
    expected[111] ^= 1
    expected[112] ^= 2
    need(receipt['rows'] == expected, 'all222 arbitrary-input columns')
    need(receipt['paid_profile'] == {1: 1571}, 'joint partial paid profile')
    need(receipt['owned_lifetimes'] == 4 and receipt['peak_owned'] == 3, 'owned lifetimes and peak')
    s = receipt['snapshots']
    prefix = s[str(metadata['both_local_caches_and_restored_X_snapshot'])]
    need(prefix['all_X_restored_at_Hub'], 'all originals restored before packet phase')
    for h in metadata['handoffs']:
        need(prefix['rows'][str(h['cache'])] == h['local_row_hex'], 'both actual pure local caches coexist')
        need(s[str(h['make_u_operation'])]['rows'][str(h['cache'])] == hex(255), 'class mode at actual facet')
        need(s[str(h['reload_l_operation'])]['rows'][str(h['packet'])] == h['local_row_hex'], 'singular packet reload')
        need(s[str(h['retain_K_operation'])]['rows'][str(h['cache'])] == h['canonical_row_hex'], 'displaced global retention')
    expected_clears = [v for h in metadata['handoffs'] for v in [h['canonical_row_hex'], h['local_row_hex']]]
    need([c['row_hex'] for c in receipt['clear_rows']] == expected_clears, 'exact owned erasure operands')
    visits = {str(f): [i for i in range(111) if f in receipt['routes'][i]] for f in metadata['facets']}
    need(len(visits[str(metadata['facets'][0])]) == 4 and len(visits[str(metadata['facets'][1])]) == 3, 'facet original-arrival counts')
    controls = []
    def mutated_without(index):
        bad = json.loads(json.dumps(word)); del bad['program'][index];bad['snapshot_indices'] = [];return bad
    for name, index in [('omit_common_copy_value', metadata['copy_value_operation']),
                        ('omit_common_carrier_restore', metadata['groups'][0]['restoration_operations'][0]),
                        ('omit_F0_exclusive_deposit', metadata['groups'][1]['deposit_operation']),
                        ('omit_F1_exclusive_deposit', metadata['groups'][3]['deposit_operation']),
                        ('omit_Y1_coordinate_preload', metadata['Y_preload_operations'][1])]:
        br = replay(mutated_without(index))
        wrong = [i for i,(a,b) in enumerate(zip(br['rows'], expected)) if a != b]
        need(wrong, ('semantic control', name))
        controls.append({'name': name, 'rejected': True, 'wrong_public_rows': wrong})
    try:
        replay(mutated_without(metadata['extra_copy_MOVE_operation']))
    except ValueError:
        controls.append({'name': 'pretend_shared_copy_is_free_at_F1', 'rejected': True, 'reason': 'cochart violation'})
    else:
        raise ValueError('unpaid shared copy passed')
    for h in metadata['handoffs']:
        bad = json.loads(json.dumps(word));bad['snapshot_indices'] = []
        i,j=h['make_u_operation'],h['reload_l_operation']
        bad['program'][i],bad['program'][j] = bad['program'][j],bad['program'][i]
        need(replay(bad)['rows'] != expected, 'singular exchange order control')
        controls.append({'name': 'reverse_exchange_order_'+str(h['coordinate']), 'rejected': True})
    args.output.mkdir(parents=True, exist_ok=True)
    data = json.dumps(word, separators=(',', ':'), sort_keys=True).encode()
    zipped = gzip.compress(data, mtime=0)
    (args.output/'WORD.json.gz').write_bytes(zipped)
    receipt.pop('rows'); receipt.pop('routes')
    result = {'status': 'PASS_ACTUAL_JOINT_L0_L1_WITH_ONE_PAID_OUTWARD_COPY',
              'native_sha256': PIN,
              'builder_predecessor_sha256': 'cf783adafb7fcb724ec4ea37e769e1003ea83fe1076cbec10dcb47ddb07dd4d8',
              'word_sha256': hashlib.sha256(zipped).hexdigest(),
              'canonical_word_json_sha256': hashlib.sha256(data).hexdigest(),
              'metadata': metadata, 'receipt': receipt,
              'original_X_facet_arrivals': visits, 'negative_controls': controls,
              'completed_Y_indices': [0,1], 'remaining_Y_indices': list(range(2,111)),
              'extra_owned_upward_profile': {1:1},
              'hypothetical_eight_packet_unit_profile_after_six_more_routes': {1:1619},
              'complete_source_claimed': False, 'complete_kappa_claimed': False,
              'scope': word['scope']}
    (args.output/'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': result['status'], 'counts': receipt['counts'],
                      'paid_profile': receipt['paid_profile'], 'owned_peak': receipt['peak_owned'],
                      'source_group_sizes': [len(g['group']) for g in metadata['groups']],
                      'facet_X_arrivals': visits}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
