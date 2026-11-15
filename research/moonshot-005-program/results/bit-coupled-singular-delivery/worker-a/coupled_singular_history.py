#!/usr/bin/env python3
"""Actual full-W source with one public-Y/packet singular-through exchange."""
from pathlib import Path
from collections import Counter
import copy
import json
from shared_facet_source import source_geometry,dot,rank_q,rank_f2,mask
from full_singular_history import D_NORMALS,runs
from eight_packet_source import price

TARGET=34
D_ORDER=[0,3,1,2,4]
S_ROLES=[34,5,11]


def build(roots,h,closed=False,coupled=True):
    db=D_NORMALS+[roots[TARGET]]
    specs=[('D',[db[i]for i in D_ORDER],0,4),('S',[roots[i]for i in S_ROLES],1,3)]
    charts={'zero':{'kind':'span','rows':[]},'Hub':{'kind':'ann','rows':[]}}
    for j,r in enumerate(roots):
        charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
    def ch(label,subset):
        if (label=='D'and subset==16)or(label=='S'and subset==1):return f'F{TARGET}'
        return f'{label}{subset}'
    ops=[];cache_values={};cache_charts={};source_groups=[];consumed=set();modes=[];mask_reads={}
    for j in range(111):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}']]
    # This actual ground record is the arbitrary public-input mask; no y=0 grant.
    ops += [['INIT','YM','zero'],['ADD',f'Y{TARGET}','YM']]
    cache_values['YM']=1<<(111+TARGET);cache_charts['YM']='zero'
    for label,normals,source_class,active in specs:
        k=len(normals);full=(1<<k)-1
        if rank_q(normals)!=k:raise ValueError('Dependent query normals')
        for subset in range(1,full+1):charts[ch(label,subset)]={'kind':'ann','rows':[n for i,n in enumerate(normals)if subset>>i&1]}
        for i in range(k):
            subset=0;mask_reads[(label,i)]=[]
            for length in range(1,k+1):
                subset |= 1<<((i+length-1)%k);name=f'{label}C{i}_{length}'
                cache_values[name]=0;cache_charts[name]=ch(label,subset);ops += [['INIT',name,ch(label,subset)]]
        groups={j:[]for j in range(1,full+1)}
        for j,r in enumerate(roots):
            if h[j]==source_class:
                pattern=sum(int(dot(r,n)==0)<<i for i,n in enumerate(normals))
                if pattern:groups[pattern].append(j)
        for n in normals[:active]:modes.append(mask(j for j,r in enumerate(roots)if h[j]==source_class and dot(r,n)==0))
        for pattern,S in groups.items():
            if not S:continue
            if any(j in consumed for j in S):raise ValueError('Source original reused')
            rs=runs(pattern,k);carrier=S[0];donors=S[1:len(rs)];others=S[1:]
            if len(rs)>len(S):raise ValueError('Insufficient actual internal donors')
            start=ch(label,pattern)
            ops += [['MOVE',f'X{carrier}',start]]
            for j in others:ops += [['MOVE',f'X{j}',start]]
            masks=[]
            for d,run in zip(donors,rs[1:]):
                name=f'{label}M{pattern}_{d}';cache_values[name]=1<<d;cache_charts[name]=ch(label,full)
                ops += [['INIT',name,start],['ADD',f'X{d}',name]]
                if pattern!=full:ops += [['MOVE',name,ch(label,full)]]
                for i in run:mask_reads[(label,i)].append(name)
                masks.append(name)
            for j in others:ops += [['ADD',f'X{j}',f'X{carrier}']]
            for j in others:
                if j not in donors:ops += [['MOVE',f'X{j}','Hub']]
            for d in donors:ops += [['ADD',f'X{carrier}',f'X{d}']]
            values=[(carrier,mask(S))]+[(d,mask(S)^(1<<d))for d in donors]
            deposits=[]
            for run,(record,value)in zip(rs,values):
                current=start
                for pos in range(len(run)):
                    suffix=run[pos:];subset=sum(1<<i for i in suffix);chart=ch(label,subset)
                    if chart!=current:ops += [['MOVE',f'X{record}',chart]];current=chart
                    name=f'{label}C{run[pos]}_{len(suffix)}'
                    if cache_charts[name]!=chart:raise ValueError('Cyclic flag mismatch')
                    ops += [['ADD',f'X{record}',name]];cache_values[name]^=value;deposits.append(name)
                ops += [['MOVE',f'X{record}','Hub']]
            # Reverse the actual elementary recoding: donor first, then aggregate.
            for d in donors:ops += [['ADD',f'X{carrier}',f'X{d}']]
            for j in others:ops += [['ADD',f'X{j}',f'X{carrier}']]
            consumed.update(S)
            source_groups.append({'class':label,'pattern':pattern,'sources':S,'carrier':carrier,'donors':donors,'runs':rs,'mask_records':masks,'deposits':deposits})
    for j in range(111):
        if j not in consumed:ops += [['MOVE',f'X{j}','Hub']]
    restored=len(ops)
    W=[mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or dot(r,roots[i])==0))for i in range(111)]
    if rank_f2(modes)!=7 or rank_f2(modes+[W[TARGET]])!=8:raise ValueError('Target seed not an initial-complement direction')
    basis=list(modes)+[W[TARGET]];selected=[TARGET]
    for i,row in enumerate(W):
        if rank_f2(basis+[row])>len(basis):basis.append(row);selected.append(i)
        if len(selected)==8:break
    if len(basis)!=15:raise ValueError('Initial W complement')
    roles=selected[1:5]+[TARGET]+selected[5:];seeds=[W[i]for i in roles]
    if len(seeds)!=8 or rank_f2(seeds)!=8 or rank_f2(seeds+modes)!=15:raise ValueError('Seed assignment')
    # Actual Y34 correction: reverse its D5 packet flag, stopping at F34.
    query=4;k=5;prefix=[];subset=0
    for length in range(1,k+1):subset|=1<<((query+length-1)%k);prefix.append(ch('D',subset))
    ops += [['MOVE',f'Y{TARGET}',prefix[-1]]]
    for name in mask_reads[('D',query)]:ops += [['ADD',name,f'Y{TARGET}']]
    for length in range(k,0,-1):
        if length<k:ops += [['MOVE',f'Y{TARGET}',prefix[length-1]]]
        ops += [['ADD',f'DC{query}_{length}',f'Y{TARGET}']]
    prepared=len(ops)
    expected={f'R{j}':(f'L{j}',1<<j)for j in range(111)}
    expected.update({n:(cache_charts[n],v)for n,v in cache_values.items()})
    paths={};packet=0;exchange=None
    for label,normals,source_class,active in specs:
        k=len(normals)
        for i in range(active):
            name=f'P{packet}';seed=seeds[packet];ops += [['INIT',name,'Hub']]
            for j in range(111):
                if seed>>j&1:ops += [['ADD',f'X{j}',name]]
            paths[name]=[8];subset=0
            for length in range(1,k+1):
                subset |= 1<<((i+length-1)%k);chart=ch(label,subset);ops += [['MOVE',name,chart]];paths[name].append(8-length)
                if packet==4 and length==1:
                    first=len(ops);ops += [['ADD',name,f'Y{TARGET}']]
                    if coupled:ops += [['ADD',f'Y{TARGET}',name]]
                    exchange={'first_add_index':first,'second_add_index':first+1 if coupled else None,'chart':chart,'packet':name,'receiver':f'Y{TARGET}'}
                ops += [['ADD',f'{label}C{i}_{length}',name]]
            for m in mask_reads[(label,i)]:ops += [['ADD',m,name]]
            ops += [['MOVE',name,'zero']];paths[name].append(0)
            value=seed^modes[packet]
            if packet==4 and coupled:
                value^=1<<TARGET
                ops += [['ADD','YM',name]]
            expected[name]=('zero',value);packet+=1
    ops += [['INIT','P7','Hub']]
    for j in range(111):
        if seeds[7]>>j&1:ops += [['ADD',f'X{j}','P7']]
    ops += [['MOVE','P7','zero']];paths['P7']=[8,0];expected['P7']=('zero',seeds[7])
    handoff=len(ops)
    if closed:
        for name in expected:ops += [['CLEAR',name]]
        for j in range(111):
            if j!=TARGET:ops += [['MOVE',f'Y{j}',f'F{j}']]
    return {'schema':'coupled-singular-history-eight-packet-v1','charts':charts,'operations':ops,
            'source_groups':source_groups,'proper_mode_rows_hex':[hex(w)for w in modes],
            'initial_seed_fitting_roles':roles,'initial_seed_rows_hex':[hex(w)for w in seeds],
            'expected_packet_paths':paths,'expected_owned_at_handoff':{n:{'chart':c,'value_hex':hex(v)}for n,(c,v)in expected.items()},
            'markers':{'all_X_restored':restored,'Y_correction_prepared':prepared,'handoff':handoff},
            'exchange':exchange,'coupled':coupled,'closed_partial':closed,'completed_targets':[TARGET],
            'new_complete_kappa':False,'mask_descent_rank_length':sum((5-g['pattern'].bit_count())*len(g['donors'])for g in source_groups if g['class']=='D')}


