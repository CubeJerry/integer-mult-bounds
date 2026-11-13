#!/usr/bin/env python3
"""Joint72 cold helper inputs, past-only owned cache provider screen."""
from collections import Counter
from fractions import Fraction as Q
from functools import reduce
from math import gcd,lcm
from pathlib import Path
from hashlib import sha256
import gzip,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def run():
    start=time.monotonic();A=load('past_util',ROOT/'worker-a/past-constraint/subsets.py');need=A.need
    wp=ROOT/'reference/pr7481/WORD.json.gz';raw=wp.read_bytes();need(sha256(raw).hexdigest()==PIN,'actual word byte pin');w=json.loads(gzip.decompress(raw));classes=list(map(A.framekey,w['frames']))
    paths={'joint':ROOT/'worker-a/cold-compose/JOINT72-ZERO-CONTACTS.json','single':ROOT/'worker-b/cold-single/SCAN.json','projected':ROOT/'projected-temporal-result.json','targets':ROOT/'independent-temporal-result.json','history':ROOT/'worker-b/history-cache/FILTER.json','two':ROOT/'worker-b/two-cache/FILTER.json'}
    d={k:json.loads(p.read_text()) for k,p in paths.items()};need(all(v['source_sha256']==PIN for v in d.values()),'all exact receipt source pins')
    cold=set(d['joint']['cold_helpers']);single=[r for r in d['single']['records'] if r['removed_paid']=={str(r['target_rank']):1}]
    need(len(cold)==72 and cold=={r['helper'] for r in single},'exact72 neutral helper set')
    zero=d['joint']['neutral_helpers'][0];zero_events=zero['zero_moves'];zero_ids=[m['event'] if isinstance(m,dict) else m for m in zero_events]
    need(len(zero_ids)==len(set(zero_ids))==72,'exact joint72 zero MOVE positions')
    single_ids={m['event'] for r in single for m in r['pure_move_events']}
    need(len(single_ids)==72 and single_ids==set(zero_ids),'joint zero MOVEs are exactly singleton union, no extra multiple-helper zeros')
    lost=Counter({int(r):c for r,c in d['joint']['lost_targets'].items()});removed=Counter({int(r):c for r,c in d['joint']['removed_paid'].items()})
    need(lost==removed and sum(lost.values())==72,'joint full target/paid cancellation pointwise')
    actual_removed=Counter()
    for event in zero_ids:
        e=w['program'][event];need(e[0]=='MOVE','literal zero MOVE position');actual_removed[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
    actual_targets=Counter(abs(len(w['frames'][w['initial'][h]])-len(w['frames'][w['final'][h]])) for h in cold)
    need(actual_removed==removed==actual_targets,'actual source literal rank cancellation')
    ids=sorted(r['event'] for r in d['projected']['records'] if r['earlier_B_hit']);need(len(ids)==14,'exact14 past-main survivors')
    targets={r['event']:r for r in d['targets']['records']};two_ids={r['event'] for r in d['two']['records']}
    def project(row):return {j:v for j,v in row.items() if j not in cold}
    records=[];hits=[]
    for event in ids:
        need(time.monotonic()-start<60,'bounded exact projected history screen');r=targets[event]
        need(w['program'][event]==['MOVE',r['owner'],r['source'],r['destination'],True],'actual owned cache binding');need(event not in zero_ids,'cache target distinct from zero-MOVE credit')
        origin=d['two'] if event in two_ids else d['history'];field='earlier_generators' if event in two_ids else 'generators'
        gens=[g for g in origin[field] if classes[g['frame']]==classes[r['destination']] and g['event']<event];gens.sort(key=lambda g:g['event'])
        original={}
        for g in gens:A.insert(original,A.decode(g['row']))
        need(len(original)==r['earlier_B_rank'],'full original history provenance/rank')
        basis={};projected_rows=[project(A.decode(g['row'])) for g in gens]
        for i,row in enumerate(projected_rows):
            value=row.copy();rep={i:Q(1)}
            for p in sorted(basis):
                if value.get(p):old,orep=basis[p];q=-value[p];A.add(value,old,q);A.add(rep,orep,q)
            if value:
                p=min(value);q=1/value[p];basis[p]=({j:q*v for j,v in value.items()},{j:q*v for j,v in rep.items()})
        target=project(A.decode(r['target']));need(target,'cache target not zero after joint specialization');residual=target.copy();rep={}
        for p in sorted(basis):
            if residual.get(p):old,orep=basis[p];q=residual[p];A.add(residual,old,-q);A.add(rep,orep,q)
        hit=not residual;record={'event':event,'owner':r['owner'],'rank':r['rank'],'source':r['source'],'destination':r['destination'],'original_history_rank':len(original),'projected_history_rank':len(basis),'history_generator_count':len(gens),'target_nonzero':True,'target':A.encode(target),'hit':hit,'residual':A.encode(residual),'basis':{str(p):A.encode(row) for p,(row,rep) in sorted(basis.items())}}
        if hit:
            check={}
            for i,q in rep.items():A.add(check,projected_rows[i],q)
            need(check==target,'exact projected complete row provider equality')
            record['witness']=[{'coefficient':str(q),'generator_index':i,**{k:v for k,v in gens[i].items() if k!='row'}} for i,q in sorted(rep.items())]
            hits.append(record)
        else:
            p=min(residual);need(p not in basis,'nonpivot quotient coordinate');probe={p:Q(1)}
            for pivot in sorted(basis,reverse=True):
                v=-sum((q*probe.get(j,0) for j,q in basis[pivot][0].items() if j!=pivot),Q(0))
                if v:probe[pivot]=v
            den=lcm(*(v.denominator for v in probe.values()));probe={j:int(v*den) for j,v in probe.items()};common=reduce(gcd,(abs(v) for v in probe.values()));probe={j:v//common for j,v in probe.items()}
            def dot(row):return sum((v*probe.get(j,0) for j,v in row.items()),Q(0))
            need(not set(probe)&cold and dot(target) and all(not dot(row) for row in projected_rows),'exact retained-input dual annihilates every chronological provider generator')
            record['integer_retained_input_dual']={str(j):v for j,v in sorted(probe.items())};record['dual_target_value']=str(dot(target));record['all_projected_generators_annihilated']=True
        records.append(record)
    price=load('directed_budget',ROOT/'budget_price.py');iraw=price.INVOICE.read_bytes();need(sha256(iraw).hexdigest()==price.PIN,'full invoice pin');invoice=json.loads(iraw);canonical=sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest();need(canonical==invoice['new_native'],'actual native payload invoice binding')
    T=Counter({int(r):c for r,c in invoice['after']['T'].items()});P=Counter({int(r):c for r,c in invoice['after']['P'].items()});newT=T.copy();newP=P.copy();credits=Counter(r['rank'] for r in hits)
    for rank,count in lost.items():newT[rank]-=17*count
    for rank,count in removed.items():newP[rank]-=17*count
    for rank,count in credits.items():newP[rank]-=17*count
    need(all(c>=0 for c in newT.values()) and all(c>=0 for c in newP.values()),'nonnegative complete invoice')
    signed={str(r):newT[r]-newP[r] for r in newT.keys()|newP.keys()};moments=[]
    for k in [Q('0.00363005817'),Q('0.003647081039689'),Q('0.0038')]:moments.append({'kappa':str(k),'complete_complex_moment':price.display(price.moment(signed,k)),'extra_native_cache_gain':price.display(price.moment(dict(credits),k))})
    out={'status':'COMPLETE_JOINT72_PAST_ONLY_OWNED_CACHE_SCREEN','source_sha256':PIN,'source_payload_sha256':canonical,'input_sha256':{k:sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},'invoice_sha256':price.PIN,'cold_helpers':sorted(cold),'retained_arbitrary_inputs':w['public']-72,'target_debit_histogram':dict(sorted(lost.items())),'zero_MOVE_credit_histogram':dict(sorted(removed.items())),'zero_MOVE_events':zero_ids,'joint_zero_MOVE_events_equal_singleton_union':True,'joint_baseline_signed_histogram_unchanged':True,'owned_cuts_total':47,'past_main_excluded_cuts_not_retested':33,'cuts_tested':len(records),'cache_hits':len(hits),'cache_credit_histogram':dict(sorted(credits.items())),'records':records,'complete_T':dict(sorted(newT.items())),'complete_P':dict(sorted(newP.items())),'native_calls':17,'moments':moments,'future_A_requirement':False,'owned_nonzero_source_CLEAR_granted_free':True,'all_neutral_helper_subsets_covered_by_relation_space_inclusion':not hits,'seconds':time.monotonic()-start,'scope':'Joint72 helper inputs zero,1429others arbitrary. Strict original past-only history; exact zero-MOVE cancellations and cached replacements. No frame changes or added scalar history; physical public zero-reframe and complete supplier bridge remain separate.'}
    (HERE/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','cold_helpers','zero_MOVE_events','complete_T','complete_P','moments')},indent=2));print('hits',[(r['event'],r['rank'],r.get('witness')) for r in hits]);print(json.dumps(moments,indent=2))
if __name__=='__main__':run()
