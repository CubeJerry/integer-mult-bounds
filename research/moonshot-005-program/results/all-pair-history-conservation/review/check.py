#!/usr/bin/env python3
"""Independent exact per-pair adjoint review of the104-pair history certificate."""
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import time

REPO = Path(__file__).resolve().parents[5]
SOURCE = REPO / 'research/shared-wire-split-composition/data/final.json.gz'
CERT = Path(__file__).resolve().parents[1] / 'CERTIFICATE.json.gz'
SOURCE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT_PIN = '073f1fc82cc83800401cf966c210d2f9ae7e533d95a2da4a2da9bfa0c2fc493e'


def need(value, message):
    if not value:
        raise ValueError(message)


def span(frame):
    values = {0}
    for vector in frame:
        values.update([a ^ vector for a in list(values)])
    return tuple(sorted(values))


def axpy(destination, source, scale):
    for index, value in source.items():
        value = destination.get(index, F(0)) + scale * value
        if value:
            destination[index] = value
        else:
            destination.pop(index, None)


def pair_check(source, records, allowed, canonical, scalars):
    """Keep only one donor/receiver pair's independent observation duals at a time."""
    adjoint = [{} for _ in range(source['public'] + source['owned_fields'])]
    observed = defaultdict(list)
    for index, record in enumerate(records):
        for role, coefficient in record['endpoint_coefficients']:
            adjoint[role][index] = -F(coefficient)
        observed[record['after_event']].append(index)
    locations = dict(enumerate(source['final']))
    checks = 0
    entries = 0
    def inspect(role, cut):
        nonlocal checks, entries
        checks += 1
        if role not in locations:
            return None
        entries += len(adjoint[role])
        if canonical[locations[role]] in allowed and adjoint[role]:
            index = min(adjoint[role])
            return {'cut': cut, 'role': role, 'chart': locations[role], 'identity_after_event': records[index]['after_event'], 'identity_role': records[index]['role'], 'coefficient': str(adjoint[role][index])}
        return None
    for role in locations:
        witness = inspect(role, len(source['program']))
        if witness:
            return witness, checks, entries
    for event in range(len(source['program']) - 1, -1, -1):
        for index in observed.get(event, ()):
            role = records[index]['role']
            need(locations[role] == records[index]['chart'], 'observation is at its actual post-MOVE chart')
            value = adjoint[role].get(index, F(0)) + 1
            if value:
                adjoint[role][index] = value
            else:
                adjoint[role].pop(index, None)
            witness = inspect(role, event + 1)
            if witness:
                return witness, checks, entries
        operation = source['program'][event]
        kind, role = operation[:2]
        changed = []
        if kind == 'ADD':
            donor = operation[2]
            axpy(adjoint[donor], adjoint[role], scalars[operation[3]])
            changed.append(donor)
        elif kind == 'COPY':
            donor = operation[2]
            axpy(adjoint[donor], adjoint[role], scalars[operation[3]])
            adjoint[role] = {}
            changed += [donor, role]
        elif kind == 'SCALE':
            coefficient = scalars[operation[2]]
            adjoint[role] = {index: coefficient * value for index, value in adjoint[role].items() if coefficient * value}
            changed.append(role)
        elif kind == 'MOVE':
            need(locations[role] == operation[3], 'reverse source location')
            locations[role] = operation[2]
            changed.append(role)
        elif kind == 'CLEAR':
            need(role not in locations, 'reverse owned retirement')
            locations[role] = operation[2]
            adjoint[role] = {}
            changed.append(role)
        elif kind == 'INIT':
            need(locations[role] == operation[2], 'reverse owned initialization')
            del locations[role]
            adjoint[role] = {}
        else:
            raise ValueError('unrecognized source opcode')
        for changed_role in changed:
            witness = inspect(changed_role, event)
            if witness:
                return witness, checks, entries
    need(locations == dict(enumerate(source['initial'])), 'complete reverse location replay')
    return None, checks, entries


