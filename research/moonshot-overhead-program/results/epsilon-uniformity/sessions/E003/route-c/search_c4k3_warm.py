#!/usr/bin/env python3
"""Bounded C(4,3) product-rectangle search with an exact load-six incumbent."""
import argparse
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize._highspy import _core as hs
from scipy.sparse import coo_matrix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=600)
    ap.add_argument('--all-products', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    words = list(product(range(4), repeat=3))
    index = {w: i for i, w in enumerate(words)}
    edges = [(i, j) for i, x in enumerate(words) for j, y in enumerate(words)
             if all(a != b for a, b in zip(x, y))]
    ei = {e: i for i, e in enumerate(edges)}
    letters = []
    for a in range(1, 16):
        for b in range(1, 16):
            if a & b:
                continue
            if not args.all_products and not (a.bit_count() + b.bit_count() == 4 or
                                             a.bit_count() == b.bit_count() == 1):
                continue
            letters.append(([i for i in range(4) if (a >> i) & 1],
                            [i for i in range(4) if (b >> i) & 1]))
    rectangles = [(tuple(index[w] for w in product(*(f[0] for f in fs))),
                   tuple(index[w] for w in product(*(f[1] for f in fs))))
                  for fs in product(letters, repeat=3)]
    ri = {rect: j for j, rect in enumerate(rectangles)}
    ncols, ne, nv = len(rectangles) + 1, len(edges), len(words)
    rows, columns, data = [], [], []
    for col, (source, dest) in enumerate(rectangles):
        for x in source:
            for y in dest:
                rows.append(ei[x, y]); columns.append(col); data.append(1)
            rows.append(ne + x); columns.append(col); data.append(1)
        for y in dest:
            rows.append(ne + nv + y); columns.append(col); data.append(1)
        rows.append(ne + 2 * nv); columns.append(col); data.append(1)
    for i in range(2 * nv):
        rows.append(ne + i); columns.append(ncols - 1); data.append(-1)
    matrix = coo_matrix((data, (rows, columns)), shape=(ne + 2 * nv + 1, ncols)).tocsc()
    lp = hs.HighsLp()
    lp.num_col_, lp.num_row_ = ncols, matrix.shape[0]
    lp.col_cost_ = np.r_[np.zeros(ncols - 1), 1.]
    lp.col_lower_ = np.zeros(ncols)
    lp.col_upper_ = np.r_[np.ones(ncols - 1), 6.]
    lp.row_lower_ = np.r_[np.ones(ne), np.full(2 * nv, -hs.kHighsInf), 64.]
    lp.row_upper_ = np.r_[np.ones(ne), np.zeros(2 * nv), hs.kHighsInf]
    lp.integrality_ = [hs.HighsVarType.kInteger] * ncols
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_ = matrix.indptr.astype(np.int32)
    lp.a_matrix_.index_ = matrix.indices.astype(np.int32)
    lp.a_matrix_.value_ = matrix.data.astype(float)
    incumbent = np.zeros(ncols)
    one_d = [([0, 1], [2, 3]), ([2, 3], [0, 1]),
             ([0], [1]), ([1], [0]), ([2], [3]), ([3], [2])]
    for a, b in product(range(4), repeat=2):
        for left, right in one_d:
            source = tuple(index[w] for w in product([x for x in range(4) if x != a], [b], left))
            dest = tuple(index[w] for w in product([a], [y for y in range(4) if y != b], right))
            incumbent[ri[source, dest]] = 1
    incumbent[-1] = 6
    assert np.all(matrix @ incumbent >= np.array(lp.row_lower_))
    assert np.all(matrix @ incumbent <= np.array(lp.row_upper_))
    solver = hs._Highs()
    solver.setOptionValue('output_flag', False)
    solver.setOptionValue('time_limit', args.seconds)
    solver.setOptionValue('threads', 2)
    solver.setOptionValue('mip_rel_gap', 0.)
    solver.passModel(lp)
    solution = hs.HighsSolution()
    solution.col_value = incumbent
    solution.value_valid = True
    assert solver.setSolution(solution) == hs.HighsStatus.kOk
    solver.run()
    result, info = solver.getSolution(), solver.getInfo()
    certificate = None
    if result.value_valid:
        chosen = [rectangles[i] for i, value in enumerate(result.col_value[:-1]) if value > .5]
        counts, left, right = [0] * ne, [0] * nv, [0] * nv
        for source, dest in chosen:
            for x in source:
                left[x] += 1
                for y in dest:
                    counts[ei[x, y]] += 1
            for y in dest:
                right[y] += 1
        assert set(counts) == {1}
        load = max(left + right)
        assert load <= 6 and len(chosen) >= 64
        certificate = {'rectangles': chosen, 'source_load': left, 'destination_load': right,
                       'maximum_load': load, 'exact_integer_validation': 'passed'}
    record = {'q': 4, 'k': 3, 'candidate_rectangles': ncols - 1,
              'candidate_family': 'all product rectangles' if args.all_products else
                                  'coordinate cuts maximal or singleton-singleton',
              'warm_incumbent_load': 6, 'global_rank_cut': 64,
              'solver_status': solver.modelStatusToString(solver.getModelStatus()),
              'solver_mip_bound': float(info.mip_dual_bound),
              'solver_objective': float(info.objective_function_value),
              'solver_nodes': int(info.mip_node_count), 'time_limit_seconds': args.seconds,
              'certificate': certificate,
              'scope': 'Exact checked upper certificate only; incomplete search is not an impossibility proof.'}
    args.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({key: value for key, value in record.items() if key != 'certificate'}))
    if certificate:
        print('EXACT_CERTIFICATE', len(chosen), load)


if __name__ == '__main__':
    main()
