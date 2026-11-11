"""Independent review: reverse timed paths, adjoint rows, and one-input paths.

This script does not import the author's verifier.  Author receipt equality is
checked only after the corresponding data has been recomputed from source.
"""
import argparse
import bisect
import gzip
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

SOURCE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
HISTORICAL_PIN = 'd46db515a5fead49b752b8d798472c883aff7698d7e5e948f0d4e336ec99054b'
BUDGET_PIN = '6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51'
DEADLINES = (28141, 33554, 34467, 37597)
DESTINATIONS = (470, 431, 394, 520)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def check_pin(raw, expected):
    require(digest(raw) == expected, 'pin mismatch')


def binary_span(generators):
    values = {0}
    for generator in generators:
        old = tuple(values)
        values.update(x ^ generator for x in old)
    return frozenset(values)


def sparse_rank(rows):
    # Maximum-column pivots, unlike the author's minimum-column convention.
    pivots = {}
    for original in rows:
        row = {k: Fraction(v) for k, v in original.items() if v}
        while row:
            pivot = max(row)
            if pivot not in pivots:
                lead = row[pivot]
                pivots[pivot] = {k: v / lead for k, v in row.items()}
                break
            lead = row[pivot]
            for k, v in pivots[pivot].items():
                value = row.get(k, Fraction(0)) - lead * v
                if value:
                    row[k] = value
                else:
                    row.pop(k, None)
    return len(pivots)


