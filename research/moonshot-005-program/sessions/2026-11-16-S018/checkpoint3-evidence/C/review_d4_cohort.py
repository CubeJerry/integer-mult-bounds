#!/usr/bin/env python3
"""Independent rational/all-column review of A's D4 cohort composition."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
from release_projection import N, binary_basis, chart, replay, require, rref
from price_projection import moment, record

PINS={
    'pruned78':('c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245',
        'dd0af2d4467b722c1692fb60b883407b4a95a8ea10b112fca0683dfc4a930edf'),
    'paid46':('27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd',
        'bd7fd31ba6cfe1bc92d26619e513184e6ce5864653cf58be7e9b68668be0d987')}
FRAMES=[[3,4,47,51],[74,80,90,92],[76,78,88,94]]


def main():
    ap=argparse.ArgumentParser()
    for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
    ap.add_argument('--base',choices=PINS,required=True)
    a=ap.parse_args()
    bp=(a.work/'A/pruned78/WORD.json' if a.base=='pruned78' else
        a.repo/'research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json')
    wp=a.work/('A/d4-cohort-'+a.base)/'WORD.json'
    br,wr=bp.read_bytes(),wp.read_bytes()
    require((hashlib.sha256(br).hexdigest(),hashlib.sha256(wr).hexdigest())==PINS[a.base],'source/word pins')
    b,w=json.loads(br),json.loads(wr)
    sr=(a.repo/b['source_path']).read_bytes()
    require(hashlib.sha256(sr).hexdigest()==b['source_sha256']==w['source_sha256'],'native root pin')
    R=json.loads(sr)['native_roots']
    for i,root in enumerate(R):
        require(chart(w['charts'][f'L{i}'])==chart({'kind':'span','rows':[root]}),('native line',i))
        require(chart(w['charts'][f'F{i}'])==chart({'kind':'ann','rows':[root]}),('native facet',i))
    for n,c in b['charts'].items():require(w['charts'][n]==c,('inherited chart unchanged',n))
    before,bt,bc=replay(b,collect=True)
    after,nt,_=replay(w,collect=True)
    D=sorted(i for g in FRAMES for i in g);ds=set(D)
    common=chart(w['charts']['D4_COMMON_MEET'])
    require(len(common)==4 and len(rref(common+chart(w['charts']['M1']))[0])==5,'actual rank4 meet below M1')
    eligible=[i for i in range(N)if len(rref(common+chart(w['charts'][f'F{i}']))[0])==7]
    require(eligible==D,'exact12 receiver cohort')
    require(w['cohort']['frames']==FRAMES,'actual quartet partition')
    require(not any(o[0]=='ADD'and o[2]in{f'X{i}'for i in D}for o in b['operations']),'immutable projected originals')
    require(not any(o[0]=='ADD'and o[1].startswith('Y')for o in b['operations']),'detached old Ys have no readers')
    require(set(w['targets'])==set(b['targets'])|ds and len(w['targets'])==52,'all52 target set')
    cache_names=[]
    pre=w['cohort']['prelude_end'];pv,pa=nt[pre]
    for group in FRAMES:
        require(all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i,j in itertools.combinations(group,2)),('orthogonal frame',group))
        for j,i in enumerate(group):
            require(pv[f'X{i}']==1<<i and pa[f'X{i}']=='Hub','source original raw at Hub after cache prelude')
            for k in range(1,4):
                interval=[group[(j+h)%4]for h in range(k)]
                expected=rref(common+tuple(tuple(z)for z in [R[h]for h in interval]))[0]
                lab=f'D4_FLAG_{i}_{k}';name=f'D4_RAW_{i}_{k}';cache_names.append(name)
                require(chart(w['charts'][lab])==expected and len(expected)==4+k,('actual cyclic source interval',i,k))
                require(pv[name]==1<<i and pa[name]==lab,('actual raw stationary cache',i,k))
                require(not any(o[0]=='MOVE'and o[1]==name for o in w['operations']),('stationary cache has no transport',name))
    for i in range(N):require(pv[f'Y{i}']==1<<(N+i)and pa[f'Y{i}']=='zero','all Ys await source at ground')
    source_checks=[]
    for j,group in zip([3,4,5],FRAMES):
        packet,field=f'P{j}',f'ZFIRST{j}'
        cap=w['operations'].index(['ADD',packet,field])
        reset=w['operations'].index(['ADD',field,packet])
        down=w['operations'].index(['MOVE',field,'D4_COMMON_MEET'])
        cv,ca=nt[cap];rv,ra=nt[reset]
        value=sum(1<<i for i in group)
        require(cv[packet]==value and ca[packet]=='M1','actual programmed packet at first capture')
        require(rv[field]==rv[packet]==value and ra[field]=='M1','actual first retention and reset operands')
        require(nt[reset+1][0][packet]==0,'lower packet reset really cancels changed source')
        require(reset<down,'first field stays for its packet reset before descending')
        require([o for o in w['operations'][:cap+1]if o[0]=='ADD'and o[1]==packet]==[['ADD',packet,field]],'no earlier packet payload reader')
        source_checks.append({'packet':packet,'capture':cap,'reset':reset,'down':down,'row_hex':hex(value)})
    ci=w['cohort']['continuation_before_operation']
    bi=b.get('carrier_interface_before_operation',bc[0])
    bv,ba=bt[bi]
    oldowners={o[1]for o in b['operations']if o[0]=='INIT'}
    ground=sorted(n for n in oldowners if n in bv and bv[n] and len(chart(b['charts'][ba[n]]))==0)
    require(len(ground)==25 and len(binary_basis(bv[n]for n in ground))==25,'actual predecessor25 fields')
    released=sorted(set(b.get('released_carriers',[]))-ds)

    def interface(ww):
        _,tr,_=replay(ww,collect=True);v,at=tr[ww['cohort']['continuation_before_operation']]
        for n in ground:require(v[n]==bv[n] and len(chart(ww['charts'][at[n]]))==0,('individual common field',n))
        for f,g in zip(['ZFIRST3','ZFIRST4','ZFIRST5'],FRAMES):
            require(v[f]==sum(1<<i for i in g) and chart(ww['charts'][at[f]])==common,('actual retained quartet field',f))
        for i in released:require(v[f'X{i}']==1<<i and at[f'X{i}']==f'L{i}',('raw native custody',i))
        for i in range(N):
            require(v[f'X{i}']==1<<i,('cut raw original',i))
            if i not in ww['targets']:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero',('available unfinished Y',i))
            else:require(v[f'Y{i}']==(1<<(N+i))^(1<<i)and at[f'Y{i}']==f'F{i}',('completed cut Y',i))
        return v,at

    values,locations=interface(w)
    require(w['released_carriers']==released,'retained original interface list')
    require(len(released)==(72 if a.base=='pruned78'else 0),'actual retained carrier count')
    controls=[]
    def reject(label,ww,check=interface):
        try:check(ww)
        except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
        else:raise ValueError(('accepted D4 control',label))
    for label,event in [
        ('omit stationary raw capture',['ADD','X3','D4_RAW_3_1']),
        ('omit true Hub source input',['ADD','X47','P3']),
        ('omit actual common descent',['MOVE','ZFIRST3','D4_COMMON_MEET']),
        ('omit first packet reset',['ADD','ZFIRST3','P3']),
        ('omit local cache retirement',['CLEAR','D4_RAW_3_1'])]:
        bad=copy.deepcopy(w);bad['operations'].remove(event);reject(label,bad,lambda ww:replay(ww))
    for label,event in [
        ('changed quartet field after decoder',['ADD','ZFIRST4','ZFIRST3']),
        ('changed named ground field after decoder',['ADD','P1','P0'])]:
        bad=copy.deepcopy(w);bad['operations'].insert(ci,event)
        bad['cohort']['continuation_before_operation']=ci+1
        bad['carrier_interface_before_operation']=ci+1
        replay(bad)
        reject(label,bad)
    if released:
        bad=copy.deepcopy(w);event=['MOVE','X5','Hub']
        require(bad['operations'].index(event)>=ci,'released carrier old closure occurs later')
        bad['operations'].remove(event);bad['operations'].insert(ci,event)
        bad['cohort']['continuation_before_operation']=ci+1
        bad['carrier_interface_before_operation']=ci+1
        replay(bad);reject('native original closes before advertised interface',bad)
    bad=copy.deepcopy(w);event=['MOVE','Y5','F5']
    require(bad['operations'].index(event)>=ci,'unfinished output closure occurs later')
    bad['operations'].remove(event);bad['operations'].insert(ci,event)
    bad['cohort']['continuation_before_operation']=ci+1
    bad['carrier_interface_before_operation']=ci+1
    replay(bad);reject('unfinished output departs before advertised interface',bad)
    originals={f'{p}{i}'for p in ['X','Y']for i in range(N)}
    owned={n:z for n,z in values.items()if n not in originals}
    support=0
    for row in owned.values():support|=row
    for i in range(N):support|=values[f'Y{i}']^(1<<(N+i))
    require(support>>N==0,'all retained source and output offsets y-free')
    S=[i for i in range(N)if support>>i&1]
    require(len(S)==(54 if a.base=='pruned78'else 111),'actual source support count')
    if a.base=='pruned78':
        require(set(S)==set(w['targets'])|{61,67},'exact known-coordinate reset interface S54')
        require(after['counts']=={'MOVE':422,'INIT':130,'ADD':423,'CLEAR':130},'complete pruned-based counts')
        require(after['movement_profile']=={1:167,2:11,3:34,4:32,5:16,6:9,7:153},'complete pruned-based movement')
    else:
        require(after['counts']=={'MOVE':538,'INIT':163,'ADD':752,'CLEAR':163},'complete paid-based counts')
        require(after['movement_profile']=={1:248,2:34,3:60,4:33,5:63,6:16,7:84},'complete paid-based movement')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):
        gate[1+7*j]=gate.get(1+7*j,0)+74
        gate[7*j]=gate.get(7*j,0)-74
    gl,gh=moment(gate);limit=(gl/6,gh/6)
    q=moment(after['movement_profile']);oldq=moment(before['movement_profile'])
    result={'status':'PASS_INDEPENDENT_D4_SHARED_TWELVE_RECEIVER_COMPOSITION',
        'base_kind':a.base,'base_sha256':PINS[a.base][0],'word_sha256':PINS[a.base][1],
        'native_source_sha256':b['source_sha256'],'frames':FRAMES,
        'exact_common_facet_cohort':D,'common_chart_rank':len(common),
        'actual_stationary_raw_caches':36,'actual_programmed_source_fields':source_checks,
        'before':before,'after':after,'all222_endpoints':True,'targets':w['targets'],
        'new_targets':sorted(set(w['targets'])-set(b['targets'])),
        'interface_index':ci,'preserved_individual_ground_fields':ground,
        'preserved_ground_rank':25,'retained_raw_native_count':len(released),
        'retained_raw_native_roles':released,'unfinished_ground_Y_count':N-len(w['targets']),
        'actual_live_owner_count':len(owned),'actual_live_owner_rank':len(binary_basis(owned.values())),
        'source_coordinate_support':S,'source_coordinate_support_size':len(S),
        'whole_moment':record(q),'base_moment':record(oldq),
        'moment_change':record((q[0]-oldq[1],q[1]-oldq[0])),
        'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),
        'controls':controls,
        'scope':'Independent actual source/co-location, all222 endpoint, common-field, stationary-cache, source-retention, native-custody and complete movement checks. Changed history contracts; no all111 construction or kappa.'}
    if a.base=='pruned78':
        baseline=moment({1:54,7:222})
        result['conditional_direct54_reset_reference']=record(baseline)
        result['reset_scope']='Known-source reset applies to a fixed future continuation only with its actual original-restoration condition. This raw54 price does not execute that continuation for free.'
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','base_kind','after','retained_raw_native_count','whole_moment','necessary_limiting_room']},indent=2))


if __name__=='__main__':main()
