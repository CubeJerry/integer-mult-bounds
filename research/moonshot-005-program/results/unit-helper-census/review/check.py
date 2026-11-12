#!/usr/bin/env python3
"""Independent complete scalar-unit census and backward joint-response review."""
import argparse,collections,gzip,hashlib,json,time
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,s):
    if not x:raise ValueError(s)
def read(p):
    b=p.read_bytes();return gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
def span(f):
    s={0}
    for x in f:s|={y^x for y in s}
    return frozenset(s)
def axpy(a,b,c=Q(1)):
    for k,v in tuple(b.items()):
        x=a.get(k,Q(0))+c*v
        if x:a[k]=x
        else:a.pop(k,None)
def encode(r):return [[k,str(v)] for k,v in sorted(r.items())]
def rank(cols):
    basis={};witness=[]
    for i,c in enumerate(cols):
        z=dict(c)
        while z:
            p=max(z)
            if p not in basis:
                a=z[p];basis[p]={j:v/a for j,v in z.items()};witness.append([i,p,str(a)]);break
            axpy(z,basis[p],-z[p])
    return len(basis),witness
def common(w):
    t={i:{i:Q(1)} for i in range(1480)};D=set(w['hosted']['Dports'])
    for k,x in enumerate(w['live']):
        y=x+112
        if k in D:t[y]={x:Q(1),y:Q(1)}
        else:t[x]={x:Q(1),y:Q(-1)};t[y]={x:Q(1,2),y:Q(1,2)}
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):t[x]={x:Q(1),y:Q(-1)}
    return t
