"""Eight early raw-axis transfers, followed by four sign-only corrections.

The parent is transformed literally. Every axis/courier excursion is removed;
all coordinate X stay native and all eight coordinate Y stay at ground at the
cut, with their correct diagonal values. Native-axis corrections are read by
all103 noncoordinate Y before they start their proper sign-query routes.
"""
from pathlib import Path
from collections import Counter
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
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'axis_early_geometry');h=module(a.repo/HELPER,'axis_early_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];wb=a.parent.read_bytes();assert hashlib.sha256(wb).hexdigest()==PARENT_SHA
    w=json.loads(wb);old_ops=w['operations'];old_cut=w['carrier_interface_before_operation']
    keys={j:key for key,I in w['semantic_operation_indices'].items()for j in I}
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    ops=[];sem={};mapping={};removed=[]
    def emit(op,key):sem.setdefault(key,[]).append(len(ops));ops.append(op)
    inserted=False
    for j,op in enumerate(old_ops[:old_cut]):
        if j==222:
            for axis in range(8):
                owner=f'EARLY_AXIS_{axis}'
                emit(['INIT',owner,f'L{axis}'],'early_axis_owner_birth')
                emit(['ADD',f'X{axis}',owner],'actual_native_axis_capture')
                emit(['MOVE',owner,'zero'],'paid_native_axis_descent')
                emit(['ADD',owner,f'Y{axis}'],'prepare_axis_diagonal_value')
            for i in range(8,111):
                for axis in range(8):
                    if N[i]>>axis&1:emit(['ADD',f'EARLY_AXIS_{axis}',f'Y{i}'],'ground_native_axis_preload')
            inserted=True
        mapping[j]=len(ops);key=keys[j]
        axis_op=('axis' in key or 'courier' in key or key.endswith(':ground_Y_inverse'))
        if key.endswith((':carrier_return',':X_inverse'))and op[1].startswith('X')and int(op[1][1:])<8:axis_op=True
        if axis_op:removed.append({'old_index':j,'semantic_key':key,'operation':op});continue
        emit(op,key)
    assert inserted;cut=len(ops);mapping[old_cut]=cut
    for j,op in enumerate(old_ops[old_cut:],old_cut):emit(op,keys[j])
    for axis in range(8):emit(['CLEAR',f'EARLY_AXIS_{axis}'],'early_axis_owner_retirement')
    expected=[1<<i if i<8 else (N[i]&255)^(int(w['Y_correction_rows_hex'][i],16)&~255)for i in range(111)]
    w['schema']='early-axis-known-eight-sign-correction-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,expected))
    w['construction']['parent_word_sha256']=PARENT_SHA
    w['construction']['early_axis_roles']=list(range(8));w['construction']['source_roles']=[i for i in w['construction']['source_roles']if i>=8]
    w['construction']['removed_parent_axis_courier_operations']=removed
    for g in w['construction']['gadgets']:
        g['axis_inputs_included']=False;g['courier_Y_roles']=[];g['source_roles']=[i for i in g['source_roles']if i>=8]
        g['query_rows_hex']={q:hex(int(v,16)&~255)for q,v in g['query_rows_hex'].items()}
        g['operations_start']=mapping[g['operations_start']];g['operations_end']=mapping[g['operations_end']]
    w['scope']='Eight early raw-axis owner descents prepare correct coordinate diagonal values at ground and all103 native-axis preloads before any Y ascent. Four sign-only proper gadgets retain16 raw sign X at2 and16 encoded pair X at3;79 original X remain native and8 correct coordinate Y remain at ground. The closed word completes exactly8 diagonal outputs and restores all X. No complete111-output supplier.'
    C,cv,ca,stats=replay_general(w,R,geo)
    assert stats['movement_profile']=={1:159,2:103,4:103,5:16,6:16,7:87}
    assert all(cv[f'X{i}']==1<<i and ca[f'X{i}']==f'L{i}'for i in range(8))
    assert all(cv[f'Y{i}']==(1<<(111+i))^(1<<i)and ca[f'Y{i}']=='zero'for i in range(8))
    assert all(cv[f'EARLY_AXIS_{i}']==1<<i and ca[f'EARLY_AXIS_{i}']=='zero'for i in range(8))
    assert Counter(len(C[ca[f'X{i}']])for i in range(111))=={1:79,2:16,3:16}
    assert Counter(len(C[ca[f'Y{i}']])for i in range(111))=={0:8,3:103}
    assert len(independent_rows([cv[f'X{i}']for i in range(111)]))==111
    assert all(expected[i].bit_count()==8 and not(expected[i]&~N[i])for i in range(8,111))
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['actual_native_axis_capture','paid_native_axis_descent','prepare_axis_diagonal_value',
                'ground_native_axis_preload','G0:early_pair_read','G1:later_pair_read','G2:pair_encode',
                'G3:later_pair_read','deferred_sign_inverse_at_Hub']:
        bad=json.loads(json.dumps(w));index=sem[key][0];del bad['operations'][index]
        if index<cut:bad['carrier_interface_before_operation']-=1
        try:replay_general(bad,R,geo)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted omitted operation',key))
    result={'status':'PASS_ACTUAL_EARLY_AXIS_KNOWN_EIGHT_SOURCE','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'correct_coordinate_diagonal_values_at_ground':8,'completed_diagonal_outputs_in_closed_word':8,
            'unfinished_noncoordinate_outputs':103,'native_axis_foreign_preloads':412,'sign_foreign_preloads':412,
            'total_unfinished_foreign_coefficients':824,'original_X_rank_histogram':{1:79,2:16,3:16},
            'original_Y_rank_histogram':{0:8,3:103},'pure_known_axis_records_at_ground':8,
            'source_original_information_rank':111,'stats':stats,'moment':h.record(moment),
            'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
