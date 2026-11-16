#!/usr/bin/env python3
"""Lower actual M1 canonical rows using existing packets and paid old readers."""
from pathlib import Path
import argparse, copy, hashlib, json
from source_loader import load
from build_canonical_masked_retention import trace

BASE='7d2fea44d7bdf8b3a63807f88371cad28f9303649db66b7d4ccbb56e9c180ada'
CASES=[{'packet':'P5','field':'ZFIRST5','retention':'P5_RET','targets':[45,48,49],
        'remove_loads':['H6_2','H6_3','Q2','RAW49','E79']},
       {'packet':'P4','field':'ZFIRST4','retention':'P4_RET','targets':[29,40,42],
        'remove_loads':['CAP2942','RAW40','E75']}]

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--count',type=int,choices=[1,2],default=1);a=p.parse_args()
    raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw)
    src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots']
    e=load(a.engine,'lower_canonical_engine');price=load(a.price_engine,'lower_canonical_price');C,OH,before=e.replay(old,R)
    cases=CASES[:a.count];points=sorted(i for d in cases for i in d['targets']);ys={f'Y{i}' for i in points}
    remove={tuple(['ADD',x,d['packet']])for d in cases for x in d['remove_loads']}
    anchors={tuple(['ADD',d['field'],d['packet']]):d for d in cases}
    ops=[]
    for i in points:ops += [['INIT',f'CANON_OLD_RAW{i}',f'L{i}'],['ADD',f'X{i}',f'CANON_OLD_RAW{i}'],['MOVE',f'CANON_OLD_RAW{i}','zero']]
    for o in old['operations']:
        if o[0]=='ADD' and o[2] in ys:continue
        if o[0]=='MOVE' and o[1] in ys:
            i=int(o[1][1:])
            if o[2]==f'F{i}':ops += [['ADD',f'CANON_OLD_RAW{i}',o[1]],o]
            continue
        if tuple(o)in remove:continue
        ops.append(o)
        if tuple(o)in anchors:
            # The first identical ADD performs the old reset. This second read
            # loads the real retained canonical row into the now-zero packet.
            ops.append(o.copy())
    ops += [['CLEAR',f'CANON_OLD_RAW{i}']for i in points]
    w=copy.deepcopy(old);w.update(operations=ops,schema='actual-canonical-lowering-with-paid-old-readers-v1',
        base_word_sha256=BASE,lowered_canonical_packets=[d['packet']for d in cases],
        newly_paid_native_returns=points,
        scope='Actual one or two independent canonical rows carried from M1 to common by existing principal descents; every old46 endpoint and all three M1 canonical/import contracts retained. Old lower readers receive explicitly paid native returns. No new completed output or full supplier.')
    C,H,after=e.replay(w,R)
    os=trace(old);ns=trace(w);oi=next(k for k,o in enumerate(old['operations'])if o[0]=='CLEAR');ni=next(k for k,o in enumerate(ops)if o[0]=='CLEAR');ov,oa=os[oi];nv,na=ns[ni]
    changed={d[k]for d in cases for k in ['packet','retention']}
    assert all(nv[n]==v and na[n]==oa[n]for n,v in ov.items()if n not in changed)
    rows=[]
    for d in cases:
        row=ov[d['field']];assert nv[d['packet']]==nv[d['retention']]==row and na[d['packet']]=='zero';rows.append(row)
    assert len(e.bb(rows))==len(cases)
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));canonical=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];cb=list(e.bb(canonical).values());assert all(e.fits(cb,r)for r in rows)
    ground=lambda v,at:[z for n,z in v.items()if not z>>111 and C[at[n]]==C['zero']]
    irank=lambda rr:len(e.bb(rr))+len(cb)-len(e.bb(rr+cb))
    oldg=ground(ov,oa);newg=ground(nv,na);known=sum(1<<i for i in old['targets'])
    unknown_rank=lambda rr:len(e.bb(z&~known for z in rr));assert unknown_rank(oldg)==0;assert unknown_rank(newg)==len(cases)
    protected={name:{'value_hex':hex(nv[name]),'chart':na[name]}for name in old['protected_source_contracts']};assert protected==old['protected_source_contracts']
    expected=before['movement_profile'].copy();n=len(points)
    for d,v in {1:-n,5:-n,7:n}.items():expected[d]+=v
    assert after['movement_profile']==expected,(after['movement_profile'],expected)
    controls=[]
    for i in points:
        for op in [['ADD',f'X{i}',f'CANON_OLD_RAW{i}'],['MOVE',f'CANON_OLD_RAW{i}','zero'],['ADD',f'CANON_OLD_RAW{i}',f'Y{i}']]:
            bad=copy.deepcopy(w);bad['operations'].remove(op)
            try:e.replay(bad,R)
            except(AssertionError,KeyError)as ex:controls.append({'removed':op,'failure':str(ex)})
            else:raise AssertionError(('accepted paid reader omission',op))
    for d in cases:
        bad=copy.deepcopy(w);op=['ADD',d['field'],d['packet']];ix=bad['operations'].index(op);assert bad['operations'][ix+1]==op;del bad['operations'][ix+1]
        e.replay(bad,R);bs=trace(bad);bi=next(k for k,o in enumerate(bad['operations'])if o[0]=='CLEAR');assert bs[bi][0][d['packet']]==0
        controls.append({'removed':'second actual canonical read at M1','packet':d['packet'],'all46_endpoints_still_pass':True,'common_canonical_contract_fails':True})
    Q=price.moment(expected);B={127:37,64:74,1:-74}
    for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
    lim=tuple(x/6 for x in price.moment(B));room=lim[0]-Q[1],lim[1]-Q[0]
    a.out.mkdir(parents=True,exist_ok=True);blob=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(blob)
    result={'status':'PASS_ACTUAL_CANONICAL_COMMON_WITH_PAID_OLD_READERS','word_sha256':hashlib.sha256(blob).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':old['source_sha256'],'before':before,'after':after,
        'canonical_common_fields':[{**{k:d[k]for k in ['packet','field','retention','targets']},'row_hex':hex(nv[d['packet']]),'retained_chart':na[d['retention']]}for d in cases],
        'all_other_old_owned_fields_and_charts_preserved':True,'protected_source_contracts':protected,
        'old46_endpoints_preserved':True,'new_completed_outputs':0,'common_canonical_intersection_rank_before':irank(oldg),'common_canonical_intersection_rank_after':irank(newg),
        'common_unfinished_quotient_rank_before':unknown_rank(oldg),'common_unfinished_quotient_rank_after':unknown_rank(newg),
        'unfinished_points_with_new_common_own_coefficient':[i for i in range(111)if i not in old['targets']and any(r>>i&1 for r in rows)],
        'exact_movement_increment':f'{n}[7]-{n}[5]-{n}[1]',
        'price':{'moment':price.display(Q),'limiting_room':price.display(room)},'controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','word_sha256','after','common_canonical_intersection_rank_after','common_unfinished_quotient_rank_after','exact_movement_increment','price']}))

if __name__=='__main__':main()