def main(a):
    started=time.monotonic();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public'];P=w['program'];F=list(map(span,w['frames']));canonical={}
    for i,f in enumerate(F):canonical.setdefault(f,i)
    cb=read(a.census);rb=read(a.responses);C=json.loads(cb);R=json.loads(rb)
    need(C['source_sha256']==R['source_sha256']==PIN and R['census_sha256']==hashlib.sha256(cb).hexdigest(),'author source/census pins')
    first=set(w['live']);main=first|{j+112 for j in first}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);routes={j:{F[w['initial'][j]]} for j in first}
    for e in P:
        if e[0]=='MOVE' and e[1] in first:routes[e[1]].add(F[e[3]])
    state={j:{j:Q(1)} for j in range(n)};loc={j:F[f] for j,f in enumerate(w['initial'])};events=[]
    for t,e in enumerate(P):
        op,j=e[:2]
        if op=='MOVE':
            need(loc[j]==F[e[2]] and bool(e[4])==(j>=n),'MOVE ownership/location');s,d=F[e[2]],F[e[3]];need(s<d or d<s,'proper nested MOVE')
            if j<n and j not in main and len(state[j])==1:
                donor,c=next(iter(state[j].items()))
                if donor in first:
                    events.append({'event':t,'helper':j,'donor':donor,'coefficient':str(c),'source':canonical[s],'target':canonical[d],'donor_access':s in routes[donor],'available_first_donors':sorted(x for x in first if s in routes[x])})
            loc[j]=d
        elif op=='INIT':need(j>=n and j not in state,'owned INIT');state[j]={};loc[j]=F[e[2]]
        elif op=='CLEAR':need(j>=n and j in state and loc[j]==F[e[2]],'owned CLEAR');del state[j];del loc[j]
        elif op=='SCALE':c=Q(e[2]);need(c and loc[j]==F[e[3]],'SCALE');state[j]={k:c*v for k,v in state[j].items()}
        elif op in ('ADD','COPY'):
            k=e[2];need(j!=k and loc[j]==loc[k]==F[e[4]],'cochart access')
            if op=='COPY':need(not state[j],'baseline zero COPY guard')
            axpy(state[j],state[k],Q(e[3]))
        else:raise ValueError(op)
    need(state==common(w) and all(loc[j]==F[w['final'][j]] for j in state),'complete1480 native endpoint replay')
    need(events==C['events'] and len(events)==38,'complete independent scalar-unit census')
    need(sum(e['donor_access'] for e in events)==37 and len({e['donor'] for e in events})==36,'access and donor census')
    print('independent complete unit census PASS',round(time.monotonic()-started,3),flush=True)
    cut={e['event']:k for k,e in enumerate(events)};off={j for j,f in enumerate(w['final']) if F[f]!=span([1,2,4,8,16,32,64,128,256])};need(len(off)==458,'offhub census')
    adj={j:({j:Q(1)} if j in off else {}) for j in range(n)};Z=[{} for e in events];L=[{} for e in events];guardbase=n+len(events)
    def row(j):return adj.setdefault(j,{})
    for t in range(len(P)-1,-1,-1):
        e=P[t];op,j=e[:2]
        if t in cut:
            k=cut[t]
            for label,c in row(j).items():
                if label<n:Z[k][label]=c
                elif label<guardbase:
                    i=label-n;need(i>k,'strict causal response');L[i][k]=c
                else:raise ValueError('nonzero COPY guard perturbation')
            axpy(row(j),{n+k:Q(1)})
        if op=='ADD':axpy(row(e[2]),row(j),Q(e[3]))
        elif op=='SCALE':adj[j]={k:Q(e[2])*v for k,v in row(j).items()}
        elif op=='COPY':axpy(row(e[2]),row(j),Q(e[3]));adj[j]={guardbase+t:Q(1)}
        elif op=='CLEAR':adj[j]={}
        elif op=='INIT':adj.pop(j,None)
    need([encode(z) for z in Z]==R['offhub_columns'] and [encode(l) for l in L]==R['chronological_L'],'independent backward Z/L')
    need(all(not g for g in R['copy_guard_responses']),'author COPY zero response')
    for k,e in enumerate(events):
        h={j:r[n+k] for j,r in adj.items() if n+k in r};need(h=={e['donor']:Q(e['coefficient'])},'forward/backward scalar payload match')
        claim=R['cuts'][k];need(claim['own_final_Y_response']==str(Z[k].get(e['donor']+112,Q(0))) and claim['offhub_support']==len(Z[k]),'own endpoint response')
    accessible=[k for k,e in enumerate(events) if e['donor_access']];nonzero=[k for k in accessible if Z[k]];families={'all38':list(range(38)),'accessible37':accessible,'accessible_nonzero':nonzero};ranks={};pivots={}
    for name,I in families.items():
        r,p=rank([Z[k] for k in I]);need(r==R['families'][name]['rank'],'author rank '+name);ranks[name]=r;pivots[name]=p
        for v in R['families'][name]['nullspace']:
            out={}
            for k,c in v:axpy(out,Z[k],Q(c))
            need(not out,'literal author nullspace relation')
    need(ranks=={'all38':36,'accessible37':35,'accessible_nonzero':35},'exact ranks')
    zeros=[events[k]['event'] for k,z in enumerate(Z) if not z];need(zeros==[36911,43070],'two exact zero columns')
    inaccessible=[e['event'] for e in events if not e['donor_access']];need(inaccessible==[42662],'one inaccessible slot')
    # Full accessible nonzero independence and precisely two zero columns proves
    # that the complete accessible kernel is their coordinate span.
    need(len(nonzero)==35 and all(k in accessible for k,z in enumerate(Z) if not z),'exact coordinate kernel')
    own=sum(bool(z.get(e['donor']+112,Q(0))) for e,z in zip(events,Z));need(own==17,'own final receiver response count')
    zidx=next(k for k,z in enumerate(Z) if not z);mutant=[dict(z) for z in Z];mutant[zidx][min(off)]=Q(1);need(mutant!=Z,'invented response in zero column rejected')
    eligible={e['event'] for e in events if e['donor_access']};need(42662 not in eligible,'granting inaccessible donor rejected')
    result={'status':'PASS_INDEPENDENT_COMPLETE_SCALAR_UNIT_HELPER_REVIEW','source_sha256':PIN,'author_census_payload_sha256':hashlib.sha256(cb).hexdigest(),'author_response_payload_sha256':hashlib.sha256(rb).hexdigest(),'complete_scalar_unit_departures':38,'distinct_donors':36,'donor_accessible_departures':37,'offhub_output_rows':458,'ranks':ranks,'independent_reverse_pivot_witnesses':pivots,'zero_response_events':zeros,'accessible_kernel_basis_events':zeros,'inaccessible_event':42662,'nonzero_own_final_Y_responses':own,'copy_guard_responses_zero':True,'method':'complete forward1480-variable census plus backward timed payload/endpoint adjoints; no author imports','negative_controls':['invented unit response at a certified zero column rejected','inaccessible event42662 cannot enter the donor-local family'],'scope':'All original public-helper MOVEs with baseline nonzero scalar times one first-X input. Does not classify arbitrary helper payloads, historical receiver decoders, or initial precompensation.','new_complete_kappa':None}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],round(time.monotonic()-started,3),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for s in ('source','census','responses','output'):p.add_argument('--'+s,type=Path,required=True)
    main(p.parse_args())
