#!/usr/bin/env python3
"""Focused adversarial checks for the five added actual seed packets."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from check import SOURCE_SHA, need
from eight_check import replay


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--word', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    raw = args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'root source pin')
    roots = json.loads(raw)['native_roots']
    base = json.loads(args.word.read_text())
    mutations = {}
    for packet in ['P3', 'P7']:
        word = copy.deepcopy(base)
        k = next(i for i, op in enumerate(word['operations']) if op[0] == 'ADD' and op[-1] == packet)
        del word['operations'][k]
        mutations['omit_actual_seed_term_'+packet] = word
    word = copy.deepcopy(base)
    k = next(i for i, op in enumerate(word['operations']) if op == ['MOVE', 'P4', 'zero'])
    word['operations'][k][-1] = 'F10'
    mutations['added_packet_does_not_reach_ground'] = word
    word = copy.deepcopy(base)
    k = next(i for i, op in enumerate(word['operations']) if op == ['INIT', 'P0', 'Hub'])
    birth = word['operations'].pop(k)
    word['operations'].insert(0, birth)
    mutations['packet_birth_precedes_source_restoration'] = word
    word = copy.deepcopy(base)
    k = next(i for i, op in enumerate(word['operations']) if op == ['MOVE', 'P6', 'zero'])
    word['operations'].insert(k+1, ['INIT', 'P6', 'Hub'])
    mutations['restarted_owned_packet_lifetime'] = word
    result = {}
    for label, word in mutations.items():
        try:
            replay(word, roots)
        except (ValueError, KeyError) as error:
            result[label] = {'rejected': True, 'reason': str(error)}
        else:
            raise ValueError('accepted semantic mutant '+label)
    args.output.write_text(json.dumps({'status': 'PASS_INDEPENDENT_EIGHT_PACKET_NEGATIVE_CONTROLS',
                                     'source_sha256': SOURCE_SHA,
                                     'word_sha256': hashlib.sha256(args.word.read_bytes()).hexdigest(),
                                     'negative_controls': result}, indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
