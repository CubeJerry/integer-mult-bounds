#!/usr/bin/env python3
"""Actual eight-packet chronological source containing all rank15 singular W.

The fixed source uses independent D8 and spinor data cohorts. This is a
historical acquisition theorem, not a complete receiver decoder.
"""
from pathlib import Path
from collections import Counter
import copy
import json
from shared_facet_source import source_geometry,dot,rank_q,rank_f2,mask
from eight_packet_source import price


D_NORMALS=[[0,0,1,1,0,0,1,-1],[0,1,1,0,-1,0,0,1],
           [0,1,1,0,0,-1,-1,0],[1,1,-1,1,0,0,0,0]]
SPINOR_NORMAL_ROLES=[5,11,21]


def runs(pattern,k):
    if pattern==(1<<k)-1:return [list(range(k))]
    out=[]
    for i in range(k):
        if pattern>>i&1 and not(pattern>>((i-1)%k)&1):
            run=[];j=i
            while pattern>>j&1:
                run.append(j);j=(j+1)%k
            out.append(run)
    return out


def build(roots,h,closed=False):
    specs=[('D',D_NORMALS,0,{5:37,10:55}),
           ('S',[roots[i]for i in SPINOR_NORMAL_ROLES],1,{})]
    charts={'zero':{'kind':'span','rows':[]},'Hub':{'kind':'ann','rows':[]}}
    for j,r in enumerate(roots):
        charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
    ops=[];cache_values={};cache_charts={};source_groups=[];consumed=set();proper_modes=[]
    for j in range(111):ops += [['INIT',f'R{j}',f'L{j}'],['ADD',f'X{j}',f'R{j}']]
    for label,normals,source_class,donor_map in specs:
        k=len(normals);full=(1<<k)-1
        if rank_q(normals)!=k:raise ValueError('Query normals not independent')
        for subset in range(1,full+1):
            charts[f'{label}{subset}']={'kind':'ann','rows':[n for i,n in enumerate(normals)if subset>>i&1]}
        for i in range(k):
            subset=0
            for length in range(1,k+1):
                subset |= 1<<((i+length-1)%k)
                name=f'{label}C{i}_{length}';cache_values[name]=0;cache_charts[name]=f'{label}{subset}'
                ops += [['INIT',name,f'{label}{subset}']]
        groups={j:[]for j in range(1,full+1)}
        for j,r in enumerate(roots):
            if h[j]!=source_class:continue
            pattern=sum(int(dot(r,n)==0)<<i for i,n in enumerate(normals))
            if pattern:groups[pattern].append(j)
        for i,n in enumerate(normals):
            proper_modes.append(mask(j for j,r in enumerate(roots)if h[j]==source_class and dot(r,n)==0))
        for pattern,d in donor_map.items():
            if d in consumed:raise ValueError('Donor original already consumed')
            if any(dot(roots[d],n)!=0 for n in normals):raise ValueError('Donor is not in common chart')
            if h[d]==source_class:raise ValueError('Donor collides with source class')
            if any(dot(roots[d],roots[r])==0 for r in SPINOR_NORMAL_ROLES):raise ValueError('Donor collides with spinor cohort')
            name=f'{label}M{d}';cache_values[name]=1<<d;cache_charts[name]=f'{label}{full}'
            ops += [['INIT',name,f'{label}{full}'],['MOVE',f'X{d}',f'{label}{full}'],['ADD',f'X{d}',name]]
        for pattern,S in groups.items():
            if not S:continue
            if any(j in consumed for j in S):raise ValueError('Original source cohort reused')
            component_runs=runs(pattern,k)
            if len(component_runs)>2 or (len(component_runs)==2)!=(pattern in donor_map):raise ValueError('Unsupported cyclic branch pattern')
            carrier=S[0];others=S[1:];start=f'{label}{pattern}'
            ops += [['MOVE',f'X{carrier}',start]]
            for j in others:
                ops += [['MOVE',f'X{j}',start],['ADD',f'X{j}',f'X{carrier}'],['MOVE',f'X{j}','Hub']]
            values=[(carrier,mask(S))]
            if len(component_runs)==2:
                d=donor_map[pattern]
                if start!=f'{label}{full}':ops += [['MOVE',f'X{d}',start]]
                ops += [['ADD',f'X{carrier}',f'X{d}']]
                values.append((d,mask(S)^(1<<d)))
            deposits=[]
            for run,(record,value)in zip(component_runs,values):
                current=start
                for position in range(len(run)):
                    suffix=run[position:];subset=sum(1<<i for i in suffix);chart=f'{label}{subset}'
                    if chart!=current:ops += [['MOVE',f'X{record}',chart]];current=chart
                    i=run[position];length=len(suffix);name=f'{label}C{i}_{length}'
                    if cache_charts[name]!=chart:raise ValueError('Run suffix not on packet flag')
                    ops += [['ADD',f'X{record}',name]];cache_values[name]^=value;deposits.append(name)
                ops += [['MOVE',f'X{record}','Hub']]
            # Recover the aggregate carrier first, using pure originals.
            for j in others:ops += [['ADD',f'X{j}',f'X{carrier}']]
            if len(component_runs)==2:
                d=donor_map[pattern]
                for j in S:ops += [['ADD',f'X{j}',f'X{d}']]
                consumed.add(d)
            consumed.update(S)
            source_groups.append({'class':label,'pattern':pattern,'sources':S,'original_aggregate_carrier':carrier,
                                  'runs':component_runs,'donor':donor_map.get(pattern),'deposited_caches':deposits})
    for j in range(111):
        if j not in consumed:ops += [['MOVE',f'X{j}','Hub']]
    restored=len(ops)
    W=[mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or dot(r,roots[i])==0))for i in range(111)]
    if rank_f2(proper_modes)!=7 or rank_f2(W+proper_modes)!=15:raise ValueError('Seven proper singular directions')
    basis=list(proper_modes);seed_roles=[];seeds=[]
    for i,row in enumerate(W):
        if rank_f2(basis+[row])>rank_f2(basis):basis.append(row);seeds.append(row);seed_roles.append(i)
        if len(seeds)==8:break
    if seed_roles!=[0,1,2,3,4,10,32,59]or rank_f2(basis)!=15:raise ValueError('Eight-dimensional initial complement')
    expected={f'R{j}':(f'L{j}',1<<j)for j in range(111)}
    expected.update({n:(cache_charts[n],v)for n,v in cache_values.items()})
    paths={};packet=0
    for label,normals,source_class,donor_map in specs:
        k=len(normals);full=(1<<k)-1
        for i in range(k):
            name=f'P{packet}';seed=seeds[packet];ops += [['INIT',name,'Hub']]
            for j in range(111):
                if seed>>j&1:ops += [['ADD',f'X{j}',name]]
            paths[name]=[8];subset=0
            for length in range(1,k+1):
                subset |= 1<<((i+length-1)%k);chart=f'{label}{subset}'
                ops += [['MOVE',name,chart],['ADD',f'{label}C{i}_{length}',name]];paths[name].append(8-length)
            for pattern,d in donor_map.items():
                if i in runs(pattern,k)[1]:ops += [['ADD',f'{label}M{d}',name]]
            ops += [['MOVE',name,'zero']];paths[name].append(0)
            expected[name]=('zero',seed^proper_modes[packet]);packet+=1
    ops += [['INIT','P7','Hub']]
    for j in range(111):
        if seeds[7]>>j&1:ops += [['ADD',f'X{j}','P7']]
    ops += [['MOVE','P7','zero']];paths['P7']=[8,0];expected['P7']=('zero',seeds[7])
    handoff=len(ops)
    if closed:
        for name in expected:ops += [['CLEAR',name]]
        for j in range(111):ops += [['MOVE',f'Y{j}',f'F{j}']]
    return {'schema':'full-singular-history-eight-packet-v1','charts':charts,'operations':ops,'source_groups':source_groups,
            'proper_mode_rows_hex':[hex(w)for w in proper_modes],'initial_seed_fitting_roles':seed_roles,
            'initial_seed_rows_hex':[hex(w)for w in seeds], 'expected_packet_paths':paths,
            'expected_owned_at_handoff':{n:{'chart':c,'value_hex':hex(v)}for n,(c,v)in expected.items()},
            'markers':{'all_X_restored':restored,'handoff':handoff},'closed_partial':closed,
            'completed_targets':[],'new_complete_kappa':False}


