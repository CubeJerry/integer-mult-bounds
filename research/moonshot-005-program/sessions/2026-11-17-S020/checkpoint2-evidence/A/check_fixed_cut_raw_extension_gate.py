"""Independent finite checks for root's fixed-quartet-cut raw-export gate.

This checks code restrictions and cut facts, not source replay (reviewed by root).
It imports no programme algebra or moment helper.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def rank(rows):
    rows = list(rows)
    pos = 0
    for col in range(111):
        pivot = next((j for j in range(pos, len(rows)) if rows[j] & (1 << col)), None)
        if pivot is None:
            continue
        rows[pos], rows[pivot] = rows[pivot], rows[pos]
        for j in range(pos + 1, len(rows)):
            if rows[j] & (1 << col):
                rows[j] ^= rows[pos]
        pos += 1
    return pos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', type=Path, default=HERE)
    parser.add_argument('--out', type=Path, default=HERE)
    args = parser.parse_args()
    inputs = args.inputs
    args.out.mkdir(parents=True, exist_ok=True)
    raw = (inputs / 'SOURCE-RECOVERY.json').read_bytes()
    assert sha256(raw).hexdigest() == SOURCE_SHA
    roots = json.loads(raw)['native_roots']
    full = (1 << 111) - 1
    foreign = [sum(1 << j for j, s in enumerate(roots)
                   if sum(a * b for a, b in zip(r, s)) == 0) for r in roots]
    canonical = [v | (1 << i) for i, v in enumerate(foreign)]
    basis = []
    for row in canonical:
        if rank(basis + [row]) > len(basis):
            basis.append(row)
    assert len(basis) == 9
    words = [0]
    for b in basis:
        words += [v ^ b for v in words]
    assert len(set(words)) == 512
    local = []
    for i in range(111):
        forbidden = full ^ foreign[i] ^ (1 << i)
        restrictions = [w & forbidden for w in words]
        kernel = [w for w, r in zip(words, restrictions) if r == 0]
        assert sorted(kernel) == sorted([0, canonical[i]])
        distance = min(r.bit_count() for r in restrictions if r)
        assert distance >= 18
        assert rank([b & forbidden for b in basis]) == 8
        local.append({'receiver': i, 'foreign_degree': foreign[i].bit_count(),
                      'restricted_rank': 8, 'nonzero_restricted_distance': distance})
    assert min(x['foreign_degree'] for x in local) == 55

    cuts = []
    for name, cap in [('quartet-source-ground', 9), ('hierarchy-source-ground', 8)]:
        wpath = inputs / name / 'WORD.json'
        word = json.loads(wpath.read_text())
        inv = json.loads((inputs / name / 'CUT-INVENTORY.json').read_text())
        result = json.loads((inputs / name / 'RESULT.json').read_text())
        assert sha256(wpath.read_bytes()).hexdigest() == inv['word_sha256'] == result['word_sha256']
        cut = word['carrier_interface_before_operation']
        assert cut == inv['cut_before_operation'] == result['source_cut']
        at = {f'X{i}': f'L{i}' for i in range(111)} | {f'Y{i}': 'zero' for i in range(111)}
        for op in word['operations'][:cut]:
            if op[0] in ('MOVE', 'INIT'):
                at[op[1]] = op[2]
            elif op[0] == 'CLEAR':
                del at[op[1]]
        assert all(at[f'Y{i}'] == 'zero' for i in range(111))
        low = [r for r in inv['fields'] if r['name'].startswith('X') and r['rank'] < 8]
        assert len(low) == 47 and all(r['rank'] in (3, 4) for r in low)
        assert all(op[2] not in {f'F{i}' for i in range(111)}
                   for op in word['operations'][:cut] if op[0] == 'MOVE' and op[1].startswith('X'))
        # All executed X charts are native rank1, half rank3, quartet rank4 or Hub.
        known_ranks = {'zero': 0, 'Hub': 8}
        known_ranks.update({f'L{i}': 1 for i in range(111)})
        for r in inv['fields']:
            known_ranks[r['chart']] = r['rank']
        assert all(known_ranks[op[2]] in (1, 3, 4, 8)
                   for op in word['operations'][:cut] if op[0] == 'MOVE' and op[1].startswith('X'))
        hi = Fraction(result['necessary_limiting_room']['rational'][1])
        lo = Fraction(result['necessary_limiting_room']['rational'][0])
        assert cap < lo <= hi < cap + 1
        lower = 111 - cap
        upper = 47 + cap
        assert lower > upper
        cuts.append({'name': name, 'word_sha256': inv['word_sha256'], 'cut': cut,
                     'held_originals': 47, 'Hub_originals': 64,
                     'future_owned_move_cap': cap, 'raw_coordinate_union_cap': cap,
                     'fitting_charge_lower_bound': lower, 'facet_charge_upper_bound': upper,
                     'contradiction_gap': lower - upper})
    out = {'status': 'PASS_INDEPENDENT_FIXED_CUT_RAW_COORDINATE_GATE_CHECKS',
           'source_sha256': SOURCE_SHA, 'canonical_rank': 9,
           'restricted_distance_histogram': dict(Counter(r['nonzero_restricted_distance'] for r in local)),
           'foreign_degree_histogram': dict(Counter(r['foreign_degree'] for r in local)),
           'receivers': local, 'cuts': cuts,
           'support17_extension': [dict(name=c['name'], common_coordinate_union_cap=17,
                fitting_charge_lower_bound=94, facet_charge_upper_bound=c['facet_charge_upper_bound'],
                contradiction_gap=94-c['facet_charge_upper_bound']) for c in cuts],
           'scope': 'All characteristic-two fields and whole widths under the reviewed linear monotone-public continuation, fixed executed prefix, complete caller, and added global-history space contained in canonical C plus coordinate space E_S with |S| <= the listed cap. No exclusion of general coded proper-chart payloads or earlier corrections.'}
    path = args.out / 'FIXED-CUT-RAW-EXTENSION-REVIEW.json'
    path.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'receivers'}, indent=2))


if __name__ == '__main__':
    main()
