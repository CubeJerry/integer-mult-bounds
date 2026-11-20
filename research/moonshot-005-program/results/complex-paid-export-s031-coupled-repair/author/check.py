#!/usr/bin/env python3
"""Verify the coupled rank-six cut and the complete two-message repair budget."""
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import cache
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
package = Path(__file__).resolve().parent.parent
pins = json.loads((package / 'SOURCE-PINS.json').read_text())
for name, digest in pins['files'].items():
    require(hashlib.sha256((args.repo / name).read_bytes()).hexdigest() == digest,
            'source pin: ' + name)
base = args.repo / 'research/moonshot-005-program/results'
inputs = base / 'complex-native-funded-donor-cuts/inputs'
spec = importlib.util.spec_from_file_location('s031_literal', inputs / '7833-construction.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)
original = source.load_word(inputs / 'DOUBLE-CANDIDATE.json.gz')
four = source.compensated(original)
five = source.compensated(original, True)
vectors = source.all_public_rows(original)
control = source.all_public_rows(five)
require(all(vectors[e] == control[e] for e in original.terminals),
        'genuine paid fifth channel preserves every target coefficient')
full_rank = source.IntegerElimination({j: j for j in range(len(original.inputs))})
for e in sorted(original.terminals):
    full_rank.add(vectors[e][1])
require(len(full_rank.rows) == 1289, 'complete original target is invertible')


def span(frame):
    values = {0}
    for vector in frame:
        values |= {x ^ vector for x in values}
    require(len(values) == 1 << len(frame), 'independent chart basis')
    return tuple(sorted(values))


spaces, canonical, aliases = {}, {}, defaultdict(list)
for chart, frame in enumerate(original.frames):
    c = spaces.setdefault(span(frame), len(spaces))
    canonical[chart] = c
    aliases[c].append(chart)
size = len(spaces)
require(size == 1102, 'canonical chart count')
routes = {e: tuple(canonical[c] for c in route) for e, route in five.routes.items()}
old_routes = {e: tuple(canonical[c] for c in route) for e, route in four.routes.items()}


def adjacency(route_map, removed=()):
    graph = [set() for _ in range(size)]
    for e, (u, v) in route_map.items():
        if e not in removed:
            graph[u].add(v)
    return graph


def closure(graph, roots):
    found = set(roots)
    todo = list(found)
    while todo:
        for v in graph[todo.pop()] - found:
            found.add(v)
            todo.append(v)
    return found


def verify_cut(certificate):
    axes = certificate['source_axes']
    terminals = certificate['terminal_slots']
    blocked = set(certificate['blocked_occurrences'])
    rank = certificate['rank']
    diagonal = [Q(x) for x in certificate['minor_diagonal']]
    require(len(diagonal) == rank and all(diagonal), 'nonzero diagonal pivots')
    require(len(set(axes)) == len(axes) == len(set(terminals)) == len(terminals) == rank,
            'square independent minor declaration')
    require(blocked <= set(four.routes), 'only retained old routes are blocked')
    roots = {canonical[original.inputs[~j]] for j in axes}
    inside = closure(adjacency(routes, blocked), roots)
    require(canonical[3] not in inside, 'any number of new observer exports cannot leave cut')
    exports = {e for e, (u, v) in routes.items() if u in inside and v not in inside}
    require(exports == blocked and len(exports) == rank, 'literal saturated outgoing boundary')
    require(all(canonical[original.terminals[e]] not in inside for e in terminals),
            'all demanded output fields lie outside cut')
    matrix = []
    for row, terminal in enumerate(terminals):
        denominator, numerators = vectors[terminal]
        values = [Q(numerators.get(j, 0), denominator) for j in axes]
        require(values == [diagonal[row] if column == row else Q(0) for column in range(rank)],
                'exact nonzero diagonal minor in original target')
        matrix.append([str(x) for x in values])
    return {'id': certificate['id'], 'rank': rank,
            'source_axes': axes, 'source_charts': [original.inputs[~j] for j in axes],
            'terminal_slots': terminals,
            'terminal_charts': [original.terminals[e] for e in terminals],
            'outgoing_occurrences': sorted(exports),
            'canonical_cut_size': len(inside),
            'raw_charts': sorted(c for c, v in canonical.items() if v in inside),
            'minor': matrix, 'minor_diagonal': [str(x) for x in diagonal],
            'observer_source_outside': True}


cut_data = json.loads((package / 'CUT.json').read_text())
cut = verify_cut(cut_data)
deleted = {86, 89777, 97232, 97241, 97320, 97323, 99064}
require(cut['canonical_cut_size'] == 422, 'exact coupled cut size')
exports = set(cut['outgoing_occurrences'])
require(exports == {43, 89777, 96408, 96513, 97320, 98077}, 'six old exports')
require(exports & deleted == {89777, 97320}, 'two specified old deletions cross cut')
remaining = sorted(exports - deleted)
require(remaining == [43, 96408, 96513, 98077], 'four surviving old exports')

rail = base / 'complex-native-contested-restoration/rail'
sys.path.insert(0, str(rail))
import price
from graph import Graph
caller = Graph()
old_profile = Counter(four.grade(route) for route in original.routes.values())
four_profile = Counter(four.grade(route) for route in four.routes.values())
deleted_profile = Counter(four.grade(four.routes[e]) for e in deleted)
require(deleted_profile == {3: 1, 4: 5, 5: 1}, 'seven-deletion grade profile')
net_profile = price.add_profiles((1, old_profile), (-1, four_profile),
                                 (1, deleted_profile), (-1, {3: 1}))
require(net_profile == {3: 1, 4: 5, 5: 2, 7: -1}, 'complete saving before new repairs')
exponent = Q(199, 200)
saving = price.moment(net_profile, exponent)
required = price.moment(price.add_profiles((1, caller.native), (-1, caller.helpers),
                (-Q(1, caller.calls), caller.fixed_root),
                (Q(1, caller.calls), caller.fixed_paid)), exponent)
allowance = saving[0] - required[1], saving[1] - required[0]
grade_three = price.moment({3: 1}, exponent)
grade_two_plus_one = price.moment({2: 1, 1: 1}, exponent)
require(2 < allowance[0] <= allowance[1] < grade_three[0] < 3,
        'two unit-grade jobs fit; a grade-three job and three jobs cannot fit')
require(allowance[1] < grade_two_plus_one[0], 'two jobs including grade two cannot fit')
after_two = allowance[0] - 2, allowance[1] - 2
controls = []
for name, mutation in [('missing_boundary', {'blocked_occurrences': [43, 96408, 96513, 97320, 98077]}),
                       ('wrong_terminal', {'terminal_slots': [min(original.terminals)] + cut_data['terminal_slots'][1:]})]:
    forged = copy.deepcopy(cut_data)
    forged.update(mutation)
    try:
        verify_cut(forged)
    except ValueError as error:
        controls.append({'mutation': name, 'rejected': str(error)})
    else:
        raise ValueError('negative control accepted: ' + name)
receipt = {
    'status': 'PASS_S031_COUPLED_REPAIR_REQUIRES_TWO_GRADE_ONE_MESSAGES',
    'scope': 'Exactly the seven declared old deletions after the genuine paid fifth-channel compensation; original input/output roles and exact target; arbitrary retained local linear recoding, histories and retiming; new paid messages may have arbitrary endpoints.',
    'complete_kappa_claimed': False, 'source_files': pins['files'],
    'deleted_occurrences': sorted(deleted), 'cut': cut,
    'deleted_boundary_occurrences': sorted(exports & deleted),
    'surviving_old_exports': remaining,
    'minimum_additional_message_count': 2,
    'kappa_screen': '0.005',
    'complete_native_saving_before_extra_repairs': price.pretty(saving),
    'complete_caller_required_saving': price.pretty(required),
    'additional_repair_allowance': price.pretty(allowance),
    'exact_allowance_bounds': [str(x) for x in allowance],
    'grade_three_cost': price.pretty(grade_three),
    'grade_two_plus_one_cost': price.pretty(grade_two_plus_one),
    'margin_after_two_grade_one_messages': price.pretty(after_two),
    'necessary_affordable_extra_route_profile': {'1': 2},
    'controls': controls,
    'review_status': 'author replay; independent admission is separate',
    'python': sys.version}
args.out.mkdir(parents=True, exist_ok=True)
(args.out / 'RESULT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(receipt['status'], 'rank', 6, 'old capacity', 4, flush=True)
print('Additional budget', receipt['additional_repair_allowance'], flush=True)
print('After two grade-one jobs', receipt['margin_after_two_grade_one_messages'], flush=True)
