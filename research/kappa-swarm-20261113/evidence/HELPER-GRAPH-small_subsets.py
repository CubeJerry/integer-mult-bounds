#!/usr/bin/env python3
"""Bounded exact minimum-column-basis funding checks on small components."""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,itertools,json,time
HERE=Path(__file__).resolve().parent
SOURCE='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
ROWS_PIN='15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834'
def need(ok,label):
    if not ok:raise ValueError(label)
def insert(basis,column):
    v=column.copy()
    while v:
        p=max(v)
        if p not in basis:
            q=1/v[p];basis[p]={i:x*q for i,x in v.items()};return True
        q=-v[p]
        for i,x in basis[p].items():
            z=v.get(i,0)+q*x
            if z:v[i]=z
            else:v.pop(i,None)
    return False
def minimum_basis(rows,targets):
    hs=set().union(*(set(r) for r in rows))
    need(hs<=set(targets),'every support coordinate has a helper target weight')
    basis={};chosen=[]
    for h in sorted(hs,key=lambda h:(targets[h],h)):
        col={i:r[h] for i,r in enumerate(rows) if r.get(h)}
        if insert(basis,col):chosen.append(h)
    return chosen,len(basis)
def check(rows,paid,targets):
    hs,rank=minimum_basis(rows,targets)
    cost=[sum(min(targets[h],k) for h in hs) for k in range(1,10)]
    removed=[sum(min(r,k) for r in paid) for k in range(1,10)]
    margin=[a-b for a,b in zip(cost,removed)]
    return dict(rank_Q=rank,column_basis=hs,basis_target_ranks=[targets[h] for h in hs],
        basis_cost_min_r_k=cost,removed_cost_min_r_k=removed,funding_margin_min_r_k=margin,
        passes=all(x>=0 for x in margin))
def controls():
    parallel=check([{0:Q(1)},{0:Q(2)}],[1,1],{0:1})
    need(parallel['rank_Q']==1 and parallel['funding_margin_min_r_k']==[-1]*9,'dependent rows remain separately charged')
    rows=[{0:Q(1),2:Q(1)},{1:Q(1),2:Q(1)}];targets={0:9,1:1,2:2}
    found=check(rows,[1,1],targets)
    need(found['column_basis']==[1,2],'rank-sorted greedy avoids expensive column')
    for k in range(1,10):
        costs=[]
        for hs in itertools.combinations(targets,2):
            b={}
            for h in hs:insert(b,{i:r[h] for i,r in enumerate(rows) if r.get(h)})
            if len(b)==2:costs.append(sum(min(targets[h],k) for h in hs))
        need(found['basis_cost_min_r_k'][k-1]==min(costs),'greedy agrees with brute column bases')
    try:minimum_basis([{999:Q(1)}],{})
    except ValueError:pass
    else:raise ValueError('missing helper target accepted')
    return dict(dependent_rows_charged=True,minimum_basis_vs_brute=True,missing_helper_target_rejected=True)
def run(maximum,output):
    start=time.monotonic();tested=controls();raw=(HERE/'ROWS.json').read_bytes()
    need(sha256(raw).hexdigest()==ROWS_PIN,'source-derived row snapshot pin')
    data=json.loads(raw);need(data['source_sha256']==SOURCE,'literal word pin')
    invraw=(HERE/'INVENTORY.json').read_bytes();inv=json.loads(invraw)
    need(inv['rows_sha256']==ROWS_PIN and inv['source_sha256']==SOURCE,'inventory pin')
    targets={int(h):r for h,r in data['targets'].items()}
    records={r['event']:r for r in data['records']};rows={e:{int(h):Q(v) for h,v in r['row'].items()} for e,r in records.items()}
    need(len(records)==len(data['records'])==468,'complete distinct main-free rows')
    covered=set();used=set();details=[];omitted=[];failures=[];subsets=0;covered_rows=0
    for c in inv['components_detail']:
        events=c['events'];hs={h for e in events for h in rows[e]}
        need(len(events)==c['rows'] and len(hs)==c['columns'] and hs==set(c['helpers']),'component support inventory')
        need(not(covered&set(events)) and not(used&hs),'disjoint component rows/columns')
        covered.update(events);used.update(hs)
        if len(events)>maximum:omitted.append(dict(id=c['id'],rows=len(events),columns=len(hs)));continue
        covered_rows+=len(events);table=[]
        for mask in range(1,2**len(events)):
            es=[e for i,e in enumerate(events) if mask>>i&1]
            result=check([rows[e] for e in es],[records[e]['rank'] for e in es],targets)
            result.update(mask=mask,events=es);subsets+=1;table.append(result)
            if not result['passes']:failures.append(dict(component=c['id'],**result))
        details.append(dict(id=c['id'],rows=len(events),columns=len(hs),subsets=table))
    need(covered==set(records),'all rows accounted including explicit omissions')
    result=dict(status='BOUNDED_EXACT_COLUMN_BASIS_FUNDING_CHECK',source_sha256=SOURCE,rows_sha256=ROWS_PIN,
        inventory_sha256=sha256(invraw).hexdigest(),maximum_component_rows=maximum,
        tested_components=len(details),tested_source_rows=covered_rows,tested_nonempty_subsets=subsets,
        integer_tariff_checks=9*subsets,all_tested_pass=not failures,failures=failures,
        omitted_components=omitted,details=details,controls=tested,seconds=time.monotonic()-start,
        scope='Only complete support components of at most the declared row bound. Omitted components prevent a universal no-gain theorem. Failure is an optimistic funding counterexample, not a physical supplier.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('details','failures')},indent=2))
    print('failures',json.dumps(failures,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--max-component-rows',type=int,default=5)
    p.add_argument('--output',type=Path,default=HERE/'SMALL-RESULT.json')
    a=p.parse_args();run(a.max_component_rows,a.output)
