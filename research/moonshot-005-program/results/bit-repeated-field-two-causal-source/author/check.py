#!/usr/bin/env python3
"""Exact causal inequalities and nonlinear controls for repeated field-width2."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import gzip
import json

PINS = {
    'native': '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
    'layout': '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
    'factor': '346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7',
    'color_review': '55062cf00045a9d8888fbea8cd613d9c8db65ef570381c282aa004e73d8aa0ae',
}


def need(value, message):
    if not value:
        raise ValueError(message)


def bits(v):
    while v:
        b = v & -v
        yield b.bit_length() - 1
        v -= b


def rank(rows):
    pivots = {}
    for v in rows:
        while v and v.bit_length() in pivots:
            v ^= pivots[v.bit_length()]
        if v:
            pivots[v.bit_length()] = v
    return len(pivots)


def entropy_controls():
    # A3-dimensional top with rank2 projection onto each of three donors.
    rows = [1 | (1 << 4), (1 << 1) | (1 << 2) | (1 << 5), 1 << 3]
    need(rank(rows) == 3, 'top rank')
    need(all(rank([v & (3 << (2 * j)) for v in rows]) == 2 for j in range(3)),
         'each top donor projection rank2')
    target = [sum(((row & x).bit_count() % 2) << k for k, row in enumerate(rows)) for x in range(64)]
    need(Counter(target) == {v: 8 for v in range(8)}, 'uniform top')
    hist, maximum_components, equality_cases = Counter(), 0, 0
    for functions in product(range(16), repeat=3):
        early = [sum(((functions[j] >> ((x >> (2 * j)) & 3)) & 1) << j for j in range(3))
                 for x in range(64)]
        parent = list(range(16))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for t, e in zip(target, early):
            a, b = find(t), find(8 + e)
            if a != b:
                parent[a] = b
        counts = Counter(find(t) for t in target)
        # H(common function)<=2 iff product(n_c**n_c)>=2**256 on64 inputs.
        integer_product = 1
        for n in counts.values():
            integer_product *= n ** n
        need(integer_product >= 2 ** 256, 'common-function entropy bound')
        equality_cases += int(integer_product == 2 ** 256)
        maximum_components = max(maximum_components, len(counts))
        hist[tuple(sorted(counts.values()))] += 1
    need(equality_cases > 0, 'entropy bound has a sharp finite control')
    # Choosing the full top as an early output improperly reads future data.
    early_zero = (0, 0, 0)
    x, y = 0, 2
    observed = lambda z: ((z >> 0) & 1, (z >> 3) & 1, (z >> 4) & 1)
    need(observed(x) == observed(y) == early_zero and target[x] != target[y],
         'future-dependent output is not an early-input function')
    return {'all_boolean_early_encoder_triples': 4096, 'integer_entropy_comparisons': True,
            'sharp_entropy_cases': equality_cases, 'maximum_common_components': maximum_components,
            'component_mass_histogram': [[list(k), v] for k, v in sorted(hist.items())],
            'future_input_causality_control_rejected': True}


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
        'color_review': pg / 'results/bit-stripe-varying-port-cut/review/output/RESULT.json.gz',
    }
    raw = {k: gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes()
           for k, p in paths.items()}
    for k, data in raw.items():
        need(sha256(data).hexdigest() == PINS[k], k + ' pin')
    native_source, layout, factor, old = [json.loads(raw[k]) for k in ('native', 'layout', 'factor', 'color_review')]
    roots, planes, mids = layout['root_table'], layout['A2'], layout['D4']
    need(roots[:111] == native_source['native_roots'], 'original native table')
    HM = [sum(1 << j for j in h) for h in planes]
    DM = [sum(1 << j for j in d) for d in mids]
    O = [sum(1 << j for j, s in enumerate(roots) if sum(a * b for a, b in zip(r, s)) == 0)
         for r in roots[:111]]
    mask = (1 << 111) - 1
    K = [(o & mask) ^ (1 << i) for i, o in enumerate(O)]
    need(rank(K) == 9, 'canonical rank9')
    for o in O:
        need(rank([k & (mask ^ (o & mask)) for k in K]) == 9, 'outside restriction')
    visible = [[i for i, o in enumerate(O) if hm & o == hm] for hm in HM]
    D_receivers = [sum(1 << i for i, o in enumerate(O) if dm & o == dm) for dm in DM]
    singleton = {next(j for j in h if j < 111): n for n, h in enumerate(planes)
                 if sum(j < 111 for j in h) == 1}
    fac = dict(factor['factors'])
    x_values = {h: 12 // len(list(bits(hm & mask))) + fac.get(h, 0)
                for h, hm in enumerate(HM) if hm & mask}
    need(all(45 * sum(x_values[h] for h, hm in enumerate(HM) if hm >> j & 1) == 5760
             for j in range(111)), 'actual early source bank size')
    old_records = {e['plane']: e for e in old['records']}
    margins, covered, uncovered, records = Counter(), 0, 0, []
    pair_count = 0
    for h, hm in enumerate(HM):
        donors = list(bits(hm & mask))
        m = len(donors)
        if m < 2:
            continue
        targets = [i for i in visible[h]
                   if all(j not in singleton or i not in visible[singleton[j]] for j in donors)]
        ports = [d for d, dm in enumerate(DM) if hm & dm == hm]
        need(len(ports) == 45, '45 actual exits')
        subsets = [sum(1 << v for v, d in enumerate(ports) if D_receivers[d] >> i & 1) for i in targets]
        need(all(s.bit_count() == 15 for s in subsets), '15 visible exits')
        for a, b in combinations(subsets, 2):
            need((a & b).bit_count() in (3, 6), 'nonempty base-pair overlap')
            pair_count += 1
        neighborhoods = [sum(1 << k for k, i in enumerate(targets) if D_receivers[d] >> i & 1)
                         for d in ports]
        u = neighborhoods.count(0)
        previous = old_records[h]
        need(previous['joint_tight_receivers'] == targets and previous['native_donors'] == donors,
             'same admitted color instance')
        need(previous['port_neighborhoods'] == sorted(set(neighborhoods) - {0})
             and previous['uncovered_ports'] == u, 'same covered ports')
        x = x_values[h]
        need((m == 3 and x in (4, 5, 6)) or (m == 2 and x == 6), 'early count cases')
        delta = 45 * (m - 1) * x - u * m * x - 180
        need(delta > 0, 'top cannot preserve actual early X entropy')
        alpha = previous['rank_cap']
        beta = alpha + 1 if alpha < m else 2 * m
        covered += beta
        uncovered += u
        margins[delta] += 1
        records.append({'H': h, 'm': m, 'x': x, 'u': u, 'top_early_deficit_at_r180': delta,
                        'alpha': alpha, 'field_star_capacity_per_r': beta})
    need(len(records) == 1108 and min(margins) == 30 and uncovered == 1436,
         'complete strict native causal census')
    need(covered == 2519, 'larger-field covered budget')
    capacity = Fraction(covered + 11 * 3) + Fraction(2 * uncovered, 15)
    deficit = 3264 - capacity
    need(capacity == Fraction(41152, 15) and deficit == Fraction(7808, 15), 'global field budget')
    control = entropy_controls()
    result = {
        'status': 'PASS_REPEATED_FIELD_TWO_CAUSAL_GATE', 'source_sha256': PINS,
        'ordinary_planes': 1108, 'receiver_pair_port_checks': pair_count,
        'early_top_deficit_histogram_at_r180': dict(sorted(margins.items())),
        'minimum_strict_early_top_deficit_at_r180': 30,
        'covered_capacity_per_r': covered, 'uncovered_ports': uncovered,
        'capacity_per_r': str(capacity), 'required_per_r': 3264, 'deficit_per_r': str(deficit),
        'r180': {'capacity': int(180 * capacity), 'required': 587520, 'deficit': int(180 * deficit)},
        'nonlinear_entropy_controls': control, 'field': 'every finite field of characteristic2',
        'identical_repetition_required': True, 'original_early_X_restoration_required': True,
        'extra_information_channel_or_changed_canonical_covered': False,
        'inherited_coloring_recomputed': False, 'new_complete_kappa': False,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(records, separators=(',', ':')) + '\n').encode()
    result['causal_census_sha256'] = sha256(payload).hexdigest()
    (args.out / 'CAUSAL-CENSUS.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], '493824 < 587520; deficit93696; every ordinary top excluded')


if __name__ == '__main__':
    main()
