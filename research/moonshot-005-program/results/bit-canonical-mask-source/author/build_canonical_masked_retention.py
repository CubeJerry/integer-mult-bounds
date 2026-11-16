#!/usr/bin/env python3
"""Acquire canonical M1 rows by coupled masks on packets and held originals.

One actual Hub-to-facet auxiliary transports u=c+r. Adding u to both the
principal packet and the held original preserves the old receiver equation;
the packet's retained row becomes c. Original restoration is explicit at Hub.
"""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load

BASE='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd'
CASES=[('P3','ZFIRST3',6,'F4',4),('P4','ZFIRST4',75,'F74',74),
       ('P5','ZFIRST5',79,'F78',78)]

def representation(rows,target):
    piv={}
    for j,row in enumerate(rows):
        co=1<<j
        while row:
            p=row.bit_length()-1
            if p in piv:r,c=piv[p];row^=r;co^=c
            else:piv[p]=(row,co);break
    co=0
    while target:
        p=target.bit_length()-1
        if p not in piv:return None
        r,c=piv[p];target^=r;co^=c
    return co

def trace(word):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    states=[]
    for o in word['operations']:
        states.append((v.copy(),at.copy()));op,n,*q=o
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='MOVE':at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='CLEAR':del v[n],at[n]
    states.append((v.copy(),at.copy()));return states

