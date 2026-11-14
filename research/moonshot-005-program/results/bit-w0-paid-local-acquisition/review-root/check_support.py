#!/usr/bin/env python3
"""Independent ambient-coordinate E7 support-cover reconstruction."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import deque
from math import gcd,lcm
import argparse,gzip,hashlib,json
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(x,s):
    if not x:raise ValueError(s)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def primitive(v):
    v=tuple(F(x) for x in v);d=lcm(*(x.denominator for x in v));w=[int(x*d) for x in v]
    g=gcd(*w);need(g!=0,'nonzero line');sgn=1 if next(x for x in w if x)>0 else -1
    return tuple(sgn*x//g for x in w)
def solve(a,b):
    n=len(a);m=[[F(x) for x in r]+[F(t)] for r,t in zip(a,b)]
    for j in range(n):
        q=next(i for i in range(j,n) if m[i][j]);m[j],m[q]=m[q],m[j];v=m[j][j];m[j]=[x/v for x in m[j]]
        for i in range(n):
            if i!=j:
                v=m[i][j];m[i]=[x-v*y for x,y in zip(m[i],m[j])]
    return tuple(m[i][-1] for i in range(n))
def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');s=json.loads(gzip.decompress(raw));actual=[]
    for i in range(111):
        v=[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]];n=dot(v,v);need(n in (1,4),'norm')
        actual.append(tuple(int(x*(2 if n==1 else 1)) for x in v))
    supports={tuple(i for i,x in enumerate(v) if x) for v in actual if sum(bool(x) for x in v)==4}
    full={tuple(2*int(i==j) for i in range(8)) for j in range(8)}
    for t in supports:
        for signs in product([-1,1],repeat=3):
            v=[0]*8;v[t[0]]=1
            for i,c in zip(t[1:],signs):v[i]=c
            full.add(tuple(v))
    need(len(full)==120 and set(actual)<=full,'120 root completion')
    for u in full:
        for v in full:
            q=dot(u,v);need(q%2==0,'Cartan integrality');w=tuple(v[i]-(q//2)*u[i] for i in range(8));w=w if next(x for x in w if x)>0 else tuple(-x for x in w)
            need(w in full,'reflection closure')
    roots=sorted(v[1:] for v in full if v[0]==0);need(len(roots)==63,'63 facet roots')
    generic=[2**i for i in range(7)];need(all(dot(r,generic) for r in roots),'generic orientation')
    pos={r if dot(r,generic)>0 else tuple(-x for x in r) for r in roots}
    sums={tuple(x+y for x,y in zip(r,t)) for r in pos for t in pos};simple=sorted(pos-sums);need(len(simple)==7,'seven simples')
    trans=list(map(list,zip(*simple)))
    for r in pos:
        c=solve(trans,r);need(all(x.denominator==1 and x>=0 for x in c),'positive simple expansion')
    masks=set();orbits=[]
    for k in range(7):
        w=primitive(solve(simple,[2*int(i==k) for i in range(7)]));seen={w};q=deque([w])
        while q:
            v=q.popleft()
            for r in simple:
                t=primitive(tuple(2*x-dot(v,r)*y for x,y in zip(v,r)))
                if t not in seen:seen.add(t);q.append(t)
        local={sum(1<<i for i,r in enumerate(roots) if dot(v,r)==0) for v in seen}
        need(len(local)==len(seen) and not(local&masks),'distinct root hyperplanes');masks|=local;orbits.append(len(seen))
    need(sorted(orbits)==sorted([378,5040,63,1008,288,2016,28]) and len(masks)==8821,'complete parabolic families')
    results=[]
    for c in range(8):
        moved=[]
        for r in actual:
            v=tuple(r[j^c] for j in range(8));moved.append(v if next(x for x in v if x)>0 else tuple(-x for x in v))
        selected=[i for i in range(8,111) if moved[i][0]==0]
        target=sum(1<<roots.index(moved[i][1:]) for i in selected)
        restricted=sorted({m&target for m in masks});counts=[m.bit_count() for m in restricted]
        best=0;witness=None;pairs=0
        for i,x in enumerate(restricted):
            for j in range(i,len(restricted)):
                if counts[i]+counts[j]<=best:continue
                y=restricted[j];v=(x|y).bit_count();pairs+=1
                if v>best:best=v;witness=[hex(x),hex(y)]
        results.append({'coordinate':c,'support_size':len(selected),'single':max(counts),'pair':best,'distinct_restrictions':len(restricted),'evaluated_pairs':pairs,'witness':witness})
    need([r['pair'] for r in results]==[44,47,47,45,45,45,45,47],'eight exact pair maxima')
    out={'status':'PASS_INDEPENDENT_AMBIENT_LOCAL_SUPPORT','native_sha256':PIN,'normal_orbits':orbits,'parabolic_masks':len(masks),'coordinate_forms':results,'method':'Fresh ambient primitive normal reflections; generic2 orientation; arbitrary-real-subspace coverage uses the stated closed-chamber argument. No author code imported.','scope':'Source-specific support-cover maxima only; no chronology or supplier admission.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
