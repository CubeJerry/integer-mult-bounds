#!/usr/bin/env python3
"""Audit the actual cut locality and the finite data for the weighted gate.

The prior independent coefficient replays are authenticated, not replaced by
author summaries. New checks inspect every field's U projection, all native
root containments, the proper-direction cap, and outward movement intervals.
"""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path

PREFIX = Path('research/moonshot-005-program')
S020 = PREFIX / 'sessions/2026-11-17-S020'
NATIVE = PREFIX / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
GEO = S020 / 'checkpoint2-evidence/C/four-plane-review/check.py'
TARGETS = {14, 17, 19, 20, 96, 99, 101, 102}
U = sorted(set(range(8, 111)) - TARGETS)
PINS = {
    'native': '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
    'geometry': '41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
    'support': '012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963',
}
CASES = [
    ('scalar', 1,
     'repo', str(S020 / 'checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json'),
     'a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc',
     'C/pair-source-audit/output/SINGLE-CUT.json',
     'bb5046f18fadf7ae1f41a3f0012ec8c36b7beb353ae2ba7733a310253de2fa65',
     410, {1: 179, 2: 111, 3: 4, 4: 103, 7: 111}),
    ('two-copy-F4', 2, 'workers', 'A/two-copy-f4/output/WORD.json',
     '9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550',
     'C/two-copy-source-cut/output/INDEPENDENT-CUT.json',
     '5b105dab7c06497f26532d671f5c4f3d17d46ab32542d8f2a51bf82cd90fe336',
     812, {1: 326, 2: 238, 4: 206, 7: 222}),
    ('three-copy-F8', 3, 'workers', 'A/three-copy-f8/output/WORD.json',
     '9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6',
     'C/pair-source-audit/output/TRIPLE-CUT.json',
     'fcbc94d829fc340ae8e38f86a175838299c21892aae2ae25a957a547af07e5d9',
     1218, {1: 489, 2: 357, 4: 309, 7: 333}),
]


def load_pinned(path, expected):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == expected, f'hash: {path}'
    return json.loads(data)


def binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            k = row.bit_length() - 1
            if k in pivots:
                row ^= pivots[k]
            else:
                pivots[k] = row
                break
    return len(pivots)


