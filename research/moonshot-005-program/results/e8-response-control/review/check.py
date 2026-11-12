#!/usr/bin/env python3
"""Independent direct three-output adjoint for the donor77 Gram target."""
import argparse,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,s):
    if not x:raise ValueError(s)
def span(f):
    s={0}
    for x in f:s|={y^x for y in s}
    return frozenset(s)
def add(a,j,c):
    v=a.get(j,Q(0))+c
    if v:a[j]=v
    else:a.pop(j,None)
def root9(v):
    S=[j for j in range(9) if v>>j&1]
    if len(S)==3:return [Q(int(j in S))-Q(1,3) for j in range(9)]
    missing=[j for j in range(9) if j not in S];need(len(S)==7 and len(missing)==2,'source root domain');return [Q(int(j==missing[0])-int(j==missing[1])) for j in range(9)]
def main(a):
    raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));P=w['program'];F=list(map(span,w['frames']));n=w['public'];claim=json.loads(a.screen.read_text());need(claim['source_sha256']==PIN and claim['donor']==77,'claimed source/donor')
    stations={F[w['initial'][77]]}|{F[e[3]] for e in P if e[:2]==['MOVE',77]};need(len(stations)==5,'source station count')
    need(stations=={F[c] for c in claim['stations']},'station identity')
    dual={113:Q(1),116:Q(-1),119:Q(1)};need([[j,str(v)] for j,v in sorted(dual.items())]==claim['dual'],'literal three-output dual')
    roots=[root9(v) for v in w['ports']];k=w['live'].index(77);target={}
    for i,x in enumerate(w['live']):
        c=sum(u*v for u,v in zip(roots[i],roots[k]))/2
        c*=Q(1) if i in w['hosted']['Dports'] else Q(1,2)
        if c:target[x+112]=c
    need([[j,str(v)] for j,v in sorted(target.items())]==claim['target'],'independent nine-dimensional Gram target')
    pairing=sum(c*target.get(j,Q(0)) for j,c in dual.items());need(pairing==Q(1,2),'target separation')
    need([target.get(j,Q(0)) for j in (113,116,119)]==[Q(0),Q(0),Q(1,2)],'single support entry on separating triple')
    loc={j:F[f] for j,f in enumerate(w['final'])};good=dict(dual);mutant={113:Q(1),119:Q(1)};badcut=None;checked=0;nonzeros=0;largest=0
    def inspect(cut):
        nonlocal checked,nonzeros,largest,badcut
        checked+=1;nonzeros+=len(good);largest=max(largest,len(good))
        for j,c in good.items():need(j in loc and loc[j] not in stations,'nonzero allowed station adjoint '+str((cut,j,c)))
        if badcut is None:
            for j,c in mutant.items():
                if loc[j] in stations:badcut={'cut':cut,'role':j,'coefficient':str(c)};break
    inspect(len(P))
    for t in range(len(P)-1,-1,-1):
        e=P[t];op,j=e[:2]
        for r in (good,mutant):
            if op=='ADD':add(r,e[2],Q(e[3])*r.get(j,Q(0)))
            elif op=='SCALE':
                v=Q(e[2])*r.get(j,Q(0));r.pop(j,None)
                if v:r[j]=v
            elif op=='COPY':v=r.pop(j,Q(0));add(r,e[2],Q(e[3])*v)
            elif op in ('INIT','CLEAR'):r.pop(j,None)
        if op=='MOVE':need(loc[j]==F[e[3]],'reverse MOVE target');loc[j]=F[e[2]]
        elif op=='CLEAR':need(j>=n and j not in loc,'reverse CLEAR');loc[j]=F[e[2]]
        elif op=='INIT':need(j>=n and loc[j]==F[e[2]],'reverse INIT');del loc[j]
        inspect(t)
    need(loc=={j:F[f] for j,f in enumerate(w['initial'])},'full source lifecycle')
    need(checked==len(P)+1==71262 and badcut is not None,'complete cut count and coefficient mutant')
    need(F[w['final'][119]] not in stations and dual[119]==1,'extra endpoint station negative control')
    result={'status':'PASS_INDEPENDENT_ALL_CUT_GRAM_TARGET_DUAL','source_sha256':PIN,'author_screen_sha256':hashlib.sha256(a.screen.read_bytes()).hexdigest(),'donor':77,'station_count':5,'cuts_checked':checked,'nonzero_adjoint_entries_examined':nonzeros,'maximum_adjoint_support':largest,'dual':[[j,str(v)] for j,v in sorted(dual.items())],'target_pairing':str(pairing),'target_on_separating_triple':['0','0','1/2'],'nonzero_row_column_rescaling_pairing':'row_scale119 * column_scale77 / 2','guard_relaxation':'No COPY guard constraint used: dual annihilates every station control even without imposing the guard.','method':'one three-output scalar adjoint checked at every source cut and every nonzero coordinate; target independently built in nine dimensions','negative_controls':{'omit_negative116_term':badcut,'extra_final119_station':{'chart':w['final'][119],'role':119,'adjoint':'1'}},'scope':'Fixed native word; arbitrary additions to existing public or owned fields at the five donor77 funded-route charts, at any source cut. Prescribed Gram column target only; no general low-rank correction-code impossibility.','new_complete_kappa':None}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],checked,nonzeros)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for s in ('source','screen','output'):p.add_argument('--'+s,type=Path,required=True)
    main(p.parse_args())
