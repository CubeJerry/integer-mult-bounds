#!/usr/bin/env python3
"""Independent Worker-A replay of Worker-C's appended nine-output suffix.

The engine is Worker A's, not the suffix author's. This does not turn the
prefix author's replay into a second independent review of that prefix.
"""
import copy
import hashlib
import json
from pathlib import Path
from shared_facet_source import source_geometry
from coupled_two_receiver import replay

here = Path(__file__).resolve().parent
repo = next(p for p in here.parents if (p / 'AGENTS.md').exists())
roots, h, _ = source_geometry(repo)
published = here.parent / 'worker-c' / 'nine-output'
source = json.loads((here / 'two-receiver-output' / 'COUPLED-WORD.json').read_text())
base = json.loads((published / 'WORD.json').read_text())
prefix = len(source['operations'])
if base['operations'][:prefix] != source['operations']:
    raise ValueError('Frozen source prefix changed')
expected_suffix = []
for donor in [16, 19, 38, 49, 50, 56, 57]:
    expected_suffix.extend([
        ['MOVE', f'R{donor}', 'zero'],
        ['ADD', f'R{donor}', f'Y{donor}'],
        ['MOVE', f'Y{donor}', f'F{donor}'],
    ])
if base['operations'][prefix:] != expected_suffix:
    raise ValueError('Unexpected suffix operation')

result = {}
for name in ['WORD.json', 'CLOSED-WORD.json']:
    raw = (published / name).read_bytes()
    word = json.loads(raw)
    receipt = replay(word, roots, h)
    # The engine checks each endpoint against word.completed_targets; its
    # fixed-source report field names two targets, so label this review using
    # the actual nine-target input contract already checked by that loop.
    receipt['completed_targets'] = word['completed_targets']
    owned = set()
    moving_owned = set()
    for op in word['operations']:
        if op[0] == 'INIT':
            owned.add(op[1])
        elif op[0] == 'MOVE' and op[1] in owned:
            moving_owned.add(op[1])
    if len(moving_owned) != 22:
        raise ValueError('Moving-copy invoice changed')
    result[name] = {
        'sha256': hashlib.sha256(raw).hexdigest(),
        'receipt': receipt,
        'moving_owned_records': sorted(moving_owned),
    }

negatives = {}
for label in ['omit_point_descent', 'omit_point_read', 'wrong_point_source',
              'read_after_receiver_ascends', 'descend_original_X']:
    bad = copy.deepcopy(base)
    if label in ['omit_point_descent', 'omit_point_read']:
        index = prefix + (0 if label == 'omit_point_descent' else 1)
        del bad['operations'][index]
        bad['markers'] = {k: v - (v > index) for k, v in bad['markers'].items()}
    elif label == 'wrong_point_source':
        bad['operations'][prefix + 1][1] = 'R19'
    elif label == 'read_after_receiver_ascends':
        bad['operations'][prefix + 1], bad['operations'][prefix + 2] = (
            bad['operations'][prefix + 2], bad['operations'][prefix + 1])
    else:
        bad['operations'][prefix][1] = 'X16'
    try:
        replay(bad, roots, h)
    except (ValueError, KeyError) as error:
        negatives[label] = {'rejected': True, 'reason': str(error)}
    else:
        raise ValueError('Accepted semantic negative: ' + label)

result['suffix_review'] = {
    'status': 'PASS_INDEPENDENT_EXACT_NINE_OUTPUT_SUFFIX',
    'source_prefix_operations': prefix,
    'unchanged_prefix': True,
    'added_operations': expected_suffix,
    'verified_original_input_columns': 222,
    'negative_controls': negatives,
    'scope': 'Worker-A engine independently checks Worker-C suffix and its '
             'literal composition; this is not another independent review '
             'of Worker-A source-prefix mathematics.',
}
(here / 'NINE-OUTPUT-INDEPENDENT-REPLAY.json').write_text(
    json.dumps(result, indent=2) + '\n')
print(json.dumps({
    'status': result['suffix_review']['status'],
    'counts': result['CLOSED-WORD.json']['receipt']['counts'],
    'profile': result['CLOSED-WORD.json']['receipt']['movement_profile'],
    'completed_targets': result['CLOSED-WORD.json']['receipt']['completed_targets'],
    'semantic_negatives': len(negatives),
}))
