"""Three real proper fields serve twelve D4 receivers by cyclic cache flags.

Author construction, using the credited retained SymPy native interpreter.
It deliberately changes the first-retention and donor-route source contracts.
No executable all111 completion or new kappa is asserted.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path('/workspace/scratch/b421dd0c4c1e')
PINS = {
    'paid46': '27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd',
    'pruned78': 'c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245',
}
SOURCE_PIN = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


def trace(ops):
    v = {f'X{i}': 1 << i for i in range(111)}
    v.update({f'Y{i}': 1 << (111+i) for i in range(111)})
    at = {f'X{i}': f'L{i}' for i in range(111)}
    at.update({f'Y{i}': 'zero' for i in range(111)})
    out = []
    for op, n, *q in ops:
        out.append((v.copy(), at.copy()))
        if op == 'INIT':
            v[n], at[n] = 0, q[0]
        elif op == 'MOVE':
            at[n] = q[0]
        elif op == 'ADD':
            v[q[0]] ^= v[n]
        elif op == 'CLEAR':
            del v[n], at[n]
    out.append((v, at))
    return out


def write_json(path, obj):
    raw = (json.dumps(obj, indent=2) + '\n').encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=ROOT/'integer-mult-bounds')
    ap.add_argument('--base', choices=PINS, default='pruned78')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    P = args.repo/'research/moonshot-005-program'
    engine_path = P/'results/bit-leaf-capacity-quotient/author/check.py'
    e = module(engine_path, 'cohort_engine')
    base_path = (P/'results/bit-canonical-mask-source/author/early-paid46/WORD.json'
                 if args.base == 'paid46' else ROOT/'work-S018/A/pruned78/WORD.json')
    raw = base_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PINS[args.base]
    w = json.loads(raw)
    source = (args.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(source).hexdigest() == SOURCE_PIN == w['source_sha256']
    R = json.loads(source)['native_roots']
    C, _, before = e.replay(w, R)
    old = w['operations']
    old_trace = trace(old)
    meet = 'D4_COMMON_MEET'
    meet_record = {'kind': 'ann', 'rows': w['charts']['M1']['rows'] + [R[47]]}
    meet_basis = e.chart(meet_record)
    assert len(meet_basis) == 4 and e.sub(meet_basis, C['M1'])
    D = [i for i in range(111) if e.sub(meet_basis, C[f'F{i}'])]
    assert D == [3, 4, 47, 51, 74, 76, 78, 80, 88, 90, 92, 94]
    ds = set(D)
    assert not any(o[0] == 'ADD' and o[2] in {f'X{i}' for i in D} for o in old)
    assert not any(o[0] == 'ADD' and o[1].startswith('Y') for o in old)
    frames = [list(a) for a in itertools.combinations(D, 4)
              if all(sum(x*y for x, y in zip(R[i], R[j])) == 0
                     for i, j in itertools.combinations(a, 2))]
    assert len(frames) == 3 and sorted(sum(frames, [])) == D
    charts = copy.deepcopy(w['charts'])
    charts[meet] = meet_record
    # Integer chart specifications: the annihilator of the unused frame lines
    # equals C plus the current cyclic interval because each frame spans C-perp.
    flags = {}
    for a in frames:
        for start in range(4):
            j = a[start]
            for length in range(1, 4):
                interval = [a[(start+k) % 4] for k in range(length)]
                lab = f'D4_FLAG_{j}_{length}'
                charts[lab] = {'kind': 'ann', 'rows': [R[z] for z in a if z not in interval]}
                assert len(e.chart(charts[lab])) == 4 + length
                flags[j, length] = lab

    new = []
    new_owners = []
    def emit(*ops):
        new.extend([list(o) for o in ops])
    # Actual raw caches are acquired before ANY old instruction. Each X follows
    # one ascending cyclic flag, then remains raw at Hub for source programming.
    for a in frames:
        for j in a:
            for length in range(1, 4):
                lab = flags[j, length]
                owner = f'D4_RAW_{j}_{length}'
                new_owners.append(owner)
                emit(('MOVE', f'X{j}', lab), ('INIT', owner, lab),
                     ('ADD', f'X{j}', owner))
            emit(('MOVE', f'X{j}', 'Hub'))
    prelude_end = len(new)
    defer_y = []
    old_to_new = {}
    activity = set()
    source_programs = []
    qmask = sum(1 << i for i in D)
    fields = [f'ZFIRST{j}' for j in (3, 4, 5)]
    first_capture = {f'P{j}': next(k for k, o in enumerate(old)
                                  if o == ['ADD', f'P{j}', f'ZFIRST{j}'])
                     for j in (3, 4, 5)}
    first_reset = {f'P{j}': next(k for k, o in enumerate(old)
                                if o == ['ADD', f'ZFIRST{j}', f'P{j}'])
                   for j in (3, 4, 5)}
    for packet, cap in first_capture.items():
        assert not any(o[0] == 'ADD' and o[1] == packet for o in old[:cap])
    injected = set()
    cut_old = w.get('carrier_interface_before_operation',
                    next(k for k, o in enumerate(old) if o[0] == 'CLEAR'))
    interface = None
    decode_begin = None
    def supply_and_decode():
        nonlocal interface, decode_begin
        decode_begin = len(new)
        for field in fields:
            emit(('MOVE', field, meet))
        for field, a in zip(fields, frames):
            for idx, i in enumerate(a):
                emit(('MOVE', f'Y{i}', meet), ('ADD', field, f'Y{i}'))
                for length in range(1, 4):
                    j = a[(idx-length) % 4]
                    lab = flags[j, length]
                    if length == 3:
                        # Use the native endpoint name for the equal geometric facet.
                        assert e.chart(charts[lab]) == C[f'F{i}']
                        lab = f'F{i}'
                    emit(('MOVE', f'Y{i}', lab),
                         ('ADD', f'D4_RAW_{j}_{length}', f'Y{i}'))
        interface = len(new)
    for k, o in enumerate(old):
        if k == cut_old:
            supply_and_decode()
        op, n, *tail = o
        if n.startswith('X') and int(n[1:]) in ds and op == 'MOVE':
            old_to_new[k] = len(new)
            continue
        if op == 'ADD' and n.startswith('X') and int(n[1:]) in ds:
            old_to_new[k] = len(new)
            continue
        if op == 'ADD' and tail[0] in first_capture and k < first_capture[tail[0]]:
            # This complete old source-loading segment has only one eventual
            # reader, its first retention. The old receiver readers are replaced.
            old_to_new[k] = len(new)
            continue
        if n.startswith('Y') and int(n[1:]) in ds:
            old_to_new[k] = len(new)
            continue
        if op == 'ADD' and tail[0].startswith('Y') and int(tail[0][1:]) in ds:
            old_to_new[k] = len(new)
            continue
        if op == 'MOVE' and n.startswith('Y') and int(n[1:]) not in set(w['targets']) | ds:
            # These old unfinished Y have no data reads. Keep them available at
            # ground at the advertised continuation boundary, then close them.
            assert old_trace[k][0][n] == 1 << (111 + int(n[1:]))
            defer_y.append(o)
            old_to_new[k] = len(new)
            continue
        if op == 'MOVE' and n in {'P3', 'P4', 'P5'} and old_trace[k][1][n] == 'Hub':
            j = int(n[1:])
            assert n not in injected and old_trace[k][1][n] == 'Hub'
            for d in frames[j-3]:
                emit(('ADD', f'X{d}', n))
            source_programs.append({'packet': n, 'before_old_operation': k,
                                    'new_program_after': len(new), 'frame': frames[j-3]})
            injected.add(n)
        emit(o)
        old_to_new[k] = len(new)
    assert interface is not None and injected == {'P3', 'P4', 'P5'}
    new.extend(defer_y)
    new.extend([['CLEAR', n] for n in new_owners])
    nw = copy.deepcopy(w)
    nw.update(charts=charts, operations=new, targets=sorted(set(w['targets']) | ds),
              schema='source-projected-D4-three-quartet-cohort-v1',
              base_word_sha256=PINS[args.base],
              source_base_kind=args.base,
              protected_source_contracts={},
              cohort={'meet': meet, 'targets': D, 'frames': frames,
                      'fields': fields, 'donor_projection_coordinates': D,
                      'source_programs': source_programs,
                      'prelude_end': prelude_end,
                      'decode_begin': decode_begin,
                      'continuation_before_operation': interface},
              carrier_interface_before_operation=interface,
              released_carriers=sorted(set(w.get('released_carriers', [])) - ds),
              scope='Completes 52 native receivers using 3 actual retained quartet fields, '
                    'one shared rank4 meet and cyclic raw-cache flags. All222 columns and '
                    'all X restoration checked. Changed old first-retention/source contracts. '
                    'No all111 completion or new kappa.')
    CC, HH, after = e.replay(nw, R)
    nt = trace(new)
    values, locations = nt[interface]
    for i in nw['released_carriers']:
        assert locations[f'X{i}'] == f'L{i}' and values[f'X{i}'] == 1 << i
    for i in set(range(111)) - set(nw['targets']):
        assert locations[f'Y{i}'] == 'zero' and values[f'Y{i}'] == 1 << (111+i)
    for field, a in zip(fields, frames):
        assert locations[field] == meet and values[field] == sum(1 << i for i in a)
    old_owned = {o[1] for o in old if o[0] == 'INIT'}
    ov, oa = old_trace[cut_old]
    ground = [n for n in old_owned if n in ov and ov[n] and C[oa[n]] == C['zero']]
    assert all(ov[n] & qmask == 0 for n in ground)
    assert all(values[n] == ov[n] and CC[locations[n]] == CC['zero'] for n in ground)
    support = sorted({i for n, z in values.items() if n in old_owned | set(new_owners)
                      for i in range(111) if z >> i & 1})
    owners_at_cut = [{'name': n, 'chart': locations[n], 'value_hex': hex(z)}
                     for n, z in values.items() if n in old_owned | set(new_owners)]
    # Check projection covariance at every retained old instruction. The changed
    # principals are exempt only between source programming and their resets.
    comparisons = 0
    for k, o in enumerate(old):
        vv, aa = nt[old_to_new[k]]
        pv, pa = old_trace[k+1]
        for name, z in pv.items():
            if name in fields or (name in first_reset and k < first_reset[name]):
                continue
            if name.startswith(('X', 'Y')) and int(name[1:]) in ds:
                continue
            if name.startswith('Y') and int(name[1:]) not in w['targets']:
                continue
            if name not in vv:
                continue
            assert vv[name] == z & ~qmask, (k, o, name, hex(vv[name]), hex(z & ~qmask))
            assert CC[aa[name]] == C[pa[name]], (k, o, name, 'chart')
            comparisons += 1
    args.out.mkdir(parents=True, exist_ok=True)
    word_sha = write_json(args.out/'WORD.json', nw)
    report = {'status': 'PASS_THREE_RETAINED_FIELDS_D4_TWELVE_RECEIVERS',
              'word_sha256': word_sha, 'base_sha256': PINS[args.base],
              'source_sha256': SOURCE_PIN,
              'credited_interpreter_sha256': hashlib.sha256(engine_path.read_bytes()).hexdigest(),
              'before': before, 'after': after, 'cohort': nw['cohort'],
              'old_targets': w['targets'], 'new_targets': sorted(ds - set(w['targets'])),
              'all_targets': nw['targets'], 'continuation_index': interface,
              'retained_native_carriers': nw['released_carriers'],
              'unfinished_Y_at_ground': sorted(set(range(111))-set(nw['targets'])),
              'preserved_individual_ground_fields': sorted(ground),
              'preserved_ground_rank': len(e.bb(values[n] for n in ground)),
              'all_live_owner_X_support': support,
              'all_live_owner_X_support_count': len(support),
              'all_live_owner_X_row_rank': len(e.bb(int(z['value_hex'], 16) for z in owners_at_cut)),
              'projection_state_comparisons': comparisons,
              'live_owners': owners_at_cut,
              'scope': nw['scope']}
    write_json(args.out/'RESULT.json', report)
    print(json.dumps({k: report[k] for k in ['status', 'word_sha256', 'after',
          'new_targets', 'continuation_index', 'all_live_owner_X_support_count']}))


if __name__ == '__main__':
    main()
