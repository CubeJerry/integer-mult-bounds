#!/usr/bin/env python3
"""Exact two-coordinate certificate for the PR6144 root-2 packet cut.

The primary interpreter uses normalized integer pairs with a shared power-of-two
 denominator. It imports no predecessor replay or independent implementation.
Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha1, sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
WORD_SHA256 = 'c71985d96bf3d4a35aae111aaba87e376f7367efb4a5686278ef293732757533'
WORD_BLOB = '69b70ee50c697b185ebf585fbe69f2487af32d1d'
README_SHA256 = '51e1e75c6520da76f379af545c06d72c66f1e4b16d86449e8bbc162535ea0bca'
README_BLOB = '7335bd466fb4a0cac2ef5b22b2f7e2005080ef6d'
CHARTS = {3, 595, 738}
ZERO = (0, 0, 0)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read_word():
    pins = json.loads((HERE / 'SOURCES.json').read_text())['vendored_inputs']
    need(len(pins) == 2, 'complete vendored input inventory')
    expected = {'inputs/pr6144-WORD.json.gz': (WORD_SHA256, WORD_BLOB, 119901),
                'inputs/pr6144-README.md': (README_SHA256, README_BLOB, 6834)}
    for pin in pins:
        need(pin['local_path'] in expected, 'known vendored input')
        digest, blob, size = expected[pin['local_path']]
        need((pin['sha256'], pin['git_blob'], pin['size']) == (digest, blob, size),
             'source manifest agrees with immutable pins')
        need(pin['commit'] == '4f3b67e7c37ae270da9584033132866d0cf63e42'
             and pin['repository'] == 'DreamingOfClouds/integer-mult-bounds' and pin['pr'] == 6144,
             'source identity pin')
        data = (HERE / pin['local_path']).read_bytes()
        need(len(data) == size and sha256(data).hexdigest() == digest,
             'immutable vendored input bytes')
        need(sha1(b'blob ' + str(size).encode() + b'\0' + data).hexdigest() == blob,
             'immutable vendored Git blob')
    need({p['local_path'] for p in pins} == set(expected), 'distinct vendored inputs')
    raw = (HERE / 'inputs/pr6144-WORD.json.gz').read_bytes()
    need(sha256(raw).hexdigest() == WORD_SHA256, 'immutable source SHA256')
    need(sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == WORD_BLOB,
         'immutable source Git blob')
    word = json.loads(gzip.decompress(raw))
    need(word['public'] == 770 and word['owned_fields'] == 29, 'source field inventory')
    need(len(word['program']) == 22818 and len(word['frames']) == 1093, 'source word inventory')
    return word


def normalize(a, b, exponent):
    if not (a or b):
        return ZERO
    while exponent and a % 2 == 0 and b % 2 == 0:
        a //= 2
        b //= 2
        exponent -= 1
    return a, b, exponent


def scale(value, coefficient):
    q = Fraction(coefficient)
    den = q.denominator
    need(den > 0 and den & (den - 1) == 0, 'source dyadic coefficient')
    return normalize(value[0] * q.numerator, value[1] * q.numerator,
                     value[2] + den.bit_length() - 1)


def plus(a, b):
    exponent = max(a[2], b[2])
    return normalize((a[0] << (exponent - a[2])) + (b[0] << (exponent - b[2])),
                     (a[1] << (exponent - a[2])) + (b[1] << (exponent - b[2])), exponent)


def rational_pair(value):
    return [str(Fraction(value[0], 1 << value[2])), str(Fraction(value[1], 1 << value[2]))]


def baseline(word):
    """Instrumented zero-packet reference; this is not a supplier candidate."""
    program = word['program']
    exact = {
        12913: ['MOVE', 451, 3, 737, False],
        12918: ['ADD', 451, 228, '1', 737],
        13481: ['COPY', 772, 146, '1', 529],
        14523: ['MOVE', 451, 737, 738, False],
    }
    for index, event in exact.items():
        need(program[index] == event, 'source event anchor ' + str(index))
    packet_reads = [i for i, event in enumerate(program)
                    if event[0] == 'ADD' and event[2] == 772]
    need(packet_reads == [13485, 13487, 13489, 13490, 13614, 13615, 13616, 13617, 13618],
         'complete packet read inventory')
    omitted = set(packet_reads) | {12918, 13481}
    result = []
    for i, event in enumerate(program):
        if i in omitted:
            result.append(None)
        elif i == 12913:
            result.append(['MOVE', 451, 3, 595, False])
        elif i == 14523:
            result.append(['MOVE', 451, 595, 738, False])
        else:
            result.append(event)
    return result, sorted(omitted)


def replay(word, program, audit_envelope=False):
    values = [ZERO for _ in range(799)]
    values[0], values[8] = (1, 0, 0), (0, 1, 0)
    at = word['initial'][:] + [None] * 29
    owned = set()
    observations = Counter()
    roles = set()
    snapshots = {}
    for cut in range(len(program) + 1):
        if audit_envelope:
            # Deliberately enumerate EVERY cut and EVERY field, including
            # unchanged fields, initial states, owned zeroes and final states.
            for role, chart in enumerate(at):
                if chart in CHARTS:
                    need(values[role] == ZERO, f'zero information envelope at cut {cut}, role {role}')
                    observations['early' if cut < 13679 else 'late'] += 1
                    roles.add(role)
        if cut in (12918, 13484, 13679, 14524):
            snapshots[cut] = {r: rational_pair(values[r]) for r in (228, 772, 451, 572)}
        if cut == len(program):
            break
        event = program[cut]
        if event is None:
            continue
        op, target = event[:2]
        need(type(target) is int and 0 <= target < 799, 'valid event target')
        if op == 'MOVE':
            need(at[target] == event[2], f'MOVE source at {cut}')
            need(event[4] is (target in owned), f'MOVE ownership at {cut}')
            at[target] = event[3]
        elif op == 'INIT':
            need(target >= 770 and target not in owned and at[target] is None, 'INIT ownership')
            owned.add(target)
            at[target], values[target] = event[2], ZERO
        elif op == 'CLEAR':
            need(target in owned and at[target] == event[2], 'CLEAR ownership/chart')
            owned.remove(target)
            at[target], values[target] = None, ZERO
        else:
            need(at[target] == event[-1] and at[target] is not None, f'target chart at {cut}')
            if op == 'SCALE':
                values[target] = scale(values[target], event[2])
            else:
                need(op in ('ADD', 'COPY'), 'known source opcode')
                source = event[2]
                need(at[source] == at[target], f'common chart at {cut}')
                value = scale(values[source], event[3])
                if op == 'COPY':
                    need(target in owned and values[target] == ZERO, 'projected COPY zero')
                    values[target] = value
                else:
                    values[target] = plus(values[target], value)
    need(not owned and at[:770] == word['final'], 'source boundary charts/owned return')
    return values, snapshots, dict(observations), sorted(roles)


def determinant(a, b):
    return Fraction(a[0] * b[1] - a[1] * b[0], 1 << (a[2] + b[2]))


def binary_rank(rows):
    pivots = {}
    for value in rows:
        while value:
            bit = value.bit_length() - 1
            if bit not in pivots:
                pivots[bit] = value
                break
            value ^= pivots[bit]
    return len(pivots)


def budgets(word):
    def route_rank_list(route):
        ranks = []
        for first, second in zip(route, route[1:]):
            left, right = word['frames'][first], word['frames'][second]
            need(binary_rank(left) == len(left) and binary_rank(right) == len(right),
                 'route frames have independent binary bases')
            need(binary_rank(left + right) == max(len(left), len(right)),
                 'optimistic route uses nested frame subspaces')
            ranks.append(abs(len(left) - len(right)))
        return ranks

    original = {}
    for role in (772, 497, 451):
        moves = [event for event in word['program'] if event[0] == 'MOVE' and event[1] == role]
        need(all(a[3] == b[2] for a, b in zip(moves, moves[1:])),
             'complete consecutive original route')
        original[role] = route_rank_list([moves[0][2]] + [event[3] for event in moves])
    # These are optimistic profiles, NOT emitted candidates.
    cases = {
        'skip737_and_direct451':
            (original[772] + original[451],
             route_rank_list([529, 520, 595]) + route_rank_list([3, 595, 738, 911, 127])),
        'skip520_737_and_direct497_451':
            (original[772] + original[497] + original[451],
             route_rank_list([529, 595]) + route_rank_list([3, 595, 914, 127])
             + route_rank_list([3, 595, 738, 911, 127])),
    }
    out = {}
    for name, (old, new) in cases.items():
        need(sum(old) == sum(new), 'equal optimistic rank mass')
        curvature = sum(r * (r - 1) for r in new)
        gain_upper = Fraction(17, 5000) * curvature
        need(gain_upper < 1, 'one new uncredited call consumes optimistic gain')
        delta = Counter(new)
        delta.subtract(old)
        out[name] = {'old_ranks': old, 'new_ranks': new,
                     'paid_delta': {str(r): n for r, n in sorted(delta.items()) if n},
                     'sum_new_r_r_minus_1': curvature,
                     'gain_upper_for_0_le_C_le_17_over_5000': str(gain_upper),
                     'gain_upper_after_one_extra_call': str(gain_upper - 1)}
    return out


def derive():
    word = read_word()
    base_program, omitted = baseline(word)
    original, snaps, _, _ = replay(word, word['program'])
    reference, _, counts, roles = replay(word, base_program, audit_envelope=True)
    expected = [ZERO for _ in range(799)]
    for r in (0, 112):
        expected[r] = (1, 0, 0)
    for r in (8, 120):
        expected[r] = (0, 1, 0)
    need(original == expected, 'original complete endpoint on both input columns')
    residual = [plus(a, scale(b, '-1')) for a, b in zip(expected, reference)]
    changed = {str(r): rational_pair(v) for r, v in enumerate(residual) if v != ZERO}
    witness = next(((i, j, determinant(a, b)) for i, a in enumerate(residual)
                    for j, b in enumerate(residual) if i < j and determinant(a, b)), None)
    need(witness is not None, 'rank-two final residual witness')
    i, j, det = witness
    return {
        'status': 'PASS_ROOT2_PACKET_CUT',
        'source_head': '4f3b67e7c37ae270da9584033132866d0cf63e42',
        'word_sha256': WORD_SHA256,
        'columns': [0, 8], 'free_other_input_coordinates': 797,
        'allowed_reference_charts': sorted(CHARTS),
        'original_events': len(word['program']),
        'deleted_reference_event_indices': omitted,
        'recharted_reference_event_indices': [12913, 14523],
        'envelope_observations': counts, 'envelope_observed_roles': roles,
        'all_envelope_projections_zero': True,
        'original_snapshots': {str(k): v for k, v in snaps.items()},
        'final_residual_rows': changed,
        'residual_rank': 2,
        'minor': {'rows': [i, j], 'matrix': [rational_pair(residual[i]), rational_pair(residual[j])],
                  'determinant': str(det)},
        'optimistic_budgets': budgets(word),
        'scope': 'One fixed linear packet; arbitrary linear recoding at the declared reference-chart contacts; fixed outside program. No new kappa.',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = derive()
    path = HERE / 'CERTIFICATE.json'
    if args.write:
        path.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    else:
        expected = json.loads(path.read_text())
        need(json.dumps(expected, sort_keys=True, separators=(',', ':')) ==
             json.dumps(result, sort_keys=True, separators=(',', ':')),
             'complete certificate equality')
    print(result['status'], 'residual_rank=2', 'minor=' + result['minor']['determinant'],
          'observations=' + str(sum(result['envelope_observations'].values())))


if __name__ == '__main__':
    main()
