#!/usr/bin/env python3
"""Exact literal thirty-output verification, full ledger and semantic controls."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
WORD='5566738ce7b2706c0094654fce0e4c1c438e82395dee2e6885ef917f2d4498f3'
BASE='d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71'

def through(w,C,chart,packets):
    target=C[chart];at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};v={n:0 for n in at};arr={n:0 for n in packets};depart={}
    for o in w['operations']:
        op,n,*q=o
        if op=='INIT':at[n]=q[0];v[n]=0
        elif op=='MOVE':
            before,after=C[at[n]]==target,C[q[0]]==target
            if before and not after and n in packets:depart[n]=v[n]
            if after and not before:
                v[n]=1<<packets.index(n)if n in packets else 0
                if n in packets:arr[n]+=1
            at[n]=q[0]
        elif op=='ADD':
            t=q[0]
            if C[at[t]]==target:assert C[at[n]]==target;v[t]^=v[n]
        elif op=='CLEAR':del at[n],v[n]
    assert all(v==1 for v in arr.values());return[depart[n]for n in packets]

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=(a.out/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw)
    br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;old=json.loads(br)
    path=Path(__file__).with_name('retained')/'source_history_engine.py';assert hashlib.sha256(path.read_bytes()).hexdigest()=='c934d8ff2f80970fa7db3dbf98e2d5a96e728b00cf314aa4a8e5d79dce632f29';sp=importlib.util.spec_from_file_location('exact_engine',path);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
    source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']]
    run=e.replay(w,R,S,15,False);rank=lambda rows:len(e.basis(rows));C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts']
    assert run['count']=={'INIT':102,'ADD':858,'MOVE':425,'CLEAR':102}and run['dirty_CLEAR']==102
    assert run['profile']=={1:96,2:69,3:56,4:13,5:71,6:23,7:96,8:1}
    assert sorted(set(w['targets'])-set(old['targets']))==[30,38,39]and set(old['targets'])<set(w['targets'])
    assert w['seed_rows_hex']==old['seed_rows_hex']and w['point_targets']==old['point_targets']and w['early_completed_targets']==[]
    for i in range(111):
        name=f'X{i}';assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==name]==[o for o in old['operations']if o[0]=='MOVE'and o[1]==name]
    matrices={'C0':through(w,C,'C0',['P0','P1','P2']),'M1':through(w,C,'M1',['P3','P4','P5'])}
    for dd in w['third_retention']:
        z,d,b,j=dd['packet'],dd['donor'],dd['old_receiver'],dd['new_receiver'];ch=dd['intermediate_chart'];triad=(1<<b)^(1<<5)^(1<<15)
        assert len(C[ch])==4 and e.contained(C[f'L{d}'],C[ch])and e.contained(C[ch],C['C0'])and e.contained(C[ch],C[f'F{b}'])
        assert e.contained(C['SH2'],C[ch])and e.contained(C[f'L{d}'],C[f'F{j}'])
        assert v[dd['intermediate_owner']]==triad and at[dd['intermediate_owner']]==ch
        assert v[dd['actual_raw_owner']]==v[dd['line_owner']]==1<<j
        assert at[dd['actual_raw_owner']]==ch and at[dd['line_owner']]==f'L{d}'
        assert [o for o in w['operations']if o[0]=='ADD'and o[2]==dd['actual_raw_owner']]==[['ADD',f'X{j}',dd['actual_raw_owner']]]
        assert not any(o[0]=='MOVE'and o[1]in[dd['actual_raw_owner'],dd['intermediate_owner']]for o in w['operations'])
        matrices[ch]=through(w,C,ch,[f'P{z}']);matrices[f'L{d}']=through(w,C,f'L{d}',[f'P{z}'])
    for dd in w['m1_retention']:matrices[f"L{dd['d']}"]=through(w,C,f"L{dd['d']}",[f"P{dd['packet']}"])
    assert all(not any(rows)for rows in matrices.values())
    obs=[int(q['row_hex'],16)for q in run['snapshots']];assert len(obs)==252 and rank(obs)==79
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));K=[(1<<i)|sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)]
    h=w['singular_h'];W=[K[i]&sum(1<<j for j in range(111)if h[j]==h[i])for i in range(111)];assert rank(K)==9 and rank(W)==15 and rank(obs+K+W)==79
    ground=[v[name]for name in v if at[name]=='zero'and not name.startswith('Y')]
    nn=[name for name in v if at[name]not in ['zero','Hub']and not name.startswith('Y')and any(v[name]>>j&1 and not e.contained(C[f'L{j}'],C[at[name]])for j in range(111))]
    assert all(q in nn for q in ['Q1','Q3','Q4'])and len(nn)==18
    normalized=ground+[v[name]for name in nn];assert rank(ground)==14
    assert rank(normalized+[v[f'Y{i}']for i in range(111)])==rank(normalized)+111
    actual=[];rawfits=[];strong=[];bases=[];access=[]
    for i in range(111):
        F=C[f'F{i}'];names=[name for name in nn if e.contained(C[at[name]],F)]
        stock=[v[name]for name in v if not name.startswith('Y')and e.contained(C[at[name]],F)]
        stock +=[row for row,q in zip(obs,run['snapshots'])if e.contained(C[q['chart']],F)]
        local=[1<<j for j in range(111)if dot(i,j)==0];relax=ground+[v[name]for name in names]+local
        if e.solve(stock,1<<i)is not None:actual.append(i)
        if e.solve(relax,1<<i)is not None:rawfits.append(i)
        base=stock+local;bases.append(base)
        if e.solve(base,1<<i)is not None:strong.append(i)
        access.append({'receiver':i,'proper_nonlocal_fields':names})
    known=set();waves=[]
    while True:
        nxt={i for i in range(111)if e.solve(bases[i]+[1<<j for j in sorted(known)],1<<i)is not None};assert known<=nxt
        if nxt==known:break
        waves.append(sorted(nxt-known));known=nxt
    duals=[]
    for i in range(111):
        if i in known:continue
        rows=bases[i]+[1<<j for j in sorted(known)];equations=rows+[1<<i];columns=[sum(((r>>j)&1)<<k for k,r in enumerate(equations))for j in range(111)];lam=e.solve(columns,1<<len(rows));assert lam is not None and lam>>i&1 and all(not((lam&r).bit_count()%2)for r in rows);duals.append({'receiver':i,'annihilator_hex':hex(lam)})
    predicates=[]
    for dd in w['third_retention']:
        z,b,j=dd['packet'],dd['old_receiver'],dd['new_receiver']
        for label,op in [('intermediate_conversion',['ADD',f'PRIVATE{b}',f'P{z}']),('triad_capture',['ADD',f'P{z}',f'TRIAD{b}']),('triad_reset',['ADD',f'TRIAD{b}',f'P{z}']),('actual_raw_capture',['ADD',f'X{j}',f'RAW_J{j}']),('actual_raw_query',['ADD',f'RAW_J{j}',f'P{z}']),('old_delivery',['ADD',f'TRIAD{b}',f'Y{b}']),('new_delivery',['ADD',f'KEEP_M{b}',f'Y{j}']),('retirement',['CLEAR',f'TRIAD{b}'])]:predicates.append((f'{label}_{z}',op))
    rejected=[]
    for label,op in predicates:
        ids=[k for k,o in enumerate(w['operations'])if o==op];assert len(ids)==1
        mutant=copy.deepcopy(w);mutant['operations'].pop(ids[0]);mutant['milestones']={key:-1 for key in w['milestones']};mutant.pop('source_cut',None)
        try:e.replay(mutant,R,S,15,False)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('accepted semantic mutant '+label)
    result={'status':'PASS_LITERAL_THIRD_RETENTION_THIRTY','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],
            'all_input_columns':222,'targets':w['targets'],'counts':run['count'],'profile':run['profile'],'dirty_CLEAR':102,
            'all_original_X_MOVE_routes_unchanged':True,'all_ground_seed_values_unchanged':True,
            'joint_cell_through_rows':matrices,'three_singular_cells_on_each_h0_packet':True,
            'actual_P_snapshots':252,'actual_P_history_rank':79,'actual_history_contains_W15_and_C9':True,
            'all111_W_witnesses':[hex(e.solve(obs,row))for row in W],'all111_C_witnesses':[hex(e.solve(obs,row))for row in K],
            'ground_rank':rank(ground),'complete_normalized_rank':rank(normalized),'rank_with_all_Y_nuisance':rank(normalized)+111,
            'proper_nonlocal_inventory':[{'name':name,'chart':at[name],'row_hex':hex(v[name])}for name in nn],
            'actual_stock_and_history_fitting':actual,'raw_local_fitting':rawfits,'strong_stock_history_raw_fitting':strong,
            'strong_free_point_feedback':{'waves':waves,'closure':sorted(known),'exclusion_duals':duals},'receiver_access':access,
            'semantic_negative_controls':rejected,'negative_controls_disable_invoice_source_cut_and_all_milestones':True,
            'scope':'Actual30 native partial endpoints. Demonstrates genuine three-cell reuse; remains within globally granted old source-bank envelope. No complete supplier or new kappa.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','counts','profile','complete_normalized_rank','actual_stock_and_history_fitting','raw_local_fitting','strong_free_point_feedback']}))
if __name__=='__main__':main()
