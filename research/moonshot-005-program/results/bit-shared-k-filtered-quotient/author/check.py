#!/usr/bin/env python3
"""Exact native K donor-cut and three-receiver filtered-quotient checks.

No author verifier is imported. The all-width statement is in PROOF.md.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path

LAYOUT_SHA = '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
ROUTES_SHA = '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'


def need(condition, label):
    if not condition:
        raise ValueError(label)


def row_basis(rows):
    pivots = {}
    for row in rows:
        x = row
        for p in sorted(pivots, reverse=True):
            if x >> p & 1:
                x ^= pivots[p]
        if x:
            p = x.bit_length() - 1
            for q in list(pivots):
                if pivots[q] >> p & 1:
                    pivots[q] ^= x
            pivots[p] = x
    return tuple(pivots[p] for p in sorted(pivots, reverse=True))


def rank(rows):
    return len(row_basis(rows))


def combine(A, rows):
    result = []
    for a in A:
        value = 0
        for j, row in enumerate(rows):
            if a >> j & 1:
                value ^= row
        result.append(value)
    return result


def finite_controls():
    # Three receivers use invertible but distinct coordinates on the same
    # two-dimensional incoming donor quotient, respecting a one-dimensional
    # early subspace. Every nonzero shear is accounted for explicitly.
    incoming = [1, 2]
    outputs = [incoming, [1, 3], [1, 2]]
    need(all(row_basis(x) == row_basis(incoming) for x in outputs), 'positive common quotient')
    need(all(row_basis(x[:1]) == (1,) for x in outputs), 'positive common early flag')
    independent_full_rank = [1, 4]
    need(rank(independent_full_rank) == 2, 'rank-only mutant retains full individual rank')
    need(rank(incoming + independent_full_rank) == 3, 'rank-only mutant exceeds common input cut')
    late_before_early = [2, 1]
    need(row_basis(late_before_early) == row_basis(incoming), 'causal mutant retains total quotient')
    need(row_basis(late_before_early[:1]) != row_basis(incoming[:1]), 'causal mutant rejected')
    extra_capacity = [1, 2, 4]
    need(rank(extra_capacity) == 3 and rank(extra_capacity + independent_full_rank) == 3,
         'changed-capacity escape is outside saturated premise')
    invertible_two = []
    for a in range(1, 4):
        for b in range(1, 4):
            if rank([a, b]) == 2:
                invertible_two.append([a, b])
    for change in invertible_two:
        need(row_basis(combine(change, incoming)) == row_basis(incoming), 'basis invariance')
        need(rank(combine(change, independent_full_rank) + incoming) == 3,
             'basis change cannot repair incompatible donor quotient')
    return {'positive_receivers': 3, 'invertible_binary_basis_changes': len(invertible_two),
            'rank_only_failure_joint_rank': 3, 'causal_failure_preserves_total_rank': 2,
            'extra_capacity_escape_rank': 3}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    base = args.repo / 'research/moonshot-005-program/results'
    lp = base / 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    rp = base / 'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    raw_l, raw_r = gzip.decompress(lp.read_bytes()), gzip.decompress(rp.read_bytes())
    need(hashlib.sha256(raw_l).hexdigest() == LAYOUT_SHA, 'layout payload pin')
    need(hashlib.sha256(raw_r).hexdigest() == ROUTES_SHA, 'route payload pin')
    layout = json.loads(raw_l)
    routes = [json.loads(line) for line in raw_r.splitlines()]
    H = list(map(frozenset, layout['A2']))
    D = list(map(frozenset, layout['D4']))
    dual = layout['dual_D4']
    roots = layout['root_table']
    native = set(range(111))
    need(len(routes) == 106560 and len(H) == 1120 and len(D) == 3150, 'native sizes')

    def orthogonal(i, j):
        return sum(x*y for x, y in zip(roots[i], roots[j])) == 0

    source = {k: frozenset(j for j in native if all(orthogonal(j, i) for i in K))
              for k, K in enumerate(H)}
    incident_D = {k: tuple(d for d in range(len(D)) if K <= D[dual[d]])
                  for k, K in enumerate(H)}
    input_counts = Counter()
    output_counts = Counter()
    for row in routes:
        phase, j, c, h, d, k, line, terminal = row
        if k is None:
            continue
        need(k in range(len(H)) and d in incident_D[k], 'actual D-K route incidence')
        input_counts[d, k, phase] += 1
        receiver = terminal if phase == 'X' else j
        output_counts[k, receiver, phase] += 1
    flag_counts = Counter(input_counts[d, k, 'X'] + input_counts[d, k, 'Y']
                          for k in incident_D for d in incident_D[k])
    need(flag_counts == {2: 50400}, 'every complete D-K flag has two actual fields')

    cut_counts = {}
    for i in native:
        ks = [k for k, K in enumerate(H) if i in K]
        for j in native:
            if not orthogonal(i, j):
                continue
            cut_counts[i, j] = sum(output_counts[k, i, 'X'] + output_counts[k, i, 'Y']
                                   for k in ks if j in source[k])
    tight_receivers = sorted(i for i in native
                            if all(n == 480 for (receiver, _), n in cut_counts.items() if receiver == i))
    need(len(tight_receivers) == 100, 'one hundred globally tight native receivers')

    all_donor_count = Counter()
    common_group_histogram = Counter()
    for k, K in enumerate(H):
        need(len(incident_D[k]) == 45, 'forty-five incoming D flags at every K')
        for j in source[k]:
            ds = [d for d in incident_D[k] if j in D[d]]
            total = sum(input_counts[d, k, 'X'] + input_counts[d, k, 'Y'] for d in ds)
            need(len(ds) == 15 and total == 30, 'tight native donor input cut at K')
            all_donor_count[len(K & native)] += 1
            eligible = [i for i in K & native if cut_counts[i, j] == 480
                        and output_counts[k, i, 'X'] + output_counts[k, i, 'Y'] == 30]
            common_group_histogram[len(eligible)] += 1

    k = 370
    need(H[k] == {1, 73, 80} and len(source[k]) == 36, 'actual K370')
    need(all(i in tight_receivers for i in H[k]), 'all three K370 receivers tight')
    need(all(output_counts[k, i, 'X'] == output_counts[k, i, 'Y'] == 15 for i in H[k]),
         'K370 receiver early-late quotas')
    details = []
    for j in sorted(source[k]):
        ds = [d for d in incident_D[k] if j in D[d]]
        early = sum(input_counts[d, k, 'X'] for d in ds)
        late = sum(input_counts[d, k, 'Y'] for d in ds)
        need(early == late == 15, 'K370 donor early-late quotas')
        need(all(input_counts[d, k, 'X'] == input_counts[d, k, 'Y'] == 1 for d in ds),
             'K370 each donor D flag split one plus one')
        details.append({'donor': j, 'D_charts': ds, 'early': early, 'late': late,
                        'receiver_total_cuts': {str(i): cut_counts[i, j] for i in sorted(H[k])}})

    # The previously retained packet's five missing donors remain visible.
    retained = json.loads((base / 'bit-native-common-frame-k-stitch/saturation-review/output/RESULT.json').read_text())
    need(set(retained['missing_donors']) == {15, 69, 70, 92, 107} <= source[k],
         'retained sparse packet fails current native donor cut')
    result = {'status': 'PASS_NATIVE_THREE_RECEIVER_K_QUOTIENT_GATE',
              'scope': 'necessary common total/early quotients; no constructed middle word or new kappa',
              'field_scope': 'every field for linear proper codes; every positive owner body width',
              'native_incoming_flags': dict(flag_counts),
              'native_K_donor_pairs_by_receiver_count': dict(all_donor_count),
              'eligible_common_quotient_group_histogram': dict(common_group_histogram),
              'globally_tight_receivers': tight_receivers,
              'K370': {'receivers': sorted(H[k]), 'native_donors': sorted(source[k]),
                       'incoming_flags': len(incident_D[k]), 'incoming_fields': 90,
                       'fields_per_donor': 30, 'early_fields_per_donor': 15,
                       'complete_receiver_quotient_rank': '30s', 'early_receiver_quotient_rank': '15s',
                       'full_D_packet_rank_per_native_donor': '2s', 'details': details},
              'controls': finite_controls(),
              'source_pins': [{'path': str(p.relative_to(args.repo)),
                              'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                             for p in [lp, rp, base / 'bit-native-common-frame-k-stitch/author/SATURATION.md',
                                       base / 'bit-middle-information-factorization/author/PROOF.md']],
              'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'])
    print(json.dumps({'K370': {'donors': 36, 'receivers': 3, 'total_rank': '30s', 'early_rank': '15s'},
                      'global_groups': dict(common_group_histogram), 'controls': result['controls']}, sort_keys=True))


if __name__ == '__main__':
    main()
