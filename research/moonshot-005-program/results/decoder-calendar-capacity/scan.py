#!/usr/bin/env python3
"""Exact source-route capacity of a current-cochart all-live decoder contract."""
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
REL='research/shared-wire-split-composition/data/final.json.gz'
def need(p,msg):
    if not p: raise ValueError(msg)
def add(a,b,c):
    for j,x in b.items():
        y=a.get(j,F(0))+c*x
        if y:a[j]=y
        else:a.pop(j,None)
def insert(a,basis):
    v=dict(a)
    while v:
        j=min(v)
        if j not in basis:
            c=v[j];basis[j]={k:x/c for k,x in v.items()};return 1
        add(v,basis[j],-v[j])
    return 0
def span(frame):
    s={0}
    for v in frame:s|={x^v for x in s}
    return tuple(sorted(s))
def calendar_floor(events):
    balance=Counter();peaks=Counter()
    for chart,innovations,funded in events:
        balance[chart]+=innovations-funded
        peaks[chart]=max(peaks[chart],balance[chart])
    return sum(peaks.values())
def controls(records):
    need(calendar_floor((f,a+b,2) for _,_,f,_,a,b in records)==0,'two-copy capacity control')
    need(calendar_floor((f,a,1) for _,_,f,_,a,_ in records)==0,'single-copy control')
    need(calendar_floor([(0,0,1),(0,1,0)])==0,'prefetch slack control')
    need(calendar_floor([(0,1,0),(0,0,1)])==1,'late credit cannot pay early demand')
    need(calendar_floor([(0,1,0),(1,1,0)])==2,'separate charts control')
    b={};need(insert({0:F(2,3)},b)==1 and insert({0:F(-7,5)},b)==0,'rational dependence control')
    need(insert({1:F(1)},b)==1,'rational independence control')
    return ['two funded fields at every MOVE gives zero','one virtual copy gives zero','prefetch slack retained','late arrivals cannot pay earlier deficits','separate charts','exact rational dependence and independence','source SHA256','typed owned MOVE and lifecycle guards']
def run(source):
    raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    w=json.loads(gzip.decompress(raw));n=w['public'];m=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    need((n,len(m))==(1480,400),'input partition')
    canonical={};keys=[canonical.setdefault(span(f),i) for i,f in enumerate(w['frames'])]
    need(all(len(span(f))==2**len(f) for f in w['frames']),'independent frame bases')
    need(len(canonical)==1094 and keys[1091]==keys[1092],'canonical chart census')
    c=[{r:F(1)} for r in range(n)]+[{} for _ in range(w['owned_fields'])]
    d=[({r:F(1)} if r in m else {}) for r in range(n)]+[{} for _ in range(w['owned_fields'])]
    current=w['initial'][:]+[None]*w['owned_fields']
    cb=defaultdict(dict);db=defaultdict(dict)
    for r in range(n):
        f=keys[current[r]];insert(c[r],cb[f]);insert(d[r],db[f])
    balances={m:Counter() for m in (1,2)};peaks={m:Counter() for m in (1,2)};witnesses={m:{} for m in (1,2)}
    records=[];census=Counter();prefixes={}
    for i,e in enumerate(w['program']):
        op,r=e[:2]
        if op=='INIT':
            need(r>=n and current[r] is None,'INIT');current[r]=e[2];c[r]={};d[r]={}
        elif op=='CLEAR':
            need(r>=n and current[r]==e[2],'CLEAR');current[r]=None;c[r]={};d[r]={}
        elif op=='MOVE':
            need(current[r]==e[2] and e[4]==(r>=n),'typed MOVE')
            sa=set(span(w['frames'][e[2]]));sb=set(span(w['frames'][e[3]]))
            need(sa<sb or sb<sa,'strict nested source MOVE')
            f=keys[e[3]];a=insert(c[r],cb[f]);b=insert(d[r],db[f]);current[r]=e[3]
            kind='main' if r in m else 'owned' if r>=n else 'helper';census[kind]+=1
            rec=[i,r,f,kind,a,b];records.append(rec)
            for owned in (1,2):
                funded=2 if kind=='main' else owned if kind=='owned' else 1
                balances[owned][f]+=a+b-funded
                if balances[owned][f]>peaks[owned][f]:
                    peaks[owned][f]=balances[owned][f];witnesses[owned][f]=i
        elif op=='SCALE':
            need(current[r]==e[3] and F(e[2])!=0,'SCALE')
            c[r]={j:F(e[2])*x for j,x in c[r].items()};d[r]={j:F(e[2])*x for j,x in d[r].items()}
        elif op in ('ADD','COPY'):
            s=e[2];need(r!=s and current[r]==current[s]==e[4],'cochart scalar')
            if op=='COPY':need(not c[r] and not d[r],'COPY zero')
            add(c[r],c[s],F(e[3]));add(d[r],d[s],F(e[3]))
        else:raise ValueError(op)
        if i+1 in (25489,25490,25728,26226,36961,71261):
            prefixes[str(i+1)]={str(k):sum(peaks[k].values()) for k in peaks}
    need(current[:n]==w['final'] and all(f is None for f in current[n:]),'endpoint')
    need({k:sum(peaks[k].values()) for k in peaks}=={1:3144,2:3111},'source capacity certificate')
    return {'status':'PASS_ALL_LIVE_DECODER_CAPACITY_FLOOR','source_sha256':PIN,'events':len(w['program']),'move_census':dict(census),'prefix_lower_bounds':prefixes,'controls':controls(records),
      'extra_arrival_floor':{str(k):sum(peaks[k].values()) for k in peaks},
      'by_chart':{str(k):{str(f):{'floor':v,'maximizing_event':witnesses[k][f]} for f,v in sorted(peaks[k].items()) if v>0} for k in peaks},
      'arrival_innovations':records,'interpretation':'owned funding 1 or2; main2, helper1; arbitrary payloads and unlimited immutable caches; all-live current-cochart two-copy decoder required. No new kappa.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    source=a.source or next((base/REL for base in Path(__file__).resolve().parents if (base/REL).is_file()),None)
    need(source is not None,'provide --source or place inside source repository');r=run(source)
    if a.output:a.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('by_chart','arrival_innovations')},indent=2))
