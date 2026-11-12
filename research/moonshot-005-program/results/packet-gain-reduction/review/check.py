#!/usr/bin/env python3
"""Independent exact controls for packet/private/history decoding criteria."""
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as Q
def need(x,s):
    if not x:raise ValueError(s)
def M(a):return [[Q(v) for v in r] for r in a]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def rank(a):
    if not a:return 0
    a=[r[:] for r in a];r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
def inrow(v,a):return rank(a)==rank(a+[v])
def main(a):
    sources=json.loads((a.author/'SOURCES.json').read_text());pins={}
    for rel,h in sources['files_sha256'].items():
        p=a.author/rel if rel=='PROOF.md' else a.programme/rel
        need(hashlib.sha256(p.read_bytes()).hexdigest()==h,'admitted dependency '+rel);pins[rel]=h
    O=M([[1],[1]]);N=M([[1,-1]]);R=M([[0,0],[0,1]]);D0=M([[1,0]]);C=M([[1,1]]);e=M([[1,0]])[0]
    need(mm(N,O)==M([[0]]) and mm(D0,O)==M([[1]]),'baseline/null identities')
    NR=mm(N,R);need(not inrow(e,C) and inrow(e,C+NR),'foreign history gain changes exact criterion')
    u=Q(7);q1=Q(3);q2=Q(5);y1=u;y2=u+q2;p=q1+q2
    need(2*y1-y2+p==u+q1,'foreign-control decoder')
    need(R[0][0]==R[1][0]==0 and NR[0][1]!=0,'target-column annihilation does not annihilate all history gain')
    # Modified initial observation must be retained: initial=u189+q,
    # final=u77+u189 restored, hence endpoint-minus-initial=u77-q.
    u77=Q(7);u189=Q(11);q=Q(3);initial=u189+q;final=u77+u189;hist=final-initial
    need(hist==u77-q and hist+2*q==u77+q and hist+q!=u77+q,'corrected initial observation')
    # A nonzero q-response can still be wholly masked by common input.
    O3=M([[0,1,0],[1,1,0],[0,0,1]]);B=M([[0],[0],[1]]);v=M([[0],[0],[1]]);D3=M([[-1,1,0]])
    need(mm(O3,v)==B and mm(D3,B)==M([[0]]),'full-record indistinguishability with restored endpoint')
    h=mm(D3,O3);need(mm(h,v)==M([[0]]),'same-record target common displacement zero')
    # A missing endpoint-restoration condition permits direct desired gain.
    badB=M([[0],[1],[0]]);need(mm(D3,badB)==M([[1]]),'nonrestored endpoint breaks no-gain conclusion')
    out={'status':'PASS_INDEPENDENT_PACKET_GAIN_ALGEBRA_AND_PINS','dependency_pins':pins,'source_reproduction':'Inherited admitted source certificates; hashes checked, not reexecuted in this derived review.','negative_controls':['foreign q2 history gain plus q1+q2 packet reveals q1 despite zero q1 gain column','modified initial189 observation changes stable decoder by minus its precompensation','nonzero history response can be common-input masked','dropping endpoint restoration permits target gain without packets'],'general_criterion':'e-D0R in row(C,S,NR)','source_specialization':'All220-station control columns satisfy NB=0; with restored stable endpoint this reduces to e in row(C,S).','new_complete_kappa':None}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for s in ('author','programme','output'):p.add_argument('--'+s,type=Path,required=True)
    main(p.parse_args())