def replay(word,roots,h):
    charts=word['charts'];dims={n:rank_q(c['rows'])if c['kind']=='span'else 8-rank_q(c['rows'])for n,c in charts.items()}
    def sub(a,b):
        x,y=charts[a],charts[b]
        if x['kind']==y['kind']=='ann':return rank_q(x['rows']+y['rows'])==rank_q(x['rows'])
        if x['kind']==y['kind']=='span':return rank_q(x['rows']+y['rows'])==rank_q(y['rows'])
        if x['kind']=='span'and y['kind']=='ann':return all(dot(v,w)==0 for v in x['rows']for w in y['rows'])
        raise ValueError('Unsupported chart inclusion')
    records={f'X{j}':{'chart':f'L{j}','value':1<<j,'owned':False}for j in range(111)}
    records.update({f'Y{j}':{'chart':'zero','value':1<<(111+j),'owned':False}for j in range(111)})
    profile=Counter();counts=Counter();history=[];paths={p:[]for p in word['expected_packet_paths']};peak=0;snapshots={}
    for count,o in enumerate(word['operations'],1):
        kind,name,*rest=o;counts[kind]+=1
        if kind=='INIT':
            if name in records:raise ValueError('Duplicate INIT')
            chart=rest[0];records[name]={'chart':chart,'value':0,'owned':True};peak=max(peak,sum(r['owned']for r in records.values()))
            if name in paths:
                if any(records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub'for j in range(111)):raise ValueError('Original not restored before packet birth')
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
        for label,k in word['markers'].items():
            if count==k:
                if any(records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub'for j in range(111)):raise ValueError('Original restoration marker')
                snapshots[label]={'counts':dict(counts),'profile':dict(sorted(profile.items())),
                    'owned':{n:{'chart':r['chart'],'value_hex':hex(r['value'])}for n,r in records.items()if r['owned']}}
    if snapshots['handoff']['owned']!=word['expected_owned_at_handoff']:raise ValueError('Exact handoff mismatch')
    if paths!=word['expected_packet_paths']:raise ValueError('Lifetime changed')
    for j in range(111):
        if records[f'X{j}']['value']!=1<<j or records[f'X{j}']['chart']!='Hub':raise ValueError('Original X endpoint')
        if records[f'Y{j}']['value']!=1<<(111+j)or records[f'Y{j}']['chart']!=(f'F{j}'if word['closed_partial']else'zero'):raise ValueError('Unserved Y endpoint')
    live=sum(r['owned']for r in records.values())
    if live!=(0 if word['closed_partial']else len(word['expected_owned_at_handoff'])):raise ValueError('Owner count')
    W=[mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or dot(r,roots[i])==0))for i in range(111)]
    rh=rank_f2(history)
    if rank_f2(history+W)!=rh:raise ValueError('Full singular W not actually in history')
    seeds=[int(x,16)for x in word['initial_seed_rows_hex']];modes=[int(x,16)for x in word['proper_mode_rows_hex']]
    if rank_f2(seeds)!=8 or rank_f2(modes)!=7 or rank_f2(seeds+modes)!=15:raise ValueError('Complement relation')
    terminal=[int(word['expected_owned_at_handoff'][f'P{i}']['value_hex'],16)for i in range(8)]
    if rank_f2(terminal)!=8:raise ValueError('Terminal rank')
    return {'status':'PASS_FULL_SINGULAR_HISTORY_ON_EIGHT_PACKETS','all_original_input_columns':222,
            'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'owned_peak':peak,'live_owned':live,
            'packet_paths':paths,'initial_seed_rank':8,'proper_acquired_mode_rank':7,
            'history_dimension':rh,'history_W_intersection':15,'history_outside_W_dimension':rh-15,
            'terminal_packet_rank':8,'snapshots':snapshots,'closed_partial':word['closed_partial'],
            'completed_targets':[],'new_complete_kappa':False}


