"""Fresh native half sums, actual rank4 Y reads, and rank3 return exports."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse
import hashlib
import itertools
import json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general
from review_half_sum_gate import independent_rows

PARENT_SHA='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'
FRESH_CUT_ROLES=[14,16,60,63,84,85,107,109]


def candidates(R,w,C,at,geo):
    groups=defaultdict(list)
    for i,r in enumerate(R):
        if i>=8 and len(C[at[f'X{i}']])==1:groups[tuple(j for j,x in enumerate(r)if x)].append(i)
    Qroles={q:I for g in w['construction']['gadgets']for q,I in g['query_roles'].items()}
    out=[]
    for support,I in groups.items():
        for ab in itertools.combinations(support,2):
            for sign in [1,-1]:
                S=[i for i in I if R[i][ab[0]]==sign*R[i][ab[1]]]
                if len(S)<3:continue
                H=geo.basis(tuple(tuple(R[i])for i in S))
                if len(H)!=3:continue
                for q,Y in Qroles.items():
                    if len(geo.basis(H+C[q]))!=4:continue
                    served=[i for i in Y if all(sum(x*y for x,y in zip(R[i],R[j]))==0 for j in S)]
                    if served:out.append({'support':list(support),'pair':list(ab),'sign':sign,'sources':S,'query':q,'receivers':served})
    out.sort(key=lambda z:(-len(z['receivers']),-len(z['sources']),z['sources'],z['query']))
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'low-retention-corrections/WORD.json')
    ap.add_argument('--limit',type=int,default=1);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();assert a.limit>0;a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'cross_geometry');h=module(a.repo/HELPER,'cross_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];wb=a.parent.read_bytes();assert hashlib.sha256(wb).hexdigest()==PARENT_SHA
    w=json.loads(wb);C,values,at,parent_stats=replay_general(w,R,geo)
    all_candidates=candidates(R,w,C,at,geo);assert len(all_candidates)==44
    old_ops=w['operations'];old_cut=w['carrier_interface_before_operation']
    keys={j:key for key,I in w['semantic_operation_indices'].items()for j in I}
    ops=[];sem={};owners=set(n for n in values if n.startswith('NATIVE_'))
    def emit(op,key,update=True):
        sem.setdefault(key,[]).append(len(ops));ops.append(op)
        if not update:return
        kind,n,*q=op
        if kind=='INIT':assert n not in values;values[n]=0;at[n]=q[0];owners.add(n)
        elif kind=='ADD':assert C[at[n]]==C[at[q[0]]];values[q[0]]^=values[n]
        elif kind=='MOVE':at[n]=q[0]
        elif kind=='CLEAR':del values[n],at[n];owners.remove(n)
    for j,op in enumerate(old_ops[:old_cut]):emit(op,keys[j],False)
    selected=[];used_sources=set();profile=Counter(parent_stats['movement_profile'])
    old_pair_carriers={at[f'X{i}']:f'X{i}'for i in range(111)if len(C[at[f'X{i}']])==3}
    for cand in all_candidates:
        if len(selected)>=a.limit:break
        S=cand['sources'];q=cand['query']
        if set(S)&used_sources:continue
        eligible=[i for i in cand['receivers']if at[f'Y{i}']==q]
        if not eligible:continue
        serial=len(selected);rep=eligible[0];H=f'CROSS_{serial}_SOURCE';J=f'CROSS_{serial}_JOIN'
        assert w['charts'][q]['kind']=='span'
        w['charts'][H]={'kind':'span','rows':[R[i]for i in S]}
        w['charts'][J]={'kind':'span','rows':w['charts'][q]['rows']+[R[i]for i in S]}
        C[H]=geo.chart(w['charts'][H]);C[J]=geo.chart(w['charts'][J])
        assert len(C[H])==3 and len(C[J])==4 and geo.sub(C[q],C[J])and geo.sub(C[H],C[J])
        assert not geo.sub(C[H],C[q]) and all(geo.sub(C[J],C[f'F{i}'])for i in eligible)
        base=f'CROSS_BASE_{serial}';export=f'CROSS_EXPORT_{serial}';collector=f'X{S[0]}';target=old_pair_carriers[q]
        baseline=values[f'Y{rep}'];row=sum(1<<i for i in S)
        emit(['INIT',base,q],'actual_old_query_baseline_birth')
        emit(['ADD',f'Y{rep}',base],'actual_old_query_baseline_capture')
        for i in S:
            assert values[f'X{i}']==1<<i and len(C[at[f'X{i}']])==1
            emit(['MOVE',f'X{i}',H],'fresh_native_source_arrival')
        for i in S[1:]:emit(['ADD',f'X{i}',collector],'fresh_half_sum_encode')
        assert values[collector]==row
        emit(['MOVE',collector,J],'fresh_collector_rank4_arrival')
        emit(['MOVE',f'Y{rep}',J],'representative_rank4_arrival')
        emit(['ADD',collector,f'Y{rep}'],'fresh_half_read')
        emit(['INIT',export,J],'new_export_birth')
        emit(['ADD',f'Y{rep}',export],'actual_rank4_Y_capture')
        emit(['MOVE',export,q],'paid_rank4_to_query_descent')
        emit(['ADD',base,export],'actual_query_baseline_removal')
        assert values[export]==row and values[f'Y{rep}']==baseline^row
        emit(['ADD',export,target],'fresh_mode_original_carrier_load')
        for i in eligible[1:]:emit(['ADD',export,f'Y{i}'],'returned_export_native_receiver_read')
        selected.append({**cand,'representative_Y_role':rep,'actual_served_Y_roles':eligible,
                         'source_plane':H,'rendezvous_chart':J,'source_collector':collector,
                         'baseline_owner':base,'export_owner':export,'changed_old_carrier':target,
                         'payload_hex':hex(row),'baseline_hex':hex(baseline)})
        used_sources.update(S)
        profile.update({1:3,2:len(S),3:1,5:len(S)-1,7:-len(S)})
    assert selected
    cut=len(ops);expected=[]
    for i in range(111):
        assert values[f'Y{i}']>>111==1<<i
        expected.append(values[f'Y{i}']&((1<<111)-1))
    assert len(independent_rows([values[f'X{i}']for i in range(111)]))==111
    inserted=False
    for j,op in enumerate(old_ops[old_cut:],old_cut):
        if keys[j]=='deferred_sign_inverse_at_Hub'and not inserted:
            for z in selected:emit(['ADD',z['source_collector'],z['changed_old_carrier']],'unload_fresh_modes_at_Hub')
            for z in selected:
                for i in z['sources'][1:]:emit(['ADD',f'X{i}',z['source_collector']],'fresh_half_sum_inverse_at_Hub')
            inserted=True
        emit(op,keys[j])
    assert inserted
    for z in selected:
        for owner in [z['baseline_owner'],z['export_owner']]:emit(['CLEAR',owner],'cross_export_retirement')
    w['schema']='cross-quartet-fresh-half-export-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,expected))
    w['construction']['parent_word_sha256']=PARENT_SHA;w['construction']['fresh_cross_quartet_exports']=selected
    w['construction']['geometric_candidate_count']=len(all_candidates)
    w['scope']='Actual fresh native half-sum acquisition at rank3, rank4 Y rendezvous, and paid one-rank export into an occupied old query3. New modes involve previously untouched X columns. All222 columns and original-X restoration are explicit. This is a partial correction/source word, not a complete diagonal supplier.'
    C,cv,ca,stats=replay_general(w,R,geo);assert stats['movement_profile']==dict(sorted((d,n)for d,n in profile.items()if n))
    assert all(cv[z['export_owner']]==int(z['payload_hex'],16)and ca[z['export_owner']]==z['query']for z in selected)
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R];K=[n^(1<<i)for i,n in enumerate(N)]
    assert all(not(expected[i]&~N[i])for i in range(111))
    old_queries=[int(x,16)for x in json.loads(wb)['Y_correction_rows_hex']];payloads=[int(z['payload_hex'],16)for z in selected]
    rank_before=len(independent_rows(K+old_queries));rank_after=len(independent_rows(K+old_queries+payloads))
    assert rank_before==21 and len(independent_rows(payloads))==len(selected)and rank_after>rank_before
    fresh_mask=sum(1<<i for i in FRESH_CUT_ROLES)
    assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in FRESH_CUT_ROLES for j in FRESH_CUT_ROLES)
    inside=[n for n in cv if any(geo.sub(C[ca[n]],C[f'F{i}'])for i in FRESH_CUT_ROLES)]
    initial_fresh_rank=len(independent_rows([cv[n]&fresh_mask for n in inside]))
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['actual_old_query_baseline_capture','fresh_half_sum_encode','fresh_half_read','actual_rank4_Y_capture',
                'paid_rank4_to_query_descent','actual_query_baseline_removal','fresh_mode_original_carrier_load',
                'unload_fresh_modes_at_Hub','fresh_half_sum_inverse_at_Hub']:
        bad=json.loads(json.dumps(w));index=sem[key][0];del bad['operations'][index]
        if index<cut:bad['carrier_interface_before_operation']-=1
        try:replay_general(bad,R,geo)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted missing operation',key))
    result={'status':'PASS_ACTUAL_CROSS_QUARTET_FRESH_EXPORT','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'fresh_export_count':len(selected),'fresh_source_roles':sorted(used_sources),
            'new_native_receiver_reads':sum(len(z['actual_served_Y_roles'])for z in selected),
            'added_foreign_input_coefficients':sum(len(z['sources'])*len(z['actual_served_Y_roles'])for z in selected),
            'total_foreign_input_coefficients':sum(row.bit_count()for row in expected),
            'actual_fresh_export_rank':len(independent_rows(payloads)),'canonical_plus_old_full_queries_rank':rank_before,
            'canonical_plus_old_full_queries_plus_fresh_export_rank':rank_after,
            'root_eight_facet_cut_roles':FRESH_CUT_ROLES,'eight_facet_union_current_selected_input_rank':initial_fresh_rank,
            'remaining_eight_facet_rank_deficit':8-initial_fresh_rank,
            'stats':stats,'moment':h.record(moment),'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'complete_diagonal_outputs':0,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
