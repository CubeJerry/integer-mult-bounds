#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exhaust all affordable endpoint pairs; reject only with exact minor cuts."""
import argparse
import json
import runpy
import sys
from collections import Counter, deque
from itertools import combinations_with_replacement
from pathlib import Path


def require(value, reason):
    if not value:
        raise ValueError(reason)


parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
package = Path(__file__).resolve().parent
core = package.parent / 'author/check.py'
old_argv = sys.argv
sys.argv = [str(core), '--repo', str(args.repo), '--out', str(args.out / 'core')]
try:
    context = runpy.run_path(str(core), run_name='__main__')
finally:
    sys.argv = old_argv
word = context['five']
canon, routes, N = context['canonical'], context['routes'], len(context['spaces'])
deleted = context['deleted']
cuts = [context['verify_cut'](cut) for cut in json.loads((package / 'BASE-CUTS.json').read_text())['cuts']]
require(len(cuts) == 4, 'four exact predecessor minors and boundaries')
representative = {v: min(c for c, value in canon.items() if value == v) for v in range(N)}
bits = {v: sum(1 << x for x in context['span'](word.frames[representative[v]])) for v in range(N)}
dim = {v: len(word.frames[representative[v]]) for v in range(N)}
reaches, initial, boundaries = [], [], []
for cut in cuts:
    blocked = set(cut['outgoing_occurrences']) | deleted
    reach = [1 << u for u in range(N)]
    for e, (u, v) in routes.items():
        if e not in blocked:
            reach[u] |= 1 << v
    for k in range(N):
        bit, row = 1 << k, reach[k]
        for u in range(N):
            if reach[u] & bit:
                reach[u] |= row
    A = 0
    for j in cut['source_axes']:
        A |= reach[canon[word.inputs[~j]]]
    require(all(not (A >> canon[word.terminals[e]] & 1) for e in cut['terminal_slots']),
            'all initial diagonal-minor outputs remain outside')
    outgoing = {e for e, (u, v) in routes.items() if e not in deleted and A >> u & 1 and not (A >> v & 1)}
    require(outgoing <= blocked, 'all unblocked old edges are internal to the closure')
    reaches.append(reach)
    initial.append(A)
    boundaries.append(set(cut['outgoing_occurrences']) - deleted)
capacities = [sum(e not in deleted and A >> u & 1 and not (A >> v & 1)
                  for e, (u, v) in routes.items()) for A in initial]
require(capacities == [1, 4, 4, 7], 'four initial capacities against ranks 2,5,6,8')
require({canon[c] for c in context['cut']['raw_charts']} == {v for v in range(N) if initial[2] >> v & 1},
        'the two-deficit cut equals the independently reconstructed core cut')

# All physically distinct directed grade-one endpoints, including parallel
# copies of existing routes. New banks are excluded by the core proof.
grade_one = []
for u in range(N):
    for v in range(N):
        if abs(dim[u] - dim[v]) == 1 and bits[u] & bits[v] in (bits[u], bits[v]):
            mask = sum(bool(A >> u & 1 and not (A >> v & 1)) << k for k, A in enumerate(initial))
            grade_one.append((u, v, mask))
require(len(grade_one) == 4802, 'complete grade-one route census')
eligible = [edge for edge in grade_one if edge[2] & 4]
require(len(eligible) == 424, 'both messages must cross the rank-six cut')
pairs = [(e[:2], f[:2]) for e, f in combinations_with_replacement(eligible, 2) if e[2] | f[2] == 15]
require(len(pairs) == 27002, 'complete fixed-cut candidate census')
closure_rejects, closure_survivors = Counter(), []
for pair in pairs:
    rejected = None
    for k, cut in enumerate(cuts):
        A = initial[k]
        for _ in range(3):
            before = A
            for u, v in pair:
                if A >> u & 1:
                    A |= reaches[k][v]
            if A == before:
                break
        else:
            raise ValueError('two-edge closure failed to stabilize')
        require(not any(A >> u & 1 and not (A >> v & 1) for u, v in pair), 'new messages do not leave their forward closure')
        exports = [e for e in boundaries[k] if A >> routes[e][0] & 1 and not (A >> routes[e][1] & 1)]
        # Every unblocked old edge is closed; these are all remaining exports.
        # Every selected source stays inside. Retaining the outside rows of
        # the exact diagonal minor gives a nonzero diagonal subminor.
        demanded = sum(not (A >> canon[word.terminals[e]] & 1) for e in cut['terminal_slots'])
        if len(exports) < demanded:
            rejected = k
            break
    if rejected is None:
        closure_survivors.append(pair)
    else:
        closure_rejects[cuts[rejected]['id']] += 1
