#!/usr/bin/env python3
"""Cache-specific funding refinement of the generic-union relaxation."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import importlib.util,json,sys
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def run():
    A=load('past_util',ROOT/'worker-a/past-constraint/subsets.py');P=load('block_pilot',HERE/'pilot.py');price=load('directed_price',ROOT/'budget_price.py');need=A.need
    rowsfile=ROOT/'worker-b/helper-graph/ROWS.json';R=json.loads(rowsfile.read_text());ranks={int(h):v for h,v in R['targets'].items()};rowmap={r['event']:r for r in R['records']};zeros=[A.decode(rowmap[e]['row']) for e in P.EVENTS];paid=[rowmap[e]['rank'] for e in P.EVENTS]
    main=json.loads((HERE/'RESULT.json').read_text());need(main['covered_zero_subsets']==16384,'full pilot census completed');spaces=json.loads((ROOT/'worker-a/past-constraint/SUBSETS.json').read_text());sites={s['event']:s for s in spaces['sites']};targets={r['event']:r for r in json.loads((ROOT/'independent-temporal-result.json').read_text())['records']}
    allZ={}
    for row,r in zip(zeros,paid):A.insert(allZ,row);need(all(ranks[h]>=r for h in row),'every zero support column dominates row credit')
    need(len(allZ)==14,'independent zero row determinant funding argument')
    certificates=[];minima={};required=(45659,45661,45663,58936)
    for event in P.CACHES:
        side=sites[event]['required_sides'][0];hist={int(p):A.decode(row) for p,row in side['history_basis'].items()};Le=[A.decode(row) for row in side['helper_extension_basis'].values()];minima[event]=min(ranks[h] for row in Le for h in row)
        qrows=[A.normal(row,hist) for row in zeros];target=A.normal(A.decode(targets[event]['target']),hist);basis={}
        for i,row in enumerate(qrows):
            val=row.copy();rep={i:Q(1)}
            for p in sorted(basis):
                if val.get(p):v,r=basis[p];q=-val[p];A.add(val,v,q);A.add(rep,r,q)
            if val:
                p=min(val);q=1/val[p];basis[p]=({j:q*v for j,v in val.items()},{j:q*v for j,v in rep.items()})
        val=target.copy();rep={}
        for p in sorted(basis):
            if val.get(p):v,r=basis[p];q=val[p];A.add(val,v,-q);A.add(rep,r,q)
        cert={'event':event,'minimum_L_support_target_rank':minima[event],'full_zero_quotient_rank':len(basis),'target_in_full_zero_quotient':not val,'full_zero_target_residual':A.encode(val)}
        if event==35152:need(val,'35152 is never already enabled by any zero subset')
        else:
            need(not val,'45656 full-zero quotient provider');need({P.EVENTS[i] for i,q in rep.items() if q}==set(required),'exact four-event provider support')
            cert['exact_zero_quotient_witness']={str(P.EVENTS[i]):str(q) for i,q in sorted(rep.items()) if q};cert['missing_required_event_nonmembership']=[]
            for missing in required:
                trial={}
                for i,row in enumerate(qrows):
                    if P.EVENTS[i]!=missing:A.insert(trial,row)
                residue=A.normal(target,trial);need(residue,'each required zero event is indispensable even with all other13');cert['missing_required_event_nonmembership'].append({'event':missing,'residual':A.encode(residue)})
        certificates.append(cert)
    need(minima=={35152:3,45656:4},'cache-specific support minima')
    mandatory_unit_events=(45659,45661,45663);units=[]
    for event in mandatory_unit_events:
        i=P.EVENTS.index(event);row=zeros[i];need(len(row)==1 and paid[i]==1,'mandatory paid rank1 unit');h=next(iter(row));need(row[h]==1 and ranks[h]==4,'mandatory unit target rank4');need(all(h not in other for j,other in enumerate(zeros) if j!=i),'mandatory unit coordinate disjoint from remaining zero rows');units.append(h)
    required_mask=sum(1<<P.EVENTS.index(e) for e in required)
    need(all((45656 in r['already_enabled_caches'])==((r['mask']&required_mask)==required_mask) for r in main['records']),'entire Boolean census matches four-event condition')
    need(all(35152 not in r['already_enabled_caches'] for r in main['records']),'all-subset 35152 miss')
    kappa=Q('0.0038');branch={'case0_no_cache':{},'case0_cache45656':{1:4,4:-3},'new_cache45656_grant_both':{1:1,2:1,4:-1},'new_cache35152_extra_over_case0':{2:1,3:-1}}
    priced={name:price.display(price.moment(hist,kappa)) for name,hist in branch.items()};need(all(Q(v['exact'][1])<0 for k,v in priced.items() if k!='case0_no_cache'),'strict refined branch signs');need(4**99>3**100,'uniform small-kappa integer comparison')
    out={'status':'NONPOSITIVE_GENERAL_CONSTRAINT_FUNDING_FOR_ASSIGNED_BLOCK','source_sha256':main['source_sha256'],'zero_events':list(P.EVENTS),'cache_events':list(P.CACHES),'zero_row_rank':14,'zero_support_minimum_target_rank':4,'cache_specific_L_support_minima':minima,'zero_row_credit_dominance_checked':True,'case0_cache45656_required_zero_events':list(required),'mandatory_disjoint_R4_unit_coordinates':units,'case0_cache35152_never_enabled':True,'certificates':certificates,'branch_signed_native_histograms':branch,'branch_upper_bounds_at_0038':priced,'overall_native_upper_bound':0,'uniform_power_price_kappa_interval':['0','1/100'],'constraint_dimension_unrestricted':True,'preparation_cleanup_and_ordinary_work_granted_free':True,'union_relaxation_positive_is_not_actual_gain':True,'full_census_sha256':sha256((HERE/'RESULT.json').read_bytes()).hexdigest(),'input_sha256':main['input_sha256'],'scope':'Assigned14-zero/2-cache block only, general helper-row constraint space with unchanged native histories. Global block decomposition/cost allocation is parent scope. No physical source or kappa.'}
    (HERE/'REFINED.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='certificates'},indent=2))
if __name__=='__main__':run()