def determinant(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    answer = Fraction(1)
    for column in range(len(a)):
        choices = [i for i in range(column, len(a)) if a[i][column]]
        if not choices:
            return Fraction(0)
        pivot = choices[-1]
        if pivot != column:
            a[pivot], a[column] = a[column], a[pivot]
            answer = -answer
        lead = a[column][column]
        answer *= lead
        for i in range(column + 1, len(a)):
            factor = a[i][column] / lead
            for j in range(column, len(a)):
                a[i][j] -= factor * a[column][j]
    return answer


def reconstruct_quiet(word, main):
    """Use per-role position histories and contacts, not a moving cohort."""
    positions = {q: [(-1, word['initial'][q])] for q in main}
    arrival = defaultdict(list)
    contacts = defaultdict(set)
    for q in main:
        arrival[q, word['initial'][q]].append(-1)
    for t, e in enumerate(word['program']):
        contacts[e[1]].add(t)
        if e[0] in ('ADD', 'COPY'):
            contacts[e[2]].add(t)
        if e[0] == 'MOVE' and e[1] in main:
            positions[e[1]].append((t, e[3]))
            arrival[e[1], e[3]].append(t)
    contacts = {h: sorted(times) for h, times in contacts.items()}
    position_times = {q: [x[0] for x in hist] for q, hist in positions.items()}
    windows = []
    for t, e in enumerate(word['program']):
        if e[0] != 'MOVE' or e[1] in main:
            continue
        _, h, origin, destination, _ = e
        next_index = bisect.bisect_right(contacts[h], t)
        next_use = contacts[h][next_index] if next_index < len(contacts[h]) else len(word['program'])
        for q in sorted(main):
            position_index = bisect.bisect_left(position_times[q], t) - 1
            if positions[q][position_index][1] != origin:
                continue
            visits = arrival[q, destination]
            later = bisect.bisect_right(visits, t)
            if later < len(visits) and visits[later] < next_use:
                windows.append({'start': t, 'close': visits[later], 'next_use': next_use,
                                'donor': q, 'helper': h, 'from': origin, 'to': destination})
    return windows


def reverse_reachable(word, main, spans, cutoff, destination, extra):
    """Trace target chart backward, with immutable chart waiting at each time."""
    chart_set = {spans[destination]}
    for t in range(cutoff - 1, -1, -1):
        e = word['program'][t]
        if e[0] != 'MOVE':
            continue
        if e[1] in main or e[1] >= word['public'] or t in extra:
            if spans[e[3]] in chart_set:
                chart_set.add(spans[e[2]])
    return {q for q in main if spans[word['initial'][q]] in chart_set}


def adjoint_row(word, main, cutoff, owner):
    """Reverse the exact linear programme from one BEFORE-MOVE output."""
    coefficients = {owner: Fraction(1)}
    for e in reversed(word['program'][:cutoff]):
        operation, destination = e[:2]
        if operation in ('INIT', 'CLEAR'):
            coefficients.pop(destination, None)
        elif operation == 'SCALE':
            if destination in coefficients:
                value = coefficients[destination] * Fraction(e[2])
                if value:
                    coefficients[destination] = value
                else:
                    coefficients.pop(destination)
        elif operation in ('ADD', 'COPY'):
            weight = coefficients.get(destination, Fraction(0))
            if operation == 'COPY':
                coefficients.pop(destination, None)
            if weight:
                source = e[2]
                value = coefficients.get(source, Fraction(0)) + weight * Fraction(e[3])
                if value:
                    coefficients[source] = value
                else:
                    coefficients.pop(source, None)
        elif operation != 'MOVE':
            raise ValueError('unknown operation')
    return {q: value for q, value in coefficients.items() if q in main and value}


def one_input_sender_paths(word, main, spans, extra, relevant, restricted_rows):
    """One independent temporal path search per relevant input coordinate."""
    cutoff = max(DEADLINES)
    moves = [(t, e) for t, e in enumerate(word['program'][:cutoff]) if e[0] == 'MOVE']
    candidates = [(t, e) for t, e in moves
                  if e[1] < word['public'] and e[1] not in main and t not in extra]
    known = {t: set() for t, _ in candidates}
    for q in sorted(relevant):
        reachable = {spans[word['initial'][q]]}
        for t, e in moves:
            origin, destination = spans[e[2]], spans[e[3]]
            if t in known and origin in reachable:
                known[t].add(q)
            if e[1] in main or e[1] >= word['public'] or t in extra:
                if origin in reachable:
                    reachable.add(destination)
    records = []
    classes = defaultdict(list)
    for t, e in candidates:
        support = tuple(sorted(known[t]))
        remaining = sparse_rank([{q: v for q, v in row.items() if q not in known[t]}
                                 for row in restricted_rows])
        require(remaining == 4, 'sender intersection is nonzero')
        records.append([t, e[1], e[2], e[3], list(support), remaining])
        classes[support].append(t)
    return records, [{'known_relevant_q': list(s), 'events': events, 'remaining_rank': 4}
                     for s, events in sorted(classes.items())]


def run(repository, author):
    source_path = repository / 'research/shared-wire-split-composition/data/final.json.gz'
    historical_path = repository / 'research/moonshot-005-program/results/historical-owned/WITNESSES.json'
    budget_path = repository / 'research/moonshot-005-program/results/prepaid-historical-budget/BUDGET.json'
    source, historical_raw, budget_raw = (p.read_bytes() for p in (source_path, historical_path, budget_path))
    check_pin(source, SOURCE_PIN)
    check_pin(historical_raw, HISTORICAL_PIN)
    check_pin(budget_raw, BUDGET_PIN)
    word = json.loads(gzip.decompress(source))
    history = json.loads(historical_raw)
    budget = json.loads(budget_raw)
    receipt = json.loads((author / 'RESULT.json').read_text())
    require((author / 'RESULT.json').read_bytes() == (author / 'RESULT-OPTIMIZED.json').read_bytes(),
            'author normal/-O receipts differ')
    main = set(word['live']) | {r + 112 for r in word['live']} | set(word['hosted']['X2']) | set(word['hosted']['Y2'])
    require(len(main) == 400, 'main count')
    spans = list(map(binary_span, word['frames']))
    require(spans[3] == frozenset({0}), 'entry frame empty')
    require(tuple(c['event'] for c in history) == DEADLINES, 'historical event order')
    require(tuple(c['to'] for c in history) == DESTINATIONS, 'historical destination order')
    actual_owners = tuple(word['program'][t][1] for t in DEADLINES)
    require(all(word['program'][t][0] == 'MOVE' for t in DEADLINES), 'return operations')

    windows = reconstruct_quiet(word, main)
    require(windows == receipt['quiet_windows'], 'quiet-window record mismatch')
    extra = {window['start'] for window in windows}
    require(len(windows) == 354 and len(extra) == 141, 'quiet census')
    plain = {}
    hybrid = {}
    full_rows = []
    for t, destination, owner, inherited in zip(DEADLINES, DESTINATIONS, actual_owners, history):
        plain[t] = reverse_reachable(word, main, spans, t, destination, set())
        hybrid[t] = reverse_reachable(word, main, spans, t, destination, extra)
        require(plain[t] == hybrid[t], 'quiet changes deadline knowledge')
        target = adjoint_row(word, main, t, owner)
        require(target == {int(k): Fraction(v) for k, v in inherited['target_row'].items()},
                'independent adjoint target mismatch')
        full_rows.append(target)
    unreachable = set(main).difference(set().union(*hybrid.values()))
    require(sorted(unreachable) == receipt['common_unreachable_q'], 'unreachable coordinates')
    require(len(unreachable) == 134, 'unreachable count')
    require(all(spans[word['initial'][q]] != spans[3] for q in unreachable), 'entry leakage')
    restricted = [{q: v for q, v in row.items() if q in unreachable} for row in full_rows]
    require([{str(q): str(v) for q, v in row.items()} for row in restricted] == receipt['restricted_rows'],
            'restricted row mismatch')
    require(sparse_rank(restricted) == 4, 'four-row rank')
    require([len(row) for row in restricted] == [32, 29, 34, 36], 'restricted supports')
    demand_checks = []
    for t, destination, row, author_demand in zip(DEADLINES, DESTINATIONS, full_rows, receipt['demands']):
        missing = sorted(q for q in row if spans[word['initial'][q]] != spans[3] and q not in hybrid[t])
        recomputed = {'event': t, 'destination': destination, 'base_reachable_q': sorted(hybrid[t]),
                      'missing_distributed_q': missing, 'missing_count': len(missing)}
        require(recomputed == author_demand, 'deadline demand mismatch')
        demand_checks.append({'event': t, 'known_inputs': len(hybrid[t]), 'missing_distributed': len(missing)})
    columns = [4, 2, 1, 0]
    minor = [[row.get(q, Fraction(0)) for q in columns] for row in restricted]
    require(determinant(minor) == Fraction(-3, 4), 'nonzero minor')

    relevant = set().union(*(set(row) for row in restricted))
    records, classes = one_input_sender_paths(word, main, spans, extra, relevant, restricted)
    records_hash = digest((json.dumps(records, separators=(',', ':')) + '\n').encode())
    require(len(records) == 2221, 'nonquiet sender census')
    require(records_hash == receipt['helper_source_record_sha256'], 'independent sender record hash')
    require(classes == receipt['helper_source_classes'], 'sender classes mismatch')
    all_helper_sources = sum(e[0] == 'MOVE' and e[1] < word['public'] and e[1] not in main
                             for e in word['program'][:max(DEADLINES)])
    require(all_helper_sources == 2277, 'all helper sender census')
    require(sparse_rank(restricted[:3]) == 3, 'three-target rank control')
    synthetic_rank = sparse_rank([{q: v for q, v in row.items() if q not in restricted[0]}
                                  for row in restricted])
    require(synthetic_rank == 3, 'synthetic sender intersection control')
    den = int(budget['additional_per_native_headroom']['denominator'])
    lower, upper = map(int, budget['additional_per_native_headroom']['numerator_bounds'])
    require(3 * den < lower <= upper < 4 * den, 'paid capacity ceiling')
    rejected_corruption = False
    try:
        check_pin(source + b'!', SOURCE_PIN)
    except ValueError:
        rejected_corruption = True
    require(rejected_corruption, 'pin negative control')

    author_files = {p.name: digest(p.read_bytes()) for p in sorted(author.iterdir()) if p.is_file()}
    require(len(author_files) == 6, 'reviewed author file census')
    return {'status': 'PASS_INDEPENDENT_TEMPORAL_REVIEW', 'author_files_sha256': author_files,
            'source_sha256': SOURCE_PIN, 'historical_certificate_sha256': HISTORICAL_PIN,
            'budget_sha256': BUDGET_PIN, 'methods': ['per-role position histories for quiet windows',
            'reverse temporal chart reachability at each BEFORE-return deadline',
            'fresh reverse adjoint programme replay for four target rows',
            'one-input forward paths for every relevant coordinate and every helper sender',
            'maximum-column exact rational elimination and independently evaluated determinant'],
            'quiet_windows': len(windows), 'quiet_unique_arcs': len(extra),
            'quiet_changes_four_deadline_knowledge': False, 'deadlines': demand_checks,
            'unreachable_coordinate_count': len(unreachable), 'restricted_row_rank': 4,
            'restricted_row_supports': [len(row) for row in restricted],
            'minor_columns': columns, 'minor_determinant': str(determinant(minor)),
            'all_helper_senders_before_last_deadline': all_helper_sources,
            'nonquiet_helper_senders_checked': len(records),
            'sender_record_sha256': records_hash, 'sender_classes': len(classes),
            'all_sender_intersection_dimensions': 0, 'paid_extra_arrival_ceiling': 3,
            'controls': {'three_targets_rank': 3, 'synthetic_sender_intersection_dimension': 1,
                         'source_pin_corruption_rejected': rejected_corruption},
            'scope': 'Four specified returned rows decoded BEFORE original return MOVEs under fixed '
                     'main/owned calendar plus the reconstructed 354 quiet windows. The rank4 and '
                     'at-least-two nonquiet helper message conclusions do not transfer automatically '
                     'to S7, which retains these four historical returns. No new kappa.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--author', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.repository, args.author)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'author_files_sha256'}, indent=2, sort_keys=True))
