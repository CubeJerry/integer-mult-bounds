#!/usr/bin/env python3
"""Independent SCC closure, exact cut enumeration and integer-power price."""
from argparse import ArgumentParser
from collections import Counter, deque
from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import io
import json
import runpy
import sys


def need(ok, why):
    if not ok:
        raise ValueError(why)


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
pkg = Path(__file__).resolve().parents[1]
for path, digest in json.loads((pkg/'root-review/SOURCE-PINS.json').read_text())['files'].items():
    need(sha256((args.repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
old = args.repo/'research/moonshot-005-program/results/complex-paid-export-s031-repair/root-review/check.py'
saved = sys.argv
sys.argv = [str(old), '--repo', str(args.repo), '--out', str(args.out/'predecessor')]
with redirect_stdout(io.StringIO()):
    ctx = runpy.run_path(str(old), run_name='__main__')
sys.argv = saved
need(ctx['result']['status'] == 'PASS_ROOT_COMPLEX_SATURATED_CUT_REVIEW', 'independent predecessor source review')
w, spans = ctx['w'], ctx['spaces']
names = {space: i for i, space in enumerate(sorted(set(spans)))}
canon = [names[space] for space in spans]
N = len(names)
need(N == 1102, 'complete physical banks')
representatives = {v: min(c for c, x in enumerate(canon) if x == v) for v in range(N)}
routes = {e: (canon[u], canon[v]) for e, (u, v) in ctx['with_observer'].items()}
deleted = {86, 89777, 97232, 97241, 97320, 97323, 99064}
target_bank = lambda e: canon[w['final'][e-w['first_output']]]
source_bank = lambda j: canon[w['initial'][j]]


def transitive(blocked):
    graph = [set() for _ in range(N)]
    reverse = [set() for _ in range(N)]
    for e, (u, v) in routes.items():
        if e not in blocked:
            graph[u].add(v)
            reverse[v].add(u)
    visited, order = set(), []
    for root in range(N):
        if root in visited:
            continue
        todo = [(root, False)]
        while todo:
            u, finished = todo.pop()
            if finished:
                order.append(u)
            elif u not in visited:
                visited.add(u)
                todo.append((u, True))
                todo.extend((v, False) for v in graph[u] if v not in visited)
    comp, members = {}, []
    for root in reversed(order):
        if root in comp:
            continue
        i = len(members)
        bankset, todo = set(), [root]
        comp[root] = i
        while todo:
            u = todo.pop()
            bankset.add(u)
            for v in reverse[u]:
                if v not in comp:
                    comp[v] = i
                    todo.append(v)
        members.append(bankset)
    dag = [set() for _ in members]
    for u in range(N):
        dag[comp[u]].update(comp[v] for v in graph[u] if comp[v] != comp[u])
    indegree = [0]*len(dag)
    for targets in dag:
        for v in targets:
            indegree[v] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    topo = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v in dag[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    need(len(topo) == len(dag), 'acyclic component condensation')
    reach = [sum(1 << v for v in group) for group in members]
    for u in reversed(topo):
        for v in dag[u]:
            reach[u] |= reach[v]
    return [reach[comp[u]] for u in range(N)]


def closure(reach, axes):
    inside = 0
    for j in axes:
        inside |= reach[source_bank(j)]
    return inside


def outgoing(inside, omitted=()):
    return {e for e, (u, v) in routes.items() if e not in omitted and inside >> u & 1 and not (inside >> v & 1)}


def verify_minor(cert):
    axes, ends = cert['source_axes'], cert['terminal_slots']
    need(len(set(axes)) == len(set(ends)) == cert['rank'], 'distinct square minor')
    diagonal = [F(x) for x in cert['minor_diagonal']]
    need(len(diagonal) == len(axes) and all(diagonal), 'nonzero diagonal')
    for i, e in enumerate(ends):
        row = ctx['reverse_row'](e)
        need([row.get(j, 0) for j in axes] == [diagonal[i] if k == i else 0 for k in range(len(axes))], 'literal exact target minor')
    blocked = set(cert['blocked_occurrences'])
    inside = closure(transitive(blocked), axes)
    need(outgoing(inside) == blocked, 'complete original saturated boundary')
    need(all(not (inside >> target_bank(e) & 1) for e in ends), 'all minor targets outside')
    return inside


core = json.loads((pkg/'CUT.json').read_text())
inside = verify_minor(core)
need(inside.bit_count() == 422, 'core cut size')
need(outgoing(inside, deleted) == {43, 96408, 96513, 98077}, 'rank-six demand with four old exports')
need(not (inside >> canon[3] & 1), 'paid observer source outside')
t = F(199, 200)
grade = ctx['grade']
deleted_profile = Counter(grade(ctx['with_observer'][e]) for e in deleted)
need(deleted_profile == {3: 1, 4: 5, 5: 1}, 'actual deletion grades')
net_profile = Counter(grade(route) for route in ctx['original'].values())
net_profile.subtract(grade(route) for route in ctx['with_observer'].values())
net_profile.update(deleted_profile)
net_profile = {j: x for j, x in net_profile.items() if x}
need(net_profile == {3: 1, 4: 5, 5: 2, 7: -1}, 'actual complete saving profile')
saving = ctx['moment'](net_profile, t)
required = ctx['moment'](ctx['required'], t)
allowance = saving[0]-required[1], saving[1]-required[0]
cost_two_plus_one = ctx['moment']({1: 1, 2: 1}, t)
need(2 < allowance[0] <= allowance[1] < 3, 'exactly two messages affordable')
need(allowance[1] < cost_two_plus_one[0], 'any grade-two upgrade is unaffordable')

cuts = json.loads((pkg/'endpoint-screen/BASE-CUTS.json').read_text())['cuts']
cut_by_id = {cut['id']: cut for cut in cuts}
reaches, initial, boundary = [], [], []
for cut in cuts:
    verify_minor(cut)
    reach = transitive(set(cut['blocked_occurrences']) | deleted)
    A = closure(reach, cut['source_axes'])
    need(all(not (A >> target_bank(e) & 1) for e in cut['terminal_slots']), 'initial selected outputs outside')
    reaches.append(reach)
    initial.append(A)
    boundary.append(set(cut['blocked_occurrences'])-deleted)
need(initial[2] == inside, 'screen and core cuts coincide')
need([len(outgoing(A, deleted)) for A in initial] == [1, 4, 4, 7], 'initial cut capacities')
bits = [sum(1 << x for x in spans[representatives[v]]) for v in range(N)]
dim = [len(w['frames'][representatives[v]]) for v in range(N)]
grade_one = []
for u in range(N):
    for v in range(N):
        if abs(dim[u]-dim[v]) == 1 and bits[u] & bits[v] in (bits[u], bits[v]):
            mask = sum(int(A >> u & 1 and not (A >> v & 1)) << k for k, A in enumerate(initial))
            grade_one.append((u, v, mask))
need(len(grade_one) == 4802, 'exhaustive nested grade-one routes')
eligible = [e for e in grade_one if e[2] & 4]
need(len(eligible) == 424, 'both added edges must cross six-demand cut')
pairs = [(e[:2], f[:2]) for e, f in combinations_with_replacement(eligible, 2) if e[2] | f[2] == 15]
need(len(pairs) == 27002, 'complete unordered fixed-cut candidates, including repetitions')
survivors, rejections = set(), Counter()
for pair in pairs:
    for k, cut in enumerate(cuts):
        A = initial[k]
        while True:
            before = A
            for u, v in pair:
                if A >> u & 1:
                    A |= reaches[k][v]
            if A == before:
                break
        exports = sum(A >> routes[e][0] & 1 and not (A >> routes[e][1] & 1) for e in boundary[k])
        demand = sum(not (A >> target_bank(e) & 1) for e in cut['terminal_slots'])
        if exports < demand:
            rejections[cut['id']] += 1
            break
    else:
        survivors.add(tuple(sorted((representatives[u], representatives[v]) for u, v in pair)))
need(len(survivors) == 180, 'independent SCC reclosure census')
print('Independent SCC and fixed-cut enumeration leaves180 pairs.', flush=True)

def verify_rejection(cert):
    pair = tuple(sorted(tuple(e) for e in cert['routes']))
    need(pair in survivors, 'rejected pair was a reclosure survivor')
    cut = cut_by_id[cert['minor_id']]
    A = {canon[c] for c in cert['raw_charts']}
    need(set(cert['raw_charts']) == {c for c, v in enumerate(canon) if v in A}, 'full physical-bank alias set')
    need({source_bank(j) for j in cut['source_axes']} <= A, 'all selected sources inside')
    need(not ({target_bank(e) for e in cut['terminal_slots']} & A), 'all selected target roles outside')
    exports = {e for e, (u, v) in routes.items() if e not in deleted and u in A and v not in A}
    added = [e for e in pair if canon[e[0]] in A and canon[e[1]] not in A]
    need(exports == set(cert['old_exports']), 'complete retained boundary')
    need(sorted(added) == sorted(tuple(e) for e in cert['new_exports']), 'complete added boundary, with multiplicity')
    need(len(exports)+len(added) == cert['capacity'] < cert['rank'] == cut['rank'], 'strict exact target-rank obstruction')
    return pair

certs = json.loads((pkg/'endpoint-screen/output/CUT-REJECTIONS.json').read_text())
rejected = {verify_rejection(cert) for cert in certs}
need(len(certs) == len(rejected) == 60, 'sixty distinct directly verified cut rejections')
remaining = sorted(survivors-rejected)
expected = json.loads((pkg/'endpoint-screen/EXPECTED-SURVIVORS.json').read_text())['pairs']
need([[list(edge) for edge in pair] for pair in remaining] == expected and len(remaining) == 120, 'complete surviving list')
bad = {**certs[0], 'capacity': certs[0]['capacity']+1}
try:
    verify_rejection(bad)
except ValueError:
    pass
else:
    raise ValueError('forged cut capacity passed')
result = {'status': 'PASS_ROOT_COUPLED_REPAIR_CUT_PRICE_AND_ENDPOINT_SCREEN',
          'core_rank': 6, 'remaining_old_exports': 4, 'core_cut_banks': 422,
          'price_engine': '96-bit rational endpoints certified by exact integer powers',
          'exact_allowance': [str(x) for x in allowance], 'allowance_approx': [float(x) for x in allowance],
          'exact_margin_after_two_grade_one': [str(x-2) for x in allowance],
          'all_directed_grade_one_routes': 4802, 'core_cut_crossing_routes': 424,
          'fixed_cut_pairs': 27002, 'SCC_reclosure_survivors': 180,
          'verified_further_cut_rejections': 60, 'remaining_pairs': 120,
          'reclosure_rejections': dict(rejections), 'forged_capacity_rejected': True,
          'new_author_code_imported': False,
          'scope': 'Fixed seven-deletion plan, original roles, arbitrary surviving local linear recoding and retiming; no surviving pair is a construction.',
          'new_complete_kappa': False}
args.out.mkdir(parents=True, exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
print(result['status'], 6, 4, 120, flush=True)
