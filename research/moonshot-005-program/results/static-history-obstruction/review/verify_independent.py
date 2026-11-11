#!/usr/bin/env python3
"""Independent reverse-reachability audit of the S004 static history cut.

Imports neither the proposed verifier nor any predecessor implementation.
Uses exhaustive binary chart spaces, reverse graph reachability, a reverse
touch pass, forward prefix replay, and reverse source adjoints.
"""
import argparse
import collections
import gzip
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

NATIVE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PREFIX = 'e87e4bfcb9772b232e6c443cf2d8ee79a7de356d381eda3aa42040e5e37003c0'
BUDGET = 'b5c4a118bb7e72a31d7ba90a8cd4b72884f9fa6470710850119d709ad3f21f40'
OLD = 'a980369a753febb491038c82f6e88f553efc5fbd7c6049abc0101d71c8659c7c'

def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def space(basis):
    result = {0}
    for vector in basis:
        result.update(x ^ vector for x in tuple(result))
    return frozenset(result)

def plus(left, right, scale=F(1)):
    answer = left.copy()
    for variable, coefficient in right.items():
        new = answer.get(variable, F(0)) + scale * coefficient
        if new:
            answer[variable] = new
        else:
            answer.pop(variable, None)
    return answer

def row_rank(rows):
    pivots = {}
    for original in rows:
        value = original.copy()
        while value:
            pivot = min(value)
            if pivot in pivots:
                value = plus(value, pivots[pivot], -value[pivot])
            else:
                denominator = value[pivot]
                pivots[pivot] = {x: c / denominator for x, c in value.items()}
                break
    return len(pivots)

def ancestors(targets, arrows):
    reverse = collections.defaultdict(set)
    for source, destination in arrows:
        reverse[destination].add(source)
    visited = set(targets)
    stack = list(visited)
    while stack:
        current = stack.pop()
        for source in reverse[current] - visited:
            visited.add(source)
            stack.append(source)
    return visited

def native_row(program, output, selected):
    row = {output: F(1)}
    for instruction in program[::-1]:
        operation, destination = instruction[:2]
        weight = row.get(destination, F(0))
        if not weight:
            continue
        if operation in ('CLEAR', 'INIT'):
            del row[destination]
        elif operation == 'SCALE':
            row[destination] = weight * F(instruction[2])
            if not row[destination]:
                del row[destination]
        elif operation in ('COPY', 'ADD'):
            source, coefficient = instruction[2:4]
            require(source != destination, 'source word has no self assignment')
            if operation == 'COPY':
                del row[destination]
            row = plus(row, {source: weight}, F(coefficient))
    return {x: y for x, y in row.items() if x in selected}

def prefix_state(prefix, charts, selected):
    positions = dict(enumerate(prefix['initial']))
    rows = {i: {} for i in positions}
    qmap = {int(q): i for q, i in prefix['difference_role_map'].items()}
    for q in selected:
        rows[qmap[q]] = {q: F(1)}
    for instruction in prefix['program']:
        operation, destination = instruction[:2]
        if operation == 'INIT':
            require(destination not in positions, 'fresh prefix owner')
            positions[destination] = instruction[2]
            rows[destination] = {}
        elif operation == 'CLEAR':
            require(destination >= prefix['public'], 'only owner clear')
            del positions[destination]
            del rows[destination]
        elif operation == 'MOVE':
            require(positions[destination] == instruction[2], 'prefix MOVE source')
            positions[destination] = instruction[3]
        elif operation == 'ADD':
            source, coefficient, chart = instruction[2:]
            require(charts[positions[destination]] == charts[positions[source]] == charts[chart], 'prefix cochart ADD')
            rows[destination] = plus(rows[destination], rows[source], F(coefficient))
        else:
            raise ValueError('unexpected prefix instruction')
    return positions, rows

def quiet_and_history(word, mains, charts):
    program = word['program']
    finish = len(program)
    # Next-touch times come from one reverse scan, independently of bisect.
    next_touch = {}
    deadlines = {}
    for time in range(finish - 1, -1, -1):
        instruction = program[time]
        operation, role = instruction[:2]
        if operation == 'MOVE' and role not in mains:
            deadlines[time] = next_touch.get(role, finish)
        touched = {role}
        if operation in ('ADD', 'COPY'):
            touched.add(instruction[2])
        for field in touched:
            next_touch[field] = time
    visits = {q: [] for q in mains}
    current = {q: (-1, charts[word['initial'][q]]) for q in mains}
    for time, instruction in enumerate(program):
        if instruction[0] == 'MOVE' and instruction[1] in mains:
            q = instruction[1]
            start, chart = current[q]
            require(chart == charts[instruction[2]], 'main itinerary source chart')
            visits[q].append((start, time, chart))
            current[q] = time, charts[instruction[3]]
    for q, (start, chart) in current.items():
        visits[q].append((start, finish, chart))
        require(len({c for _, _, c in visits[q]}) == len(visits[q]), 'monotone distinct main visits')
    windows = []
    for time, deadline in deadlines.items():
        instruction = program[time]
        source, target = charts[instruction[2]], charts[instruction[3]]
        for q in sorted(mains):
            starts = [a for a, b, c in visits[q] if c == source and a < time < b]
            arrivals = [a for a, b, c in visits[q] if c == target and time < a < deadline]
            if starts and arrivals:
                require(len(starts) == len(arrivals) == 1, 'unique quiet donor visits')
                windows.append((time, instruction[1], q, instruction[2], instruction[3], arrivals[0], deadline))
    return sorted(windows), visits

