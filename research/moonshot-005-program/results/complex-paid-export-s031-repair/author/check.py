#!/usr/bin/env python3
"""Verify saturated multi-source cuts without a solver or optimization library."""
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


cut_data = json.loads((package / 'CUTS.json').read_text())['cuts']
cuts = [verify_cut(c) for c in cut_data]
mandatory_by_rank = set().union(*(set(c['outgoing_occurrences']) for c in cuts))
require([c['rank'] for c in cuts] == [2, 5, 6, 8], 'four exact cut ranks')

# Reconstruct the inherited circulation roster rather than assuming that every
# high-grade route not listed in CUTS.json is freely deletable.
graph = adjacency(old_routes)
reverse = [set() for _ in range(size)]
for u, neighbours in enumerate(graph):
    for v in neighbours:
        reverse[v].add(u)


@cache
def reachable(vertex):
    return closure(graph, [vertex])


def balance(word):
    values = Counter(canonical[c] for c in word.inputs.values())
    values.subtract(Counter(canonical[c] for c in word.terminals.values()))
    for u, v in word.routes.values():
        values[canonical[u]] -= 1
        values[canonical[v]] += 1
    return {v: count for v, count in values.items() if count}


require(not balance(original), 'original canonical chart balance')
require(balance(four) == {canonical[278]: 1, canonical[282]: -1},
        'four-channel route imbalance')
require(not reverse[canonical[3]], 'no old route returns to chart 3')
require(canonical[278] not in reachable(canonical[282]), 'no observer path to 278')
shadow, = set(five.routes) - set(original.routes)
require(five.routes[shadow] == (3, 282), 'exact fully paid observer route')
for destination in [278, 282]:
    region = reachable(canonical[3]) & closure(reverse, [canonical[destination]])
    require(all(four.grade(four.routes[e]) <= 2 for e, (u, v) in old_routes.items()
                if u in region and v in region), 'unused path region has no high-grade old route')
wide = {e for e, route in four.routes.items() if four.grade(route) >= 3}
wide_cycles = {e for e in wide if old_routes[e][0] in reachable(old_routes[e][1])}
require(len(wide) == 1076, 'retained high-grade count')
require(wide_cycles == {43, 86, 89777, 96404, 96513, 97232, 97241,
                        97320, 97323, 99064, 100120}, 'inherited eleven-cycle roster')
new_mandatory = mandatory_by_rank & wide_cycles
require(new_mandatory == {43, 89777, 96404, 96513, 97320, 100120},
        'six newly mandatory high-grade cycle occurrences')
possible = wide_cycles - new_mandatory
require(possible == {86, 97232, 97241, 97323, 99064}, 'only five high-grade deletions remain possible')
deleted_profile = Counter(four.grade(four.routes[e]) for e in possible)
require(deleted_profile == {3: 1, 4: 4}, 'optimistic remaining high-grade deletion profile')

# Outward exact dyadic arithmetic in the inherited complete 48-call tariff.
rail = base / 'complex-native-contested-restoration/rail'
sys.path.insert(0, str(rail))
import price
from graph import Graph
caller = Graph()
old_profile = Counter(four.grade(route) for route in original.routes.values())
four_profile = Counter(four.grade(route) for route in four.routes.values())
require(price.add_profiles((1, old_profile), (-1, four_profile)) == {3: 1, 5: 1, 7: -1},
        'actual four-channel route changes are charged')
net_profile = price.add_profiles((1, old_profile), (-1, four_profile),
                                 (1, deleted_profile), (-1, {3: 1}))
require(net_profile == {3: 1, 4: 4, 5: 1, 7: -1}, 'one paid observer and all optimistic savings')
pricing = {}
for kappa in [Q(43, 10000), Q(1, 200)]:
    exponent = 1 - kappa
    saving = price.moment(net_profile, exponent)
    required = price.moment(price.add_profiles((1, caller.native), (-1, caller.helpers),
                (-Q(1, caller.calls), caller.fixed_root),
                (Q(1, caller.calls), caller.fixed_paid)), exponent)
    margin = saving[0] - required[1], saving[1] - required[0]
    if kappa == Q(1, 200):
        require(margin[1] < 0, 'even optimistic high-grade-only repairs fail .005')
    else:
        require(margin[0] > 0, 'the .0043 numerical screen remains open')
    pricing[str(kappa)] = {
        'maximum_optimistic_net_saving': price.pretty(saving),
        'complete_caller_required_saving': price.pretty(required),
        'remaining_margin': price.pretty(margin),
        'exact_margin_bounds': [str(x) for x in margin],
        'extra_parallel_observer_cost_each': price.pretty(price.moment({3: 1}, exponent))}

# Controls check the proof's actual failure modes, not just the receipt format.
controls = []
for c in cuts:
    rank = c['rank']
    inside = {canonical[chart] for chart in c['raw_charts']}
    for deleted in c['outgoing_occurrences']:
        remaining = sum(e != deleted and u in inside and v not in inside
                        for e, (u, v) in routes.items())
        require(remaining == rank - 1 < rank,
                'literal single-export deletion loses a complete field of capacity')
controls.append('Deleting any one listed export lowers capacity below the verified nonsingular-minor rank.')
bad = copy.deepcopy(cut_data[0])
bad['terminal_slots'][0] = min(original.terminals)
try:
    verify_cut(bad)
except ValueError:
    controls.append('Wrong public terminal is rejected by the exact cut/minor checker.')
else:
    raise ValueError('wrong-terminal mutation unexpectedly passed')
bad = copy.deepcopy(cut_data[0])
bad['blocked_occurrences'].pop()
try:
    verify_cut(bad)
except ValueError:
    controls.append('Omitting a boundary occurrence is rejected; reachability is recomputed.')
else:
    raise ValueError('omitted-boundary mutation unexpectedly passed')
controls.append('The literal fifth-channel source reproduces all original target rows as the positive control.')

receipt = {
    'status': 'PASS_S031_SATURATED_COMPLEX_CUTS_AND_HIGH_GRADE_SCREEN',
    'complete_kappa_claimed': False,
    'source_columns': len(original.inputs), 'canonical_charts': size,
    'cuts': cuts, 'mandatory_by_new_rank_cuts': sorted(mandatory_by_rank),
    'newly_mandatory_high_grade_cycle_occurrences': sorted(new_mandatory),
    'retained_high_grade_occurrences': len(wide),
    'mandatory_high_grade_occurrences': len(wide) - len(possible),
    'remaining_possible_high_grade_deletions': sorted(possible),
    'optimistic_deleted_profile': dict(sorted(deleted_profile.items())),
    'optimistic_net_saving_profile_with_one_paid_observer': net_profile,
    'prices': pricing, 'controls': controls,
    'scope': 'Original 1289 input/output roles and target; retained four-channel endpoints may be deleted; '
             'any positive number of fully paid parallel 3->282 exports; arbitrary retained local linear '
             'recoding, histories and retiming. Rank-cut necessity permits arbitrary additional deletions. '
             'The .005 tariff exclusion permits only old high-grade deletions and charges at least one new observer. '
             'Low-grade deletions, new nonparallel routes, retargeted endpoints and changed targets need separate analysis.'}
args.out.mkdir(parents=True, exist_ok=True)
(args.out / 'RESULT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(receipt['status'], len(cuts), len(new_mandatory), len(possible), flush=True)
for kappa, row in pricing.items():
    print(kappa, 'margin', row['remaining_margin'], flush=True)
