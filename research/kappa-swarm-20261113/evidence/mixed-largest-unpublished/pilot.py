#!/usr/bin/env python3
"""Optimistic general-constraint funding gate for the assigned14-zero block."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import argparse,gzip,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
EVENTS=(32681,39855,39857,39859,45659,45661,45663,45698,45701,45706,51637,57989,58936,76469)
CACHES=(35152,45656)
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def run(limit):
    start=time.monotonic();A=load('past_util',ROOT/'worker-a/past-constraint/subsets.py');need=A.need
    raw=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(raw).hexdigest()==PIN,'native source pin');w=json.loads(gzip.decompress(raw))
    paths={'zero_rows':ROOT/'worker-b/helper-graph/ROWS.json','L_spaces':ROOT/'worker-a/past-constraint/SUBSETS.json','targets':ROOT/'independent-temporal-result.json','arrangement':ROOT/'cache-zero-arrangement-exploration.json'}
    data={k:json.loads(p.read_text()) for k,p in paths.items()};need(all(data[k]['source_sha256']==PIN for k in ('zero_rows','L_spaces','targets')),'actual source pins')
    block=next(r for r in data['arrangement']['components_with_cache_spaces'] if r['cache_sites']==['cache:35152','cache:45656']);need(tuple(block['zero_events'])==EVENTS,'assigned mixed block')
    rowmap={r['event']:r for r in data['zero_rows']['records']};zeros=[A.decode(rowmap[e]['row']) for e in EVENTS];paid=[rowmap[e]['rank'] for e in EVENTS]
    ranks={int(h):r for h,r in data['zero_rows']['targets'].items()}
    need(all(r==abs(len(w['frames'][w['initial'][h]])-len(w['frames'][w['final'][h]])) for h,r in ranks.items()),'all1101 actual helper price weights')
    allZ={}
    for event,row,r in zip(EVENTS,zeros,paid):
        need(w['program'][event][0]=='MOVE' and r==abs(len(w['frames'][w['program'][event][2]])-len(w['frames'][w['program'][event][3]])),'actual zero candidate paid rank');need(all(ranks[h]>=r for h in row),'each zero row support rank dominates paid rank');A.insert(allZ,row)
    need(len(allZ)==14,'all14 zero rows independent')
    sites={s['event']:s for s in data['L_spaces']['sites']};targets={r['event']:r for r in data['targets']['records']};L={};cachedata={};cache_ranks={}
    for event in CACHES:
        side=sites[event]['required_sides'][0];need(side['side']=='past','past-only L space');P={int(p):A.decode(r) for p,r in side['history_basis'].items()};Le={int(p):A.decode(r) for p,r in side['helper_extension_basis'].items()}
        for row in Le.values():A.insert(L,row)
        x=A.decode(targets[event]['target']);need(A.normal(x,P),'original cache not funded');cache_ranks[event]=targets[event]['rank']
        cachedata[event]={'target':A.normal(x,P),'zero_residues':[A.normal(row,P) for row in zeros],'P_rank':len(P),'L_dim':len(Le)}
    support=set().union(*(set(row) for row in L.values()));Zsupport=set().union(*(set(row) for row in zeros));need(min(ranks[h] for h in support)==3 and min(ranks[h] for h in Zsupport)==4,'cheap generic row strictly below zero support')
    # Every prefix uses exact projections; L-normal residues precomputed as requested.
    families=[]
    for k in range(1,10):
        zk=[{h:v for h,v in row.items() if ranks[h]<=k} for row in zeros];Lk={}
        for row in L.values():A.insert(Lk,{h:v for h,v in row.items() if ranks[h]<=k})
        families.append((zk,Lk,[A.normal(row,Lk) for row in zk]))
    price=load('directed_price',ROOT/'budget_price.py');kappa=Q('0.0038');price_cache={}
    def value(hist):
        key=tuple(sorted((int(r),c) for r,c in hist.items() if c))
        if key not in price_cache:price_cache[key]=price.moment(dict(key),kappa)
        return price_cache[key]
    def bhist(prefix):
        out=Counter();previous=0
        for k,r in enumerate(prefix,1):need(r>=previous,'nondecreasing column prefix rank');out[k]=r-previous;previous=r
        return Counter({k:c for k,c in out.items() if c})
    records=[];best0=None;best1=None;enabled_counts=Counter();beta_patterns=Counter()
    for mask in range(min(limit,1<<14)):
        if time.monotonic()-start>60:break
        selected=[j for j in range(14) if mask>>j&1];credit=Counter(paid[j] for j in selected);rho=len(selected);prefix=[];generic=[]
        for zk,Lk,qk in families:
            basis={};quotient={}
            for j in selected:A.insert(basis,zk[j]);A.insert(quotient,qk[j])
            prefix.append(len(basis));generic.append(min(len(basis)+1,len(Lk)+len(quotient)))
        need(prefix[-1]==rho and generic[-1]==rho+1,'full generic dimension');beta=bhist(prefix);betag=bhist(generic);difference=betag.copy();difference.subtract(beta);need({k:c for k,c in difference.items() if c}=={3:1},'generic extension costs exactly one rank3 target')
        enabled=[]
        for event in CACHES:
            basis={}
            for j in selected:A.insert(basis,cachedata[event]['zero_residues'][j])
            if not A.normal(cachedata[event]['target'],basis):enabled.append(event)
        delta0=credit.copy();delta0.update(cache_ranks[e] for e in enabled);delta0.subtract(beta)
        delta1=credit.copy();delta1.update(cache_ranks.values());delta1.subtract(betag)
        v0=value(delta0);v1=value(delta1);row={'mask':mask,'zero_events':[EVENTS[j] for j in selected],'rho':rho,'column_prefix_ranks':prefix,'generic_prefix_ranks':generic,'beta_histogram':dict(beta),'generic_beta_histogram':dict(betag),'already_enabled_caches':enabled,'case0_signed_native_histogram':{k:c for k,c in delta0.items() if c},'case1_signed_native_histogram':{k:c for k,c in delta1.items() if c},'case0_upper':price.display(v0),'case1_upper':price.display(v1)};records.append(row)
        if best0 is None or v0[1]>Q(best0['case0_upper']['exact'][1]):best0=row
        if best1 is None or v1[1]>Q(best1['case1_upper']['exact'][1]):best1=row
        enabled_counts[tuple(enabled)]+=1;beta_patterns[tuple(sorted(beta.items()))]+=1
    out={'status':'COMPLETE_14_ZERO_BLOCK_RELAXATION' if len(records)==16384 else 'BOUNDED_PILOT_14_ZERO_BLOCK_RELAXATION','source_sha256':PIN,'input_sha256':{k:sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},'requested_limit':limit,'covered_zero_subsets':len(records),'total_zero_subsets':16384,'zero_events':list(EVENTS),'cache_events':list(CACHES),'cache_ranks':cache_ranks,'L_union_dimension':len(L),'all_zero_rank':len(allZ),'all_helper_weights_verified':len(ranks),'cache_quotient_dimensions':{e:{'P_rank':v['P_rank'],'L_dim':v['L_dim']} for e,v in cachedata.items()},'minimum_L_support_target_rank':3,'minimum_zero_support_target_rank':4,'generic_beta_equals_betaZ_plus_rank3_for_all_masks_checked':True,'each_independent_zero_row_credit_dominated_by_every_support_column_price':True,'kappa':str(kappa),'case0_best':best0,'case1_best':best1,'already_enabled_patterns':{str(k):v for k,v in enabled_counts.items()},'price_histograms_evaluated':len(price_cache),'records':records,'seconds':time.monotonic()-start,'scope':'Optimistic generic-one-extra-row lower funding cost while granting both cache credits. Case1 need not have a direction enabling both caches. No physical candidate, complete source or kappa.'}
    name='PILOT.json' if limit<=256 else 'RESULT.json';(HERE/name).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('records','case0_best','case1_best')},indent=2));print(json.dumps({'case0_best':best0,'case1_best':best1},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=256);run(ap.parse_args().limit)
