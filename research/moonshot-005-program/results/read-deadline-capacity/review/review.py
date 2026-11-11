#!/usr/bin/env python3
"""Independent rational online audit of read-deadline calendar capacities."""
import argparse,gzip,hashlib,json
from fractions import Fraction as Q
from collections import defaultdict,Counter
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def require(x,s):
    if not x:raise ValueError(s)
def axpy(a,b,c):
    for j,x in b.items():
        v=a.get(j,Q(0))+c*x
        if v:a[j]=v
        else:a.pop(j,None)
def extend(row,basis):
    a=dict(row)
    while a:
        j=min(a);v=a[j]
        if j not in basis:
            basis[j]={k:x/v for k,x in a.items()};return 1
        axpy(a,basis[j],-v)
    return 0
def frame_key(b):
    s={0}
    for x in b:s|={t^x for t in s}
    return tuple(sorted(s))
def run(source,author):
    raw=source.read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public'];N=n+w['owned_fields']
    main=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);require((n,len(main))==(1480,400),'partition')
    aliases={};keys=[aliases.setdefault(frame_key(f),i) for i,f in enumerate(w['frames'])]
    c=[{r:Q(1)} if r<n else {} for r in range(N)];d=[{r:Q(1)} if r in main else {} for r in range(N)];at=w['initial'][:]+[None]*w['owned_fields']
    cb=defaultdict(dict);db={mode:defaultdict(dict) for mode in ('main_departure_and_endpoint','endpoint_only')};known=[True]*N
    net={(mode,o):Counter() for mode in db for o in (1,2)};peak={k:Counter() for k in net};where={k:{} for k in net};records=[]
    for r in range(n):
        f=keys[at[r]];extend(c[r],cb[f])
        for mode in db:extend(d[r],db[mode][f])
    def ask(r,kind,i,phase,mode=None):
        if kind==0 and known[r]:return
        f=keys[at[r]];fresh=extend(c[r] if kind==0 else d[r],cb[f] if kind==0 else db[mode][f])
        if kind==0:known[r]=True
        if not fresh:return
        records.append([i,phase,r,f,kind,mode if kind else 'both'])
        for m in db if kind==0 else (mode,):
            for o in (1,2):
                k=(m,o);net[k][f]+=1
                if net[k][f]>peak[k][f]:peak[k][f]=net[k][f];where[k][f]=[i,phase,r,kind]
    for i,e in enumerate(w['program']):
        op,r=e[:2]
        if op=='INIT':
            require(r>=n and at[r] is None,'INIT');at[r]=e[2];c[r]={};d[r]={};known[r]=True
        elif op=='CLEAR':
            require(r>=n and at[r]==e[2],'CLEAR');at[r]=None;c[r]={};d[r]={};known[r]=True
        elif op=='MOVE':
            require(at[r]==e[2] and e[4]==(r>=n),'MOVE type/source')
            if r in main:ask(r,1,i,'before-departure','main_departure_and_endpoint')
            at[r]=e[3];known[r]=False;f=keys[at[r]]
            for m,o in net:net[(m,o)][f]-=2 if r in main else o if r>=n else 1
        elif op in ('ADD','COPY'):
            s=e[2];require(r!=s and at[r]==at[s]==e[4],'cochart read');z=Q(e[3]);require(z!=0,'nonzero coefficient')
            ask(r,0,i,'before-target-read');ask(s,0,i,'before-source-read')
            if op=='COPY':require(not c[r] and not d[r],'literal COPYzero')
            axpy(c[r],c[s],z);axpy(d[r],d[s],z)
        elif op=='SCALE':
            require(at[r]==e[3] and Q(e[2])!=0,'SCALE');ask(r,0,i,'before-scale-read')
            c[r]={j:Q(e[2])*v for j,v in c[r].items()};d[r]={j:Q(e[2])*v for j,v in d[r].items()}
        else:raise ValueError(op)
    require(at[:n]==w['final'] and all(x is None for x in at[n:]),'final charts')
    for r in range(n):ask(r,0,len(w['program']),'common-endpoint')
    for r in sorted(main):
        for m in db:ask(r,1,len(w['program']),'difference-endpoint',m)
    charts={m:{str(o):{str(f):{'floor':v,'first_maximizer':where[(m,o)][f]} for f,v in sorted(peak[(m,o)].items()) if v>0} for o in (1,2)} for m in db}
    floors={m:{str(o):sum(peak[(m,o)].values()) for o in (1,2)} for m in db}
    a=json.loads(author.read_text())['cases']['read_deadlines'];require(records==a['records'],'every independent rational demand record');require(charts==a['by_chart'],'all chart maxima/time witnesses');require(floors==a['extra_arrival_floors'],'all floors')
    return {'status':'PASS_INDEPENDENT_RATIONAL_READ_DEADLINE_CAPACITY','source_sha256':PIN,'author_certificate_sha256':hashlib.sha256(author.read_bytes()).hexdigest(),'floors':floors,'records_checked':len(records),'method':'Separately implemented exact Fraction/min-pivot online replay; author uses modular maximum-pivot. Both use proved scalar-closure membership caching. No author implementation imported.','scope':'Read-deadline and final common states; main-departure plus endpoint or endpoint-only differences; fixed arrival calendar. Zero rank relaxation is not feasibility.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.author);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(s)
    print(s,end='')
