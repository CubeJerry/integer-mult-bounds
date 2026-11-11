#!/usr/bin/env python3
"""Exact all-history annihilation of route-eligible initial helper columns.

No predecessor, search, or author-review implementation is imported. This
verifier propagates eligible helper columns through every source instruction,
including local scalar writes, rather than inferring observability from a
timed graph or a sampled set of inputs.
"""
import argparse, collections, gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path

SOURCE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def space(basis):
    answer = {0}
    for vector in basis:
        answer.update(x ^ vector for x in tuple(answer))
    return frozenset(answer)

def axpy(left, right, scalar):
    result = left.copy()
    for q, value in right.items():
        new = result.get(q, F(0)) + scalar * value
        if new:
            result[q] = new
        else:
            result.pop(q, None)
    return result

def adjoint(program, output, allowed):
    row = {output: F(1)}
    for instruction in reversed(program):
        operation, destination = instruction[:2]
        value = row.get(destination, F(0))
        if not value:
            continue
        if operation in ('INIT', 'CLEAR'):
            del row[destination]
        elif operation == 'SCALE':
            row[destination] = value * F(instruction[2])
            if not row[destination]:
                del row[destination]
        elif operation in ('ADD', 'COPY'):
            source = instruction[2]
            need(source != destination, 'distinct source and destination')
            if operation == 'COPY':
                del row[destination]
            row = axpy(row, {source: value}, F(instruction[3]))
    return {q: value for q, value in row.items() if q in allowed}

