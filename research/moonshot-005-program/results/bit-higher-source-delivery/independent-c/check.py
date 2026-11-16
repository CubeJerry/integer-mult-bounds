#!/usr/bin/env python3
"""Independent32/34 actual higher-source delivery and complete stock audit."""
import argparse,copy,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PINS={32:'73a6c4adb00498a0c33956a3aa1a0525eb143fa0179a4abaeb238b150774da45',34:'46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'}
BASE='6a1eef8ef1f620914b3f014c9ba129bbe389c6fd5a010872f3e5cca88f5cb52f'
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    wr=a.word.read_bytes();w=json.loads(wr);n=len(w['targets']);assert hashlib.sha256(wr).hexdigest()==PINS[n];br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;base=json.loads(br)
    retained=Path(__file__).with_name('retained');e=module(retained/'source_history_engine.py','independent');t=module(retained/'interval_price.py','rigorous_price')
    source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];S=[int(r,16)for r in w['seed_rows_hex']]
    run=e.replay(w,R,S,15,False);base_run=e.replay(base,R,[int(x,16)for x in base['seed_rows_hex']],15,False);rank=lambda rows:len(e.basis(rows));C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];old=base_run['cuts']['seed']['values']
    added=[10,27]if n==32 else[10,19,20,27];assert sorted(set(w['targets'])-set(base['targets']))==added and set(base['targets'])<set(w['targets'])
    count={32:{'INIT':111,'ADD':890,'MOVE':433,'CLEAR':111},34:{'INIT':114,'ADD':902,'MOVE':435,'CLEAR':114}}
    profiles={32:{1:108,2:65,3:56,4:13,5:72,6:24,7:95},34:{1:110,2:65,3:56,4:13,5:73,6:24,7:94}}
    assert run['count']==count[n]and run['dirty_CLEAR']==count[n]['CLEAR']and run['profile']==profiles[n]
    records=[w['higher_source_delivery']]+([w['extra_source_delivery']]if n==34 else[])
    for rec in records:
        z=rec['packet'];mask=sum(1<<j for j in rec['ground_mask_points']);d=27 if z==7 else 19;j=10 if z==7 else 20
        assert v[rec['first_retention']]==old[f'P{z}']^mask and at[rec['first_retention']]==rec['first_chart']
        assert v[rec['second_retention']]==v[rec['actual_acquired_owner']]==1<<j and at[rec['second_retention']]==f'L{d}'
        assert v[rec['actual_raw_owner']]==1<<d and at[rec['actual_raw_owner']]==f'L{d}'and v[f'P{z}']==(1<<d)^mask
        assert len(C[rec['first_chart']])==6 and e.contained(C[f'L{d}'],C[rec['first_chart']])and e.contained(C[f'L{d}'],C[f'F{j}'])
    changed={r['packet']for r in records};assert all(v[f'P{z}']==old[f'P{z}']for z in range(8)if z not in changed)
    for j in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{j}']==[o for o in base['operations']if o[0]=='MOVE'and o[1]==f'X{j}']
    ground=[r for name,r in v.items()if at[name]=='zero'and not name.startswith('Y')]
    nn=[name for name in v if at[name]not in ['zero','Hub']and not name.startswith('Y')and any(v[name]>>j&1 and not e.contained(C[f'L{j}'],C[at[name]])for j in range(111))]
    assert all(name in nn for name in ['Q1','Q3','Q4','HKEEP_D7','HKEEP_L27']);normal=ground+[v[name]for name in nn]
    assert rank(normal+[v[f'Y{i}']for i in range(111)])==rank(normal)+111
    obs=[int(q['row_hex'],16)for q in run['snapshots']];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));K=[(1<<i)|sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];hh=w['singular_h'];W=[K[i]&sum(1<<j for j in range(111)if hh[i]==hh[j])for i in range(111)]
    stockfits=[];rawfits=[];bases=[];access=[]
    for i in range(111):
        F=C[f'F{i}'];stock=[v[name]for name in v if not name.startswith('Y')and e.contained(C[at[name]],F)];stock +=[row for row,q in zip(obs,run['snapshots'])if e.contained(C[q['chart']],F)]
        local=[1<<j for j in range(111)if dot(i,j)==0];names=[name for name in nn if e.contained(C[at[name]],F)]
        if e.solve(stock,1<<i)is not None:stockfits.append(i)
        if e.solve(ground+[v[name]for name in names]+local,1<<i)is not None:rawfits.append(i)
        bases.append(stock+local);access.append({'receiver':i,'proper_nonlocal_fields':names})
    known=set();waves=[]
    while True:
        nxt={i for i in range(111)if e.solve(bases[i]+[1<<j for j in sorted(known)],1<<i)is not None};assert known<=nxt
        if nxt==known:break
        waves.append(sorted(nxt-known));known=nxt
    duals=[]
    for i in range(111):
        if i in known:continue
        rows=bases[i]+[1<<j for j in sorted(known)];eq=rows+[1<<i];cols=[sum(((r>>j)&1)<<k for k,r in enumerate(eq))for j in range(111)];lam=e.solve(cols,1<<len(rows));assert lam is not None and lam>>i&1 and all(not((lam&r).bit_count()%2)for r in rows);duals.append({'receiver':i,'annihilator_hex':hex(lam)})
    profile=run['profile'];delta=Counter(profile)
    for k,value in base_run['profile'].items():delta[k]-=value
    expected={1:2,2:1,5:1,6:1,7:-1,8:-1}if n==32 else{1:4,2:1,5:2,6:1,7:-2,8:-1};assert{k:value for k,value in delta.items()if value}==expected
    B=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
    for j in range(1,9):B[1+7*j]+=Fraction(74,6);B[7*j]-=Fraction(74,6)
    room=B.copy()
    for k,value in profile.items():room[k]-=value
    tests=[('omit_real_private_capture',['ADD','X10','AFF0']),('omit_old_P7_retention',['ADD','P7','HKEEP_D7']),('omit_first_reset',['ADD','HKEEP_D7','P7']),('omit_real_higher_query',['ADD','AFF0','P7']),('omit_low_line_retention',['ADD','P7','HKEEP_L27']),('omit_second_reset',['ADD','HKEEP_L27','P7']),('omit_native_raw_capture',['ADD','X27','HRAW27']),('omit_new_nonlocal_delivery',['ADD','HKEEP_L27','Y10']),('omit_ground_mask',['ADD','E73','Y27']),('omit_new_retirement',['CLEAR','HKEEP_L27'])]
    if n==34:tests +=[('omit_Extra_source_capture',['ADD','X20','EXTRA_AFF']),('omit_P6_old_retention',['ADD','P6','HKEEP_E6']),('omit_P6_reset',['ADD','HKEEP_E6','P6']),('omit_Extra_actual_query',['ADD','EXTRA_AFF','P6']),('omit_L19_retention',['ADD','P6','HKEEP_L19']),('omit_L19_reset',['ADD','HKEEP_L19','P6']),('omit_native19_capture',['ADD','X19','HRAW19']),('omit_Y20_delivery',['ADD','HKEEP_L19','Y20']),('omit_Y19_mask',['ADD','E75','Y19']),('omit_Extra_retirement',['CLEAR','HKEEP_E6'])]
    rejected=[]
    for label,op in tests:
        m=copy.deepcopy(w);ids=[j for j,o in enumerate(m['operations'])if o==op]
        assert len(ids)==(2 if label=='omit_Extra_actual_query'else 1)
        m['operations'].pop(ids[-1]if label=='omit_Extra_actual_query'else ids[0]);m['milestones']={k:-1 for k in w['milestones']};m.pop('source_cut',None)
        try:e.replay(m,R,S,15,False)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('accepted mutant '+label)
    receipt={'status':'PASS_INDEPENDENT_ACTUAL_HIGHER_SOURCE','word_sha256':PINS[n],'common_expanded_base_sha256':BASE,'native_source_sha256':w['source_sha256'],'columns':222,'targets':w['targets'],'counts':run['count'],'profile':profile,'dirty_CLEAR':run['dirty_CLEAR'],
             'all_original_X_MOVE_routes_unchanged':True,'changed_P6_P7_terminal_rows_and_old_code_replacements_checked':True,
             'history_snapshot_count':len(obs),'history_rank':rank(obs),'history_W_intersection':rank(obs)+15-rank(obs+W),'history_C_intersection':rank(obs)+9-rank(obs+K),
             'ground_rank':rank(ground),'proper_nonlocal_count':len(nn),'complete_normalized_rank':rank(normal),'rank_with_all_Y_nuisance':rank(normal)+111,
             'proper_nonlocal_inventory':[{'name':name,'chart':at[name],'row_hex':hex(v[name])}for name in nn],
             'actual_stock_history_fitting':stockfits,'raw_local_fitting':rawfits,'strong_feedback':{'waves':waves,'closure':sorted(known),'exclusion_duals':duals},'receiver_access':access,
             'price':t.report(t.interval(profile)),'increment_over_expanded':t.report(t.interval(delta)),'limiting_room':t.report(t.interval(room)),
             'semantic_negative_controls':rejected,'negative_controls_disable_all_milestones_source_cut_and_invoice':True,
             'scope':'Actual32/34 endpoints with realhigher-source acquisition andunchangedXpaths. ChangedP6/P7groundrows retained. No globalbankgrants,complete supplier ornewkappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');(a.out/'SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');print(json.dumps({k:receipt[k]for k in ['status','counts','profile','history_rank','history_W_intersection','history_C_intersection','ground_rank','proper_nonlocal_count','complete_normalized_rank','actual_stock_history_fitting','raw_local_fitting','price','limiting_room']}))
if __name__=='__main__':main()
