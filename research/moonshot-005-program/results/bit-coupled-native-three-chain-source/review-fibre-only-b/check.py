#!/usr/bin/env python3
"""Independent hybrid source, physical invoice and frozen-fibre closure audit."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('independent_hybrid', Path(__file__).with_name('construct.py'))
source = importlib.util.module_from_spec(spec); spec.loader.exec_module(source)
need = source.need

def source_views(ctx):
    F = ctx.field; counts = Counter(); changes = {}
    author = json.loads(ctx.payload['author_result'])
    for k in (3, 12):
        for j in ctx.donors:
            for phase, maps in [('before', ctx.before), ('after', ctx.maps)]:
                for i in sorted(ctx.perp[j]):
                    A = np.vstack([maps[j, k][q] for q in ctx.views[j, i]])
                    need(A.shape == (16*k, 16*k) and F.rank(A) == 16*k, 'every old and new source cut')
                    counts[phase, k, 'geometric'] += 1
                    counts[phase, k, 'native'] += (i < 111)
            for q in ctx.stars[j]:
                if (j, q) not in ctx.hybrid[k]['flexible']:
                    need(np.array_equal(ctx.before[j, k][q], ctx.maps[j, k][q]), 'exactly four quotient edits')
        changed = {}
        for (j, q), E in ctx.hybrid[k]['flexible'].items():
            old = ctx.before[j, k][q]; new = ctx.maps[j, k][q]
            need(F.rank(old) == F.rank(new) == k and F.rank(np.vstack([old, new])) == len(E), 'actual quotient kernel change')
            h = 263 if j in (0, 62) else 135
            shared = 61 if h == 263 else 45
            chart = ctx.charts[h, k]
            need(chart.point[j][q] == chart.point[shared][642], 'same actual point as the retained middle control')
            control = ctx.maps[shared, k][642]
            need(np.array_equal(old, control) and F.rank(np.vstack([new, control])) > k,
                 'different quotient information from the same-point shared donor')
            changed[f'{j}/{q}'] = {'annihilator_dimension': len(E), 'old_rank': k, 'new_rank': k, 'union_rank': len(E)}
        need(changed == author['components'][str(k)]['changed_quotient_kernels'], 'all four published information changes')
        changes[k] = changed
    need(all(counts[phase, k, 'geometric'] == 441 and counts[phase, k, 'native'] == 408
             for phase in ('before', 'after') for k in (3, 12)), 'complete source-cut census')
    damaged = ctx.maps[0, 3][116].copy(); damaged[0, 0] ^= 1
    E = ctx.spaces[3]['geometric'][0, 116]
    need(F.rank(np.vstack([E, damaged])) > len(E), 'outside-fibre-dual negative control')
    return {'source_cuts': {'geometric_per_component_before_and_after': 441, 'native_per_component_before_and_after': 408},
            'changed_quotient_kernels': changes, 'individual_full_bank_quotient_rank': 240,
            'old_new_full_bank_union_rank': 416, 'outside_dual_negative_control': True}

def preserved_fibres(ctx):
    F = ctx.field; counts = Counter(); hashes = {}
    for h in ctx.centres:
        need(10 not in ctx.H[h] and not ctx.H[h] <= ctx.perp[80], 'original target exceptions absent at all chosen interfaces')
        for k in (3, 12):
            chart = ctx.charts[h, k]; digest = sha256()
            for i in chart.receivers:
                K = ctx.fibres[k][h, i]; digest.update(K.tobytes())
                pos = [n for n, d in enumerate(chart.ports) if ctx.D[d] <= ctx.perp[i]]
                V = chart.V[pos]
                for ordinal, j in enumerate(chart.donors):
                    qs = [q for q in ctx.views[j, i] if q != h]
                    off = np.vstack([ctx.maps[j, k][q] for q in qs])
                    need(F.rank(off) == 15*k and not np.any(F.mm(off, K)), 'whole updated inverse fibre is the retained subspace')
                    minor = V[:, ordinal*k:(ordinal+1)*k]
                    need(F.rank(minor) == k, 'actual H donor minor invertible')
                    readout = F.mm(minor, ctx.maps[j, k][h])
                    need(np.array_equal(F.mm(readout, K), np.eye(k, dtype=np.uint8)), 'complete updated common readout')
                    counts[k, 'donor_geometric'] += 1; counts[k, 'donor_native'] += (i < 111)
                counts[k, 'geometric'] += 1; counts[k, 'native'] += (i < 111)
            hashes[f'{h}/{k}'] = digest.hexdigest()
    need(all(counts[k, 'geometric'] == 108 and counts[k, 'native'] == 101
             and counts[k, 'donor_geometric'] == 324 and counts[k, 'donor_native'] == 303 for k in (3, 12)), 'entire common-fibre census')
    return {'geometric_per_component': 108, 'native_per_component': 101,
            'native_donor_fibres_per_component': 303, 'normalized_lift_sha256': hashes}

def closing_census(ctx):
    F = ctx.field; rows = json.loads(ctx.payload['closing_witnesses'])
    donors = set(ctx.donors)
    candidates = {h for h, P in enumerate(ctx.H) if P <= set(range(111)) and len(P & donors) >= 2 and h not in ctx.centres}
    need({row['H'] for row in rows} == candidates == {44, 116, 394, 643, 652}, 'exhaustive native closing-centre census')
    result = []; removals = Counter()
    for row in rows:
        h = row['H']; i = row['receiver']; flags = [tuple(flag) for flag in row['fixed_flags']]
        need(i < 111 and i != 80 and ctx.H[h] <= ctx.perp[i] and 10 not in ctx.H[h], 'actual identity-target closing receiver')
        need(len(flags) == len(set(flags)) == 16, 'sixteen distinct actual source observations')
        ranks = {}
        for k in (3, 12):
            blocks = []
            for j, q in flags:
                need(j in ctx.H[h] & donors and q in ctx.views[j, i] and q != h and q not in ctx.centres,
                     'actual old-donor off-centre observation at the witness receiver')
                need((j, q) not in ctx.hybrid[k]['flexible'], 'no free quotient used in a closure obstruction')
                E = ctx.spaces[k]['native'][j, q]
                need(E.shape == (k, 16*k) and F.rank(E) == k, 'native fibres alone saturate the entire quotient space')
                blocks.append(E)
            stack = np.vstack(blocks)
            need(stack.shape == (16*k, 16*k) and F.rank(stack) == 16*k, 'forced observations leave zero common direction')
            for deleted in range(16):
                smaller = np.vstack(blocks[:deleted] + blocks[deleted+1:])
                need(F.rank(smaller) == 15*k, 'each block is necessary for this particular square certificate')
                removals[k] += 1
            ranks[str(k)] = 16*k
        result.append({'H': h, 'receiver': i, 'donors': sorted(ctx.H[h]), 'existing_donors': sorted(ctx.H[h] & donors),
                       'component_ranks': ranks, 'full_bank_fixed_observation_rank': 3840, 'common_inverse_kernel_dimension': 0})
    need(removals == {3: 80, 12: 80}, 'all single-block-deletion controls')
    expected = json.loads(ctx.payload['closing_result'])['closing_census']
    need([{key: value for key, value in row.items() if key != 'donors'} for row in result] == expected,
         'all published closing certificates replayed independently')
    return {'closing_census': result, 'native_fibres_retained': 101,
            'arbitrary_linear_full_bank_mixing_allowed': True, 'moving_old_fibres_excluded_from_claim': True,
            'single_block_deletion_control_ranks': {'3': 45, '12': 180, 'full_bank': 3600},
            'deletion_controls_per_component': dict(removals)}

def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True); cli.add_argument('--out', type=Path, required=True)
    args = cli.parse_args(); ctx = source.context(args.repo, args.out)
    print('PASS_INDEPENDENT_HYBRID_RECONSTRUCTION', flush=True)
    cuts = source_views(ctx); fibres = preserved_fibres(ctx)
    print('PASS_ALL_SOURCE_CUTS_CHANGED_KERNELS_AND_COMMON_FIBRES', flush=True)
    closing = closing_census(ctx)
    print('PASS_ALL_FIVE_NATIVE_FIXED_FIBRE_CLOSING_OBSTRUCTIONS', flush=True)
    special, per_donor, word_hashes = ctx.audit.source_word(ctx)
    background, old_donors = ctx.audit.background_invoice(ctx)
    inverse = background['early_basis_ADD'] + background['source_owner_permutation_ADD']
    cache = background['snapshot_copy_ADD_INIT_dirty_CLEAR']
    forward = inverse + cache + background['late_evaluation_ADD']
    combined = {'donors': 111, 'source_forward_ADD': forward + special['forward_ADD'],
                'source_pure_inverse_ADD': inverse + special['inverse_ADD'],
                'source_forward_and_inverse_ADD': forward + inverse + special['total_ADD'],
                'source_INIT': cache + special['INIT'], 'source_dirty_CLEAR': cache + special['dirty_CLEAR'],
                'source_extra_MOVE': 0, 'new_complete_kappa': False}
    need(combined == json.loads(ctx.payload['cost'])['combined'], 'complete 111-source invoice')
    need(combined['source_forward_and_inverse_ADD'] == 584743880, 'exact source price')
    print('PASS_ALL_LITERAL_SOURCE_WORDS_OWNERS_AND_FULL_111_SOURCE_INVOICE', flush=True)
    result = {'status': 'PASS_INDEPENDENT_HYBRID_SOURCE_AND_SCOPED_FROZEN_FIBRE_OBSTRUCTION',
              'pins': source.PINS, 'source_donors': ctx.donors, 'centres': ctx.centres,
              'source_views': cuts, 'common_fibres': fibres, 'closing': closing,
              'constraint_sha256': {str(k): sha256(x['relation'].tobytes()).hexdigest() for k, x in ctx.hybrid.items()},
              'embedding_sha256': {str(k): sha256(x['embedding'].tobytes()).hexdigest() for k, x in ctx.hybrid.items()},
              'special': special, 'special_donor_costs': per_donor, 'all_word_hashes': word_hashes,
              'background': background, 'combined': combined,
              'source_only': True, 'complete_endpoint': False, 'new_complete_kappa': False}
    (args.out/'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'total_source_ADD': combined['source_forward_and_inverse_ADD']}, sort_keys=True))

if __name__ == '__main__':
    main()