def run(args):
    path = args.repository / 'research/shared-wire-split-composition/data/final.json.gz'
    need(sha(path) == SOURCE, 'pinned source word')
    word = json.loads(gzip.decompress(path.read_bytes()))
    program = word['program']
    charts = [space(frame) for frame in word['frames']]
    representative = {}
    for label, chart in enumerate(charts):
        representative.setdefault(chart, label)
    mains = set(word['live']) | {q + 112 for q in word['live']} | set(word['hosted']['X2']) | set(word['hosted']['Y2'])
    donors = {q for q in mains if charts[word['initial'][q]] != charts[3]}
    receivers = mains - donors
    helpers = set(range(word['public'])) - mains
    need(len(mains) == 400 and len(donors) == len(receivers) == 200 and len(helpers) == 1080, 'source role partition')
    itinerary = {q: [charts[word['initial'][q]]] for q in mains}
    for instruction in program:
        if instruction[0] == 'MOVE' and instruction[1] in mains:
            itinerary[instruction[1]].append(charts[instruction[3]])
    need(all(len(set(route)) == len(route) for route in itinerary.values()), 'monotone distinct main chart visits')
    eligible = {x: {h for h in helpers if charts[word['initial'][h]] in itinerary[x] and charts[word['final'][h]] == charts[127]} for x in donors}
    all_eligible = set().union(*eligible.values())
    need(len(all_eligible) == 45 and sum(bool(hs) for hs in eligible.values()) == 88, 'all eligible helper sets')
    pairs = []
    endpoint_rows = {}
    for y in sorted(receivers):
        row = adjoint(program, y, mains)
        endpoint_rows[y] = row
        for x in sorted(set(row) & donors):
            pairs.append({'donor': x, 'receiver': y, 'endpoint_coefficient': str(row[x])})
    pairs.sort(key=lambda pair: (pair['donor'], pair['receiver']))
    need(len(pairs) == 104, '104 actual nonentry-to-entry endpoint dependencies')
    nontrivial = [pair for pair in pairs if eligible[pair['donor']]]
    need(len(nontrivial) == 46, '46 nonempty helper-access dependencies')
    forbidden = collections.defaultdict(set)
    demands = collections.defaultdict(list)
    for pair in nontrivial:
        x, y = pair['donor'], pair['receiver']
        for chart in itinerary[y]:
            forbidden[chart].update(eligible[x])
            demands[chart].append((x, y))
    rows = {q: ({q: F(1)} if q in all_eligible else {}) for q in range(word['public'])}
    positions = dict(enumerate(word['initial']))
    counters = collections.Counter()
    per_pair = collections.Counter()
    def observe(role, event):
        chart = charts[positions[role]]
        counters['all_historical_field_states'] += 1
        if chart in forbidden:
            counters['relevant_historical_field_states'] += 1
            counters['nonzero_other_helper_rows_at_relevant_charts'] += bool(rows[role])
            need(not set(rows[role]) & forbidden[chart], 'eligible helper column reaches receiver history at event ' + str(event))
            for pair in demands[chart]:
                per_pair[pair] += 1
    for q in sorted(rows):
        observe(q, -1)
    for time, instruction in enumerate(program):
        operation, destination = instruction[:2]
        if operation == 'INIT':
            need(destination not in positions, 'fresh source-owned field')
            positions[destination] = instruction[2]
            rows[destination] = {}
        elif operation == 'CLEAR':
            need(destination >= word['public'], 'owned retirement only')
            del positions[destination]
            del rows[destination]
            continue
        elif operation == 'MOVE':
            need(positions[destination] == instruction[2], 'actual MOVE source')
            positions[destination] = instruction[3]
        elif operation == 'ADD':
            source, coefficient, chart = instruction[2:]
            need(charts[positions[destination]] == charts[positions[source]] == charts[chart], 'cochart source ADD')
            rows[destination] = axpy(rows[destination], rows[source], F(coefficient))
        elif operation == 'COPY':
            rows[destination] = {q: F(instruction[3]) * value for q, value in rows[instruction[2]].items() if F(instruction[3]) * value}
        elif operation == 'SCALE':
            rows[destination] = {q: F(instruction[2]) * value for q, value in rows[destination].items() if F(instruction[2]) * value}
        else:
            raise ValueError('unrecognized source instruction')
        observe(destination, time)
    need(all(positions[q] == word['final'][q] for q in range(word['public'])), 'all final public charts')
    need(set(per_pair) == {(pair['donor'], pair['receiver']) for pair in nontrivial}, 'all nontrivial dependency histories checked')
    # Control 1: actual native main-input injection reaches its required output.
    first = nontrivial[0]
    x, y = first['donor'], first['receiver']
    main_effect = endpoint_rows[y][x]
    need(main_effect != 0 and not set(rows[y]) & eligible[x], 'main/helper perturbation distinction')
    # Control 2: hub access exposes the eligible helper input coordinates.
    largest = max(nontrivial, key=lambda pair: (len(eligible[pair['donor']]), -pair['donor']))
    a, b = largest['donor'], largest['receiver']
    hs = sorted(eligible[a])
    need(len(hs) == 9 and charts[127] not in itinerary[b], 'genuine off-itinerary hub control')
    for helper in hs:
        need(adjoint(program, helper, set(range(word['public']))) == {helper: F(1)}, 'full-input helper identity endpoint control')
        need(charts[word['final'][helper]] == charts[127], 'actual helper hub endpoint')
    controls = [
        {'change': 'inject into the actual common main input rather than an eligible helper input', 'donor': x, 'receiver': y, 'endpoint_coefficient': str(main_effect), 'outside_scope': 'This modifies a required common-main endpoint; it is not an initial-helper substitution.'},
        {'change': 'grant receiver access to final helper rows at chart127', 'donor': a, 'receiver': b, 'helper_inputs': hs, 'independent_observable_modes': len(hs), 'outside_scope': 'Chart127 is absent from the receiver itinerary; these nine exact identity rows become available only under changed geometric access.'},
    ]
    certificate = {
        'source_sha256': SOURCE,
        'all_eligible_helper_inputs': sorted(all_eligible),
        'all_nonentry_donor_eligible_helper_sets': {str(x): sorted(hs) for x, hs in sorted(eligible.items())},
        'required_endpoint_dependencies': pairs,
        'nontrivial_dependency_histories': [dict(pair, donor_itinerary=[representative[c] for c in itinerary[pair['donor']]], receiver_itinerary=[representative[c] for c in itinerary[pair['receiver']]], eligible_helper_inputs=sorted(eligible[pair['donor']]), historical_states_checked=per_pair[pair['donor'], pair['receiver']], all_eligible_columns_zero=True) for pair in nontrivial],
        'history_census': dict(sorted(counters.items())),
        'controls': controls,
    }
    destination = args.packet / 'CERTIFICATE.json'
    serialized = json.dumps(certificate, indent=2, sort_keys=True) + '\n'
    if args.write_certificate:
        destination.write_text(serialized)
    else:
        need(destination.read_text() == serialized, 'exact certificate reproduction')
    return {'status': 'PASS_ALL_HISTORY_INITIAL_HELPER_COLUMN_ANNIHILATION', 'source_sha256': SOURCE, 'certificate_sha256': sha(destination), 'native_instructions': len(program), 'nonentry_donors': len(donors), 'entry_receivers': len(receivers), 'eligible_initial_helpers': len(all_eligible), 'donors_with_nonempty_eligible_set': sum(bool(hs) for hs in eligible.values()), 'actual_required_endpoint_dependencies': len(pairs), 'nontrivial_nonempty_helper_dependency_pairs': len(nontrivial), 'trivial_empty_helper_dependency_pairs': len(pairs)-len(nontrivial), 'all_eligible_helper_columns_zero_on_all_receiver_histories': True, 'history_census': dict(sorted(counters.items())), 'negative_controls': controls, 'scope': 'For every actual nonentry-to-entry endpoint dependency, arbitrary changes confined to helper inputs initially accessible on the donor itinerary and ending at127 leave every native historical observation on the receiver itinerary unchanged. Observation and donor/receiver access clocks waived; common native instruction order fixed. Does not cover midrun state injection, changed native operations, extra observation geometry, or additional source channels. No new kappa.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write-certificate', action='store_true')
    arguments = parser.parse_args()
    result = run(arguments)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'])
