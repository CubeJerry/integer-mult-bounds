#!/usr/bin/env python3
"""Complete Y1,Y3,Y5 while retaining the actual eight-packet singular history."""
from pathlib import Path
from collections import Counter
import copy
import json
from shared_facet_source import source_geometry,dot,rank_q,rank_f2,mask
from triple_source import build as triple_build
from eight_packet_source import price


def build(roots,h,closed=False):
    base=triple_build(roots,h)
    facets=base['facets'];donors=base['donors'];charts=base['charts']
    ops=[]
    for j in range(111):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}']]
    for o in base['operations'][:base['markers']['restored']]:
        if o[0]=='INIT'and o[1].startswith('R'):continue
        if o[0]=='ADD'and o[-1].startswith('R'):continue
        ops.append(o)
    moved=set(base['moved_original_sources'])
    groups={k:[]for k in range(1,8)}
    for j,r in enumerate(roots):
        if not h[j]:
            p=sum(int(dot(r,roots[f])==0)<<i for i,f in enumerate(facets))
            if p:groups[p].append(j)
    if not set(donors)<=set(groups[7]):raise ValueError('Spinor donors must lie in D8 triple group')
    ops += [['INIT','DT','D']]
    for i in range(3):
        ops += [['INIT',f'DZ{i}',f'E{i}'],['INIT',f'DC{i}',f'F{facets[i]}']]
        ops += [['ADD',f'M{i}','DT']]
    for j in groups[7]:
        if j in donors:continue
        ops += [['MOVE',f'X{j}','D'],['ADD',f'X{j}','DT'],['MOVE',f'X{j}','Hub']];moved.add(j)
    pairs=[3,6,5]
    carrier_roles=[]
    for i,p in enumerate(pairs):
        S=groups[p]
        if not S:raise ValueError('Empty native D8 pair group')
        carrier=S[0];carrier_roles.append(carrier);others=S[1:]
        ops += [['MOVE',f'X{carrier}',f'E{i}']]
        for j in others:
            ops += [['MOVE',f'X{j}',f'E{i}'],['ADD',f'X{j}',f'X{carrier}'],['MOVE',f'X{j}','Hub']]
        ops += [['ADD',f'X{carrier}',f'DZ{i}'],['MOVE',f'X{carrier}',f'F{facets[(i+1)%3]}'],
                ['ADD',f'X{carrier}',f'DC{(i+1)%3}'],['MOVE',f'X{carrier}','Hub']]
        for j in others:ops += [['ADD',f'X{j}',f'X{carrier}']]
        moved.update(S)
    for i,p in enumerate([1,2,4]):
        for j in groups[p]:
            ops += [['MOVE',f'X{j}',f'F{facets[i]}'],['ADD',f'X{j}',f'DC{i}'],['MOVE',f'X{j}','Hub']];moved.add(j)
    for j in range(111):
        if j not in moved:ops += [['MOVE',f'X{j}','Hub']]
    restored=len(ops)
    K=[mask(j for j,r in enumerate(roots)if j==i or dot(r,roots[i])==0)for i in range(111)]
    hm=mask(j for j in range(111)if h[j]);seeds=[K[i]for i in[1,3,5,10,11,15,30]]+[K[0]&hm]
    expected={f'R{j}':(f'L{j}',1<<j)for j in range(111)}
    for name,x in base['expected_owned_at_handoff'].items():
        if not name.startswith(('R','P')):expected[name]=(x['chart'],int(x['value_hex'],16))
    expected['DT']=('D',mask(groups[7]))
    for i in range(3):
        expected[f'DZ{i}']=(f'E{i}',mask(groups[pairs[i]]))
        expected[f'DC{i}']=(f'F{facets[i]}',mask(groups[1<<i])^mask(groups[pairs[(i-1)%3]]))
    for i,seed in enumerate(seeds):
        ops += [['INIT',f'P{i}','Hub']]
        for j in range(111):
            if seed>>j&1:ops += [['ADD',f'X{j}',f'P{i}']]
        if i<3:
            ops += [['MOVE',f'P{i}',f'T{i}'],['ADD',f'C{i}',f'P{i}'],['MOVE',f'P{i}',f'E{i}'],['ADD',f'Z{i}',f'P{i}'],
                    ['MOVE',f'P{i}','D'],['ADD','Zt',f'P{i}'],['ADD',f'M{i}',f'P{i}'],['MOVE',f'P{i}','zero']]
            expected[f'P{i}']=('zero',seed^(K[facets[i]]&hm))
        else:
            ops += [['MOVE',f'P{i}','zero']];expected[f'P{i}']=('zero',seed)
    packet_handoff=len(ops)
    for i,f in enumerate(facets):
        ops += [['ADD',f'P{i}',f'Y{f}'],['MOVE',f'Y{f}','D'],['ADD','DT',f'Y{f}'],
                ['MOVE',f'Y{f}',f'E{i}'],['ADD',f'DZ{i}',f'Y{f}'],
                ['MOVE',f'Y{f}',f'F{f}'],['ADD',f'DC{i}',f'Y{f}']]
    completed=len(ops)
    if closed:
        for name in expected:ops += [['CLEAR',name]]
        for j in range(111):
            if j not in facets:ops += [['MOVE',f'Y{j}',f'F{j}']]
    return {'schema':'singular-eight-packet-three-output-v1','facets':facets,'donors':donors,
            'D8_groups':{str(k):v for k,v in groups.items()},'D8_aggregate_carriers':carrier_roles,
            'charts':charts,'operations':ops,'closed_partial':closed,'completed_targets':facets,
            'markers':{'all_X_restored':restored,'packets_at_ground':packet_handoff,'three_Y_completed':completed},
            'expected_owned_at_handoff':{k:{'chart':c,'value_hex':hex(v)}for k,(c,v)in expected.items()},
            'expected_packet_paths':{f'P{i}':([8,7,6,5,0]if i<3 else[8,0])for i in range(8)},
            'new_complete_kappa':False}


