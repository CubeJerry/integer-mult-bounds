#!/usr/bin/env python3
"""One credited helper constraint and multiple generous cache providers."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,gzip,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
ROWPIN='15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834'
SITES=[30581,30593,35152,35448,35452,36346,36358,39875,39884,41646,42487,42500,44253,45656]
def need(ok,label):
    if not ok:raise ValueError(label)
def add(dst,src,q):
    for h,v in src.items():
        z=dst.get(h,0)+q*v
        if z:dst[h]=z
        else:dst.pop(h,None)
def residual(row,basis):
    v=row.copy()
    for p in sorted(basis,reverse=True):
        if v.get(p):add(v,basis[p],-v[p])
    return v
def insert(basis,row):
    v=residual(row,basis)
    if not v:return
    p=max(v);basis[p]={h:x/v[p] for h,x in v.items()}
def canon(row):return tuple((h,v/row[min(row)]) for h,v in sorted(row.items())) if row else ()
def decode(row):return {int(h):Q(v) for h,v in row.items()}
def space(frame):
    s={0}
    for v in frame:s|={x^v for x in s}
    return frozenset(s)
def enabled(query,u):
    basis,v,key=query;r=residual(u,basis)
    if canon(r)!=key:return None
    p=min(v);return v[p]/r[p]
def run(output,seconds):
    start=time.monotonic();deadline=start+seconds;pins={}
    need(residual({4:Q(1),3:Q(3)},{3:{3:Q(1),1:Q(2)}})=={4:Q(1),1:Q(-6)},'all pivot control')
    need(canon({1:Q(2),2:Q(-4)})==canon({1:Q(-1),2:Q(2)}),'proportional direction control')
    b={0:{0:Q(1)}};t={0:Q(1),1:Q(1)};v=residual(t,b);q=(b,v,canon(v))
    need(enabled(q,{1:Q(1)})==1,'constraint really enables provider')
    need(enabled(q,{2:Q(1)}) is None,'wrong helper direction rejected')
    need(enabled(q,{0:Q(1)}) is None,'direction already inside provider span rejected')
    def load(path,zipped=False):
        raw=(ROOT/path).read_bytes();pins[str(path)]=sha256(raw).hexdigest()
        x=json.loads(gzip.decompress(raw) if zipped else raw)
        if isinstance(x,dict) and 'source_sha256' in x:need(x['source_sha256']==PIN,'source binding')
        return x
    w=load('reference/pr7481/WORD.json.gz',True);need(pins['reference/pr7481/WORD.json.gz']==PIN,'word pin')
    rd=load('worker-b/helper-graph/ROWS.json');need(pins['worker-b/helper-graph/ROWS.json']==ROWPIN,'468 row snapshot')
    need(len(rd['records'])==len({e['event'] for e in rd['records']})==468,'no duplicated MOVE benefit')
    caller=load('reference/pr7481/CALLER-EXACT.json')
    need(pins['reference/pr7481/CALLER-EXACT.json']=='255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc','exact Git caller bytes')
    calls=sum(e[0]=='J' for e in caller['events']);need(calls==caller['stages']==17,'actual17 calls')
    hist=load('worker-b/history-cache/FILTER.json');two=load('worker-b/two-cache/FILTER.json')
    actual={r['event']:r for r in load('independent-temporal-result.json')['records']}
    proj={r['event']:r for r in load('projected-temporal-result.json')['records']}
    live={r['event']:r for r in load('worker-b/relocate/KERNEL-RESULT.json')['records']}
    need(sorted(e for e,r in proj.items() if r['earlier_B_hit'])==SITES,'all14 projected earlier-B survivors')
    frames=[space(f) for f in w['frames']]
    mains=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    helpers=set(range(w['public']))-mains;need(len(helpers)==1101,'helper partition')
    T={h:len(w['frames'][w['final'][h]])-len(w['frames'][w['initial'][h]]) for h in helpers}
    queries={};quotients=[]
    def query(event,kind,gens,frame,past):
        ids=[i for i,g in enumerate(gens) if frames[g['frame']]==frames[frame] and (g['event']<event if past else g['event']>event)]
        basis={}
        for i in ids:insert(basis,decode(gens[i]['row']))
        v=residual(decode(actual[event]['target']),basis);need(v,'unrestricted history not a provider')
        need(len(basis)==actual[event]['earlier_B_rank' if past else 'later_A_rank'],'independent history rank')
        quotients.append(dict(event=event,kind=kind,frame=frame,generator_indices=ids,rank=len(basis),target_residual={str(h):str(x) for h,x in v.items()}))
        return basis,v,canon(v)
    for e in SITES:
        r=actual[e];need(proj[e]['earlier_B_hit'],'earlier-B projected prerequisite')
        ins=w['program'][e];need(ins[0]=='MOVE' and ins[4] and ins[1:4]==[r['owner'],r['source'],r['destination']],'exact owned site')
        need(set(decode(r['target']))&mains,'nonzero target main projection')
        gens=hist['generators'] if live[e]['source']['inside'] else two['earlier_generators']
        a=query(e,'pastB',gens,r['destination'],True)
        queries[e]=(a,None)
    directions={canon({h:Q(1)}):dict(unit=h,zero_moves=[]) for h in sorted(helpers)}
    for e in rd['records']:
        u=decode(e['row']);need(u and set(u)<=helpers,'main-free zero MOVE')
        directions.setdefault(canon(u),dict(unit=None,zero_moves=[]))['zero_moves'].append(dict(event=e['event'],rank=e['rank'],owner=e['owner']))
    pricepath=ROOT/'budget_price.py';pins['budget_price.py']=sha256(pricepath.read_bytes()).hexdigest()
    need(pins['budget_price.py']=='527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb','directed price engine')
    sp=importlib.util.spec_from_file_location('shared_constraint_price',pricepath);P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
    invoice=load(str(P.INVOICE.relative_to(ROOT)));need(pins[str(P.INVOICE.relative_to(ROOT))]==P.PIN,'complete invoice pin')
    target={int(r):n for r,n in invoice['after']['T'].items()};paid={int(r):n for r,n in invoice['after']['P'].items()}
    base={r:target.get(r,0)-paid.get(r,0) for r in target.keys()|paid.keys()};kappa=Q(19,5000)
    baseline=P.moment(base,kappa);need(baseline[1]<0,'baseline complete deficit')
    candidates=[];positive=[];best=None
    for key,meta in directions.items():
        if time.monotonic()>deadline:raise TimeoutError('shared-constraint census incomplete')
        u=dict(key);hits=[]
        for e,(past,future) in queries.items():
            a=enabled(past,u)
            if a is None:continue
            b=enabled(future,u) if future else None
            if future and b is None:continue
            hits.append(dict(event=e,rank=actual[e]['rank'],past_alpha=str(a),future_alpha=None if b is None else str(b)))
        benefits={e['event']:e for e in meta['zero_moves']}
        for e in hits:
            need(e['event'] not in benefits or benefits[e['event']]['rank']==e['rank'],'same original event rank')
            benefits[e['event']]=e
        H=min(u,key=lambda h:(T[h],h));gain=Counter(e['rank'] for e in benefits.values());gain[T[H]]-=1
        gain={r:n for r,n in sorted(gain.items()) if n}
        native=P.moment(gain,kappa);complete=P.moment({r:base.get(r,0)+calls*gain.get(r,0) for r in base.keys()|gain.keys()},kappa)
        rec=dict(id=len(candidates),direction={str(h):str(v) for h,v in key},coordinate_unit=meta['unit'],
            enabled_caches=hits,zero_moves=meta['zero_moves'],lost_target_helper=H,lost_target_rank=T[H],
            exact_matching_boundaries=len({(w['initial'][h],w['final'][h]) for h in u})==1,
            gain_rank_profile=gain,native_gain=P.display(native),complete_signed17_moment=P.display(complete),
            optimistic_complete_positive=complete[0]>0)
        rec['credited_event_union']=[dict(event=e['event'],rank=e['rank']) for e in sorted(benefits.values(),key=lambda e:e['event'])]
        rec['native_gain_positive']=native[0]>0
        candidates.append(rec)
        if best is None or complete[0]>best[0]:best=(complete[0],rec['id'])
        if complete[0]>0:positive.append(rec['id'])
    out=dict(status='COMPLETE_EXACT_CREDITED_SHARED_CONSTRAINT_SCREEN',source_sha256=PIN,input_sha256=pins,
        coordinate_units=1101,mainfree_MOVE_rows=468,nonunit_MOVE_classes=len(directions)-1101,
        direction_classes=len(directions),checked_candidates=len(candidates),
        sites=SITES,quotients=quotients,baseline_complete_moment=P.display(baseline),kappa=str(kappa),native_calls=17,
        positive_candidates=positive,best_candidate=best[1],candidates=candidates,seconds=time.monotonic()-start,
        cache_enabling_candidates=sum(bool(c['enabled_caches']) for c in candidates),
        multisite_candidates=sum(len(c['enabled_caches'])>1 for c in candidates),
        native_positive_candidates=[c['id'] for c in candidates if c['native_gain_positive']],
        controls=dict(all_pivots=True,proportional_directions=True,wrong_helper_rejected=True,zero_quotient_rejected=True,
            event_union_no_double_credit=True,distinct_MOVE_credits=True,history_ranks=True),
        scope='All14 earlier-B main-projection survivors, granting source owned CLEAR and all cleanup free. No live-source or future-A condition. One helper constraint; cache and zero-MOVE EVENT UNION; cheapest original support target debit. Cumulative histories only. No physical word or kappa claim.')
    output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('candidates','quotients','input_sha256')},indent=2))
    print('best',json.dumps(candidates[best[1]],indent=2))
    print('cache_enabling',[(c['id'],[h['event'] for h in c['enabled_caches']]) for c in candidates if c['enabled_caches']])
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--seconds',type=float,default=60)
    a=p.parse_args();run(a.output,a.seconds)
