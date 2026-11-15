#!/usr/bin/env python3
"""Independent check that a changed proper-mode basis escapes the singleton gate."""
import argparse
import hashlib
import json
from pathlib import Path

from check import SOURCE_SHA, bits, dot, kernel, need, rank2, rref
from eight_check import binary_basis, solve_combination


def check(source, candidate):
    raw = source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'authenticated root source')
    roots = json.loads(raw)['native_roots']
    body = json.loads(candidate.read_text())
    omitted = [0, 0, 1, 1, 0, 0, 1, -1]
    h = bits(j for j, root in enumerate(roots)
             if ((dot(roots[72], root)+dot(omitted, root))//2) % 2)
    canonical = [bits(j for j, other in enumerate(roots)
                      if j == i or dot(root, other) == 0)
                 for i, root in enumerate(roots)]
    all_x = (1 << 111)-1
    W = binary_basis([row & (h if h >> i & 1 else all_x ^ h)
                      for i, row in enumerate(canonical)])
    seeds = [canonical[i] for i in [1, 3, 5, 10, 11, 15, 30]] + [canonical[0] & h]
    need(rank2(W) == 15 and rank2(seeds) == 8, 'fixed target and seed dimensions')
    rows, normals, charts = [], [], []
    for entry in body['modes']:
        word, normal = int(entry['word']), entry['normal']
        support = [root for j, root in enumerate(roots) if word >> j & 1]
        need(solve_combination(W, word) is not None, 'mode belongs to W')
        need(all(dot(root, normal) == 0 for root in support), 'mode supported in stated facet')
        need(len(rref(support)) == 7, 'support spans its unique actual facet')
        need(kernel([normal]) == rref(support), 'exact facet identity')
        rows.append(word)
        normals.append(normal)
        charts.append(kernel([normal]))
    need(len(rows) == 7 and rank2(seeds+rows) == 15, 'seven modes complete W with fixed eight seeds')
    demands, witnesses = [], []
    for j, root in enumerate(roots):
        demand = [k for k, row in enumerate(rows) if row >> j & 1]
        distinct = {charts[k] for k in demand}
        common = [i for i, other in enumerate(roots)
                  if all(dot(other, normals[k]) == 0 for k in demand)]
        if demand:
            need(j in common, 'each demanded original lies in acquisition intersection')
        if len(distinct) >= 2:
            demands.append({'source': j, 'demanded_mode_indices': demand,
                            'distinct_facets': len(distinct), 'common_native_originals': common})
            if common == [j]:
                witnesses.append(j)
    need(not witnesses, 'changed basis passes every singleton-source test')
    # A negative control verifies the detector against the old fixed basis.
    old_normals = [roots[i] for i in [1, 3, 5, 10, 30, 61]] + [omitted]
    old_rows = [canonical[i] & h for i in [1, 3, 5, 10, 30, 61]]
    old_rows.append(bits(j for j, root in enumerate(roots) if dot(root, omitted) == 0))
    old_witnesses = []
    for j in range(111):
        demand = [k for k, row in enumerate(old_rows) if row >> j & 1]
        if len(demand) >= 2:
            common = [i for i, root in enumerate(roots)
                      if all(dot(root, old_normals[k]) == 0 for k in demand)]
            if common == [j]:
                old_witnesses.append(j)
    need(6 in old_witnesses, 'old-basis X6 negative control')
    return {'status': 'PASS_INDEPENDENT_CHANGED_BASIS_CONTROL',
            'source_sha256': SOURCE_SHA,
            'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'seed_rank': 8, 'mode_count': 7, 'distinct_acquisition_facets': len(set(charts)),
            'seed_plus_mode_rank': 15, 'all_modes_in_W': True, 'all_real_support_ranks': 7,
            'singleton_witnesses': witnesses, 'source_demands': demands,
            'old_basis_negative_control_witnesses': old_witnesses,
            'classification': 'Finite exact counterexample to a basis-independent singleton gate; no source construction.',
            'new_complete_kappa': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(check(args.source, args.candidate), indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
