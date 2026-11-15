#!/usr/bin/env python3
"""Independent eight-packet replay and full-history fitting/placement tests."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

from check import SOURCE_SHA, bits, dot, kernel, need, price, rank2, rref


def replay(word, roots):
    charts = {name: rref(spec['rows']) if spec['kind'] == 'span' else kernel(spec['rows'])
              for name, spec in word['charts'].items()}
    for i, root in enumerate(roots):
        need(charts[f'L{i}'] == rref([root]), 'native line chart')
        need(charts[f'F{i}'] == kernel([root]), 'native facet chart')
    need(len(charts['Hub']) == 8 and not charts['zero'], 'Hub and ground identity')
    omitted = [0, 0, 1, 1, 0, 0, 1, -1]
    h = [((dot(roots[72], root)+dot(omitted, root))//2)%2 for root in roots]
    facets, donors = word['facets'], word['donors']
    need(len(set(facets)) == len(set(donors)) == 3, 'three independent branches/carriers')
    need(all(not h[i] for i in facets+donors), 'D8 normal/carrier classes')
    need(charts['D'] == kernel([roots[i] for i in facets]) and len(charts['D']) == 5, 'actual rank-five common chart')
    need(all(dot(roots[d], roots[i]) == 0 for d in donors for i in facets), 'donor source containment')
    for i in range(3):
        need(charts[f'T{i}'] == charts[f'F{facets[i]}'], 'branch facet identity')
        need(charts[f'E{i}'] == kernel([roots[facets[i]], roots[facets[(i+1)%3]]]), 'pair chart identity')
    patterns = {k: set() for k in range(1, 8)}
    for j, root in enumerate(roots):
        if h[j]:
            signature = sum((dot(root, roots[f]) == 0) << i for i, f in enumerate(facets))
            if signature:
                patterns[signature].add(j)
    need({str(k): sorted(v) for k, v in patterns.items()} == word['patterns'], 'exact source incidence classes')
    seeds = [{j for j, root in enumerate(roots) if j == f or dot(root, roots[f]) == 0}
             if word['canonical_seeds'] else set() for f in facets]
    pairs = [3, 6, 5]
    moved = list(range(111))
    need(moved == word['moved_original_sources'], 'all moved source inputs accounted')
    expected = {f'R{j}': (f'L{j}', 1 << j) for j in moved}
    expected['Zt'] = ('D', bits(patterns[7]))
    for i in range(3):
        incoming = (i-1)%3
        expected[f'Z{i}'] = (f'E{i}', bits(patterns[pairs[i]]))
        expected[f'M{i}'] = ('D', 1 << donors[incoming])
        expected[f'C{i}'] = (f'T{i}', bits(patterns[1 << i]) ^ bits(patterns[pairs[incoming]]) ^ (1 << donors[incoming]))
        mode = bits(j for j, root in enumerate(roots) if h[j] and dot(root, roots[facets[i]]) == 0)
        expected[f'P{i}'] = ('zero', bits(seeds[i]) ^ mode)
    extra_seed_rows = [bits(j for j, root in enumerate(roots) if j == i or dot(root, roots[i]) == 0) for i in [10, 11, 15, 30]] + [bits(j for j, root in enumerate(roots) if h[j] and (j == 0 or dot(root, roots[0]) == 0))]
    for i, row in enumerate(extra_seed_rows, 3):
        expected[f'P{i}'] = ('zero', row)
    records = {f'X{i}': [f'L{i}', 1 << i, False] for i in range(111)}
    records.update({f'Y{i}': ['zero', 1 << (111+i), False] for i in range(111)})
    counts, profile = Counter(), Counter()
    paths = {f'P{i}': [] for i in range(8)}
    peak = dirty = 0
    checked_handoff = False
    history = []
    all_x = (1 << 111)-1
    hmask = bits(j for j, value in enumerate(h) if value)
    canonical = [bits(j for j, other in enumerate(roots) if j == i or dot(root, other) == 0) for i, root in enumerate(roots)]
    wrows = [row & (hmask if h[i] else all_x ^ hmask) for i, row in enumerate(canonical)]
    inclusion = {}

    def contains(outer, inner):
        if (outer, inner) not in inclusion:
            inclusion[outer, inner] = len(rref(charts[outer]+charts[inner])) == len(charts[outer])
        return inclusion[outer, inner]

    def handoff():
        live = {name: (record[0], record[1]) for name, record in records.items() if record[2]}
        need(live == expected, 'independently derived triple handoff')
        for i in range(111):
            need(records[f'X{i}'][:2] == ['Hub' if i in moved else f'L{i}', 1 << i], 'restored live original X')
            need(records[f'Y{i}'][:2] == ['zero', 1 << (111+i)], 'unchanged live original Y')

    for step, operation in enumerate(word['operations'], 1):
        kind, name, *arguments = operation
        counts[kind] += 1
        if kind == 'INIT':
            need(name not in records and arguments[0] in charts, 'fresh owned zero birth')
            records[name] = [arguments[0], 0, True]
            peak = max(peak, sum(record[2] for record in records.values()))
            if name in paths:
                need(not paths[name], 'continuous packet lifetime')
                paths[name].append(len(charts[arguments[0]]))
                for i in moved:
                    need(records[f'X{i}'][:2] == ['Hub', 1 << i], 'source restoration before packet birth')
        elif kind == 'ADD':
            target = arguments[0]
            need(name in records and target in records and name != target, 'live distinct ADD records')
            need(charts[records[name][0]] == charts[records[target][0]], f'actual cochart ADD at {step}')
            records[target][1] ^= records[name][1]
        elif kind == 'MOVE':
            need(name in records and arguments[0] in charts, 'live MOVE role and chart')
            old, value, owned = records[name]
            new = arguments[0]
            need(contains(old, new) if owned else contains(new, old), f'monotone nested MOVE at {step}')
            delta = abs(len(charts[old])-len(charts[new]))
            need(delta > 0, 'positive rank movement')
            profile[delta] += 1
            records[name][0] = new
            if name in paths:
                paths[name].append(len(charts[new]))
        elif kind == 'CLEAR':
            if not checked_handoff:
                handoff()
                checked_handoff = True
            need(name in records and records[name][2], 'owned record erasure')
            dirty += bool(records[name][1])
            del records[name]
        else:
            raise ValueError('unknown operation')
        for packet in paths:
            if packet in records and records[packet][0] != 'Hub':
                history.append(records[packet][1] & all_x)
    if not checked_handoff:
        handoff()
    need(all(paths[f'P{i}'] == ([8,7,6,5,0] if i<3 else [8,0]) for i in range(8)), 'eight continuous packet routes')
    for i in range(111):
        need(records[f'X{i}'][1] == 1 << i, 'all final X restored')
        need(records[f'Y{i}'][1] == 1 << (111+i), 'all final unserved Y unchanged')
        if word['closed_partial']:
            need(records[f'X{i}'][0] == 'Hub' and charts[records[f'Y{i}'][0]] == charts[f'F{i}'], 'closed original endpoint charts')
    live = sum(record[2] for record in records.values())
    need(live == (0 if word['closed_partial'] else len(expected)), 'complete owner count')
    rank_h, rank_joint = rank2(history), rank2(wrows+history)
    need(rank_joint == 22, 'seven actual outside-W historical directions')
    need(rank_h == 18, 'exact eight-packet historical dimension')
    e = sum(len(patterns[k]) for k in [1, 2, 4])
    p = sum(len(patterns[k]) for k in [3, 5, 6])
    t = len(patterns[7])
    if word['closed_partial']:
        need(dict(profile) == {1: e+18, 2: p, 3: t, 4: t+3, 5: p+3, 6: e, 7: 219-e-p-t, 8: 5}, 'independent closed profile formula')
    return {'status': 'PASS_INDEPENDENT_EIGHT_PACKET_SOURCE', 'canonical_seeds': word['canonical_seeds'],
            'closed_partial': word['closed_partial'], 'facets': facets, 'donors': donors,
            'patterns': {'exclusive': e, 'pair': p, 'triple': t}, 'moved_originals': len(moved),
            'operations': dict(sorted(counts.items())), 'movement_profile': dict(sorted(profile.items())),
            'rank_length': sum(rank*count for rank, count in profile.items()), 'moment': price(profile),
            'peak_owned': peak, 'live_owned': live, 'dirty_clears_under_retained_contract': dirty,
            'history_rank': rank_h, 'history_plus_W_rank': rank_joint,
            'history_W_intersection': rank_h+15-rank_joint, 'outside_W_dimension': rank_joint-15,
            'packet_paths': paths, 'all_222_columns_replayed': True, 'completed_Y_targets': 0,
            'all_original_X_restored': True, 'all_original_Y_unchanged': True, 'new_complete_kappa': False,
            'history_basis': [str(row) for row in binary_basis(history)],
            'records_at_final': {name: {'chart':record[0], 'coefficient_hex':hex(record[1]), 'owned':record[2]} for name,record in records.items()}}


def binary_basis(rows):
    pivots = {}
    for row in rows:
        while row:
            lead = row.bit_length()-1
            if lead in pivots:
                row ^= pivots[lead]
            else:
                pivots[lead] = row
                break
    return list(pivots.values())


def solve_combination(rows, target):
    pivots = {}
    for i, row in enumerate(rows):
        coefficient = 1 << i
        while row:
            lead = row.bit_length()-1
            if lead in pivots:
                old, mask = pivots[lead]
                row ^= old
                coefficient ^= mask
            else:
                pivots[lead] = row, coefficient
                break
    coefficient = 0
    while target:
        lead = target.bit_length()-1
        if lead not in pivots:
            return None
        row, mask = pivots[lead]
        target ^= row
        coefficient ^= mask
    return coefficient


def combine(rows, mask):
    value = 0
    for i, row in enumerate(rows):
        if mask >> i & 1:
            value ^= row
    return value


def kernel_combinations(rows):
    pivots, answer = {}, []
    for i, row in enumerate(rows):
        coefficient = 1 << i
        while row:
            lead = row.bit_length()-1
            if lead in pivots:
                old, mask = pivots[lead]
                row ^= old
                coefficient ^= mask
            else:
                pivots[lead] = row, coefficient
                break
        if not row:
            answer.append(coefficient)
    return answer


def separator(projected, target, allowed):
    echelon = binary_basis(projected)
    residual = target
    pivots = {row.bit_length()-1: row for row in echelon}
    for lead in sorted(pivots, reverse=True):
        if residual >> lead & 1:
            residual ^= pivots[lead]
    need(bool(residual), 'separator requires inconsistent target')
    free = residual.bit_length()-1
    witness = 1 << free
    for lead in sorted(pivots):
        row = pivots[lead]
        if ((row & witness).bit_count() % 2):
            witness |= 1 << lead
    need(not (witness & ~allowed), 'dual witness uses only forbidden/local-complement coordinates')
    need(all((row & witness).bit_count() % 2 == 0 for row in projected), 'dual witness annihilates observations')
    need((target & witness).bit_count() % 2 == 1, 'dual witness changes required own input')
    return witness


def fitting_analysis(roots, history, records):
    all_x = (1 << 111)-1
    omitted = [0,0,1,1,0,0,1,-1]
    h = [((dot(roots[72],r)+dot(omitted,r))//2)%2 for r in roots]
    hmask = bits(i for i,value in enumerate(h) if value)
    canonical = [bits(j for j,r in enumerate(roots) if i==j or dot(root,r)==0) for i,root in enumerate(roots)]
    split = [row & (hmask if h[i] else all_x ^ hmask) for i,row in enumerate(canonical)]
    W = binary_basis(split)
    G = binary_basis(history)
    extension = []
    for row in W:
        if solve_combination(G+extension,row) is None:
            extension.append(row)
    H = G+extension
    need((len(G),len(W),len(extension)) == (18,15,4), 'actual history and W quotient dimensions')
    terminal = [int(records[f'P{i}']['coefficient_hex'],16)&all_x for i in range(8)]
    need(rank2(terminal)==8, 'terminal packet code rank eight')
    receipts=[]
    forced=[]
    counts=Counter()
    for i,root in enumerate(roots):
        local = bits(j for j,r in enumerate(roots) if dot(root,r)==0)
        nonlocal_mask = all_x ^ local
        projected = [row & nonlocal_mask for row in G]
        coefficients = solve_combination(projected,1<<i)
        entry={'receiver':i,'native_class':h[i], 'global_history_feasible':coefficients is not None,
               'local_history_dimension':len(G)-rank2(projected)}
        if coefficients is not None:
            fitting=combine(G,coefficients)
            need((fitting&nonlocal_mask)==1<<i,'actual fitting coefficient certificate')
            entry.update({'fitting_row_hex':hex(fitting),'history_coefficient_mask':coefficients})
        else:
            dual=separator(projected,1<<i,nonlocal_mask)
            need(all((row&dual).bit_count()%2==0 for row in G),'full-history dual annihilation')
            entry['dual_input_hex']=hex(dual)
            entry['dual_input_support']=[j for j in range(111) if dual>>j&1]
        counts['historical_feasible' if coefficients is not None else 'historical_infeasible']+=1
        terminal_projected=[row&nonlocal_mask for row in terminal]
        terminal_coeff=solve_combination(terminal_projected,1<<i)
        entry['terminal_feasible_with_all_local_inputs']=terminal_coeff is not None
        counts['terminal_feasible' if terminal_coeff is not None else 'terminal_infeasible']+=1
        # The quotient of local fitting freedom in H=G+W, modulo G.
        local_kernel=kernel_combinations([row&nonlocal_mask for row in H])
        quotient_local=binary_basis(mask>>len(G) for mask in local_kernel)
        a_coordinates=solve_combination(H,split[i])
        need(a_coordinates is not None,'split fitting lies in G+W')
        required=a_coordinates>>len(G)
        entry['H_local_quotient_basis']=quotient_local
        entry['required_W_quotient_class']=required
        if not quotient_local:
            forced.append((i,required))
        receipts.append(entry)
    forced_basis=binary_basis(row for _,row in forced)
    # Best single proper W addition, granting its whole code everywhere.
    proper_path=Path(__file__).resolve().parent.parent/'RESULT.json'
    proper_data=json.loads(proper_path.read_text())
    proper_words=[int(row['word']) for row in proper_data['proper_words']]
    addition_results=[]
    quotient_representatives={}
    for row in proper_words:
        coordinate=solve_combination(H,row)>>len(G)
        quotient_representatives.setdefault(coordinate,row)
    for coordinate,row in sorted(quotient_representatives.items()):
        if not coordinate:
            continue
        feasible=[]
        for i,root in enumerate(roots):
            forbidden=all_x ^ bits(j for j,r in enumerate(roots) if dot(root,r)==0)
            if solve_combination([r&forbidden for r in G+[row]],1<<i) is not None:
                feasible.append(i)
        addition_results.append({'quotient':coordinate,'mode_hex':hex(row),'feasible_count':len(feasible),'newly_feasible':[i for i in feasible if not receipts[i]['global_history_feasible']]})
    return {'status':'PASS_EXACT_FULL_HISTORY_FITTING_SCREEN','history_rank':len(G),'terminal_rank':rank2(terminal),
            'history_plus_canonical_rank':rank2(G+canonical),'history_intersection_canonical':len(G)+9-rank2(G+canonical),
            'counts':dict(counts),'receivers':receipts,'W_quotient_extension_rows':[hex(row) for row in extension],
            'forced_unique_quotient_rows':forced,'forced_unique_quotient_rank':len(forced_basis),
            'single_proper_mode_extensions':addition_results,'global_history_is_free_information_relaxation':True,
            'new_complete_kappa':False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--words',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=args.source.read_bytes()
    need(hashlib.sha256(source).hexdigest()==SOURCE_SHA,'source pin')
    roots=json.loads(source)['native_roots']
    names=['WORD.json','CLOSED-WORD.json']
    words={name:json.loads((args.words/name).read_text()) for name in names}
    variants={name:replay(word,roots) for name,word in words.items()}
    live=variants['WORD.json']
    analysis=fitting_analysis(roots,[int(row) for row in live['history_basis']],live['records_at_final'])
    result={'status':'PASS_INDEPENDENT_EIGHT_PACKET_AND_HISTORY_REVIEW','author_code_imported':False,
            'source_sha256':SOURCE_SHA,'word_sha256':{name:hashlib.sha256((args.words/name).read_bytes()).hexdigest() for name in names},
            'variants':variants,'fitting_analysis':analysis,'new_complete_kappa':False}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()

