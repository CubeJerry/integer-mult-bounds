#!/usr/bin/env python3
"""Exact entrance-preparation obstruction for the h770/event41646 cache.

No deferred use of paid original-prefix work is credited by this test.
"""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
from collections import Counter, defaultdict
import gzip, importlib.util, json, sys, time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);out=importlib.util.module_from_spec(spec)
    sys.modules[name]=out;spec.loader.exec_module(out);return out
def run():
    started=time.monotonic();A=load('past_gate',ROOT/'worker-a/past-constraint/subsets.py');need=A.need
    wp=ROOT/'reference/pr7481/WORD.json.gz';raw=wp.read_bytes();need(sha256(raw).hexdigest()==PIN,'native byte pin')
    w=json.loads(gzip.decompress(raw));classes=list(map(A.framekey,w['frames']))
    pp=ROOT/'worker-a/past-constraint/SUBSETS.json';res=json.loads(pp.read_text());need(res['source_sha256']==PIN,'past gate source')
    rec=next(r for r in res['subsets'] if r['events']==[41646]);u=next(A.decode(row) for row in rec['basis'].values() if '770' in row)
    need(rec['dimension']==2 and u[770]==Q(-17,32),'exact demotion family')
    hp=ROOT/'worker-b/two-cache/FILTER.json';history=json.loads(hp.read_text());need(history['source_sha256']==PIN,'history source pin')
    cut=next(r for r in history['records'] if r['event']==41646);need(w['program'][41646]==['MOVE',1530,593,549,True],'actual cache cut')
    target=A.decode(cut['target_row']);gens=[g for g in history['earlier_generators'] if g['event']<41646 and classes[g['frame']]==classes[549]];gens.sort(key=lambda g:g['event'])
    basis={}
    for i,row in enumerate([A.decode(g['row']) for g in gens]+[u]):
        value=row.copy();rep={i:Q(1)}
        for p in sorted(basis):
            if value.get(p):
                v,rv=basis[p];q=-value[p];A.add(value,v,q);A.add(rep,rv,q)
        need(value,'independent strict history plus relation');p=min(value);q=1/value[p]
        basis[p]=({j:q*v for j,v in value.items()},{j:q*v for j,v in rep.items()})
    value=target.copy();rep={}
    for p in sorted(basis):
        if value.get(p):
            v,rv=basis[p];q=value[p];A.add(value,v,-q);A.add(rep,rv,q)
    need(not value and rep.get(len(gens))==8,'exact relation-enabled provider')
    check={}
    for i,q in rep.items():A.add(check,u if i==len(gens) else A.decode(gens[i]['row']),q)
    need(check==target,'full-row provider equality')
    def frames(h):return {'initial':w['initial'][h],'initial_basis':w['frames'][w['initial'][h]],'final':w['final'][h],'final_basis':w['frames'][w['final'][h]]}
    donors=[{'helper':h,'relation_coefficient':str(q),'preparation_coefficient':str(-q/u[770]),**frames(h)} for h,q in sorted(u.items()) if h!=770]
    groups=defaultdict(list)
    for d in donors:groups[d['initial']].append(d['helper'])
    need(len(u)==137 and len(groups[3])==135 and groups[593]==[1426] and len(groups)==2,'mandatory entrance groups')
    need(w['initial'][770]==115 and len(w['frames'][115])==5,'h770 required entrance')
    need(u[126] and w['initial'][126]==3 and w['frames'][3]==[],'mandatory independent empty-frame witness')
    touches=[{'event':i,'instruction':e} for i,e in enumerate(w['program']) if e[1]==770 or (e[0] in ('ADD','COPY') and e[2]==770)]
    need(touches[0]=={'event':33814,'instruction':['COPY',1525,770,'1',115]},'first original h770 use')
    witness=[{'coefficient':str(q),'history_index':i,**{k:v for k,v in gens[i].items() if k!='row'}} for i,q in sorted(rep.items()) if i<len(gens)]
    stage={'status':'EXPLICIT_RELATION_CACHE_WITNESS_AND_DONOR_FRAME_STAGE','source_sha256':PIN,'event':41646,'literal':w['program'][41646],'h':770,'h_frames':frames(770),'relation_basis_dim':2,'relation':A.encode(u),'relation_support':len(u),'optional_other_basis':{'937':'1'},'preparation_donors':donors,'donor_initial_groups':[{'frame':f,'basis':w['frames'][f],'dimension':len(w['frames'][f]),'count':len(hs),'helpers':hs} for f,hs in sorted(groups.items())],'earlier_cache_witness':witness,'relation_coefficient_in_target':'8','cache_witness_exact':True,'strict_clock_max':max(gens[i]['event'] for i in rep if i<len(gens)),'h_native_touches':touches,'all_donor_histories_unchanged_before_deleted_cut':True,'scope':'Entrance preparation only; no credit for original paid prefix. Final private erasure provisionally free. No source or kappa.'}
    (HERE/'STAGE1.json').write_text(json.dumps(stage,indent=2)+'\n')
    cp=ROOT/'worker-a/selected/frozen/clifford_exact.py';C=load('retained_clifford',cp)
    charts={f:C.canonical_frame(9,tuple(w['frames'][f])) for f in (3,593,115)};routes=[]
    for old,new,expected in [(3,593,1),(593,115,4),(3,115,5)]:
        op=charts[old].adjoint().then(charts[new]);record,compiled=C.lower_child(op)
        need(record['rank']==expected and compiled.tab==op.tab and compiled.zero_state()==op.zero_state(),'actual retained rank and absolute-phase factorization')
        routes.append({'source':old,'destination':new,'rank':expected,'record':record,'absolute_phase_checked':True})
    price=load('directed_price',ROOT/'budget_price.py');iraw=price.INVOICE.read_bytes();need(sha256(iraw).hexdigest()==price.PIN,'complete invoice pin');invoice=json.loads(iraw)
    canonical=sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest();need(canonical==invoice['new_native'],'invoice actual native payload')
    t,p=invoice['after']['T'],invoice['after']['P'];signed=Counter({r:t.get(r,0)-p.get(r,0) for r in t.keys()|p.keys()})
    points=[]
    for kappa in [Q('0.00363005817'),Q('0.003647081039689'),Q('0.0038')]:
        delta=Counter({'6':1,'4':-1,'5':-1});trial=signed.copy()
        for rank,count in delta.items():trial[rank]+=17*count
        gain=price.moment(delta,kappa);full=price.moment(trial,kappa)
        need(gain[1]<0 and full[1]<0,'even lower-bound preparation fails selected and comparator complete budgets')
        points.append({'kappa':str(kappa),'native_gain_before_preparation':price.display(price.moment({'6':1,'4':-1},kappa)),'preparation_lower_bound':price.display(price.price(5,kappa)),'preparation_upper_bound_recursive_only':price.display(price.moment({'1':1,'4':1},kappa)),'optimistic_net_native_gain':price.display(gain),'baseline_complete_moment':price.display(price.moment(signed,kappa)),'optimistic_complete_moment':price.display(full)})
    result={'status':'NEGATIVE_ENTRANCE_PREPARATION_LOWER_BOUND','source_sha256':PIN,'source_payload_sha256':canonical,'input_sha256':{'past_gate':sha256(pp.read_bytes()).hexdigest(),'history':sha256(hp.read_bytes()).hexdigest(),'clifford_code':sha256(cp.read_bytes()).hexdigest(),'budget_code':sha256((ROOT/'budget_price.py').read_bytes()).hexdigest()},'invoice_sha256':price.PIN,'event':41646,'demoted_helper':770,'mandatory_dependency_witness':{'donor':126,'coefficient_in_h770':str(-u[126]/u[770]),'source_frame':3,'source_dimension':0,'required_frame':115,'required_dimension':5},'all_relation_family_members_require_this_dependency':True,'recursive_preparation_lower_bound_rank':5,'explicit_recursive_upper_bound_ranks':[1,4],'actual_clifford_routes':routes,'price_points':points,'ordinary_phase_cache_and_cleanup_costs_granted_free':True,'owned_final_private_erasure_provisionally_free':True,'no_original_prefix_credit':True,'no_deferred_initialization_claim':True,'seconds':time.monotonic()-started,'scope':'Whole-field scalar-contact/MOVE entrance preparation, independent donors, fixed required entrance frame. Deferred preparation using original paid prefix is outside this obstruction. No physical supplier or kappa.'}
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('actual_clifford_routes','price_points')},indent=2))
    print(json.dumps([{'kappa':r['kappa'],'net_native':r['optimistic_net_native_gain']['decimal_display_only'],'full_moment':r['optimistic_complete_moment']['decimal_display_only']} for r in points],indent=2))
if __name__=='__main__':run()
