"""Finite exact product-rectangle partition experiment, not an asymptotic proof."""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--q', type=int, default=4)
    ap.add_argument('--coordinates', type=int, default=2)
    ap.add_argument('--load', type=int, default=3)
    ap.add_argument('--seconds', type=float, default=45)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    q, k = args.q, args.coordinates
    vertices = list(itertools.product(range(q), repeat=k))
    vi = {v: i for i, v in enumerate(vertices)}
    edges = [(i, j) for i, x in enumerate(vertices) for j, y in enumerate(vertices)
             if all(a != b for a, b in zip(x, y))]
    ei = {e: i for i, e in enumerate(edges)}
    letters = []
    for a in range(1, 1 << q):
        for b in range(1, 1 << q):
            if not (a & b):
                letters.append(([i for i in range(q) if (a >> i) & 1],
                                [i for i in range(q) if (b >> i) & 1]))
    rectangles = []
    for factors in itertools.product(letters, repeat=k):
        left = [vi[x] for x in itertools.product(*(f[0] for f in factors))]
        right = [vi[y] for y in itertools.product(*(f[1] for f in factors))]
        rectangles.append((left, right))
    rows, cols, vals = [], [], []
    ne, nv = len(edges), len(vertices)
    for j, (left, right) in enumerate(rectangles):
        for x in left:
            for y in right:
                rows.append(ei[x, y]); cols.append(j); vals.append(1)
        for x in left:
            rows.append(ne + x); cols.append(j); vals.append(1)
        for y in right:
            rows.append(ne + nv + y); cols.append(j); vals.append(1)
    matrix = coo_matrix((vals, (rows, cols)),
                        shape=(ne + 2 * nv, len(rectangles))).tocsc()
    result = milp(np.ones(len(rectangles)), integrality=np.ones(len(rectangles)),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(matrix,
            np.r_[np.ones(ne), np.zeros(2 * nv)],
            np.r_[np.ones(ne), np.full(2 * nv, args.load)]),
        options={'time_limit': args.seconds, 'mip_rel_gap': 0.0})
    output = {'q': q, 'coordinates': k, 'load_cap': args.load,
        'restricted_model': 'Cartesian products of disjoint letter-subset rectangles',
        'vertices_per_side': nv, 'edges': ne, 'candidate_rectangles': len(rectangles),
        'solver_status': int(result.status), 'solver_message': result.message,
        'time_limit_seconds': args.seconds, 'certificate': None}
    if result.x is not None:
        chosen = [rectangles[i] for i, value in enumerate(result.x) if value > 0.5]
        cover = {e: 0 for e in edges}
        left_load, right_load = [0] * nv, [0] * nv
        for left, right in chosen:
            for x in left:
                left_load[x] += 1
                for y in right:
                    if (x, y) not in cover:
                        raise AssertionError('nonedge in selected rectangle')
                    cover[x, y] += 1
            for y in right:
                right_load[y] += 1
        assert all(count == 1 for count in cover.values()), 'not an exact partition'
        assert max(left_load + right_load) <= args.load, 'load cap violated'
        output['certificate'] = {'rectangles': chosen, 'left_load': left_load,
            'right_load': right_load, 'exact_integer_check': 'PASS',
            'number_of_rectangles': len(chosen)}
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: val for key, val in output.items() if key != 'certificate'}))
    if output['certificate'] is not None:
        print('PASS_EXACT_PARTITION', len(chosen), max(left_load + right_load))


if __name__ == '__main__':
    main()
