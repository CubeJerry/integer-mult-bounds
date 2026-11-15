#!/usr/bin/env python3
"""Materialize the eight declared seed packets plus three acquired W modes.

This still leaves all Y outputs unserved; history rank is not delivery.
"""
from pathlib import Path
from collections import Counter
import copy
import json
from shared_facet_source import source_geometry, dot, rank_q, rank_f2, mask
from triple_source import build
from price import F, moment, encode


def extend(roots,h,closed=False):
    word=build(roots,h,canonical=True)
    ops=word['operations'];at=next(i for i,o in enumerate(ops)if o==['INIT','P0','Hub'])
    extra=[]
    for j in range(111):
        if j not in word['moved_original_sources']:
            extra += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}'],['MOVE',f'X{j}','Hub']]
            word['expected_owned_at_handoff'][f'R{j}']={'chart':f'L{j}','value_hex':hex(1<<j)}
    ops[at:at]=extra
    K=[mask(j for j,r in enumerate(roots)if j==i or dot(r,roots[i])==0)for i in range(111)]
    hm=mask(j for j in range(111)if h[j])
    seed_specs=[('K10',K[10]),('K11',K[11]),('K15',K[15]),('K30',K[30]),('hK0',K[0]&hm)]
    for i,(_,row)in enumerate(seed_specs,3):
        ops += [['INIT',f'P{i}','Hub']]
        for j in range(111):
            if row>>j&1:ops += [['ADD',f'X{j}',f'P{i}']]
        ops += [['MOVE',f'P{i}','zero']]
        word['expected_owned_at_handoff'][f'P{i}']={'chart':'zero','value_hex':hex(row)}
    word['schema']='singular-eight-seed-three-innovation-source-v1'
    word['moved_original_sources']=list(range(111))
    word['markers']={'handoff':len(ops)}
    word['seed_specifications']=['K1','K3','K5']+[s for s,_ in seed_specs]
    word['expected_packet_paths']={f'P{i}':([8,7,6,5,0]if i<3 else[8,0])for i in range(8)}
    word['closed_partial']=closed
    if closed:
        for name in word['expected_owned_at_handoff']:ops += [['CLEAR',name]]
        for j in range(111):ops += [['MOVE',f'Y{j}',f'F{j}']]
    return word


def replay(word,roots,h):
    charts=word['charts'];dims={k:rank_q(c['rows'])if c['kind']=='span'else 8-rank_q(c['rows'])for k,c in charts.items()}
    def sub(a,b):
        x,y=charts[a],charts[b]
        if x['kind']==y['kind']=='ann':return rank_q(x['rows']+y['rows'])==rank_q(x['rows'])
        if x['kind']==y['kind']=='span':return rank_q(x['rows']+y['rows'])==rank_q(y['rows'])
        if x['kind']=='span'and y['kind']=='ann':return all(dot(v,w)==0 for v in x['rows']for w in y['rows'])
        raise ValueError('Unsupported chart inclusion')
    records={f'X{i}':{'chart':f'L{i}','value':1<<i,'owned':False}for i in range(111)}
    records.update({f'Y{i}':{'chart':'zero','value':1<<(111+i),'owned':False}for i in range(111)})
    counts=Counter();profile=Counter();peak=0;paths={p:[]for p in word['expected_packet_paths']};history=[];handoff=None
    for count,op in enumerate(word['operations'],1):
        kind,name,*rest=op;counts[kind]+=1
        if kind=='INIT':
            if name in records:raise ValueError('Duplicate INIT')
            chart=rest[0];records[name]={'chart':chart,'value':0,'owned':True}
            peak=max(peak,sum(r['owned']for r in records.values()))
            if name in paths:
                if any(records[f'X{j}']['chart']!='Hub'or records[f'X{j}']['value']!=1<<j for j in range(111)):raise ValueError('All originals must be restored at Hub before packet birth')
                paths[name].append(dims[chart])
        elif kind=='ADD':
            target=rest[0]
            if target==name or records[name]['chart']!=records[target]['chart']:raise ValueError('Unavailable ADD')
            records[target]['value']^=records[name]['value']
        elif kind=='MOVE':
            dest=rest[0];rec=records[name];src=rec['chart']
            if not(sub(dest,src)if rec['owned']else sub(src,dest)):raise ValueError('Illegal nested MOVE')
            delta=abs(dims[dest]-dims[src])
            if delta==0:raise ValueError('Zero-rank MOVE')
            profile[delta]+=1;rec['chart']=dest
            if name in paths:paths[name].append(dims[dest])
        elif kind=='CLEAR':
            if not records[name]['owned']:raise ValueError('Original CLEAR')
            del records[name]
        else:raise ValueError('Unknown operation')
        for name in paths:
            if name in records and records[name]['chart']!='Hub':history.append(records[name]['value'])
        if count==word['markers']['handoff']:
            actual={name:{'chart':r['chart'],'value_hex':hex(r['value'])}for name,r in records.items()if r['owned']}
            if actual!=word['expected_owned_at_handoff']:raise ValueError('Actual handoff differs')
            handoff={'records':actual,'counts':dict(counts),'movement_profile':dict(sorted(profile.items()))}
    if paths!=word['expected_packet_paths']:raise ValueError('Packet lifetime mismatch')
    for j in range(111):
        if records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub':raise ValueError('Original X endpoint')
        if records[f'Y{j}']['value']!=1<<(111+j)or records[f'Y{j}']['chart']!=(f'F{j}'if word['closed_partial']else'zero'):raise ValueError('Unserved original Y endpoint')
    live=sum(r['owned']for r in records.values())
    if live!=(0 if word['closed_partial'] else 129):raise ValueError('Owner count mismatch')
    hm=mask(j for j in range(111)if h[j]);allones=(1<<111)-1
    K=[mask(j for j,r in enumerate(roots)if j==i or dot(r,roots[i])==0)for i in range(111)]
    W=[row&(hm if h[i]else allones^hm)for i,row in enumerate(K)]
    G8=[K[i]for i in[1,3,5,10,11,15,30]]+[K[0]&hm]
    desired=G8+[K[i]&hm for i in[1,3,5]]
    rh=rank_f2(history);rj=rank_f2(history+W)
    if(rank_f2(G8),rank_f2(desired),rh,rh+15-rj,rj-15)!=(8,11,18,11,7):raise ValueError('Historical W trace differs')
    if rank_f2(history+desired)!=rh:raise ValueError('Desired eleven-dimensional subcode not in actual history')
    terminal=[int(handoff['records'][f'P{i}']['value_hex'],16)for i in range(8)]
    if rank_f2(terminal)!=8:raise ValueError('Terminal packet rank')
    return {'status':'PASS_ACTUAL_EIGHT_PACKET_ELEVEN_MODE_SOURCE','counts':dict(counts),
            'movement_profile':dict(sorted(profile.items())),'rank_length':sum(k*v for k,v in profile.items()),
            'owned_peak':peak,'live_owned':live,'history_dimension':rh,'history_W_intersection':11,
            'history_outside_W_dimension':7,'initial_seed_rank':8,'terminal_packet_rank':8,
            'missing_target_code_dimensions':4,'packet_paths':paths,'handoff':handoff,
            'all_original_input_columns':222,'completed_targets':[],'closed_partial':word['closed_partial'],
            'new_complete_kappa':False}


