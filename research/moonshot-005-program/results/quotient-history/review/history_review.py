#!/usr/bin/env python3
"""Independent adjoint, metadata and scalar-mode audit of history reductions."""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
from reverse_review import reverse, need, add, PIN

def row(x):
    return {int(k): F(v) for k, v in x.items()}

def span(vectors):
    s = {0}
    for v in vectors:
        s |= {a ^ v for a in tuple(s)}
    return frozenset(s)

def run(source, packet, reverse_rows, budget):
    raw = source.read_bytes(); need(hashlib.sha256(raw).hexdigest() == PIN, 'source pin')
    w = json.loads(gzip.decompress(raw)); program = w['program']; N = w['public']
    M = set(w['live']) | {r + 112 for r in w['live']} | set(w['hosted']['X2']) | set(w['hosted']['Y2'])
    spans = [span(x) for x in w['frames']]
    E = {r for r in M if len(spans[w['initial'][r]]) == 1}
    c = json.loads((packet / 'CERTIFICATE.json').read_text())
    rr = json.loads(reverse_rows.read_text())
    for r in rr:
        need(row(r['full_q_row']) == row(c['source_target_rows'][str(r['event'])]), 'independent full target equality')
    wants = {}; observation_rows = {}; used = []
    for h in c['history_reductions']:
        for name, case in h['cases'].items():
            if case['status'] != 'MEMBER':
                continue
            total = row(case['entry_residual'])
            need(set(total) <= E, 'entry-only residual')
            for term in case['terms']:
                o = term['observation']; k = (o['event'], o['role'])
                need(o['event'] < h['event'], 'strict earlier phase')
                need(spans[o['chart']] == spans[h['destination']], 'canonical destination span')
                need(o['role'] >= N or (name == 'owned_main' and o['role'] in M), 'history grammar')
                if k not in observation_rows:
                    full = reverse(program, o['event'] + 1, o['role'])
                    observation_rows[k] = {i: a for i, a in full.items() if i in M}
                need(observation_rows[k] == row(o['row']), 'reverse observation row')
                for i, a in observation_rows[k].items():
                    add(total, i, F(term['coefficient']) * a)
                wants.setdefault(o['event'], []).append(o)
                used.append((h['event'], name, k))
            need(total == row(c['source_target_rows'][str(h['event'])]), 'full positive identity')
    size = N + w['owned_fields']; charts = list(w['initial']) + [None] * w['owned_fields']
    versions = [-1] * size; birth = [None] * size; move = [None] * size
    values = [F(int(i in (0, 20))) for i in range(size)]
    target_event = 37606; B = spans[529]; seen = set(); history = []
    def record(i, r):
        if i >= target_event or charts[r] is None or not (r in M or r >= N) or spans[charts[r]] != B:
            return
        need(values[r] == 0, 'all earlier owned/main history annihilated by psi')
        k = (r, versions[r], birth[r])
        if k in seen:
            return
        seen.add(k)
        full = reverse(program, i + 1, r)
        qrow = {j: a for j, a in full.items() if j in M}
        if qrow:
            history.append((i, r, qrow))
    for r in M:
        record(-1, r)
    ledger = {(x['use_event'], x['owner']): x for x in c['current_owned_observer_ledger']}
    for i, e in enumerate(program):
        op, r = e[:2]
        if i == target_event:
            need(r == 1511 and values[r] == 4, 'target psi response')
        for (event, owner), x in ledger.items():
            if event == i:
                need((birth[owner], versions[owner], move[owner], charts[owner]) == (x['birth'], x['value_version'], x['last_move'], x['current_chart']), 'owned observer provenance')
        if op == 'ADD':
            values[r] += F(e[3]) * values[e[2]]; versions[r] = i
        elif op == 'SCALE':
            values[r] *= F(e[2]); versions[r] = i
        elif op == 'COPY':
            values[r] = F(e[3]) * values[e[2]]; versions[r] = i
        elif op == 'INIT':
            values[r] = F(0); charts[r] = e[2]; birth[r] = i; versions[r] = i; move[r] = None
        elif op == 'CLEAR':
            values[r] = F(0); charts[r] = None
        elif op == 'MOVE':
            charts[r] = e[3]; move[r] = i
        else:
            raise ValueError('unknown operator')
        for o in wants.get(i, []):
            q = o['role']
            need(charts[q] is not None and spans[charts[q]] == spans[o['chart']], 'actual observation chart')
            need((versions[q], birth[q], move[q]) == (o['value_version'], o['birth'], o['last_move']), 'actual history version and lifetime')
        record(i, r)
    need(len(history) == 10, 'complete ten nonzero historical rows')
    bad = next(h for h in c['history_reductions'] if h['event'] == target_event)
    author = bad['cases']['owned_main']['all_candidate_records']
    need({(i, r) for i, r, _ in history} == {(x['event'], x['role']) for x in author}, 'complete independent candidate history')
    for i, r, qrow in history:
        o = next(x for x in author if (x['event'], x['role']) == (i, r))
        need(qrow == row(o['row']), 'all ten reverse historical rows')
    budget_raw = budget.read_bytes()
    need(hashlib.sha256(budget_raw).hexdigest() == c['prepaid_budget_sha256'], 'predecessor budget pin')
    budget_record = json.loads(budget_raw)['additional_per_native_headroom']
    p = c['fresh_preload_price']; D = int(p['denominator'])
    need(F(p['existing_headroom_upper']) == F(int(budget_record['numerator_bounds'][1]), int(budget_record['denominator'])), 'exact inherited budget')
    for rank, label in [(3, 'rank3_bounds'), (4, 'rank4_bounds')]:
        lo, hi = map(int, p[label]); target = rank ** 199 * D ** 200
        need(lo ** 200 <= target <= hi ** 200, 'exact200th-power enclosure')
    need(F(int(p['rank4_bounds'][0]), D) > F(p['existing_headroom_upper']), 'strict paid gap')
    target = row(c['source_target_rows']['37606'])
    need(target.get(0, F(0)) + target.get(20, F(0)) == 4, 'dual on independently reproduced row')
    mutant = dict(target); add(mutant, 0, F(1))
    need(mutant != target, 'coefficient mutation rejected')
    return {'status': 'PASS_INDEPENDENT_HISTORY_ADJOINT_AND_DUAL', 'source_sha256': PIN, 'full_target_rows_compared': len(rr), 'distinct_positive_observations_reversed': len(observation_rows), 'positive_identity_cases': sum(v['status'] == 'MEMBER' for h in c['history_reductions'] for v in h['cases'].values()), 'complete_obstruction_history_rows': len(history), 'obstruction_event': target_event, 'dual': 'row[0]+row[20]', 'target_dual_value': '4', 'owned_observer_provenances_checked': len(ledger), 'exact_rank4_price_exclusion': True, 'method': 'Independent reverse adjoints plus literal metadata and scalar-mode replay; no author implementation imported.', 'scope': 'History identities and scoped information obstruction; all observation acquisition and physical costs remain premises.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for key in ('source', 'packet', 'reverse-rows', 'budget', 'output'):
        p.add_argument('--' + key, type=Path, required=True)
    a = p.parse_args(); result = run(a.source, a.packet, a.reverse_rows, a.budget)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
