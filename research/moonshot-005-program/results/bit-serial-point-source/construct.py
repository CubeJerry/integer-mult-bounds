#!/usr/bin/env python3
"""Literal four-D/three-S source with a three-receiver serial packet.

Composes the admitted orthogonal staircase with the point-seeded source.
Original source inputs provide actual corrections before Hub restoration;
ground public-y prefix masks make both packet feedbacks exact. All source
data are imported read-only from --repo. No complete supplier is claimed.
"""
from pathlib import Path
from collections import Counter
import copy,json,sys
TARGET=34
D_ORDER=[0,3,1,2]
S_ROLES=[34,5,11]
SECOND_TARGET=17

def configure(repo):
    source=Path(repo)/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a'
    sys.path.insert(0,str(source))
    import shared_facet_source as g
    import full_singular_history as f
    import eight_packet_source as e
    globals().update({name:getattr(g,name)for name in['source_geometry','dot','rank_q','rank_f2','mask']})
    globals().update(D_NORMALS=f.D_NORMALS,runs=f.runs,price=e.price)
    return g.source_geometry(Path(repo))

def build(roots,h,closed=False):
    coupled=True
    db=D_NORMALS+[roots[TARGET]]
    specs=[('D',[db[i]for i in D_ORDER],0,4),('S',[roots[i]for i in S_ROLES],1,3)]
    charts={'zero':{'kind':'span','rows':[]},'Hub':{'kind':'ann','rows':[]}}
    for j,r in enumerate(roots):
        charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
    def ch(label,subset):
        if (label=='D'and subset==16)or(label=='S'and subset==1):return f'F{TARGET}'
        if label=='S'and subset==8:return f'F{SECOND_TARGET}'
        return f'{label}{subset}'
    charts['PAIR_K']={'kind':'ann','rows':[roots[i]for i in[34,5,11,17]]}
    charts['TRIPLE_K']={'kind':'ann','rows':[roots[i]for i in[34,5,11,17,9]]}
    ops=[];cache_values={};cache_charts={};source_groups=[];consumed=set();modes=[];mask_reads={};mask_routes=[]
    for j in range(111):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}']]
    # This actual ground record is the arbitrary public-input mask; no y=0 grant.
    ops += [['INIT','YM','zero'],['ADD',f'Y{TARGET}','YM']]
    cache_values['YM']=1<<(111+TARGET);cache_charts['YM']='zero'
    ops += [['INIT','PAIR_C17','F34'],['INIT','TRIPLE_C9','PAIR_K'],['INIT','YM17','zero'],['ADD','Y17','YM17'],['ADD','Y34','Y17'],['ADD','Y17','Y9']]
    cache_values['PAIR_C17']=1<<17;cache_charts['PAIR_C17']='F34'
    cache_values['TRIPLE_C9']=1<<9;cache_charts['TRIPLE_C9']='PAIR_K'
    cache_values['YM17']=1<<128;cache_charts['YM17']='zero'
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
            rs=sorted(runs(pattern,k),key=lambda run:-len(run));carrier=S[0];donors=S[1:len(rs)];others=S[1:]
            if len(rs)>len(S):raise ValueError('Insufficient actual internal donors')
            start=ch(label,pattern)
            ops += [['MOVE',f'X{carrier}',start]]
            for j in others:ops += [['MOVE',f'X{j}',start]]
            masks=[]
            for d,run in zip(donors,rs[1:]):
                if len(run)!=1:raise ValueError('This local-mask construction requires a singleton masked run')
                recipient=run[0];prefix=0
                for length in range(1,k+1):
                    prefix |= 1<<((recipient+length-1)%k)
                    if prefix&pattern==pattern:break
                dest=ch(label,prefix)
                name=f'{label}M{pattern}_{d}';cache_values[name]=1<<d;cache_charts[name]=dest
                ops += [['INIT',name,start],['ADD',f'X{d}',name]]
                if dest!=start:ops += [['MOVE',name,dest]]
                mask_routes.append({'record':name,'start':start,'destination':dest,'recipient_query':[label,recipient],
                                    'rank_drop':rank_q(charts[dest]['rows'])-rank_q(charts[start]['rows'])})
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
    roles=selected[1:5]+[TARGET]+selected[5:];seeds=[W[i]for i in roles];seeds[4]=(1<<TARGET)^(1<<SECOND_TARGET)^(1<<9)^modes[4]
    if len(seeds)!=8 or rank_f2(seeds)!=8 or rank_f2(seeds+modes)!=15:raise ValueError('Seed assignment')
    ops += [['MOVE','Y34','PAIR_K'],['ADD','TRIPLE_C9','Y34'],
            ['MOVE','Y34','S7'],['ADD','SC0_3','Y34'],
            ['MOVE','Y34','S3'],['ADD','SC0_2','Y34'],
            ['MOVE','Y34','F34'],['ADD','SC0_1','Y34'],['ADD','PAIR_C17','Y34'],
            ['MOVE','Y17','PAIR_K'],['ADD','TRIPLE_C9','Y17'],['MOVE','Y9','TRIPLE_K']]
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
                for m in mask_reads[(label,i)]:
                    if cache_charts[m]==chart:ops += [['ADD',m,name]]
            if packet==4:
                ops += [['MOVE',name,'PAIR_K'],['ADD',name,'Y17'],['ADD','Y17',name],['MOVE','Y17','F17'],['MOVE',name,'TRIPLE_K'],['ADD',name,'Y9'],['MOVE','Y9','F9']]
                paths[name]+=[4,3]
            ops += [['MOVE',name,'zero']];paths[name].append(0)
            value=seed^modes[packet]
            if packet==4 and coupled:
                value^=(1<<TARGET)^(1<<17)
                ops += [['ADD','YM',name],['ADD','YM17',name]]
            expected[name]=('zero',value);packet+=1
    ops += [['INIT','P7','Hub']]
    for j in range(111):
        if seeds[7]>>j&1:ops += [['ADD',f'X{j}','P7']]
    ops += [['MOVE','P7','zero']];paths['P7']=[8,0];expected['P7']=('zero',seeds[7])
    handoff=len(ops)
    if closed:
        for name in expected:ops += [['CLEAR',name]]
        for j in range(111):
            if j not in[TARGET,SECOND_TARGET,9]:ops += [['MOVE',f'Y{j}',f'F{j}']]
    # Intercept actual pure source coordinates before cohort alteration.
    # Both splits preserve original monotonicity and total rank length.
    raw_ops=ops;ops=[];index_map={};captured=set()
    for old_index,op in enumerate(raw_ops):
        index_map[old_index]=len(ops)
        if op==['MOVE','X17','Hub'] and 'X17' not in captured:
            ops += [['MOVE','X17','F34'],['ADD','X17','PAIR_C17']];captured.add('X17')
        if op==['MOVE','X9','S7'] and 'X9' not in captured:
            ops += [['MOVE','X9','PAIR_K'],['ADD','X9','TRIPLE_C9']];captured.add('X9')
        ops.append(op)
    index_map[len(raw_ops)]=len(ops)
    if captured!={'X17','X9'}:raise ValueError('Actual correction capture not found')
    restored=index_map[restored];prepared=index_map[prepared];handoff=index_map[handoff]
    for key in ['first_add_index','second_add_index']:
        exchange[key]=index_map[exchange[key]]
    return {'schema':'serial-point-four-D-three-S-three-output-source-v1','charts':charts,'operations':ops,
            'source_groups':source_groups,'proper_mode_rows_hex':[hex(w)for w in modes],
            'initial_seed_fitting_roles':[role if i!=4 else None for i,role in enumerate(roles)],'off_code_seed_packet':4,'off_code_seed_role':None,'off_code_seed_formula':'e34+e17+e9+M34','initial_seed_rows_hex':[hex(w)for w in seeds],
            'expected_packet_paths':paths,'expected_owned_at_handoff':{n:{'chart':c,'value_hex':hex(v)}for n,(c,v)in expected.items()},
            'markers':{'all_X_restored':restored,'Y_correction_prepared':prepared,'handoff':handoff},
            'exchange':exchange,'coupled':coupled,'closed_partial':closed,'completed_targets':[TARGET,SECOND_TARGET,9],
            'new_complete_kappa':False,'mask_routes':mask_routes,'mask_descent_rank_length':sum(m['rank_drop']for m in mask_routes)}


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
    profile=Counter();counts=Counter();dirty_clears=0;history=[];paths={p:[]for p in word['expected_packet_paths']};peak=0;snapshots={};exchange_values=[]
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
            dirty_clears+=bool(records[name]['value'])
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
                    expected=(1<<(111+TARGET))^(1<<17)^(1<<9)^mask(j for j,r in enumerate(roots)if h[j]and dot(r,roots[TARGET])==0)
                    if records[f'Y{TARGET}']['value']!=expected or records[f'Y{TARGET}']['chart']!=f'F{TARGET}':raise ValueError('Actual Y correction missing')
                snapshots[label]={'counts':dict(counts),'profile':dict(sorted(profile.items())),
                    'owned':{n:{'chart':r['chart'],'value_hex':hex(r['value'])}for n,r in records.items()if r['owned']}}
    if snapshots['handoff']['owned']!=word['expected_owned_at_handoff']:raise ValueError('Exact handoff mismatch')
    if paths!=word['expected_packet_paths']:raise ValueError('Packet lifetime changed')
    for j in range(111):
        if records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub':raise ValueError('Original X endpoint')
        expected=(1<<(111+j))^((1<<j)if j in word['completed_targets']else 0)
        chart=f'F{j}'if(word['closed_partial']or j in word['completed_targets'])else'zero'
        if records[f'Y{j}']['value']!=expected or records[f'Y{j}']['chart']!=chart:raise ValueError('Original Y endpoint')
    W=[mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or dot(r,roots[i])==0))for i in range(111)]
    rh=rank_f2(history);wt=rh+15-rank_f2(history+W)
    if wt!=15:raise ValueError('Full singular W lost from actual coupled history')
    terminal=[int(word['expected_owned_at_handoff'][f'P{i}']['value_hex'],16)for i in range(8)]
    if any(v>>111 for v in terminal):raise ValueError('Arbitrary public-y mask remains in terminal packet')
    return {'status':'PASS_SERIAL_POINT_THREE_OUTPUT_W_HISTORY','all_original_input_columns':222,
            'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'owned_peak':peak,'dirty_clears':dirty_clears,
            'live_owned':sum(r['owned']for r in records.values()),'packet_paths':paths,
            'history_dimension':rh,'history_W_intersection':wt,
            'history_public_y_projection_rank':rank_f2([v>>111 for v in history]),
            'history_pure_X_dimension':rh-rank_f2([v>>111 for v in history]),
            'terminal_packet_rank':rank_f2(terminal),'exchange_values':exchange_values,
            'snapshots':snapshots,'mask_descent_rank_length':word['mask_descent_rank_length'],
            'closed_partial':word['closed_partial'],'coupled':word['coupled'],'completed_targets':[TARGET,SECOND_TARGET,9],
            'new_complete_kappa':False}


