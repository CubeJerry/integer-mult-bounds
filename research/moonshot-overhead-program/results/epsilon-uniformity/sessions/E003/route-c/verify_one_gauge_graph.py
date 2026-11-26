#!/usr/bin/env python3
"""Exact component criterion versus direct subspace assignment searches."""
from itertools import product
from functools import lru_cache
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def parity(x):
    return x.bit_count() & 1


def points(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


@lru_cache(None)
def subspaces(d):
    known, frontier = {1}, {1}
    while frontier:
        following = set()
        for space in frontier:
            for x in range(1 << d):
                if (space >> x) & 1:
                    continue
                larger = space | sum(1 << (x ^ u) for u in points(space))
                if larger not in known:
                    following.add(larger)
        known.update(following)
        frontier = following
    return tuple(sorted(known))


@lru_cache(None)
def perpendicular(space, d):
    return sum(1 << x for x in range(1 << d)
               if all(not parity(x & u) for u in points(space)))


def span(vectors):
    result = 1
    for x in vectors:
        result |= sum(1 << (x ^ u) for u in points(result))
    return result


def criterion(directions, edges, d):
    n = len(directions)
    adjacency = [[] for _ in range(2 * n)]
    for v, w in edges:
        adjacency[v].append(n + w)
        adjacency[n + w].append(v)
    seen, components = set(), []
    inputs, outputs = [1] * n, [1] * n
    for start in range(2 * n):
        if start in seen or not adjacency[start]:
            continue
        component, pending = {start}, [start]
        seen.add(start)
        while pending:
            node = pending.pop()
            for other in adjacency[node]:
                if other not in seen:
                    seen.add(other)
                    component.add(other)
                    pending.append(other)
        a = sorted(v for v in component if v < n)
        b = sorted(v - n for v in component if v >= n)
        components.append((a, b))
        if any(parity(directions[v] & directions[w]) for v in a for w in b):
            return False, None, components
        common = span(directions[w] for w in b)
        for v in a:
            inputs[v] = common
        for w in b:
            outputs[w] = perpendicular(common, d)
    auxiliary = [perpendicular(1 | (1 << direction), d) for direction in directions]
    assert all(not (u & ~aux) for u, aux in zip(inputs, auxiliary))
    assert all(not (v & ~aux) for v, aux in zip(outputs, auxiliary))
    assert all(outputs[w] == perpendicular(inputs[v], d) for v, w in edges)
    return True, (inputs, outputs), components


def brute(directions, edges, d):
    n = len(directions)
    incoming = [[v for v, dest in edges if dest == w] for w in range(n)]
    outgoing = {v for v, _ in edges}
    auxiliary = [perpendicular(1 | (1 << direction), d) for direction in directions]
    allowed = [tuple(u for u in subspaces(d) if not u & ~auxiliary[v])
               if v in outgoing else (1,) for v in range(n)]
    attempts = 0
    for inputs in product(*allowed):
        attempts += 1
        good = True
        for w, sources in enumerate(incoming):
            if not sources:
                continue
            candidate = perpendicular(inputs[sources[0]], d)
            if candidate & ~auxiliary[w] or any(perpendicular(inputs[v], d) != candidate for v in sources):
                good = False
                break
        if good:
            return True, attempts
    return False, attempts


def main():
    d, n = 3, 3
    norm_one = [x for x in range(1 << d) if parity(x)]
    graphs = assignments = feasible = infeasible = 0
    for directions in product(norm_one, repeat=n):
        eligible = [(v, w) for v in range(n) for w in range(n)
                    if v != w and not parity(directions[v] & directions[w])]
        for edge_mask in range(1 << len(eligible)):
            edges = [edge for i, edge in enumerate(eligible) if (edge_mask >> i) & 1]
            predicted, _, _ = criterion(directions, edges, d)
            found, tried = brute(directions, edges, d)
            assert predicted == found
            graphs += 1
            assignments += tried
            feasible += found
            infeasible += not found
    controls = []
    examples = [
        ('norm_one_triangle', 3, (1, 2, 4), [(i, j) for i in range(3) for j in range(3) if i != j], False),
        ('directed_triangle_is_different', 3, (1, 2, 4), [(0, 1), (1, 2), (2, 0)], True),
        ('complete_bipartite', 3, (1, 1, 2, 2), [(i, j) for i in range(4) for j in range(4) if (i < 2) != (j < 2)], True),
        ('isolated_vertex', 3, (1, 2, 7), [(0, 1), (1, 0)], True),
        ('triangle_free_P4', 4, (1, 2, 13, 7), [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)], False),
        ('directed_P4', 4, (1, 2, 13, 7), [(0, 1), (1, 2), (2, 3)], True),
    ]
    for name, dim, directions, edges, expected in examples:
        assert all(parity(v) for v in directions)
        assert all(not parity(directions[v] & directions[w]) for v, w in edges)
        prediction, assignment, components = criterion(directions, edges, dim)
        found, tried = brute(directions, edges, dim)
        assert prediction == found == expected
        if name == 'triangle_free_P4':
            full = [(i, j) for i in range(4) for j in range(4)
                    if i != j and not parity(directions[i] & directions[j])]
            assert full == sorted(edges)
            assert parity(directions[0] & directions[3]) == 1
        controls.append({'case': name, 'feasible': found, 'input_assignments_examined': tried,
                         'endpoint_components': components})
    receipt = {'status': 'passed', 'directed_graph_family': {
                   'dimension': d, 'labels': n, 'direction_tuples': len(norm_one) ** n,
                   'graphs': graphs, 'input_assignments_examined': assignments,
                   'feasible': feasible, 'infeasible': infeasible},
               'controls': controls,
               'scope': 'Exact finite graph/subspace checks of the stated one-gauge, individual-monomial-route model.',
               'sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ['ONE-GAUGE-GRAPH-CLASSIFICATION.md', Path(__file__).name]}}
    (ROOT / 'one-gauge-graph-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
