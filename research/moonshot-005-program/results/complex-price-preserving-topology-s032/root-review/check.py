#!/usr/bin/env python3
"""Independent raw-DAG audit of four complete finite cut covers.

Reuses only generic helpers from root's earlier independent audit.
Imports no author constructor, target evaluator, cut finder or optimizer.
@CubeJerry with OpenAI assistance. Apache-2.0.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import gzip
import importlib.util
import json


def determinant(rows):
    """Exact determinant by fraction-free elimination, with pivoting."""
    a = [list(map(Q, row)) for row in rows]
    n = len(a)
    if n == 0:
        return Q(1)
    sign, previous = 1, Q(1)
    for i in range(n - 1):
        pivot = next((k for k in range(i, n) if a[k][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            sign = -sign
        p = a[i][i]
        for k in range(i + 1, n):
            for j in range(i + 1, n):
                a[k][j] = (p*a[k][j] - a[k][i]*a[i][j])/previous
            a[k][i] = Q(0)
        previous = p
    return sign*a[-1][-1]


def elements(basis):
    values = [0]
    for x in basis:
        values += [x ^ y for y in values]
    return tuple(sorted(values))


def load_graph(base):
    helper = base/'complex-source-hub-s032/root-review/check.py'
    spec = importlib.util.spec_from_file_location('prior_root_helpers', helper)
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    raw = gzip.decompress((base/'complex-native-funded-donor-cuts/inputs/DOUBLE-CANDIDATE.json.gz').read_bytes())
    h.need(sha256(raw).hexdigest() == '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48', 'raw source')
    w = json.loads(raw)
    old = {e: {j: Q(v) for j, v in row} for e, row in w['forms']}
    forms = {e: row.copy() for e, row in old.items() if e != 95914}
    schedule = [e for e in w['schedule'] if e != 95914]
    routes = {e: (u, v) for e, u, v in w['moves'] if e != 95914}
    routes.update({94019: (3, 278), 90369: (3, 304), 88: (278, 127)})
    observer = max(schedule) + 1
    schedule.insert(schedule.index(90369) + 1, observer)
    routes[observer] = (3, 282)
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
    h.need(len(routes) == 5707, 'all paid routes')
    raw_keys = [h.binary_key(f) for f in w['frames']]
    ordered = sorted((elements(k), k) for k in set(raw_keys))
    keys = [k for _, k in ordered]
    spaces = [set(s) for s, _ in ordered]
    index = {k: i for i, k in enumerate(keys)}
    canonical = [index[k] for k in raw_keys]
    h.need(len(keys) == 1102, 'physical bank aliases')
    edges = {e: (canonical[u], canonical[v]) for e, (u, v) in routes.items()}
    allowed = []
    for u in range(len(keys)):
        for v in range(u + 1, len(keys)):
            if abs(len(keys[u]) - len(keys[v])) == 1 and (spaces[u] < spaces[v] or spaces[v] < spaces[u]):
                allowed.extend(((u, v), (v, u)))
    h.need(len(allowed) == 4802, 'complete directed grade-one inventory')
    cache = {}
    def row(slot):
        if slot not in cache:
            target = h.expand(slot, old, w['schedule'])
            h.need(h.expand(slot, forms, schedule) == target, 'compensation preserves audited target')
            cache[slot] = target
        return cache[slot]
    return h, w, keys, routes, canonical, edges, allowed, row, cache


def main():
    ap = ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    base = args.repo/'research/moonshot-005-program/results'
    pins = json.loads((here/'SOURCE-PINS.json').read_text())['files']
    for path, digest in pins.items():
        if sha256((args.repo/path).read_bytes()).hexdigest() != digest:
            raise ValueError('source pin '+path)
    h, w, keys, routes, canonical, edges, allowed, row, target_cache = load_graph(base)
    reports, minor_cache = [], {}
    expected = {43: (432, 13944, 279), 89777: (424, 8471, 295),
                96404: (420, 2211, 219), 96513: (432, 1140, 6)}
    for choice, counts in expected.items():
        cert = json.loads((here.parent/f'swap-{choice}/COMPACT-CUTS.json').read_text())
        deleted = {86, 97232, 97241, 97320, 97323, 99064, choice}
        h.need(sorted(deleted) == cert['deleted'], 'exact deletion set')
        grades = Counter(abs(len(keys[edges[e][0]]) - len(keys[edges[e][1]])) for e in deleted)
        h.need(grades == {3: 1, 4: 5, 5: 1}, 'exact price profile')
        def verify(c):
            mask = int(c['canonical_bank_mask'], 16)
            h.need(0 <= mask < 1 << len(keys), 'mask range')
            axes, slots = c['source_axes'], c['terminal_slots']
            n = c['rank']
            h.need(len(axes) == len(set(axes)) == len(slots) == len(set(slots)) == n and n > 0, 'minor shape')
            h.need(all(mask >> canonical[w['initial'][a]] & 1 for a in axes), 'sources inside')
            h.need(all(not (mask >> canonical[w['final'][s-w['first_output']]] & 1) for s in slots), 'terminals outside')
            key = tuple(axes), tuple(slots)
            if key not in minor_cache:
                minor_cache[key] = determinant([[row(s).get(a, 0) for a in axes] for s in slots])
            h.need(minor_cache[key] != 0, 'nonzero exact determinant')
            full = sorted(e for e, (u, v) in edges.items() if mask >> u & 1 and not (mask >> v & 1))
            retained = [e for e in full if e not in deleted]
            h.need(retained == c['old_exports'], 'complete boundary')
            h.need(len(full) >= n, 'unmodified paid word satisfies cut')
            return mask, len(retained), n
        initial = [verify(c) for c in cert['initial_cuts']]
        extra = [verify(c) for c in cert['separating_cuts']]
        h.need(len(initial) == 7 and initial[2][1:] == (4, 6), 'fresh six-demand cut')
        core = initial[2][0]
        eligible = [(u, v) for u, v in allowed if core >> u & 1 and not (core >> v & 1)]
        crossings = []
        for mask, capacity, rank in initial + extra:
            bits = sum(int(bool(mask >> u & 1 and not (mask >> v & 1))) << i for i, (u, v) in enumerate(eligible))
            crossings.append((bits, capacity, rank))
        passed, uncovered = 0, []
        for i, j in combinations_with_replacement(range(len(eligible)), 2):
            def deficient(c):
                bits, capacity, rank = c
                return capacity + ((bits >> i) & 1) + ((bits >> j) & 1) < rank
            if any(deficient(c) for c in crossings[:7]):
                continue
            passed += 1
            if not any(deficient(c) for c in crossings[7:]):
                uncovered.append((i, j))
        h.need((len(eligible), passed, len(extra)) == counts, 'independent exact census')
        h.need(len(eligible) == cert['initial_source_route_count'] and passed == cert['fixed_pairs'], 'certificate census')
        h.need(not uncovered, 'complete finite cover')
        forged = dict(cert['initial_cuts'][2], old_exports=cert['initial_cuts'][2]['old_exports'][:-1])
        try:
            verify(forged)
        except ValueError as error:
            h.need(str(error) == 'complete boundary', 'forged-boundary control reason')
        else:
            raise ValueError('forged boundary accepted')
        reports.append(dict(choice=choice, eligible_routes=len(eligible), pairs_after_initial=passed,
                            separating_cuts=len(extra), full_boundary_checks=len(initial)+len(extra), survivors=0))
        print('PROFILE', choice, passed, 'pairs; zero survivors', flush=True)
    price = json.loads((base/'complex-paid-export-s031-coupled-repair/root-review/output/RESULT.json').read_text())
    h.need(Q(2) < Q(price['exact_allowance'][0]) < Q(price['exact_allowance'][1]) < Q('2.125014706818'), 'inherited exact allowance')
    low, high = Q('1.993080525655735'), Q('1.993080525655736')
    h.need(low**200 < 2**199 < high**200, 'exact integer-power grade-two bound')
    h.need(1+low-Q('2.125014706818') == Q('0.868065818837735'), 'strict price deficit')
    h.need(sum(r['full_boundary_checks'] for r in reports) == 827, 'complete cut count')
    result = dict(status='PASS_INDEPENDENT_FOUR_PROFILE_CUT_COVER', profiles=reports,
                  directed_grade_one_routes=len(allowed), exact_target_rows=len(target_cache),
                  distinct_nonzero_minors=len(minor_cache), complete_boundary_checks=827,
                  forged_boundary_controls=4, original_paid_cut_controls=827,
                  author_executable_imported=False, closure_or_optimizer_used=False,
                  inherited_120_pair_list_used=False,
                  reused='root earlier generic reverse-DAG and binary-RREF helpers; pinned prior allowance',
                  strict_moment_deficit_lower='0.868065818837735', new_kappa=False)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], flush=True)


if __name__ == '__main__':
    main()
