"""Recovery-only source/owner census; not a physical wrapper implementation."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import types

BASE = 'e54523517d0f03e58352e647c403a5af3e525a57'
PINS = {
 'research/shared-wire-split-composition/data/caller.json':
 '3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e',
 'research/current-scalar-flat-tables/vendor/lifecycle/source_ir.py':
 '54dd93bc50bd10e974c70794df1c13da27f0e3d8cdb6cfe6791a63280096f1b1',
}
WORD_SHA = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'


def need(value, message):
    if not value:
        raise ValueError(message)


def census(word, caller):
    need(len(caller['events']) == 3095 and word['public'] == 1480, 'selected sizes')
    ports = word['live']
    second = dict(zip(word['hosted']['Dports'], zip(word['hosted']['X2'], word['hosted']['Y2'])))
    main_slots = set(ports) | {x + 112 for x in ports} | set(word['hosted']['X2']) | set(word['hosted']['Y2'])
    helpers = sorted(set(range(word['public'])) - main_slots)
    need(len(main_slots) == 400 and len(helpers) == 1080, 'public partition')
    jobs, mappings, helper_owners = [], [], set()
    for index, event in enumerate(caller['events']):
        if event[0] != 'J':
            continue
        _, stage, a, b = event
        names = {}
        for pi, slot in enumerate(ports):
            roles = a if pi in second else b[:2]
            names[slot] = ('main', pi, roles[0])
            names[slot + 112] = ('main', pi, roles[1])
            if pi in second:
                u, v = second[pi]
                names[u] = ('main', pi, roles[2])
                names[v] = ('main', pi, roles[3])
        for slot in helpers:
            owner = ('helper', index, slot)
            need(owner not in helper_owners, 'fresh occurrence-qualified helper')
            helper_owners.add(owner)
            names[slot] = owner
        need(set(names) == set(range(1480)), 'complete actual public slots')
        need(len(set(names.values())) == 1480, 'injective actual public owner map')
        jobs.append((index, stage))
        mappings.append([[slot, names[slot]] for slot in range(1480)])
    need([stage for _, stage in jobs] == list(range(1, 19)), 'actual chronological stages')
    return jobs, mappings, helper_owners


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', type=Path)
    parser.add_argument('selected_word', type=Path)
    args = parser.parse_args()
    frozen = {}
    for path, expected in PINS.items():
        data = subprocess.check_output(['git', '-C', str(args.repository), 'show', BASE + ':' + path], timeout=30)
        need(hashlib.sha256(data).hexdigest() == expected, 'source pin ' + path)
        frozen[path] = data
    data = args.selected_word.read_bytes()
    need(hashlib.sha256(data).hexdigest() == WORD_SHA, 'native bytes')
    word = json.loads(gzip.decompress(data))
    caller = json.loads(frozen['research/shared-wire-split-composition/data/caller.json'])
    jobs, mappings, helpers = census(word, caller)
    mutated = copy.deepcopy(caller)
    mutated['events'][21][2][2] = mutated['events'][21][2][0]
    try:
        census(word, mutated)
    except ValueError as error:
        need(str(error) == 'injective actual public owner map', 'alias control diagnostic')
        control = str(error)
    else:
        raise ValueError('alias control escaped')
    ir = types.ModuleType('a4_frozen_source_ir')
    sys.modules[ir.__name__] = ir
    path = 'research/current-scalar-flat-tables/vendor/lifecycle/source_ir.py'
    exec(compile(frozen[path], path, 'exec'), ir.__dict__)
    try:
        ir.current_caller(word, caller)
    except KeyError as error:
        need(str(error) == "'kind'", 'expected caller-family schema boundary')
        producer = 'KeyError: kind'
    else:
        raise ValueError('old caller producer unexpectedly accepted selected source')
    pairs = json.dumps(mappings, sort_keys=True, separators=(',', ':')).encode()
    result = {
        'status': 'PASS_SOURCE_CENSUS_NOT_PHYSICAL_JOIN', 'base': BASE,
        'source_pins': PINS, 'native_sha256': WORD_SHA,
        'actual_J_sites': jobs, 'native_instructions': len(word['program']),
        'public_slots_per_call': word['public'], 'owned_labels_excluded': word['owned_fields'],
        'boundary_conversions': 2 * sum(len(row) for row in mappings),
        'fresh_helpers': len(helpers), 'ordered_public_owner_map_sha256': hashlib.sha256(pairs).hexdigest(),
        'first_call_named_slots': {str(slot): mappings[0][slot][1] for slot in (0, 112, 772, 882, 17, 129, 3)},
        'old_producer_on_exact_selected_caller': producer, 'alias_negative_control': control,
        'outcome': 'Blocked at actual physical owner/format production; no new contribution claimed.'
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
