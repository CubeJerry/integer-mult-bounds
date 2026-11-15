#!/usr/bin/env python3
"""Independent exact replay of the changed-basis full singular history."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

from check import SOURCE_SHA, bits, dot, kernel, need, price, rank2, rref
from eight_check import binary_basis, solve_combination

D_NORMALS = [[0,0,1,1,0,0,1,-1], [0,1,1,0,-1,0,0,1],
             [0,1,1,0,0,-1,-1,0], [1,1,-1,1,0,0,0,0]]


def cyclic_components(pattern, size):
    if pattern == (1 << size)-1:
        return [list(range(size))]
    starts = [i for i in range(size) if pattern >> i & 1 and not pattern >> ((i-1)%size) & 1]
    result = []
    for start in starts:
        component = []
        j = start
        while pattern >> j & 1:
            component.append(j)
            j = (j+1) % size
        result.append(component)
    return result


def geometry(roots, charts):
    omitted = D_NORMALS[0]
    h = [((dot(roots[72], root)+dot(omitted, root))//2) % 2 for root in roots]
    all_x = (1 << 111)-1
    hmask = bits(j for j, value in enumerate(h) if value)
    canonical = [bits(j for j, other in enumerate(roots) if i == j or dot(root, other) == 0)
                 for i, root in enumerate(roots)]
    W = [row & (hmask if h[i] else all_x ^ hmask) for i, row in enumerate(canonical)]
    seed_roles = [0,1,2,3,4,10,32,59]
    seeds = [W[i] for i in seed_roles]
    expected = {f'R{j}':(f'L{j}', 1 << j) for j in range(111)}
    modes, cohorts = [], []
    consumed = set()
    for label, normals, source_class, branch_donors in [
        ('D',D_NORMALS,0,{5:37,10:55}), ('S',[roots[i] for i in [5,11,21]],1,{})]:
        size = len(normals)
        need(len(rref(normals)) == size, 'independent cohort query normals')
        for subset in range(1, 1 << size):
            need(charts[f'{label}{subset}'] == kernel([normal for i, normal in enumerate(normals) if subset >> i & 1]), 'literal cohort intersection chart')
        groups = {pattern:set() for pattern in range(1, 1 << size)}
        for j, root in enumerate(roots):
            if h[j] == source_class:
                pattern = sum((dot(root, normal) == 0) << i for i, normal in enumerate(normals))
                if pattern:
                    groups[pattern].add(j)
        cache = {}
        for i in range(size):
            for length in range(1, size+1):
                subset = bits((i+k)%size for k in range(length))
                cache[f'{label}C{i}_{length}'] = [f'{label}{subset}', 0]
        for pattern, donor in branch_donors.items():
            need(h[donor] != source_class and all(dot(roots[donor], normal) == 0 for normal in normals), 'opposite-class donor lies in common chart')
            need(all(dot(roots[donor], roots[i]) != 0 for i in [5,11,21]), 'donor excluded from spinor source cohort')
            need(donor not in consumed, 'donor path unused')
            consumed.add(donor)
            expected[f'{label}M{donor}'] = (f'{label}{(1 << size)-1}', 1 << donor)
        for pattern, sources in groups.items():
            if not sources:
                continue
            need(not (sources & consumed), 'disjoint original source cohorts')
            consumed.update(sources)
            components = cyclic_components(pattern, size)
            need(len(components) <= 2 and (len(components) == 2) == (pattern in branch_donors), 'exact two-run branch obligation')
            for component_index, component in enumerate(components):
                row = bits(sources)
                if component_index:
                    row ^= 1 << branch_donors[pattern]
                for offset, i in enumerate(component):
                    cache[f'{label}C{i}_{len(component)-offset}'][1] ^= row
            cohorts.append({'class':label,'pattern':pattern,'sources':sorted(sources),
                            'runs':components,'donor':branch_donors.get(pattern)})
        expected.update({name:tuple(value) for name, value in cache.items()})
        modes += [bits(j for j, root in enumerate(roots) if h[j] == source_class and dot(root, normal) == 0)
                  for normal in normals]
    need((rank2(seeds),rank2(modes),rank2(seeds+modes),rank2(W)) == (8,7,15,15), 'eight seeds complement seven proper W modes')
    need(rank2(W+modes) == 15 and all(len(rref([root for j, root in enumerate(roots) if row >> j & 1])) == 7 for row in modes), 'all acquired modes are proper singular codewords')
    for i, seed in enumerate(seeds):
        expected[f'P{i}'] = ('zero', seed ^ (modes[i] if i < 7 else 0))
    return W, seeds, modes, expected, cohorts


def replay(word, roots):
    charts = {name:rref(spec['rows']) if spec['kind']=='span' else kernel(spec['rows'])
              for name,spec in word['charts'].items()}
    need(len(charts['Hub']) == 8 and not charts['zero'], 'Hub and ground')
    for j, root in enumerate(roots):
        need(charts[f'L{j}'] == rref([root]) and charts[f'F{j}'] == kernel([root]), 'native charts')
    W,seeds,modes,expected,cohorts = geometry(roots,charts)
    records = {f'X{j}':[f'L{j}',1 << j,False] for j in range(111)}
    records.update({f'Y{j}':['zero',1 << (111+j),False] for j in range(111)})
    paths = {f'P{i}':[] for i in range(8)}
    counts,profile = Counter(),Counter()
    history,events,seen = [],[],set()
    peak = dirty = 0
    handoff_checked = False
    final_handoff = None
    inclusions = {}

    def contains(outer,inner):
        if (outer,inner) not in inclusions:
            inclusions[outer,inner] = len(rref(charts[outer]+charts[inner])) == len(charts[outer])
        return inclusions[outer,inner]

    def handoff():
        actual = {name:(r[0],r[1]) for name,r in records.items() if r[2]}
        need(actual == expected,'all independent cache/point/packet handoff values')
        for j in range(111):
            need(records[f'X{j}'][:2] == ['Hub',1 << j],'restored X at handoff')
            need(records[f'Y{j}'][:2] == ['zero',1 << (111+j)],'unserved Y at handoff')
        return {name:{'chart':r[0],'coefficient_hex':hex(r[1]),'owned':r[2]} for name,r in records.items()}

    for step,operation in enumerate(word['operations'],1):
        kind,name,*args = operation
        counts[kind] += 1
        if kind == 'INIT':
            need(name not in records and args[0] in charts,'fresh owned zero birth')
            records[name] = [args[0],0,True]
            peak = max(peak,sum(r[2] for r in records.values()))
            if name in paths:
                need(not paths[name],'one continuous packet lifetime')
                paths[name].append(len(charts[args[0]]))
                need(all(records[f'X{j}'][:2] == ['Hub',1 << j] for j in range(111)), 'all originals restored before any packet birth')
        elif kind == 'ADD':
            target = args[0]
            need(name in records and target in records and name != target,'live distinct ADD roles')
            need(charts[records[name][0]] == charts[records[target][0]],f'literal cochart ADD at {step}')
            records[target][1] ^= records[name][1]
        elif kind == 'MOVE':
            need(name in records and args[0] in charts,'live movement roles')
            old,value,owned = records[name]
            new = args[0]
            need(contains(old,new) if owned else contains(new,old),f'monotone nested MOVE at {step}')
            rank = abs(len(charts[old])-len(charts[new]))
            need(rank > 0,'positive movement rank')
            profile[rank] += 1
            records[name][0] = new
            if name in paths:
                paths[name].append(len(charts[new]))
        elif kind == 'CLEAR':
            if not handoff_checked:
                final_handoff = handoff()
                handoff_checked = True
            need(name in records and records[name][2],'owned erasure only')
            dirty += bool(records[name][1])
            del records[name]
        else:
            raise ValueError('unsupported operation')
        for packet in paths:
            if packet in records and records[packet][0] != 'Hub':
                chart,row,_ = records[packet]
                history.append(row)
                key = packet,chart,row
                if key not in seen:
                    events.append({'operation':step,'packet':packet,'chart':chart,'value_hex':hex(row)})
                    seen.add(key)
    if not handoff_checked:
        final_handoff = handoff()
    for i in range(8):
        need(paths[f'P{i}'] == ([8,7,6,5,4,0] if i < 4 else ([8,7,6,5,0] if i < 7 else [8,0])),'literal eight-packet flags')
    for j in range(111):
        need(records[f'X{j}'][:2] == ['Hub',1 << j],'final original X value/chart')
        need(records[f'Y{j}'][:2] == [f'F{j}' if word['closed_partial'] else 'zero',1 << (111+j)],'all final Y remain unserved')
    need(sum(r[2] for r in records.values()) == (0 if word['closed_partial'] else 146),'all owners counted')
    need(rank2(history) == rank2(history+W) == 29,'actual history contains W and has rank29')
    need(rank2([expected[f'P{i}'][1] for i in range(8)]) == 8,'terminal rank8')
    for i in range(8):
        need(any(event['packet']==f'P{i}' and int(event['value_hex'],16)==seeds[i] for event in events),'actual departing seed occurs in history')
    if word['closed_partial']:
        need(dict(profile) == {1:98,2:42,3:21,4:27,5:52,6:32,7:115,8:1},'complete independent movement profile')
        need(sum(rank*count for rank,count in profile.items()) == 2*111*7+8*8,'complete monotone endpoint rank length')
    return {'status':'PASS_INDEPENDENT_FULL_SINGULAR_HISTORY','all_222_columns_replayed':True,
            'operations':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(rank*count for rank,count in profile.items()),'moment':price(profile),
            'peak_owned':peak,'live_owned':sum(r[2] for r in records.values()),
            'dirty_clears_under_retained_contract':dirty,'packet_paths':paths,
            'history_rank':29,'history_W_intersection':15,'outside_W_dimension':14,'terminal_rank':8,
            'initial_seed_rank':8,'proper_mode_rank':7,'all_originals_restored_before_packet_birth':True,
            'initial_seed_rows_hex':[hex(row) for row in seeds],'proper_mode_rows_hex':[hex(row) for row in modes],
            'history_basis_hex':[hex(row) for row in binary_basis(history)],'packet_events':events,
            'independent_source_cohorts':cohorts,'actual_handoff':final_handoff,
            'completed_Y_targets':0,'new_complete_kappa':False}


def mutants(base,roots):
    predicates = {
        'omit_actual_mask_copy':lambda op:op==['ADD','X37','DM37'],
        'omit_branched_original_copy':lambda op:op==['ADD','X12','X37'],
        'omit_packet_mask_removal':lambda op:op==['ADD','DM37','P2'],
        'omit_D8_flag_read':lambda op:op==['ADD','DC0_1','P0'],
        'omit_spinor_flag_read':lambda op:op==['ADD','SC0_1','P4'],
        'omit_eighth_actual_seed_term':lambda op:op[0]=='ADD' and op[-1]=='P7',
        'omit_original_donor_restoration':lambda op:op==['ADD','X84','X37'],
    }
    result = {}
    for label,predicate in predicates.items():
        word = copy.deepcopy(base)
        index = next(i for i,op in enumerate(word['operations']) if predicate(op))
        del word['operations'][index]
        try:
            replay(word,roots)
        except (ValueError,KeyError) as error:
            result[label]={'rejected':True,'reason':str(error)}
        else:
            raise ValueError('accepted semantic mutant '+label)
    word = copy.deepcopy(base)
    index = next(i for i,op in enumerate(word['operations']) if op==['MOVE','P2','D15'])
    word['operations'][index][-1]='zero'
    try:
        replay(word,roots)
    except (ValueError,KeyError) as error:
        result['skip_common_mask_meeting']={'rejected':True,'reason':str(error)}
    else:
        raise ValueError('accepted unavailable mask meeting')
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--words',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args = p.parse_args()
    raw = args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'native root source pin')
    roots = json.loads(raw)['native_roots']
    words = {name:json.loads((args.words/name).read_text()) for name in ['WORD.json','CLOSED-WORD.json']}
    result={'status':'PASS_INDEPENDENT_FULL_SINGULAR_HISTORY_REVIEW','source_sha256':SOURCE_SHA,
            'author_code_imported':False,
            'word_sha256':{name:hashlib.sha256((args.words/name).read_bytes()).hexdigest() for name in words},
            'variants':{name:replay(word,roots) for name,word in words.items()},
            'negative_controls':mutants(words['WORD.json'],roots),'new_complete_kappa':False}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
