#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Direct exact certificate replay for four price-preserving deletion profiles."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import argparse, importlib.util, json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def span(frame):
    result = {0}
    for x in frame:
        result |= {x ^ y for y in result}
    return tuple(sorted(result))


def exact_rank(rows):
    a = [list(map(Q, row)) for row in rows]
    height = len(a)
    if not height:
        return 0
    r = 0
    for j in range(len(a[0])):
        k = next((k for k in range(r, height) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        d = a[r][j]
        a[r] = [x / d for x in a[r]]
        for k in range(r + 1, height):
            d = a[k][j]
            if d:
                a[k] = [x - d * y for x, y in zip(a[k], a[r])]
        r += 1
        if r == height:
            break
    return r


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = args.repo.resolve()
    pins = json.loads((here / 'SOURCE-PINS.json').read_text())['files']
    for path, digest in pins.items():
        need(sha256((repo / path).read_bytes()).hexdigest() == digest, 'source changed: ' + path)
    source = repo / 'research/moonshot-005-program/results/complex-native-funded-donor-cuts/inputs/7833-construction.py'
    spec = importlib.util.spec_from_file_location('native', source)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    g = native.compensated(native.load_word(source.with_name('DOUBLE-CANDIDATE.json.gz')), True)
    values = native.all_public_rows(g)
    spaces = sorted({span(frame) for frame in g.frames})
    index = {s: i for i, s in enumerate(spaces)}
    canonical = {c: index[span(f)] for c, f in enumerate(g.frames)}
    need(len(spaces) == 1102, 'physical bank count')
    routes = {e: (canonical[u], canonical[v]) for e, (u, v) in g.routes.items()}
    grade_one = []
    for u, a in enumerate(spaces):
        for v, b in enumerate(spaces):
            if len(a) * 2 == len(b) and set(a) <= set(b) or len(b) * 2 == len(a) and set(b) <= set(a):
                grade_one.append((u, v))
    need(len(grade_one) == 4802, 'complete directed grade-one route inventory')
    reports = []
    control_count = 0
    for choice in [43, 89777, 96404, 96513]:
        certificate = json.loads((here / ('swap-' + str(choice)) / 'COMPACT-CUTS.json').read_text())
        deleted = {86, 97232, 97241, 97320, 97323, 99064, choice}
        need(sorted(deleted) == certificate['deleted'], 'exact deletion family')
        need(Counter(g.grade(g.routes[e]) for e in deleted) == {3: 1, 4: 5, 5: 1}, 'unchanged complete deletion price profile')
        cache = {}
        def verify_cut(cut):
            mask = int(cut['canonical_bank_mask'], 16)
            need(0 <= mask < 1 << len(spaces), 'bank mask range')
            inputs, outputs = cut['source_axes'], cut['terminal_slots']
            need(len(inputs) == len(set(inputs)) and len(outputs) == len(set(outputs)), 'distinct minor labels')
            need(all(mask >> canonical[g.inputs[~j]] & 1 for j in inputs), 'minor inputs inside')
            need(all(not (mask >> canonical[g.terminals[e]] & 1) for e in outputs), 'minor outputs outside')
            key = tuple(inputs), tuple(outputs)
            if key not in cache:
                matrix = [[Q(values[e][1].get(j, 0), values[e][0]) for j in inputs] for e in outputs]
                cache[key] = exact_rank(matrix)
            need(cache[key] == cut['rank'] == len(inputs) == len(outputs), 'exact full-rank target minor')
            boundary = sorted(e for e, (u, v) in routes.items() if e not in deleted and mask >> u & 1 and not (mask >> v & 1))
            need(boundary == cut['old_exports'], 'full surviving old boundary')
            return mask, len(boundary), cut['rank']
        initial = [verify_cut(c) for c in certificate['initial_cuts']]
        separating = [verify_cut(c) for c in certificate['separating_cuts']]
        need(len(initial) == 7 and initial[2][1:] == (4, 6), 'reclosed six-demand cut needs two new fields')
        # Direct geometry and cut capacity, not a reclosure computation.
        core_mask = initial[2][0]
        eligible = [(u, v) for u, v in grade_one if core_mask >> u & 1 and not (core_mask >> v & 1)]
        need(len(eligible) == certificate['initial_source_route_count'], 'eligible route census')
        cut_crossings = []
        for mask, capacity, demanded in initial + separating:
            bits = sum(bool(mask >> u & 1 and not (mask >> v & 1)) << i for i, (u, v) in enumerate(eligible))
            cut_crossings.append((bits, capacity, demanded))
        fixed = survivors = 0
        hit_count = Counter()
        for u, v in combinations_with_replacement(range(len(eligible)), 2):
            if any(cap + ((bits >> u) & 1) + ((bits >> v) & 1) < dem for bits, cap, dem in cut_crossings[:7]):
                continue
            fixed += 1
            for k, (bits, cap, dem) in enumerate(cut_crossings[7:]):
                if cap + ((bits >> u) & 1) + ((bits >> v) & 1) < dem:
                    hit_count[k] += 1
                    break
            else:
                survivors += 1
        need(fixed == certificate['fixed_pairs'] and fixed > 0, 'fixed-cut pair census and nontrivial cover')
        need(survivors == 0, 'every possible old-bank grade-one pair has an explicit cut obstruction')
        # Falsification: the first initial cut cannot understate the actual old boundary.
        c = certificate['initial_cuts'][2]
        forged = dict(c, old_exports=c['old_exports'][:-1])
        try:
            verify_cut(forged)
        except ValueError as error:
            need('boundary' in str(error), 'boundary-control reason')
            control_count += 1
        else:
            raise ValueError('forged boundary accepted')
        reports.append(dict(choice=choice, deleted=sorted(deleted),
                            eligible_grade_one_routes=len(eligible), fixed_cut_pairs=fixed,
                            explicit_separating_cuts=len(separating), survivors=survivors,
                            full_boundary_checks=len(initial) + len(separating),
                            distinct_exact_target_minors=len(cache),
                            rank_six_old_capacity=initial[2][1]))
        print('PROFILE', choice, fixed, 'pairs;', len(separating), 'exact cuts; survivors0', flush=True)
    price_receipt = json.loads((repo / 'research/moonshot-005-program/results/complex-paid-export-s031-coupled-repair/root-review/output/RESULT.json').read_text())
    allowance = [Q(v) for v in price_receipt['exact_allowance']]
    need(Q(2) < allowance[0] < allowance[1] < Q('2.125014706818'), 'authenticated inherited allowance enclosure')
    lower = Q('1.993080525655735')
    need(lower ** 200 < Q(2) ** 199, 'grade-two exact lower bound')
    need(1 + lower - Q('2.125014706818') == Q('0.868065818837735'), 'same strict price deficit')
    result = dict(status='PASS_S032_FOUR_PRICE_PRESERVING_TOPOLOGIES_EXCLUDED',
                  profiles=reports, directed_grade_one_routes=4802,
                  negative_controls=control_count,
                  common_extra_moment_deficit_strictly_greater_than='0.868065818837735',
                  closure_algorithm_or_optimizer_used=False,
                  new_kappa=False, complete_supplier=False)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], flush=True)


if __name__ == '__main__':
    main()
