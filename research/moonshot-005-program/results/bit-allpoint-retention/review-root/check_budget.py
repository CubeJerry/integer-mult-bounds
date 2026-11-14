#!/usr/bin/env python3
"""Independent dyadic budget from the admitted caller and actual coalesced word."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def main(a):
    raw=a.caller.read_bytes();need(hashlib.sha256(raw).hexdigest()=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','admitted caller pin');c=json.loads(raw)
    N,H,P,T=({int(r):F(v) for r,v in c[k].items()} for k in ['native_paid','helper_target','paired_paid','paired_target'])
    def combine(*terms):
        out=Counter()
        for s,d in terms:
            for r,v in d.items():out[r]+=s*v
        return {r:v for r,v in out.items() if v}
    S=combine((F(1,36),T),(F(-1,36),P));limit=combine((1,N),(-1,H),(1,S))
    b=(a.word).read_bytes();w=json.loads(gzip.decompress(b));paid=Counter(abs(w['frames'][str(o[3])]['dim']-w['frames'][str(o[2])]['dim']) for o in w['program'] if o[0]=='MOVE');Q=combine((1,paid),(48,{1:1}))
    need(Q=={1:853,2:15,3:84,4:84,5:15,6:4,7:8},'actual coalesced closed prefix plus six full unit paths')
    scale=1<<144;powers={}
    def power(r):
        if r not in powers:
            n=r**199*scale**200;l,h=0,r*scale+1
            while h-l>1:
                m=(h+l)//2
                if m**200<=n:l=m
                else:h=m
            need(l**200<=n<h**200,'independent dyadic enclosure');powers[r]=(F(l,scale),F(h,scale))
        return powers[r]
    def val(d):
        lo=hi=F(0)
        for r,v in d.items():
            l,h=power(r);lo+=v*(l if v>0 else h);hi+=v*(h if v>0 else l)
        return lo,hi
    inf=val(combine((1,limit),(-1,Q)));finite={m:val(combine((1,limit),(-1,Q),(F(1,m-1),S))) for m in range(2,18,2)}
    need(0<inf[0]<inf[1]<1 and finite[14][1]<0<finite[16][0],'sharp stated first even threshold and less-than-one unit slack')
    need(val(S)[1]<0,'allowance strictly increases with fixed multiplicity')
    native_raw=a.native.read_bytes();need(hashlib.sha256(native_raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native invoice pin');n=json.loads(gzip.decompress(native_raw));counts=Counter(o[0] for o in n['program']);live=peak=0
    for o in n['program']:
        if o[0]=='INIT':live+=1;peak=max(peak,live)
        elif o[0]=='CLEAR':live-=1
    need(counts=={'INIT':237,'ADD':30789,'SWAP':3,'MOVE':2871,'CLEAR':237} and live==0 and peak==237,'full native ordinary ledger including three SWAPs')
    aa=json.loads(a.author.read_text())['conditional_profiles']['coalesced_X_unit_Y_packet_q9'];al,ah=F(aa['limiting_margin']['lower_rational']),F(aa['limiting_margin']['upper_rational']);need(al<=inf[0]<inf[1]<=ah,'distinct tighter independent enclosure within author range')
    out=dict(status='PASS_INDEPENDENT_CONDITIONAL_POINT_PREFIX_BUDGET',coalesced_word_sha256=hashlib.sha256(b).hexdigest(),dyadic_bits=144,profile=Q,limiting_margin=list(map(str,inf)),first_even_m_if_no_new_moves_or_X_stops=16,fixed_even_margins={str(m):list(map(str,p)) for m,p in finite.items()},native_ordinary_counts=dict(counts),native_peak=peak,shared_ordinary_count_scope='For the declared shared linear conjugation:222 input and222 output ADDs per private rail; native3SWAPs and all native instructions retained. Does not certify a missing completed Q or compiler.',scope='Only conditional movement screening; six future packet paths carry no constructed decoder. All source/read/erasure/ordinary/physical contracts remain.',new_kappa=None)
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'limiting_margin':float(inf[0]),'first_even_m':16}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ['native','caller','word','author','output']:p.add_argument('--'+k,type=Path,required=True)
    main(p.parse_args())
