#!/usr/bin/env python3
"""Separate dyadic interval and typed macro review; no author imports."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
def need(x,m):
    if not x:raise ValueError(m)
def span(b):
    s={0}
    for v in b:s|={u^v for u in tuple(s)}
    return s
def axpy(a,b,c):
    for k,v in b.items():
        z=a.get(k,F(0))+c*v
        if z:a[k]=z
        else:a.pop(k,None)
def bound(r):
    d=1<<128;n=r**199*d**200;l,h=0,r*d+1
    while h-l>1:
        m=(h+l)//2
        if m**200<=n:l=m
        else:h=m
    need(l**200<=n<(l+1)**200,'directed 200th-power bracket')
    return F(l,d),F(l if l**200==n else l+1,d)
def macro(w,p,ops):
    M=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));q={j:1480+i for i,j in enumerate(M)}
    coupled=[(x,x+112) for i,x in enumerate(w['live']) if i not in w['hosted']['Dports']]
    R={j:{j:F(1)} for j in range(1880)};L=dict(enumerate(w['final']));L.update({q[j]:w['final'][j] for j in M})
    for x,y in coupled:R[q[y]]={q[x]:F(1,2),q[y]:F(1,2)}
    E={j:r.copy() for j,r in R.items()}
    for x,y in coupled:E[q[x]]={q[x]:F(1),q[y]:F(-1)}
    C=list(map(span,w['frames']));counts=Counter();paid=Counter();peak=0
    for e in ops:
        op,j=e[:2];counts[op]+=1
        if op=='INIT':need(j>=1880 and j not in L,'new owned lifetime');L[j]=e[2];R[j]={}
        elif op=='CLEAR':need(j>=1880 and L.get(j)==e[2],'owned retirement');del L[j];del R[j]
        elif op=='ADD':
            need(j!=e[2] and L.get(j)==L.get(e[2])==e[4],'live distinct cochart ADD');axpy(R[j],R[e[2]],F(e[3]))
        elif op=='SCALE':need(L.get(j)==e[3] and F(e[2])!=0,'typed SCALE');R[j]={k:F(e[2])*v for k,v in R[j].items()}
        elif op=='MOVE':
            need(type(e[4]) is bool and e[4] and j>=1880 and L.get(j)==e[2],'owned route');need(C[e[2]]<C[e[3]],'strict ascent');paid[len(w['frames'][e[3]])-len(w['frames'][e[2]])]+=1;L[j]=e[3]
        else:raise ValueError('opcode')
        peak=max(peak,len(L)-1880)
    need(R==E and len(L)==1880,'all1880 independent coefficient rows and cleanup')
    need(paid=={1:8} and peak==1,'eight rank1 and peak1')
    need(counts=={'INIT':8,'ADD':16,'MOVE':8,'SCALE':8,'CLEAR':8},'full macro census')
    return {'rows':1880,'coupled_pairs':coupled,'counts':dict(counts),'paid':dict(paid),'peak_owned':peak}
def main(a):
    rb=a.source.read_bytes();ib=a.invoice.read_bytes();need(hashlib.sha256(rb).hexdigest()==PIN,'source');need(hashlib.sha256(ib).hexdigest()==IPIN,'invoice');w=json.loads(gzip.decompress(rb));I=json.loads(ib);author=json.loads(a.author.read_text());T={int(r):n for r,n in I['T4'].items()};P={int(r):n for r,n in I['P4'].items()}
    B={r:bound(r) for r in set(T)|set(P)|set(range(1,10))};out={}
    for name,h in [('H4_no_second_owned',{}),('eight_rank9_packets',{9:8}),('eight_packets_and_reverse_eight',{9:8,1:8}),('two_independent_eight_packet_trips_and_reverse_eight',{9:16,1:8})]:
        Q=Counter(P);Q.update({r:18*n for r,n in h.items()});lo=hi=F(0)
        for r in B:
            c=T.get(r,0)-Q.get(r,0);lo+=c*B[r][0 if c>=0 else 1];hi+=c*B[r][1 if c>=0 else 0]
        ap=author['profiles'][name];need(Q=={int(r):n for r,n in ap['paid_histogram'].items()},'all18 repetitions per bin')
        al,ah=[F(int(x),int(ap['margin_denominator'])) for x in ap['margin_numerator_bounds']];need(al<=lo<=hi<=ah,'independent interval inside author bracket')
        need(sum(Q.values())==ap['paid_count'] and sum(T.values())==ap['target_count'],'caller counts')
        need(sum(r*(T.get(r,0)-Q.get(r,0)) for r in B)==ap['rank_surplus'],'signed rank surplus')
        for r,k in ap['max_further_uniform_rank_calls'].items():
            if k is None:need(hi<0,'negative margin')
            else:need(lo-18*k*B[int(r)][1]>0 and hi-18*(k+1)*B[int(r)][0]<0,'strict sharp integral ceiling')
        out[name]={'headroom_interval':list(map(str,(lo/18,hi/18))),'paid_count':sum(Q.values()),'rank_surplus':ap['rank_surplus']}
    eight=tuple(F(v) for v in out['eight_rank9_packets']['headroom_interval']);need(eight[1]<35,'at least35 new calls violates prefix allowance')
    need(9**199>8**200,'simple independent rank9 comparison')
    pb=a.macro.read_bytes();p=json.loads(gzip.decompress(pb));m=macro(w,p,p['program']);bad=[e.copy() for e in p['program']];at=next(i for i,e in enumerate(bad) if e[0]=='ADD' and e[3]=='-2');bad[at][3]='-1'
    try:macro(w,p,bad)
    except ValueError:pass
    else:raise ValueError('wrong reverse coefficient accepted')
    R={'status':'PASS_INDEPENDENT_DYADIC_PACKET_INVOICE_AND_REVERSE_MACRO','source_sha256':PIN,'invoice_sha256':IPIN,'grid':'2^128','profiles':out,'reverse_macro':m,'macro_payload_sha256':hashlib.sha256(gzip.decompress(pb)).hexdigest(),'controls':['wrong reverse coefficient rejected','eight rank9 plus35 rank1 strictly exceeds H4','next integer at every rank cutoff rejected'],'scope':'Conditional H4 invoice and entry-contracted reverse macro; no residual provider, full supplier or new kappa.'};a.output.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(R['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--invoice',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--macro',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
