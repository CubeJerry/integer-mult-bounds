#!/usr/bin/env python3
"""Actual-ground normalization of arbitrary Y and known X columns.

Constructive boundary lemma, with a native111 physical control.  This is not
a complete BIT supplier.  The separate endpoint checker imports no A/R code.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

from release_projection import N, chart, rref, require, replay
from price_projection import moment, record


def evaluate(w):
    """Legal full native replay, retaining unrestricted final linear maps."""
    cs = {k: chart(v) for k, v in w['charts'].items()}
    v = {f'X{i}': 1 << i for i in range(N)}
    v.update({f'Y{i}': 1 << (N+i) for i in range(N)})
    at = {f'X{i}': f'L{i}' for i in range(N)}
    at.update({f'Y{i}': 'zero' for i in range(N)})
    own, ever = set(), set()
    memo, states = {}, []
    counts, profile = Counter(), Counter()
    dirty = peak = 0

    def sub(a, b):
        if (a, b) not in memo:
            memo[a, b] = len(rref(cs[a]+cs[b])[0]) == len(cs[b])
        return memo[a, b]

    for k, o in enumerate(w['operations']):
        states.append((v.copy(), at.copy()))
        op, n, *q = o
        counts[op] += 1
        if op == 'INIT':
            require(n not in v and n not in ever, (k, 'birth', n))
            require(q[0] in cs, (k, 'birth chart'))
            v[n], at[n] = 0, q[0]
            own.add(n); ever.add(n)
        elif op == 'ADD':
            d = q[0]
            require(n != d and n in v and d in v, (k, 'ADD labels', o))
            require(sub(at[n], at[d]) and sub(at[d], at[n]),
                    (k, 'actual ADD co-location', o, at[n], at[d]))
            v[d] ^= v[n]
        elif op == 'MOVE':
            require(n in v and q[0] in cs, (k, 'MOVE labels', o))
            old, new = at[n], q[0]
            require(sub(new, old) if n in own else sub(old, new),
                    (k, 'monotone MOVE', o, old))
            jump = abs(len(cs[old])-len(cs[new]))
            require(jump > 0, (k, 'strict MOVE', o))
            profile[jump] += 1; at[n] = new
        elif op == 'CLEAR':
            require(n in own, (k, 'owned CLEAR', o))
            dirty += bool(v[n]); own.remove(n)
            del v[n], at[n]
        else:
            raise ValueError((k, 'opcode', o))
        peak = max(peak, len(own))
    require(not own and len(v) == 2*N, 'complete owned lifetimes')
    require(all(at[f'X{i}'] == 'Hub' and at[f'Y{i}'] == f'F{i}'
                for i in range(N)), 'all original final charts')
    return v, at, states, {'counts': dict(counts),
        'movement_profile': dict(sorted(profile.items())),
        'dirty_CLEAR': dirty, 'peak_owned': peak}


def inverse_add_word(rows):
    """Eliminate binary M to I; these actual row ADDs implement M^{-1}."""
    a, ops = list(rows), []
    n = len(a)
    require(all(0 <= r < 1 << n for r in a), 'square binary Y matrix')

    def add(src, dst):
        require(src != dst, 'distinct row ADD')
        a[dst] ^= a[src]; ops.append(['ADD', f'Y{src}', f'Y{dst}'])

    for col in range(n):
        pivot = next((j for j in range(col, n) if a[j] >> col & 1), None)
        require(pivot is not None, ('singular homogeneous Y map', col))
        if pivot != col:
            add(pivot, col); add(col, pivot); add(pivot, col)
        for j in range(n):
            if j != col and a[j] >> col & 1:
                add(col, j)
    require(a == [1 << j for j in range(n)], 'inverse elimination identity')
    return ops


def source_representation(row, donors):
    basis = {}
    for j, (_, value) in enumerate(donors):
        comb = 1 << j
        while value:
            p = value.bit_length()-1
            if p in basis:
                value ^= basis[p][0]; comb ^= basis[p][1]
            else:
                basis[p] = value, comb
                break
    comb = 0
    while row:
        p = row.bit_length()-1
        require(p in basis, ('error outside actual ground source span', p))
        row ^= basis[p][0]; comb ^= basis[p][1]
    return [donors[j][0] for j in range(len(donors)) if comb >> j & 1]


def normalize(w, boundary, donor_names):
    final, _, states, report = evaluate(w)
    require(all(final[f'X{i}'] == 1 << i for i in range(N)),
            'original X endpoint must already be raw and independent of y')
    v, at = states[boundary]
    require(all(v[f'Y{i}'] == 1 << (N+i) and at[f'Y{i}'] == 'zero'
                for i in range(N)), 'all actual Y raw at ground boundary')
    donors = [(n, v[n]) for n in donor_names]
    require(all(at[n] == 'zero' and 0 <= row < 1 << N for n, row in donors),
            'actual pure-X ground donors')
    require(all(row < 1 << N for n, row in v.items() if not n.startswith('Y')),
            'only Y contains arbitrary y at normalization boundary')
    M = [final[f'Y{i}'] >> N for i in range(N)]
    inv = inverse_add_word(M)
    F = [final[f'Y{i}'] & ((1 << N)-1) for i in range(N)]
    desired = [(1 << i) if i in w['targets'] else 0 for i in range(N)]
    errors = [a ^ b for a, b in zip(desired, F)]
    preloads = [['ADD', n, f'Y{i}'] for i, error in enumerate(errors)
                for n in source_representation(error, donors)]
    out = copy.deepcopy(w)
    out['operations'] = (w['operations'][:boundary]+preloads+inv+
                         w['operations'][boundary:])
    out['schema'] = 'actual-ground-output-normalization-v1'
    out['ground_normalization'] = {'boundary': boundary,
        'source_owners': donor_names, 'preload_operations': preloads,
        'inverse_operations': inv, 'homogeneous_Y_rows_hex': [hex(r) for r in M],
        'unnormalized_X_increment_rows_hex': [hex(r) for r in F],
        'desired_minus_actual_rows_hex': [hex(r) for r in errors]}
    out['scope'] = ('All111 raw X endpoints and all111 arbitrary Y columns are '
        'physically normalized;46 completed increments. Constructive ground '
        'interface control, not a completed supplier or a new kappa.')
    return out, report


def build_control(base):
    w = {k: copy.deepcopy(base[k]) for k in
         ['source_path', 'source_sha256', 'charts', 'targets']}
    w['charts']['NORM_J01'] = {'kind': 'span',
        'rows': base['charts']['L0']['rows']+base['charts']['L1']['rows']}
    ops = []
    names = [f'KNOWN_RAW{i}' for i in w['targets']]
    for i, n in zip(w['targets'], names):
        ops.extend([['INIT', n, f'L{i}'], ['ADD', f'X{i}', n], ['MOVE', n, 'zero']])
    boundary = len(ops)
    ops.extend([['MOVE', f'Y{i}', 'L0'] for i in [2, 3, 4]])
    ops.extend([['ADD', 'X0', 'Y2'], ['ADD', 'Y2', 'Y3'],
                ['ADD', 'Y3', 'Y4'], ['MOVE', 'Y2', 'NORM_J01'],
                ['MOVE', 'Y3', 'NORM_J01'], ['MOVE', 'X1', 'NORM_J01'],
                ['ADD', 'X1', 'Y3'], ['ADD', 'Y3', 'Y2']])
    ops.extend([['MOVE', f'X{i}', 'Hub'] for i in range(N)])
    ops.extend([['MOVE', f'Y{i}', f'F{i}'] for i in range(N)])
    ops.extend([['CLEAR', n] for n in names])
    w['operations'] = ops
    w['schema'] = 'unnormalized-output-carrier-control-v1'
    return w, boundary, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    bp = a.repo/'research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json'
    raw = bp.read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
        '27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd', 'base pin')
    base = json.loads(raw)
    source = (a.repo/base['source_path']).read_bytes()
    require(hashlib.sha256(source).hexdigest() == base['source_sha256'], 'native source pin')
    roots = json.loads(source)['native_roots']
    for i, r in enumerate(roots):
        require(chart(base['charts'][f'L{i}']) == chart({'kind':'span','rows':[r]}), ('native L', i))
        require(chart(base['charts'][f'F{i}']) == chart({'kind':'ann','rows':[r]}), ('native F', i))
    un, cut, names = build_control(base)
    word, before = normalize(un, cut, names)
    after, _, _ = replay(word)
    require(before['movement_profile'] == after['movement_profile'], 'zero new movement')
    require(before['counts']['INIT'] == after['counts']['INIT'] and
            before['counts']['CLEAR'] == after['counts']['CLEAR'], 'zero extra owners')
    M = word['ground_normalization']['homogeneous_Y_rows_hex']
    require([int(M[i], 16) for i in [2,3,4]] ==
        [1 << 3, (1 << 2) ^ (1 << 3), (1 << 2) ^ (1 << 3) ^ (1 << 4)],
        'nontrivial actual Y forwarding map')
    controls = []

    def reject(label, fn):
        try:
            fn()
        except (ValueError, KeyError) as e:
            controls.append({'control': label, 'rejected': True, 'reason': str(e)})
        else:
            raise ValueError(('accepted negative control', label))

    reject('omit all actual ground normalization', lambda: replay(un))
    bad = copy.deepcopy(word)
    for o in word['ground_normalization']['inverse_operations']:
        bad['operations'].remove(o)
    reject('omit invertible Y preconditioning', lambda: replay(bad))
    bad_offset = copy.deepcopy(word)
    bad_offset['operations'].remove(['ADD', 'KNOWN_RAW1', 'Y2'])
    reject('omit actual known-column offset', lambda: replay(bad_offset))
    bad_ground = copy.deepcopy(word)
    bad_ground['operations'].remove(['MOVE', 'KNOWN_RAW1', 'zero'])
    reject('claim ground donor before physical arrival', lambda: replay(bad_ground))
    singular = copy.deepcopy(un)
    singular['operations'][cut:cut] = [['INIT', 'SINGULAR_Y_CACHE', 'zero'],
        ['ADD', 'Y2', 'SINGULAR_Y_CACHE'], ['ADD', 'SINGULAR_Y_CACHE', 'Y2'],
        ['CLEAR', 'SINGULAR_Y_CACHE']]
    reject('singular final Y transfer cannot be normalized', lambda: normalize(singular, cut, names))
    unknown = copy.deepcopy(un)
    unknown['operations'][cut:cut] = [['MOVE', 'Y0', 'L5'], ['ADD', 'X5', 'Y0']]
    reject('unknown input error outside actual ground span', lambda: normalize(unknown, cut, names))
    contaminated = copy.deepcopy(un)
    at = contaminated['operations'].index(['ADD', 'X0', 'Y2'])
    contaminated['operations'].insert(at+1, ['ADD', 'Y2', 'X0'])
    reject('uncorrected original X y contamination', lambda: normalize(contaminated, cut, names))
    # Explicit second independent whole-record coordinate block.
    final, _, _, _ = evaluate(word)
    for i in range(N):
        for lane in range(2):
            for name in [f'X{i}', f'Y{i}']:
                row = sum(1 << (2*j+lane) for j in range(2*N) if final[name] >> j & 1)
                desired = (1 << (2*i+lane)) if name.startswith('X') else (
                    (1 << (2*(N+i)+lane)) ^ ((1 << (2*i+lane)) if i in word['targets'] else 0))
                require(row == desired, ('width-two tensor column', name, lane))
    result = {'status': 'PASS_ACTUAL_GROUND_OUTPUT_NORMALIZATION_CONTROL',
        'source_sha256': base['source_sha256'], 'base_sha256': hashlib.sha256(raw).hexdigest(),
        'before': before, 'after': after, 'physical_source_rows': len(names),
        'actual_Y_forwarding_roles': [2,3,4], 'proper_forwarding_charts': ['L0','NORM_J01'],
        'new_ground_preload_ADDs': len(word['ground_normalization']['preload_operations']),
        'new_ground_inverse_ADDs': len(word['ground_normalization']['inverse_operations']),
        'all222_endpoint_columns': True, 'explicit_width_two_columns': 444,
        'whole_movement_moment': record(moment(after['movement_profile'])),
        'controls': controls, 'scope': word['scope']}
    a.out.mkdir(parents=True, exist_ok=True)
    for name, obj in [('UNNORMALIZED-WORD', un), ('WORD', word)]:
        data = (json.dumps(obj, indent=2)+'\n').encode()
        (a.out/(name+'.json')).write_bytes(data)
        result[name.lower().replace('-', '_')+'_sha256'] = hashlib.sha256(data).hexdigest()
    (a.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status','after','new_ground_preload_ADDs',
        'new_ground_inverse_ADDs','word_sha256','whole_movement_moment']}, indent=2))


if __name__ == '__main__':
    main()