def replay(word,roots,h):
    charts=word['charts'];dims={k:rank_q(c['rows'])if c['kind']=='span'else 8-rank_q(c['rows'])for k,c in charts.items()}
    def sub(a,b):
        x,y=charts[a],charts[b]
        if x['kind']==y['kind']=='ann':return rank_q(x['rows']+y['rows'])==rank_q(x['rows'])
        if x['kind']==y['kind']=='span':return rank_q(x['rows']+y['rows'])==rank_q(y['rows'])
        if x['kind']=='span'and y['kind']=='ann':return all(dot(v,w)==0 for v in x['rows']for w in y['rows'])
        raise ValueError('Unsupported inclusion')
    records={f'X{i}':{'chart':f'L{i}','value':1<<i,'owned':False}for i in range(111)}
    records.update({f'Y{i}':{'chart':'zero','value':1<<(111+i),'owned':False}for i in range(111)})
    profile=Counter();counts=Counter();paths={p:[]for p in word['expected_packet_paths']};history=[];peak=0;snapshots={}
    for count,op in enumerate(word['operations'],1):
        kind,name,*rest=op;counts[kind]+=1
        if kind=='INIT':
            if name in records:raise ValueError('Duplicate INIT')
            c=rest[0];records[name]={'chart':c,'value':0,'owned':True};peak=max(peak,sum(r['owned']for r in records.values()))
            if name in paths:
                if any(records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub'for j in range(111)):raise ValueError('Original not restored before packet')
                paths[name].append(dims[c])
        elif kind=='ADD':
            target=rest[0]
            if name==target or records[name]['chart']!=records[target]['chart']:raise ValueError('Unavailable ADD')
            records[target]['value']^=records[name]['value']
        elif kind=='MOVE':
            dest=rest[0];rec=records[name];src=rec['chart']
            if not(sub(dest,src)if rec['owned']else sub(src,dest)):raise ValueError('Illegal monotone MOVE')
            delta=abs(dims[src]-dims[dest])
            if not delta:raise ValueError('Zero-rank MOVE')
            profile[delta]+=1;rec['chart']=dest
            if name in paths:paths[name].append(dims[dest])
        elif kind=='CLEAR':
            if not records[name]['owned']:raise ValueError('Original CLEAR')
            del records[name]
        else:raise ValueError('Unknown operation')
        for name in paths:
            if name in records and records[name]['chart']!='Hub':history.append(records[name]['value'])
        for label,k in word['markers'].items():
            if k==count:
                if label=='all_X_restored'and any(records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub'for j in range(111)):raise ValueError('Original restoration marker')
                snapshots[label]={'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
                     'owned':{name:{'chart':r['chart'],'value_hex':hex(r['value'])}for name,r in records.items()if r['owned']},
                     'served_Y':{f'Y{j}':{'chart':records[f'Y{j}']['chart'],'value_hex':hex(records[f'Y{j}']['value'])}for j in word['completed_targets']}}
    if paths!=word['expected_packet_paths']:raise ValueError('Lifetime changed')
    if snapshots['three_Y_completed']['owned']!=word['expected_owned_at_handoff']:raise ValueError('Owned handoff mismatch')
    for j in range(111):
        if records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub':raise ValueError('Original X endpoint')
        served=j in word['completed_targets'];want=(1<<(111+j))^((1<<j)if served else 0)
        if records[f'Y{j}']['value']!=want:raise ValueError(f'Original Y{j} value')
        if records[f'Y{j}']['chart']!=(f'F{j}'if served or word['closed_partial']else'zero'):raise ValueError('Y endpoint chart')
    live=sum(r['owned']for r in records.values())
    if live!=(0 if word['closed_partial']else 136):raise ValueError('Owner count')
    hm=mask(j for j in range(111)if h[j]);allones=(1<<111)-1
    K=[mask(j for j,r in enumerate(roots)if j==i or dot(r,roots[i])==0)for i in range(111)]
    W=[row&(hm if h[i]else allones^hm)for i,row in enumerate(K)]
    rh=rank_f2(history);rj=rank_f2(history+W)
    if(rh,rh+15-rj,rj-15)!=(18,11,7):raise ValueError('Packet history changed')
    return {'status':'PASS_SINGULAR_EIGHT_PACKET_THREE_OUTPUT','all_original_input_columns':222,
            'completed_targets':word['completed_targets'],'closed_partial':word['closed_partial'],
            'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'owned_peak':peak,'live_owned':live,
            'packet_paths':paths,'history_dimension':18,'history_W_intersection':11,'history_outside_W_dimension':7,
            'snapshots':snapshots,'new_complete_kappa':False}


if __name__=='__main__':
    here=Path(__file__).parent;repo=next(p for p in here.parents if(p/'AGENTS.md').exists());roots,h,pins=source_geometry(repo)
    out=here/'three-output';out.mkdir(exist_ok=True)
    result={'status':'PASS_SINGULAR_EIGHT_PACKET_THREE_OUTPUT','source_pins':pins,'receipts':{},'negative_controls':{}}
    for closed in[False,True]:
        word=build(roots,h,closed);receipt=replay(word,roots,h);name=('CLOSED-'if closed else'')+'WORD.json'
        (out/name).write_text(json.dumps(word,sort_keys=True,indent=2)+'\n');result['receipts'][name]=receipt
    base=build(roots,h)
    predicates={'omit_reused_pure_mask':lambda o:o==['ADD','M0','DT'],
                'omit_D8_pair_capture':lambda o:o[0]=='ADD'and o[-1]=='DZ0',
                'omit_D8_pair_delivery':lambda o:o[0]=='ADD'and o[-1]=='DC1',
                'omit_D8_carrier_restoration':lambda o:o[0]=='ADD'and o[-1]==f"X{base['D8_aggregate_carriers'][0]}"and o[1].startswith('X'),
                'omit_ground_decoder_read':lambda o:o==['ADD','P0','Y1'],
                'omit_triple_decoder_read':lambda o:o==['ADD','DT','Y1'],
                'omit_pair_decoder_read':lambda o:o==['ADD','DZ0','Y1'],
                'omit_facet_decoder_read':lambda o:o==['ADD','DC0','Y1']}
    for label,predicate in predicates.items():
        word=copy.deepcopy(base)
        matches=[i for i,o in enumerate(word['operations'])if predicate(o)]
        i=matches[-1] if label=='omit_D8_carrier_restoration' else matches[0]
        del word['operations'][i]
        word['markers']={k:v-(v>i)for k,v in word['markers'].items()}
        try:replay(word,roots,h)
        except(ValueError,KeyError)as exc:result['negative_controls'][label]={'rejected':True,'reason':str(exc)}
        else:raise ValueError('Accepted semantic mutant')
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    bill=price(result['receipts']['CLOSED-WORD.json']['movement_profile']);bill['scope']='Actual source completes Y1,Y3,Y5 on the same eight lifetimes; other108Y remain unserved. No complete supplier or new kappa.'
    (out/'PRICE.json').write_text(json.dumps(bill,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'completed_targets':[1,3,5],'profile':result['receipts']['CLOSED-WORD.json']['movement_profile'],
                      'rank_length':result['receipts']['CLOSED-WORD.json']['rank_length'],'moment':bill['moment']['lower_decimal'],'limiting_room':bill['limiting_room']['lower_decimal']}))
