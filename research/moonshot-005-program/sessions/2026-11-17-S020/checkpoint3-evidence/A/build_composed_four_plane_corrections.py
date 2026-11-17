"""Four disjoint-source, disjoint-receiver proper correction gadgets.

The first two use complementary coordinate quartets and independent Y couriers.
The other two use sign inputs only. No original's lower route is restarted.
"""
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE, SHA, HELPER, CHECK, module
from build_four_plane_correction import replay_general


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    h=module(a.repo/HELPER,'composed_helper');e=module(a.repo/CHECK,'composed_geometry')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots']
    E=[[int(i==j)for j in range(8)]for i in range(8)]
    charts={'zero':{'kind':'span','rows':[]},'Hub':{'kind':'span','rows':E}}
    for i,r in enumerate(R):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
    ops=[];sem=defaultdict(list);owners=[]
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    def emit(op,key):
        sem[key].append(len(ops));ops.append(op);kind,n,*q=op
        if kind=='INIT':values[n]=0;at[n]=q[0];owners.append(n)
        elif kind=='ADD':values[q[0]]^=values[n]
        elif kind=='MOVE':at[n]=q[0]
        elif kind=='CLEAR':del values[n],at[n];owners.remove(n)
    def add(x,y,key):emit(['ADD',x,y],key)
    def move(x,p,key):emit(['MOVE',x,p],key)
    for i in range(111):emit(['INIT',f'NATIVE_{i}',f'L{i}'],'native_birth');add(f'X{i}',f'NATIVE_{i}','native_capture')
    configs=[([0,1,6,7],[0,1],[6,7],[2,3]),([2,3,4,5],[2,4],[3,5],[0,1]),
             ([0,1,4,5],[0,5],[1,4],[]),([0,2,5,7],[0,7],[2,5],[])]
    expected=[0]*111;used_sources=set();served=set();data=[]
    for k,(support,ab,cd,couriers)in enumerate(configs):
        tag=f'G{k}';aa,bb=ab;cc,dd=cd;axes=bool(couriers)
        signs=[i for i,r in enumerate(R)if[j for j,x in enumerate(r)if x]==support]
        assert len(signs)==8
        sources=signs+(support if axes else[])
        assert not used_sources.intersection(sources) and all(at[f'X{i}']==f'L{i}'for i in sources)
        used_sources.update(sources);charts[tag]={'kind':'span','rows':[E[i]for i in support]}
        queries={};qrows={};pairs={}
        for s in[1,-1]:
            for label,(x,y),other in [('A',ab,cd),('B',cd,ab)]:
                q=f'{tag}_{label}{s}';I=[i for i in signs if R[i][x]==s*R[i][y]]
                charts[q]={'kind':'span','rows':[R[i]for i in I]}
                candidates=[i for i,r in enumerate(R)if[j for j in support if r[j]]==sorted([x,y])and r[x]==-s*r[y]]
                queries[q]=[i for i in candidates if i not in served]
                qrows[q]=sum(1<<i for i in I+(other if axes else[]))
            for t in[1,-1]:
                I=[i for i in signs if R[i][aa]==s*R[i][bb]and R[i][cc]==t*R[i][dd]];assert len(I)==2
                P=f'{tag}_PAIR_{s}_{t}';charts[P]={'kind':'span','rows':[R[i]for i in I]}
                early=f'{tag}_A{s}'if s==t else f'{tag}_B{t}';late=f'{tag}_B{t}'if s==t else f'{tag}_A{s}'
                pairs[P]={'roles':I,'early':early,'late':late}
        current=sorted(i for I in queries.values()for i in I)
        assert len(current)==len(set(current))and not served.intersection(current)
        assert all(at[f'Y{i}']=='zero'for i in current+couriers)
        served.update(current);start=len(ops)
        if axes:
            for q,courier in[(f'{tag}_A-1',couriers[0]),(f'{tag}_B-1',couriers[1])]:
                for i in queries[q]:add(f'Y{courier}',f'Y{i}',f'{tag}:ground_Y_inverse')
        inverse=[]
        for P,info in pairs.items():
            x,y=info['roles'];move(f'X{x}',P,f'{tag}:pair_arrival');move(f'X{y}',P,f'{tag}:pair_arrival')
            add(f'X{y}',f'X{x}',f'{tag}:pair_encode');inverse.append((x,y))
            for i in queries[info['early']]:move(f'Y{i}',P,f'{tag}:early_query_arrival');add(f'X{x}',f'Y{i}',f'{tag}:early_pair_read')
            move(f'X{y}',tag,f'{tag}:raw_donor_return');move(f'X{x}',info['late'],f'{tag}:later_pair_arrival')
        axis_data=[]
        if axes:
            axis_data=[(cc,dd,f'{tag}_A1',f'{tag}_A-1',couriers[0]),(aa,bb,f'{tag}_B1',f'{tag}_B-1',couriers[1])]
            for x,y,direct,later,courier in axis_data:
                P=f'{tag}_AXIS_{x}_{y}';charts[P]={'kind':'span','rows':[E[x],E[y]]}
                move(f'X{x}',P,f'{tag}:axis_arrival');move(f'X{y}',P,f'{tag}:axis_arrival');add(f'X{y}',f'X{x}',f'{tag}:axis_encode');inverse.append((x,y))
                move(f'Y{courier}',P,f'{tag}:courier_arrival');add(f'X{x}',f'Y{courier}',f'{tag}:courier_load')
                move(f'Y{courier}',later,f'{tag}:courier_delivery');move(f'X{y}',tag,f'{tag}:axis_donor_return');move(f'X{x}',direct,f'{tag}:axis_delivery')
        for q,I in queries.items():
            carrier=next(info['roles'][0]for info in pairs.values()if info['late']==q)
            if axes:
                axis_source=f'X{cc}'if q==f'{tag}_A1'else f'X{aa}'if q==f'{tag}_B1'else f'Y{couriers[0]}'if q==f'{tag}_A-1'else f'Y{couriers[1]}'
            for i in I:
                move(f'Y{i}',q,f'{tag}:query_plane_arrival');add(f'X{carrier}',f'Y{i}',f'{tag}:later_pair_read')
                if axes:add(axis_source,f'Y{i}',f'{tag}:axis_read')
                expected[i]=qrows[q];assert values[f'Y{i}']==(1<<(111+i))^expected[i]
        for x,y in inverse:move(f'X{x}',tag,f'{tag}:carrier_return')
        for x,y in reversed(inverse):add(f'X{y}',f'X{x}',f'{tag}:X_inverse')
        for x,y,direct,later,courier in axis_data:
            move(f'Y{courier}',tag,f'{tag}:courier_cleanup_arrival');add(f'X{x}',f'Y{courier}',f'{tag}:courier_cleanup');add(f'X{y}',f'Y{courier}',f'{tag}:courier_cleanup')
            assert values[f'Y{courier}']==1<<(111+courier)
        assert all(values[f'X{i}']==1<<i for i in range(111))
        data.append({'gadget':k,'support':support,'pair_partition':[ab,cd],'axis_inputs_included':axes,'source_roles':sorted(sources),
                     'courier_Y_roles':couriers,'served_receivers':current,'query_roles':queries,'query_rows_hex':{q:hex(r)for q,r in qrows.items()},
                     'oriented_pairs':pairs,'operations_start':start,'operations_end':len(ops)})
    assert served==set(range(8,111)) and len(used_sources)==40
    cut=len(ops)
    for i in range(111):move(f'X{i}','Hub','X_endpoint')
    for i in range(111):move(f'Y{i}',f'F{i}','Y_endpoint')
    for n in list(owners):emit(['CLEAR',n],'native_retirement')
    word={'schema':'composed-quartet-four-plane-corrections-v1','source_path':SOURCE,'source_sha256':SHA,
          'charts':charts,'operations':ops,'carrier_interface_before_operation':cut,'Y_correction_rows_hex':list(map(hex,expected)),
          'construction':{'gadgets':data,'served_receivers':sorted(served),'source_roles':sorted(used_sources)},
          'semantic_operation_indices':dict(sem),'scope':'Actual four-gadget composition supplies one proper-chart local correction to all103 noncoordinate Ys;58 receive six terms and45 receive four. All original X and courier Ys restored; all222 columns,111 native snapshots and complete invoice. No diagonal output or complete supplier.'}
    C,cv,ca,stats=replay_general(word,R,e)
    assert stats['movement_profile']=={1:191,2:127,3:4,4:143,7:75}
    assert sum(v.bit_count()for v in expected)==528
    q=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',word)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,
        'fields':[{'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['G0:ground_Y_inverse','G1:ground_Y_inverse','G0:courier_cleanup','G1:courier_cleanup','G2:early_pair_read','G2:later_pair_read','G2:X_inverse','G3:early_pair_read','G3:later_pair_read','G3:X_inverse']:
        alt=json.loads(json.dumps(word));del alt['operations'][alt['semantic_operation_indices'][key][0]];alt['carrier_interface_before_operation']-=1
        try:replay_general(alt,R,e)
        except AssertionError:controls.append(key)
        else:raise AssertionError(('accepted omission',key))
    result={'status':'PASS_ACTUAL_FOUR_GADGET_CORRECTION_COMPOSITION','word_sha256':pin,'source_cut':cut,
            'gadgets':[{'support':d['support'],'source_count':len(d['source_roles']),'served_count':len(d['served_receivers']),'axis_inputs_included':d['axis_inputs_included']}for d in data],
            'served_receivers':103,'supplied_foreign_coefficients':528,'source_originals_used':40,'source_originals_still_native':71,
            'originals_at_Hub_at_cut':0,'stats':stats,'moment':h.record(q),'necessary_limiting_room':h.record((ceiling[0]-q[1],ceiling[1]-q[0])),
            'negative_controls':controls,'complete_diagonal_outputs':0,'scope':word['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
