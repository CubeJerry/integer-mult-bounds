"""Actual proper half-mode reservoir with every Y retained at ground."""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, hashlib, itertools, json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general
from review_half_sum_gate import independent_rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'full_half_geometry');h=module(a.repo/HELPER,'full_half_arithmetic')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];E=[[int(i==j)for j in range(8)]for i in range(8)]
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    K=[n^(1<<i)for i,n in enumerate(N)]
    charts={'zero':{'kind':'span','rows':[]},'Hub':{'kind':'span','rows':E}}
    for i,r in enumerate(R):
        charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
    groups=defaultdict(list)
    for i,r in enumerate(R):
        if i>=8:groups[tuple(k for k,x in enumerate(r)if x)].append(i)
    configurations=[]
    for serial,(support,roles)in enumerate(groups.items()):
        candidates=[]
        for x,y in itertools.combinations(support,2):
            for sign in [1,-1]:
                S=[i for i in roles if R[i][x]==sign*R[i][y]]
                if len(geo.basis(tuple(tuple(R[i])for i in S)))==3:
                    candidates.append({'pair':[x,y],'sign':sign,'roles':S,'row':sum(1<<i for i in S)})
        base=None
        for x,y in itertools.combinations(support,2):
            both=[z for z in candidates if z['pair']==[x,y]]
            if len(both)==2:
                base=both;break
        assert base is not None
        selected=list(base);basis=independent_rows([z['row']for z in selected])
        for z in candidates:
            new=independent_rows(basis+[z['row']])
            if len(new)>len(basis):selected.append(z);basis=new
            if len(basis)==4:break
        assert len(selected)==4 and len(basis)==4
        G=f'RESERVOIR_G{serial}';charts[G]={'kind':'span','rows':[E[k]for k in support]}
        for n,z in enumerate(selected):
            z['chart']=f'RESERVOIR_H{serial}_{n}';z['owner']=f'HALF_{serial}_{n}'
            z['acquisition']='direct_proper_capture'if n<2 else'paid_quartet_export'
            charts[z['chart']]={'kind':'span','rows':[R[i]for i in z['roles']]}
        configurations.append({'support':list(support),'roles':roles,'quartet_chart':G,'modes':selected})
    C={n:geo.chart(c)for n,c in charts.items()};ops=[];sem={};owners=[]
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    def emit(op,key):
        sem.setdefault(key,[]).append(len(ops));ops.append(op);kind,name,*args=op
        if kind=='INIT':assert name not in values;values[name]=0;places[name]=args[0];owners.append(name)
        elif kind=='ADD':assert C[places[name]]==C[places[args[0]]];values[args[0]]^=values[name]
        elif kind=='MOVE':places[name]=args[0]
        elif kind=='CLEAR':del values[name],places[name];owners.remove(name)
    for i in range(111):
        emit(['INIT',f'NATIVE_{i}',f'L{i}'],'native_cache_birth')
        emit(['ADD',f'X{i}',f'NATIVE_{i}'],'native_capture')
    for i in range(8):
        owner=f'AXIS_{i}';emit(['INIT',owner,f'L{i}'],'axis_owner_birth')
        emit(['ADD',f'X{i}',owner],'axis_actual_capture');emit(['MOVE',owner,'zero'],'axis_paid_descent')
        emit(['ADD',owner,f'Y{i}'],'axis_diagonal_prepare')
    for i in range(8,111):
        for j in range(8):
            if N[i]>>j&1:emit(['ADD',f'AXIS_{j}',f'Y{i}'],'ground_axis_preload')
    for g in configurations:
        G=g['quartet_chart']
        for z in g['modes'][:2]:
            S=z['roles'];H=z['chart'];collector=f'X{S[0]}'
            for i in S:emit(['MOVE',f'X{i}',H],'direct_half_native_gather')
            for i in S[1:]:emit(['ADD',f'X{i}',collector],'direct_half_encode')
            emit(['INIT',z['owner'],H],'direct_half_owner_birth')
            emit(['ADD',collector,z['owner']],'direct_half_actual_capture')
            for i in S[1:]:emit(['ADD',f'X{i}',collector],'direct_half_original_inverse')
            assert values[z['owner']]==z['row']
            for i in S:
                assert values[f'X{i}']==1<<i
                emit(['MOVE',f'X{i}',G],'raw_original_quartet_arrival')
        assert all(values[f'X{i}']==1<<i and places[f'X{i}']==G for i in g['roles'])
        for z in g['modes'][2:]:
            emit(['INIT',z['owner'],G],'cross_half_owner_birth')
            for i in z['roles']:emit(['ADD',f'X{i}',z['owner']],'cross_half_actual_gather')
            emit(['MOVE',z['owner'],z['chart']],'cross_half_paid_unit_descent')
            assert values[z['owner']]==z['row']
    for i in range(111):emit(['MOVE',f'X{i}','Hub'],'original_X_endpoint_before_cut')
    canonical=[];cb=[]
    for i,row in enumerate(K):
        new=independent_rows(cb+[row])
        if len(new)==len(cb):continue
        owner=f'CANONICAL_{i}';emit(['INIT',owner,'Hub'],'canonical_owner_birth')
        for j in range(111):
            if row>>j&1:emit(['ADD',f'X{j}',owner],'canonical_actual_Hub_gather')
        assert values[owner]==row;canonical.append({'role':i,'owner':owner,'row_hex':hex(row)});cb=new
        if len(cb)==9:break
    assert len(cb)==9
    cut=len(ops);expected=[1<<i if i<8 else N[i]&255 for i in range(111)]
    assert all(values[f'Y{i}']==(1<<(111+i))^expected[i]and places[f'Y{i}']=='zero'for i in range(111))
    for i in range(111):emit(['MOVE',f'Y{i}',f'F{i}'],'public_Y_endpoint')
    for owner in list(owners):emit(['CLEAR',owner],'owned_retirement')
    for g in configurations:
        for z in g['modes']:z['row_hex']=hex(z.pop('row'))
    w={'schema':'all-proper-half-reservoir-ground-retention-v1','source_path':SOURCE,'source_sha256':SHA,
       'charts':charts,'operations':ops,'semantic_operation_indices':sem,'carrier_interface_before_operation':cut,
       'Y_correction_rows_hex':list(map(hex,expected)),
       'construction':{'quartets':configurations,'canonical_Hub_basis':canonical,'known_axis_roles':list(range(8))},
       'scope':'All111 Y remain at ground,8 coordinate diagonals and412 native-axis preloads prepared. All111 X are restored at Hub. Four actual proper half modes per quartet span all56 sign-affine directions;28 are directly captured at rank3 and28 are physically exported4→3. Nine canonical modes are actually gathered at Hub. This is a complete-invoice partial source, not a111-output supplier.'}
    C,cv,ca,stats=replay_general(w,R,geo)
    assert stats['movement_profile']=={1:139,2:103,4:103,7:119}
    half_owners=[z['owner']for g in configurations for z in g['modes']]
    half_rows=[cv[n]for n in half_owners];assert len(half_owners)==56 and len(independent_rows(half_rows))==56
    all_halves=[]
    for support,I in groups.items():
        for x,y in itertools.combinations(support,2):
            for sign in [1,-1]:all_halves.append(sum(1<<i for i in I if R[i][x]==sign*R[i][y]))
    assert len(independent_rows(half_rows+all_halves))==56
    assert len(independent_rows(half_rows+[1<<i for i in range(8)]+K))==64
    assert all(ca[n].startswith('RESERVOIR_H')and len(C[ca[n]])==3 for n in half_owners)
    assert all(ca[f'X{i}']=='Hub'and cv[f'X{i}']==1<<i for i in range(111))
    # Every actual initial field inside a receiver facet has only native-neighbour
    # unknown X support. The8 known axis columns are conditioned away.
    xmask=(1<<111)-1;leaks=[]
    for i in range(8,111):
        for name,row in cv.items():
            if geo.sub(C[ca[name]],C[f'F{i}'])and row&xmask&~255&~N[i]:leaks.append([i,name])
    assert not leaks
    moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[
        {'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['axis_actual_capture','axis_paid_descent','ground_axis_preload','direct_half_native_gather',
                'direct_half_encode','direct_half_actual_capture','direct_half_original_inverse',
                'cross_half_actual_gather','cross_half_paid_unit_descent','canonical_actual_Hub_gather']:
        bad=json.loads(json.dumps(w));j=sem[key][0];del bad['operations'][j]
        if j<cut:bad['carrier_interface_before_operation']-=1
        try:
            _,bv,bp,_=replay_general(bad,R,geo);assert (bv,bp)==(cv,ca)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted missing operation',key))
    result={'status':'PASS_ACTUAL_FULL_PROPER_HALF_RESERVOIR','word_sha256':pin,'source_cut':cut,'live_fields':len(cv),
            'actual_half_mode_count_rank':[56,56],'direct_proper_half_captures':28,'paid_quartet_to_half_exports':28,
            'full_half_plus_known_axes_rank':64,'actual_canonical_Hub_rank':9,'all111_original_X_raw_at_Hub':True,
            'all111_Y_retained_at_ground':True,'completed_coordinate_diagonals':8,'native_axis_foreign_preloads':412,
            'all_inside_facet_unknown_information_is_native':True,'stats':stats,'moment':h.record(moment),
            'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),
            'negative_controls':controls,'scope':w['scope']}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
