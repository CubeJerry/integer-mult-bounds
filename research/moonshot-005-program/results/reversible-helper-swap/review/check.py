#!/usr/bin/env python3
"""Independent swap composition review: exact adjoint/pulse, word identity and types."""
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
EVENT, DONOR, RECEIVER, HELPER = 41779, 60, 213, 1024


def need(value, message):
    if not value:
        raise ValueError(message)


def read_gz(path):
    raw = path.read_bytes()
    payload = gzip.decompress(raw)
    return json.loads(payload), hashlib.sha256(raw).hexdigest(), hashlib.sha256(payload).hexdigest()


def serial(row):
    return [[i, str(value)] for i, value in sorted(row.items()) if value]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def span(frame):
    values = {0}
    for vector in frame:
        values.update([a ^ vector for a in list(values)])
    return values


def exact_cut(source):
    # An adjoint of the prefix, independent of the author's full forward row replay.
    coeff = {HELPER: F(1)}
    for operation in reversed(source['program'][:EVENT]):
        kind, a = operation[:2]
        if kind in ('INIT', 'CLEAR'):
            coeff.pop(a, None)
        elif kind == 'SCALE':
            coeff[a] = coeff.get(a, F(0)) * F(operation[2])
        elif kind in ('ADD', 'COPY'):
            b, c = operation[2], F(operation[3])
            coeff[b] = coeff.get(b, F(0)) + c * coeff.get(a, F(0))
            if kind == 'COPY':
                coeff.pop(a, None)
        elif kind != 'MOVE':
            raise ValueError('unknown source opcode')
    h = {i: value for i, value in coeff.items() if value}
    need(all(0 <= i < 1480 for i in h), 'adjoint reaches only independent public inputs')
    pulse = {HELPER: F(1)}
    guards = []
    for index, operation in enumerate(source['program'][EVENT:], EVENT):
        kind, a = operation[:2]
        if kind in ('INIT', 'CLEAR'):
            pulse.pop(a, None)
        elif kind == 'SCALE':
            pulse[a] = pulse.get(a, F(0)) * F(operation[2])
        elif kind in ('ADD', 'COPY'):
            b, c = operation[2], F(operation[3])
            if kind == 'COPY':
                guards.append([index, str(pulse.get(a, F(0)))])
                need(not pulse.get(a, F(0)), 'perturbed COPY guard')
            pulse[a] = pulse.get(a, F(0)) + c * pulse.get(b, F(0))
        elif kind != 'MOVE':
            raise ValueError('unknown source opcode')
    z = {i: value for i, value in pulse.items() if value}
    need(z and all(i < 1480 and source['final'][i] == 127 for i in z), 'nonzero response lies at actual hub')
    return h, z, guards


def expected_word(source, raw, cache, z):
    ops = [['ADD', raw[role], role, '-1', source['initial'][role]] for role in sorted(raw)]
    reservations = []
    markers = {}
    rename = lambda role: role + 400 if role >= 1480 else role
    for index, operation in enumerate(source['program']):
        if index == EVENT:
            markers['swap_start'] = len(ops)
            ops += [['ADD', HELPER, raw[DONOR], '1', 962], ['ADD', raw[DONOR], HELPER, '-1', 962], ['ADD', HELPER, raw[DONOR], '1', 962], ['SCALE', raw[DONOR], '-1', 962]]
        mapped = list(operation)
        mapped[1] = rename(mapped[1])
        if mapped[0] in ('ADD', 'COPY'):
            mapped[2] = rename(mapped[2])
        ops.append(mapped)
        if index == EVENT:
            markers['receiver_observation'] = len(ops)
            ops += [['ADD', raw[RECEIVER], HELPER, '1', 221], ['INIT', cache, 221], ['ADD', cache, HELPER, '1', 221], ['MOVE', cache, 221, 127, True]]
        if operation[0] == 'MOVE' and operation[1] in raw:
            reservations.append({'source_event': index, 'physical_event': len(ops), 'role': operation[1]})
            ops.append(['MOVE', raw[operation[1]], operation[2], operation[3], False])
    markers['common_completion'] = len(ops)
    ops += [['ADD', cache, raw[DONOR], '-1', 127]]
    ops += [['ADD', role, cache, str(-value), 127] for role, value in sorted(z.items())]
    ops += [['ADD', raw[DONOR], cache, '1', 127], ['CLEAR', cache, 127]]
    markers['common_and_raw_restored'] = len(ops)
    ops += [['ADD', raw[role], role, '1', source['final'][role]] for role in sorted(raw)]
    return ops, reservations, markers