require(len(closure_survivors) == 180, 'exact reclosure screen leaves 180 endpoint pairs')
print('Exhaustive fixed and reclosed cuts:', len(pairs), 'to', 180, flush=True)
class LimitedDinic:
 def __init__(self,n):self.adj=[[]for _ in range(n)]
 def add(self,u,v,c):
  a=[v,c,None];b=[u,0,a];a[2]=b;self.adj[u].append(a);self.adj[v].append(b)

 def flow(self,s,t,stop):
  val=0;n=len(self.adj)
  while val<stop:
   self.level=[-1]*n;self.level[s]=0;todo=deque([s])
   while todo:
    u=todo.popleft()
    for v,c,_ in self.adj[u]:
     if c and self.level[v]<0:self.level[v]=self.level[u]+1;todo.append(v)
   if self.level[t]<0:break
   self.cur=[0]*n
   def dfs(u,f):
    if u==t:return f
    while self.cur[u]<len(self.adj[u]):
     e=self.adj[u][self.cur[u]];v,c,back=e
     if c and self.level[v]==self.level[u]+1:
      z=dfs(v,min(f,c))
      if z:e[1]-=z;back[1]+=z;return z
     self.cur[u]+=1
    return 0
   while val<stop:
    z=dfs(s,stop-val)
    if not z:break
    val+=z
  return val,{v for v,l in enumerate(self.level)if l>=0}

# The flow search only discovers a cut. Each rejection is checked directly
# against the exact source graph and diagonal minor, independently of any
# claimed optimality of the flow implementation.
base = [(u, v, e) for e, (u, v) in routes.items() if e not in deleted]
flow_rejections, survivors = [], []
for pair in closure_survivors:
    rejected = False
    for cut in cuts:
        network = LimitedDinic(N + 2)
        for u, v, e in base:
            network.add(u, v, 1)
        for u, v in pair:
            network.add(u, v, 1)
        roots = {canon[word.inputs[~j]] for j in cut['source_axes']}
        targets = {canon[word.terminals[e]] for e in cut['terminal_slots']}
        for u in roots:
            network.add(N, u, 1289)
        for u in targets:
            network.add(u, N + 1, 1289)
        value, A = network.flow(N, N + 1, cut['rank'])
        if value >= cut['rank']:
            continue
        A -= {N, N + 1}
        require(roots <= A and not (targets & A), 'all minor inputs inside and outputs outside the deficient cut')
        outgoing = [e for u, v, e in base if u in A and v not in A]
        added = [(u, v) for u, v in pair if u in A and v not in A]
        require(len(outgoing) + len(added) == value < cut['rank'], 'direct exact deficient-cut capacity')
        flow_rejections.append({'routes': [[representative[u], representative[v]] for u, v in pair],
                                'minor_id': cut['id'], 'rank': cut['rank'], 'capacity': value,
                                'old_exports': outgoing,
                                'new_exports': [[representative[u], representative[v]] for u, v in added],
                                'raw_charts': sorted(c for c, v in canon.items() if v in A)})
        rejected = True
        break
    if not rejected:
        survivors.append(sorted([[representative[u], representative[v]] for u, v in pair]))
survivors.sort()
require(len(flow_rejections) == 60 and len(survivors) == 120, 'final exact screen census')
require(survivors == json.loads((package / 'EXPECTED-SURVIVORS.json').read_text())['pairs'], 'complete endpoint list matches retained artifact')
args.out.mkdir(parents=True, exist_ok=True)
(args.out / 'CUT-REJECTIONS.json').write_text(json.dumps(flow_rejections, indent=2) + '\n')
result = {'status': 'PASS_S031_EXHAUSTIVE_TWO_GRADE_ONE_ENDPOINT_SCREEN',
          'complete_supplier_constructed': False,
          'scope': 'Necessary exact minor-cut conditions for the fixed seven-deletion plan; arbitrary surviving internal linear recoding and retiming.',
          'directed_grade_one_routes': len(grade_one), 'routes_crossing_core_cut': len(eligible),
          'fixed_cut_pair_candidates': len(pairs), 'closure_rejections': dict(closure_rejects),
          'closure_survivors': len(closure_survivors), 'additional_verified_minor_cut_rejections': len(flow_rejections),
          'survivor_count': len(survivors), 'remaining_endpoint_pairs': survivors,
          'review_status': 'author exact enumeration; independent review is separate'}
(args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(result['status'], len(survivors), flush=True)
