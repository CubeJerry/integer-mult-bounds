#!/usr/bin/env python3
"""Author exact source replay and targeted ghost-interface negative controls."""
import argparse
import copy
import gzip
import json
import sys
from collections import Counter
from pathlib import Path


def main(a):
    sys.path.insert(0, str(a.reconstruction))
    from common import F, add, inverse, load_inputs, mul, need, rank, sha
    import build as base
    s, _, invoice = load_inputs(a.repo)
    wb = (a.output / 'WORD.json.gz').read_bytes()
    w = json.loads(gzip.decompress(wb))
    r = json.loads((a.output / 'RESULT.json').read_text())
    need(sha(wb) == r['word_sha256'], 'word receipt pin')
    meta = w['parked_dual_ghosts']
    records = meta['records']
    raw = {int(k): v for k, v in w['private_role_map'].items()}
    q = {x: {p: F(1), x: F(-1)} for x, p in raw.items()}
    full, full_loc = base.interpret_prefix(s, w)
    observed_word = copy.deepcopy(w)
    observed_word['marks']['common_starts'] = meta['observation_boundary']
    observed, observed_loc = base.interpret_prefix(s, observed_word)
    for rec in records:
        need(observed[rec['ghost']] == {j: F(c) for j, c in rec['observation_all1880_input_row']},
             'all1880-coordinate pure-D actual ghost')
        need(observed_loc[rec['ghost']] == 127 and
             observed[rec['physical_B']] == q[rec['hosted_B']], 'actual parked input and output chart')
    # An explicit information inverse of the public reverse map recovers every B.
    recovered = 0
    for b, values in w['hosted_reverse_output_corrections'].items():
        b = int(b)
        row = full[raw[b]]
        for d, c in values:
            row = add(row, full[raw[d]], -F(c))
        need(row == q[b], 'explicit public reverse information inverse')
        recovered += 1
    need(recovered == 96, 'all96 genuine dual inputs recovered')
    bill = base.typed(s, w)
    bill.pop('final_locations')
    need(json.loads(json.dumps(bill)) == r['bill'], 'whole-word physical bill')
    need(sum(int(k) * v for k, v in r['bill']['raw_histogram'].items()) == 3200,
         'all400 raw endpoint rankmass retained')
    mutant_rejections = {}

    def reject(name, mutant):
        try:
            state, locations = base.interpret_prefix(s, mutant)
            need(state == full and locations == full_loc, 'wrong exact public prefix state')
            base.typed(s, mutant)
        except (ValueError, KeyError) as error:
            mutant_rejections[name] = str(error)
        else:
            raise ValueError('mutant survived: ' + name)

    rec = records[0]
    m = copy.deepcopy(w)
    m['program'][rec['activate_event']][2] = 3
    reject('zero_activated_at_wrong_chart', m)
    m = copy.deepcopy(w)
    m['program'][rec['public_restore_event']][3] = '0'
    reject('discard_observation_without_restoring_public_B', m)
    first_move = next(i for i, e in enumerate(w['program'])
                      if e[0] == 'MOVE' and e[1] == rec['ghost'])
    m = copy.deepcopy(w)
    m['program'][first_move][4] = False
    reject('ghost_transport_charged_as_raw', m)
    first_read = next(i for i, e in enumerate(w['program'][rec['activate_event'] + 1:],
                                             rec['activate_event'] + 1)
                      if e[0] in ('ADD', 'COPY') and e[2] == rec['ghost'])
    m = copy.deepcopy(w)
    m['program'][first_read][2] = rec['physical_B']
    reject('parked_input_read_at_former_encoding_chart', m)
    m = copy.deepcopy(w)
    m['program'][rec['park_event']][3] = rec['activation_chart']
    reject('genuine_original_never_reaches_hub', m)
    if meta['completion_events']:
        m = copy.deepcopy(w)
        event = meta['completion_events'][0]['event']
        m['program'][event][3] = str(-F(m['program'][event][3]))
        reject('wrong_ghost_decoder_sign', m)
    # Omitting the new owned legs is an accounting error even if raw refinement
    # and the inherited eight packet calls have been paid.
    paid = Counter({int(k): v for k, v in r['conditional_caller']['P_partial'].items()})
    unpaid = paid.copy()
    for k, v in r['ghost_owned_move_histogram'].items():
        unpaid[int(k)] -= 18 * v
    need(unpaid != paid and all(v >= 0 for v in unpaid.values()), 'meaningful unpaid-owned mutant')
    mutant_rejections['owned_ghost_ascent_omitted_from_full_invoice'] = (
        'Rejected: explicit actual owned MOVE histogram is absent from claimed caller.')
    result = {'status': 'PASS_AUTHOR_GHOST_SOURCE_CHECKS_AND_NEGATIVE_CONTROLS',
              'word_sha256': sha(wb), 'word_payload_sha256': sha(gzip.decompress(wb)),
              'full_input_coordinates': 1880, 'explicit_recovered_hosted_inputs': recovered,
              'actual_ghost_observation_checks': len(records),
              'same_raw_rankmass': 3200, 'mutants': mutant_rejections,
              'scope': 'Author replay and exact targeted mutants. Independent review remains distinct.'}
    (a.output / 'AUDIT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--reconstruction', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    main(p.parse_args())