def types_and_counts(source, word):
    locations = dict(enumerate(word['initial']))
    spaces = [span(frame) for frame in source['frames']]
    counts, moves = Counter(), Counter()
    peak = 0
    for operation in word['program']:
        kind, a = operation[:2]
        need(0 <= a < word['public'] + word['owned_fields'], 'role namespace')
        counts[kind] += 1
        if kind == 'INIT':
            need(a >= 1880 and a not in locations, 'fresh owned initialization')
            locations[a] = operation[2]
        elif kind == 'CLEAR':
            need(a >= 1880 and locations.get(a) == operation[2], 'owned retirement at real chart')
            del locations[a]
        elif kind == 'MOVE':
            before, after, owned = operation[2:]
            need(locations.get(a) == before and type(owned) is bool and owned == (a >= 1880), 'MOVE ownership/location')
            need(spaces[before] < spaces[after] or owned and spaces[after] < spaces[before], 'proper nested MOVE')
            locations[a] = after
            moves[abs(len(source['frames'][before]) - len(source['frames'][after]))] += 1
        elif kind in ('ADD', 'COPY'):
            b, coefficient, chart = operation[2:]
            need(a != b and locations.get(a) == locations.get(b) == chart, 'cochart arithmetic')
            F(coefficient)
        elif kind == 'SCALE':
            need(locations.get(a) == operation[3] and F(operation[2]) != 0, 'nonzero cochart scaling')
        else:
            raise ValueError('unknown word opcode')
        peak = max(peak, len(locations) - 1880)
    need(set(locations) == set(range(1880)), 'all owned fields retired')
    raw = {int(role): physical for role, physical in word['private_role_map'].items()}
    for role in range(1480):
        need(locations[role] == source['final'][role], 'common final chart')
    for role, physical in raw.items():
        need(locations[physical] == source['final'][role], 'raw final chart')
    return dict(counts), {str(rank): count for rank, count in sorted(moves.items())}, peak


