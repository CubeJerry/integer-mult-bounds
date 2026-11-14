#!/usr/bin/env python3
"""Finite exact premises for PROOF.md; not a universal-theorem prover."""
import argparse
import gzip
import hashlib
import json
import random
from fractions import Fraction as F
from pathlib import Path

NATIVE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rank(rows, p):
    a = [list(row) for row in rows]
    if not a:
        return 0
    need(all(len(row) == len(a[0]) for row in a), 'rectangular matrix')
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = pow(a[r][c] % p, -1, p)
        a[r] = [x * z % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c] % p:
                z = a[i][c]
                a[i] = [(x-z*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def binary_basis(rows):
    b, chosen = {}, []
    for index, row in enumerate(rows):
        while row:
            p = row.bit_length()-1
            if p in b:
                row ^= b[p]
            else:
                b[p] = row
                chosen.append(index)
                break
    return b, chosen


def binary_rank(rows):
    return len(binary_basis(rows)[0])


def contains(row, b):
    while row:
        p = row.bit_length()-1
        if p not in b:
            return False
        row ^= b[p]
    return True


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def fails(function, name):
    try:
        function()
    except ValueError:
        return name
    raise ValueError('negative control accepted: ' + name)


def actual(raw):
    need(hashlib.sha256(raw).hexdigest() == NATIVE, 'native exact bytes')
    source = json.loads(gzip.decompress(raw))
    frames = {int(k): v for k, v in source['frames'].items()}
    roots = [list(map(F, frames[source['start'][i]]['B'][0])) for i in range(111)]
    for i, root in enumerate(roots):
        need(frames[source['start'][i]]['dim'] == 1, 'original X born on line')
        need(frames[source['final'][i]]['dim'] == 8, 'original X ends at Hub')
        need(frames[source['start'][111+i]]['dim'] == 0, 'arbitrary original Y born at ground')
        facet = frames[source['final'][111+i]]
        need(facet['dim'] == 7, 'original Y terminal facet')
        need(all(dot(root, list(map(F, row))) == 0 for row in facet['B']), 'actual facet perpendicular')
    for i in range(8):
        need(all((root != 0) == (j == i) for j, root in enumerate(roots[i])), 'actual coordinate order')
    need(len({source['final'][111+i] for i in range(111)}) == 111, 'distinct terminal facets')
    k = [sum(int(i == j or dot(a, b) == 0) << j for j, b in enumerate(roots))
         for i, a in enumerate(roots)]
    local = [row ^ 255 for row in k[:8]]
    h = [row ^ (1 << i) for i, row in enumerate(k[:8])]
    for i in range(8):
        need(local[i] != 0, 'each local demand has positive rank')
        need(all(dot(roots[i], roots[j]) == 0 for j in range(111) if local[i] >> j & 1), 'L_i actual proper support')
        need(all(dot(roots[i], roots[j]) == 0 for j in range(111) if h[i] >> j & 1), 'H_i actual proper support')
        need(h[i] == local[i] ^ (255 ^ (1 << i)), 'mixed local identity')
    inside = [i for i, root in enumerate(roots) if root[0] == root[1] == 0]
    mask = sum(1 << i for i in inside)
    common = local[0] & mask
    need(len(inside) == 28, 'pair inside X count')
    need(common == local[1] & mask, 'identical pair inside demand')
    need(common.bit_count() == 22 and common & 255 == 0, 'common22 noncoordinate inputs')
    need(binary_rank(local) == 4, 'eight pure rows joint rank4')
    need(binary_rank(k[:8]) == 4, 'coordinate K rank4')
    need(binary_rank(h) == 8, 'masked x rank8')
    mix = k[:8] + h
    need(binary_rank(mix) == 12, 'combined historical x rank12')
    need(binary_rank(k[:2] + h[:2]) == 4, 'two exchanges historical x rank4')
    # Unknown-y masks make all eight demands independent on the FULL input.
    masked = [h[i] ^ (1 << (111+i)) for i in range(8)]
    need(binary_rank(masked) == 8, 'independent unknown-y masked demands')
    # Each noncoordinate port has a noncontact with exactly the same mix column.
    pairs = []
    for i in range(8, 111):
        supp = tuple(j for j, v in enumerate(roots[i]) if v)
        need(len(supp) == 4, 'four-coordinate noncoordinate root')
        possible = [j for j in range(8, 111) if j != i
                    and tuple(a for a, v in enumerate(roots[j]) if v) == supp
                    and dot(roots[i], roots[j]) != 0]
        need(possible, 'actual noncontact same-support partner')
        j = min(possible)
        need(not (k[i] >> j & 1), 'separating partner is forbidden fitting column')
        need(all((row >> i & 1) == (row >> j & 1) for row in mix), 'identical mix columns')
        pairs.append({'receiver': i, 'noncontact': j, 'real_support': list(supp)})
    # A separate exact restriction elimination confirms the same complete list.
    fits = []
    all_columns = (1 << 111)-1
    for i in range(111):
        forbidden = all_columns ^ (k[i] ^ (1 << i))
        if contains(1 << i, binary_basis([row & forbidden for row in mix])[0]):
            fits.append(i)
    need(fits == list(range(8)), 'exact mix fitted ports')
    exchanges = []
    for i in range(8):
        y_in = (1 << (111+i)) ^ h[i]
        p_in = k[i]
        y_out = y_in ^ p_in
        p_out = p_in ^ y_out
        need(y_out == (1 << (111+i)) ^ (1 << i), 'arbitrary-Y endpoint')
        need(p_out == y_in, 'packet through block zero')
        need(p_out >> (111+i) & 1, 'outgoing history retains unknown Y')
        exchanges.append({'port': i, 'incoming_packet': hex(p_in), 'Y_input': hex(y_in),
                          'Y_output': hex(y_out), 'packet_output': hex(p_out)})
    controls = []
    controls.append(fails(lambda: actual(raw+b' '), 'native source byte alteration'))
    # These controls use the full symbolic 222-column equality.
    i = 0
    need_y = (1 << 111) ^ 1
    controls.append(fails(lambda: need(h[i] ^ k[i] == need_y, 'zero-Y mutant endpoint'), 'silently zeroed original Y'))
    controls.append(fails(lambda: need(k[i] == masked[i], 'missing second ADD'), 'omitted packet reload ADD'))
    controls.append(fails(lambda: need(binary_rank([row & ((1 << 111)-1) for row in masked]) == 8
                                     and all(row >> (111+i) & 1 for i, row in enumerate([z & ((1 << 111)-1) for z in masked])),
                                     'all original Y columns retained'), 'omitted independent Y columns'))
    relations = [bits for bits in range(1, 256)
                 if not xor(local[i] for i in range(8) if bits >> i & 1)]
    need(len(relations) == 15, 'four-dimensional demand relation kernel')
    return {
        'facets': source['final'][111:119],
        'pair_cut': {'inside_X': inside, 'inside_Y_count': 111, 'baseline_outward_records': 139,
                     'common_X': [i for i in range(111) if common >> i & 1], 'extra_capacity_in_units_of_V': 1},
        'eight_cut': {'baseline_outward_records': 222, 'demand_rows': [hex(z) for z in local],
                      'basis_indices': binary_basis(local)[1], 'joint_rank': 4,
                      'nonzero_relation_masks': relations, 'extra_capacity_in_units_of_V': 4},
        'mixed_history': {'K_rank': 4, 'H_rank': 8, 'combined_rank': 12,
                          'basis_indices_in_K_then_H': binary_basis(mix)[1],
                          'pair_rank': 4, 'masked_full_input_rank': 8,
                          'admitted_fitting_receivers': fits, 'excluded_receiver_witnesses': pairs},
        'symbolic_exchanges': exchanges, 'controls': controls}


def xor(values):
    out = 0
    for value in values:
        out ^= value
    return out


def cut_check(a, n, groups, demands, p):
    need(all(len(row) == n for row in a), 'input width retained')
    need(rank(a, p) == n, 'full input cut rank')
    flat = [j for group in groups for j in group]
    need(len(flat) == len(set(flat)), 'disjoint recipient arms')
    need(all(0 <= j < len(a) for j in flat), 'valid transfer row index')
    for group, demand in zip(groups, demands):
        rows = [a[j] for j in group]
        need(rank(rows+demand, p) == rank(rows, p), 'actual demand available on arm')
    delta = sum(rank(d, p) for d in demands)-rank([row for d in demands for row in d], p)
    need(delta <= len(a)-n, 'cut redundancy inequality')
    return delta


def cut_examples():
    rng = random.Random(20261114)
    counts, max_delta = {}, 0
    for p in (2, 3, 5):
        count = 0
        for n in range(1, 8):
            for extra in range(4):
                m = n+extra
                for sample in range(5):
                    while True:
                        a = [[rng.randrange(p) for _ in range(n)] for _ in range(m)]
                        if rank(a, p) == n:
                            break
                    groups = [[j for j in range(m) if j % 3 == t] for t in range(3)]
                    demands = []
                    for group in groups:
                        rows = []
                        for _ in group:
                            coeff = [rng.randrange(p) for j in group]
                            rows.append([sum(c*a[j][column] for c, j in zip(coeff, group)) % p
                                         for column in range(n)])
                        demands.append(rows)
                    delta = cut_check(a, n, groups, demands, p)
                    max_delta = max(max_delta, delta)
                    count += 1
        counts[str(p)] = count
    sharp = cut_check([[1, 0], [1, 0], [0, 1]], 2, [[0], [1]], [[[1, 0]], [[1, 0]]], 2)
    need(sharp == 1, 'sharp duplicate demand example')
    masked = cut_check([[1, 1, 0], [1, 0, 1], [1, 0, 0]], 3,
                       [[0], [1]], [[[1, 1, 0]], [[1, 0, 1]]], 2)
    need(masked == 0, 'masked duplicate demand escape')
    controls = [
        fails(lambda: cut_check([[1]], 1, [[0], [0]], [[[1]], [[1]]], 2), 'one shared outward row falsely called disjoint'),
        fails(lambda: cut_check([[1, 0], [1, 0]], 2, [[0], [1]], [[[1, 0]], [[1, 0]]], 2), 'missing restored input direction'),
        fails(lambda: cut_check([[1, 0], [0, 1]], 2, [[0], [1]], [[[1, 0]], [[1, 0]]], 2), 'unavailable duplicate pure demand')]
    return {'random_full_rank_cases_by_field': counts, 'maximum_tested_demand_redundancy': max_delta,
            'sharp_extra_scalar_capacity': sharp, 'masked_extra_scalar_capacity': masked,
            'negative_controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    source = actual(args.native.read_bytes())
    examples = cut_examples()
    result = {'status': 'PASS_REVERSIBLE_MULTICAST_CUT_FINITE_PREMISES', 'native_sha256': NATIVE,
              'source': source, 'abstract_examples': examples,
              'universal_proof': 'PROOF.md Sections1-3; finite examples do not prove it',
              'complete_source': False, 'new_kappa': None}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'all_eight_extra_crossings': 4,
                      'pair_extra_crossings': 1, 'mixed_history_rank': 12,
                      'noncoordinate_exclusions': len(source['mixed_history']['excluded_receiver_witnesses']),
                      'finite_field_cases': sum(examples['random_full_rank_cases_by_field'].values())}))


if __name__ == '__main__':
    main()