def price(profile):
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    def add(*terms):
        out=Counter()
        for c,p in terms:
            for r,v in p.items():out[r]+=c*v
        return dict(out)
    P2=add((36,N),(444,{1:1}), (444,{7*j:1 for j in range(1,9)}))
    T2=add((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
    limiting=add((1,N),(-1,H),(F(1,36),T2),(F(-1,36),P2))
    room=add((1,limiting),(-1,profile))
    rows=[]
    for m in[2,4,6,8]:
        paid=add((F(m,2),P2),(-18*(m-1),N),(18*(m-1),profile))
        target=add((F(m,2),T2),(-18*(m-1),H))
        margin=moment(add((1,target),(-1,paid)))
        rows.append({'m':m,'target_minus_paid_moment':encode(margin),'strictly_positive':margin[0]>0})
    return {'status':'PASS_DIRECTED_ACTUAL_EIGHT_PACKET_PARTIAL_INVOICE','t':'199/200','profile':profile,
            'moment':encode(moment(profile)),'limiting_room':encode(moment(room)),
            'finite_even_m_controls':rows,'scope':'Actual eight-packet partial source, zero Y completions; movement positivity is necessary only. No supplier or new kappa.','new_complete_kappa':False}


if __name__=='__main__':
    here=Path(__file__).parent;repo=next(p for p in here.parents if(p/'AGENTS.md').exists());roots,h,pins=source_geometry(repo)
    out=here/'eight-output';out.mkdir(exist_ok=True)
    result={'status':'PASS_ACTUAL_EIGHT_PACKET_ELEVEN_MODE_SOURCE','source_pins':pins,'receipts':{},'negative_controls':{}}
    for closed in[False,True]:
        word=extend(roots,h,closed);receipt=replay(word,roots,h);name=('CLOSED-'if closed else'')+'WORD.json'
        (out/name).write_text(json.dumps(word,indent=2,sort_keys=True)+'\n');result['receipts'][name]=receipt
    base=extend(roots,h)
    for label,predicate in{
        'omit_last_seed_read':lambda o:o[0]=='ADD'and o[-1]=='P7',
        'omit_last_seed_lifetime':lambda o:o==['MOVE','P7','zero'],
        'omit_unconsumed_original_ascent':lambda o:o[0]=='MOVE'and o[1].startswith('X')and o[-1]=='Hub'
    }.items():
        word=copy.deepcopy(base);i=next(i for i,o in enumerate(word['operations'])if predicate(o));del word['operations'][i]
        word['markers']['handoff']-=1
        try:replay(word,roots,h)
        except(ValueError,KeyError)as exc:result['negative_controls'][label]={'rejected':True,'reason':str(exc)}
        else:raise ValueError('Accepted semantic mutant')
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    bill=price(result['receipts']['CLOSED-WORD.json']['movement_profile']);(out/'PRICE.json').write_text(json.dumps(bill,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'W_trace':11,'history_dimension':18,'rank_length':result['receipts']['CLOSED-WORD.json']['rank_length'],'moment':bill['moment']['lower_decimal'],'limiting_room':bill['limiting_room']['lower_decimal']}))