def main():
    start = time.monotonic()
    source_bytes = SOURCE.read_bytes()
    cert_payload = gzip.decompress(CERT.read_bytes())
    need(hashlib.sha256(source_bytes).hexdigest() == SOURCE_PIN, 'source pin')
    need(hashlib.sha256(cert_payload).hexdigest() == CERT_PIN, 'certificate payload pin')
    source = json.loads(gzip.decompress(source_bytes))
    certificate = json.loads(cert_payload)
    need(certificate['source_sha256'] == SOURCE_PIN and certificate['native_instructions'] == len(source['program']) == 71261, 'source metadata')
    first = {}
    canonical = []
    for index, frame in enumerate(source['frames']):
        first.setdefault(span(frame), index)
        canonical.append(first[span(frame)])
    xs = source['live']
    ys = [role + 112 for role in xs]
    need(len(xs) == 104 and certificate['endpoint_roles'] == ys, '104 active paired endpoints')
    routes = {role: [canonical[source['initial'][role]]] for role in xs + ys}
    for operation in source['program']:
        if operation[0] == 'MOVE' and operation[1] in routes:
            routes[operation[1]].append(canonical[operation[3]])
    station_sets = []
    observing_pairs = defaultdict(list)
    for index, (x, y) in enumerate(zip(xs, ys)):
        donor_stations, receiver_stations = set(routes[x]), set(routes[y])
        need(not donor_stations.intersection(receiver_stations), 'paired donor and receiver chart sets disjoint')
        station_sets.append(donor_stations)
        for chart in receiver_stations:
            observing_pairs[chart].append(index)
        expected_pair = {'donor': x, 'receiver': y, 'donor_station_charts': routes[x], 'receiver_route_charts': routes[y], 'initial_observations': sum(canonical[chart] in receiver_stations for chart in source['initial'])}
        need(certificate['pairs'][index] == expected_pair, 'independent source itinerary and initial observation census')
    expected_arrivals = []
    for event, operation in enumerate(source['program']):
        if operation[0] == 'MOVE':
            for pair in observing_pairs[canonical[operation[3]]]:
                expected_arrivals.append({'pair': pair, 'donor': xs[pair], 'receiver': ys[pair], 'after_event': event, 'role': operation[1], 'chart': operation[3]})
    records = certificate['arrival_identities']
    need(len(records) == len(expected_arrivals) == 2846, 'exhaustive source arrival census')
    by_pair = [[] for _ in xs]
    term_histogram = Counter()
    for record, expected in zip(records, expected_arrivals):
        need({key: value for key, value in record.items() if key != 'endpoint_coefficients'} == expected, 'arrival source/version binding')
        seen = set()
        for role, coefficient in record['endpoint_coefficients']:
            need(role in ys and role not in seen and F(coefficient), 'nonzero independent endpoint coefficients')
            seen.add(role)
        term_histogram[len(seen)] += 1
        by_pair[record['pair']].append(record)
    scalars = {}
    for operation in source['program']:
        if operation[0] in ('ADD', 'COPY'):
            scalars[operation[3]] = F(operation[3])
        elif operation[0] == 'SCALE':
            scalars[operation[2]] = F(operation[2])
    total_checks = total_entries = 0
    for pair, pair_records in enumerate(by_pair):
        witness, checks, entries = pair_check(source, pair_records, station_sets[pair], canonical, scalars)
        need(witness is None, json.dumps({'pair': pair, 'failure': witness}))
        total_checks += checks
        total_entries += entries
        if pair % 16 == 15 or pair == 103:
            print('EXACT_PAIRS', pair + 1, 'elapsed', round(time.monotonic() - start, 2), flush=True)
    # Wrong endpoint coefficient: perturb the first identity by its paired Y endpoint.
    first_record = records[0]
    pair = first_record['pair']
    mutant = [dict(record) for record in by_pair[pair]]
    position = next(i for i, record in enumerate(mutant) if record['after_event'] == first_record['after_event'] and record['role'] == first_record['role'])
    coeffs = {role: F(value) for role, value in mutant[position]['endpoint_coefficients']}
    coeffs[ys[pair]] = coeffs.get(ys[pair], F(0)) + 1
    mutant[position]['endpoint_coefficients'] = [[role, str(value)] for role, value in sorted(coeffs.items()) if value]
    wrong_lambda, _, _ = pair_check(source, mutant, station_sets[pair], canonical, scalars)
    need(wrong_lambda is not None, 'wrong lambda mutation must fail')
    # Enlarge only this pair's donor access to one actual receiver chart.
    extra_chart = canonical[first_record['chart']]
    need(extra_chart not in station_sets[pair], 'negative-control chart is outside the admitted donor stations')
    extra_access, _, _ = pair_check(source, by_pair[pair], station_sets[pair] | {extra_chart}, canonical, scalars)
    need(extra_access is not None, 'added forbidden chart must invalidate a certified relation')
    result = {'status': 'PASS_INDEPENDENT_EXACT_ALL104_PAIR_HISTORY_REVIEW', 'source_sha256': SOURCE_PIN, 'certificate_payload_sha256': CERT_PIN, 'independent_parser': True, 'method': 'Separate exact rational adjoint replay for each donor/receiver pair; no author imports or extraction algorithm', 'pairs': 104, 'arrivals': 2846, 'source_cuts': len(source['program']) + 1, 'per_pair_changed_role_checks': total_checks, 'per_pair_nonzero_entries_inspected': total_entries, 'term_count_histogram': dict(sorted(term_histogram.items())), 'negative_controls': {'wrong_endpoint_coefficient': wrong_lambda, 'additional_donor_chart': {'added_chart': extra_chart, 'witness': extra_access}}, 'elapsed_seconds': time.monotonic() - start, 'scope': 'All live-role controls at all original stations for each donor separately. Arrival responses factor through104 commonY endpoint responses. Does not grant the union of all donor stations or extra raw/mixed histories. Exact source/certificate review, not a multiplication theorem.'}
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