def main():
    source, source_hash, _ = read_gz(REPO / 'research/shared-wire-split-composition/data/final.json.gz')
    word, _, word_hash = read_gz(PACKET / 'SWAP-WORD.json.gz')
    report_bytes = (PACKET / 'RESULT.json').read_bytes()
    report = json.loads(report_bytes)
    pin = json.loads((PACKET / 'WORD-PIN.json').read_text())
    need(source_hash == '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883', 'native source pin')
    need(word_hash == pin['decompressed_sha256'] == '13197190b0030fcc5100f35ae1d71a15e350708bafa000fc0dea39b48e3a9f96', 'reviewed exact word payload')
    need(source['program'][EVENT] == ['MOVE', HELPER, 962, 221, False], 'exact source event')
    h, z, guards = exact_cut(source)
    need(serial(h) == report['actual_displaced_common_row'] and serial(z) == report['neutral_hub_response'], 'independent source h and z')
    loss, loss_hash, _ = read_gz(REPO / 'research/moonshot-005-program/results/single-overwrite-loss/CERTIFICATE.json.gz')
    need(loss_hash == '8a500a84ec0b1dd3a10c38278d522908ccfc8f999625edff4d02fa1a898e7181', 'independently reviewed loss certificate pin')
    old = next(record for record in loss['records'] if record['event'] == EVENT)
    need(old['payload_sha256'] == digest(serial(h)) and old['response_sha256'] == digest(serial(z)), 'source rows match retained independent review')
    need(not old['hub_recoverable_payload'], 'outside-hub payload scope')
    mains = sorted(set(source['live']) | {i + 112 for i in source['live']} | set(source['hosted']['X2']) | set(source['hosted']['Y2']))
    raw = {role: 1480 + index for index, role in enumerate(mains)}
    need(len(raw) == 400 and {str(role): physical for role, physical in raw.items()} == word['private_role_map'], 'complete actual raw bank')
    cache = 1880 + source['owned_fields']
    expected, reservations, marks = expected_word(source, raw, cache, z)
    need(word['program'] == expected and word['raw_reservations'] == reservations and word['marks'] == marks, 'literal source subsequence and inserted operations')
    need(len(reservations) == len({r['source_event'] for r in reservations}) == 1710, 'all raw MOVE reservations used exactly once')
    need(word['initial'] == source['initial'] + [source['initial'][role] for role in mains], 'initial physical charts')
    need(word['public'] == 1880 and word['owned_fields'] == source['owned_fields'] + 1, 'declared record namespace')
    counts, moves, peak = types_and_counts(source, word)
    need(counts == report['bill']['opcode_counts'] and moves == report['bill']['move_rank_histogram'] and peak == report['bill']['peak_owned'] == 43, 'independent physical invoice')
    native_counts = Counter(op[0] for op in source['program'])
    baseline = native_counts + Counter({'ADD': 800, 'MOVE': 1710})
    incremental = {opcode: counts.get(opcode, 0) - baseline.get(opcode, 0) for opcode in ['ADD', 'SCALE', 'MOVE', 'INIT', 'CLEAR', 'COPY']}
    need(incremental == {'ADD': 32, 'SCALE': 1, 'MOVE': 1, 'INIT': 1, 'CLEAR': 1, 'COPY': 0}, 'complete incremental count')
    # Literal swap and terminal restoration on independent common h, raw q, receiver r.
    H, donor, receiver = [F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]
    add = lambda a, b, c=F(1): [x + c*y for x, y in zip(a, b)]
    H = add(H, donor)
    donor = add(donor, H, F(-1))
    H = add(H, donor)
    donor = [-x for x in donor]
    need(H == [0, 1, 0] and donor == [1, 0, 0], 'reversible swap on independent values')
    receiver = add(receiver, H)
    returned = H.copy()
    difference = add(returned, donor, F(-1))
    need(difference == [-1, 1, 0], 'real retained records produce q-h')
    for coefficient in z.values():
        perturbation = [coefficient * x for x in difference]
        need(add(perturbation, difference, -coefficient) == [0, 0, 0], 'every common pulse corrected')
    donor = add(donor, difference)
    need(donor == [0, 1, 0] and receiver == [0, 1, 1], 'declared invertible raw shear')
    source_copies = [i for i, op in enumerate(source['program']) if op[0] == 'COPY']
    need(source_copies == [31737] and all(i < EVENT for i in source_copies) and not guards, 'actual COPY guard unchanged by later loan')
    need(-2 * z[52] * h[2] == -1 and raw[DONOR] == 1535 and raw[RECEIVER] == 1677, 'negative-control coefficients')
    result = {'status': 'PASS_INDEPENDENT_SWAP_SOURCE_COMPOSITION_AND_TYPES', 'source_sha256': source_hash, 'word_payload_sha256': word_hash, 'author_result_sha256': hashlib.sha256(report_bytes).hexdigest(), 'source_h_method': 'Backward adjoint of the literal source prefix', 'source_z_method': 'Exact one-dimensional suffix pulse', 'payload_support': len(h), 'response_support': len(z), 'instructions': len(word['program']), 'opcode_counts': counts, 'move_rank_histogram': moves, 'peak_owned': peak, 'incremental_counts': incremental, 'raw_reservations_once': len(reservations), 'all_common_rows_restored_by_identity': 1480, 'all_private_rows_preserved_by_invertible_shear': 400, 'source_guard_unchanged': source_copies, 'scope': 'Exact typed-word comparison, independently reconstructed cut/pulse and universal composition proof using the reviewed pinned native baseline. Does not rerun a full1880-column baseline replay. A single cross-coordinate shear, not the complete private target, supplier or kappa improvement.'}
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
