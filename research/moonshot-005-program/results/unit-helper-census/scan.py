#!/usr/bin/env python3
"""Exact complete public-helper scalar-unit payload census."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def check(x,s):
    if not x:raise ValueError(s)
def span(f):
    s={0}
    for b in f:s|={x^b for x in tuple(s)}
    return tuple(sorted(s))
def add(a,b,c):
    for k,v in tuple(b.items()):
        z=a.get(k,F(0))+c*v
        if z:a[k]=z
        else:a.pop(k,None)
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
raw=args.source.read_bytes();check(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw))
first={};canon=[]
for i,f in enumerate(w['frames']):
    s=span(f);first.setdefault(s,i);canon.append(first[s])
X=set(w['live']);M=X|{x+112 for x in X}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
routes={j:[canon[w['initial'][j]]] for j in w['live']}
for e in w['program']:
    if e[0]=='MOVE' and e[1] in X:routes[e[1]].append(canon[e[3]])
R={j:{j:F(1)} for j in range(w['public'])};loc={j:canon[w['initial'][j]] for j in range(w['public'])};events=[];cs={}
def c(s):
    if s not in cs:cs[s]=F(s)
    return cs[s]
for event,e in enumerate(w['program']):
    op,j=e[:2]
    if op=='MOVE':
        check(loc[j]==canon[e[2]],'MOVE source')
        if j<w['public'] and j not in M and len(R[j])==1:
            donor,value=next(iter(R[j].items()))
            if donor in X:events.append(dict(event=event,helper=j,donor=donor,coefficient=str(value),source=canon[e[2]],target=canon[e[3]],donor_access=canon[e[2]] in routes[donor],available_first_donors=sorted(x for x in X if canon[e[2]] in routes[x])))
        loc[j]=canon[e[3]]
    elif op=='INIT':check(j not in R,'live INIT');R[j]={};loc[j]=canon[e[2]]
    elif op=='CLEAR':check(j>=w['public'],'public CLEAR');del R[j];del loc[j]
    elif op=='SCALE':check(loc[j]==canon[e[3]],'SCALE chart');R[j]={k:c(e[2])*v for k,v in R[j].items() if c(e[2])*v}
    elif op in ('ADD','COPY'):
        check(loc[j]==loc[e[2]]==canon[e[4]],'ADD chart')
        if op=='COPY':check(not R[j],'COPY target')
        add(R[j],R[e[2]],c(e[3]))
    else:raise ValueError(op)
target={j:{j:F(1)} for j in range(w['public'])}
for k,x in enumerate(w['live']):
    y=x+112
    if k in w['hosted']['Dports']:target[y]={y:F(1),x:F(1)}
    else:target[x]={x:F(1),y:F(-1)};target[y]={x:F(1,2),y:F(1,2)}
for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):target[x]={x:F(1),y:F(-1)}
check(R==target,'full public endpoint map');check(all(loc[j]==canon[w['final'][j]] for j in loc),'final locations')
out=dict(schema='all-source-unit-helper-payloads-v1',source_sha256=PIN,events=events,total=len(events),donor_accessible_count=sum(e['donor_access'] for e in events),distinct_donors=len({e['donor'] for e in events}),distinct_accessible_donors=len({e['donor'] for e in events if e['donor_access']}),full1480_endpoint_replay='PASS',status='Exact complete unit-payload census; no receiver decoder or restoration asserted.')
payload=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode();args.output.write_bytes(gzip.compress(payload,mtime=0) if args.output.suffix=='.gz' else payload);print(json.dumps({k:v for k,v in out.items() if k!='events'},sort_keys=True))
