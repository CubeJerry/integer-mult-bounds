#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check three exact route cuts; no search solver or numerical rank is used."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    if not rows:
        return 0
    height, width, pivot = len(rows), len(rows[0]), 0
    for j in range(width):
        k = next((k for k in range(pivot, height) if rows[k][j]), None)
        if k is None:
            continue
        rows[pivot], rows[k] = rows[k], rows[pivot]
        scale = rows[pivot][j]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for k in range(pivot + 1, height):
            scale = rows[k][j]
            if scale:
                rows[k] = [a - scale * b for a, b in zip(rows[k], rows[pivot])]
        pivot += 1
        if pivot == height:
            break
    return pivot


def span(frame):
    result = {0}
    for v in frame:
        result |= {v ^ x for x in result}
    return tuple(sorted(result))


def root_at(start):
    return next(p for p in [start, *start.parents] if (p / 'AGENTS.md').is_file())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = (args.repo or root_at(here)).resolve()
    for path, expected in json.loads((here / 'SOURCE-PINS.json').read_text())['files'].items():
        require(sha256((repo / path).read_bytes()).hexdigest() == expected, 'source changed: ' + path)
    res = repo / 'research/moonshot-005-program/results'
    source = res / 'complex-native-funded-donor-cuts/inputs/7833-construction.py'
    spec = importlib.util.spec_from_file_location('s031_native', source)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    graph = native.compensated(native.load_word(source.with_name('DOUBLE-CANDIDATE.json.gz')), True)
    values = native.all_public_rows(graph)
    predecessor = res / 'complex-paid-export-s031-coupled-repair'
    pairs = json.loads((predecessor / 'endpoint-screen/EXPECTED-SURVIVORS.json').read_text())['pairs']
    require(len(pairs) == 120 and len({tuple(map(tuple, p)) for p in pairs}) == 120, 'distinct predecessor pair census')
    witness = json.loads((here / 'CUTS.json').read_text())
    deleted = set(witness['deleted'])
    require(deleted == {86, 89777, 97232, 97241, 97320, 97323, 99064}, 'exact deletion inventory')
    require(len(graph.routes) == 5707, 'genuine paid compensation route count')
    frames = {c: span(f) for c, f in enumerate(graph.frames)}
    require(len(set(frames.values())) == 1102, 'physical bank census')
    for pair in pairs:
        for u, v in pair:
            require(graph.grade((u, v)) == 1, 'every old survivor has grade-one new routes')
    reports = []
    controls = []

    def verify_cut(cut):
        charts = set(cut['raw_charts'])
        selected = {frames[c] for c in charts}
        require(charts == {c for c, f in frames.items() if f in selected}, 'cut must contain every physical alias')
        inputs, outputs = cut['input_axes'], cut['terminal_slots']
        require(len(inputs) == len(set(inputs)) and len(outputs) == len(set(outputs)), 'minor labels distinct')
        require(all(graph.inputs[~j] in charts for j in inputs), 'minor inputs inside cut')
        require(all(graph.terminals[e] not in charts for e in outputs), 'minor outputs outside cut')
        matrix = [[Q(values[e][1].get(j, 0), values[e][0]) for j in inputs] for e in outputs]
        require(rank(matrix) == cut['rank'] == len(inputs) == len(outputs), 'exact nonzero full target minor')
        old = sorted(e for e, (u, v) in graph.routes.items() if e not in deleted and u in charts and v not in charts)
        require(old == cut['old_exports'], 'complete old cut boundary')
        full = sorted(e for e, (u, v) in graph.routes.items() if u in charts and v not in charts)
        require(len(full) >= cut['rank'], 'full paid positive control has enough cut capacity')
        bad, good = [], []
        capacities = []
        for i, pair in enumerate(pairs):
            cap = len(old) + sum(u in charts and v not in charts for u, v in pair)
            capacities.append(cap)
            (bad if cap < cut['rank'] else good).append(i)
        return dict(id=cut['id'], rank=cut['rank'], physical_banks=len(selected),
                    raw_chart_count=len(charts), input_axes=inputs, terminal_slots=outputs,
                    target_minor=[[str(v) for v in row] for row in matrix],
                    old_exports=old, full_paid_exports=full,
                    rejected_pair_indices=bad, passing_pair_indices=good,
                    capacity_histogram=dict(sorted(Counter(capacities).items())))

    for cut in witness['cuts']:
        report = verify_cut(cut)
        require(report['rejected_pair_indices'] == cut['rejected_pair_indices'], 'complete pair rejection list')
        reports.append(report)
        # A cut certificate with the old capacity understated must fail.
        forged = dict(cut, old_exports=cut['old_exports'][:-1])
        try:
            verify_cut(forged)
        except ValueError as error:
            require('boundary' in str(error), 'expected forged boundary rejection')
            controls.append('cut_' + cut['id'] + '_omitted_old_export_rejected')
        else:
            raise ValueError('forged cut boundary accepted')
        forged = dict(cut, input_axes=[cut['input_axes'][0]] * len(cut['input_axes']))
        try:
            verify_cut(forged)
        except ValueError as error:
            require('distinct' in str(error), 'expected duplicated minor rejection')
            controls.append('cut_' + cut['id'] + '_dependent_minor_rejected')
        else:
            raise ValueError('dependent target minor accepted')
    require(len(reports) == 3, 'three new cuts')
    coverage = set().union(*(set(r['rejected_pair_indices']) for r in reports))
    require(coverage == set(range(120)), 'every old survivor has a new exact cut obstruction')
    assigned, census = set(), []
    for r in reports:
        new = set(r['rejected_pair_indices']) - assigned
        census.append(len(new))
        assigned |= new
    require(census == [75, 36, 9], 'sequential survivor reduction')
    require(any(r['passing_pair_indices'] for r in reports), 'individual cuts do not falsely reject every pair')
    # Exact lower bound: lower^200 < 2^199 < upper^200.
    lower = Q(398616105131147, 200000000000000)
    upper = Q(249135065706967, 125000000000000)
    require(lower ** 200 < Q(2) ** 199 < upper ** 200, 'exact rational grade-two cost enclosure')
    allowance_upper = Q('2.125014706818')
    deficit = 1 + lower - allowance_upper
    require(deficit == Q('0.868065818837735') and deficit > 0, 'strict .005 repair deficit')
    result = dict(status='PASS_S032_ALL_120_COMPLEX_REPAIR_PAIRS_EXCLUDED',
                  scope='Exact seven deletions, genuine paid fifth observer, fixed remaining old route endpoints and original target roles. Arbitrary surviving local linear recoding, histories and causal retiming; every positive finite field width over characteristic zero.',
                  deleted=sorted(deleted), predecessor_pairs=120, cuts=reports,
                  sequential_new_rejections=census, survivors=[],
                  negative_controls=controls,
                  cost_lower_bound='1 + 2^(199/200)', grade_two_interval=[str(lower), str(upper)],
                  inherited_allowance_upper=str(allowance_upper), strict_deficit_lower=str(deficit),
                  previous_endpoint_screen='Independently admitted predecessor reused; this command rechecks all new minors, boundaries and all120 remaining pairs, not the complete earlier enumeration.',
                  new_kappa=False, whole_supplier=False)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], '75+36+9=120; no surviving affordable pair; deficit>0.868065818837735')


if __name__ == '__main__':
    main()
