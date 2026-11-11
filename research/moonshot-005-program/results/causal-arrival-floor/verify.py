#!/usr/bin/env python3
"""Exact causal normalized-row arrival floor; no predecessor scientific imports."""
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
SOURCE='research/shared-wire-split-composition/data/final.json.gz'
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,message):
    if not ok:raise ValueError(message)
def span_key(rows):
    s={0}
    for r in rows:s|={x^r for x in s}
    return tuple(sorted(s))
def insert(row,basis):
    v=row.copy()
    while v:
        j=min(v)
        if j not in basis:
            a=v[j];basis[j]={k:x/a for k,x in v.items()};return True
        a=v[j]
        for k,b in basis[j].items():
            x=v.get(k,F(0))-a*b
            if x:v[k]=x
            else:v.pop(k,None)
    return False
def addrow(dst,src,c):
    for j,v in src.items():
        x=dst.get(j,F(0))+c*v
        if x:dst[j]=x
        else:dst.pop(j,None)
def scan(w,all_aux_arrivals_free=False):
    mains=set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    need(len(mains)==400,'main census')
    rows=[{} for _ in range(w['public']+w['owned_fields'])]
    for j,r in enumerate(sorted(mains)):rows[r]={j:F(1)}
    canonical={};keys=[]
    for i,frame in enumerate(w['frames']):keys.append(canonical.setdefault(span_key(frame),i))
    need(len(canonical)==1094 and keys[1091]==keys[1092],'frame-span census')
    cache=defaultdict(dict);current=w['initial'][:]+[None]*w['owned_fields']
    for r in mains:insert(rows[r],cache[keys[current[r]]])
    counts=Counter();records=[];free=demands=0;moves=Counter();live=set();peak=0
    for index,event in enumerate(w['program']):
        op,r=event[:2]
        if op=='INIT':
            need(r>=w['public'] and current[r] is None,'INIT guard')
            current[r]=event[2];rows[r]={};live.add(r);peak=max(peak,len(live))
        elif op=='CLEAR':
            need(r>=w['public'] and current[r]==event[2],'CLEAR chart')
            current[r]=None;rows[r]={};live.remove(r)
        elif op=='MOVE':
            need(current[r]==event[2] and event[2]!=event[3],'MOVE source guard')
            current[r]=event[3];kind='main' if r in mains else 'owned' if r>=w['public'] else 'helper';moves[kind]+=1
            if kind=='main' or all_aux_arrivals_free:
                fresh=insert(rows[r],cache[keys[event[3]]]);free+=kind=='main' and fresh
        elif op=='SCALE':
            need(current[r]==event[3],'SCALE chart');c=F(event[2]);need(c!=0,'nonzero SCALE')
            rows[r]={j:c*v for j,v in rows[r].items()}
        elif op in ('ADD','COPY'):
            s=event[2];c=F(event[3]);chart=event[4]
            need(r!=s and current[r]==current[s]==chart,'cochart distinct-source scalar')
            need(c!=0,'nonzero ADD coefficient')
            if op=='COPY':need(not rows[r],'homogeneous COPY-zero guard')
            if r in mains and s not in mains:
                demands+=1
                if insert(rows[s],cache[keys[chart]]):
                    counts[keys[chart]]+=1;records.append([index,r,s,keys[chart]])
            addrow(rows[r],rows[s],c)
        else:raise ValueError('unknown opcode')
    need(current[:w['public']]==w['final'] and not live,'endpoint charts/lifetimes')
    return {'deliveries':len(records),'demand_events':demands,'free_main_innovations':free,
      'by_chart':{str(k):v for k,v in sorted(counts.items())},'records':records,
      'move_counts':dict(moves),'source_owned_peak':peak}
def run(path):
    raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source SHA256 mismatch')
    need(hashlib.sha256(raw+b'\n').hexdigest()!=PIN,'source corruption control')
    w=json.loads(gzip.decompress(raw));r=scan(w)
    need(r['deliveries']==984 and r['demand_events']==7988,'source delivery count')
    need(r['free_main_innovations']==1610 and r['move_counts']['owned']==47,'free/owned counts')
    budget_upper=F(1771183385103604616,18000000000000000)
    need(F(98)<budget_upper<F(99),'exact inherited per-native budget ceiling')
    need(r['records'][0]==[25747,40,812,36] and r['records'][-1]==[51662,79,352,127],'boundary records')
    control=scan(w,all_aux_arrivals_free=True)
    need(control['deliveries']==0,'all auxiliary arrivals granted must remove deficit')
    b={};need(insert({0:F(1)},b) and not insert({0:F(7,3)},b),'rational dependence control')
    need(insert({1:F(1)},b),'independent row control')
    need(not insert({0:F(1),1:F(-7,5)},b),'fractional combination control')
    need(insert({0:F(1)},{}),'different-chart knowledge control')
    r['arrival_record_sha256']=hashlib.sha256(json.dumps(r['records'],separators=(',',':')).encode()).hexdigest()
    r.update(status='PASS_FROZEN_PREFIX_CAUSAL_ARRIVAL_FLOOR',source_path=SOURCE,source_sha256=PIN,
      source_events=len(w['program']),field='Q, exact Fraction arithmetic',alias_grant=[1091,1092],
      unchanged_H4_budget={'extra_move_count_upper':98,'owned_arrival_credit_upper':47,'inherited_per_native_upper':str(budget_upper),
       'fixed_helper_extra_arrival_floor':937,'required_helper_arrival_floor':839},
      controls=['source corruption','all auxiliary arrivals granted yields zero deficit','rational dependence/independence','chart-local knowledge','fractional combination'],
      scope='Frozen main prefixes and literal main MOVE payloads; fixed common helper MOVE payloads for 937 floor. No new kappa.')
    return r
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--records',action='store_true');a=p.parse_args();path=a.source
    if path is None:
        path=next((d/SOURCE for d in Path(__file__).resolve().parents if (d/SOURCE).is_file()),None)
        need(path is not None,'run inside repository or use --source')
    r=run(path)
    if not a.records:
        r['first_arrival']=r['records'][0];r['last_arrival']=r['records'][-1]
        r['demand_chart_count']=len(r['by_chart']);del r['records'];del r['by_chart']
    print(json.dumps(r,indent=2,sort_keys=True))
