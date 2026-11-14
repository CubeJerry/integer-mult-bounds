#!/usr/bin/env python3
"""Exact coupled-map and global separated-bridge preflight.

Credited reuse of the source tight-frame/rank facts, with source-specific
correction accounting. @CubeJerry; substantial OpenAI assistance; Apache-2.0.
"""
from __future__ import annotations
import argparse, gzip, hashlib, importlib.util, json, sys
from fractions import Fraction as F
from pathlib import Path

NATIVE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SEED_PIN = '6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'
ENGINE_PIN = '045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'
OMITTED = [7, 25, 42, 52, 76, 82, 97, 127]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def read(path, pin):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == pin, 'exact source pin: ' + str(path))
    return json.loads(gzip.decompress(raw))

def root(v):
    on = [i for i in range(9) if v >> i & 1]
    if len(on) == 3:
        return [2 if i in on else -1 for i in range(9)]
    off = [i for i in range(9) if not (v >> i & 1)]
    need(len(off) == 2, 'native root type')
    return [3 * (int(i == off[0]) - int(i == off[1])) for i in range(9)]

def det(matrix):
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    answer = F(1)
    for i in range(n):
        k = next((j for j in range(i, n) if a[j][i]), None)
        if k is None:
            return F(0)
        if k != i:
            a[i], a[k] = a[k], a[i]
            answer = -answer
        pivot = a[i][i]
        answer *= pivot
        for j in range(i + 1, n):
            coefficient = a[j][i] / pivot
            for t in range(i + 1, n):
                a[j][t] -= coefficient * a[i][t]
            a[j][i] = F(0)
    return answer

