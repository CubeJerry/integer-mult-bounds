#!/usr/bin/env python3
"""Independent set-valued replay and finite premises for the two cut theorems."""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
NATIVE='research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'

def need(c,m):
    if not c:raise ValueError(m)

def dot(a,b):return sum(Fraction(x)*Fraction(y) for x,y in zip(a,b))

def binary_rank(rows):
    piv={}
    for r in rows:
        while r:
            j=r.bit_length()-1
            if j in piv:r^=piv[j]
            else:piv[j]=r;break
    return len(piv)

def qrank(rows):
    a=[list(map(Fraction,r)) for r in rows];at=0
    for c in range(len(a[0]) if a else 0):
        j=next((j for j in range(at,len(a)) if a[j][c]),None)
        if j is None:continue
        a[at],a[j]=a[j],a[at];v=a[at][c];a[at]=[x/v for x in a[at]]
        for j in range(at+1,len(a)):
            v=a[j][c]
            if v:a[j]=[x-v*y for x,y in zip(a[j],a[at])]
        at+=1
    return at

def replay(word,program):
    live={i:(chart,{i}) for i,chart in enumerate(word['start'])}
    ever=set(live);counts=Counter();moves=Counter()
    for op in program:
        kind,r=op[:2];counts[kind]+=1
        if kind=='INIT':
            need(r>=222 and r not in ever,'fresh owned initialization')
            ever.add(r);live[r]=(op[2],set())
        elif kind=='ADD':
            _,r,s,chart=op
            need(r!=s and live[r][0]==live[s][0]==chart,'same-chart addition')
            live[r]=(chart,live[r][1]^live[s][1])
        elif kind=='MOVE':
            _,r,a,b=op;need(live[r][0]==a,'move starts at actual chart')
            aa,bb=word['frames'][str(a)],word['frames'][str(b)]
            delta=bb['dim']-aa['dim'];need(delta!=0,'strict-rank move')
            small,large=(aa,bb) if delta>0 else (bb,aa)
            need(all(dot(x,y)==0 for x in small['B'] for y in large['A']),'exact real containment')
            need(delta>0 if r<222 else (r in (334,335) and delta<0),'source monotonicity interface')
            moves[abs(delta)]+=1;live[r]=(b,live[r][1])
        elif kind=='CLEAR':
            need(r>=222 and live[r][0]==op[2],'owned clear at actual chart')
            del live[r]
        else:raise ValueError(kind)
    return live,counts,moves

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=(a.repo/NATIVE).read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');native=json.loads(gzip.decompress(raw))
    word_raw=a.prefix.read_bytes();word=json.loads(gzip.decompress(word_raw))
    need(word['start']==native['start'][:222] and word['public']==222,'original input interface')
    for key,frame in native['frames'].items():need(word['frames'][key]==frame,'native chart unchanged')
    for key,frame in word['frames'].items():
        if key in native['frames']:continue
        need(qrank(frame['B'])==frame['dim'] and qrank(frame['A'])==8-frame['dim'],'new frame ranks')
        need(all(dot(x,y)==0 for x in frame['B'] for y in frame['A']),'new frame annihilator')
    R=[native['frames'][str(native['start'][i])]['B'][0] for i in range(111)]
    K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(R)) for i,r in enumerate(R)]
    as_set=lambda x:{j for j in range(111) if x>>j&1}
    live,counts,moves=replay(word,word['program'])
    need(set(live)==set(range(335)),'actual retained ownership')
    for i in range(111):
        need(live[i]==(native['final'][i],{i}),'original X restored')
        need(live[222+i]==(native['start'][i],{i}),'genuine point copy')
        need(live[111+i]==(native['final'][111+i] if i==92 else native['start'][111+i],{111+i,i} if i==92 else {111+i}),'original Y state')
    ground=native['start'][111];C=live[333][0]
    need(live[333][1]==as_set(K[92]),'pure canonical cache')
    need(live[334]==(ground,as_set(K[92]&K[54])),'pure ground quadratic')
    need(counts==Counter(INIT=114,ADD=234,MOVE=174,CLEAR=1),'independent prefix counts')
    need(moves==Counter({1:29,2:32,5:32,6:27,7:54}),'independent prefix move profile')
    contains_cache=[i for i in range(111) if all(dot(b,R[i])==0 for b in word['frames'][str(C)]['B'])]
    need(contains_cache==[54,84,92],'exact cache-to-facet access')
    need(K[92]^K[54]^K[84]==(1<<111)-1,'canonical A2 partition')

    # Independent frame, different from the author's chosen coordinate frame.
    frame=[2,8,9,14,15,60,92,93]
    need(all(dot(R[i],R[j])!=0 for i,j in itertools.combinations(frame,2)),'independent eight-frame')
    labels=[]
    for row in K:
        w=sum(((row>>j)&1)<<c for c,j in enumerate(frame))
        labels.append(w^(255 if w.bit_count()%2==0 else 0))
    q=lambda v:v.bit_count()*(v.bit_count()+1)//2%2
    bil=lambda u,v:((u&v).bit_count()+u.bit_count()*v.bit_count())%2
    need(len(set(labels))==111 and all(q(v)==1 for v in labels),'source quadric with independent frame')
    need(all((1^bil(labels[i],labels[j]))==(K[i]>>j&1) for i in range(111) for j in range(111)),'all source polar pairings')
    need(labels[92]^labels[54]==labels[84],'independent A2 label identity')

    def cut(state,S):
        O=[]
        for chart,values in state.values():
            if any(all(dot(b,R[t])==0 for b in word['frames'][str(chart)]['B']) for t in S):
                O.append(sum(1<<j for j in values))
        T=[(1<<t)|(1<<(111+t)) for t in S]
        d=binary_rank(O+T)-binary_rank(O)
        return dict(receivers=S,observation_rank=binary_rank(O),target_augmented_rank=binary_rank(O+T),deficit=d)
    S7=[2,8,9,14,15,60,93];old8=[2,8,14,21,46,48,81,84]
    cuts=[cut(live,S7),cut(live,old8)];need(all(c['deficit']==7 for c in cuts),'matching seven cuts')
    old,_,_=replay(word,word['program'][:-5]);negative=cut(old,old8);need(negative['deficit']==8,'without purification the old eight cut remains')

    certpath=a.repo/'research/moonshot-005-program/results/bit-minimum-rank-nine/CERTIFICATE.json'
    cert=json.loads(certpath.read_text());frames=cert['frames_pairwise_REAL_NONorthogonal'];freq=Counter(i for F in frames for i in F);roles=sorted(freq)
    need(len(frames)==9 and len(roles)==26 and all(n%2==0 for n in freq.values()),'odd-frame even-incidence witness')
    need(not(set(roles)&{54,84,92}),'witness avoids all cache-access facets')
    need(all(len(set(F))==8 and all(dot(R[i],R[j])!=0 for i,j in itertools.combinations(F,2)) for F in frames),'all witness frames exact real nonorthogonality')
    need(all(not all(dot(b,R[t])==0 for b in word['frames'][str(C)]['B']) for t in roles),'no witness receiver gets cache for free')
    out=dict(status='PASS_INDEPENDENT_PURIFIED_PIVOT_CUT_REVIEW',source_sha256=PIN,prefix_sha256=hashlib.sha256(word_raw).hexdigest(),parity_certificate_sha256=hashlib.sha256(certpath.read_bytes()).hexdigest(),prefix_counts=dict(counts),prefix_move_profile=dict(moves),cache_access_facets=contains_cache,independent_quadric_basis=frame,cuts=cuts,negative_without_purification=negative,witness_roles=roles,witness_multiplicity_histogram=dict(Counter(freq.values())),all_union_deficit=7,future_downward_capacity_lower_bound='8V',proof='REVIEW.md',new_complete_kappa=False)
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('witness_roles','cuts','negative_without_purification')}))

if __name__=='__main__':main()
