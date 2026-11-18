#!/usr/bin/env python3
"""Construct every physical original field route of the 24-lane balanced source."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip,json,struct
from balance import verify
from layout import need

def build(w,factor,out=None):
    checks=verify(w,factor);u=dict(factor['factors']);b=checks['paid_GF_copies'];need(b==5760,'frozen factor dilation')
    B=[tuple(i for i in h if i<111) for h in w['A2']];P=w['dual_D4'];flags=[set() for d in P]
    for _,d,h,*_ in w['routes']:
        if h is not None:flags[d].add(h)
    left=[]
    for d,hs in enumerate(flags):
        ents=[[],[]]
        for h in sorted(hs):
            js=B[h];m=len(js);x=12//m+u.get(h,0) if m else 0;e=max(8,x)
            for j in js:
                ents[0].extend([(h,j)]*x);ents[1].extend([(h,j)]*(e-x))
            ents[1].extend([(h,-1)]*(24-m*e))
        need(len(ents[0])+len(ents[1])==384,'full flag array');left.append(ents)
    count=Counter();moves=Counter();src=Counter();dst=Counter();digest=sha256();store=bytearray();f=out.open('wb') if out else None
    def route(kind,d,left_flag,right_flag):
        h,j=left_flag;k,i=right_flag
        if kind==0:role=j;index=src[j];src[j]+=1
        else:role=i;index=dst[i];dst[i]+=1
        need(0<=role<111,'actual public native holder')
        # The file order is public. Counts for source and receiver independently assign IDs.
        store.extend(struct.pack('<BHHHhhhh',kind,role,index,d,h,j,k,i))
        if len(store)>=1<<16:
            digest.update(store)
            if f:f.write(store)
            store.clear()
        ranks=[1] if kind==0 else [0]
        if h>=0:
            if kind==1 and j>=0:ranks.append(1)
            ranks.append(2)
        ranks.append(4)
        if k>=0:
            ranks.append(6)
            if i>=0:ranks.append(7)
        if kind==0:ranks.append(8)
        for t,v in zip(ranks,ranks[1:]):need(t<v,'nested rank move');moves[v-t]+=1
        count[kind,'short' if h<0 else 'pad' if j<0 else 'real','short' if k<0 else 'pad' if i<0 else 'real']+=1
    blank=(-1,-1)
    for d in range(len(P)):
        lx,ly=left[d];ry,rx=left[P[d]];need(len(ly)<=len(ry) and len(rx)<=len(lx),'genuine local FIFO pairings')
        for l,r in zip(ly,ry):route(1,d,l,r)
        for l,r in zip(lx,rx):route(0,d,l,r)
        for l,r in zip(lx[len(rx):],ry[len(ly):]):route(0,d,l,blank);route(1,d,blank,r)
    if store:
        digest.update(store)
        if f:f.write(store)
    if f:f.close()
    need(len(src)==len(dst)==111 and set(src.values())==set(dst.values())=={b},'all actual originals used exactly once')
    moves[8]+=9*b;mp={k:Fraction(v,b) for k,v in sorted(moves.items())}
    need(mp=={1:Fraction(4451,8),2:Fraction(7213,16),4:24,8:9},'exact public movement profile')
    return {'status':'PASS_BALANCED_1278720_REAL_ROUTES','paid_GF_copies':b,'paid_binary_copies_at_GF_2_29':29*b,
            'packed_layout_format':'little endian <BHHHhhhh: 0=X or 1=Y, role, within_role, D, H, j, K, i; negative labels are missing',
            'route_sha256':digest.hexdigest(),'native_each_role_per_kind':b,'actual_field_routes':sum(count.values()),
            'route_census':[[*k,v] for k,v in sorted(count.items())],'GF_move_counts':dict(sorted(moves.items())),
            'normalized_movement_profile':{k:str(v) for k,v in mp.items()},'all_canonical_descents':9*b,'gate':'geometry only; matrices by existence theorem'}

if __name__=='__main__':
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--factor',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--word',type=Path);a=ap.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    data=build(json.loads(raw),json.loads(a.factor.read_bytes()),a.word);data['factor_sha256']=sha256(a.factor.read_bytes()).hexdigest()
    a.out.write_text(json.dumps(data,indent=2)+'\n');print(data['status'],data['route_sha256'],data['normalized_movement_profile'])
