#!/usr/bin/env python3
"""Three actual cocharted mixed exports, plus an explicit global-fit screen."""
import copy
import hashlib
import json
from pathlib import Path
from shared_facet_source import source_geometry, dot, rank_q, rank_f2, mask
from coupled_two_receiver import replay
from eight_packet_source import price

here = Path(__file__).resolve().parent
repo = next(p for p in here.parents if (p / 'AGENTS.md').exists())
roots, h, pins = source_geometry(repo)
source_path = here / 'two-receiver-output' / 'COUPLED-WORD.json'
source_raw = source_path.read_bytes()
source = json.loads(source_raw)
word = copy.deepcopy(source)
names = ['DC1_1', 'DC1_2', 'DC2_1']
normals = word['charts']['D6']['rows'] + [roots[0]]
word['charts']['SHARED5'] = {'kind': 'ann', 'rows': normals}
word['operations'].extend([['MOVE', name, 'SHARED5'] for name in names])
for name in names:
    word['expected_owned_at_handoff'][name]['chart'] = 'SHARED5'
word['markers']['handoff'] = len(word['operations'])
word['schema'] = 'three-coded-shared-export-v1'
word['shared_export'] = {
    'records': names, 'chart': 'SHARED5', 'dimension': 8-rank_q(normals),
    'recipient_frame_role': 0, 'rank_drops': [2, 1, 2],
}
out = here / 'shared-export-output'
out.mkdir(exist_ok=True)
result = {'status': 'PASS_ACTUAL_THREE_COCHARTED_MIXED_EXPORTS',
          'source_pins': pins,
          'source_prefix_sha256': hashlib.sha256(source_raw).hexdigest()}
word_hashes = {}
for closed in [False, True]:
    current = copy.deepcopy(word)
    if closed:
        for name in current['expected_owned_at_handoff']:
            current['operations'].append(['CLEAR', name])
        for j in range(111):
            if j not in current['completed_targets']:
                current['operations'].append(['MOVE', f'Y{j}', f'F{j}'])
        current['closed_partial'] = True
    receipt = replay(current, roots, h)
    name = ('CLOSED-' if closed else '') + 'WORD.json'
    raw = (json.dumps(current, indent=2, sort_keys=True) + '\n').encode()
    if (out / name).exists() and (out / name).read_bytes() != raw:
        raise ValueError('Frozen word bytes changed: ' + name)
    (out / name).write_bytes(raw)
    word_hashes[name] = hashlib.sha256(raw).hexdigest()
    result[name] = receipt
gate = json.loads((here / 'SHARED-EXPORT-GATE.json').read_text())
Q = [int(v, 16) for v in gate['dual_columns_in_111_bits_hex']]
G = [int(v, 16) for v in gate['G_rows_hex']]
Z = [int(word['expected_owned_at_handoff'][name]['value_hex'], 16) for name in names]
signatures = [sum(((z & q).bit_count() % 2) << k for k, q in enumerate(Q)) for z in Z]
if rank_f2(signatures) != 3 or signatures != [5, 3, 1]:
    raise ValueError('The actual payloads do not close the displayed cut')
result['shared_cut_signatures'] = signatures
result['source_prefix_unchanged'] = word['operations'][:-3] == source['operations']

def separating_dual(rows, role):
    pivots = {}
    for row, rhs in [(r, 0) for r in rows] + [(1 << role, 1)]:
        while row:
            j = (row & -row).bit_length() - 1
            if j not in pivots:
                pivots[j] = (row, rhs)
                break
            p, q = pivots[j]
            row ^= p
            rhs ^= q
        else:
            if rhs:
                raise ValueError('No separating dual exists')
    value = 0
    for j, (row, rhs) in sorted(pivots.items(), reverse=True):
        if rhs ^ ((row & value).bit_count() % 2):
            value |= 1 << j
    return value

fits, failed = [], []
for i in range(111):
    forbidden = mask(j for j in range(111) if dot(roots[i], roots[j]) != 0)
    rows = [v & forbidden for v in G + Z]
    if rank_f2(rows + [1 << i]) == rank_f2(rows):
        fits.append(i)
    else:
        dual = separating_dual(rows, i)
        if dual & ~forbidden or not (dual >> i & 1) or any(
                (g & dual).bit_count() % 2 for g in G + Z):
            raise ValueError('Invalid receiver obstruction dual')
        failed.append({'role': i, 'dual_hex': hex(dual)})
new_frame = [0, 22, 23, 30, 32, 60, 61, 107]
if any(dot(roots[i], roots[j]) == 0 for i in new_frame for j in new_frame):
    raise ValueError('Invalid surviving noncontact frame')
frame_rank = rank_f2([v & mask(new_frame) for v in G + Z])
if frame_rank != 5:
    raise ValueError('Surviving rank-five cut changed')
result['global_relaxation'] = {
    'rank': rank_f2(G + Z), 'feasible_receivers': fits,
    'failed_receiver_duals': failed,
    'surviving_noncontact_frame': new_frame,
    'restriction_rank': frame_rank,
    'scope': 'All three exports and all seven donor coordinates granted '
             'globally; this is necessary only and stronger than real access. '
             'The source still completes exactly Y17,Y34.',
}
negative_controls = {}
for label, change in [('omit_export', 'omit'), ('wrong_upward_export', 'up')]:
    bad = copy.deepcopy(word)
    if change == 'omit':
        del bad['operations'][-1]
        bad['markers']['handoff'] -= 1
    else:
        bad['operations'][-1][-1] = 'Hub'
    try:
        replay(bad, roots, h)
    except (ValueError, KeyError) as error:
        negative_controls[label] = {'rejected': True, 'reason': str(error)}
    else:
        raise ValueError('Accepted bad shared export')
negative_controls['duplicate_payload_direction'] = rank_f2(signatures[:2] + signatures[:1]) == 2
result['negative_controls'] = negative_controls
(out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
bill = price(result['CLOSED-WORD.json']['movement_profile'])
(out / 'PRICE.json').write_text(json.dumps(bill, indent=2) + '\n')
manifest = {
    'word_sha256': word_hashes,
    'price_sha256': hashlib.sha256((out / 'PRICE.json').read_bytes()).hexdigest(),
    'result_sha256': hashlib.sha256((out / 'RESULT.json').read_bytes()).hexdigest(),
    'source_prefix_sha256': hashlib.sha256(source_raw).hexdigest(),
}
(out / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'dual_signatures': signatures,
                  'global_relaxation_rank': rank_f2(G + Z),
                  'relaxed_feasible_count': len(fits),
                  'relaxed_feasible_receivers': fits,
                  'moment': bill['moment']['lower_decimal'],
                  'limiting_room': bill['limiting_room']['lower_decimal']}))
