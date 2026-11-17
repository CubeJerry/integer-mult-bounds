"""Actual frame-derived proper export from the ground-retention source."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import itertools
import json
from build_quartet_compression_source import SOURCE, SHA, CHECK, HELPER, module
from build_four_plane_correction import replay_general
from review_half_sum_gate import independent_rows
from check_raw_cache_reactivation import quotient_basis, residual

PARENT_SHA = '4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'
FRAME_CERT = 'research/moonshot-005-program/results/bit-proper-flat-cubic-generators/author/RESULT.json'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--parent', type=Path, default=Path(__file__).resolve().parent/'ground-retention-known8/WORD.json')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
    geo = module(a.repo/CHECK, 'frame_export_geometry')
    h = module(a.repo/HELPER, 'frame_export_helper')
    rb = (a.repo/SOURCE).read_bytes(); assert hashlib.sha256(rb).hexdigest() == SHA
    R = json.loads(rb)['native_roots']
    pb = a.parent.read_bytes(); assert hashlib.sha256(pb).hexdigest() == PARENT_SHA
    w = json.loads(pb); C, values, at, parent_stats = replay_general(w, R, geo)
    fb = (a.repo/FRAME_CERT).read_bytes(); frame = json.loads(fb)['independent_generators'][57]
    assert frame['native_difference'] == [1, 4, 73, 78, 81, 86]
    S = [73, 78, 81, 86]; row = sum(1 << i for i in S)
    assert all(values[f'X{i}'] == 1 << i and len(C[at[f'X{i}']]) == 1 for i in S)
    q, H, J = 'G2_A-1', 'FRAME_SOURCE', 'FRAME_JOIN'
    w['charts'][H] = {'kind': 'span', 'rows': [R[i] for i in S]}
    w['charts'][J] = {'kind': 'span', 'rows': w['charts'][q]['rows']+[R[i] for i in S]}
    C[H] = geo.chart(w['charts'][H]); C[J] = geo.chart(w['charts'][J])
    assert (len(C[H]), len(C[J]), len(C[q])) == (3, 5, 3)
    assert geo.sub(C[H], C[J]) and geo.sub(C[q], C[J])
    target, collector, export = 'X31', 'X73', 'FRAME_EXPORT'
    assert at[target] == q and values[target].bit_count() == 2
    old_ops = w['operations']; old_cut = w['carrier_interface_before_operation']
    keys = {j: key for key, indices in w['semantic_operation_indices'].items() for j in indices}
    ops = []; sem = {}

    def emit(op, key, update=True):
        sem.setdefault(key, []).append(len(ops)); ops.append(op)
        if not update: return
        kind, name, *args = op
        if kind == 'INIT':
            assert name not in values
            values[name] = 0; at[name] = args[0]
        elif kind == 'ADD':
            assert C[at[name]] == C[at[args[0]]]
            values[args[0]] ^= values[name]
        elif kind == 'MOVE': at[name] = args[0]
        elif kind == 'CLEAR': del values[name], at[name]

    for j, op in enumerate(old_ops[:old_cut]): emit(op, keys[j], False)
    for i in S: emit(['MOVE', f'X{i}', H], 'frame_native_source_arrival')
    for i in S[1:]: emit(['ADD', f'X{i}', collector], 'frame_mode_encode')
    assert values[collector] == row
    emit(['MOVE', collector, J], 'frame_collector_join_arrival')
    emit(['INIT', export, J], 'frame_export_birth')
    emit(['ADD', collector, export], 'frame_actual_original_capture')
    emit(['MOVE', export, q], 'frame_paid_two_rank_descent')
    emit(['ADD', export, target], 'frame_mode_old_carrier_load')
    cut = len(ops); assert cut == old_cut+12
    assert len(independent_rows([values[f'X{i}'] for i in range(111)])) == 111
    assert values[export] == row
    inserted = False
    for j, op in enumerate(old_ops[old_cut:], old_cut):
        if keys[j] == 'deferred_sign_inverse_at_Hub' and not inserted:
            emit(['ADD', collector, target], 'frame_mode_unload_at_Hub')
            for i in S[1:]: emit(['ADD', f'X{i}', collector], 'frame_source_inverse_at_Hub')
            inserted = True
        emit(op, keys[j])
    assert inserted
    emit(['CLEAR', export], 'frame_export_retirement')
    w['schema'] = 'frame-derived-proper-export-v1'
    w['operations'] = ops; w['semantic_operation_indices'] = sem
    w['carrier_interface_before_operation'] = cut
    w['construction']['parent_word_sha256'] = PARENT_SHA
    w['construction']['frame_derived_export'] = {
        'credited_frame_certificate': FRAME_CERT, 'credited_frame_certificate_sha256': hashlib.sha256(fb).hexdigest(),
        'generator_ordinal': 57, 'full_native_difference': frame['native_difference'],
        'omitted_known_coordinate_roles': [1, 4], 'actual_source_roles': S,
        'source_chart': H, 'join_chart': J, 'query_chart': q, 'source_collector': collector,
        'changed_old_carrier': target, 'export_owner': export, 'payload_hex': hex(row)}
    w['scope'] = ('Actual frame-derived input mode acquired from four still-native originals, '
                  'copied at a rank-five join and delivered to a rank-three query by one paid '
                  'two-rank descent. The mode is outside both Q2 plus known coordinate units '
                  'and the entire pair-equality-half bank plus coordinate units. All95 retained '
                  'ground Ys stay ground at the source cut. This partial closed word still '
                  'completes only8 coordinate diagonal outputs; no complete supplier is claimed.')
    C, cv, ca, stats = replay_general(w, R, geo)
    profile = Counter(parent_stats['movement_profile']); profile.update({2: 6, 3: 1, 5: 3, 7: -4})
    assert stats['movement_profile'] == dict(sorted(profile.items()))
    assert stats['counts'] == {'INIT': 120, 'ADD': 612, 'MOVE': 316, 'CLEAR': 120}
    assert cv[export] == row and ca[export] == q
    assert Counter(len(C[ca[f'Y{i}']]) for i in range(111)) == {0: 95, 3: 16}
    N = [sum(1 << j for j, s in enumerate(R) if sum(x*y for x, y in zip(r, s)) == 0) for r in R]
    canonical = independent_rows([n ^ (1 << i) for i, n in enumerate(N)])
    axes = [1 << i for i in range(8)]
    q2 = independent_rows([u & v for u in canonical for v in canonical])
    q3 = independent_rows([u & v & z for u in canonical for v in canonical for z in canonical])
    assert (len(canonical), len(q2), len(q3)) == (9, 36, 84)
    assert residual(quotient_basis(q2+axes), row)
    assert not residual(quotient_basis(q3+axes), row)
    assert residual(quotient_basis(q3), row)
    assert not residual(quotient_basis(q3), row ^ (1 << 1) ^ (1 << 4))
    groups = defaultdict(list)
    for i, r in enumerate(R):
        if i >= 8: groups[tuple(j for j, x in enumerate(r) if x)].append(i)
    halves = []
    for support, indices in groups.items():
        for x, y in itertools.combinations(support, 2):
            for sign in [-1, 1]:
                halves.append(sum(1 << i for i in indices if R[i][x] == sign*R[i][y]))
    half_bank = independent_rows(halves+axes)
    assert len(half_bank) == 64
    assert all(not residual(quotient_basis(half_bank), c) for c in canonical)
    assert residual(quotient_basis(half_bank), row)
    current_query_rows = [int(x, 16) for x in w['Y_correction_rows_hex']]
    before_bank = independent_rows(canonical+axes+current_query_rows)
    assert len(before_bank) == 29 and len(independent_rows(before_bank+[row])) == 30
    own_access = [i for i in S if geo.sub(C[q], C[f'F{i}'])]
    assert own_access == [81, 86]
    actual_own_fields = {str(i): [name for name in cv if cv[name] & (1 << i)
                                and geo.sub(C[ca[name]], C[f'F{i}'])] for i in own_access}
    assert all(export in fields and target in fields for fields in actual_own_fields.values())
    moment = h.moment(stats['movement_profile']); gate = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        gate[1+7*j] = gate.get(1+7*j, 0)+74; gate[7*j] = gate.get(7*j, 0)-74
    ceiling = tuple(v/6 for v in h.moment(gate)); pin = h.save(a.out/'WORD.json', w)
    h.save(a.out/'CUT-INVENTORY.json', {'word_sha256': pin, 'cut_before_operation': cut, 'fields': [
        {'name': name, 'chart': ca[name], 'rank': len(C[ca[name]]), 'row_hex': hex(value)}
        for name, value in sorted(cv.items())]})
    controls = []
    for key in ['frame_mode_encode', 'frame_actual_original_capture', 'frame_paid_two_rank_descent',
                'frame_mode_old_carrier_load', 'frame_mode_unload_at_Hub', 'frame_source_inverse_at_Hub']:
        bad = json.loads(json.dumps(w)); index = sem[key][0]; del bad['operations'][index]
        if index < cut: bad['carrier_interface_before_operation'] -= 1
        try: replay_general(bad, R, geo)
        except AssertionError: controls.append('omit_'+key)
        else: raise AssertionError(('accepted missing operation', key))
    bad = json.loads(json.dumps(w)); u = sem['frame_mode_unload_at_Hub'][0]
    inv = sem['frame_source_inverse_at_Hub']; assert inv == list(range(u+1, u+4))
    bad['operations'][u:u+4] = bad['operations'][u+1:u+4]+[bad['operations'][u]]
    try: replay_general(bad, R, geo)
    except AssertionError: controls.append('restore_frame_collector_before_unload')
    else: raise AssertionError('accepted wrong inverse order')
    result = {'status': 'PASS_ACTUAL_FRAME_DERIVED_PROPER_EXPORT', 'word_sha256': pin,
              'parent_word_sha256': PARENT_SHA, 'source_cut': cut, 'actual_source_roles': S,
              'export_payload_hex': hex(row), 'export_source_join_query_ranks': [3, 5, 3],
              'original_X_rank': 111, 'ground_public_Y_count': 95, 'completed_diagonal_outputs': 8,
              'original_X_chart_rank_histogram': dict(sorted(Counter(len(C[ca[f'X{i}']]) for i in range(111)).items())),
              'full_pair_half_plus_axes_rank_before_after': [64, 65],
              'Q2_plus_axes_rank_before_after': [44, 45], 'in_Q3_plus_axes': True, 'in_Q3': False,
              'canonical_queries_axes_rank_before_after': [29, 30],
              'own_information_receiver_roles_at_query': own_access, 'actual_fields_inside_own_facets': actual_own_fields,
              'stats': stats, 'moment': h.record(moment),
              'necessary_limiting_room': h.record((ceiling[0]-moment[1], ceiling[1]-moment[0])),
              'negative_controls': controls, 'scope': w['scope']}
    h.save(a.out/'RESULT.json', result); print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
