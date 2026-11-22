#!/usr/bin/env python3
"""Independent reverse-DAG and complete-boundary audit of S032 cut witnesses.

No author construction, target evaluator, cut finder or solver is imported.
@CubeJerry with OpenAI assistance. Apache-2.0.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json


def need(ok, label):
    if not ok:
        raise ValueError(label)


def add(to, row, scale):
    for k, v in row.items():
        value = to.get(k, 0) + scale*v
        if value:
            to[k] = value
        else:
            to.pop(k, None)


def expand(slot, forms, schedule):
    weights = {slot: Q(1)}
    for e in reversed(schedule):
        value = weights.pop(e, 0)
        if value:
            add(weights, forms[e], value)
    need(all(k < 0 for k in weights), 'all final dependencies are original inputs')
    return {~k: v for k, v in weights.items()}


def binary_key(frame):
    basis = {}
    for vector in frame:
        while vector:
            bit = vector.bit_length()-1
            if bit in basis:
                vector ^= basis[bit]
            else:
                basis[bit] = vector
                break
    for bit in sorted(basis):
        for larger in basis:
            if larger > bit and (basis[larger] >> bit) & 1:
                basis[larger] ^= basis[bit]
    return tuple(basis[k] for k in sorted(basis, reverse=True))


def main():
    ap = ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    base = args.repo/'research/moonshot-005-program/results'
    for path, expected in json.loads((Path(__file__).parent/'SOURCE-PINS.json').read_text())['files'].items():
        need(sha256((args.repo/path).read_bytes()).hexdigest() == expected, 'pinned input '+path)
    source = base/'complex-native-funded-donor-cuts/inputs/DOUBLE-CANDIDATE.json.gz'
    raw = gzip.decompress(source.read_bytes())
    need(sha256(raw).hexdigest() == '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48', 'source payload')
    word = json.loads(raw)
    old = {e: {j: Q(v) for j, v in row} for e, row in word['forms']}
    forms = {e: row.copy() for e, row in old.items()}
    schedule = [e for e in word['schedule'] if e != 95914]
    del forms[95914]
    moves = {e: (u, v) for e, u, v in word['moves'] if e != 95914}
    moves.update({94019: (3, 278), 90369: (3, 304), 88: (278, 127)})
    observer = max(schedule)+1
    schedule.insert(schedule.index(90369)+1, observer)
    moves[observer] = (3, 282)
    forms[94019] = {~1288: Q(1)}
    forms[90369] = old[94019].copy()
    forms[88] = {**old[95914], 94019: Q(-845660160)}
    forms[observer] = old[90369].copy()
    for e in schedule:
        if e in (94019, 90369, 88, observer):
            continue
        if 94019 in forms[e]:
            forms[e][90369] = forms[e].pop(94019)
        if 90369 in old[e]:
            forms[e][observer] = forms[e].pop(90369)
    need(len(moves) == 5707, 'all paid routes retained')
    aliases = [binary_key(f) for f in word['frames']]
    need(len(set(aliases)) == 1102, 'physical chart identities')
    witness_path = base/'complex-source-hub-s032/CUTS.json'
    cuts = json.loads(witness_path.read_text())
    deleted = set(cuts['deleted'])
    need(deleted == {86, 89777, 97232, 97241, 97320, 97323, 99064}, 'seven deletions')
    pair_path = base/'complex-paid-export-s031-coupled-repair/endpoint-screen/EXPECTED-SURVIVORS.json'
    pairs = json.loads(pair_path.read_text())['pairs']
    need(len(pairs) == len({tuple(map(tuple, p)) for p in pairs}) == 120, 'predecessor survivors')
    receipts = []
    coverage = set()
    for cut in cuts['cuts']:
        charts = set(cut['raw_charts'])
        physical = {aliases[c] for c in charts}
        need(charts == {j for j, key in enumerate(aliases) if key in physical}, 'no split physical alias')
        axes, slots = cut['input_axes'], cut['terminal_slots']
        need(all(word['initial'][a] in charts for a in axes), 'source side')
        need(all(word['final'][s-word['first_output']] not in charts for s in slots), 'target side')
        minor = []
        for slot in slots:
            target = expand(slot, old, word['schedule'])
            need(expand(slot, forms, schedule) == target, 'actual compensation preserves each audited endpoint')
            minor.append([target.get(a, 0) for a in axes])
        identity = [[Q(i == j) for j in range(len(axes))] for i in range(len(axes))]
        need(minor == identity, 'independent exact identity minor')
        full = sorted(e for e, (u, v) in moves.items() if u in charts and v not in charts)
        retained = [e for e in full if e not in deleted]
        need(retained == cut['old_exports'], 'complete retained boundary')
        capacities = [len(retained)+sum(u in charts and v not in charts for u, v in p) for p in pairs]
        rejected = [i for i, c in enumerate(capacities) if c < len(axes)]
        need(rejected == cut['rejected_pair_indices'], 'all pair coverage rebuilt')
        coverage.update(rejected)
        receipts.append(dict(id=cut['id'], target_rank=len(axes), full_boundary=full,
                             retained_boundary=retained, rejected_pairs=len(rejected),
                             capacity_histogram=dict(Counter(capacities))))
    need(coverage == set(range(120)), 'every prior survivor excluded')
    need(receipts[2]['rejected_pairs'] == 120, 'third cut alone suffices')
    previous = json.loads((base/'complex-paid-export-s031-coupled-repair/root-review/output/RESULT.json').read_text())
    need(previous['remaining_pairs'] == 120 and previous['all_directed_grade_one_routes'] == 4802, 'retained exhaustive screen')
    need(Q(previous['exact_allowance'][1]) < Q('2.125014706818'), 'outward inherited allowance')
    lower, upper = Q('1.993080525655735'), Q('1.993080525655736')
    need(lower**200 < 2**199 < upper**200, 'independent integer-power tariff check')
    deficit = 1+lower-Q('2.125014706818')
    need(deficit == Q('0.868065818837735'), 'strict inherited allowance comparison')
    result = dict(status='PASS_INDEPENDENT_S032_COMPLEX_CUT_AUDIT',
                  imported_author_code=False, method='reverse DAG over exact rational coefficients; binary reduced chart bases; all retained routes',
                  cuts=receipts, prior_survivors_checked=120, all_excluded=True,
                  strict_moment_deficit_lower=str(deficit),
                  predecessor_exhaustiveness_and_allowance='source-bound earlier independent admission reused',
                  new_kappa=False)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], '2,2,4 identity demands; third cut rejects all120')


if __name__ == '__main__':
    main()
