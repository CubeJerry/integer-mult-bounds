#!/usr/bin/env python3
"""Three simultaneous singular-mode innovations via a cyclic source schedule.

Author implementation reuses only the pair package's source and arithmetic
utilities. An independent reviewer must replay the emitted word separately.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json
import copy
from shared_facet_source import source_geometry, dot, rank_q, rank_f2, mask


def build(roots,h,facets=(1,3,5),canonical=False,closed=False):
    if len(set(facets))!=3 or any(h[i] for i in facets):
        raise ValueError('Three distinct class-zero facets required')
    if rank_q([roots[i]for i in facets])!=3:
        raise ValueError('Real normals not independent')
    all_chart=[j for j,r in enumerate(roots)if not h[j]and all(dot(r,roots[i])==0 for i in facets)]
    if len(all_chart)<3:
        raise ValueError('Missing three actual common-chart D8 carriers')
    donors=all_chart[:3]
    patterns={k:[]for k in range(1,8)}
    for j,r in enumerate(roots):
        if h[j]:
            p=sum(int(dot(r,roots[i])==0)<<k for k,i in enumerate(facets))
            if p:patterns[p].append(j)
    singles=[1,2,4];pairs=[3,6,5]
    charts={'zero':{'kind':'span','rows':[]},'Hub':{'kind':'ann','rows':[]},
            'D':{'kind':'ann','rows':[roots[i]for i in facets]}}
    for j,r in enumerate(roots):
        charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
    for i,f in enumerate(facets):
        charts[f'T{i}']={'kind':'ann','rows':[roots[f]]}
        charts[f'E{i}']={'kind':'ann','rows':[roots[facets[i]],roots[facets[(i+1)%3]]]}
    seeds=[{j for j,r in enumerate(roots)if j==f or dot(r,roots[f])==0}if canonical else set()for f in facets]
    native_union=set(sum(patterns.values(),[]))
    moved=set(native_union)|set(donors)
    ops=[]
    for j in sorted(moved):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}']]
    ops += [['INIT','Zt','D']]
    for i in range(3):
        ops += [['INIT',f'Z{i}',f'E{i}'],['INIT',f'C{i}',f'T{i}'],['INIT',f'M{i}','D']]
    for j in patterns[7]:ops += [['MOVE',f'X{j}','D'],['ADD',f'X{j}','Zt'],['MOVE',f'X{j}','Hub']]
    for edge,d in enumerate(donors):
        target=(edge+1)%3
        ops += [['MOVE',f'X{d}','D'],['ADD',f'X{d}',f'M{target}']]
    for edge,(d,p)in enumerate(zip(donors,pairs)):
        target=(edge+1)%3
        for j in patterns[p]:ops += [['MOVE',f'X{j}',f'E{edge}'],['ADD',f'X{j}',f'Z{edge}'],['MOVE',f'X{j}','Hub']]
        ops += [['MOVE',f'X{d}',f'E{edge}'],['ADD',f'Z{edge}',f'X{d}'],
                ['MOVE',f'X{d}',f'T{target}'],['ADD',f'X{d}',f'C{target}'],['MOVE',f'X{d}','Hub']]
    for i,p in enumerate(singles):
        for j in patterns[p]:ops += [['MOVE',f'X{j}',f'T{i}'],['ADD',f'X{j}',f'C{i}'],['MOVE',f'X{j}','Hub']]
    acquired=len(ops)
    for d,p in zip(donors,pairs):
        for j in patterns[p]:ops += [['ADD',f'X{j}',f'X{d}']]
    restored=len(ops)
    extra=set.union(*seeds)-moved
    for j in sorted(extra):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}'],['MOVE',f'X{j}','Hub']]
    moved |= extra
    expected={'Zt':('D',mask(patterns[7]))}
    for i in range(3):
        incoming=(i-1)%3
        expected[f'Z{i}']=(f'E{i}',mask(patterns[pairs[i]]))
        expected[f'C{i}']=(f'T{i}',mask(patterns[singles[i]])^mask(patterns[pairs[incoming]])^(1<<donors[incoming]))
        expected[f'M{i}']=('D',1<<donors[incoming])
        mode=mask(j for j in native_union if dot(roots[j],roots[facets[i]])==0)
        expected[f'P{i}']=('zero',mask(seeds[i])^mode)
    for j in moved:expected[f'R{j}']=(f'L{j}',1<<j)
    for i in range(3):
        ops += [['INIT',f'P{i}','Hub']]
        for j in sorted(seeds[i]):ops += [['ADD',f'X{j}',f'P{i}']]
        ops += [['MOVE',f'P{i}',f'T{i}'],['ADD',f'C{i}',f'P{i}'],
                ['MOVE',f'P{i}',f'E{i}'],['ADD',f'Z{i}',f'P{i}'],
                ['MOVE',f'P{i}','D'],['ADD','Zt',f'P{i}'],['ADD',f'M{i}',f'P{i}'],
                ['MOVE',f'P{i}','zero']]
    handoff=len(ops)
    if closed:
        for name in expected:ops += [['CLEAR',name]]
        for j in range(111):
            if j not in moved:ops += [['MOVE',f'X{j}','Hub']]
            ops += [['MOVE',f'Y{j}',f'F{j}']]
    return {'schema':'singular-cyclic-three-source-v1','facets':list(facets),'donors':donors,
            'patterns':{str(k):v for k,v in patterns.items()},'canonical_seeds':canonical,
            'moved_original_sources':sorted(moved),'closed_partial':closed,
            'charts':charts,'operations':ops,'markers':{'acquired':acquired,'restored':restored,'handoff':handoff},
            'expected_owned_at_handoff':{k:{'chart':c,'value_hex':hex(v)}for k,(c,v)in expected.items()},
            'completed_targets':[],'new_complete_kappa':False}


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
    profile=Counter();counts=Counter();peak=0;paths={f'P{i}':[]for i in range(3)};history=[];snapshots={}
    for count,op in enumerate(word['operations'],1):
        kind,name,*rest=op;counts[kind]+=1
        if kind=='INIT':
            c=rest[0]
            if name in records or c not in charts:raise ValueError('Bad INIT')
            records[name]={'chart':c,'value':0,'owned':True}
            peak=max(peak,sum(r['owned']for r in records.values()))
            if name in paths:
                for j in word['moved_original_sources']:
                    if records[f'X{j}']['chart']!='Hub'or records[f'X{j}']['value']!=1<<j:raise ValueError('Original not restored at packet birth')
                paths[name].append(dims[c])
        elif kind=='ADD':
            dest=rest[0]
            if name==dest or records[name]['chart']!=records[dest]['chart']:raise ValueError('Unavailable ADD')
            records[dest]['value']^=records[name]['value']
        elif kind=='MOVE':
            dest=rest[0];rec=records[name];src=rec['chart']
            if not(sub(dest,src)if rec['owned']else sub(src,dest)):raise ValueError('Illegal monotone MOVE')
            d=abs(dims[src]-dims[dest])
            if not d:raise ValueError('Zero-rank move')
            profile[d]+=1;rec['chart']=dest
            if name in paths:paths[name].append(dims[dest])
        elif kind=='CLEAR':
            if not records[name]['owned']:raise ValueError('Original CLEAR')
            del records[name]
        else:raise ValueError('Bad operation')
        for name in paths:
            if name in records and records[name]['chart']!='Hub':history.append(records[name]['value'])
        for label,k in word['markers'].items():
            if k==count:snapshots[label]={'counts':dict(counts),'profile':dict(sorted(profile.items())),
                        'records':{name:{'chart':r['chart'],'value_hex':hex(r['value'])}for name,r in records.items()if r['owned']}}
    if snapshots['handoff']['records']!=word['expected_owned_at_handoff']:raise ValueError('Handoff mismatch')
    for i in range(111):
        if records[f'X{i}']['value']!=1<<i or records[f'Y{i}']['value']!=1<<(111+i):raise ValueError('Original value mismatch')
        if records[f'X{i}']['chart']!=('Hub'if word['closed_partial']or i in word['moved_original_sources']else f'L{i}'):raise ValueError('X endpoint chart')
        if records[f'Y{i}']['chart']!=(f'F{i}'if word['closed_partial']else 'zero'):raise ValueError('Y endpoint chart')
    if any(p!=[8,7,6,5,0]for p in paths.values()):raise ValueError('Continuous packet path')
    live=sum(r['owned']for r in records.values())
    if live!=(0 if word['closed_partial']else len(word['expected_owned_at_handoff'])):raise ValueError('Owner count')
    hm=mask(i for i in range(111)if h[i]);allones=(1<<111)-1
    K=[mask(j for j,r in enumerate(roots)if j==i or dot(r,roots[i])==0)for i in range(111)]
    W=[row&(hm if h[i]else allones^hm)for i,row in enumerate(K)]
    rh=rank_f2(history);rj=rank_f2(W+history)
    return {'status':'PASS_SINGULAR_CYCLIC_THREE_SOURCE','facets':word['facets'],'donors':word['donors'],
            'canonical_seeds':word['canonical_seeds'],'closed_partial':word['closed_partial'],
            'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'owned_peak':peak,'live_owned':live,
            'packet_paths':paths,'history_dimension':rh,'history_W_intersection':rh+15-rj,
            'history_outside_W_dimension':rj-15,'snapshots':snapshots,
            'all_original_input_columns':222,'completed_targets':[],'new_complete_kappa':False}


if __name__=='__main__':
    here=Path(__file__).parent;repo=next(p for p in here.parents if(p/'AGENTS.md').exists());roots,h,pins=source_geometry(repo)
    out=here/'triple-output';out.mkdir(exist_ok=True)
    results={'status':'PASS_SINGULAR_CYCLIC_THREE_SOURCE','source_pins':pins,'preferred':{},'variants':[],'negative_controls':{}}
    for canonical in (False,True):
        for closed in (False,True):
            word=build(roots,h,canonical=canonical,closed=closed);receipt=replay(word,roots,h)
            name=('CANONICAL-'if canonical else'')+('CLOSED-'if closed else'')+'WORD.json'
            (out/name).write_text(json.dumps(word,sort_keys=True,indent=2)+'\n');results['preferred'][name]=receipt
    for facets in combinations([1,3,5,10,30,61],3):
        for canonical in (False,True):
            word=build(roots,h,facets,canonical,True);receipt=replay(word,roots,h)
            p=word['patterns'];e=sum(len(p[str(j)])for j in[1,2,4]);pair=sum(len(p[str(j)])for j in[3,5,6]);t=len(p['7'])
            expected={1:e+18,2:pair,3:t,4:t+3,5:pair+3,6:e,7:219-e-pair-t}
            if receipt['movement_profile']!=expected or receipt['rank_length']!=1578:raise ValueError('Closed profile formula')
            if canonical and receipt['history_W_intersection']!=6:raise ValueError('Three independent W innovations')
            results['variants'].append({k:v for k,v in receipt.items()if k!='snapshots'})
    base=build(roots,h)
    predicates={'omit_triple_capture':lambda o:o[0]=='ADD'and o[-1]=='Zt',
                'omit_pair_capture':lambda o:o[0]=='ADD'and o[-1]=='Z0',
                'omit_pure_donor_mask':lambda o:o==['ADD','X7','M1'],
                'omit_original_injection':lambda o:o==['ADD','Z0','X7'],
                'omit_original_restore':lambda o:o[0]=='ADD'and o[-1]=='X7'and o[1]!='Z0',
                'omit_shared_read':lambda o:o==['ADD','Zt','P0'],
                'omit_mask_unread':lambda o:o==['ADD','M0','P0'],
                'omit_pair_packet_read':lambda o:o==['ADD','Z0','P0']}
    for label,pred in predicates.items():
        word=copy.deepcopy(base);i=next(i for i,o in enumerate(word['operations'])if pred(o));del word['operations'][i]
        word['markers']={k:v-(v>i)for k,v in word['markers'].items()}
        try:replay(word,roots,h)
        except(ValueError,KeyError)as exc:results['negative_controls'][label]={'rejected':True,'reason':str(exc)}
        else:raise ValueError('Accepted mutant '+label)
    (out/'RESULT.json').write_text(json.dumps(results,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':results['status'],'variants':len(results['variants']),
                      'negative_controls':len(results['negative_controls']),
                      'preferred_profile':results['preferred']['CLOSED-WORD.json']['movement_profile'],
                      'canonical_history_W_intersection':results['preferred']['CANONICAL-WORD.json']['history_W_intersection']}))
