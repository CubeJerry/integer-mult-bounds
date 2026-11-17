"""Retain one actual Y representative per sign query and87 Ys at ground."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general

PARENT_SHA='1e25b33b748e5ef5599394167acd207d4d3f91afcc202192969adb41734879e7'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'early-axis-known8/WORD.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'ground_retention_geometry');h=module(a.repo/HELPER,'ground_retention_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots']
    wb=a.parent.read_bytes();assert hashlib.sha256(wb).hexdigest()==PARENT_SHA;w=json.loads(wb)
    selected={min(I)for g in w['construction']['gadgets']for I in g['query_roles'].values()};assert len(selected)==16
    deferred=set(range(8,111))-selected;assert len(deferred)==87
    old_ops=w['operations'];old_cut=w['carrier_interface_before_operation'];keys={j:key for key,I in w['semantic_operation_indices'].items()for j in I}
    ops=[];sem={};mapping={};removed=[]
    relevant=(':early_query_arrival',':early_pair_read',':query_plane_arrival',':later_pair_read')
    for j,op in enumerate(old_ops):
        mapping[j]=len(ops);key=keys[j]
        if key.endswith(relevant):
            target=op[1]if op[0]=='MOVE'else op[2]
            assert target.startswith('Y')
            if int(target[1:])in deferred:removed.append(j);continue
        sem.setdefault(key,[]).append(len(ops));ops.append(op)
    cut=mapping[old_cut];assert len(removed)==4*87
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    expected=[int(v,16)for v in w['Y_correction_rows_hex']]
    for i in deferred:expected[i]=N[i]&255
    w['schema']='early-axis-known-eight-ground-retention-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,expected))
    w['construction']['parent_word_sha256']=PARENT_SHA
    w['construction']['representative_query_Y_roles']=sorted(selected);w['construction']['deferred_ground_Y_roles']=sorted(deferred)
    w['construction']['served_receivers']=sorted(selected)
    for g in w['construction']['gadgets']:
        g['deferred_query_roles']={q:[i for i in I if i in deferred]for q,I in g['query_roles'].items()}
        g['query_roles']={q:[i for i in I if i in selected]for q,I in g['query_roles'].items()}
        g['served_receivers']=[i for i in g['served_receivers']if i in selected]
        g['operations_start']=mapping[g['operations_start']];g['operations_end']=mapping[g['operations_end']]
    w['scope']='Earlier-axis source with only16 query representatives raised to rank3;87 noncoordinate Y retain native-axis preloads at ground and8 correct coordinate Y remain ground. All111 X source information is retained, with79 raw native,16 raw donors2 and16 pair collectors3. Closed partial word completes8 diagonal outputs. Deferred sign-query reads are not granted.'
    C,cv,ca,stats=replay_general(w,R,geo)
    assert stats['movement_profile']=={1:72,2:16,4:16,5:16,6:16,7:174}
    assert [i for i in range(111)if ca[f'Y{i}']=='zero']==sorted(set(range(8))|deferred)
    assert Counter(len(C[ca[f'Y{i}']])for i in range(111))=={0:95,3:16}
    assert all(cv[f'Y{i}']==(1<<(111+i))^expected[i]for i in range(111))
    assert all(expected[i].bit_count()==(8 if i in selected else 4)for i in range(8,111))
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['actual_native_axis_capture','prepare_axis_diagonal_value','ground_native_axis_preload',
                'G0:early_pair_read','G1:later_pair_read','G2:pair_encode','G3:later_pair_read','deferred_sign_inverse_at_Hub']:
        bad=json.loads(json.dumps(w));index=sem[key][0];del bad['operations'][index]
        if index<cut:bad['carrier_interface_before_operation']-=1
        try:replay_general(bad,R,geo)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted missing operation',key))
    result={'status':'PASS_ACTUAL_EARLY_SOURCE_WITH95_GROUND_Y','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'ground_public_Y_count':95,'raised_query_representatives':sorted(selected),
            'deferred_ground_noncoordinate_Y_count':87,'correct_coordinate_values_at_ground':8,
            'completed_diagonal_outputs_in_closed_word':8,'unfinished_native_foreign_coefficients':476,
            'native_axis_preloads':412,'sign_preloads':64,'original_X_rank_histogram':{1:79,2:16,3:16},
            'original_Y_rank_histogram':{0:95,3:16},'stats':stats,'moment':h.record(moment),
            'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
