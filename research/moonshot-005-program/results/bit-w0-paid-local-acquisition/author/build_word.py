#!/usr/bin/env python3
"""Paid pre-Hub L0 acquisition and a literal K0/L0 mode exchange.

This emits a partial 222-input BIT word: all X restored, only Y0 completed.
Every moving record is an original X/Y or the one designated packet.
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
            need((dd > dc if a < 222 else dd < dc), ('declared monotone direction', n, op))
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
            snapshots[str(n)] = {'rows': {str(i): hex(rows[i]) for i in (111, 222, 223) if i in rows},
                                 'all_X_restored_at_Hub': all(rows[i] == 1 << i and where[i] == word['hub'] for i in range(111))}
    need(set(rows) == set(range(222)), 'all owned lifetimes retired')
    need([where[i] for i in range(222)] == word['final'], 'all public endpoint charts')
    return {'rows': [rows[i] for i in range(222)], 'counts': dict(counts),
            'paid_profile': dict(sorted(paid.items())), 'owned_lifetimes': lifetimes,
            'peak_owned': peak, 'clear_rows': clears, 'snapshots': snapshots,
            'routes': routes, 'exact_nested_move_pairs': len(move_pairs)}


def emit(native, certificate):
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

    def unit_move(i, target, prefer_e0=False):
        current = where[i]
        if current == target:
            return
        small, large = spaces[current], spaces[target]
        need(len(small) != len(large), ('no alias-only route', i, current, target))
        if len(small) < len(large):
            need(included(small, large), ('ascending route inclusion', i, current, target))
            candidates = ([eye[0]] if prefer_e0 else [])+list(large)
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

    cache, packet = 222, 223
    init(cache, f0)
    # Public Y0 collects six coordinate inputs at a genuine proper predecessor.
    c6 = chart(eye[1:7])
    unit_move(111, c6)
    y_preload = []
    for i in range(1, 7):
        unit_move(i, c6)
        y_preload.append(add(111, i, c6))
        unit_move(i, hub, prefer_e0=True)
    unit_move(111, f0)
    unit_move(7, f0)
    y_preload.append(add(111, 7, f0))
    unit_move(7, hub)
    groups = certificate['l0_three_arrival_groups']
    acquired = []
    group_indices = []
    for g in groups:
        indices = g['indices']
        carrier = g['carrier']
        need(carrier == indices[0], 'deterministic carrier')
        c = chart(g['chart_basis'])
        need(len(spaces[c]) == 6 and included(spaces[c], spaces[f0]), 'proper acquisition chart')
        need(all(included(spaces[native['start'][i]], spaces[c]) for i in indices), 'each raw input actually lies in acquisition chart')
        unit_move(carrier, c)
        for i in indices[1:]:
            unit_move(i, c)
            add(carrier, i, c)
            # In rank6 -> Hub refinement, the intermediate facet contains e0,
            # so these donors do not secretly add F0 arrivals.
            unit_move(i, hub, prefer_e0=True)
        unit_move(carrier, f0)
        deposit = add(cache, carrier, f0)
        unit_move(carrier, hub)
        restorations = [add(carrier, i, hub) for i in indices[1:]]
        acquired.append({'carrier': carrier, 'group': indices, 'chart': c,
                         'deposit_operation': deposit, 'restoration_operations': restorations})
        group_indices.extend(indices)
    roots = [[F(x) for x in native['frames'][str(native['start'][i])]['B'][0]] for i in range(111)]
    local_indices = [i for i in range(8, 111) if roots[i][0] == 0]
    need(sorted(group_indices) == local_indices and len(set(group_indices)) == 49, 'exact L0 acquisition partition')
    for i in range(111):
        unit_move(i, hub, prefer_e0=True)
    before_packet = len(ops)-1
    birth = init(packet, hub)
    canonical_indices = [i for i in range(111) if i == 0 or roots[i][0] == 0]
    need(len(canonical_indices) == 57, 'K0 source support')
    for i in canonical_indices:
        add(packet, i, hub)
    packet_ready = len(ops)-1
    unit_move(packet, f0)
    exchange_begin = len(ops)
    # S=L0 and P=K0. This two-ADD exchange has packet-through D=0.
    make_u0 = add(cache, packet, f0)
    reload_l0 = add(packet, cache, f0)
    complete_y0 = add(111, cache, f0)
    retain_k0 = add(cache, packet, f0)
    clear(cache, f0)
    unit_move(packet, zero)
    ground = len(ops)-1
    clear(packet, zero)
    for i in range(1, 111):
        unit_move(111+i, native['final'][111+i])
    snapshots = [before_packet, birth, packet_ready, make_u0, reload_l0,
                 complete_y0, retain_k0, ground]
    used = set(native['start'][:222]+native['final'][:222])
    for e in ops:
        used.update(e[-2:] if e[0] == 'MOVE' else [e[-1]])
    word = {'schema': 'BIT-W0-pre-Hub-local-acquisition-and-singular-exchange-v1',
            'public': 222, 'owned_fields': 2, 'hub': hub,
            'start': native['start'][:222], 'final': native['final'][:222],
            'frames': {c: frames[c] for c in sorted(used)}, 'program': ops,
            'snapshot_indices': snapshots,
            'scope': 'Literal scalar-F2 partial source. All111 original X restored; Y0=y0+x0; other110 Y unchanged. One monotone packet; one charged stationary cache. No complete111-target source, supplier or kappa.'}
    meta = {'f0': f0, 'coordinate_Y_predecessor': c6, 'three_groups': acquired,
            'Y_coordinate_preload_operations': y_preload,
            'all_X_restored_before_packet_birth_snapshot': before_packet,
            'packet_birth_operation': birth, 'packet_ready_snapshot': packet_ready,
            'exchange_begin': exchange_begin, 'make_u0_operation': make_u0,
            'reload_l0_operation': reload_l0, 'complete_Y0_operation': complete_y0,
            'retain_K0_operation': retain_k0, 'packet_ground_snapshot': ground,
            'new_charts': [c for c in created if c in used],
            'l0_row_hex': hex(sum(1 << i for i in local_indices)),
            'k0_row_hex': hex(sum(1 << i for i in canonical_indices)),
            'u0_row_hex': hex(255)}
    return word, meta


def main(args):
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'native source pin')
    native = json.loads(gzip.decompress(raw))
    support_bytes = args.support.read_bytes()
    certificate = json.loads(support_bytes)
    need(certificate['native_sha256'] == PIN, 'support source identity')
    word, metadata = emit(native, certificate)
    receipt = replay(word)
    expected = [1 << i for i in range(222)]
    expected[111] ^= 1
    need(receipt['rows'] == expected, 'all222 arbitrary-input endpoint rows')
    need(receipt['paid_profile'] == {1: 1562}, 'exact complete-original-path movement count')
    need(receipt['owned_lifetimes'] == receipt['peak_owned'] == 2, 'one stationary cache and one packet')
    s = receipt['snapshots']
    need(s[str(metadata['all_X_restored_before_packet_birth_snapshot'])]['all_X_restored_at_Hub'], 'no causal cycle: X restored before K0 birth')
    need(s[str(metadata['make_u0_operation'])]['rows']['222'] == metadata['u0_row_hex'], 'actual class-mode observation')
    need(s[str(metadata['reload_l0_operation'])]['rows']['223'] == metadata['l0_row_hex'], 'actual new packet payload')
    need(s[str(metadata['retain_K0_operation'])]['rows']['222'] == metadata['k0_row_hex'], 'actual old global mode retained')
    need([c['row_hex'] for c in receipt['clear_rows']] == [metadata['k0_row_hex'], metadata['l0_row_hex']], 'explicit erasure operands')
    visits = [i for i in range(111) if metadata['f0'] in receipt['routes'][i]]
    need(visits == [7, 8, 9, 12], 'exact four original-X F0 arrivals')
    controls = []
    for name, index in [('omit_first_group_deposit', metadata['three_groups'][0]['deposit_operation']),
                        ('omit_first_carrier_restoration', metadata['three_groups'][0]['restoration_operations'][0]),
                        ('omit_unknown_Y_coordinate_preload', metadata['Y_coordinate_preload_operations'][2]),
                        ('omit_singular_packet_reload', metadata['reload_l0_operation'])]:
        bad = json.loads(json.dumps(word))
        del bad['program'][index]
        bad['snapshot_indices'] = []
        br = replay(bad)
        wrong = [i for i, (a, b) in enumerate(zip(br['rows'], expected)) if a != b]
        clear_wrong = [c['row_hex'] for c in br['clear_rows']] != [metadata['k0_row_hex'], metadata['l0_row_hex']]
        need(wrong or clear_wrong, ('semantic negative control', name))
        controls.append({'name': name, 'rejected': True, 'wrong_public_rows': wrong,
                         'wrong_historical_or_erasure_rows': clear_wrong})
    # Placing the K0 acquisition before a real group carrier reaches Hub is
    # syntactically invalid; exact cochart validation must reject it.
    bad = json.loads(json.dumps(word))
    early = metadata['three_groups'][0]['deposit_operation']
    bad['program'].insert(early, ['ADD', 8, 0, word['hub']])
    bad['snapshot_indices'] = []
    try:
        replay(bad)
    except ValueError:
        controls.append({'name': 'early_Hub_read_of_F0_carrier', 'rejected': True})
    else:
        raise ValueError('early nonlocal read passed')
    # Reverse the two load-bearing ADDs: this loses the desired zero-through
    # cell and changes the actual receiver row.
    bad = json.loads(json.dumps(word))
    i, j = metadata['make_u0_operation'], metadata['reload_l0_operation']
    bad['program'][i], bad['program'][j] = bad['program'][j], bad['program'][i]
    bad['snapshot_indices'] = []
    br = replay(bad)
    need(br['rows'] != expected, 'exchange-order control')
    controls.append({'name': 'reverse_exchange_ADD_order', 'rejected': True})
    args.output.mkdir(parents=True, exist_ok=True)
    word_bytes = json.dumps(word, separators=(',', ':'), sort_keys=True).encode()
    gz = gzip.compress(word_bytes, mtime=0)
    (args.output/'WORD.json.gz').write_bytes(gz)
    receipt.pop('rows')
    receipt.pop('routes')
    result = {'status': 'PASS_ACTUAL_L0_ACQUISITION_AND_SINGULAR_HANDOFF',
              'native_sha256': PIN, 'support_certificate_sha256': hashlib.sha256(support_bytes).hexdigest(),
              'word_sha256': hashlib.sha256(gz).hexdigest(),
              'canonical_word_json_sha256': hashlib.sha256(word_bytes).hexdigest(),
              'metadata': metadata, 'receipt': receipt, 'negative_controls': controls,
              'completed_Y_indices': [0], 'remaining_Y_indices': list(range(1, 111)),
              'historical_global_modes': ['L0 at first ground arrival', 'K0 at the singular F0 cell'],
              'historical_global_rank': 2, 'F0_original_X_arrivals': visits,
              'ordinary_ADD_count': receipt['counts']['ADD'],
              'owned_erasure_retained': True,
              'no_new_complete_kappa': True,
              'scope': word['scope']}
    (args.output/'WORD-RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': result['status'], 'counts': receipt['counts'],
                      'paid_profile': receipt['paid_profile'], 'completed_Y': [0],
                      'owned_lifetimes': receipt['owned_lifetimes'], 'new_chart_count': len(metadata['new_charts'])}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--support', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
