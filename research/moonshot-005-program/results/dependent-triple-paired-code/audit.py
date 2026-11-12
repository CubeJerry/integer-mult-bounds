#!/usr/bin/env python3
"""Actual-source residual rank, exact current-row checks, and semantic mutants."""
import argparse
import copy
import sys
from pathlib import Path


def main(a):
    sys.path.insert(0, str(a.reconstruction))
    from common import F, need, load_inputs, sha, gzip, json, rank, root, add
    import build as replay
    s, original, _ = load_inputs(a.repo)
    wb = (a.output / 'WORD.json.gz').read_bytes()
    w = json.loads(gzip.decompress(wb))
    fb = (a.output / 'FORWARD.json.gz').read_bytes()
    forward = json.loads(gzip.decompress(fb))
    raw = {int(x): j for x, j in w['private_role_map'].items()}
    actual, locations = replay.interpret_prefix(s, w)
    baseline, old_locations = replay.interpret_prefix(s, forward)
    need(locations == old_locations, 'same actual prefix charts')
    selected = [0, 1, 98]
    hosted = {s['live'][k]: (x, y) for k, x, y in
              zip(s['hosted']['Dports'], s['hosted']['X2'], s['hosted']['Y2'])}
    roots = {x: root(s['frames'][s['initial'][x]][0]) for x in s['live']}
    dot = lambda x, y: sum(u * v for u, v in zip(roots[x], roots[y]))
    X, Y = s['hosted']['X2'], s['hosted']['Y2']
    iy = {y: i for i, y in enumerate(Y)}
    ix = {x: i for i, x in enumerate(X)}
    response = [[F(0) for _ in Y] for _ in X]
    q = {r: {raw[r]: F(1), r: F(-1)} for r in raw}
    reverse = {}
    for j, (b, _) in hosted.items():
        expected = baseline[raw[b]]
        for i in selected:
            d = hosted[i][1]
            c = F(dot(i, j), 8) if i != j else F(0)
            response[ix[b]][iy[d]] = c
            if c:
                reverse.setdefault(b, {})[d] = c
                expected = add(expected, q[d], c)
        need(actual[raw[b]] == expected, 'real hosted row matches source Gram')
    for field, old in baseline.items():
        if field not in {raw[b] for b in X}:
            need(actual[field] == old, 'other1880-coordinate rows preserved')
    for i in selected:
        need(actual[raw[i + 112]] == add(q[i + 112], q[i]),
             'real ordinary first receiver completed')
    declared = {int(b): {int(d): F(c) for d, c in row}
                for b, row in w['paired_reverse_corrections'].items()}
    need(declared == reverse, 'metadata exactly matches source-derived map')
    residual = [[F(i == j) + response[i][j] for j in range(96)]
                for i in range(96)]
    gram = [[dot(i, j) for j in selected] for i in selected]
    need(rank(gram) == 2 and rank(residual) == 95,
         'actual source residual loses exactly one rank')
    relation = [1, -1, -1]
    need(all(sum(h * roots[i][k] for h, i in zip(relation, selected)) == 0
             for k in range(8)), 'explicit source root dependence')
    kernel = [F(0) for _ in Y]
    for i, h in zip(selected, relation):
        kernel[iy[hosted[i][1]]] = F(h)
    need(all(sum(c * h for c, h in zip(row, kernel)) == 0
             for row in residual), 'actual source residual annihilates relation')
    need(all(sum(kernel[i] * residual[i][j] for i in range(96)) == 0
             for j in range(96)), 'actual left residual kernel')
    need(all(residual[i][i] == 1 for i in range(96)),
         'no individual reverse pair is completed')

    mutants = {}
    def reject(name, mutated):
        try:
            rows, charts = replay.interpret_prefix(s, mutated)
            need(rows == actual and charts == locations,
                 'wrong exact1880-coordinate prefix')
            replay.typed(s, mutated)
        except (ValueError, KeyError, IndexError) as error:
            mutants[name] = str(error)
        else:
            raise ValueError('mutant survived: ' + name)

    group = w['paired_collection']['groups'][0]
    for name, event, coefficient in [
        ('dual_encoder_retains_original', group['encoder_snapshots'][-1] + 1, '0'),
        ('dual_facet_injection_wrong_sign', group['injections'][0]['event'], '1'),
        ('dual_decoder_retains_original', group['decoder_snapshots'][-1] + 1, '0'),
    ]:
        mutated = copy.deepcopy(w)
        need(mutated['program'][event][0] == 'ADD', 'actual mutant ADD location')
        mutated['program'][event][3] = coefficient
        reject(name, mutated)
    injection = group['injections'][0]
    source = raw[injection['source_Y2']]
    source_moves = [event for event, instruction in enumerate(w['program'])
                    if event < injection['event'] and instruction[0] == 'MOVE'
                    and instruction[1] == source]
    need(len(source_moves) == 1, 'literal one selected Y2 positioning route')
    mutated = copy.deepcopy(w)
    mutated['program'][source_moves[0]][3] = 127
    reject('Y2_source_not_at_actual_facet', mutated)
    provenance = w['parent_forward_collection_provenance']
    pivot = next(term for term in provenance['donor_terms'] if term.get('pivot'))
    parent_event = pivot['inverse_scale_event']
    matching = [event for event, inherited in enumerate(w['parent_event_of_output'])
                if inherited == parent_event]
    need(len(matching) == 1, 'one inherited primal inverse SCALE')
    mutated = copy.deepcopy(w)
    mutated['program'][matching[0]][2] = '1'
    reject('primal_pivot_inverse_not_applied', mutated)
    route = provenance['receiver_routes'][0]
    parent_event = route['reads'][0]['move_event']
    matching = [event for event, inherited in enumerate(w['parent_event_of_output'])
                if inherited == parent_event]
    need(len(matching) == 1, 'one inherited receiver acquisition MOVE')
    mutated = copy.deepcopy(w)
    mutated['program'][matching[0]][3] = s['final'][route['receiver']]
    reject('forward_receiver_skips_pair_chart', mutated)
    bad_kernel = kernel.copy()
    bad_kernel[iy[hosted[1][1]]] *= -1
    need(any(sum(c * h for c, h in zip(row, bad_kernel))
             for row in residual), 'wrong-sign kernel rejected')
    mutants['reverse_kernel_wrong_sign'] = 'nonzero exact residual image'
    result = {
        'status': 'PASS_SOURCE_RESIDUAL_RANK95_AND_SEMANTIC_MUTANTS',
        'word_sha256': sha(wb), 'word_payload_sha256': sha(gzip.decompress(wb)),
        'source_sha256': original['source_sha256'],
        'independent_input_coordinates': 1880,
        'source_Gram': gram, 'source_Gram_rank': 2,
        'reverse_addition_rank': rank(response),
        'remaining_reverse_target_rank': 95,
        'ordinary_reverse_pairs_completed': 0,
        'source_root_relation': dict(zip(map(str, selected), relation)),
        'actual_reverse_input_kernel': {str(y): str(c) for y, c in zip(Y, kernel) if c},
        'completed_reverse_output_combination': {str(x): str(c) for x, c in zip(X, kernel) if c},
        'mutants': mutants,
        'scope': 'Exact finite source verification, using retained replay helpers. '
                 'One reverse residual direction is removed; no individual reverse '
                 'pair or complete shared native is completed. No new kappa.',
    }
    (a.output / 'AUDIT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--reconstruction', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
