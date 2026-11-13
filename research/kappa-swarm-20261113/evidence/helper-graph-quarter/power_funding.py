#!/usr/bin/env python3
"""Exact author certificate for dependent row-matroid blocks, pending review."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,json,time
HERE=Path(__file__).resolve().parent
ROWS_PIN='15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834'
def need(ok,label):
    if not ok:raise ValueError(label)
def add(dst,src,q):
    for h,v in src.items():
        z=dst.get(h,0)+q*v
        if z:dst[h]=z
        else:dst.pop(h,None)
def insert(basis,row):
    v=row.copy()
    while v:
        p=max(v)
        if p not in basis:
            q=1/v[p];basis[p]={h:x*q for h,x in v.items()};return True
        add(v,basis[p],-v[p])
    return False
def rank(rows):
    basis={}
    for row in rows:insert(basis,row)
    return len(basis)
def minimum_basis(rows,targets):
    hs=set().union(*(set(r) for r in rows));need(hs<=set(targets),'all target weights present')
    basis={};chosen=[]
    for h in sorted(hs,key=lambda h:(targets[h],h)):
        if insert(basis,{i:r[h] for i,r in enumerate(rows) if r.get(h)}):chosen.append(h)
    return chosen,len(basis)
def controls():
    need(rank([{0:Q(1),1:Q(1)},{0:Q(1),1:Q(-1)}])==2,'overlapping-support direct sum')
    need(rank([{0:Q(1),1:Q(1)},{0:Q(2),1:Q(2)}])==1,'false direct sum rejected')
    need(1000*1-1023*2<0,'overpriced dependent pair rejected')
    need(1000*4-1023*2>0,'funded dependent pair accepted')
    need(9*1000**100<1023**100,'strict rational power envelope')
    need(9*6**4<11**4,'quarter-power rational envelope')
    return dict(overlapping_support_direct_sum=True,false_direct_sum_rejected=True,
                overpriced_dependent_pair_rejected=True,integer_power_envelope=True,quarter_power_envelope=True)
def run(output):
    start=time.monotonic();deadline=start+60;tested=controls();raw=(HERE/'ROWS.json').read_bytes()
    need(sha256(raw).hexdigest()==ROWS_PIN,'source row pin');d=json.loads(raw)
    mr=(HERE/'MATROID-COMPONENTS.json').read_bytes();m=json.loads(mr)
    inv=json.loads((HERE/'INVENTORY.json').read_text())
    need(m['rows_sha256']==inv['rows_sha256']==ROWS_PIN,'all source bindings')
    records={e['event']:e for e in d['records']};need(len(records)==468,'all main-free rows')
    rows={e:{int(h):Q(v) for h,v in r['row'].items()} for e,r in records.items()}
    targets={int(h):r for h,r in d['targets'].items()}
    need(all(row and set(row)<=set(targets) for row in rows.values()),'nonempty valid helper support')
    need(all(1<=r<=9 for r in targets.values()),'power envelope rank domain')
    need(all(1<=r['rank']<=9 for r in records.values()),'paid rank domain')
    need(all(records[e]['rank']<=min(targets[h] for h in row) for e,row in rows.items()),'pointwise support rank domination')
    partitioned=set();column_support=set()
    for c in inv['components_detail']:
        es=set(c['events']);hs={h for e in es for h in rows[e]}
        need(es and not(partitioned&es) and not(column_support&hs),'support blocks disjoint')
        need(len(es)==c['rows'] and len(hs)==c['columns'] and hs==set(c['helpers']),'support block dimensions')
        partitioned|=es;column_support|=hs
    need(partitioned==set(records),'all source rows partitioned')
    giant=set(next(c['events'] for c in inv['components_detail'] if c['id']==0))
    B=set(m['basis_events']);need(len(B)==342 and B<=giant,'full original row basis coverage')
    need(rank([rows[e] for e in sorted(B)])==342,'fresh full-row basis independence')
    coordinates={e:{e:Q(1)} for e in B};nonbasis=set()
    for rel in m['fundamental_relations']:
        e=rel['nonbasis_event'];v={int(h):Q(q) for h,q in rel['relation'].items()}
        need(e in giant-B and e not in nonbasis and v.get(e)==1,'unique nonbasis relation')
        need(set(v)-{e}<=B and all(v.values()),'fundamental relation uses basis only')
        zero={}
        for j,q in v.items():add(zero,rows[j],q)
        need(not zero,'exact full-source relation')
        coordinates[e]={j:-q for j,q in v.items() if j!=e};nonbasis.add(e)
    need(B|nonbasis==giant and len(nonbasis)==5,'entire giant expansion')
    accounted=set();rank_sum=0;blocks=[];failures=[];independent=dependent=0
    for c in m['components']:
        es=set(c['events']);bs=B&es
        need(es and not(accounted&es) and es<=giant,'component disjoint coverage')
        need(set(c['basis_events'])==bs and all(set(coordinates[e])<=bs for e in es),'each component expansion stays local')
        need(rank([coordinates[e] for e in sorted(es)])==len(bs)==c['rank_Q'],'component exact rank')
        accounted|=es;rank_sum+=len(bs)
        if len(es)==1:continue
        events=sorted(es);table=[0];checks=[]
        for mask in range(1,2**len(events)):
            if time.monotonic()>deadline:raise TimeoutError('bounded dependent-subset checks')
            selected=[e for i,e in enumerate(events) if mask>>i&1]
            r=rank([coordinates[e] for e in selected]);table.append(r)
            if r==len(selected):independent+=1;continue
            dependent+=1
            H,r2=minimum_basis([rows[e] for e in selected],targets)
            need(r2==r,'full-source column rank agrees with certified row coordinates')
            paid_sum=sum(records[e]['rank'] for e in selected);target_sum=sum(targets[h] for h in H)
            margin=1000*target_sum-1023*paid_sum
            quarter_margin=6*target_sum-11*paid_sum
            check=dict(mask=mask,events=selected,rank_Q=r,basis_H=H,
                paid_rank_counts=dict(Counter(records[e]['rank'] for e in selected)),
                basis_target_rank_counts=dict(Counter(targets[h] for h in H)),
                paid_linear_sum=paid_sum,basis_target_linear_sum=target_sum,
                integer_coarse_margin=margin,historical_001_passes=margin>=0,
                quarter_integer_margin=quarter_margin,passes=quarter_margin>=0)
            checks.append(check)
            if quarter_margin<0:failures.append(dict(component=c['id'],**check))
        blocks.append(dict(id=c['id'],events=events,rows=len(events),rank_Q=len(bs),
            subset_ranks_Q_binary_order=table,dependent_subset_checks=checks))
    need(accounted==giant and rank_sum==342,'direct-sum giant rank accounting')
    outside=[]
    for c in inv['components_detail']:
        if c['id']==0:continue
        es=c['events'];actual=rank([rows[e] for e in es])
        need(actual==len(es),'all other support components independent')
        outside.append(dict(id=c['id'],rows=len(es),rank_Q=actual))
    out=dict(status='AUTHOR_DEPENDENT_BLOCK_FUNDING_PENDING_INDEPENDENT_REVIEW' if not failures else 'COARSE_ENVELOPE_FAILURES',
        source_sha256=d['source_sha256'],rows_sha256=ROWS_PIN,matroid_components_sha256=sha256(mr).hexdigest(),
        power_interval=['0','1/4'],strict_integer_envelope='9*6^4<11^4',
        coefficient_rule='6*sum(basis target ranks)>=11*sum(paid ranks)',
        historical_power_interval=['0','1/100'],historical_integer_envelope='9*1000^100<1023^100',
        giant_rows=347,giant_rank_Q=342,giant_coloops=321,dependent_blocks=len(blocks),
        nonempty_subsets_in_dependent_blocks=independent+dependent,
        independent_subsets_funded_by_support=independent,dependent_subsets_checked=dependent,
        all_dependent_subsets_coarsely_funded=not failures,failures=failures,
        outside_support_component_rows=sum(c['rows'] for c in outside),outside_components=outside,
        blocks=blocks,controls=tested,seconds=time.monotonic()-start,
        minimum_basis_to_paid_linear_ratio=str(min(Q(c['basis_target_linear_sum'],c['paid_linear_sum']) for b in blocks for c in b['dependent_subset_checks'])),
        claim_limit='Author certificate only. Universal composition requires independent review of source, row direct sums, Laplace basis-price inequality and graph restriction. No physical or kappa gain.')
    output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('blocks','outside_components','failures')},indent=2))
    print('failures',json.dumps(failures,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'POWER-RESULT.json')
    a=p.parse_args();run(a.output)
