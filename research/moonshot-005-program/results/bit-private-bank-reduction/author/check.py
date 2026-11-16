#!/usr/bin/env python3
"""Bounded exact optimistic private-bank admission screen; no physical delivery claim."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    wr=a.word.read_bytes();w=json.loads(wr);assert hashlib.sha256(wr).hexdigest()=='d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71';source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots']
    path=Path(__file__).with_name('retained')/'source_history_engine.py';sp=importlib.util.spec_from_file_location('exact',path);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
    rank=lambda rows:len(e.basis(rows));rem=lambda B,v:reduce(B,v)
    local=[[1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0]for i in range(111)]
    run=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];C=run['C']
    common_visitors=[c['roles']for c in w['cache_metadata']if(c['family']==0 or(c['family']==1 and len(c['receivers'])==3))];assert list(map(len,common_visitors))==[20,10]
    BB=[r for name,r in v.items()if not name.startswith('Y')and at[name]=='zero']
    for chart in ['C0','M1']:BB +=[r for name,r in v.items()if not name.startswith('Y')and C[at[name]]==C[chart]]
    BB +=[1<<j for group in common_visitors for j in group];assert rank(BB)==47
    E=set(w['point_targets']);groups=[[j for j in f['group']if j not in E]for f in w['forks']]+[[j for j in w['h1_private_roles'][str(i)]if j not in E]for i in[4,74,78]]
    cases=[]
    for mask in range(64):
        gr=sorted(set(j for k,gg in enumerate(groups)if mask>>k&1 for j in gg));B=BB+[1<<j for j in gr];initial=[];known=set();waves=[]
        while True:
            total=B+[1<<j for j in sorted(known)];nxt={i for i in range(111)if rem(e.basis(total+local[i]),1<<i)==0};assert known<=nxt
            if not waves:initial=sorted(nxt)
            if nxt==known:break
            waves.append(sorted(nxt-known));known=nxt
        cases.append({'private_bank_mask':mask,'selected_banks':[k for k in range(6)if mask>>k&1],
                      'globally_granted_raw_roles':gr,'initial_fit_count':len(initial),'initial_fits':initial,
                      'feedback_closure_count':len(known),'feedback_closure':sorted(known),'feedback_waves':waves,
                      'global_bank_rank_before_feedback':rank(B)})
    maximum=max(c['feedback_closure_count']for c in cases);minimal=[c for c in cases if c['feedback_closure_count']==111 and all(cases[c['private_bank_mask']^(1<<j)]['feedback_closure_count']<111 for j in c['selected_banks'])]
    full=cases[-1];allrows=BB+[1<<j for gg in groups for j in gg]+[1<<j for j in full['feedback_closure']];duals=[]
    for i in range(111):
        if i in full['feedback_closure']:continue
        rows=allrows+local[i];equations=rows+[1<<i];cols=[sum(((r>>j)&1)<<k for k,r in enumerate(equations))for j in range(111)];v=e.solve(cols,1<<len(rows));assert v is not None and v>>i&1 and all(not((r&v).bit_count()%2)for r in rows);duals.append({'receiver':i,'annihilator_hex':hex(v)})
    K=[(1<<i)|sum(local[i])for i in range(111)];assert rank(K)==9
    assert all(e.solve(allrows+K+local[i],1<<i)is not None for i in range(111))
    leftover_groups=[5,7,9,11];filters=[[int(rec['row_hex'],16)for rec in w['history_cache_metadata']if rec['group']==g]for g in leftover_groups]
    for rec in w['history_cache_metadata']:
        if rec['group']in leftover_groups:assert run['cuts']['seed']['values'][rec['name']]==int(rec['row_hex'],16)and at[rec['name']]==rec['chart']
    completion_cases=[]
    for mask in range(16):
        extra=[row for k,group in enumerate(filters)if mask>>k&1 for row in group];M=allrows+extra
        fits=[i for i in range(111)if e.solve(M+local[i],1<<i)is not None]
        known=set(fits);rounds=[]
        while True:
            add={i for i in range(111)if i not in known and e.solve(M+[1<<j for j in sorted(known)]+local[i],1<<i)is not None}
            if not add:break
            rounds.append(sorted(add));known|=add
        completion_cases.append({'filter_bank_mask':mask,'groups':[leftover_groups[k]for k in range(4)if mask>>k&1],
                                 'additional_rank':rank(M)-rank(allrows),'fitting_count':len(fits),'fits':fits,
                                 'feedback_closure_count':len(known),'feedback_closure':sorted(known),'additional_feedback_waves':rounds,
                                 'canonical_missing_dimensions':rank(M+K)-rank(M)})
    full_witnesses=[]
    for i in full['feedback_closure']:
        rows=BB+[1<<j for gg in groups for j in gg]+local[i];co=e.solve(rows,1<<i);assert co is not None;full_witnesses.append({'receiver':i,'coefficient_hex':hex(co)})
    all_filter_rows=[row for group in filters for row in group];positive_rows=allrows+all_filter_rows
    positive=[]
    for i in range(111):
        co=e.solve(positive_rows+local[i],1<<i);assert co is not None;positive.append({'receiver':i,'coefficient_hex':hex(co)})
    canonical_witnesses=[hex(e.solve(positive_rows,row))for row in K]
    result={'status':'PASS_EXACT_SIX_PRIVATE_BANK_SUBSET_SCREEN','base_word_sha256':hashlib.sha256(wr).hexdigest(),'native_source_sha256':w['source_sha256'],
            'reconstructed_common_bank_rows_hex':[hex(r)for r in BB],'common_source_visitors':common_visitors,
            'private_groups':groups,'baseline_global_bank_rank':rank(BB),'case_count':64,'maximum_feedback_coverage':maximum,
            'inclusion_minimal_all111_masks':[c['private_bank_mask']for c in minimal],'all_six_bank_case':full,
            'all_six_bank_exclusion_duals':duals,'all_six_bank_fitting_witnesses':full_witnesses,'cases':cases,
            'positive_control_adding_C9_fits_all111':True,'remaining_filter_bank_completion_cases':completion_cases,
            'remaining_filter_groups':leftover_groups,'actual_remaining_filter_rows_hex':[[hex(row)for row in group]for group in filters],
            'all_four_banks_positive_all111_witnesses':positive,'all_four_banks_canonical_witnesses':canonical_witnesses,
            'scope':'Optimistically grants entire preceding C0/M1 source banks globally, then any subset of all six actual higher private-visitor banks globally, plus all geometric rawlocals and iterative free raw-output feedback. No field acquisition or movement is claimed. Fixed binary data tensor-lifts over characteristic two.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','private_groups','maximum_feedback_coverage','inclusion_minimal_all111_masks','all_six_bank_case','all_six_bank_exclusion_duals']}))
def reduce(B,v):
    for p in sorted(B,reverse=True):
        if v>>p&1:v^=B[p]
    return v
if __name__=='__main__':main()
