#!/usr/bin/env python3
"""Actual column substitutions couple the three E imports into lower triples.

Every old use of original b is consistently replaced by b+e in its source
caches and Hub loads. The old b output is repaired by a geometric triple
decoder, and e becomes a new output. No independent raw-b import is granted.
"""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load

BASE='0fa6fd43de9e1782168ed811f39110cfd58f8035f5e90fc81c92c859fd2df96c'
CASES=[('P2',12,39,8,'J22','PRIVATE22','RAW_J39','KEEP_M22',['E77']),
       ('P1',11,38,9,'J23','PRIVATE23','RAW_J38','KEEP_M23',[]),
       ('P0',7,30,36,'J16','PRIVATE16','RAW_J30','KEEP_M16',[])]
DELTA={1:8,2:2,3:-3,4:2,5:2,6:-1,7:-2}


def locations(word):
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    out=[]
    for o in word['operations']:
        out.append(at.copy());op,n,*q=o
        if op=='INIT':at[n]=q[0]
        elif op=='MOVE':at[n]=q[0]
        elif op=='CLEAR':del at[n]
    return out


def build(old,R,case):
    packet,a,b,c,J,private,raw_old,keep,masks=case
    xb,xc=f'X{b}',f'X{c}';ya,yb,yc=f'Y{a}',f'Y{b}',f'Y{c}'
    imp=f'IMPORT_E{c}';prefix=f'{packet}_E{c}'
    K,A,B=f'{prefix}_K',f'{prefix}_A',f'{prefix}_B'
    rbl,rcl,rba,rcb=[f'{prefix}_{s}'for s in['RAW_BL','RAW_CL','RAW_BA','RAW_CB']]
    w=copy.deepcopy(old);where=locations(old)
    for name,T in[(K,[a,b]),(A,[c,b]),(B,[c,a])]:
        assert name not in w['charts'];w['charts'][name]={'kind':'span','rows':[R[i]for i in T]}
    private_birth=[o[2]for o in old['operations']if o[:2]==['INIT',private]]
    assert len(private_birth)==1 and private_birth[0]in[J,'M0']
    retime=private_birth[0]==J
    private_sources=[o[1]for o in old['operations']if o[0]=='ADD'and o[2]==private and o[1]!=xb]
    if retime:assert all(n.startswith('X')for n in private_sources)
    cache_targets=[];hub_loads=[]
    for k,o in enumerate(old['operations']):
        if o[0]=='ADD'and o[2]==xb:raise AssertionError('original b is modified')
        if o[0]=='ADD'and o[1]==xb:
            if where[k][xb]=='Hub':hub_loads.append(o[2])
            elif o[2]!=raw_old:cache_targets.append(o[2])
    assert len(cache_targets)==len(set(cache_targets)) and private in cache_targets
    ops=[['INIT',rbl,f'L{b}'],['ADD',xb,rbl],
         ['INIT',rcl,f'L{c}'],['ADD',xc,rcl],
         ['INIT',rba,A],['INIT',rcb,B]]
    for k,o in enumerate(old['operations']):
        op,n,*q=o
        if raw_old in o:
            if op=='ADD'and n==raw_old and q==[packet]:ops.append(['ADD',imp,packet])
            continue
        if o==['INIT',private,J]:ops.append(['INIT',private,'M0']);continue
        if o==['INIT',keep,f'L{a}']:ops.append(['INIT',keep,K]);continue
        if op=='ADD'and q[0]==private and retime:continue
        if o==['MOVE',xb,J]:
            ops += [['MOVE',xb,A],['ADD',xb,rba],['MOVE',xb,'Extra6'],['ADD',xb,imp]]
            continue
        if o==['MOVE',xb,'C0']:continue
        if op=='ADD'and n==xb:
            if where[k][xb]=='Hub':ops += [o,['ADD',xc,q[0]]]
            continue
        if o==['MOVE',xc,'Extra6']:
            ops += [['MOVE',xc,B],['ADD',xc,rcb]]
        if o==['MOVE',imp,'M1']:
            ops.append(['MOVE',imp,'M0'])
            ops += [['ADD',imp,d]for d in cache_targets]
            ops.append(['MOVE',imp,J]);continue
        if o==['ADD',private,packet]and where[k][packet]==J:continue
        if o==['MOVE',packet,J]and retime:
            ops.append(['ADD',private,packet])
        if o==['MOVE',packet,f'L{a}']:
            ops += [['MOVE',packet,K],['ADD',packet,keep]]
        if o in[['ADD',packet,keep],['ADD',keep,packet]]:continue
        if o==['MOVE',ya,f'F{a}']:
            ops += [['MOVE',ya,f'L{c}'],['ADD',rcl,ya],
                    ['MOVE',ya,A],['ADD',rba,ya]]
        if o==['MOVE',yb,f'L{a}']:
            ops += [['ADD',d,yb]for d in[packet]+masks]
            ops.append(o);ops.append(['ADD',f'RAW{a}',yb]);continue
        if o==['ADD',keep,yb]:continue
        if o==['MOVE',yb,f'F{b}']:
            ops += [['MOVE',yb,B],['ADD',rcb,yb]]
        if o==['MOVE',yc,f'F{c}']:
            ops += [['MOVE',yc,f'L{b}'],['ADD',rbl,yc],
                    ['MOVE',yc,K],['ADD',keep,yc]]
        ops.append(o)
        if retime and op=='MOVE'and n in private_sources and q==['C0']:
            ops.append(['ADD',n,private])
    ops += [['CLEAR',n]for n in[rbl,rcl,rba,rcb]]
    w['operations']=ops;w['targets']=sorted(w['targets']+[c])
    w['schema']='encoded-original-lower-triples-native-word-v1'
    records=w.get('encoded_lower_triples',[])
    records.append({'packet':packet,'triple':[a,b,c],
                    'logical_source_substitution':{str(b):[b,c]},
                    'original_b_new_route':[f'L{b}',A,'Extra6','Hub'],
                    'actual_coded_import':imp,'coded_import_rows':[b,c],
                    'coded_import_route':['Extra6','M0',J],
                    'replaced_actual_M0_cache_contributions':cache_targets,
                    'actual_Hub_loads_with_extra_c_read':hub_loads,
                    'private_cache_retimed_to_M0':retime,
                    'retained_pair_field':keep,'retained_pair_chart':K,
                    'new_stationary_native_and_plane_captures':[rbl,rcl,rba,rcb],
                    'no_independent_raw_b_import':True})
    w['encoded_lower_triples']=records
    w['scope']='Actual partial endpoints with source-wide binary column substitutions, coded existing imports, and physical nested triple decoders. All originals restored; no complete111 supplier or new kappa.'
    return w,records[-1]


