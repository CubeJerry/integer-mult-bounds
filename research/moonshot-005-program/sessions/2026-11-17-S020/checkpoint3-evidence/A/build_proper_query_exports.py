"""Actual one-rank Y-derived query exports into held original carriers.

Selected query Ys retain their partial output. A fresh owner reads the query,
removes the actual axis delivery where necessary, descends to the early pair,
and removes the saved arbitrary-Y baseline. It then loads a raw pair donor.
"""
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE,SHA,HELPER,CHECK,module
from build_four_plane_correction import replay_general

PARENT_SHA='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'low-retention-corrections/WORD.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    h=module(a.repo/HELPER,'query_export_helper');e=module(a.repo/CHECK,'query_export_geometry')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots']
    parent_raw=a.parent.read_bytes();assert hashlib.sha256(parent_raw).hexdigest()==PARENT_SHA;w=json.loads(parent_raw)
    old_ops=w['operations'];oldcut=w['carrier_interface_before_operation'];keys={j:k for k,I in w['semantic_operation_indices'].items()for j in I}
    selections=[];before=defaultdict(list);extra_owners=[]
    for g in w['construction']['gadgets']:
        tag=f"G{g['gadget']}"
        for label in['A1','A-1','B1']:
            q=f'{tag}_{label}';rep=g['query_roles'][q][0]
            P,early=next((P,z)for P,z in g['oriented_pairs'].items()if z['early']==q)
            late=next(z for z in g['oriented_pairs'].values()if z['late']==q)
            base=f'Y_BASELINE_{q}';axis=f'AXIS_HISTORY_{q}'if g['axis_inputs_included']else None;packet=f'QUERY_EXPORT_{q}'
            idx=next(j for j in w['semantic_operation_indices'][f'{tag}:early_pair_read']if old_ops[j][2]==f'Y{rep}')
            before[idx]+=[(['INIT',base,P],'baseline_cache_birth'),(['ADD',f'Y{rep}',base],'actual_early_Y_baseline')]
            extra_owners.append(base)
            if axis:
                axis_idx=next(j for j in w['semantic_operation_indices'][f'{tag}:axis_read']if old_ops[j][2]==f'Y{rep}')
                src=old_ops[axis_idx][1]
                before[axis_idx]+=[(['INIT',axis,q],'axis_history_birth'),(['ADD',src,axis],'actual_axis_delivery_snapshot')]
                extra_owners.append(axis)
            extra_owners.append(packet)
            sign_row=int(g['query_rows_hex'][q],16)&~255
            assert sign_row.bit_count()==4
            selections.append({'query':q,'representative_Y':rep,'pair_chart':P,'baseline_cache':base,'axis_history':axis,
                               'export_field':packet,'carrier_X':early['roles'][1],'unchanged_sum_carriers':[early['roles'][0],late['roles'][0]],
                               'sign_query_row_hex':hex(sign_row)})
    assert len(selections)==12 and len(extra_owners)==30
    ops=[];sem=defaultdict(list);mapping={}
    def emit(op,key):sem[key].append(len(ops));ops.append(op)
    for j,op in enumerate(old_ops[:oldcut]):
        mapping[j]=len(ops)
        for inserted,key in before[j]:emit(inserted,key)
        emit(op,keys[j])
    mapping[oldcut]=len(ops);old_interface_after_capture=len(ops)
    for z in selections:
        p=z['export_field'];emit(['INIT',p,z['query']],'query_export_birth')
        emit(['ADD',f"Y{z['representative_Y']}",p],'actual_corrected_Y_read')
        if z['axis_history']:emit(['ADD',z['axis_history'],p],'remove_actual_axis_delivery')
        emit(['MOVE',p,z['pair_chart']],'one_rank_proper_export')
        emit(['ADD',z['baseline_cache'],p],'actual_Y_baseline_unmask')
        emit(['ADD',p,f"X{z['carrier_X']}"],'actual_coded_original_load')
    cut=len(ops);inserted_inverse=False
    for j,op in enumerate(old_ops[oldcut:],oldcut):
        key=keys[j]
        if key=='deferred_sign_inverse_at_Hub'and not inserted_inverse:
            for z in reversed(selections):
                for p in z['unchanged_sum_carriers']:
                    emit(['ADD',f'X{p}',f"X{z['carrier_X']}"],'actual_coded_original_inverse')
            inserted_inverse=True
        emit(op,key)
    assert inserted_inverse
    for n in extra_owners:emit(['CLEAR',n],'new_owner_retirement')
    w['schema']='proper-query-exports-into-original-carriers-v1';w['operations']=ops;w['semantic_operation_indices']=dict(sem)
    w['carrier_interface_before_operation']=cut;w['construction']['parent_word_sha256']=PARENT_SHA
    w['construction']['query_exports']=selections;w['construction']['old_interface_after_cache_capture']=old_interface_after_capture
    for g in w['construction']['gadgets']:
        g['operations_start']=mapping[g['operations_start']];g['operations_end']=mapping[g['operations_end']]
    w['scope']='Actual12 independent sign-query fields exported one rank from corrected Y histories, unmasked by actual earlier Y caches, and loaded into12 held original carriers. All103 partial Y corrections retained, all222 original endpoints restored by actual ordered Hub inverses. No canonical bank, diagonal completion or supplier.'
    C,cv,ca,stats=replay_general(w,R,e)
    assert stats['movement_profile']=={1:187,2:111,3:4,4:111,5:16,6:16,7:75}
    pure=[]
    for z in selections:
        p=z['export_field'];row=int(z['sign_query_row_hex'],16)
        assert cv[p]==row and len(C[ca[p]])==2
        n=f"X{z['carrier_X']}";assert cv[n]==(1<<z['carrier_X'])^row and len(C[ca[n]])==2 and cv[n].bit_count()==3
        support_rows=tuple(tuple(R[j])for j in range(111)if cv[n]>>j&1)
        assert len(e.basis(support_rows))==3
        pure.append(row)
    assert len(h.binary_basis(pure))==12 and len(h.binary_basis([cv[f'X{i}']for i in range(111)]))==111
    K=[(1<<i)^sum(1<<j for j,s in enumerate(R)if sum(a*b for a,b in zip(r,s))==0)for i,r in enumerate(R)]
    assert len(h.binary_basis(K+pure))==21
    q=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in['actual_early_Y_baseline','actual_axis_delivery_snapshot','actual_corrected_Y_read','remove_actual_axis_delivery','one_rank_proper_export','actual_Y_baseline_unmask','actual_coded_original_load','actual_coded_original_inverse']:
        alt=json.loads(json.dumps(w));j=sem[key][0];del alt['operations'][j]
        if j<cut:alt['carrier_interface_before_operation']-=1
        try:replay_general(alt,R,e)
        except AssertionError:controls.append(key)
        else:raise AssertionError(('accepted bad export',key))
    result={'status':'PASS_ACTUAL_ONE_RANK_QUERY_EXPORTS_INTO_ORIGINAL_CARRIERS','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'proper_exports':12,'export_source_rank':3,'export_terminal_rank':2,'exported_X_information_rank':12,
            'exported_source_union_size':len({j for row in pure for j in range(111)if row>>j&1}),
            'canonical_plus_exported_algebraic_rank':21,'new_coded_rank2_originals':12,'coded_payload_native_span_rank':3,
            'original_X_information_rank':111,'served_receivers':103,'supplied_foreign_coefficients':528,'stats':stats,
            'moment':h.record(q),'necessary_limiting_room':h.record((ceiling[0]-q[1],ceiling[1]-q[0])),
            'negative_controls':controls,'complete_diagonal_outputs':0,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