def report_interval(iv):
    with localcontext() as ctx:
        ctx.prec = 60
        return {'rational': [str(x) for x in iv],
                'decimal': [str(Decimal(x.numerator) / Decimal(x.denominator)) for x in iv]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--workers', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    roots = load_pinned(args.repo / NATIVE, PINS['native'])['native_roots']
    assert sha256((args.repo / GEO).read_bytes()).hexdigest() == PINS['geometry']
    spec = importlib.util.spec_from_file_location('pinned_fraction_geometry', args.repo / GEO)
    geo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geo)
    support = load_pinned(args.workers / 'C/induced95-rigidity/FULL-SUPPORT-CERTIFICATE.json', PINS['support'])
    assert sorted(map(int, support['canonical_vectors'])) == U
    proper = sorted(w['binary_code_mask'] for w in support['all_nonzero_words']
                    if w['real_support_rank'] == 7)
    assert len(proper) == 25
    assert all(mask.bit_count() % 2 == 1 for mask in proper)
    triples = list(combinations(proper, 3))
    assert len(triples) == 2300
    assert all(binary_rank(t) == 3 for t in triples), 'proper directions contain no dependent triple'
    # A shortened canonical word in a real chart of rank <=6 is zero. In rank7
    # its scalar shortening has dimension at most1: the25 proper normals differ.
    normals = [tuple(w['annihilator_basis'][0]) for w in support['all_nonzero_words']
               if w['real_support_rank'] == 7]
    assert len({geo.basis((n,)) for n in normals}) == 25
    gate = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        gate[1 + 7*j] = gate.get(1 + 7*j, 0) + 74
        gate[7*j] = gate.get(7*j, 0) - 74
    caller = tuple(x / 6 for x in geo.moment(gate))
    reports, all_fields = [], {}
    for name, b, owner, word_name, word_hash, cut_name, cut_hash, field_count, expected_profile in CASES:
        word_path = (args.repo if owner == 'repo' else args.workers) / word_name
        word = load_pinned(word_path, word_hash)
        cut = load_pinned(args.workers / cut_name, cut_hash)
        assert len(cut) == field_count
        charts = {n: geo.chart(s) for n, s in word['charts'].items()}
        # Recompute movement invoice and every cut location from the full word.
        def public_name(c, kind, i):
            return (f'C{c}__' if b > 1 else '') + f'{kind}{i}'
        positions = {public_name(c, k, i): (f'L{i}' if k == 'X' else 'zero')
                     for c in range(b) for k in ['X', 'Y'] for i in range(111)}
        profile, actual_cut_positions = Counter(), None
        for index, operation in enumerate(word['operations']):
            if index == word['carrier_interface_before_operation']:
                actual_cut_positions = positions.copy()
            op, field, *rest = operation
            if op == 'INIT':
                positions[field] = rest[0]
            elif op == 'MOVE':
                gap = abs(len(charts[positions[field]]) - len(charts[rest[0]]))
                assert gap > 0
                profile[gap] += 1
                positions[field] = rest[0]
            elif op == 'CLEAR':
                del positions[field]
            else:
                assert op == 'ADD'
        assert dict(profile) == expected_profile
        assert actual_cut_positions == {f['name']: f['chart'] for f in cut}
        field_reports = []
        memberships = 0
        for field in cut:
            row = int(field['row_hex'], 16)
            assert 0 <= row < 1 << (222*b)
            chart = charts[field['chart']]
            assert len(chart) == field['rank']
            roles = [i for i in U if any((row >> (222*c + i)) & 1 for c in range(b))]
            leaks = [i for i in roles if not geo.contained(geo.basis((tuple(roots[i]),)), chart)]
            assert not leaks, f"geometric U-support leak in {field['name']}: {leaks}"
            memberships += len(roles)
            field_reports.append({'field': field['name'], 'chart': field['chart'],
                                  'rank': len(chart), 'projected_U_support': roles,
                                  'all_support_roots_contained': True})
        q = tuple(x / b for x in geo.moment(dict(profile)))
        room = caller[0] - q[1], caller[1] - q[0]
        threshold = geo.moment({4: 9*b, 1: 8*b})
        # At most one low exterior descent: m=1 never improves the threshold;
        # m>=2 contributes (m+1)[3] rather than m[4], m<=b+1.
        delta = geo.moment({3: b+2, 4: -(b+1)})
        if delta[0] >= 0:
            one_profile = {4: 9*b, 1: 8*b}
        else:
            assert delta[1] < 0
            one_profile = {4: 8*b-1, 3: b+2, 1: 8*b}
        one = tuple(x / b for x in geo.moment(one_profile))
        deficit = one[0] - room[1], one[1] - room[0]
        assert deficit[0] > 0, 'strict exclusion at current caller ceiling'
        report = {
            'source': name, 'copies': b, 'word_sha256': word_hash,
            'cut_sha256': cut_hash, 'cut': word['carrier_interface_before_operation'],
            'all_original_columns': 222*b, 'all_live_fields': len(cut),
            'projected_root_memberships_checked': memberships,
            'geometric_U_support_leaks': 0,
            'field_rank_histogram': dict(sorted(Counter(f['rank'] for f in cut).items())),
            'source_movement_profile': dict(profile),
            'normalized_source_moment': report_interval(q),
            'normalized_room': report_interval(room),
            'zero_low_exterior_extra_profile': {4: 9*b, 1: 8*b},
            'zero_low_exterior_normalized_bill': report_interval(tuple(x/b for x in threshold)),
            'maximum_low_origin_events_with_one_low_exterior': b+1,
            'one_low_exterior_best_lower_profile': one_profile,
            'at_most_one_low_exterior_normalized_bill': report_interval(one),
            'strict_normalized_deficit': report_interval(deficit),
        }
        reports.append(report)
        all_fields[name] = field_reports
    result = {
        'status': 'PASS_SCOPED_WEIGHTED_FORMATION_DELIVERY_GATE',
        'pins': PINS, 'remaining95_roles': U,
        'independent_proper_triples_checked': len(triples),
        'all_proper_masks_have_odd_weight': True,
        'proper_direction_set': proper,
        'all_proper_normal_lines_distinct': True,
        'caller_ceiling_per_copy': report_interval(caller),
        'sources': reports,
        'scope': 'Characteristic-two linear continuations; exactly9b D_U downward events; at most one exterior downward event with destination rank<=4. Arbitrary recoding, whole-record width V, cross-bank matrices, owned paid turns, and arbitrary exterior descents to rank>=5 remain allowed. Private arrivals are positive MOVEs of either direction. No unrestricted formation tariff.',
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    (args.out / 'ALL-FIELD-LOCALITY.json').write_text(json.dumps(all_fields, indent=2) + '\n')
    print(result['status'])
    for r in reports:
        print(r['source'], 'fields', r['all_live_fields'], 'leaks', r['geometric_U_support_leaks'],
              'bill', r['at_most_one_low_exterior_normalized_bill']['decimal'][0],
              'deficit', r['strict_normalized_deficit']['decimal'][0])


if __name__ == '__main__':
    main()