def values_at(word,anchor):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    for o in word['operations']:
        if o==anchor:return v,at
        op,n,*q=o
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='MOVE':at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='CLEAR':del v[n],at[n]
    raise AssertionError(anchor)


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--stages',type=int,default=3);a=p.parse_args()
    raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw)
    source=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==old['source_sha256'];R=json.loads(source)['native_roots']
    e=load(a.engine,'encoded_triple_geometry');price=load(a.price_engine,'encoded_triple_price')
    _,_,initial=e.replay(old,R);stages=[];base_hash=BASE
    for case in CASES[:a.stages]:
        packet,x,y,z,J,private,raw_old,keep,masks=case
        OC,OH,before=e.replay(old,R);w,record=build(old,R,case);w['base_word_sha256']=base_hash
        C,H,after=e.replay(w,R)
        assert all(sum(a*b for a,b in zip(R[i],R[j]))==0 for i in[x,y,z]for j in[x,y,z]if i!=j)
        prefix=f'{packet}_E{z}';K,A,B=f'{prefix}_K',f'{prefix}_A',f'{prefix}_B'
        assert e.sub(C[K],C[J])and e.sub(C[A],C['Extra6'])and e.sub(C[B],C['Extra6'])
        ov,oa=values_at(old,['INIT','P7','D3_21'])
        nv,na=values_at(w,['INIT','P7','D3_21'])
        exceptions={raw_old,f'IMPORT_E{z}',f'X{y}'}
        inherited=[]
        for n,r in ov.items():
            if n in exceptions:continue
            transformed=r^((1<<z)if r>>y&1 else 0)
            assert nv[n]==transformed,(case,n,'prepacket logical source substitution')
            inherited.append({'field':n,'old_chart':oa[n],'new_chart':na[n],
                              'old_row_hex':hex(r),'new_row_hex':hex(nv[n])})
        # Before any output decode, every coded import and retained code is actual.
        v,at=values_at(w,['MOVE','Y16','SH2'])
        imp=f'IMPORT_E{z}';assert v[imp]==(1<<y)^(1<<z)and at[imp]==J
        assert v[keep]==(1<<y)^(1<<z)and at[keep]==K
        code=v[packet]
        for mask in masks:code^=v[mask]
        assert code==sum(1<<i for i in[x,y,z])
        expected=before['movement_profile'].copy()
        for d,n in DELTA.items():expected[d]=expected.get(d,0)+n
        assert after['movement_profile']==expected,(case,after['movement_profile'],expected)
        controls=[]
        omitted=[['ADD',f'X{y}',imp],['MOVE',imp,'M0'],['MOVE',imp,J],
                 ['ADD',imp,private],['ADD',f'X{z}',record['actual_Hub_loads_with_extra_c_read'][0]],
                 ['ADD',packet,keep],['ADD',f'{prefix}_RAW_BL',f'Y{z}'],
                 ['ADD',keep,f'Y{z}'],['ADD',f'{prefix}_RAW_CL',f'Y{x}'],
                 ['ADD',f'{prefix}_RAW_BA',f'Y{x}'],['ADD',f'{prefix}_RAW_CB',f'Y{y}']]
        for op in omitted:
            bad=copy.deepcopy(w);bad['operations'].remove(op)
            try:e.replay(bad,R)
            except (AssertionError,KeyError)as ex:controls.append({'removed':op,'failure':str(ex)})
            else:raise AssertionError(('accepted semantic omission',op))
        # One-sided substitution must fail even though a coded source is available.
        bad=copy.deepcopy(w)
        for dest in record['actual_Hub_loads_with_extra_c_read']:bad['operations'].remove(['ADD',f'X{z}',dest])
        try:e.replay(bad,R)
        except (AssertionError,KeyError)as ex:controls.append({'removed':'all matching Hub substitution reads','failure':str(ex)})
        else:raise AssertionError('one-sided source substitution accepted')
        Q=price.moment(after['movement_profile']);budget={127:37,64:74,1:-74}
        for j in range(1,9):budget[1+7*j]=budget.get(1+7*j,0)+74;budget[7*j]=budget.get(7*j,0)-74
        lim=tuple(q/6 for q in price.moment(budget));room=lim[0]-Q[1],lim[1]-Q[0]
        target=a.out/f'outputs{len(w["targets"])}';target.mkdir(parents=True,exist_ok=True)
        encoded=(json.dumps(w,indent=2)+'\n').encode();(target/'WORD.json').write_bytes(encoded);pin=hashlib.sha256(encoded).hexdigest()
        report={'status':'PASS_ACTUAL_ENCODED_ORIGINAL_LOWER_TRIPLE','word_sha256':pin,'base_word_sha256':base_hash,'native_source_sha256':w['source_sha256'],'before':before,'after':after,'target_count':len(w['targets']),'new_target':z,'source_substitution':record,'actual_coded_import_value_hex':hex(v[imp]),'actual_retained_pair_value_hex':hex(v[keep]),'actual_ground_triple_hex':hex(code),'prepacket_inherited_field_substitution_count':len(inherited),'prepacket_substitution_exceptions':sorted(exceptions),'prepacket_source_substitution_fields':inherited,'signed_movement_increment':DELTA,'exact_movement_increment':'8[1]+2[2]-3[3]+2[4]+2[5]-[6]-2[7]','linear_rank_volume_increment':sum(d*n for d,n in DELTA.items()),'price':{'moment':price.display(Q),'limiting_allowance':price.display(lim),'limiting_room':price.display(room),'increment':price.display(price.moment(DELTA))},'negative_controls':controls,'scope':w['scope']}
        (target/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');stages.append(report)
        print(json.dumps({k:report[k]for k in['status','word_sha256','target_count','new_target','after','price']}),flush=True)
        old=w;base_hash=pin
    (a.out/'CHAIN.json').write_text(json.dumps({'initial_word_sha256':BASE,'initial_replay':initial,'stages':[{'targets':r['target_count'],'word_sha256':r['word_sha256'],'new_target':r['new_target'],'counts':r['after']['counts'],'price':r['price']}for r in stages]},indent=2)+'\n')


if __name__=='__main__':main()
