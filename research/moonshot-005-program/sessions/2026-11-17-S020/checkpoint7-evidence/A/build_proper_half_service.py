"""Four proper half exports serve seven raised receivers via reversible Y swaps."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general

PARENT_SHA='eb49a700e9d815d975120ba56271d414a2a15ee01254c8f5f3203fdfb52c2a59'
PLAN=[(14,97,'HALF_4_1',[42,45]),(17,98,'HALF_2_2',[23,26]),
      (19,100,'HALF_2_2',[23,26]),(96,15,'HALF_9_1',[77,80]),
      (99,16,'HALF_9_1',[77,80]),(101,18,'HALF_9_0',[74,75]),
      (102,21,'HALF_9_0',[74,75])]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'parity-receiver-relays/WORD.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'proper_service_geometry');h=module(a.repo/HELPER,'proper_service_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];pb=a.parent.read_bytes();assert hashlib.sha256(pb).hexdigest()==PARENT_SHA
    w=json.loads(pb);C,pv,pp,parent_stats=replay_general(w,R,geo)
    halfs={z['owner']:z for g in w['construction']['quartets']for z in g['modes']}
    relays={i:z for z in w['construction']['receiver_parity_relays']for i in z['receiver_roles']}
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    services=[];exports={}
    for serial,(i,k,source,plane_roles)in enumerate(PLAN):
        z=halfs[source];H=z['chart'];T=pp[f'Y{i}'];key=(source,tuple(plane_roles))
        if key not in exports:
            number=len(exports);P=f'HALF_SERVICE_P{number}';owner=f'HALF_SERVICE_EXPORT_{number}'
            w['charts'][P]={'kind':'span','rows':[R[j]for j in plane_roles]}
            C[P]=geo.chart(w['charts'][P]);assert len(C[P])==2 and geo.sub(C[P],C[H])
            exports[key]={'source_owner':source,'source_chart':H,'export_chart':P,'export_owner':owner,
                          'plane_native_roles':plane_roles,'payload_hex':z['row_hex']}
        e=exports[key];P=e['export_chart'];J=f'HALF_SERVICE_J{serial}'
        frame=relays[i]['receiver_roles'];D=sum(1<<j for j in frame if j!=i)
        rows=[R[j]for j in frame if j!=i]+[R[j]for j in plane_roles]
        w['charts'][J]={'kind':'span','rows':rows};C[J]=geo.chart(w['charts'][J])
        row=int(z['row_hex'],16)
        assert len(C[T])==3 and len(C[J])==4 and geo.sub(C[T],C[J])and geo.sub(C[P],C[J])
        assert geo.sub(C[J],C[f'F{i}'])and geo.sub(C[J],C[f'F{k}'])and pp[f'Y{k}']=='zero'
        assert not(row&~N[i]) and not(D&~N[k]) and row&~N[k]
        assert pv[source]==row and pp[source]==H
        services.append({'receiver':i,'courier':k,'receiver_initial_chart':T,'rendezvous_chart':J,
                         'export_owner':e['export_owner'],'export_chart':P,'half_payload_hex':hex(row),
                         'courier_final_native_correction_hex':hex(D)})
    assert len(exports)==4 and len({z['receiver']for z in services})==7 and len({z['courier']for z in services})==7
    oldops=w['operations'];oldcut=w['carrier_interface_before_operation']
    keys={j:key for key,I in w['semantic_operation_indices'].items()for j in I}
    inverse_at=w['semantic_operation_indices']['relay_ground_baseline_inverse'][0]
    ops=[];sem={};values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    def emit(op,key):
        sem.setdefault(key,[]).append(len(ops));ops.append(op);kind,name,*args=op
        if kind=='INIT':assert name not in values;values[name]=0;places[name]=args[0]
        elif kind=='ADD':assert C[places[name]]==C[places[args[0]]],op;values[args[0]]^=values[name]
        elif kind=='MOVE':places[name]=args[0]
        elif kind=='CLEAR':del values[name],places[name]
    for j,op in enumerate(oldops[:oldcut]):
        if j==inverse_at:
            assert all(places[f'Y{i}']=='zero'for i in range(111))
            for z in reversed(services):
                emit(['ADD',f"Y{z['receiver']}",f"Y{z['courier']}"],'half_service_ground_inverse')
                emit(['ADD',f"Y{z['courier']}",f"Y{z['receiver']}"],'half_service_ground_inverse')
        emit(op,keys[j])
    for e in exports.values():
        emit(['INIT',e['export_owner'],e['source_chart']],'half_service_owner_birth')
        emit(['ADD',e['source_owner'],e['export_owner']],'half_service_actual_capture')
        emit(['MOVE',e['export_owner'],e['export_chart']],'half_service_paid_unit_descent')
    for z in services:
        i,k=z['receiver'],z['courier'];P=z['export_chart'];J=z['rendezvous_chart']
        emit(['MOVE',f'Y{k}',P],'half_service_courier_proper_arrival')
        emit(['ADD',z['export_owner'],f'Y{k}'],'half_service_actual_proper_read')
        emit(['MOVE',f'Y{k}',J],'half_service_courier_joint_arrival')
        emit(['MOVE',f'Y{i}',J],'half_service_receiver_joint_arrival')
        emit(['ADD',f'Y{k}',f'Y{i}'],'half_service_to_receiver')
        emit(['ADD',f'Y{i}',f'Y{k}'],'half_service_courier_swap_cleanup')
    cut=len(ops);assert cut==2089
    expected=[int(x,16)for x in w['Y_correction_rows_hex']]
    for z in services:
        expected[z['receiver']]^=int(z['half_payload_hex'],16)
        expected[z['courier']]^=int(z['courier_final_native_correction_hex'],16)
    assert all(values[f'Y{i}']==(1<<(111+i))^expected[i]for i in range(111))
    assert all(not(expected[i]&~N[i])for i in range(8,111))
    for j,op in enumerate(oldops[oldcut:],oldcut):emit(op,keys[j])
    for e in exports.values():emit(['CLEAR',e['export_owner']],'half_service_export_retirement')
    w['schema']='proper-half-service-through-public-Y-swaps-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,expected))
    w['construction']['parent_word_sha256']=PARENT_SHA
    w['construction']['proper_half_service']={'exports':list(exports.values()),'services':services,
                                             'inverse_before_parent_operation':inverse_at}
    w['scope']='Four actual rank3→rank2 half exports serve seven already-raised parity receivers through seven fresh public Y couriers. Shared exports fan out. Two forward Y ADDs deliver the half sum and cancel courier nonnative garbage, leaving a native parity correction. Earlier inverse ADDs restore arbitrary initial Y/axis baselines. All111 X remain raw Hub;8 diagonal outputs only; no full supplier.'
    C,cv,ca,stats=replay_general(w,R,geo)
    profile=Counter(parent_stats['movement_profile']);profile.update({1:11,2:14,3:14,4:-7,7:-7})
    assert stats['movement_profile']==dict(sorted(profile.items()))
    assert stats['counts']=={'INIT':198,'ADD':1461,'MOVE':541,'CLEAR':198}
    assert Counter(len(C[ca[f'Y{i}']])for i in range(111))=={0:88,3:1,4:22}and len(cv)==420
    assert sum(expected[i].bit_count()for i in range(8,111))==485
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['half_service_ground_inverse','half_service_actual_capture','half_service_paid_unit_descent',
                'half_service_actual_proper_read','half_service_to_receiver','half_service_courier_swap_cleanup']:
        bad=json.loads(json.dumps(w));j=sem[key][0];del bad['operations'][j]
        if j<cut:bad['carrier_interface_before_operation']-=1
        try:
            _,bv,bp,_=replay_general(bad,R,geo);assert(bv,bp)==(cv,ca)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted missing operation',key))
    bad=json.loads(json.dumps(w));j=sem['half_service_ground_inverse'][0];op=bad['operations'].pop(j)
    k=next(k for k,o in enumerate(bad['operations'])if o[:2]==['MOVE',op[1]])
    bad['operations'].insert(k+1,op)
    try:replay_general(bad,R,geo)
    except AssertionError:controls.append('late_ground_inverse_rejected')
    else:raise AssertionError('accepted late inverse')
    result={'status':'PASS_ACTUAL_PROPER_HALF_RECEIVER_SERVICE','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'live_fields':420,'actual_proper_export_count':4,'served_raised_receivers':7,
            'fresh_public_Y_couriers':7,'additional_foreign_terms_on_targets':28,'additional_foreign_terms_on_couriers':21,
            'total_unfinished_foreign_terms':485,'all_courier_nonnative_garbage_cancelled':True,
            'all_arbitrary_initial_Y_coefficients_identity':True,'all111_original_X_restored':True,
            'completed_diagonal_outputs':8,'public_Y_rank_histogram':{0:88,3:1,4:22},
            'additional_owned_MOVEs':4,'stats':stats,'moment':h.record(moment),
            'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
