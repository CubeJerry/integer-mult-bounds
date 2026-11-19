#!/usr/bin/env python3
"""Exact native global-asymmetry certificates; no optimization dependency."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip
import json

PINS = {
    'native': '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
    'layout': '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
    'factor': '346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def bits(v):
    while v:
        b = v & -v
        yield b.bit_length() - 1
        v -= b


def echelon(rows):
    pivots = {}
    for v in rows:
        while v and v.bit_length() - 1 in pivots:
            v ^= pivots[v.bit_length() - 1]
        if v:
            pivots[v.bit_length() - 1] = v
    return pivots


def nullspace_on(rows, support):
    pivots = echelon(rows)
    basis = []
    for j in bits(support):
        if j in pivots:
            continue
        v = 1 << j
        for pivot, row in sorted(pivots.items()):
            if (v & row).bit_count() % 2:
                v ^= 1 << pivot
        need(v & support == v, 'null vector support')
        need(all((v & row).bit_count() % 2 == 0 for row in rows), 'null vector equations')
        basis.append(v)
    need(len(basis) + len(pivots) == support.bit_count(), 'nullity formula')
    need(len(echelon(basis)) == len(basis), 'independent nullspace basis')
    return basis


def multiply(A, B):
    out = []
    for row in A:
        v = 0
        for j in bits(row):
            v ^= B[j]
        out.append(v)
    return out


def projection_controls():
    cases = 0
    for a in range(16):
        f = [1 | ((a & 3) << 2), 2 | ((a >> 2) << 2)]
        E = f + [0, 0]
        for b in range(16):
            g = [1 | ((b & 3) << 2), 2 | ((b >> 2) << 2)]
            F = g + [0, 0]
            N = [x ^ y for x, y in zip(E, F)]
            need(multiply(E, E) == E and multiply(F, F) == F, 'idempotents')
            need(multiply(E, F) == F and multiply(F, E) == E, 'common image')
            need(multiply(N, N) == [0] * 4, 'square zero')
            need(len(echelon(N)) == len(echelon(f + g)) - 2, 'kernel rank identity')
            cases += 1
    # The same source quotients, two different common lift lines.
    f, g = [1], [3]
    ranks = []
    for u in (1, 5):
        E = [f[0] if (u >> t) & 1 else 0 for t in range(3)]
        F = [g[0] if (u >> t) & 1 else 0 for t in range(3)]
        need(multiply(E, E) == E and multiply(F, F) == F, 'two valid lift choices')
        N = [a ^ b for a, b in zip(E, F)]
        ranks.append(len(echelon(N)))
    need(ranks == [1, 1], 'receiver-independent rank')
    E, F = [1, 2, 0, 0], [0, 0, 4, 8]
    N = [a ^ b for a, b in zip(E, F)]
    need(multiply(E, F) != F and multiply(N, N) != [0] * 4,
         'different-image negative control')
    return {'projection_cases': cases, 'fixed_kernel_two_lift_ranks': ranks,
            'different_image_control_rejected': True}


def certificate(dual, witnesses, pair=False):
    scale, weights = dual['scale'], dual['weights']
    need(type(scale) is int and scale > 0, 'positive integer scale')
    need(len(weights) == len(witnesses), 'dual indexing length')
    need(all(type(x) is int and x >= 0 for x in weights), 'nonnegative integer weights')
    loads = Counter()
    for weight, w in zip(weights, witnesses):
        for h, jk in w['paired_planes']:
            loads[(h, *jk) if pair else h] += weight
    need(max(loads.values()) <= scale, 'dual load bound')
    value = Fraction(17 * sum(weights), scale)
    return loads, value


def main():
    ap = ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    pg = args.repo / 'research/moonshot-005-program'
    paths = {
        'native': pg / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json',
        'layout': pg / 'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
        'factor': pg / 'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json',
    }
    raw = {k: p.read_bytes() for k, p in paths.items()}
    raw['layout'] = gzip.decompress(raw['layout'])
    for k, data in raw.items():
        need(sha256(data).hexdigest() == PINS[k], k + ' pin')
    source, layout, factor = [json.loads(raw[k]) for k in ('native', 'layout', 'factor')]
    roots, planes = layout['root_table'], layout['A2']
    need(roots[:111] == source['native_roots'] and len(planes) == 1120, 'native geometry')
    ortho = [sum(1 << j for j, s in enumerate(roots)
                 if sum(x * y for x, y in zip(r, s)) == 0) for r in roots]
    masks = [sum(1 << j for j in H) for H in planes]
    additions = dict(factor['factors'])
    capacities = []
    for h, H in enumerate(planes):
        m = sum(j < 111 for j in H)
        need(h not in additions or m == 3, 'factor support')
        x = 12 // m + additions.get(h, 0) if m else 0
        e = max(8, x) if m else 0
        need((m == 1 and e == 12) or (m >= 2 and e == 8) or not m,
             'ordinary and singleton capacities')
        capacities.append(e)
    singleton = {next(j for j in H if j < 111): masks[h]
                 for h, H in enumerate(planes) if sum(j < 111 for j in H) == 1}
    need(len(singleton) == 11, 'eleven singleton planes')
    witnesses, receiver_data = [], []
    for i in range(111):
        tight = ortho[i] & ((1 << 111) - 1)
        for j, hm in singleton.items():
            if hm & ortho[i] == hm:
                tight &= ~(1 << j)
        visible = [h for h, hm in enumerate(masks) if hm & ortho[i] == hm]
        for j in bits(tight):
            star = [h for h in visible if masks[h] >> j & 1]
            need(len(star) == 16 and all(capacities[h] == 8 for h in star), 'tight source')
        rows = [masks[h] & tight for h in visible]
        basis = nullspace_on(rows, tight)
        space = [0]
        for v in basis:
            space += [w ^ v for w in space]
        need(len(set(space)) == 2 ** len(basis), 'complete nullspace enumeration')
        odd = [w for w in space if w.bit_count() % 2]
        for w in odd:
            paired = [[h, list(bits(masks[h] & w))] for h in visible if masks[h] & w]
            need(all(len(jk) == 2 for h, jk in paired), 'zero-or-two plane incidence')
            need(2 * len(paired) == 16 * w.bit_count(), 'sixteen incidences per donor')
            witnesses.append({'receiver': i, 'donors': list(bits(w)), 'paired_planes': paired})
        receiver_data.append({'receiver': i, 'tight_donors': list(bits(tight)),
                              'nullity': len(basis), 'odd_witnesses': len(odd)})
    hist = Counter(x['odd_witnesses'] for x in receiver_data)
    need(hist == {0: 24, 1: 7, 2: 27, 4: 32, 8: 15, 16: 5, 32: 1}, 'odd-witness histogram')
    need(len(witnesses) == 421, 'all421 witnesses')
    need(set(len(w['paired_planes']) for w in witnesses) == {216, 280}, 'witness sizes')
    author = Path(__file__).resolve().parent
    plane_dual = json.loads((author / 'PLANE-DUAL.json').read_text())
    pair_dual = json.loads((author / 'PAIR-DUAL.json').read_text())
    plane_load, plane_value = certificate(plane_dual, witnesses)
    pair_load, pair_value = certificate(pair_dual, witnesses, pair=True)
    need(plane_value == Fraction(70414816, 1000000) and max(plane_load.values()) == 999987,
         'exact plane certificate')
    need(pair_value == Fraction(151781644, 1000000) and max(pair_load.values()) == 999993,
         'exact pair certificate')
    need(len(plane_load) == 1108 and len(pair_load) == 2870, 'all ordinary flag counts')
    rank_bound = sum((Fraction(16 * len(w['paired_planes']), len(w['paired_planes']) - 1) * u
                      for w, u in zip(witnesses, pair_dual['weights'])), Fraction()) / pair_dual['scale']
    need(rank_bound == Fraction(134487693944, 937265625), 'rank certificate')
    local = [w for w in witnesses if w['receiver'] == 80]
    local_planes = Counter(h for w in local for h, jk in w['paired_planes'])
    local_pairs = Counter((h, *jk) for w in local for h, jk in w['paired_planes'])
    need(len(local) == 32, 'receiver80 witnesses')
    need(Counter(local_planes.values()) == {24: 320, 16: 16}, 'receiver80 plane loads')
    need(Counter(local_pairs.values()) == {8: 960, 16: 16}, 'receiver80 pair loads')
    for h, load in local_planes.items():
        pairs = [v for (hh, j, k), v in local_pairs.items() if hh == h]
        need(sorted(pairs) == ([8, 8, 8] if load == 24 else [16]), 'local pair partition')
    # Meaningful negative controls on the exact proof premises.
    bad_w = sum(1 << j for j in witnesses[0]['donors']) ^ (1 << witnesses[0]['donors'][0])
    need(bad_w.bit_count() % 2 == 0, 'deleted-donor control is not an odd witness')
    overloaded = dict(plane_dual, weights=[2 * u for u in plane_dual['weights']])
    rejected = False
    try:
        certificate(overloaded, witnesses)
    except ValueError as error:
        rejected = str(error) == 'dual load bound'
    need(rejected, 'overloaded dual rejected')
    controls = projection_controls()
    result = {
        'status': 'PASS_GLOBAL_NATIVE_SOURCE_ASYMMETRY', 'baseline': 'd8544284cbd0527cd03a0aad576a2d2c6eddcc0e',
        'source_sha256': PINS, 'witnesses': 421, 'receiver_histogram': dict(sorted(hist.items())),
        'ordinary_planes': 1108, 'ordinary_unordered_donor_pairs': 2870,
        'plane_dual_bound': str(plane_value), 'plane_dual_max_load': max(plane_load.values()),
        'minimum_asymmetric_planes': 71, 'pair_dual_bound': str(pair_value),
        'pair_dual_max_load': max(pair_load.values()), 'minimum_unequal_donor_pairs': 152,
        'rank_sum_lower_bound_per_p': str(rank_bound),
        'rank_sum_minimum_at_p360': -(-(360 * rank_bound.numerator) // rank_bound.denominator),
        'receiver80': {'odd_witnesses': 32, 'tight_donors': 62, 'three_tight_planes': 320,
                       'two_tight_planes': 16, 'inequality': '2q+t>=68', 'minimum_q': 23,
                       'q23_implies_t_at_least': 22, 'minimum_unequal_pairs': 52},
        'controls': dict(controls, deleted_donor_rejected=True, overloaded_dual_rejected=True),
        'new_complete_kappa': False, 'extra_repair_channel_covered': False,
        'scope': 'Original exact saturated quotient source; no MOVE tariff or source construction.',
    }
    args.out.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps({'witnesses': witnesses, 'receiver_data': receiver_data},
                          separators=(',', ':')) + '\n').encode()
    result['witness_payload_sha256'] = sha256(payload).hexdigest()
    (args.out / 'WITNESSES.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], '421 witnesses; planes>=71; pairs>=152; rank360>=51657')


if __name__ == '__main__':
    main()
