"""Export actual retained pair originals, without reading any Y record.

Every new owner copies one real pair-sum X at its current query chart, descends
one rank to that query's earlier pair, and changes its retained raw donor.
The Hub closure unloads these changes before the retained pair inverses.
"""
from pathlib import Path
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general
from review_half_sum_gate import independent_rows

PARENT_SHA='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'low-retention-corrections/WORD.json')
    ap.add_argument('--queries-per-gadget',type=int,choices=[1,3,4],default=4)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'direct_pair_geometry');h=module(a.repo/HELPER,'direct_pair_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];wb=a.parent.read_bytes();assert hashlib.sha256(wb).hexdigest()==PARENT_SHA
    w=json.loads(wb);C,old_values,old_places,_=replay_general(w,R,geo)
    old_ops=w['operations'];old_cut=w['carrier_interface_before_operation']
    keys={j:key for key,indices in w['semantic_operation_indices'].items()for j in indices}
    ops=[];sem={};exports=[]
    def emit(op,key):sem.setdefault(key,[]).append(len(ops));ops.append(op)
    for j,op in enumerate(old_ops[:old_cut]):emit(op,keys[j])
    chosen_suffixes=['A1','A-1','B1','B-1'][:a.queries_per_gadget]
    for g in w['construction']['gadgets']:
        pairs=g['oriented_pairs'];gid=g['gadget']
        for suffix in chosen_suffixes:
            query=f'G{gid}_{suffix}'
            late_chart,late=next((p,z)for p,z in pairs.items()if z['late']==query)
            early_chart,early=next((p,z)for p,z in pairs.items()if z['early']==query)
            carrier=f"X{late['roles'][0]}";donor=f"X{early['roles'][1]}";owner=f'DIRECT_PAIR_{gid}_{suffix}'
            expected=sum(1<<j for j in late['roles'])
            assert old_places[carrier]==query and old_values[carrier]==expected
            assert old_places[donor]==early_chart and old_values[donor]==1<<early['roles'][1]
            assert len(C[query])==3 and len(C[early_chart])==2 and geo.sub(C[early_chart],C[query])
            assert not geo.sub(C[late_chart],C[early_chart])
            assert len(geo.basis(C[late_chart]+C[early_chart]))==3
            emit(['INIT',owner,query],'direct_pair_birth')
            emit(['ADD',carrier,owner],'actual_pair_snapshot')
            emit(['MOVE',owner,early_chart],'paid_pair_descent')
            emit(['ADD',owner,donor],'direct_pair_donor_load')
            exports.append({'owner':owner,'source_original':carrier,'source_pair':late['roles'],
                            'source_query':query,'destination_chart':early_chart,'changed_donor':donor,
                            'changed_donor_native_role':early['roles'][1],'row_hex':hex(expected)})
    cut=len(ops);unloaded=False
    for j,op in enumerate(old_ops[old_cut:],old_cut):
        if keys[j]=='deferred_sign_inverse_at_Hub' and not unloaded:
            for z in exports:emit(['ADD',z['source_original'],z['changed_donor']],'unload_pair_at_Hub_before_old_inverses')
            unloaded=True
        emit(op,keys[j])
    assert unloaded
    for z in exports:emit(['CLEAR',z['owner']],'direct_pair_retirement')
    w['schema']='actual-direct-pair-export-retained-original-v1'
    w['operations']=ops;w['semantic_operation_indices']=sem;w['carrier_interface_before_operation']=cut
    w['construction']['parent_word_sha256']=PARENT_SHA
    w['construction']['direct_pair_exports']=exports
    w['construction']['queries_per_gadget']=a.queries_per_gadget
    w['scope']='Actual pair-sum exports from existing X carriers at rank3 to retained rank2 donors, with charged unit descents and no Y reads. All222 partial endpoint columns restore; all103 existing Y corrections remain. New directions outside the previous canonical-plus-sign-query bank. No complete diagonal supplier.'
    C,values,places,stats=replay_general(w,R,geo);k=len(exports)
    assert k==4*a.queries_per_gadget and stats['movement_profile']=={1:175+k,2:111,3:4,4:111,5:16,6:16,7:75}
    assert all(values[z['owner']]==int(z['row_hex'],16)and places[z['owner']]==z['destination_chart']for z in exports)
    assert all(values[z['changed_donor']]==(1<<z['changed_donor_native_role'])^int(z['row_hex'],16)for z in exports)
    assert len(independent_rows([values[f'X{i}']for i in range(111)]))==111
    N=[sum(1<<j for j,s in enumerate(R)if sum(u*v for u,v in zip(r,s))==0)for r in R]
    K=[v^(1<<i)for i,v in enumerate(N)]
    query_rows=[int(v,16)&~255 for v in w['Y_correction_rows_hex']]
    pair_rows=[int(z['row_hex'],16)for z in exports]
    assert len(independent_rows(pair_rows))==k
    old_rank=len(independent_rows(K+query_rows));new_rank=len(independent_rows(K+query_rows+pair_rows))
    assert old_rank==21 and new_rank==25
    full_query_rows=[int(v,16)for v in w['Y_correction_rows_hex']]
    old_full_rank=len(independent_rows(K+full_query_rows));new_full_rank=len(independent_rows(K+full_query_rows+pair_rows))
    assert old_full_rank==21 and new_full_rank==(25 if a.queries_per_gadget==1 else 29)
    assert len(independent_rows(K+pair_rows))==9+k
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':places[n],'rank':len(C[places[n]]),'row_hex':hex(v)}for n,v in sorted(values.items())]})
    controls=[]
    for key in ['actual_pair_snapshot','paid_pair_descent','direct_pair_donor_load','unload_pair_at_Hub_before_old_inverses']:
        bad=json.loads(json.dumps(w));index=sem[key][0];del bad['operations'][index]
        if index<cut:bad['carrier_interface_before_operation']-=1
        try:replay_general(bad,R,geo)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted missing operation',key))
    wrong=json.loads(json.dumps(w));unload=sem['unload_pair_at_Hub_before_old_inverses'];old_inverse=sem['deferred_sign_inverse_at_Hub']
    insert_after=max(old_inverse)+1
    reordered=wrong['operations'];moved=[reordered[i]for i in unload]
    wrong['operations']=[op for i,op in enumerate(reordered)if i not in unload]
    at=insert_after-len(unload);wrong['operations'][at:at]=moved
    try:replay_general(wrong,R,geo)
    except AssertionError:controls.append('unload_after_old_pair_inverses')
    else:raise AssertionError('accepted wrong Hub inverse order')
    result={'status':'PASS_ACTUAL_DIRECT_PAIR_EXPORTS','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'actual_exports':k,'queries_per_gadget':a.queries_per_gadget,
            'actual_pure_pair_rank':len(independent_rows(pair_rows)),'source_original_information_rank':111,
            'canonical_plus_old_sign_queries_rank':old_rank,'canonical_plus_old_sign_queries_and_actual_pairs_rank':new_rank,
            'canonical_plus_actual_pair_rows_rank':9+k,'new_directions_mod_previous_bank':new_rank-old_rank,
            'canonical_plus_old_full_queries_rank':old_full_rank,
            'canonical_plus_old_full_queries_and_actual_pairs_rank':new_full_rank,
            'new_directions_mod_old_full_query_bank':new_full_rank-old_full_rank,
            'stats':stats,'moment':h.record(moment),'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'complete_diagonal_outputs':0,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
