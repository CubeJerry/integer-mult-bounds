#!/usr/bin/env python3
"""Actual parked-input, short-activated zero dual slots on frozen source words.

The two modes preserve a frozen parent's public source effects; the eight mode
also completes eight actual hosted reverse outputs using the retained ghosts.
All new storage is real owned storage. No global adjoint is assumed.
"""
import argparse
import copy
import gzip
import json
import sys
from collections import Counter
from pathlib import Path


def main(a):
    sys.path.insert(0, str(a.reconstruction))
    from common import F, add, inverse, load_inputs, mul, need, rank, ser, sha, space
    import build as base

    s, fused, invoice = load_inputs(a.repo)
    parent_path = (a.frame_parent if a.variant == 'one' else a.paired_parent)
    parent_bytes = parent_path.read_bytes()
    p = json.loads(gzip.decompress(parent_bytes))
    pin = ('2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
           if a.variant == 'one' else
           'bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a')
    need(sha(gzip.decompress(parent_bytes)) == pin, 'frozen parent payload')
    raw = {int(k): v for k, v in p['private_role_map'].items()}
    hosted = {s['live'][k]: (x, y) for k, x, y in
              zip(s['hosted']['Dports'], s['hosted']['X2'], s['hosted']['Y2'])}
    B = [5, 56, 65, 69, 77, 96, 100, 103]
    selected = [56] if a.variant == 'one' else [0, 7, 20, 27, 36, 46, 57, 111]
    complete = [] if a.variant == 'one' else B
    rows0, loc0 = base.interpret_prefix(s, p)
    q = {r: {raw[r]: F(1), r: F(-1)} for r in raw}
    old_cut = p['marks']['common_starts']
    frames = s['frames'] + [d['frame'] for d in p.get('additional_charts', [])]
    sites = list(map(space, frames))
    source_d = {y for x, y in hosted.values()}
    records = []
    by_physical = {}
    first_event = {}
    for k, d in enumerate(selected):
        r = hosted[d][0]
        physical = raw[r]
        ghost = 1880 + p['owned_fields'] + k
        uses = [(t, e) for t, e in enumerate(p['program'][400:old_cut], 400)
                if e[1] == physical or e[0] in ('ADD', 'COPY') and e[2] == physical]
        need(uses and uses[0][1][0] == 'MOVE', 'first access is unread ascent')
        t, e = uses[0]
        need(e[2] == s['initial'][r] and e[4] is False,
             'authentic raw initial ascent')
        C = e[3]
        need(len(frames[C]) == 6 and sites[s['initial'][r]] < sites[C],
             'actual dimension-six first activation')
        need(loc0[physical] == 127, 'parent decoded dual slot reaches hub')
        observed = add(rows0[physical], q[r], -1)
        coeff = {y: observed.get(raw[y], F(0)) for y in sorted(source_d)}
        coeff = {y: c for y, c in coeff.items() if c}
        want = {}
        for y, c in coeff.items():
            want = add(want, q[y], c)
        need(observed == want, 'parent dual endpoint is its original plus pure D')
        rec = {'first_donor': d, 'hosted_B': r, 'physical_B': physical,
               'ghost': ghost, 'activation_chart': C,
               'parent_first_move_event': t, 'parent_first_move': e,
               'observation_D_coefficients': ser(coeff),
               'observation_all1880_input_row': ser(observed)}
        records.append(rec)
        by_physical[physical] = rec
        first_event[t] = rec

    coefficient_rows = [{y: F(c) for y, c in r['observation_D_coefficients']}
                        for r in records]
    targets = [hosted[d][1] for d in complete]
    decoder = []
    if complete:
        need(all(set(row) <= set(targets) for row in coefficient_rows),
             'eight ghosts involve exactly target D bank')
        matrix = [[row.get(y, F(0)) for y in targets] for row in coefficient_rows]
        need(rank(matrix) == 8, 'eight actual correction observations span eight D values')
        decoder = inverse(matrix)
        need(mul(decoder, matrix) == [[F(i == j) for j in range(8)] for i in range(8)],
             'exact ghost decoder')
        for d in complete:
            need(rows0[raw[hosted[d][0]]] == q[hosted[d][0]],
                 'each selected public B is unchanged in this parent')

    ops = []
    lineage = []
    mapping = {}
    boundaries = {}
    active = set()
    redirections = []

    def emit(e, parent=None):
        pos = len(ops)
        ops.append(e)
        lineage.append(parent)
        return pos

    def finish_ghosts():
        observation = len(ops)
        for rec in records:
            rec['public_restore_event'] = emit(
                ['ADD', rec['physical_B'], rec['ghost'], '1', 127])
        completion_events = []
        for i, d in enumerate(complete):
            b = raw[hosted[d][0]]
            for j, rec in enumerate(records):
                if decoder[i][j]:
                    t = emit(['ADD', b, rec['ghost'], str(-decoder[i][j]), 127])
                    completion_events.append({'event': t, 'target_first_donor': d,
                                              'ghost': rec['ghost'],
                                              'coefficient': str(-decoder[i][j])})
        for rec in records:
            rec['retire_event'] = emit(['CLEAR', rec['ghost'], 127])
        return observation, completion_events

    observation_at = None
    completion_events = []
    for t, e0 in enumerate(p['program']):
        if t == old_cut:
            observation_at, completion_events = finish_ghosts()
        boundaries[t] = len(ops)
        if t in first_event:
            rec = first_event[t]
            mapping[t] = len(ops)
            rec['park_event'] = emit(['MOVE', rec['physical_B'], e0[2], 127, False], t)
            rec['activate_event'] = emit(['INIT', rec['ghost'], rec['activation_chart']])
            active.add(rec['physical_B'])
            continue
        e = copy.deepcopy(e0)
        changed = False
        if t < old_cut:
            if e[1] in active:
                e[1] = by_physical[e[1]]['ghost']
                changed = True
                if e[0] == 'MOVE':
                    e[4] = True
            if e[0] in ('ADD', 'COPY') and e[2] in active:
                e[2] = by_physical[e[2]]['ghost']
                changed = True
        mapping[t] = emit(e, t)
        if changed:
            redirections.append({'parent_event': t, 'new_event': mapping[t]})
    need(observation_at is not None and len(mapping) == len(p['program']),
         'all parent operations consumed once')
    w = copy.deepcopy(p)
    for key in ['paired_collection', 'second_frame_feedback', 'paired_reverse_corrections']:
        if key in w:
            w['parent_' + key + '_provenance'] = w.pop(key)
    w.update(schema='moonshot-S008-short-activated-parked-dual-ghost-' + a.variant + '-v1',
             program=ops, owned_fields=p['owned_fields'] + len(records),
             parent_word_sha256=sha(parent_bytes), parent_payload_sha256=pin,
             parent_event_of_output=lineage,
             marks={k: boundaries[v] for k, v in p['marks'].items()},
             native_event_to_physical=[mapping[v] for v in p['native_event_to_physical']],
             parked_dual_ghosts={'records': records, 'observation_boundary': observation_at,
                                'redirections': redirections,
                                'completed_first_donors': complete,
                                'completion_D_roles': targets,
                                'decoder': [[str(c) for c in row] for row in decoder],
                                'completion_events': completion_events,
                                'scope': 'Genuine original B is parked unchanged; the active dual slot '
                                         'is an actual owned zero initialized at its first cochart '
                                         'encoder. All parent event metadata is ancestor provenance.'})
    w['reservation_accounting'] = ('All parent source legs are retained or replaced explicitly. '
                                  'Parked B uses one direct rank8 raw ascent; the old first rank5 '
                                  'segment is consumed, and its remaining active slot route is '
                                  'paid owned ghost transport. No erased ghost transport credit.')
    obs_word = copy.deepcopy(w)
    obs_word['marks']['common_starts'] = observation_at
    obs_rows, obs_locs = base.interpret_prefix(s, obs_word)
    for rec in records:
        want = {j: F(c) for j, c in rec['observation_all1880_input_row']}
        need(obs_locs[rec['ghost']] == 127 and obs_rows[rec['ghost']] == want,
             'actual retained ghost observation at hub on all1880 coordinates')
        need(obs_rows[rec['physical_B']] == q[rec['hosted_B']],
             'original B genuinely remains parked and authentic')
    rows, loc = base.interpret_prefix(s, w)
    need(loc == loc0 and set(rows) == set(rows0), 'same public prefix locations and live set')
    expected_deltas = {raw[hosted[d][0]]: q[hosted[d][1]] for d in complete}
    for r, row in rows0.items():
        want = add(row, expected_deltas[r], -1) if r in expected_deltas else row
        need(rows[r] == want, 'exact1880-column prefix endpoint delta')
    tail = w['program'][w['marks']['common_starts']:]
    need(tail == p['program'][old_cut:], 'literal original common suffix')
    for d in complete:
        role = hosted[d][0]
        uses = [e for e in tail if e[1] == raw[role] or
                e[0] in ('ADD', 'COPY') and e[2] == raw[role]]
        need(uses == [['ADD', raw[role], role, '1', 127]],
             'completed reverse output has no suffix feedback')
        need(rows[raw[role]] == add(q[role], q[hosted[d][1]], -1),
             'actual hosted reverse output completed')
    parent_bill = base.typed(s, p)
    bill = base.typed(s, w)
    need(bill.pop('final_locations') == parent_bill.pop('final_locations'),
         'same final public endpoints and no live owned fields')
    own_hist = Counter()
    for e in w['program']:
        if e[0] == 'MOVE' and any(e[1] == rec['ghost'] for rec in records):
            own_hist[abs(len(frames[e[3]]) - len(frames[e[2]]))] += 1
    raw_src = Counter(abs(len(s['frames'][e[3]]) - len(s['frames'][e[2]]))
                      for e in s['program'] if e[0] == 'MOVE' and e[1] in raw)
    T = Counter({int(k): v for k, v in invoice['T4'].items()})
    P = Counter({int(k): v for k, v in invoice['P4'].items()})
    raw_new = Counter(bill['raw_histogram'])
    for r in raw_new.keys() | raw_src.keys() | own_hist.keys():
        P[r] += 18 * (raw_new[r] - raw_src[r] + own_hist[r])
    P[9] += 18 * 8
    need(all(v >= 0 for v in P.values()), 'nonnegative full caller invoice')
    move_new = Counter(bill['move_rank_histogram'])
    move_old = Counter(parent_bill['move_rank_histogram'])
    delta = {r: move_new[r] - move_old[r] for r in move_new.keys() | move_old.keys()
             if move_new[r] != move_old[r]}
    need(delta == {5: -len(records), 8: len(records)},
         'exact complete paid transport delta: rank8 replaces rank5')
    lo, hi = base.interval({r: T[r] - P[r] for r in T.keys() | P.keys()})
    H = sorted(hosted)
    residual = []
    actual_reverse_corrections = {}
    for d in H:
        row = add(rows[raw[hosted[d][0]]], q[hosted[d][0]], -1)
        coeff = {y: row.get(raw[y], F(0)) for y in sorted(source_d)}
        coeff = {y: c for y, c in coeff.items() if c}
        reconstructed = {}
        for y, c in coeff.items():
            reconstructed = add(reconstructed, q[y], c)
        need(row == reconstructed, 'complete actual reverse endpoint correction interface')
        actual_reverse_corrections[str(hosted[d][0])] = ser(coeff)
        row = add(row, q[hosted[d][1]], 1)
        residual.append([row.get(raw[hosted[e][1]], F(0)) for e in H])
    residual_rank = rank(residual)
    w['hosted_reverse_output_corrections'] = actual_reverse_corrections
    a.output.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(w, sort_keys=True, separators=(',', ':')).encode()
    blob = gzip.compress(payload, mtime=0, compresslevel=9)
    (a.output / 'WORD.json.gz').write_bytes(blob)
    result = {'status': 'PASS_ACTUAL_SHORT_ZERO_ACTIVATION_AND_RETAINED_OBSERVATION',
              'variant': a.variant, 'source_sha256': p['source_sha256'],
              'parent_word_sha256': sha(parent_bytes), 'parent_payload_sha256': pin,
              'word_sha256': sha(blob), 'word_payload_sha256': sha(payload),
              'independent_input_coordinates': 1880,
              'ghost_count': len(records), 'selected_first_donors': selected,
              'actual_completed_reverse_first_donors': complete,
              'actual_completed_reverse_B_roles': [hosted[d][0] for d in complete],
              'actual_reverse_residual_rank': residual_rank,
              'ghost_observation_rank': rank([[row.get(y, F(0)) for y in sorted(source_d)]
                                              for row in coefficient_rows]),
              'bill': bill, 'ghost_owned_move_histogram': dict(sorted(own_hist.items())),
              'complete_transport_delta': dict(sorted(delta.items())),
              'ordinary_delta': {k: bill['opcode_counts'].get(k, 0) -
                                    parent_bill['opcode_counts'].get(k, 0)
                                 for k in bill['opcode_counts'].keys() |
                                 parent_bill['opcode_counts'].keys()},
              'same_literal_common_suffix': True,
              'all_parent_public_outputs_preserved_except_listed_completed_reverse': True,
              'conditional_caller': {'T4': dict(sorted(T.items())),
                                     'P_partial': dict(sorted(P.items())),
                                     'paid_positions': sum(P.values()),
                                     'target_positions': sum(T.values()),
                                     'rank_surplus': sum(r * (T[r] - P[r])
                                                         for r in T.keys() | P.keys()),
                                     'remaining_moment_per_native_lower': str(lo / 18),
                                     'remaining_moment_per_native_upper': str(hi / 18),
                                     'remaining_moment_per_native_decimal': float(lo / 18),
                                     'retained_paid_packets': {9: 8}},
              'scope': 'Actual source-word short zero activation and endpoint-preserving '
                       'observation interface. Eight variant completes eight actual hosted '
                       'reverse outputs. No global adjoint, global target construction, '
                       'supplier admission or new kappa is asserted.'}
    (a.output / 'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: result[k] for k in ['variant', 'word_payload_sha256',
          'ghost_count', 'ghost_observation_rank', 'actual_reverse_residual_rank',
          'actual_completed_reverse_first_donors', 'bill', 'conditional_caller']}, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--reconstruction', type=Path, required=True)
    ap.add_argument('--frame-parent', type=Path, required=True)
    ap.add_argument('--paired-parent', type=Path, required=True)
    ap.add_argument('--variant', choices=['one', 'eight'], required=True)
    ap.add_argument('--output', type=Path, required=True)
    main(ap.parse_args())
