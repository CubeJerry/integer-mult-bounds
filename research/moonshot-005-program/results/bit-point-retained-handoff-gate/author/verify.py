#!/usr/bin/env python3
"""Exact native premises for the point-retained continuation theorem.

No builder or predecessor checker is imported. This finite calculation supplies
the native facts used in PROOF.md; it is not the universal proof by itself.
Credit @CubeJerry and native/programme predecessors; OpenAI assistance.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

NATIVE_PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
GOOD20 = [0, 9, 15, 16, 17, 20, 29, 36, 37, 44, 46, 47,
          50, 54, 60, 63, 65, 70, 77, 83, 90, 92, 107, 109]
BANK1 = [12, 48, 77, 84, 91, 99]
BANK2 = [13, 47, 80, 87, 88, 96]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def basis(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return list(pivots.values())


def rational_rank(rows):
    rows = [[Fraction(v) for v in row] for row in rows]
    at = 0
    for column in range(8):
        pivot = next((j for j in range(at, len(rows)) if rows[j][column]), None)
        if pivot is None:
            continue
        rows[at], rows[pivot] = rows[pivot], rows[at]
        scale = rows[at][column]
        rows[at] = [v/scale for v in rows[at]]
        for j in range(len(rows)):
            if j != at:
                scale = rows[j][column]
                rows[j] = [v-scale*w for v, w in zip(rows[j], rows[at])]
        at += 1
        if at == len(rows):
            break
    return at


def indices(mask):
    return [j for j in range(111) if mask >> j & 1]


def main(args):
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == NATIVE_PIN, 'native bytes changed')
    native = json.loads(gzip.decompress(raw))
    roots = []
    for i in range(111):
        frame = native['frames'][str(native['start'][i])]
        need(frame['dim'] == 1 and len(frame['B']) == 1, 'source is not a line')
        roots.append([Fraction(x) for x in frame['B'][0]])
    for i in range(111):
        for j in range(i):
            need(rational_rank([roots[i], roots[j]]) == 2, 'duplicate source line')
        facet = native['frames'][str(native['final'][111+i])]
        frows = [[Fraction(x) for x in row] for row in facet['B']]
        need(facet['dim'] == 7 and rational_rank(frows) == 7,
             'receiver facet rank')
        need(all(dot(roots[i], row) == 0 for row in frows), 'wrong receiver facet')
    full = (1 << 111)-1
    K = [sum(1 << j for j in range(111)
             if j == i or dot(roots[i], roots[j]) == 0) for i in range(111)]
    cbasis = basis(K)
    need(len(cbasis) == 9, 'canonical code rank')
    words = [0]
    for row in cbasis:
        words += [w ^ row for w in words]
    need(len(set(words)) == 512, 'code enumeration')
    S = [row ^ (1 << i) for i, row in enumerate(K)]
    records = []
    for i in range(111):
        noncontact = full ^ K[i]
        admissible = [w for w in words if w and not (w >> i & 1)]
        need(len(admissible) == 255, 'diagonal-zero subcode dimension')
        witness = min(admissible, key=lambda w: ((w & noncontact).bit_count(), w))
        rho = (witness & noncontact).bit_count()
        partner = min((h for h in range(111) if h != i),
                      key=lambda h: ((S[i] & ~S[h]).bit_count(), h))
        gap = (S[i] & ~S[partner]).bit_count()-1
        records.append(dict(receiver=i, rho=rho, gap=gap,
                            distance_witness_hex=hex(witness),
                            distance_support=indices(witness & noncontact),
                            worst_partner=partner,
                            partner_difference=indices(S[i] & ~S[partner])))
    rho_census = dict(sorted(Counter(r['rho'] for r in records).items()))
    gap_census = dict(sorted(Counter(r['gap'] for r in records).items()))
    need(rho_census == {18: 7, 19: 24, 20: 52, 21: 16, 22: 11, 23: 1},
         'punctured distance census')
    need(gap_census == {20: 4, 21: 26, 22: 47, 23: 25, 24: 8, 25: 1},
         'one-point suffix gap census')
    good = [r['receiver'] for r in records if min(r['rho'], r['gap']) >= 21]
    need(good == GOOD20 and len(good) > 20, 'twenty-port pigeonhole witness')
    need(min(s.bit_count() for s in S) == 55, 'no-interaction gap')
    # The strict distance bound has a real failure control at its boundary.
    ctrl = min(records, key=lambda r: (r['rho'], r['receiver']))
    tmask = sum(1 << j for j in ctrl['distance_support'])
    witness = int(ctrl['distance_witness_hex'], 16)
    i = ctrl['receiver']
    need(witness and not (witness >> i & 1) and not (witness & (full ^ K[i]) & ~tmask),
         'distance boundary control')
    need((K[i] ^ witness) != K[i] and ((K[i] ^ witness) >> i & 1),
         'noncanonical difference remains at distance boundary')
    # A proper mixed bank is not a single line cache: it can contain two inputs.
    pair_receiver = 0
    j, k = indices(S[pair_receiver])[:2]
    need(j != k and rational_rank([roots[j], roots[k]]) == 2,
         'two incomparable source lines')
    need(dot(roots[pair_receiver], roots[j]) == dot(roots[pair_receiver], roots[k]) == 0,
         'mixed rank-two bank lies in receiver facet')
    T0 = sorted({0, *BANK1, *BANK2})
    need(len(T0) == 13, 'two-bank supported innovation size')
    need(rational_rank([roots[j] for j in BANK1]) == 3 and
         rational_rank([roots[j] for j in BANK2]) == 3, 'two candidate bank ranks')
    need(all(dot(roots[i], roots[j]) == 0 for i in BANK1 for j in BANK2),
         'bank planes orthogonal')
    out = dict(
        status='PASS_NATIVE_POINT_RETAINED_TWENTY_PORT_GATE_PREMISES',
        native_sha256=NATIVE_PIN, code_rank=9,
        canonical_basis_hex=[hex(v) for v in cbasis],
        codewords=512, rho_histogram=rho_census, gap_histogram=gap_census,
        good_receivers=good, universal_supported_innovation_limit=20,
        point_retained_local_read_capacity=1,
        no_incoming_interaction_missing_contacts=54,
        rows=records,
        controls={
            'strict_distance_boundary': ctrl,
            'mixed_bank_outside_point_interface':
                dict(receiver=pair_receiver, source_indices=[j, k], bank_rank=2,
                     explanation='One mixed rank-two bank read may expose both inputs; two stationary line reads cannot lie on one upward chain.'),
            'public_turn_outside_monotone_interface':
                dict(source_indices=[j, k], ranks=[0, 1, 0, 1],
                     explanation='The 1-to-0 move permits two incomparable point visits and violates monotonicity.'),
        },
        conditional_bank_application={
            'T0': T0, 'size': 13, 'arbitrary_additional_coordinate_directions_excluded': 7,
            'source_status': 'WIP not admitted by this theorem or checker',
        },
        scope='Finite native premises only; the all-field/all-width chronological theorem is proved in PROOF.md. Monotone public receivers; point-only local reads; all other actual X histories in C plus supported innovations. No new kappa.',
        complete_supplier=False, new_kappa=False,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: out[k] for k in ('status', 'rho_histogram', 'gap_histogram',
                                         'good_receivers', 'universal_supported_innovation_limit')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args())