def replay(word,roots,h):
    charts=word['charts'];dims={n:rank_q(c['rows'])if c['kind']=='span'else 8-rank_q(c['rows'])for n,c in charts.items()}
    def sub(a,b):
        x,y=charts[a],charts[b]
        if x['kind']==y['kind']=='ann':return rank_q(x['rows']+y['rows'])==rank_q(x['rows'])
        if x['kind']==y['kind']=='span':return rank_q(x['rows']+y['rows'])==rank_q(y['rows'])
        if x['kind']=='span'and y['kind']=='ann':return all(dot(v,w)==0 for v in x['rows']for w in y['rows'])
        raise ValueError('Unsupported inclusion')
    records={f'X{j}':{'chart':f'L{j}','value':1<<j,'owned':False}for j in range(111)}
    records.update({f'Y{j}':{'chart':'zero','value':1<<(111+j),'owned':False}for j in range(111)})
    profile=Counter();counts=Counter();history=[];paths={p:[]for p in word['expected_packet_paths']};peak=0;snapshots={};exchange_values=[]
    for count,o in enumerate(word['operations'],1):
        kind,name,*rest=o;counts[kind]+=1
        if kind=='INIT':
            if name in records:raise ValueError('Duplicate owner')
            chart=rest[0];records[name]={'chart':chart,'value':0,'owned':True};peak=max(peak,sum(r['owned']for r in records.values()))
            if name in paths:
                if any(records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub'for j in range(111)):raise ValueError('Source unavailable before packet birth')
                paths[name].append(dims[chart])
        elif kind=='ADD':
            target=rest[0]
            if name==target or records[name]['chart']!=records[target]['chart']:raise ValueError('Unavailable ADD')
            records[target]['value']^=records[name]['value']
        elif kind=='MOVE':
            dest=rest[0];r=records[name];src=r['chart']
            if not(sub(dest,src)if r['owned']else sub(src,dest)):raise ValueError('Illegal monotone MOVE')
            delta=abs(dims[src]-dims[dest])
            if not delta:raise ValueError('Zero-rank MOVE')
            profile[delta]+=1;r['chart']=dest
            if name in paths:paths[name].append(dims[dest])
        elif kind=='CLEAR':
            if not records[name]['owned']:raise ValueError('Original CLEAR')
            del records[name]
        else:raise ValueError('Unknown operation')
        for name in paths:
            if name in records and records[name]['chart']!='Hub':history.append(records[name]['value'])
        if count-1 in[word['exchange']['first_add_index'],word['exchange']['second_add_index']]:
            exchange_values.append({'operation_index':count-1,'Y_hex':hex(records[f'Y{TARGET}']['value']),'P_hex':hex(records['P4']['value'])})
        for label,k in word['markers'].items():
            if count==k:
                if any(records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub'for j in range(111)):raise ValueError('Original restoration marker')
                if label=='Y_correction_prepared':
                    expected=(1<<(111+TARGET))^mask(j for j,r in enumerate(roots)if h[j]==h[TARGET]and dot(r,roots[TARGET])==0)
                    if records[f'Y{TARGET}']['value']!=expected or records[f'Y{TARGET}']['chart']!=f'F{TARGET}':raise ValueError('Actual Y correction missing')
                snapshots[label]={'counts':dict(counts),'profile':dict(sorted(profile.items())),
                    'owned':{n:{'chart':r['chart'],'value_hex':hex(r['value'])}for n,r in records.items()if r['owned']}}
    if snapshots['handoff']['owned']!=word['expected_owned_at_handoff']:raise ValueError('Exact handoff mismatch')
    if paths!=word['expected_packet_paths']:raise ValueError('Packet lifetime changed')
    for j in range(111):
        if records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub':raise ValueError('Original X endpoint')
        expected=(1<<(111+j))^((1<<j)if j==TARGET else 0)
        chart=f'F{j}'if(word['closed_partial']or j==TARGET)else'zero'
        if records[f'Y{j}']['value']!=expected or records[f'Y{j}']['chart']!=chart:raise ValueError('Original Y endpoint')
    W=[mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or dot(r,roots[i])==0))for i in range(111)]
    rh=rank_f2(history);wt=rh+15-rank_f2(history+W)
    if wt!=15:raise ValueError('Full singular W lost from actual coupled history')
    terminal=[int(word['expected_owned_at_handoff'][f'P{i}']['value_hex'],16)for i in range(8)]
    if any(v>>111 for v in terminal):raise ValueError('Arbitrary public-y mask remains in terminal packet')
    return {'status':'PASS_ACTUAL_SINGULAR_Y_CELL_WITH_FULL_W_HISTORY','all_original_input_columns':222,
            'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'owned_peak':peak,
            'live_owned':sum(r['owned']for r in records.values()),'packet_paths':paths,
            'history_dimension':rh,'history_W_intersection':wt,
            'history_public_y_projection_rank':rank_f2([v>>111 for v in history]),
            'history_pure_X_dimension':rh-rank_f2([v>>111 for v in history]),
            'terminal_packet_rank':rank_f2(terminal),'exchange_values':exchange_values,
            'snapshots':snapshots,'mask_descent_rank_length':word['mask_descent_rank_length'],
            'closed_partial':word['closed_partial'],'coupled':word['coupled'],'completed_targets':[TARGET],
            'new_complete_kappa':False}


