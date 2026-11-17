"""Two actual four-receiver parity corrections using correct axis Y couriers."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, itertools, json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general

PARENT_SHA='6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'full-half-reservoir/WORD.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'parity_relay_geometry');h=module(a.repo/HELPER,'parity_relay_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];pb=a.parent.read_bytes();assert hashlib.sha256(pb).hexdigest()==PARENT_SHA
    w=json.loads(pb);C,_,_,parent_stats=replay_general(w,R,geo)
    specs=[([0,2,4,6],[14,17,19,20],[1,3,5,7]),([1,3,5,7],[96,99,101,102],[0,2,4,6])]
    configs=[]
    for serial,(support,S,helpers)in enumerate(specs):
        g=next(g for g in w['construction']['quartets']if g['support']==support)
        assert all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i,j in itertools.combinations(S,2))
        aa,bb,cc,dd=S;prefix=f'PARITY_{serial}'
        Pcd=prefix+'_CD';Pbd=prefix+'_BD';Pac=prefix+'_AC'
        for name,I in [(Pcd,[cc,dd]),(Pbd,[bb,dd]),(Pac,[aa,cc])]:
            w['charts'][name]={'kind':'span','rows':[R[i]for i in I]}
        triples={i:prefix+'_T'+str(i)for i in S}
        for i,name in triples.items():w['charts'][name]={'kind':'span','rows':[R[j]for j in S if j!=i]}
        z={'support':support,'receiver_roles':S,'helper_axis_Y_roles':helpers,'quartet_chart':g['quartet_chart'],
           'pair_cd':Pcd,'pair_bd':Pbd,'pair_ac':Pac,'triple_charts':triples,
           'pair_owner':prefix+'_PAIR_SOURCE','raw_cleanup_owners':{i:prefix+'_RAW'+str(i)for i in S}}
        configs.append(z)
    C={n:geo.chart(z)for n,z in w['charts'].items()}
    for z in configs:
        for i,P in z['triple_charts'].items():
            assert len(C[P])==3 and geo.sub(C[P],C[f'F{i}'])
        assert all(geo.sub(C[z['quartet_chart']],C[f'F{i}'])for i in z['helper_axis_Y_roles'])
    oldops=w['operations'];oldcut=w['carrier_interface_before_operation']
    keys={j:key for key,I in w['semantic_operation_indices'].items()for j in I}
    ops=[];sem={};values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};extraowners=[]
    def emit(op,key):
        sem.setdefault(key,[]).append(len(ops));ops.append(op);kind,name,*args=op
        if kind=='INIT':assert name not in values;values[name]=0;places[name]=args[0]
        elif kind=='ADD':assert C[places[name]]==C[places[args[0]]],(op,places[name],places[args[0]]);values[args[0]]^=values[name]
        elif kind=='MOVE':places[name]=args[0]
        elif kind=='CLEAR':del values[name],places[name]
    pairdone=set();rawdone=False
    for j,op in enumerate(oldops[:oldcut]):
        if keys[j]=='direct_half_native_gather':
            for serial,z in enumerate(configs):
                cc,dd=z['receiver_roles'][2:]
                if serial not in pairdone and op[1]in[f'X{cc}',f'X{dd}']:
                    assert places[f'X{cc}']==f'L{cc}'and places[f'X{dd}']==f'L{dd}'
                    for i in [cc,dd]:emit(['MOVE',f'X{i}',z['pair_cd']],'relay_pair_source_arrival')
                    emit(['ADD',f'X{dd}',f'X{cc}'],'relay_pair_source_encode')
                    emit(['INIT',z['pair_owner'],z['pair_cd']],'relay_pair_owner_birth')
                    emit(['ADD',f'X{cc}',z['pair_owner']],'relay_pair_actual_capture')
                    emit(['ADD',f'X{dd}',f'X{cc}'],'relay_pair_source_inverse')
                    extraowners.append(z['pair_owner']);pairdone.add(serial)
        if keys[j]=='original_X_endpoint_before_cut'and not rawdone:
            for z in configs:
                for i,name in z['raw_cleanup_owners'].items():
                    assert values[f'X{i}']==1<<i and places[f'X{i}']==z['quartet_chart']
                    emit(['INIT',name,z['quartet_chart']],'relay_cleanup_owner_birth')
                    emit(['ADD',f'X{i}',name],'relay_actual_raw_cleanup_capture');extraowners.append(name)
            rawdone=True
        emit(op,keys[j])
    assert pairdone=={0,1}and rawdone
    augmented_source_cut=len(ops)
    for z in configs:
        aa,bb,cc,dd=z['receiver_roles'];ha,hb,hc,hd=z['helper_axis_Y_roles'];T=z['triple_charts']
        # The inverse of the complete future Y-to-Y network is performed while
        # every field is still at ground, on its full actual baseline value.
        forwards=[(aa,cc),(bb,dd),(ha,aa),(hb,bb),(hc,cc),(hd,dd)]
        for source,target in reversed(forwards):emit(['ADD',f'Y{source}',f'Y{target}'],'relay_ground_baseline_inverse')
        for receiver,source in [(aa,bb),(bb,aa),(cc,dd),(dd,cc)]:
            emit(['MOVE',f'Y{receiver}',f'L{source}'],'relay_receiver_native_arrival')
            emit(['ADD',f'NATIVE_{source}',f'Y{receiver}'],'relay_receiver_actual_native_read')
        for receiver in [aa,cc]:emit(['MOVE',f'Y{receiver}',z['pair_bd']],'relay_first_pair_rendezvous')
        emit(['ADD',f'Y{aa}',f'Y{cc}'],'relay_receiver_pair_forward')
        for receiver in [bb,dd]:emit(['MOVE',f'Y{receiver}',z['pair_ac']],'relay_second_pair_rendezvous')
        emit(['ADD',f'Y{bb}',f'Y{dd}'],'relay_receiver_pair_forward')
        for receiver in [aa,bb,cc,dd]:emit(['MOVE',f'Y{receiver}',T[receiver]],'relay_receiver_triple_arrival')
        for helper,receiver in [(ha,aa),(hb,bb)]:
            emit(['MOVE',f'Y{helper}',z['pair_cd']],'relay_helper_pair_arrival')
            emit(['ADD',z['pair_owner'],f'Y{helper}'],'relay_helper_actual_pair_read')
            emit(['MOVE',f'Y{helper}',T[receiver]],'relay_helper_triple_arrival')
            emit(['ADD',f'Y{helper}',f'Y{receiver}'],'relay_helper_forward')
        for helper,receiver,source in [(hc,cc,aa),(hd,dd,bb)]:
            emit(['MOVE',f'Y{helper}',f'L{source}'],'relay_helper_native_arrival')
            emit(['ADD',f'NATIVE_{source}',f'Y{helper}'],'relay_helper_actual_native_read')
            emit(['MOVE',f'Y{helper}',T[receiver]],'relay_helper_triple_arrival')
            emit(['ADD',f'Y{helper}',f'Y{receiver}'],'relay_helper_forward')
        for helper,sources in [(ha,[cc,dd]),(hb,[cc,dd]),(hc,[aa]),(hd,[bb])]:
            emit(['MOVE',f'Y{helper}',z['quartet_chart']],'relay_helper_cleanup_arrival')
            for source in sources:emit(['ADD',z['raw_cleanup_owners'][source],f'Y{helper}'],'relay_helper_actual_cleanup')
            assert values[f'Y{helper}']==(1<<(111+helper))^(1<<helper)
    cut=len(ops);expected=[int(v,16)for v in w['Y_correction_rows_hex']]
    for z in configs:
        for i in z['receiver_roles']:expected[i]^=sum(1<<j for j in z['receiver_roles']if j!=i)
    assert all(values[f'Y{i}']==(1<<(111+i))^expected[i]for i in range(111))
    for j,op in enumerate(oldops[oldcut:],oldcut):emit(op,keys[j])
    for name in extraowners:emit(['CLEAR',name],'relay_added_owner_retirement')
    w['schema']='two-parity-frame-public-Y-correction-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,expected))
    w['construction']['parent_word_sha256']=PARENT_SHA;w['construction']['receiver_parity_relays']=configs
    w['construction']['augmented_reservoir_cut_before_operation']=augmented_source_cut
    w['scope']='Actual two-frame parity-neighbour correction:8 receivers each acquire all3 own-frame native neighbours;8 already-correct coordinate Y records act as couriers and are restored using actually captured raw quartet fields. Ground inverse preloads cancel all arbitrary Y/axis baselines. No added owned movement. All111 X remain restored at Hub;8 diagonal outputs only, no complete supplier.'
    C,cv,ca,stats=replay_general(w,R,geo)
    profile=Counter(parent_stats['movement_profile']);profile.update({1:48,2:4,3:8,4:8,7:-16})
    assert stats['movement_profile']==dict(sorted(profile.items()))
    assert stats['counts']=={'INIT':194,'ADD':1422,'MOVE':516,'CLEAR':194}
    assert len(cv)==416
    assert Counter(len(C[ca[f'Y{i}']])for i in range(111))=={0:95,3:8,4:8}
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    assert all(not(expected[i]&~N[i])for i in range(8,111))
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['relay_pair_actual_capture','relay_pair_source_inverse','relay_actual_raw_cleanup_capture',
                'relay_ground_baseline_inverse','relay_receiver_actual_native_read','relay_receiver_pair_forward',
                'relay_helper_actual_pair_read','relay_helper_actual_native_read','relay_helper_forward','relay_helper_actual_cleanup']:
        bad=json.loads(json.dumps(w));j=sem[key][0];del bad['operations'][j]
        if j<cut:bad['carrier_interface_before_operation']-=1
        try:replay_general(bad,R,geo)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted missing operation',key))
    result={'status':'PASS_ACTUAL_OWN_PARITY_PUBLIC_Y_RELAYS','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
            'source_cut':cut,'augmented_reservoir_cut':augmented_source_cut,'live_fields':len(cv),
            'new_three_neighbour_receivers':[i for z in configs for i in z['receiver_roles']],
            'cleaned_correct_axis_Y_couriers':[i for z in configs for i in z['helper_axis_Y_roles']],
            'additional_foreign_coefficients':24,'total_unknown_receiver_foreign_coefficients':436,
            'added_owned_MOVEs':0,'new_pure_pair_source_owners':2,'new_actual_raw_quartet_cleanup_owners':8,
            'all_arbitrary_Y_coefficients_identity':True,'all_original_X_restored_at_Hub':True,
            'public_Y_rank_histogram':{0:95,3:8,4:8},'stats':stats,'moment':h.record(moment),
            'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
