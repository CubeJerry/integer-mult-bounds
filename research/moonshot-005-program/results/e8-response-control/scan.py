#!/usr/bin/env python3
"""Exact all-time station controllability screen for one prescribed E8 response."""
import argparse,gzip,hashlib,json,time
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
    if not x:raise ValueError(m)
def add(a,b,c=F(1)):
    for j,v in b.items():
        z=a.get(j,F(0))+c*v
        if z:a[j]=z
        else:a.pop(j,None)
def span(f):
    s={0}
    for b in f:s|={x^b for x in tuple(s)}
    return frozenset(s)
def root(v):
    S=[j for j in range(9) if v>>j&1]
    if len(S)==3:
        return [2*int(j in S) for j in range(8)] if 8 in S else [1 if j in S else -1 for j in range(8)]
    T=[j for j in range(9) if j not in S];need(len(T)==2,'root domain')
    if 8 in T:return [1 if j==T[0] else -1 for j in range(8)]
    return [2*int(j==T[0])-2*int(j==T[1]) for j in range(8)]
def main(a):
    started=time.monotonic();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'pin');w=json.loads(gzip.decompress(raw));P=w['program'];n=w['public'];C=list(map(span,w['frames']));donor=a.donor
    stations=[w['initial'][donor]]+[e[3] for e in P if e[:2]==['MOVE',donor]];space={C[x] for x in stations};off=[j for j in range(n) if C[w['final'][j]]!=C[127]]
    R={j:({j:F(1)} if j in off else {}) for j in range(n)};loc=dict(enumerate(w['final']));basis=[];records=[];seen=set();candidate_count=0
    def collect(j,cut):
        nonlocal candidate_count
        if j not in loc or C[loc[j]] not in space or not R[j]:return
        key=tuple(sorted(R[j].items()))
        if key in seen:return
        seen.add(key);candidate_count+=1;r=dict(R[j]);elim=[]
        for k,(p,b) in enumerate(basis):
            c=r.get(p,F(0))
            if c:add(r,b,-c);elim.append([k,c])
        if r:
            p=min(r);v=r[p];basis.append((p,{k:c/v for k,c in r.items()}));records.append(dict(cut=cut,role=j,chart=loc[j],pivot=p,scale=str(v),eliminated=[[k,str(c)] for k,c in elim]))
    for j in loc:collect(j,len(P))
    for t in range(len(P)-1,-1,-1):
        e=P[t];op,j=e[:2];changed=[]
        if op=='ADD':s=e[2];add(R[s],R[j],F(e[3]));changed=[s]
        elif op=='SCALE':R[j]={k:F(e[2])*c for k,c in R[j].items()};changed=[j]
        elif op=='COPY':s=e[2];add(R[s],R[j],F(e[3]));R[j]={n:F(1)};changed=[s,j]
        elif op=='MOVE':loc[j]=e[2];changed=[j]
        elif op=='CLEAR':loc[j]=e[2];R[j]={};changed=[j]
        elif op=='INIT':del loc[j];del R[j]
        else:raise ValueError(op)
        for j in changed:collect(j,t)
    k=w['live'].index(donor);A=[root(v) for v in w['ports']];target={}
    for i,x in enumerate(w['live']):
        c=F(sum(u*v for u,v in zip(A[i],A[k])),8)*(1 if i in w['hosted']['Dports'] else F(1,2))
        if c:target[x+112]=c
    residual=dict(target);beta=[F(0) for _ in basis]
    for i,(p,b) in enumerate(basis):
        c=residual.get(p,F(0))
        if c:add(residual,b,-c);beta[i]=c
    dual={}
    if residual:
        dual={min(residual):F(1)}
        for pivot,row in reversed(basis):
            v=sum((dual.get(j,F(0))*c for j,c in row.items()),F(0))
            if v:add(dual,{pivot:F(1)},-v)
        need(all(not sum((dual.get(j,F(0))*c for j,c in row.items()),F(0)) for pivot,row in basis),'dual annihilates basis')
        need(sum((dual.get(j,F(0))*c for j,c in target.items()),F(0))!=0,'dual separates target')
    controls=[]
    if not residual:
        for i in range(len(records)-1,-1,-1):
            c=beta[i]/F(records[i]['scale'])
            if c:
                controls.append({k:v for k,v in records[i].items() if k in ('cut','role','chart')}|{'coefficient':str(c)})
                for j,v in records[i]['eliminated']:beta[j]-=c*F(v)
        controls.sort(key=lambda r:(r['cut'],r['role']))
    out=dict(schema='e8-column-all-time-station-control-screen-v1',source_sha256=PIN,donor=donor,stations=stations,offhub_dimension=len(off),guard_coordinates=1,distinct_candidate_columns=candidate_count,reachable_rank=len(basis),target=[[j,str(c)] for j,c in sorted(target.items())],target_reachable=not residual,residual=[[j,str(c)] for j,c in sorted(residual.items())],controls=controls,dual=[[j,str(c)] for j,c in sorted(dual.items())],dual_target_pairing=str(sum((dual.get(j,F(0))*c for j,c in target.items()),F(0))),basis_records=records,seconds=time.monotonic()-started,status='Exact algebraic screen; physical compiler and independent review pending.')
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('target','controls','basis_records','residual')},indent=2));print('residual',out['residual'][:10],'controls',len(controls))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--donor',type=int,default=77);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
