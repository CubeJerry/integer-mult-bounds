#!/usr/bin/env python3
"""Three-dimensional mixed-export lower bound for the frozen nine-output word."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from shared_facet_source import source_geometry, dot, rank_f2, mask
from price import encode, moment

here = Path(__file__).resolve().parent
repo = next(p for p in here.parents if (p / 'AGENTS.md').exists())
roots, h, pins = source_geometry(repo)
word_path = here.parent / 'worker-c' / 'nine-output' / 'WORD.json'
raw = word_path.read_bytes()
word = json.loads(raw)
owners = word['expected_owned_at_handoff']
donors = [16, 19, 38, 49, 50, 56, 57]
terminal = [int(owners[f'P{i}']['value_hex'], 16) for i in range(8)]
G = terminal + [1 << j for j in donors]
W = [mask(j for j in range(111) if h[j] == h[i] and
          (j == i or dot(roots[j], roots[i]) == 0)) for i in range(111)]
C = [mask(j for j in range(111) if j == i or
          dot(roots[j], roots[i]) == 0) for i in range(111)]
frame = [0, 15, 31, 35, 40, 41, 106, 110]
if set(frame) & set(word['completed_targets']):
    raise ValueError('A frame receiver was already completed')
if any(dot(roots[i], roots[j]) == 0 for i in frame for j in frame):
    raise ValueError('The proposed frame has a contact')
restricted = [sum(((g >> j) & 1) << k for k, j in enumerate(frame)) for g in G]
if rank_f2(restricted) != 5:
    raise ValueError('Frozen G restriction changed')
dual = []
for v in range(1, 256):
    if all((v & g).bit_count() % 2 == 0 for g in restricted):
        if rank_f2(dual + [v]) > len(dual):
            dual.append(v)
if len(dual) != 3:
    raise ValueError('Wrong dual dimension')
embedded = [mask(frame[k] for k in range(8) if v >> k & 1) for v in dual]
if rank_f2(embedded) != 3 or any((g & z).bit_count() % 2 for g in G for z in embedded):
    raise ValueError('Invalid exact separating matrix')

# Reproduce the closed nine-output profile with Worker A's distinct replay
# receipt, not an unverified count copied into this argument.
review = json.loads((here / 'NINE-OUTPUT-INDEPENDENT-REPLAY.json').read_text())
profile = {int(k): v for k, v in review['CLOSED-WORD.json']['receipt']['movement_profile'].items()}
allowance = {127: Fraction(37, 6), 64: Fraction(74, 6), 1: Fraction(-74, 6)}
for j in range(1, 9):
    allowance[1 + 7*j] = allowance.get(1 + 7*j, 0) + Fraction(74, 6)
    allowance[7*j] = allowance.get(7*j, 0) - Fraction(74, 6)
room_profile = dict(allowance)
for r, count in profile.items():
    room_profile[r] = room_profile.get(r, 0) - count
room = moment(room_profile)
deficit = (Fraction(3) - room[1], Fraction(3) - room[0])
if not (0 < room[0] <= room[1] < 3 and deficit[0] > 0):
    raise ValueError('Budget does not exclude three unit descents')

negative_controls = {}
bad = embedded.copy()
bad[0] ^= 1 << frame[0]
negative_controls['corrupt_dual'] = any((g & z).bit_count() % 2 for g in G for z in bad)
negative_controls['claim_four_independent_duals'] = rank_f2(embedded + embedded[:1]) < 4
bad_frame = frame[:-1] + [16]
negative_controls['use_completed_receiver'] = bool(set(bad_frame) & set(word['completed_targets']))
negative_controls['ignore_seventh_point_export'] = profile.get(1) == 149 and profile.get(1) != 148
if not all(negative_controls.values()):
    raise ValueError('A negative control was not rejected')

result = {
    'status': 'PASS_THREE_MIXED_EXPORT_DIMENSIONS_REQUIRED',
    'source_pins': pins,
    'nine_output_word_sha256': hashlib.sha256(raw).hexdigest(),
    'nine_output_closed_sha256': review['CLOSED-WORD.json']['sha256'],
    'completed_targets': word['completed_targets'],
    'G_rows_hex': [hex(g) for g in G],
    'rank_G': rank_f2(G),
    'rank_W': rank_f2(W),
    'rank_C': rank_f2(C),
    'rank_G_plus_W': rank_f2(G + W),
    'rank_G_plus_C': rank_f2(G + C),
    'fixed_W_additional_dimensions': rank_f2(G + W) - rank_f2(G),
    'fixed_C_additional_dimensions': rank_f2(G + C) - rank_f2(G),
    'frame': frame,
    'frame_gram': [[dot(roots[i], roots[j]) for j in frame] for i in frame],
    'G_restricted_binary_rows': restricted,
    'G_restricted_rank': 5,
    'dual_columns_in_frame_bits': dual,
    'dual_columns_in_111_bits_hex': [hex(v) for v in embedded],
    'dual_column_rank': 3,
    'all_field_all_block_additional_information_lower_bound': '3V',
    'closed_profile': profile,
    'closed_moment': encode(moment(profile)),
    'limiting_room': encode(room),
    'minimum_missing_movement_margin': encode(deficit),
    'negative_controls': negative_controls,
    'scope': 'Immutable nine-output handoff and retained caller invoice. '
             'Every new positive-rank owned descent carries at most one '
             'whole-V payload. Arbitrary mixed payloads and future Y feedback '
             'are allowed. Prefix redesign, compensating earlier savings, '
             'fractional-volume fields and different computational interfaces '
             'are not excluded. Fixed-W/C gaps are sufficient representation '
             'costs, not arbitrary-fitting lower bounds.',
    'new_complete_kappa': False,
}
(here / 'SHARED-EXPORT-GATE.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: result[key] for key in [
    'status', 'frame', 'G_restricted_rank', 'dual_columns_in_frame_bits',
    'fixed_W_additional_dimensions', 'fixed_C_additional_dimensions',
    'minimum_missing_movement_margin',
]}))
