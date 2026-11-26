#!/usr/bin/env python3
"""C(4,3), load-five feasibility after fixing a high-efficiency product rectangle."""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--case', type=int, choices=[0, 1, 2], required=True)
    ap.add_argument('--seconds', type=float, default=300)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    q, k, cap = 4, 3, 5
    words = list(itertools.product(range(q), repeat=k))
    index = {word: i for i, word in enumerate(words)}
    edges = [(i, j) for i, x in enumerate(words) for j, y in enumerate(words)
             if all(a != b for a, b in zip(x, y))]
    edge_index = {edge: i for i, edge in enumerate(edges)}
    factors = [([0, 1], [2, 3]), ([0], [1, 2, 3]), ([1, 2, 3], [0])]
    shapes = [(0, 0, 0), (0, 0, 1), (0, 1, 2)]
    fixed = tuple([index[word] for word in itertools.product(*(factors[j][side] for j in shapes[args.case]))]
                  for side in (0, 1))
    fixed_source, fixed_dest = map(set, fixed)
    all_letters = []
    for a in range(1, 1 << q):
        for b in range(1, 1 << q):
            if not a & b:
                all_letters.append(([i for i in range(q) if (a >> i) & 1],
                                    [i for i in range(q) if (b >> i) & 1]))
    rectangles = []
    for fs in itertools.product(all_letters, repeat=k):
        source = [index[word] for word in itertools.product(*(f[0] for f in fs))]
        dest = [index[word] for word in itertools.product(*(f[1] for f in fs))]
        if fixed_source.intersection(source) and fixed_dest.intersection(dest):
            continue
        rectangles.append((source, dest))
    ne, nv = len(edges), len(words)
    rows, columns = [], []
    for col, (source, dest) in enumerate(rectangles):
        for x in source:
            for y in dest:
                rows.append(edge_index[x, y]); columns.append(col)
            rows.append(ne + x); columns.append(col)
        for y in dest:
            rows.append(ne + nv + y); columns.append(col)
    matrix = coo_matrix((np.ones(len(rows)), (rows, columns)),
                        shape=(ne + 2 * nv, len(rectangles))).tocsc()
    lower = np.r_[np.ones(ne), np.zeros(2 * nv)]
    upper = np.r_[np.ones(ne), np.full(2 * nv, cap)]
    for x in fixed[0]:
        upper[ne + x] -= 1
        for y in fixed[1]:
            lower[edge_index[x, y]] = upper[edge_index[x, y]] = 0
    for y in fixed[1]:
        upper[ne + nv + y] -= 1
    result = milp(np.zeros(len(rectangles)), integrality=np.ones(len(rectangles)),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, lower, upper),
                  options={'time_limit': args.seconds, 'mip_rel_gap': 0.0})
    certificate = None
    if result.x is not None:
        chosen = [fixed] + [rectangles[i] for i, value in enumerate(result.x) if value > .5]
        counts, source_load, dest_load = [0] * ne, [0] * nv, [0] * nv
        for source, dest in chosen:
            for x in source:
                source_load[x] += 1
                for y in dest:
                    counts[edge_index[x, y]] += 1
            for y in dest:
                dest_load[y] += 1
        assert set(counts) == {1}
        assert max(source_load + dest_load) <= cap
        certificate = {'rectangles': chosen, 'source_load': source_load,
                       'destination_load': dest_load, 'exact_integer_validation': 'passed'}
    record = {'q': q, 'k': k, 'load_cap': cap, 'fixed_case': args.case,
              'fixed_rectangle': fixed, 'remaining_candidates': len(rectangles),
              'solver_status': int(result.status), 'solver_message': result.message,
              'time_limit_seconds': args.seconds, 'certificate': certificate,
              'scope': 'All Cartesian product rectangles disjoint from one fixed rectangle; status is solver evidence.'}
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({key: value for key, value in record.items() if key != 'certificate'}))
    if certificate:
        print('EXACT_LOAD_FIVE_PARTITION', len(chosen))


if __name__ == '__main__':
    main()