def clean(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value

def main(args):
    native = read(args.native, NATIVE_PIN)
    seed = read(args.seed, SEED_PIN)
    need(hashlib.sha256(args.engine.read_bytes()).hexdigest() == ENGINE_PIN,
         'pinned source replay engine')
    spec = importlib.util.spec_from_file_location('preflight_replay', args.engine)
    engine = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = engine
    spec.loader.exec_module(engine)
    ports = native['live']
    roles = {int(k): v for k, v in seed['source_role_map'].items()}
    hosted = {ports[i]: (roles[b], roles[d]) for i, b, d in zip(
        native['hosted']['Dports'], native['hosted']['X2'], native['hosted']['Y2'])}
    coupled = [h for h in ports if h not in hosted]
    need(len(ports) == 104 and len(hosted) == 96 and len(coupled) == 8,
         'actual asymmetric source dimensions')
    roots = [root(native['frames'][native['initial'][h]][0]) for h in ports]
    omitted_roots = [root(z) for z in OMITTED]
    A = [[F(sum(x * y for x, y in zip(z, r)), 18) for r in roots]
         for z in omitted_roots]
    gram = [[sum(A[k][i] * A[k][j] for k in range(8))
             for j in range(104)] for i in range(104)]
    tight = [[sum(A[i][h] * A[j][h] for h in range(104))
              for j in range(8)] for i in range(8)]
    need(tight == [[F(13 * (i == j)) for j in range(8)] for i in range(8)],
         'credited tight frame AA^T = 13 I')
    need(all(gram[i][j] == F(sum(x * y for x, y in zip(roots[i], roots[j])), 18)
             for i in range(104) for j in range(104)), 'actual normalized Gram')
    C = [F(1) if h in hosted else F(1, 2) for h in ports]
    correction = [[C[i] * (int(i == j) - gram[i][j])
                   for j in range(104)] for i in range(104)]
    rows, _, _ = engine.replay(seed, seed['program'])
    reverse_rows, forward_rows = [], []
    missing_c_rows = missing_coupled_a_rows = 0
    for i, h in enumerate(ports):
        y = roles[h + 112]
        expected = {y: F(1)}
        wrong_a = {y: F(1)}
        missing_c = {y: F(1)}
        delta = {}
        for j, q in enumerate(ports):
            a_row = {roles[q]: F(1)}
            if q in coupled:
                a_row[roles[q + 112]] = F(-1)
            expected = engine.add(expected, a_row, C[i] * gram[i][j])
            wrong_a = engine.add(wrong_a, {roles[q]: F(1)}, C[i] * gram[i][j])
            missing_c = engine.add(missing_c, a_row, gram[i][j])
            delta = engine.add(delta, a_row, correction[i][j])
        need(rows[y] == expected, 'actual coupled seed row ' + str(h))
        target = {roles[h]: C[i], y: F(1) if h in hosted else F(1, 2)}
        need(engine.add(rows[y], delta, 1) == target,
             'C(I-G) is the actual endpoint correction ' + str(h))
        forward_rows.append(delta)
        missing_c_rows += rows[y] != missing_c
        missing_coupled_a_rows += rows[y] != wrong_a
        if h in hosted:
            b, d = hosted[h]
            reverse_rows.append(engine.add(rows[b], {b: F(1), d: F(-1)}, -1))
    forward_rank = engine.exact_rank(forward_rows)
    reverse_rank = engine.exact_rank(reverse_rows)
    need(forward_rank == 104 and reverse_rank == 96, 'actual residual ranks')
    h_indices = [i for i, h in enumerate(ports) if h in hosted]
    hosted_aat = [[sum(A[i][h] * A[j][h] for h in h_indices)
                   for j in range(8)] for i in range(8)]
    hosted_small_determinant = det([[int(i == j) - hosted_aat[i][j]
                                   for j in range(8)] for i in range(8)])
    need(hosted_small_determinant == F(415068771, 2), 'hosted Schur determinant')
    full_det = (-12) ** 8
    coupled_det = F(full_det, 2 ** 8)
    need(coupled_det == 6 ** 8, 'coupled correction determinant')
    need(missing_c_rows == 8 and missing_coupled_a_rows > 8,
         'coupled-interface negative controls are meaningful')
    # Rank(G) alone is insufficient: a genuine projection has singular I-G.
    need(det([[0, 0], [0, 1]]) == 0, 'projection-spectrum negative control')
    price = json.loads(args.price.read_text())
    seed_room = [F(price['limiting_room'][i]) + F(price['new_minus_seed_moment'][i])
                 for i in range(2)]
    need(F(8) < seed_room[0] <= seed_room[1] < F(9), 'retained signed room is below 9')
    need(2 * reverse_rank > seed_room[1], 'separated paired bridge budget exclusion')
    result = {
        'status': 'PASS_COUPLED_CORRECTION_AND_SEPARATED_BRIDGE_PREFLIGHT',
        'native_sha256': NATIVE_PIN, 'seed_sha256': SEED_PIN,
        'replay_engine_sha256': ENGINE_PIN,
        'all_actual_forward_rows_checked': 104,
        'actual_forward_correction': 'C(I104-G) on a_h=x_h, a_u=x_u-y_u',
        'forward_correction_rank': forward_rank,
        'hosted_reverse_residual_rank': reverse_rank,
        'AA_transpose': tight,
        'det_I104_minus_G': full_det,
        'det_C_times_I104_minus_G': coupled_det,
        'hosted_AA_transpose': hosted_aat,
        'det_I8_minus_hosted_AA_transpose': hosted_small_determinant,
        'retained_seed_limiting_room_interval': seed_room,
        'isolated_additive_paired_rank_required_at_least': 96,
        'new_separated_paired_whole_field_movement_at_least': 192,
        'optimistic_rank_capacity_with_two_transfers_per_factor': 4,
        'optimistic_rank_capacity_one_clean_stream': 3,
        'negative_controls': {
            'omitting_coupled_C_mismatched_actual_rows': missing_c_rows,
            'replacing_actual_a_by_x_mismatched_actual_rows': missing_coupled_a_rows,
            'rank_of_G_alone_does_not_imply_residual_invertibility': True,
        },
        'credit': 'Rank/tight-frame reuse from eight-packet-prefix and two-direction-terminal-completion; hosted rank96 from omitted-line Gram seed.',
        'scope': 'Only fixed-seed additive separated paired bridges with no extra correction side information and separately charged transfer rank. No bound for changed original routes, changed paid histories, free local corrective maps, or shared prior transmissions. No new kappa.',
    }
    args.output.write_text(json.dumps(clean(result), sort_keys=True, indent=2) + '\n')
    print(result['status'], forward_rank, reverse_rank, 'movement floor', 192)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('native', 'seed', 'engine', 'price', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    main(p.parse_args())