def run(args):
    root = args.repository
    base = root / 'research/moonshot-005-program/results'
    source_path = root / 'research/shared-wire-split-composition/data/final.json.gz'
    prefix_path = base / 'paid-observable-acquisition/LIFTED-PREFIX.json'
    budget_path = base / 'relay-acquisition-budget/RESULT.json'
    old_path = base / 'endpoint-obstruction/CERTIFICATE.json'
    for path, pin in [(source_path, NATIVE), (prefix_path, PREFIX), (budget_path, BUDGET), (old_path, OLD)]:
        require(sha(path) == pin, 'pinned source: ' + str(path))
    reviewed = json.loads((args.review / 'REVIEWED-FILES.json').read_text())
    for filename, pin in reviewed.items():
        require(sha(args.packet / filename) == pin, 'frozen reviewed file: ' + filename)
    word = json.loads(gzip.decompress(source_path.read_bytes()))
    prefix = json.loads(prefix_path.read_text())
    price = json.loads(budget_path.read_text())
    old = json.loads(old_path.read_text())
    certificate = json.loads((args.packet / 'CERTIFICATE.json').read_text())
    proposed_result = json.loads((args.packet / 'RESULT.json').read_text())
    charts = [space(x) for x in word['frames']]
    require(len(set(charts)) == 1094, '1094 actual chart spaces')
    main = set(word['live']) | {q + 112 for q in word['live']} | set(word['hosted']['X2']) | set(word['hosted']['Y2'])
    pairs = old['witness_pairs']
    selected = {x['input'] for x in pairs}
    require(len(main) == 400 and len(selected) == len(pairs) == 46, 'source and selected input cardinality')
    windows, histories = quiet_and_history(word, main, charts)
    require(len(windows) == 354 and len({x[0] for x in windows}) == 141, 'independent full quiet-window census')
    moves = [x for x in word['program'] if x[0] == 'MOVE']
    arrows = {(charts[x[2]], charts[x[3]]) for x in moves if x[1] in main or x[4]}
    arrows.update((charts[x[3]], charts[x[4]]) for x in windows)
    require(len(arrows) == 853, 'independent static allowed arc census')
    cut = {charts[i] for i in certificate['canonical_cut_representatives']}
    require(len(cut) == 220, '220 distinct chart spaces in displayed cut')
    require(all(a not in cut or b in cut for a, b in arrows), 'displayed cut is closed')
    all_selected_history = {chart for q in selected for _, _, chart in histories[q]}
    require(all_selected_history <= cut, 'every selected raw main history lies inside')
    sinks = [charts[word['final'][x['output']]] for x in pairs]
    require(len(set(sinks)) == 46 and not set(sinks) & cut, '46 distinct outside sink charts')
    # Independent direction: explore backwards from each sink, never from K.
    excluded_pairs = 0
    for sink in sinks:
        backward = ancestors([sink], arrows)
        for q in selected:
            require(not backward & {c for _, _, c in histories[q]}, 'every raw history excluded from this sink')
            excluded_pairs += 1
    require(excluded_pairs == 2116, 'all46 squared history exclusions')
    endpoint_rows = []
    determinant = F(1)
    for pair in pairs:
        q, y = pair['input'], pair['output']
        row = native_row(word['program'], y, selected)
        require(row == {q: F(pair['coefficient'])}, 'fresh source endpoint adjoint')
        require(word['final'][y] == pair['target_chart'], 'actual endpoint chart')
        endpoint_rows.append(row)
        determinant *= row[q]
    require(determinant == F(1, 8), 'endpoint diagonal determinant')
    positions, values = prefix_state(prefix, charts, selected)
    outside = {q: row for q, row in values.items() if charts[positions[q]] not in cut and row}
    require(set(outside) == {1931, 1932}, 'actual replay has precisely two informative outside fields')
    r, s = outside[1931], outside[1932]
    minor = r[17] * s[20] - r[20] * s[17]
    require(minor == F(-1, 8) and row_rank([r, s]) == 2, 'actual outside rank and nonsingular minor')
    require(row_rank(endpoint_rows + [r, s]) - row_rank([r, s]) == 44, 'independent exact quotient rank44')
    require(certificate['aggregate_restriction_rows'] == [{str(q): str(c) for q, c in sorted(row.items())} for row in [r, s]], 'authored aggregate metadata agrees with literal replay')
    escapes = []
    for time, instruction in enumerate(word['program']):
        if instruction[0] == 'MOVE' and charts[instruction[2]] in cut and charts[instruction[3]] not in cut:
            require(instruction[1] not in main and not instruction[4], 'all escaping source moves are public helpers')
            escapes.append({'event': time, 'helper': instruction[1], 'source': instruction[2], 'target': instruction[3], 'rank': len(word['frames'][instruction[3]]) - len(word['frames'][instruction[2]])})
    require(escapes == certificate['escape_occurrences'] and len(escapes) == 399, 'complete source escape inventory')
    upper = F(price['variants']['eight_facet_copies']['remaining_paid_moment_per_native_interval'][1])
    require(F(8) < upper < F(9), 'at most8 extra positive integer-rank full calls')
    # Concrete controls expose exactly the relaxation boundaries.
    all_arrows = {(charts[x[2]], charts[x[3]]) for x in moves}
    full_reachable_pairs = 0
    for sink in sinks:
        backward = ancestors([sink], all_arrows)
        full_reachable_pairs += sum(bool(backward & {c for _, _, c in histories[q]}) for q in selected)
    require(full_reachable_pairs > 0, 'all-helper control destroys exclusion')
    require(all(any(charts[word['initial'][q]] in ancestors([sink], all_arrows) for q in selected) for sink in sinks), 'all46 sinks become reachable under all-helper grant')
    chosen = escapes[0]
    require(charts[chosen['source']] in cut and charts[chosen['target']] not in cut, 'one concrete nonquiet helper exits the cut')
    require(row_rank([r, s] * 100) == 2, 'duplicated aggregates never create modes')
    # Columns17,20 pivot; all other44 coordinate modes complement the two forms.
    complement = [{q: F(1)} for q in selected if q not in (17, 20)]
    require(len(complement) == 44 and row_rank([r, s] + complement) == 46, '44 independent modes remove exactly the rank deficit')
    require(row_rank([{q: F(1)} for q in selected]) == 46, 'global raw reread removes rank restriction')
    require(proposed_result['remaining_message_lower_bound'] == 44 and proposed_result['additional_original_helper_crossing_field_units_needed_if_at_most8_new_paid'] == 36, 'author quantitative conclusions match independent reconstruction')
    return {
        'status': 'PASS_INDEPENDENT_STATIC_HISTORY_CUT_REVIEW',
        'native_sha256': NATIVE,
        'reviewed_files_manifest_sha256': sha(args.review / 'REVIEWED-FILES.json'),
        'independence': 'No imports or execution of author/predecessor verifiers; exhaustive chart-space sets, reverse graph reachability, reverse touch deadlines, literal prefix replay, fresh source adjoints.',
        'quiet_windows': len(windows),
        'quiet_starts': len({x[0] for x in windows}),
        'distinct_allowed_arcs': len(arrows),
        'closed_cut_charts': len(cut),
        'history_to_sink_excluded_pairs': excluded_pairs,
        'selected_endpoint_determinant': str(determinant),
        'actual_outside_field_ids': sorted(outside),
        'actual_outside_rank': 2,
        'actual_outside_minor_columns': [17, 20],
        'actual_outside_minor': str(minor),
        'required_outside_pool_information_field_units': 44,
        'required_already_paid_nonquiet_helper_units_if8_new_paid': 36,
        'candidate_original_helper_crossings': len(escapes),
        'candidate_crossing_rank_histogram': dict(sorted(collections.Counter(x['rank'] for x in escapes).items())),
        'controls': {
            'allow_all_original_helper_arcs_reachable_input_sink_pairs': full_reachable_pairs,
            'all_helper_grant_reaches_each_of46_sinks': True,
            'one_concrete_forbidden_crossing': chosen,
            '200_aggregate_copies_rank': 2,
            '44_global_coordinate_complements_plus_rs_rank': 46,
            'global_raw_reread_rank': 46,
        },
        'scope': 'Accept source-specific all-volume linear cut theorem and current-profile36-paid-helper escape requirement. It does not forbid informative nonquiet helper recoding, prove a complete native, or establish a new kappa.'
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--review', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'])