def build(old,R,e,count):
    states=trace(old);ops=old['operations'];dot=lambda i,j:sum(a*b for a,b in zip(R[i],R[j]))
    canonical=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)]
    cb=list(e.bb(canonical).values());assert len(cb)==9
    candidates=[]
    for packet,field,h,facet,receiver in CASES[:count]:
        start=next(k for k,o in enumerate(ops)if o[0]=='ADD'and o[2]==packet and states[k][1][packet]=='Hub')
        capture=ops.index(['ADD',packet,field]);facet_move=ops.index(['MOVE',packet,facet])
        r=states[capture][0][packet]
        hv,ha=states[start];donors=[f'X{i}'for i in range(111)if ha[f'X{i}']=='Hub']
        restore=next(k for k in range(facet_move,len(ops))if states[k+1][1].get(f'X{h}')=='Hub'and states[k+1][0].get(f'X{h}')==1<<h)
        rv,ra=states[restore+1];restore_donors=[f'X{i}'for i in range(111)if i!=h and ra[f'X{i}']=='Hub']
        possibilities=[]
        for mask in range(1,1<<len(cb)):
            c=0
            for j,z in enumerate(cb):
                if mask>>j&1:c^=z
            u=c^r;hs=representation([hv[n]for n in donors],u)
            if hs is None:continue
            rs=representation([rv[n]for n in restore_donors],u)
            if rs is None:continue
            possibilities.append((hs.bit_count()+rs.bit_count(),u.bit_count(),mask,c,u,hs,rs))
        assert possibilities,(packet,'no actual canonical target')
        possibilities.sort()
        candidates.append({'packet':packet,'field':field,'held':h,'facet':facet,'receiver':receiver,
                           'source_index':start,'capture_index':capture,'facet_move_index':facet_move,
                           'restoration_index':restore,'old_row':r,'Hub_donors':donors,
                           'restore_donors':restore_donors,'possibilities':possibilities,
                           'Hub_rows':[hv[n]for n in donors],
                           'restore_rows':[rv[n]for n in restore_donors]})
    # Exact three-way minimum over the candidate lists subject to independence.
    best=None
    def choose(k,selected,cost):
        nonlocal best
        if best is not None and cost>best[0]:return
        if k==len(candidates):
            key=(cost,tuple(x[2]for x in selected))
            if best is None or key<(best[0],best[1]):best=(cost,key[1],selected.copy())
            return
        lower=sum(d['possibilities'][0][0]for d in candidates[k+1:])
        for row in candidates[k]['possibilities']:
            if best is not None and cost+row[0]+lower>best[0]:break
            if len(e.bb([x[3]for x in selected]+[row[3]]))!=len(selected)+1:continue
            choose(k+1,selected+[row],cost+row[0])
    choose(0,[],0);assert best
    before={};after={};records=[]
    for d,choice in zip(candidates,best[2]):
        packet,field,h,facet=d['packet'],d['field'],d['held'],d['facet'];aux=f'CANON_AUX_{packet}'
        _,_,mask,c,u,hs,rs=choice
        capture_reads=[n for j,n in enumerate(d['Hub_donors'])if hs>>j&1]
        restoration_reads=[n for j,n in enumerate(d['restore_donors'])if rs>>j&1]
        before.setdefault(d['source_index'],[]).extend([['INIT',aux,'Hub']]+[['ADD',n,aux]for n in capture_reads]+[['MOVE',aux,facet]])
        after.setdefault(d['facet_move_index'],[]).extend([['ADD',aux,packet],['ADD',aux,f'X{h}']])
        after.setdefault(d['restoration_index'],[]).extend([['ADD',n,f'X{h}']for n in restoration_reads])
        records.append({'packet':packet,'retained_field':field,'retained_chart':'M1','held_original':f'X{h}',
                        'coupling_chart':facet,'receiver_whose_two_masks_cancel':d['receiver'],
                        'auxiliary':aux,'old_retained_row_hex':hex(d['old_row']),
                        'canonical_row_hex':hex(c),'mask_row_hex':hex(u),'canonical_basis_mask':mask,
                        'available_canonical_choices':len(d['possibilities']),
                        'Hub_source_originals':capture_reads,'Hub_restoration_originals':restoration_reads,
                        'source_old_index':d['source_index'],'coupling_after_old_index':d['facet_move_index'],
                        'restoration_after_old_index':d['restoration_index'],
                        'mask_construction_ADDs':len(capture_reads),'original_restoration_ADDs':len(restoration_reads),
                        'new_unresolved_support':[i for i in range(111)if i not in old['targets']and c>>i&1]})
    newops=[]
    for k,o in enumerate(ops):newops += before.get(k,[])+[o]+after.get(k,[])
    newops += [['CLEAR',d['auxiliary']]for d in records]
    w=copy.deepcopy(old);w.update(operations=newops,schema='coupled-held-original-canonical-retention-v1',
        base_word_sha256=BASE,canonical_retention_couplings=records,
        canonical_code_definition='K_i = e_i + sum_{j: r_i dot r_j=0} e_j; C9=span_i K_i',
        scope='Actual canonical source rows atM1 via coupled packet/held-original masks; all46 old endpoints and original restorations retained. New source information, not new completed outputs or full supplier.')
    return w,records,cb,best[0]

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--count',type=int,default=3);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw)
    src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'canonical_mask_engine');price=load(a.price_engine,'canonical_mask_price');OC,OH,before=e.replay(old,R)
    w,records,cb,paid_adds=build(old,R,e,a.count);C,H,after=e.replay(w,R);n=len(records)
    expected=before['movement_profile'].copy();expected[1]+=n;assert after['movement_profile']==expected
    assert after['counts']=={k:v+({'INIT':n,'ADD':paid_adds+2*n,'MOVE':n,'CLEAR':n}[k])for k,v in before['counts'].items()}
    assert after['dirty_CLEAR']==before['dirty_CLEAR']+n
    oldstates=trace(old);newstates=trace(w)
    oi=next(k for k,o in enumerate(old['operations'])if o[0]=='CLEAR');ni=next(k for k,o in enumerate(w['operations'])if o[0]=='CLEAR');ov,oa=oldstates[oi];nv,na=newstates[ni];changed={d['retained_field']for d in records}
    assert all(nv[name]==row and na[name]==oa[name]for name,row in ov.items()if name not in changed)
    for d in records:assert nv[d['retained_field']]==int(d['canonical_row_hex'],16)and na[d['retained_field']]=='M1'
    m1old=[r for name,r in ov.items()if not r>>111 and C[oa[name]]==C['M1']]
    m1new=[r for name,r in nv.items()if not r>>111 and C[na[name]]==C['M1']]
    irank=lambda rows:len(e.bb(rows))+len(cb)-len(e.bb(rows+cb))
    assert irank(m1old)==0 and irank(m1new)==n
    protected={name:{'value_hex':hex(nv[name]),'chart':na[name]}for name in old['protected_source_contracts']};assert protected==old['protected_source_contracts']
    controls=[]
    for d in records:
        aux=d['auxiliary'];packet=d['packet'];held=d['held_original']
        tests=[['MOVE',aux,d['coupling_chart']],['ADD',aux,packet],['ADD',aux,held],
               ['ADD',d['Hub_source_originals'][0],aux],['ADD',d['Hub_restoration_originals'][0],held],['CLEAR',aux]]
        for op in tests:
            bad=copy.deepcopy(w);bad['operations'].remove(op)
            try:e.replay(bad,R)
            except(AssertionError,KeyError)as ex:controls.append({'removed':op,'failure':str(ex)})
            else:raise AssertionError(('accepted mask/source omission',op))
        # Coupled deletion preserves old endpoints but removes the new contract.
        bad=copy.deepcopy(w)
        remove=[['ADD',aux,packet],['ADD',aux,held]]+[['ADD',x,held]for x in d['Hub_restoration_originals']]
        # Locate restoration reads by their inserted block, not by equal old ADDs.
        for op in remove[:2]:bad['operations'].remove(op)
        seq=remove[2:];ix=next(i for i in range(len(bad['operations']))if bad['operations'][i:i+len(seq)]==seq);del bad['operations'][ix:ix+len(seq)]
        e.replay(bad,R);bs=trace(bad);bi=next(k for k,o in enumerate(bad['operations'])if o[0]=='CLEAR');assert bs[bi][0][d['retained_field']]==int(d['old_retained_row_hex'],16)
        controls.append({'removed':'both coupled masks and their matching restoration','packet':packet,'old46_endpoints_still_pass':True,'new_canonical_source_contract_fails':True})
    # Each canonical field is simultaneously and legally readable by the last
    # packet at M1 immediately after its ordinary retention reset.
    probe=copy.deepcopy(w);last=records[-1];anchor=['ADD',last['retained_field'],last['packet']];ix=probe['operations'].index(anchor)+1
    extra=[]
    for d in records:extra += [['ADD',d['retained_field'],last['packet']]]*2
    probe['operations'][ix:ix]=extra;e.replay(probe,R)
    Q=price.moment(expected);B={127:37,64:74,1:-74}
    for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
    lim=tuple(x/6 for x in price.moment(B));room=lim[0]-Q[1],lim[1]-Q[0]
    a.out.mkdir(parents=True,exist_ok=True);blob=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(blob)
    out={'status':'PASS_ACTUAL_CANONICAL_M1_RETENTION_BY_COUPLED_MASKS','word_sha256':hashlib.sha256(blob).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':old['source_sha256'],'before':before,'after':after,'actual_couplings':records,'canonical_basis_hex':[hex(r)for r in cb],'M1_canonical_intersection_rank_before':0,'M1_canonical_intersection_rank_after':n,'all_other_old_owned_values_and_charts_preserved':True,'protected_source_contracts':protected,'all46_old_endpoints_preserved':True,'new_complete_outputs':0,'joint_actual_M1_read_unread_probe_passes':True,'exact_movement_increment':f'{n}[1]','price':{'moment':price.display(Q),'limiting_allowance':price.display(lim),'limiting_room':price.display(room)},'negative_and_source_contract_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in['status','word_sha256','after','M1_canonical_intersection_rank_after','price']}))

if __name__=='__main__':main()
