#!/usr/bin/env python3
"""Independent S008 terminal quotient and full-word review.

Imports only the root review's independent forward engine, not author code.
Prepared for @CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

from review import PIN, add, interpret, native_target, need, root_floor, span


def row_rank(rows):
    pivots = {}
    for values in rows:
        row = values.copy()
        while row:
            p = min(row)
            if p not in pivots:
                v = row[p]
                pivots[p] = {i: x / v for i, x in row.items()}
                break
            add(row, pivots[p], -row[p])
    return len(pivots)


def main(args):
    raw = args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'authentic native source')
    native = json.loads(gzip.decompress(raw))
    before_payload = gzip.decompress(args.partial.read_bytes())
    after_payload = gzip.decompress(args.complete.read_bytes())
    before, after = json.loads(before_payload), json.loads(after_payload)
    n = len(before['program'])
    need(n == 6952 and len(after['program']) == 32712, 'literal word lengths')
    need(after['program'][:n] == before['program'], 'identical executed prefix')
    need(after['initial'] == before['initial'] and after['public'] == 1880,
         'same original physical domain')
    original = native_target(native)
    source_rows, source_locations, source_receipt = interpret(native, native)
    need(source_rows == original, 'fresh source forward identity')
    need(source_locations == dict(enumerate(native['final'])), 'source finals')
    main_roles = sorted(set(native['live']) | {x + 112 for x in native['live']} |
                        set(native['hosted']['X2']) | set(native['hosted']['Y2']))
    raw_roles = {r: 1480 + i for i, r in enumerate(main_roles)}
    need(before['initial'] == native['initial'] + [native['initial'][r] for r in main_roles], 'authentic original1880 initial charts')
    expected = {i: row.copy() for i, row in original.items()}
    for r, private in raw_roles.items():
        need(set(original[r]) <= raw_roles.keys(), 'source main map closed')
        expected[private] = {raw_roles[i]: v for i, v in original[r].items()}
    finals = native['final'] + [native['final'][r] for r in main_roles]
    before_rows, before_locations, before_receipt = interpret(native, before)
    after_rows, after_locations, after_receipt = interpret(native, after)
    need(after_rows == expected, 'all1880 complete source targets')
    need(before_locations == after_locations == dict(enumerate(finals)),
         'actual identical final charts')

    # Quotients use actual subspaces, merging chart aliases automatically.
    spaces = [span(f) for f in native['frames']]
    grouped = defaultdict(list)
    for role, chart in before_locations.items():
        grouped[spaces[chart]].append(role)
    deficits = []
    for space, roles in grouped.items():
        current = [before_rows[r] for r in roles]
        target = [expected[r] for r in roles]
        current_rank = row_rank(current)
        union_rank = row_rank(current + target)
        if union_rank != current_rank:
            deficits.append(dict(chart_ids=sorted({before_locations[r] for r in roles}),
                                 dimension=(len(space).bit_length() - 1),
                                 roles=len(roles), current_rank=current_rank,
                                 union_rank=union_rank, deficit=union_rank-current_rank))
    hub = [d for d in deficits if d['dimension'] == 9]
    facets = [d for d in deficits if d['dimension'] == 8]
    need(len(deficits) == 105 and len(hub) == 1 and len(facets) == 104,
         '105 distinct actual required subspaces')
    need(hub[0]['deficit'] == 208 and all(d['deficit'] == 2 for d in facets),
         'hub208 and facet2 deficits')
    need(sum(d['deficit'] for d in deficits) == 416, 'sharp summed floor')
    suffix = after['program'][n:]
    suffix_counts = dict(Counter(o[0] for o in suffix))
    need(suffix_counts == {'INIT':432,'ADD':24480,'MOVE':416,'CLEAR':432},
         'all suffix operations charged')
    move_ranks = Counter(abs(len(native['frames'][o[2]])-len(native['frames'][o[3]]))
                         for o in suffix if o[0] == 'MOVE')
    need(dict(move_ranks) == {1:416}, 'exact rank-one attainment')
    need(after_receipt['peak_owned'] == 113 and after_receipt['owned_lifetimes'] == 464,
         'physical owner peak and lifetimes')

    invoice = json.loads(args.invoice.read_bytes())
    T = {int(k):v for k,v in invoice['T4'].items()}
    P = {int(k):v for k,v in invoice['P4'].items()}
    native_hist = Counter(source_receipt['move_histogram'])
    raw_hist = Counter(abs(len(native['frames'][o[2]])-len(native['frames'][o[3]]))
                       for o in native['program'] if o[0] == 'MOVE' and o[1] in raw_roles)
    for r in set(native_hist) | set(raw_hist) | set(after_receipt['move_histogram']):
        P[r] = P.get(r,0) + 18*(after_receipt['move_histogram'].get(r,0)-native_hist[r]-raw_hist[r])
    need(all(v >= 0 for v in P.values()), 'complete histogram nonnegative')
    surplus = sum(r*(T.get(r,0)-P.get(r,0)) for r in set(T)|set(P))
    need(sum(P.values()) == 49968 and sum(T.values()) == 27344 and surplus == -5600,
         'complete caller accounting')
    den = 10**24
    lo = hi = 0
    for r in set(T) | set(P):
        d = T.get(r,0)-P.get(r,0)
        z = r**199 * den**200
        a = root_floor(z,200)
        b = a if a**200 == z else a+1
        lo += d*(a if d>=0 else b)
        hi += d*(b if d>=0 else a)
    bounds = [F(lo,18*den), F(hi,18*den)]
    need(F(-401188,1000) < bounds[0] <= bounds[1] < F(-401187,1000),
         'rigorously failing target moment')

    negatives = []
    predicates = [
        ('omit_actual_inbound_move', lambda o:o[0]=='MOVE', 'omit'),
        ('omit_actual_outbound_move', lambda o:o[0]=='MOVE' and len(native['frames'][o[2]])==9, 'omit'),
        ('reverse_public_update_sign', lambda o:o[0]=='ADD' and o[1]<1880 and o[2]>=1880, 'sign'),
        ('omit_coupled_inverse_entry', lambda o:o[0]=='ADD' and '/' in o[3] and F(o[3]).denominator>16, 'omit'),
    ]
    for label, pred, action in predicates:
        bad = dict(after)
        bad['program'] = [o.copy() for o in after['program']]
        k = next(k for k in range(n,len(bad['program'])) if pred(bad['program'][k]))
        if action == 'omit':
            bad['program'].pop(k)
        else:
            bad['program'][k][3] = str(-F(bad['program'][k][3]))
        try:
            mutated, locations, _ = interpret(native,bad)
            need(mutated == expected and locations == after_locations, 'mutant target mismatch')
        except ValueError as error:
            negatives.append(dict(mutation=label,event=k,rejected=str(error)))
        else:
            raise ValueError('accepted negative control '+label)
    receipt = dict(status='PASS_INDEPENDENT_SHARP_416_TERMINAL_REVIEW',
        source_sha256=PIN,partial_payload_sha256=hashlib.sha256(before_payload).hexdigest(),
        complete_payload_sha256=hashlib.sha256(after_payload).hexdigest(),
        method='Fresh root forward symbolic interpreter and exact actual-chart quotient ranks; no author code imports',
        source_all1480_inputs=True,complete_all1880_inputs=True,identical_partial_prefix=True,
        local_quotients=sorted(deficits,key=lambda d:(-d['dimension'],d['chart_ids'])),
        summed_field_arrival_floor=416,suffix_counts=suffix_counts,suffix_move_histogram=dict(move_ranks),
        complete_physical=after_receipt,paid_histogram=P,paid_count=sum(P.values()),target_count=sum(T.values()),
        rank_surplus=surplus,moment_per_native_bounds=[str(x) for x in bounds],negative_controls=negatives,
        scope='Sharp append-only full-field linear terminal bound for this exact partial word. Earlier code and retained records may evade it. Complete finite normalized word fails target budget. No new kappa.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','summed_field_arrival_floor','paid_count','rank_surplus']}))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    for name in ['source','partial','complete','invoice','output']:
        p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
