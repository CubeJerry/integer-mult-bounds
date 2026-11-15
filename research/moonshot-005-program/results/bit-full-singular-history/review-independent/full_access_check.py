#!/usr/bin/env python3
"""Actual downset information and small frozen-cache export gates."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from check import SOURCE_SHA, bits, dot, kernel, need, rank2, rref
from eight_check import binary_basis, combine, separator, solve_combination
from full_history_check import replay


def check(source, word_path):
    raw = source.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'authenticated root source')
    roots = json.loads(raw)['native_roots']
    word = json.loads(word_path.read_text())
    result = replay(word, roots)
    records = result['actual_handoff']
    charts = {name:rref(spec['rows']) if spec['kind']=='span' else kernel(spec['rows'])
              for name,spec in word['charts'].items()}
    T = [int(records[f'P{i}']['coefficient_hex'],16) for i in range(8)]
    all_x = (1 << 111)-1
    caches = {name:record for name,record in records.items()
              if record['owned'] and not name.startswith(('R','P')) and int(record['coefficient_hex'],16)}
    need(len(caches) == 22, 'all nonzero retained nonpoint caches')
    for name, record in records.items():
        if record['owned'] and not name.startswith('P'):
            row = int(record['coefficient_hex'],16)
            need(not row & ~all_x, 'all preprocessed caches are pure X')
            for j, root in enumerate(roots):
                if row >> j & 1:
                    need(len(rref(charts[record['chart']]+rref([root]))) == len(charts[record['chart']]), 'cache input support inside literal chart')
    for kind,name,*arguments in word['operations']:
        if kind == 'ADD' and arguments[0].startswith('P'):
            need(name.startswith('X') or name in records and records[name]['owned'] and not name.startswith('P'),
                 'packet updates have no packet or Y feedback')
    receivers, projections = [], []
    for i, root in enumerate(roots):
        local = bits(j for j, other in enumerate(roots) if dot(root,other) == 0)
        forbidden = all_x ^ local
        F = charts[f'F{i}']
        events = [event for event in result['packet_events'] if len(rref(F+charts[event['chart']])) == 7]
        rows = [int(event['value_hex'],16) for event in events]
        for event,row in zip(events,rows):
            terminal = T[int(event['packet'][1:])]
            need(not ((row ^ terminal) & forbidden), 'actual downset observation equals its terminal value modulo local originals')
        projected = [row & forbidden for row in rows]
        terminal_projected = [row & forbidden for row in T]
        need(rank2(projected) == rank2(terminal_projected) == rank2(projected+terminal_projected), 'same projected information space')
        coefficients = solve_combination(terminal_projected,1 << i)
        entry = {'receiver':i,'available_history_rank':rank2(rows),'available_event_count':len(events),
                 'terminal_feasible':coefficients is not None,'downset_feasible':coefficients is not None}
        if coefficients is None:
            dual = separator(terminal_projected,1 << i,forbidden)
            need(all((row & dual).bit_count()%2 == 0 for row in rows), 'dual annihilates every accessible historical row')
            entry.update({'dual_input_hex':hex(dual),'dual_input_support':[j for j in range(111) if dual >> j & 1]})
        else:
            entry.update({'terminal_coefficient_mask':coefficients,'fitting_row_hex':hex(combine(T,coefficients))})
        receivers.append(entry)
        projections.append((forbidden,terminal_projected))
    feasible = [entry['receiver'] for entry in receivers if entry['downset_feasible']]
    need(feasible == [17,59], 'exact two feasible native receivers')
    names = list(caches)
    cache_rows = [int(caches[name]['coefficient_hex'],16) for name in names]
    cache_projections = [[row & forbidden for row in cache_rows] for forbidden,_ in projections]
    subset_results = {}
    for size in [1,2,3]:
        best,leaders,distribution = -1,[],Counter()
        rejected = 0
        for choice in itertools.combinations(range(len(cache_rows)),size):
            fits = []
            first_failure = None
            for i,(_,base) in enumerate(projections):
                added = [cache_projections[i][j] for j in choice]
                if solve_combination(base+added,1 << i) is not None:
                    fits.append(i)
                elif first_failure is None:
                    first_failure = i
            distribution[len(fits)] += 1
            if len(fits) > best:
                best,leaders = len(fits),[]
            if len(fits) == best:
                leaders.append({'caches':[names[j] for j in choice],'feasible_receivers':fits})
            need(first_failure is not None,'no small cache subset completes all receivers')
            i = first_failure
            forbidden,base = projections[i]
            dual = separator(base+[cache_projections[i][j] for j in choice],1 << i,forbidden)
            need(all((row & dual).bit_count()%2 == 0 for row in T+[cache_rows[j] for j in choice]), 'all-field subset failure certificate')
            rejected += 1
        subset_results[str(size)] = {'subsets_checked':rejected,'best_fitted_count':best,'leaders':leaders,
                                     'fitted_count_histogram':dict(sorted(distribution.items())),
                                     'complete_subsets':0,'each_failed_subset_has_checked_dual_counterinput':True}
    need([subset_results[str(size)]['best_fitted_count'] for size in [1,2,3]] == [5,9,12], 'exact small-cache maxima')
    all_global = T+cache_rows
    need(rank2(all_global) == 29, 'all caches plus terminals recover full history')
    need(all(solve_combination([row & forbidden for row in all_global],1 << i) is not None
             for i,(forbidden,_) in enumerate(projections)), 'all-global-history positive control fits111')
    return {'status':'PASS_EXACT_FULL_HISTORY_ACCESS_GATE','source_sha256':SOURCE_SHA,
            'word_sha256':hashlib.sha256(word_path.read_bytes()).hexdigest(),
            'receivers':receivers,'feasible_receivers':feasible,'infeasible_receiver_count':109,
            'every_accessible_history_equal_to_terminal_mod_local':True,
            'stationary_caches_source_local_at_literal_charts':True,
            'nonzero_nonpoint_caches':[{**caches[name],'name':name,'chart_dimension':len(charts[caches[name]['chart']])} for name in names],
            'global_small_cache_subset_tests':subset_results,
            'positive_control_all22_cache_values_and_T_rank':29,
            'positive_control_all22_cache_values_and_T_fitted_receivers':111,
            'scope':'Frozen flags/values; no new nonlocal cache movements or coupled feedback. Small-cache tests grant selected current rows globally and exclude only subsets of at most three such rows.',
            'existing_theorem_applied':'results/bit-source-packet-scattering/author/PROOF.md Theorem1; current D_C=I',
            'new_complete_kappa':False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--word',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    args.output.write_text(json.dumps(check(args.source,args.word),indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
