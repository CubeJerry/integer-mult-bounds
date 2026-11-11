"""Extract and check a source endpoint/history transfer law."""
import argparse
import collections
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(v,m):
    if not v:raise ValueError(m)
def span(frame):
    s={0}
    for x in frame:s.update(x^y for y in tuple(s))
    return frozenset(s)
def add(row,j,v):
    z=row.get(j,Q(0))+v
    if z:row[j]=z
    else:row.pop(j,None)
def check_dual(w,C,rec,stations):
    P=w['program'];a={189:-Q(rec['endpoint_coefficient'])} if Q(rec['endpoint_coefficient']) else {};loc=dict(enumerate(w['final']));at=rec['after_event'];h=rec['role'];touched=0
    def check(j,t):
        nonlocal touched
        if j in loc and C[loc[j]] in stations:
            touched+=1
            need(not a.get(j),f'nonzero station adjoint at cut{t}, role{j}, chart{loc[j]}, value{a.get(j)}')
    for j in loc:check(j,len(P))
    for t in range(len(P)-1,-1,-1):
        if t==at:
            need(loc[h]==rec['chart'],'observation exact location')
            add(a,h,Q(1));check(h,t+1)
        e=P[t];op,j=e[:2];changed=[]
        if op=='ADD':
            s=e[2];add(a,s,a.get(j,Q(0))*Q(e[3]));changed=[s]
        elif op=='COPY':
            s=e[2];add(a,s,a.get(j,Q(0))*Q(e[3]));a.pop(j,None);changed=[s,j]
        elif op=='SCALE':
            z=a.get(j,Q(0))*Q(e[2]);a.pop(j,None)
            if z:a[j]=z
            changed=[j]
        elif op=='MOVE':loc[j]=e[2];changed=[j]
        elif op=='CLEAR':loc[j]=e[2];a.pop(j,None);changed=[j]
        elif op=='INIT':loc.pop(j,None);a.pop(j,None)
        else:raise ValueError(op)
        for j in changed:check(j,t)
    return {'observation':(at,h,rec['chart']),'endpoint_coefficient':rec['endpoint_coefficient'],'station_checks':touched,'baseline_functional_support':len(a),'baseline_row':{str(j):str(v) for j,v in sorted(a.items())}}
def main(args):
    raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'pin');w=json.loads(gzip.decompress(raw));C=list(map(span,w['frames']));P=w['program'];donor=77;receiver=189
    ds=[w['initial'][donor]]+[e[3] for e in P if e[:2]==['MOVE',donor]];rs=[w['initial'][receiver]]+[e[3] for e in P if e[:2]==['MOVE',receiver]]
    stations={C[c] for c in ds};route={C[c] for c in rs};need(not stations&route,'disjoint station/receiver chart spaces')
    loc=dict(enumerate(w['initial']));a={77:Q(1)};obs=[];initial=[j for j,ch in enumerate(w['initial']) if C[ch] in route]
    for t,e in enumerate(P):
        op,j=e[:2]
        if op=='ADD':add(a,j,a.get(e[2],Q(0))*Q(e[3]))
        elif op=='COPY':
            z=a.get(e[2],Q(0))*Q(e[3]);a.pop(j,None)
            if z:a[j]=z
        elif op=='SCALE':
            z=a.get(j,Q(0))*Q(e[2]);a.pop(j,None)
            if z:a[j]=z
        elif op=='INIT':a.pop(j,None);loc[j]=e[2]
        elif op=='CLEAR':a.pop(j,None);loc.pop(j)
        elif op=='MOVE':
            loc[j]=e[3]
            if C[e[3]] in route:obs.append({'after_event':t,'role':j,'chart':e[3],'endpoint_coefficient':str(a.get(j,Q(0)))})
    need(len(obs)==19 and len(initial)==1046 and a.get(189)==1,'source census')
    cert={'schema':'donor77-receiver189-rank-one-response/1','source_sha256':PIN,'donor':donor,'receiver':receiver,'station_charts':ds,'receiver_charts':rs,'initial_observation_count':len(initial),'arrival_observations':obs,'endpoint':{'role':189,'chart':w['final'][189]},'claim':'For arbitrary additive interventions at the five donor stations at all native times, each receiver arrival perturbation equals its listed coefficient times the final common189 perturbation.'}
    checked=[check_dual(w,C,x,stations) for x in obs]
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n');args.output.with_name('rank-one-extraction-result.json').write_text(json.dumps({'source_sha256':PIN,'checked':checked},indent=2,sort_keys=True)+'\n')
    print('PASS_RANK_ONE_HISTORY_RESPONSE',len(obs),collections.Counter(x['endpoint_coefficient'] for x in obs))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
