#!/usr/bin/env python3
"""Independent full-222-column audit of the Y34/packet source."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from check import SOURCE_SHA, bits, dot, kernel, need, price, rank2, rref
from eight_check import binary_basis, solve_combination
from full_history_check import D_NORMALS, cyclic_components

TARGET = 34


def derive(roots, charts, localized=False, second_receiver=False):
    b = D_NORMALS[0]
    h = [((dot(roots[72],root)+dot(b,root))//2)%2 for root in roots]
    all_x = (1 << 111)-1
    hm = bits(j for j,value in enumerate(h) if value)
    canonical = [bits(j for j,other in enumerate(roots) if i==j or dot(root,other)==0)
                 for i,root in enumerate(roots)]
    W = [row & (hm if h[i] else all_x ^ hm) for i,row in enumerate(canonical)]
    seeds = [W[i] for i in [0,1,2,3,34,4,8,59]]
    specs = [('D',[D_NORMALS[i] for i in [0,3,1,2]]+[roots[TARGET]],0,4),
             ('S',[roots[i] for i in ([34,5,11,17] if second_receiver else [34,5,11])],1,3)]
    expected = {f'R{j}':(f'L{j}',1 << j) for j in range(111)}
    expected['YM'] = ('zero',1 << (111+TARGET))
    modes,groups,masks = [],[],[]
    consumed = set()

    def chart(label,subset):
        if second_receiver and (label,subset)==('S',8):
            return 'F17'
        return f'F{TARGET}' if (label,subset) in [('D',16),('S',1)] else f'{label}{subset}'

    for label,normals,source_class,active in specs:
        size = len(normals)
        need(len(rref(normals))==size,'independent source/query normals')
        for subset in range(1,1 << size):
            need(charts[chart(label,subset)]==kernel([normal for i,normal in enumerate(normals) if subset >> i & 1]),'actual cohort intersection chart')
        cache = {}
        for i in range(size):
            for length in range(1,size+1):
                subset = bits((i+k)%size for k in range(length))
                cache[f'{label}C{i}_{length}'] = [chart(label,subset),0]
        source_groups = {pattern:[] for pattern in range(1,1 << size)}
        for j,root in enumerate(roots):
            if h[j]==source_class:
                pattern = sum((dot(root,normal)==0) << i for i,normal in enumerate(normals))
                if pattern:
                    source_groups[pattern].append(j)
        for pattern,sources in source_groups.items():
            if not sources:
                continue
            need(not (set(sources)&consumed),'disjoint original source groups')
            consumed.update(sources)
            components = cyclic_components(pattern,size)
            if localized:
                components.sort(key=lambda component:-len(component))
            need(len(components)<=len(sources),'actual internal donors available')
            donors = sources[1:len(components)]
            for index,component in enumerate(components):
                value = bits(sources)
                if index:
                    donor = donors[index-1]
                    value ^= 1 << donor
                    name = f'{label}M{pattern}_{donor}'
                    destination_pattern = (1 << size)-1
                    if localized:
                        need(len(component)==1,'masked run is a singleton')
                        destination_pattern = 0
                        for length in range(1,size+1):
                            destination_pattern |= 1 << ((component[0]+length-1)%size)
                            if destination_pattern & pattern == pattern:
                                break
                    destination = chart(label,destination_pattern)
                    expected[name] = (destination,1 << donor)
                    masks.append({'record':name,'source':donor,'birth_chart':chart(label,pattern),
                                  'final_chart':destination,'paid_rank_descent':destination_pattern.bit_count()-pattern.bit_count(),
                                  'nonlocal_at_final_chart':len(rref(charts[destination]+rref([roots[donor]])))>len(charts[destination])})
                for offset,i in enumerate(component):
                    cache[f'{label}C{i}_{len(component)-offset}'][1] ^= value
            groups.append({'class':label,'pattern':pattern,'sources':sources,'runs':components,'internal_donors':donors})
        expected.update({name:tuple(value) for name,value in cache.items()})
        modes += [bits(j for j,root in enumerate(roots) if h[j]==source_class and dot(root,normal)==0)
                  for normal in normals[:active]]
    need((rank2(seeds),rank2(modes),rank2(seeds+modes),rank2(W))==(8,7,15,15),'eight complementary seeds and seven W modes')
    need(len(masks)==(7 if second_receiver else 5) and sum(x['paid_rank_descent'] for x in masks)==(7 if second_receiver else (5 if localized else 10)),'all masks and their exact paid rank units')
    foreign = bits(j for j,root in enumerate(roots) if h[j]==h[TARGET] and dot(root,roots[TARGET])==0)
    need(foreign ^ W[TARGET] == 1 << TARGET,'exact D8 foreign correction')
    return W,seeds,modes,expected,groups,masks,foreign


def replay(word,roots,localized=False,second_receiver=False):
    charts = {name:rref(spec['rows']) if spec['kind']=='span' else kernel(spec['rows'])
              for name,spec in word['charts'].items()}
    need(len(charts['Hub'])==8 and not charts['zero'],'Hub and ground')
    for j,root in enumerate(roots):
        need(charts[f'L{j}']==rref([root]) and charts[f'F{j}']==kernel([root]),'native charts')
    W,seeds,modes,expected,groups,masks,foreign = derive(roots,charts,localized,second_receiver)
    served = [17,34] if second_receiver else [34]
    owner_count = 168 if second_receiver else 159
    if second_receiver:
        need(seeds[5]^modes[5]==W[17],'actual terminal P5 equals A17')
    coupled_ops = [op for op in word['operations'] if op==['ADD','Y34','P4']]
    need(len(coupled_ops)<=1,'at most one literal singular exchange')
    coupled = bool(coupled_ops)
    for i,seed in enumerate(seeds):
        value = seed ^ (modes[i] if i<7 else 0)
        if i==4 and coupled:
            value ^= 1 << TARGET
        expected[f'P{i}'] = ('zero',value)
    records = {f'X{j}':[f'L{j}',1 << j,False] for j in range(111)}
    records.update({f'Y{j}':['zero',1 << (111+j),False] for j in range(111)})
    counts,profile = Counter(),Counter()
    packet_paths = {f'P{i}':[] for i in range(8)}
    y_path = [0]
    y17_path = [0]
    history,events,seen = [],[],set()
    exchanges,first_ground = [],{}
    inclusions = {}
    peak = dirty = 0
    checked_handoff = False
    final_handoff = None

    def contains(outer,inner):
        if (outer,inner) not in inclusions:
            inclusions[outer,inner] = len(rref(charts[outer]+charts[inner]))==len(charts[outer])
        return inclusions[outer,inner]

    def handoff():
        actual = {name:(r[0],r[1]) for name,r in records.items() if r[2]}
        need(actual==expected,'independently derived full owned handoff')
        for j in range(111):
            need(records[f'X{j}'][:2]==['Hub',1 << j],'all X restored at handoff')
            value = (1 << (111+j)) ^ ((1 << j) if j in served else 0)
            need(records[f'Y{j}'][:2]==[f'F{j}' if j in served else 'zero',value],'exact served Y targets and all others unchanged')
        return {name:{'chart':r[0],'coefficient_hex':hex(r[1]),'owned':r[2]} for name,r in records.items()}

    for step,operation in enumerate(word['operations'],1):
        kind,name,*args = operation
        counts[kind] += 1
        if kind=='INIT':
            need(name not in records and args[0] in charts,'fresh owned zero birth')
            records[name] = [args[0],0,True]
            peak = max(peak,sum(r[2] for r in records.values()))
            if name in packet_paths:
                need(not packet_paths[name],'one continuous packet lifetime')
                packet_paths[name].append(len(charts[args[0]]))
                need(all(records[f'X{j}'][:2]==['Hub',1 << j] for j in range(111)),'all originals restored before packet births')
                if name=='P0':
                    need(records['Y34'][:2]==['F34',(1 << 145)^foreign],'arbitrary-y foreign correction prepared before packets')
        elif kind=='ADD':
            target = args[0]
            need(name in records and target in records and name!=target,'live distinct ADD records')
            need(charts[records[name][0]]==charts[records[target][0]],f'literal cochart ADD at {step}')
            before = {role:records[role][1] for role in ['Y34','P4'] if role in records}
            records[target][1] ^= records[name][1]
            if operation==['ADD','P4','Y34']:
                need(before=={'Y34':(1 << 145)^foreign,'P4':W[TARGET]},'exact exchange boundary')
                need(records['Y34'][1]==(1 << 145)^(1 << TARGET),'literal Y34 output')
                exchanges.append({'operation':step,'kind':'deliver','before':{k:hex(v) for k,v in before.items()},'after_Y_hex':hex(records['Y34'][1]),'after_P_hex':hex(records['P4'][1])})
            if operation==['ADD','Y34','P4']:
                need(before=={'Y34':(1 << 145)^(1 << TARGET),'P4':W[TARGET]},'updated Y enters singular exchange')
                need(records['P4'][1]==(1 << 145)^foreign,'packet-through zero actual value')
                exchanges.append({'operation':step,'kind':'zero_through','after_Y_hex':hex(records['Y34'][1]),'after_P_hex':hex(records['P4'][1])})
        elif kind=='MOVE':
            need(name in records and args[0] in charts,'live MOVE roles')
            old,value,owned = records[name]
            new = args[0]
            need(contains(old,new) if owned else contains(new,old),f'monotone nested MOVE at {step}')
            delta = abs(len(charts[old])-len(charts[new]))
            need(delta>0,'positive movement rank')
            profile[delta] += 1
            records[name][0] = new
            if name in packet_paths:
                packet_paths[name].append(len(charts[new]))
                if new=='zero':
                    need(name not in first_ground,'first ground arrival of same lifetime')
                    first_ground[name] = {'operation':step,'value_hex':hex(value)}
            if name=='Y34':
                y_path.append(len(charts[new]))
            if name=='Y17':
                y17_path.append(len(charts[new]))
        elif kind=='CLEAR':
            if not checked_handoff:
                final_handoff = handoff()
                checked_handoff = True
            need(name in records and records[name][2],'owned erasure only')
            dirty += bool(records[name][1])
            del records[name]
        else:
            raise ValueError('unknown primitive')
        for packet in packet_paths:
            if packet in records and records[packet][0]!='Hub':
                chart,row,_ = records[packet]
                history.append(row)
                key = packet,chart,row
                if key not in seen:
                    events.append({'operation':step,'packet':packet,'chart':chart,'value_hex':hex(row)})
                    seen.add(key)
    if not checked_handoff:
        final_handoff = handoff()
    for i in range(8):
        expected_path = [8,7,6,5,4,3,0] if i<4 else (([8,7,6,5,4,0] if second_receiver else [8,7,6,5,0]) if i<7 else [8,0])
        need(packet_paths[f'P{i}']==expected_path,'continuous packet flag')
    need(y_path==[0,3,4,5,6,7],'literal upward receiver correction flag')
    if second_receiver:
        need(y17_path==[0,4,5,6,7],'literal second receiver correction flag')
    need(len(exchanges)==(2 if coupled else 1),'actual exchange operation count')
    for j in range(111):
        need(records[f'X{j}'][:2]==['Hub',1 << j],'final X endpoints')
        value = (1 << (111+j)) ^ ((1 << j) if j in served else 0)
        chart = f'F{j}' if word['closed_partial'] or j in served else 'zero'
        need(records[f'Y{j}'][:2]==[chart,value],'all222 final Y columns and charts')
    need(sum(r[2] for r in records.values())==(0 if word['closed_partial'] else owner_count),'all owner lifetimes accounted')
    terminal = [expected[f'P{i}'][1] for i in range(8)]
    need(all(row >> 111==0 for row in terminal),'arbitrary public y removed from terminal packets')
    rh = rank2(history)
    ry = rank2(row >> 111 for row in history)
    need(rank2(history+W)==rh,'full222-column history contains every pure-X W row')
    need(ry==(1 if coupled else 0),'actual public-y projection dimension')
    need(rank2(terminal)==8,'terminal packet dimension')
    if coupled:
        need(rh==(37 if second_receiver else 33),'full coupled historical dimension')
        need(int(first_ground['P4']['value_hex'],16)==expected['P4'][1]^(1 <<145),'first-ground payload retains actual public-y mask')
    if word['closed_partial']:
        expected_profile = {1:113,2:32,3:38,4:49,5:28,6:29,7:117,8:1}
        if localized:
            expected_profile[1] += 5
            expected_profile[2] -= 5
        if second_receiver:
            expected_profile = {1:142,2:19,3:49,4:66,5:22,6:22,7:112,8:1}
        need(dict(profile)==expected_profile,'complete movement profile')
        need(sum(rank*count for rank,count in profile.items())==2*111*7+8*8+(7 if second_receiver else (5 if localized else 10)),'endpoint movements plus paid mask descents')
    return {'status':'PASS_INDEPENDENT_COUPLED_HISTORY','coupled':coupled,'localized_masks':localized,'second_receiver':second_receiver,'all_222_columns_replayed':True,
            'operations':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(rank*count for rank,count in profile.items()),'moment':price(profile),
            'peak_owned':peak,'live_owned':sum(r[2] for r in records.values()),
            'dirty_clears_under_retained_contract':dirty,'packet_paths':packet_paths,'Y34_path':y_path,
            'completed_targets':served,'remaining_unserved_targets':111-len(served),'history_rank_full222':rh,
            'history_W_intersection_full222':15,'history_public_Y_projection_rank':ry,
            'history_pure_X_dimension':rh-ry,'terminal_rank':8,'terminal_W_intersection':rank2(terminal)+15-rank2(terminal+W),
            'actual_exchange':exchanges,'first_ground_payloads':first_ground,'internal_mask_routes':masks,
            'initial_seed_rows_hex':[hex(row) for row in seeds],'proper_mode_rows_hex':[hex(row) for row in modes],
            'history_basis_hex':[hex(row) for row in binary_basis(history)],'packet_events':events,
            'independently_derived_groups':groups,'actual_handoff':final_handoff,
            'boundary_crossings':[f'{len(masks)} paid descending source copies']+(['public-Y feedback through zero packet coefficient'] if coupled else []),
            'new_complete_kappa':False}


def negative_controls(base,roots,localized=False,second_receiver=False):
    tests = {
        'erase_public_y_mask_capture':lambda op:op==['ADD','Y34','YM'],
        'erase_internal_original_mask_capture':lambda op:op==['ADD','X38','DM11_38'],
        'erase_internal_mask_descent':lambda op:op[0]=='MOVE' and op[1]=='DM11_38',
        'erase_receiver_foreign_facet_read':lambda op:op==['ADD','DC4_1','Y34'],
        'erase_packet_to_receiver_delivery':lambda op:op==['ADD','P4','Y34'],
        'erase_updated_Y_feedback':lambda op:op==['ADD','Y34','P4'],
        'erase_ground_public_y_cancellation':lambda op:op==['ADD','YM','P4'],
        'erase_internal_donor_restoration':lambda op:op==['ADD','X35','X38'],
    }
    if second_receiver:
        tests.update({'erase_Y17_ground_read':lambda op:op==['ADD','P5','Y17'],
                      'erase_Y17_foreign_facet_read':lambda op:op==['ADD','SC3_1','Y17'],
                      'erase_Y17_nonlocal_mask_read':lambda op:op==['ADD','SM10_19','Y17']})
    result = {}
    for label,predicate in tests.items():
        word = copy.deepcopy(base)
        matches = [i for i,op in enumerate(word['operations']) if predicate(op)]
        need(matches,'meaningful semantic mutant exists')
        index = matches[-1] if label=='erase_internal_donor_restoration' else matches[0]
        del word['operations'][index]
        try:
            replay(word,roots,localized,second_receiver)
        except (ValueError,KeyError) as error:
            result[label]={'rejected':True,'reason':str(error)}
        else:
            raise ValueError('accepted semantic mutant '+label)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--words',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--localized',action='store_true')
    p.add_argument('--second-receiver',action='store_true')
    args = p.parse_args()
    raw = args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'source hash pin')
    roots = json.loads(raw)['native_roots']
    names = ['COUPLED-WORD.json','COUPLED-CLOSED-WORD.json','UNCOPLED-WORD.json','UNCOPLED-CLOSED-WORD.json']
    words = {name:json.loads((args.words/name).read_text()) for name in names}
    variants={name:replay(word,roots,args.localized,args.second_receiver) for name,word in words.items()}
    old=[int(row,16) for row in variants['UNCOPLED-WORD.json']['history_basis_hex']]
    new=[int(row,16) for row in variants['COUPLED-WORD.json']['history_basis_hex']]
    augmented=old+[1 <<34,1 <<145]
    need(rank2(new)==rank2(augmented)==rank2(new+augmented)==len(old)+2,'exact feedback gain is x34 and y34')
    feedback_gain={'uncoupled_history_rank':len(old),'coupled_history_rank':len(new),
                   'coupled_equals_uncoupled_plus_x34_and_y34':True,
                   'x34_coefficient_mask':solve_combination(new,1 <<34),
                   'y34_coefficient_mask':solve_combination(new,1 <<145)}
    result={'status':'PASS_INDEPENDENT_COUPLED_AND_CONTROL_REVIEW','source_sha256':SOURCE_SHA,
            'author_code_imported':False,'word_sha256':{name:hashlib.sha256((args.words/name).read_bytes()).hexdigest() for name in names},
            'variants':variants,'feedback_gain':feedback_gain,
            'negative_controls':negative_controls(words['COUPLED-WORD.json'],roots,args.localized,args.second_receiver),'new_complete_kappa':False}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
