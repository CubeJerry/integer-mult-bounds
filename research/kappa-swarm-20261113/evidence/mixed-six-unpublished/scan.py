#!/usr/bin/env python3
"""Independent exact-Q pilot of two six-zero-row mixed cache relaxations."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from hashlib import sha256
import argparse,gzip,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
ROWPIN='15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834'
ASSIGNED=[([42487],[31351,35683,43283,43285,46810,47178]),([35448,35452],[34154,34156,46841,47000,48515,49195])]
def need(ok,label):
    if not ok:raise ValueError(label)
def add(a,b,q):
    for h,v in b.items():
        z=a.get(h,0)+q*v
        if z:a[h]=z
        else:a.pop(h,None)
def normal(row,basis):
    v=row.copy()
    for p in sorted(basis,reverse=True):
        if v.get(p):add(v,basis[p],-v[p])
    return v
def insert(basis,row):
    v=normal(row,basis)
    if v:
        p=max(v);basis[p]={h:a/v[p] for h,a in v.items()}
def echelon(rows):
    b={}
    for row in rows:insert(b,row)
    return b
def decode(row):return {int(h):Q(a) for h,a in row.items()}
def encode(row):return {str(h):str(a) for h,a in sorted(row.items())}
def space(f):
    s={0}
    for v in f:s|={x^v for x in s}
    return frozenset(s)
def helper_extension(P,target,mains,helpers):
    need(normal(target,P),'target is not in old history')
    image={};L={}
    for row in list(P.values())+[target]:
        full=row.copy();v={h:a for h,a in row.items() if h in mains}
        for p in sorted(image,reverse=True):
            if v.get(p):q=v[p];add(v,image[p][0],-q);add(full,image[p][1],-q)
        if v:
            p=max(v);q=1/v[p];image[p]=({h:a*q for h,a in v.items()},{h:a*q for h,a in full.items()})
        else:
            need(set(full)<=helpers,'kernel is helper-only');insert(L,full)
    need(len(L)+len(image)==len(P)+1,'helper extension rank-nullity')
    return L
def run(output,seconds):
    start=time.monotonic();deadline=start+seconds;pins={}
    need(normal({9:Q(1),4:Q(3)},{4:{4:Q(1),2:Q(2)}})=={9:Q(1),2:Q(-6)},'all-pivot quotient control')
    toy=helper_extension(echelon([{0:Q(1),1:Q(1)}]),{0:Q(1),2:Q(1)},{0},{1,2})
    need(len(toy)==1 and not normal({1:Q(1),2:Q(-1)},toy),'helper-intersection control')
    z={1:Q(1),2:Q(1)};u={1:Q(1),2:Q(2)}
    need(len(echelon([z,u]))==2 and len(echelon([z,z]))==1,'generic versus row-inside-Z control')
    def load(path,zipped=False):
        raw=(ROOT/path).read_bytes();pins[str(path)]=sha256(raw).hexdigest();x=json.loads(gzip.decompress(raw) if zipped else raw)
        if isinstance(x,dict) and 'source_sha256' in x:need(x['source_sha256']==PIN,'source binding')
        return x
    w=load('reference/pr7481/WORD.json.gz',True);need(pins['reference/pr7481/WORD.json.gz']==PIN,'word pin')
    rd=load('worker-b/helper-graph/ROWS.json');need(pins['worker-b/helper-graph/ROWS.json']==ROWPIN,'zero-row pin')
    history=load('worker-b/history-cache/FILTER.json');two=load('worker-b/two-cache/FILTER.json')
    actual={r['event']:r for r in load('independent-temporal-result.json')['records']}
    arrangement=load('cache-zero-arrangement-exploration.json')
    classes=[space(f) for f in w['frames']];mains=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    helpers=set(range(w['public']))-mains;T={h:len(w['frames'][w['final'][h]])-len(w['frames'][w['initial'][h]]) for h in helpers}
    zeros={r['event']:r for r in rd['records']};target_rows={e:decode(r['target']) for e,r in actual.items()}
    need(len(mains)==400 and len(helpers)==1101 and all(1<=r<=9 for r in T.values()),'actual helper target domain')
    cache={};site_evidence=[]
    source_fail={r['event'] for r in two['records']}
    for e in [42487,35448,35452]:
        r=actual[e];need(w['program'][e]==['MOVE',r['owner'],r['source'],r['destination'],True],'actual cache literal')
        need(set(target_rows[e])&mains,'nonzero target main projection')
        gens=two['earlier_generators'] if e in source_fail else history['generators']
        ids=[j for j,g in enumerate(gens) if g['event']<e and classes[g['frame']]==classes[r['destination']]]
        P=echelon(decode(gens[j]['row']) for j in ids);need(len(P)==r['earlier_B_rank'],'strict raw history rank')
        L=helper_extension(P,target_rows[e],mains,helpers)
        extended=echelon(list(P.values())+[target_rows[e]])
        need(all(not normal(row,extended) for row in L.values()),'independent helper-extension inclusion')
        cache[e]=dict(P=P,L=L,residual=normal(target_rows[e],P),rank=r['rank'])
        site_evidence.append(dict(event=e,literal=w['program'][e],history_generator_indices=ids,
            history_origin='two.earlier_generators' if e in source_fail else 'history.generators',
            history_rank=len(P),L_dimension=len(L),L_basis=[encode(row) for row in L.values()]))
    need([cache[e]['rank'] for e in [42487,35448,35452]]==[4,2,1],'actual cache ranks')
    caller=load('reference/pr7481/CALLER-EXACT.json');need(pins['reference/pr7481/CALLER-EXACT.json']=='255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc','exact caller bytes')
    calls=sum(e[0]=='J' for e in caller['events']);need(calls==caller['stages']==17,'actual17calls')
    pp=ROOT/'budget_price.py';pins['budget_price.py']=sha256(pp.read_bytes()).hexdigest();need(pins['budget_price.py']=='527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb','price code pin')
    spec=importlib.util.spec_from_file_location('mixed_price',pp);price=importlib.util.module_from_spec(spec);sys.modules[spec.name]=price;spec.loader.exec_module(price)
    ip=str(price.INVOICE.relative_to(ROOT));invoice=load(ip);need(pins[ip]==price.PIN,'invoice pin')
    need(sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest()==invoice['new_native'],'invoice actual native payload')
    ta={int(r):n for r,n in invoice['after']['T'].items()};pa={int(r):n for r,n in invoice['after']['P'].items()}
    base={r:ta.get(r,0)-pa.get(r,0) for r in ta.keys()|pa.keys()};kappa=Q(19,5000)
    draft=ROOT/'repo/research/kappa-swarm-20261113/evidence/mixed-cache-budget/RELAXATION-DRAFT.md';pins[str(draft.relative_to(ROOT))]=sha256(draft.read_bytes()).hexdigest()
    def profile(prefix):
        need(prefix[0]==0 and all(prefix[k]>=prefix[k-1] for k in range(1,10)),'monotone exact prefix ranks')
        return {k:prefix[k]-prefix[k-1] for k in range(1,10) if prefix[k]!=prefix[k-1]}
    def budget(benefit,debit):
        delta=Counter(benefit);delta.subtract(debit);delta={r:z for r,z in delta.items() if z}
        native=price.moment(delta,kappa);full=price.moment({r:base.get(r,0)+calls*delta.get(r,0) for r in base.keys()|delta.keys()},kappa)
        return dict(native_profile=delta,native=price.display(native),full_signed17=price.display(full),positive_native=native[0]>0,positive_full=full[0]>0)
    results=[];complete=True;total_subsets=0
    for events,zevents in ASSIGNED:
        chosen=next(c for c in arrangement['components_with_cache_spaces'] if sorted(int(s.split(':')[1]) for s in c['cache_sites'])==events)
        need(chosen['zero_events']==zevents and len(set(zevents))==6,'assigned exact component')
        Zrows=[]
        for e in zevents:
            r=zeros[e];ins=w['program'][e];need(ins[0]=='MOVE' and ins[1]==r['owner'] and abs(len(w['frames'][ins[2]])-len(w['frames'][ins[3]]))==r['rank'],'actual zero MOVE literal')
            row=decode(r['row']);need(row and set(row)<=helpers and e not in events,'helper-only disjoint zero event');Zrows.append(row)
        L=echelon(row for e in events for row in cache[e]['L'].values())
        Lpre=[];Zpre=[];Rpre=[]
        for k in range(10):
            b=echelon({h:a for h,a in row.items() if T[h]<=k} for row in L.values());Lpre.append(b)
            zp=[{h:a for h,a in row.items() if T[h]<=k} for row in Zrows];Zpre.append(zp);Rpre.append([normal(row,b) for row in zp])
        cache_res={e:[normal(row,cache[e]['P']) for row in Zrows] for e in events}
        cases=[];subset_records=[]
        for mask in range(64):
            if time.monotonic()>deadline:complete=False;break
            selected=[i for i in range(6) if mask>>i&1];bp=[];up=[]
            for k in range(10):
                bp.append(len(echelon(Zpre[k][i] for i in selected)))
                up.append(len(Lpre[k])+len(echelon(Rpre[k][i] for i in selected)))
                if mask in (0,63):
                    direct=len(echelon(list(Lpre[k].values())+[Zpre[k][i] for i in selected]))
                    need(direct==up[k],'quotient union-rank sanity check')
            beta=profile(bp);enabled=[]
            for e in events:
                mod=echelon(cache_res[e][i] for i in selected)
                if not normal(cache[e]['residual'],mod):enabled.append(e)
            zero_benefit=Counter(zeros[zevents[i]]['rank'] for i in selected)
            benefit=zero_benefit.copy();benefit.update(cache[e]['rank'] for e in enabled)
            c0=dict(mask=mask,case=0,zero_events=[zevents[i] for i in selected],already_enabled=enabled,
                zero_prefix_ranks=bp,debit_profile=beta,**budget(benefit,beta));cases.append(c0)
            record=dict(mask=mask,zero_events=c0['zero_events'],rank_Z=bp[9],already_enabled=enabled,
                zero_prefix_ranks=bp,union_prefix_ranks=up,case0=c0)
            if len(enabled)<len(events) and up[9]>bp[9]:
                gp=[min(bp[k]+1,up[k]) for k in range(10)];gamma=profile(gp)
                need(gp[9]==bp[9]+1,'one generic independent row')
                need(sum(r*n for r,n in gamma.items())>=sum(r*n for r,n in beta.items())+1,'augmented minimum linear debit')
                benefit=zero_benefit.copy();benefit.update(cache[e]['rank'] for e in events)
                c1=dict(mask=mask,case=1,zero_events=c0['zero_events'],already_enabled=enabled,
                    granted_caches=events,generic_prefix_ranks=gp,debit_profile=gamma,
                    witness='Generic rank/debit witness only; all cache benefits granted without a common actual enabling direction.',
                    **budget(benefit,gamma));cases.append(c1);record['case1']=c1
            subset_records.append(record);total_subsets+=1
        best=max(cases,key=lambda c:Q(c['native']['exact'][1]))
        local=dict(cache_events=events,zero_events=zevents,L_union_dimension=len(L),subsets_covered=len(subset_records),expected_subsets=64,
            cases_evaluated=len(cases),max_native_interval=price.display((max(Q(c['native']['exact'][0]) for c in cases),max(Q(c['native']['exact'][1]) for c in cases))),
            best_upper_case=best,positive_native_cases=[dict(mask=c['mask'],case=c['case']) for c in cases if c['positive_native']],
            positive_full_cases=[dict(mask=c['mask'],case=c['case']) for c in cases if c['positive_full']],subsets=subset_records)
        results.append(local)
        if not complete:break
    out=dict(status='COMPLETE_TWO_SIX_ZERO_COMPONENT_RELAXATIONS' if complete else 'BOUNDED_PARTIAL_RELAXATION',source_sha256=PIN,
        input_sha256=pins,kappa=str(kappa),native_calls=calls,baseline=price.display(price.moment(base,kappa)),
        covered_subsets=total_subsets,expected_subsets=128,site_evidence=site_evidence,components=results,seconds=time.monotonic()-start,
        controls=dict(all_pivot_quotient=True,exact_kernel_rank_nullity=True,exact_source_literals=True,union_rank_formula_checked=True,synthetic_helper_intersection=True,generic_outside_Z=True),
        scope='Locally exact-Q relaxation arithmetic: generic one-row lower target debit and possibly unrealizable grant of all caches. Fixed scalar-linear helper-domain model only. Global proof/source partition pending C40 review. Positive relaxation is not a construction or kappa.')
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['input_sha256','site_evidence','components']},indent=2))
    for r in results:print(json.dumps({k:v for k,v in r.items() if k not in ['subsets','positive_native_cases','positive_full_cases']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--seconds',type=float,default=60);a=p.parse_args();run(a.output,a.seconds)
