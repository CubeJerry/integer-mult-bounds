"""Retain sign originals below their quartets after the actual correction layer.

The frozen parent word is used only as a literal source. All source-aware
cochart/value/movement checks rerun on the transformed complete word.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE,SHA,HELPER,CHECK,module
from build_four_plane_correction import replay_general

PARENT_SHA='fbbae97bf0c71ca5d1f74bbe272e5507690f09d991600fe42f1636f0386c7433'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'composed-four-plane-corrections/WORD.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    h=module(a.repo/HELPER,'lowret_helper');e=module(a.repo/CHECK,'lowret_geometry')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots']
    parent_raw=a.parent.read_bytes();assert hashlib.sha256(parent_raw).hexdigest()==PARENT_SHA;w=json.loads(parent_raw)
    old_ops=w['operations'];oldcut=w['carrier_interface_before_operation'];index_keys={j:k for k,I in w['semantic_operation_indices'].items()for j in I}
    removed=set();deferred=[];donors=[];carriers=[]
    for j,op in enumerate(old_ops[:oldcut]):
        key=index_keys[j]
        if key.endswith(':raw_donor_return'):
            removed.add(j);donors.append(int(op[1][1:]));assert op[0]=='MOVE'
        elif key.endswith(':carrier_return') and int(op[1][1:])>=8:
            removed.add(j);carriers.append(int(op[1][1:]));assert op[0]=='MOVE'
        elif key.endswith(':X_inverse') and int(op[1][1:])>=8:
            removed.add(j);deferred.append(op);assert op[0]=='ADD'
    assert len(donors)==len(carriers)==len(deferred)==16 and len(removed)==48
    ops=[];sem={};mapping={}
    def emit(op,key):
        sem.setdefault(key,[]).append(len(ops));ops.append(op)
    for j,op in enumerate(old_ops[:oldcut]):
        mapping[j]=len(ops)
        if j not in removed:emit(op,index_keys[j])
    cut=len(ops);mapping[oldcut]=cut;inserted=False
    for j,op in enumerate(old_ops[oldcut:],oldcut):
        key=index_keys[j]
        if key=='Y_endpoint' and not inserted:
            for inverse in deferred:emit(inverse,'deferred_sign_inverse_at_Hub')
            inserted=True
        emit(op,key)
    assert inserted
    w['schema']='composed-correction-low-sign-retention-v1';w['operations']=ops;w['semantic_operation_indices']=sem;w['carrier_interface_before_operation']=cut
    w['construction']['parent_word_sha256']=PARENT_SHA
    w['construction']['raw_sign_donors_retained_at_rank2']=sorted(donors)
    w['construction']['encoded_sign_carriers_retained_at_rank3']=sorted(carriers)
    for g in w['construction']['gadgets']:
        g['operations_start']=mapping[g['operations_start']];g['operations_end']=mapping[g['operations_end']]
    w['scope']='Actual103-receiver proper-correction layer with16 raw rank2 sign originals and16 encoded rank3 sign-sum originals retained. Eight coordinate X restore atquartets;71 X remain native. All222 public columns restore under actual Hub inverse closure. No complete diagonal output or supplier.'
    C,cv,ca,stats=replay_general(w,R,e)
    assert stats['movement_profile']=={1:175,2:111,3:4,4:111,5:16,6:16,7:75}
    assert all(cv[f'X{i}']==1<<i and len(C[ca[f'X{i}']])==2 for i in donors)
    assert all(cv[f'X{i}'].bit_count()==2 and len(C[ca[f'X{i}']])==3 for i in carriers)
    assert len(h.binary_basis([cv[f'X{i}']for i in range(111)]))==111
    q=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for j in[0,5,10,15]:
        alt=json.loads(json.dumps(w));del alt['operations'][sem['deferred_sign_inverse_at_Hub'][j]]
        try:replay_general(alt,R,e)
        except AssertionError:controls.append(f'omit_deferred_inverse_{j}')
        else:raise AssertionError('accepted omitted deferred inverse')
    result={'status':'PASS_ACTUAL_CORRECTION_LAYER_WITH_LOW_SIGN_RETENTION','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'original_X_rank_histogram':dict(Counter(len(C[ca[f'X{i}']])for i in range(111))),
            'raw_rank2_originals':16,'encoded_rank3_originals':16,'raw_rank4_coordinate_originals':8,'raw_native_originals':71,
            'original_X_information_rank':111,'served_receivers':103,'supplied_foreign_coefficients':528,'stats':stats,
            'moment':h.record(q),'necessary_limiting_room':h.record((ceiling[0]-q[1],ceiling[1]-q[0])),
            'negative_controls':controls,'complete_diagonal_outputs':0,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
