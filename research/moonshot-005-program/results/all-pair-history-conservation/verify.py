#!/usr/bin/env python3
"""Exact reconstruction of the previously unpublished104-pair source law."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip, hashlib, json, time
from pathlib import Path

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,msg):
    if not ok: raise ValueError(msg)
def axpy(dst,src,c=F(1)):
    for k,v in tuple(src.items()):
        z=dst.get(k,F(0))+c*v
        if z: dst[k]=z
        else: dst.pop(k,None)
def space(frame):
    s={0}
    for v in frame: s|={v^x for x in tuple(s)}
    return frozenset(s)
def derive(w,C,records,control,ys,scalars):
    """Solve exact relations from the complete permitted control span."""
    n=len(ys);adj=[{} for _ in range(w['public']+w['owned_fields'])]
    for i,y in enumerate(ys): adj[y]={i:F(1)}
    bytime=defaultdict(list);pair=[r['pair'] for r in records];bases=[{} for _ in ys]
    for i,r in enumerate(records): bytime[r['after_event']].append(i)
    loc=dict(enumerate(w['final']));samples=0
    def inspect(j,t):
        nonlocal samples
        if j not in loc or not adj[j]: return
        pairs=control.get(C[loc[j]],())
        if not pairs: return
        common={k:v for k,v in adj[j].items() if k<n};local=defaultdict(dict)
        for k,v in adj[j].items():
            if k>=n: local[pair[k-n]][k]=v
        for i in pairs:
            row=dict(common);row.update(local.get(i,{}))
            if not row: continue
            samples+=1;basis=bases[i]
            for pivot in sorted(basis):
                if pivot in row: axpy(row,basis[pivot],-row[pivot])
            if row:
                p=min(row);need(p<n,f'new receiver direction pair{i} cut{t} role{j} pivot{p}')
                c=row[p];basis[p]={k:v/c for k,v in row.items()}
    for j in loc: inspect(j,len(w['program']))
    for t in range(len(w['program'])-1,-1,-1):
        for i in bytime.get(t,()):
            r=records[i];j=r['role'];need(loc[j]==r['chart'],'extraction observation chart');adj[j][n+i]=adj[j].get(n+i,F(0))+1;inspect(j,t+1)
        e=w['program'][t];op,j=e[:2]
        if op in ('ADD','COPY'):
            axpy(adj[e[2]],adj[j],scalars[str(e[3])]);inspect(e[2],t)
            if op=='COPY': adj[j]={};inspect(j,t)
        elif op=='SCALE':
            c=scalars[str(e[2])];adj[j]={k:c*v for k,v in adj[j].items() if c*v};inspect(j,t)
        elif op=='MOVE': loc[j]=e[2];inspect(j,t)
        elif op=='CLEAR': loc[j]=e[2];adj[j]={};inspect(j,t)
        elif op=='INIT': loc.pop(j);adj[j]={}
        if t%10000==0: print('DERIVE',t,'samples',samples,'maxrank',max(map(len,bases)),flush=True)
    for i,r in enumerate(records):
        coeff={};basis=bases[r['pair']]
        for p in sorted(basis,reverse=True):
            value=basis[p].get(n+i,F(0))-sum(v*coeff.get(k,F(0)) for k,v in basis[p].items() if p<k<n)
            if value: coeff[p]=value
        r['endpoint_coefficients']=[[ys[k],str(v)] for k,v in sorted(coeff.items())]
    return dict(samples=samples,rank_histogram=dict(sorted(Counter(map(len,bases)).items())))
def main(a):
    start=time.monotonic();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    w=json.loads(gzip.decompress(raw));P=w['program'];seen={}
    C=[seen.setdefault(space(f),i) for i,f in enumerate(w['frames'])]
    xs=w['live'];ys=[x+112 for x in xs];pos={x:i for i,x in enumerate(xs)}
    route={x:[C[w['initial'][x]]] for x in xs+ys}
    for e in P:
        if e[0]=='MOVE' and e[1] in route: route[e[1]].append(C[e[3]])
    observe=defaultdict(list);control=defaultdict(set)
    for i,(x,y) in enumerate(zip(xs,ys)):
        need(not set(route[x])&set(route[y]),f'pair chart intersection{x}')
        for c in set(route[y]): observe[c].append(i)
        for c in set(route[x]): control[c].add(i)
    rows=[{pos[j]:F(1)} if j in pos else {} for j in range(w['public']+w['owned_fields'])]
    loc=dict(enumerate(w['initial']));records=[]
    scalars={str(c):F(c) for e in P for c in ([e[3]] if e[0] in ('ADD','COPY') else [e[2]] if e[0]=='SCALE' else [])}
    for t,e in enumerate(P):
        op,j=e[:2]
        if op=='ADD': axpy(rows[j],rows[e[2]],scalars[str(e[3])])
        elif op=='COPY':
            need(not rows[j],'zero COPY X columns');rows[j]={k:c*scalars[str(e[3])] for k,c in rows[e[2]].items()}
        elif op=='SCALE':
            c=scalars[str(e[2])];rows[j]={k:c*v for k,v in rows[j].items() if c*v}
        elif op=='INIT': rows[j]={};loc[j]=e[2]
        elif op=='CLEAR': rows[j]={};loc.pop(j)
        elif op=='MOVE':
            need(loc[j]==e[2],'forward chart');loc[j]=e[3]
            for i in observe[C[e[3]]]: records.append(dict(pair=i,donor=xs[i],receiver=ys[i],after_event=t,role=j,chart=e[3],x_response=rows[j].copy()))
        else: raise ValueError(op)
    need(len(records)==2846,'arrival census');gain=[]
    for i,y in enumerate(ys): need(set(rows[y])=={i},'endpoint diagonal');gain.append(rows[y][i])
    for r in records: r['endpoint_coefficients']=[[ys[j],str(c/gain[j])] for j,c in sorted(r.pop('x_response').items())]
    print('FORWARD',len(records),'baseline_ansatz_max_terms',max(len(r['endpoint_coefficients']) for r in records),'seconds',round(time.monotonic()-start,3),flush=True)
    extraction=derive(w,C,records,control,ys,scalars)
    print('DERIVED','max_terms',max(len(r['endpoint_coefficients']) for r in records),'seconds',round(time.monotonic()-start,3),flush=True)
    adj=[{} for _ in rows];bytime=defaultdict(list);pair=[r['pair'] for r in records]
    for i,r in enumerate(records):
        bytime[r['after_event']].append(i)
        for j,c in r['endpoint_coefficients']: adj[j][i]=-F(c)
    loc=dict(enumerate(w['final']));entries=0;checks=0;fail=[];maxlive=sum(map(len,adj))
    def inspect(j,t):
        nonlocal entries,checks
        if j not in loc: return
        checks+=1;entries+=len(adj[j]);allowed=control.get(C[loc[j]],())
        for i,v in adj[j].items():
            if pair[i] in allowed:
                fail.append(dict(identity=i,cut=t,role=j,chart=loc[j],coefficient=str(v),observation=records[i]))
                if len(fail)>=5: raise ValueError(json.dumps(fail))
    for j in loc: inspect(j,len(P))
    for t in range(len(P)-1,-1,-1):
        for i in bytime.get(t,()):
            r=records[i];j=r['role'];need(loc[j]==r['chart'],'reverse observation chart');v=adj[j].get(i,F(0))+1
            if v: adj[j][i]=v
            else: adj[j].pop(i,None)
            inspect(j,t+1)
        e=P[t];op,j=e[:2]
        if op in ('ADD','COPY'):
            k=e[2];axpy(adj[k],adj[j],scalars[str(e[3])]);inspect(k,t)
            if op=='COPY': adj[j]={};inspect(j,t)
        elif op=='SCALE':
            c=scalars[str(e[2])];adj[j]={k:c*v for k,v in adj[j].items() if c*v};inspect(j,t)
        elif op=='MOVE': need(loc[j]==e[3],'reverse MOVE');loc[j]=e[2];inspect(j,t)
        elif op=='CLEAR': loc[j]=e[2];adj[j]={};inspect(j,t)
        elif op=='INIT': loc.pop(j);adj[j]={}
        else: raise ValueError(op)
        if t%10000==0:
            maxlive=max(maxlive,sum(map(len,adj)));print('ADJOINT',t,'seconds',round(time.monotonic()-start,3),flush=True)
    need(not fail,'nonzero control adjoint')
    cert=dict(schema='moonshot-all-pair-history-conservation-v1',source_sha256=PIN,native_instructions=len(P),public_common_fields=w['public'],
        pairs=[dict(donor=x,receiver=y,donor_station_charts=route[x],receiver_route_charts=route[y],initial_observations=sum(C[c] in set(route[y]) for c in w['initial'])) for x,y in zip(xs,ys)],
        endpoint_roles=ys,arrival_identities=records,
        scope='Each donor separately: all-cut controls at its original station charts. Histories factor through104 commonY endpoints; no additional routes or correlated side information.')
    payload=(json.dumps(cert,indent=2,sort_keys=True)+'\n').encode();a.output.mkdir(parents=True,exist_ok=True)
    (a.output/'CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    result=dict(status='PASS_ALL104_PAIR_HISTORY_IDENTITIES',source_sha256=PIN,certificate_payload_sha256=hashlib.sha256(payload).hexdigest(),pairs=len(xs),arrivals=len(records),cuts=len(P)+1,term_count_histogram=dict(sorted(Counter(len(r['endpoint_coefficients']) for r in records).items())),extraction=extraction,checked_nonzero_adjoint_entries=entries,checked_changed_role_states=checks,sampled_max_live_adjoint_entries=maxlive,elapsed_seconds=time.monotonic()-start,new_complete_kappa=None)
    (a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