if __name__=='__main__':
    here=Path(__file__).parent;repo=next(p for p in here.parents if(p/'AGENTS.md').exists());roots,h,pins=source_geometry(repo)
    out=here/'coupled-output';out.mkdir(exist_ok=True)
    result={'status':'PASS_ACTUAL_SINGULAR_Y_CELL_WITH_FULL_W_HISTORY','source_pins':pins,'receipts':{},'negative_controls':{}}
    for coupled in[False,True]:
        for closed in[False,True]:
            word=build(roots,h,closed,coupled);receipt=replay(word,roots,h)
            name=('COUPLED-'if coupled else'UNCOPLED-')+('CLOSED-'if closed else'')+'WORD.json'
            (out/name).write_text(json.dumps(word,sort_keys=True,indent=2)+'\n');result['receipts'][name]=receipt
    base=build(roots,h,False,True)
    predicates={'omit_y_mask':lambda o:o==['ADD',f'Y{TARGET}','YM'],
                'omit_internal_mask_capture':lambda o:o[0]=='ADD'and o[-1].startswith('DM'),
                'omit_mask_descent':lambda o:o[0]=='MOVE'and o[1].startswith('DM'),
                'omit_receiver_correction':lambda o:o==['ADD','DC4_1',f'Y{TARGET}'],
                'omit_receiver_delivery':lambda o:o==['ADD','P4',f'Y{TARGET}'],
                'omit_singular_exchange':lambda o:o==['ADD',f'Y{TARGET}','P4'],
                'omit_ground_unmask':lambda o:o==['ADD','YM','P4']}
    for label,pred in predicates.items():
        bad=copy.deepcopy(base);i=next(i for i,o in enumerate(bad['operations'])if pred(o));del bad['operations'][i]
        bad['markers']={k:v-(v>i)for k,v in bad['markers'].items()}
        bad['exchange']={k:(v-(v>i)if isinstance(v,int)else v)for k,v in bad['exchange'].items()}
        try:replay(bad,roots,h)
        except(ValueError,KeyError)as exc:result['negative_controls'][label]={'rejected':True,'reason':str(exc)}
        else:raise ValueError('Accepted semantic mutant '+label)
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    bill=price(result['receipts']['COUPLED-CLOSED-WORD.json']['movement_profile']);bill['scope']='Actual Y34 complete and W15 retained in history through one singular public-Y/packet cell. Remaining110 receivers unserved. No complete supplier or new kappa.'
    (out/'PRICE.json').write_text(json.dumps(bill,sort_keys=True,indent=2)+'\n')
    r=result['receipts']['COUPLED-CLOSED-WORD.json'];print(json.dumps({k:r[k]for k in['status','counts','movement_profile','rank_length','history_dimension','history_W_intersection','history_pure_X_dimension','terminal_packet_rank']}));print(json.dumps({'moment':bill['moment']['lower_decimal'],'limiting_room':bill['limiting_room']['lower_decimal']}))