if __name__=='__main__':
    here=Path(__file__).parent;repo=next(p for p in here.parents if(p/'AGENTS.md').exists());roots,h,pins=source_geometry(repo)
    out=here/'full-history-output';out.mkdir(exist_ok=True)
    result={'status':'PASS_FULL_SINGULAR_HISTORY_ON_EIGHT_PACKETS','source_pins':pins,'receipts':{},'negative_controls':{}}
    for closed in[False,True]:
        word=build(roots,h,closed);receipt=replay(word,roots,h);name=('CLOSED-'if closed else'')+'WORD.json'
        (out/name).write_text(json.dumps(word,sort_keys=True,indent=2)+'\n');result['receipts'][name]=receipt
    base=build(roots,h)
    tests={'omit_initial_point_capture':lambda o:o==['ADD','X37','R37'],
           'omit_donor_mask_capture':lambda o:o==['ADD','X37','DM37'],
           'omit_donor_copy':lambda o:o[0]=='ADD'and o[-1]=='X37',
           'omit_packet_unmask':lambda o:o==['ADD','DM37','P2'],
           'omit_proper_mode_read':lambda o:o[0]=='ADD'and o[1]=='DC0_1'and o[-1]=='P0',
           'omit_spinor_mode_read':lambda o:o[0]=='ADD'and o[1]=='SC0_1'and o[-1]=='P4',
           'omit_eighth_seed_read':lambda o:o[0]=='ADD'and o[-1]=='P7'}
    for label,pred in tests.items():
        w=copy.deepcopy(base);i=next(i for i,o in enumerate(w['operations'])if pred(o));del w['operations'][i]
        w['markers']={k:v-(v>i)for k,v in w['markers'].items()}
        try:replay(w,roots,h)
        except(ValueError,KeyError)as exc:result['negative_controls'][label]={'rejected':True,'reason':str(exc)}
        else:raise ValueError('Accepted mutant '+label)
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    bill=price(result['receipts']['CLOSED-WORD.json']['movement_profile']);bill['scope']='Actual complete acquisition of singular W in chronological history, not receiver delivery. All Y values unserved. No full supplier or new kappa.'
    (out/'PRICE.json').write_text(json.dumps(bill,sort_keys=True,indent=2)+'\n')
    r=result['receipts']['CLOSED-WORD.json'];print(json.dumps({'status':result['status'],'history_dimension':r['history_dimension'],'W_trace':15,'rank_length':r['rank_length'],'profile':r['movement_profile'],'moment':bill['moment']['lower_decimal'],'limiting_room':bill['limiting_room']['lower_decimal']}))
