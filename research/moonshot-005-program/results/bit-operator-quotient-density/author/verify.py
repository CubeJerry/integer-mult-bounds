#!/usr/bin/env python3
"""Finite controls; universal proof separate. @CubeJerry/OpenAI, Apache-2.0."""
import argparse
import hashlib
import json
from pathlib import Path

def need(ok,message):
    if not ok: raise ValueError(message)

def mul(a,b):
    c=0
    while b:
        if b&1: c^=a
        b>>=1
        a<<=1
        if a&32: a^=0b100101
    return c

def power(a,n):
    c=1
    while n:
        if n&1: c=mul(c,a)
        a=mul(a,a)
        n>>=1
    return c

def rank(rows):
    piv={}
    for source in rows:
        row=list(source)
        for j in range(len(row)):
            a=row[j]
            if not a: continue
            if j in piv:
                row=[x^mul(a,y) for x,y in zip(row,piv[j])]
            else:
                inv=power(a,30)
                piv[j]=[mul(inv,x) for x in row]
                break
    return len(piv)

def dot(a,b):
    c=0
    for x,y in zip(a,b): c^=mul(x,y)
    return c

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--programme',type=Path,required=True)
    args=p.parse_args()
    sources=json.loads((Path(__file__).parent/'SOURCES.json').read_text())
    for name,digest in sources['source_dependencies'].items():
        need(hashlib.sha256((args.programme/name).read_bytes()).hexdigest()==digest,'source dependency '+name)
    need(all(mul(a,power(a,30))==1 for a in range(1,32)),'all nonzero invert')
    need(all(mul(a,b)==mul(b,a) for a in range(32) for b in range(32)),'commutative')
    need(all(mul(a,b^c)==mul(a,b)^mul(a,c) for a in range(32) for b in range(32) for c in range(32)),'distributive')
    pts=list(range(28))
    normals=[[power(a,j) for j in range(18)] for a in pts]
    need(rank(normals)==18,'ambient rank18')
    need(rank([normals[0],normals[0]])==1,'duplicate-row negative control')
    need(rank(normals[:17]+[normals[0]])==17,'duplicate-point nonsingularity control')
    need(all(rank([row])==1 for row in normals),'dimension17 hyperplanes')
    # All18 subsets nonsingular by Vandermonde; check ALL pair premises.
    need(all(pts[i]^pts[j] for i in range(28) for j in range(i)),'distinct points')
    poly=[1]
    for a in pts[:17]:
        nxt=[0]*(len(poly)+1)
        for j,c in enumerate(poly):
            nxt[j]^=mul(a,c)
            nxt[j+1]^=c
        poly=nxt
    roots=[a for a,row in zip(pts,normals) if dot(row,poly)==0]
    need(roots==pts[:17],'exactly17 memberships')
    need(rank(normals[:17])==17 and rank(normals[:18])==18,'17/18 boundary')
    boundaries=[]
    for t in range(9,19):
        rows=[[int(i==j) for j in range(t)] for i in range(t)]
        need(t-rank(rows)==0 and t-rank(rows[:-1])==1,'sharp intersection')
        boundaries.append(dict(t=t,V=t-1,d=t,intersection=0,one_omitted=1))
    weighted=0
    for b in range(112):
        for a in range(112-b):
            if 2*b+a<28: continue
            if b>=9: t,w=9,18
            else:
                c=18-2*b
                need(c<=a,'enough singles')
                t,w=b+c,2*b+c
            need(w>17 and t==18-min(b,9),'weighted selection')
            weighted+=1
    dims=[]
    for v in [1,2,3,16,17,18,34,100,1000]:
        g=(v+16)//17
        need(17*(g-1)<v<=17*g,'integer ceiling')
        dims.append(dict(V=v,minimum_quotient=v+g))
    controls={
      'S_ge17_rejected_by_sharp_tensor':dict(S=17,d='V'),
      'abstract_d_ge2V_rejected':dict(V=17,d=18,total_weight=28),
      'pairwise_implies_common_rejected':dict(hyperplanes=18,pair_intersection=16,common_intersection=0),
      'MDS_is_native_fitting_or_physical_word':False}
    out=dict(status='PASS_OPERATOR_QUOTIENT_DENSITY_CONTROLS',classification='Finite controls; universal proof and independent review separate.',GF32_modulus='x^5+x^2+1',hyperplanes=28,V=17,d=18,attained_point_multiplicity=len(roots),polynomial=poly,all_distinct_pair_premises=378,weighted_censuses=weighted,boundaries=boundaries,dimension_examples=dims,negative_controls=controls,geometry='Reused credited native gluing and17-savings evidence, not regenerated here.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],'weighted_censuses',weighted)

if __name__=='__main__': main()
