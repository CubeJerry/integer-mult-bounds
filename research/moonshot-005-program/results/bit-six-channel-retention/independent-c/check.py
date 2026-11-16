#!/usr/bin/env python3
"""Independent literal replay, complete custody ledger and feedback relaxation."""
import argparse, copy, hashlib, importlib.util, json
from pathlib import Path

PINS={21:'1253ce71d23750d912ca9b43837c9b0193c61ecebf967fe44287d2bdc195522d',
      27:'d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.word.read_bytes();w=json.loads(raw);n=len(w['targets']);assert hashlib.sha256(raw).hexdigest()==PINS[n]
    enginefile=Path(__file__).with_name('retained')/'source_history_engine.py'
    spec=importlib.util.spec_from_file_location('independent_replay',enginefile);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
    src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots']
    seeds=[int(v,16)for v in w['seed_rows_hex']];run=e.replay(w,roots,seeds,15,False)
    rank=lambda rows:len(e.basis(rows));dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    K=[(1<<i)|sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)]
    h=w['singular_h'];W=[K[i]&sum(1<<j for j in range(111)if h[j]==h[i])for i in range(111)]
    assert rank(K)==9 and rank(W)==15 and rank(K+W)==16
    obs=[int(t['row_hex'],16)for t in run['snapshots']];hr=rank(obs);assert rank(obs+K+W)==hr
    v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];C=run['C']
    early=sorted(w['early_completed_targets']);assert early==[16,22,23]
    ground_names=[name for name in v if at[name]=='zero'and not name.startswith('Y')]
    ground=[v[name]for name in ground_names]
    proper_names=[name for name in v if at[name]not in ['zero','Hub']and not name.startswith('Y')]
    nonlocal_names=[name for name in proper_names if any(v[name]>>j&1 and not e.contained(C[f'L{j}'],C[at[name]])for j in range(111))]
    assert all(name in nonlocal_names for name in ['Q1','Q3','Q4'])
    assert len(nonlocal_names)==(9 if n==21 else 15)
    for dd in w['multi_retention']:
        z,d,b=dd['packet'],dd['d'],dd['b']
        assert v[f'KEEP_C{z}']==int(dd['first_retention_hex'],16)and at[f'KEEP_C{z}']=='C0'
        assert v[f'KEEP_M{b}']==int(dd['h_hex'],16)and at[f'KEEP_M{b}']==f'L{d}'
        assert v[f'RAW{d}']==1<<d
    for dd in w.get('m1_retention',[]):
        z,d,b=dd['packet'],dd['d'],dd['b']
        assert v[f'ZFIRST{z}']==int(dd['first_retention_hex'],16)and at[f'ZFIRST{z}']=='M1'
        assert v[f'ZKEEP{b}']==int(dd['h_hex'],16)and at[f'ZKEEP{b}']==f'L{d}'
        assert v[f'ZRAW{d}']==1<<d
    normalized=ground+[v[name]for name in nonlocal_names]
    assert rank(normalized+[v[f'Y{i}']for i in range(111)])==rank(normalized)+111
    local=[[1<<j for j in range(111)if dot(i,j)==0]for i in range(111)]
    visible_stock=[];relaxed=[];access=[];actual_bases=[];relaxed_bases=[]
    for i in range(111):
        F=C[f'F{i}'];ns=[name for name in nonlocal_names if e.contained(C[at[name]],F)]
        stock=[v[name]for name in v if not name.startswith('Y')and e.contained(C[at[name]],F)]
        stock +=[row for row,t in zip(obs,run['snapshots'])if e.contained(C[t['chart']],F)]
        rbase=ground+[v[name]for name in ns]+local[i]
        actual_bases.append(stock);relaxed_bases.append(rbase)
        if e.solve(stock,1<<i)is not None:visible_stock.append(i)
        if e.solve(rbase,1<<i)is not None:relaxed.append(i)
        access.append({'receiver':i,'proper_nonlocal_fields':ns,'actual_stock_plus_history_rank':rank(stock),'raw_local_relaxation_rank':rank(rbase)})
    assert visible_stock==w['targets'] and relaxed==w['targets']
    def closure(bases):
        known=set();waves=[]
        while True:
            rows=[1<<j for j in sorted(known)]
            available={i for i in range(111)if e.solve(bases[i]+rows,1<<i)is not None}
            assert known<=available
            if available==known:return waves,sorted(known)
            waves.append(sorted(available-known));known=available
    actual_waves,actual_closed=closure(actual_bases);relaxed_waves,relaxed_closed=closure(relaxed_bases)
    closure_duals=[]
    granted=[1<<j for j in relaxed_closed]
    for i in range(111):
        if i in relaxed_closed:continue
        measurements=relaxed_bases[i]+granted
        equations=measurements+[1<<i]
        columns=[sum(((row>>j)&1)<<k for k,row in enumerate(equations))for j in range(111)]
        lam=e.solve(columns,1<<len(measurements));assert lam is not None
        assert lam>>i&1 and all((lam&row).bit_count()%2==0 for row in measurements)
        closure_duals.append({'receiver':i,'annihilator_hex':hex(lam)})
    # Every completed Y retains its independent original nuisance column. No
    # raw x_i is granted in the actual ledger; feedback grants are a separate
    # deliberately optimistic iteration, after the static source is frozen.
    tests=[('omit_early_nonlocal_read',lambda o:o==['ADD','P0','Y16']),
           ('omit_first_retention_capture',lambda o:o==['ADD','P0','KEEP_C0']),
           ('omit_first_reset',lambda o:o==['ADD','KEEP_C0','P0']),
           ('omit_low_line_capture',lambda o:o==['ADD','P0','KEEP_M16']),
           ('omit_low_line_reset',lambda o:o==['ADD','KEEP_M16','P0']),
           ('omit_shared_actual_source',lambda o:o==['ADD','X5','SHARED']),
           ('omit_paid_nonlocal_Q_descent',lambda o:o==['MOVE','Q1','M1']),
           ('omit_old_endpoint_replacement',lambda o:o==['ADD','KEEP_C0','Y3']),
           ('omit_retention_clear',lambda o:o==['CLEAR','KEEP_M16'])]
    if n==27:
        tests += [('omit_M1_first_reset',lambda o:o==['ADD','ZFIRST3','P3']),
                  ('omit_M1_line_capture',lambda o:o==['ADD','P3','ZKEEP2']),
                  ('omit_M1_line_reset',lambda o:o==['ADD','ZKEEP2','P3']),
                  ('omit_M1_cross_donor_preload',lambda o:o==['ADD','P4','Y2']),
                  ('omit_M1_nonlocal_read',lambda o:o==['ADD','ZKEEP2','Y2']),
                  ('omit_M1_local_correction',lambda o:o==['ADD','ZCORR2','Y2'])]
    rejected=[]
    for label,pred in tests:
        indices=[j for j,o in enumerate(w['operations'])if pred(o)];assert indices,label
        m=copy.deepcopy(w);m['operations'].pop(indices[0]);m['milestones']={k:-1 for k in w['milestones']};m.pop('source_cut',None)
        try:e.replay(m,roots,seeds,15,False)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('semantic mutant passed: '+label)
    # This control isolates the newly changed checkpoint contract, with the
    # identical physical word: it must reject false untouched-Y metadata.
    m=copy.deepcopy(w);m['early_completed_targets']=[]
    try:e.replay(m,roots,seeds,15,False)
    except AssertionError:rejected.append('false_untouched_Y_seedcut_claim')
    else:raise AssertionError('early-Y checkpoint forgery accepted')
    result={'status':'PASS_INDEPENDENT_MULTI_RETENTION_SOURCE','word_sha256':PINS[n],
            'native_source_sha256':w['source_sha256'],'engine_sha256':hashlib.sha256(enginefile.read_bytes()).hexdigest(),
            'columns':222,'targets':w['targets'],'early_completed_targets':early,
            'counts':run['count'],'profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],
            'actual_P_snapshot_count':len(obs),'actual_P_history_rank':hr,'actual_P_history_contains_W15_and_C9':True,
            'all111_W_witnesses':[hex(e.solve(obs,row))for row in W],
            'all111_C_witnesses':[hex(e.solve(obs,row))for row in K],
            'ground_rank':rank(ground),'full_nonlocal_normalized_rank':rank(normalized),
            'normalized_rank_with_all_Y_nuisance':rank(normalized)+111,
            'proper_nonlocal_inventory':[{'name':name,'chart':at[name],'row_hex':hex(v[name])}for name in nonlocal_names],
            'actual_stock_and_history_visible':visible_stock,'raw_local_relaxed_fitting':relaxed,
            'free_point_feedback_actual_stock':{'waves':actual_waves,'closure':actual_closed},
            'free_point_feedback_raw_local':{'waves':relaxed_waves,'closure':relaxed_closed},
            'raw_local_feedback_exclusion_duals':closure_duals,
            'receiver_access':access,'semantic_negative_controls':rejected,
            'negative_controls_disable_all_milestones_source_cut_and_invoice':True,
            'scope':'Literal finite source tensor-lifts over characteristic two. History and feedback are optimistic access analyses, not extra physical deliveries. All paid Q descents and Y nuisance columns retained. No new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','targets','counts','profile','actual_P_history_rank','ground_rank','full_nonlocal_normalized_rank','free_point_feedback_raw_local','semantic_negative_controls']}))
if __name__=='__main__':main()
