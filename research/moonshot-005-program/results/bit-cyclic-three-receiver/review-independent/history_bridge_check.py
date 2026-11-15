#!/usr/bin/env python3
"""Exact historical/terminal closure quotients; no physical delivery assumption."""
import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from check import SOURCE_SHA, bits, dot, kernel, need, rank2, rref
from eight_check import binary_basis, combine, kernel_combinations, replay, separator, solve_combination


def rank_mod(rows, prime=107):
    rows = [[x % prime for x in row] for row in rows]
    rank = 0
    for column in range(8):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [(x*inverse) % prime for x in rows[rank]]
        for i in range(rank+1, len(rows)):
            value = rows[i][column]
            if value:
                rows[i] = [(x-value*y) % prime for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == 8:
            break
    return rank


def integer_normal(vector):
    denominator = math.lcm(*(x.denominator for x in vector))
    integers = [int(x*denominator) for x in vector]
    divisor = math.gcd(*integers)
    integers = [x//divisor for x in integers]
    if next(x for x in integers if x) < 0:
        integers = [-x for x in integers]
    return integers


def quotient_analysis(roots, base, target_rows):
    base = binary_basis(base)
    extension = []
    for row in binary_basis(target_rows):
        if solve_combination(base+extension, row) is None:
            extension.append(row)
    whole = base+extension
    all_x = (1 << 111)-1
    receivers = []
    for i, root in enumerate(roots):
        local = bits(j for j, other in enumerate(roots) if dot(root, other) == 0)
        forbidden = all_x ^ local
        projected = [row & forbidden for row in base]
        coefficients = solve_combination(projected, 1 << i)
        local_q = binary_basis(mask >> len(base)
                               for mask in kernel_combinations([row & forbidden for row in whole]))
        target_coordinates = solve_combination(whole, target_rows[i])
        need(target_coordinates is not None, 'target fitting row lies in whole space')
        required = target_coordinates >> len(base)
        need((solve_combination(local_q, required) is not None) == (coefficients is not None),
             'quotient equation equals direct receiver fitting test')
        entry = {'receiver': i, 'base_feasible': coefficients is not None,
                 'required_quotient': required, 'local_quotient_basis': local_q}
        if coefficients is None:
            witness = separator(projected, 1 << i, forbidden)
            need(all((row & witness).bit_count() % 2 == 0 for row in base), 'dual annihilates full base')
            entry['dual_input_hex'] = hex(witness)
            entry['dual_input_support'] = [j for j in range(111) if witness >> j & 1]
        else:
            fitting = combine(base, coefficients)
            need((fitting & forbidden) == 1 << i, 'actual fitting witness')
            entry['fitting_row_hex'] = hex(fitting)
            entry['base_coefficient_mask'] = coefficients
        receivers.append(entry)
    # If every local ambiguity is already forced into the added observation
    # space, the receiver forces its required quotient into that space too.
    # This is a scalar-extension proof certificate, not a finite subspace search.
    forced, steps = [], []
    changed = True
    while changed:
        changed = False
        for entry in receivers:
            required = entry['required_quotient']
            local_q = entry['local_quotient_basis']
            if solve_combination(forced, required) is None and all(solve_combination(forced, row) is not None for row in local_q):
                steps.append({'receiver': entry['receiver'], 'required_quotient': required,
                              'local_quotient_basis': local_q, 'previous_forced_basis': list(forced)})
                forced = binary_basis(forced+[required])
                changed = True
    need(len(forced) == len(extension), 'all quotient dimensions are universally compulsory')
    return {'base_rank': len(base), 'whole_rank': len(whole), 'quotient_dimension': len(extension),
            'minimum_added_global_information_per_width': len(forced),
            'extension_rows_hex': [hex(row) for row in extension],
            'base_feasible_count': sum(entry['base_feasible'] for entry in receivers),
            'forced_steps': steps, 'receivers': receivers,
            'scope': 'New global linear observations lie in the stated whole space; no transport is supplied.'}, extension


def feasible_count(roots, rows):
    all_x = (1 << 111)-1
    return sum(solve_combination([row & (all_x ^ bits(j for j, other in enumerate(roots) if dot(root, other) == 0))
                                  for row in rows], 1 << i) is not None
               for i, root in enumerate(roots))


def check(source, word_path):
    raw = source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'authenticated native root source')
    roots = json.loads(raw)['native_roots']
    word = json.loads(word_path.read_text())
    receipt = replay(word, roots)
    G = [int(row) for row in receipt['history_basis']]
    T = [int(receipt['records_at_final'][f'P{i}']['coefficient_hex'], 16) for i in range(8)]
    canonical = [bits(j for j, other in enumerate(roots) if i == j or dot(root, other) == 0)
                 for i, root in enumerate(roots)]
    b = [0, 0, 1, 1, 0, 0, 1, -1]
    h = bits(j for j, root in enumerate(roots) if ((dot(roots[72], root)+dot(b, root))//2) % 2)
    all_x = (1 << 111)-1
    split = [row & (h if h >> i & 1 else all_x ^ h) for i, row in enumerate(canonical)]
    C = binary_basis(canonical)
    W = binary_basis(split)
    need((rank2(G), rank2(T), len(C), len(W)) == (18, 8, 9, 15), 'fixed interface dimensions')
    gw, ew = quotient_analysis(roots, G, split)
    gc, ec = quotient_analysis(roots, G, canonical)
    tc, et = quotient_analysis(roots, T, canonical)
    need((gw['quotient_dimension'], gc['quotient_dimension'], tc['quotient_dimension']) == (4, 2, 5), 'four/two/five exact gaps')
    need((gc['base_feasible_count'], tc['base_feasible_count']) == (38, 14), 'historical and terminal counts')
    original_canonical_seed_indices = [1, 3, 5, 10, 11, 15, 30]
    old_seeds = [canonical[i] for i in original_canonical_seed_indices]
    need(rank2(old_seeds) == 7 and all(solve_combination(G, row) is not None for row in old_seeds), 'seven original canonical seeds remain in history')
    need(rank2(G)+len(C)-rank2(G+C) == 7, 'no canonical dimension gained beyond original seeds')
    proper = []
    rank_histogram = Counter()
    for mask in range(1, 1 << len(C)):
        row = combine(C, mask)
        support = [root for j, root in enumerate(roots) if row >> j & 1]
        rank = rank_mod(support)
        rank_histogram[rank] += 1
        if rank < 8:
            need(len(rref(support)) == rank == 7, 'matching exact real rank lower and upper bounds')
            normal = integer_normal(kernel(support)[0])
            need(all(dot(root, normal) == 0 for root in support), 'exact rational normal certificate')
            need(all(rref([normal]) != rref([root]) for root in roots), 'proper canonical normal is omitted')
            need(row == bits(j for j, root in enumerate(roots) if dot(root, normal) == 0), 'proper canonical word is full omitted-root contact mode')
            proper.append({'mode_hex': hex(row), 'source_count': len(support), 'real_support_rank': rank,
                           'normal': normal, 'historical_quotient': solve_combination(G+ec, row) >> len(G),
                           'terminal_quotient': solve_combination(T+et, row) >> len(T)})
    need(len(proper) == 9 and rank_histogram == {7:9, 8:502}, 'complete canonical proper-mode classification')
    c = [1, 0, 0, 1, 1, 0, 0, 1]
    kb = bits(j for j, root in enumerate(roots) if dot(root, b) == 0)
    kc = bits(j for j, root in enumerate(roots) if dot(root, c) == 0)
    need(solve_combination(C, kb) is not None and solve_combination(C, kc) is not None, 'both proposed additions are canonical modes')
    need(rank2(G+[kb, kc]) == 20, 'two proper additions span the missing canonical quotient')
    coefficients = [solve_combination(G+[kb, kc], row) for row in canonical]
    need(all(coefficient is not None for coefficient in coefficients), 'all canonical fitting rows supplied algebraically')
    for row, coefficient in zip(canonical, coefficients):
        need(combine(G+[kb, kc], coefficient) == row, 'exact full fitting representation')
    single_counts = {str(q):feasible_count(roots, G+[combine(ec, q)]) for q in range(1, 4)}
    need(single_counts == {'1':59, '2':68, '3':60}, 'single canonical quotient extensions remain incomplete')
    need(feasible_count(roots, G+[kb, kc]) == 111, 'both additions give all relaxed receiver fits')
    need(rank2([mode['terminal_quotient'] for mode in proper]) == 5, 'proper canonical modes span terminal completion quotient')
    return {'status': 'PASS_EXACT_HISTORICAL_TERMINAL_BRIDGE', 'source_sha256': SOURCE_SHA,
            'word_sha256': hashlib.sha256(word_path.read_bytes()).hexdigest(), 'author_code_imported': False,
            'G_plus_W': gw, 'G_plus_C': gc, 'T_plus_C': tc,
            'G_intersection_C_dimension': 7, 'T_intersection_C_dimension': 4,
            'G_intersection_C_equals_original_seed_span': original_canonical_seed_indices,
            'new_canonical_dimensions_from_masked_history': 0,
            'proper_canonical_classification': proper, 'canonical_nonzero_word_real_rank_histogram': dict(rank_histogram),
            'two_mode_algebraic_completion': {'normals': [b, c], 'mode_hex': [hex(kb), hex(kc)],
                                            'canonical_fitting_coefficients': coefficients,
                                            'basis_order': '18 history basis rows, then K_b, then K_c',
                                            'history_basis_hex': [hex(row) for row in G],
                                            'receiver_fits': 111, 'actual_source_or_delivery_constructed': False},
            'single_nonzero_canonical_quotient_receiver_counts': single_counts,
            'negative_controls': {'only_K_b_fits': feasible_count(roots, G+[kb]),
                                  'only_K_c_fits': feasible_count(roots, G+[kc]),
                                  'terminal_replaces_history_fits': feasible_count(roots, T+[kb, kc])},
            'new_complete_kappa': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--word', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.write_text(json.dumps(check(args.source, args.word), indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
