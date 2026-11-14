#!/usr/bin/env python3
"""Independent finite controls by enumerating every identity preimage first.
@CubeJerry/OpenAI; Apache-2.0. Universal proof reviewed separately.
"""
import argparse,itertools,json
from collections import Counter
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)

M=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
def dot(a,b):
    r=0
    for x,y in zip(a,b):r^=M[x][y]
    return r
def scaled(a,c):return tuple(M[x][c] for x in a)
def plus(a,b):return tuple(x^y for x,y in zip(a,b))
def plane(a,b):return {plus(scaled(a,x),scaled(b,y)) for x,y in itertools.product(range(4),repeat=2)}
def project(a):
    x=next((v for v in a if v),0)
    if not x:return None
    inv=next(y for y in range(1,4) if M[x][y]==1)
    return scaled(a,inv)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    cubic=[(1,t,M[t][t],M[t][M[t][t]]) for t in range(4)]+[(0,0,0,1)]
    conic=[(1,t,M[t][t]) for t in range(4)]+[(0,0,1)]
    vectors3=list(itertools.product(range(4),repeat=3))
    projective3=sorted({project(v) for v in vectors3 if any(v)})
    records=[];maps={};census=Counter()
    for g in itertools.product(range(4),repeat=4):
        left=g[:3];right=g[1:]
        if len(plane(left,right))<16:continue
        row0=[u for u in vectors3 if (dot(u,left),dot(u,right))==(1,0)]
        row1=[u for u in vectors3 if (dot(u,left),dot(u,right))==(0,1)]
        need(len(row0)==len(row1)==4,'full-rank Hankel has four solutions per identity row')
        for u,v in itertools.product(row0,row1):
            kernel=[z for z in projective3 if dot(u,z)==dot(v,z)==0]
            need(len(kernel)==1,'selector has exactly one projective kernel')
            typ=conic.index(kernel[0]) if kernel[0] in conic else None
            U=(u,v);maps[U]=typ;records.append((U,typ,g))
    need(len(records)==3840 and len(maps)==3120,'complete identity maps and preimages')
    for typ in maps.values():census[str(typ)]+=1
    checks=0;cover=Counter();omitted=0
    for chosen in itertools.combinations(range(5),4):
        span={tuple(0 for _ in range(4))}
        for j in chosen:span={plus(v,scaled(cubic[j],c)) for v in span for c in range(4)}
        need(len(span)==256,'every four cubic points independent')
        pairs=list(itertools.combinations(chosen,2));planes={ij:plane(cubic[ij[0]],cubic[ij[1]]) for ij in pairs}
        for U,typ,g in records:
            n=0;miss=0
            for ij,P in planes.items():
                inside=g in P;miss+=inside
                local=typ is None or cubic[typ] in P
                if local and not inside:n+=1
                if typ in ij:need(not inside,'incident exceptional plane cannot contain identity preimage')
            if typ is None:need(n>=5 and miss<=1,'regular identity preimage covered five times')
            elif typ in chosen:need(n==3,'selected exceptional map covered three times')
            else:need(n==0,'omitted fifth exceptional map outside proof');omitted+=1
            checks+=1;cover[n]+=1
    weights=[]
    for w0 in range(29):
        for w1 in range(29-w0):
            for w2 in range(29-w0-w1):
                w=(w0,w1,w2,28-w0-w1-w2)
                if all(w[i]+w[j]<=14 for i,j in itertools.combinations(range(4),2)):weights.append(w)
    need(weights==[(7,7,7,7)],'unique nonnegative equality weights')
    need(not any(all(x%2==0 for x in w) for w in weights),'equality parity excludes target')
    boundary=(6,6,6,6,4)
    need(sum(boundary)==28 and all(boundary[i]+boundary[j]<=14 for i,j in itertools.combinations(range(5),2)), 'five-type pair bounds alone do not exclude target')
    out=dict(status='PASS_INDEPENDENT_FOUR_TYPE_PARITY_CONTROLS',field='F4',identity_maps=len(maps),all_identity_preimage_pairs=len(records),map_type_census=dict(census),type_set_preimage_checks=checks,coverage_histogram=dict(cover),fifth_type_scope_controls=omitted,unique_weights_without_parity=weights,even_weight_solutions=0,five_type_abstract_boundary=boundary,scope='Independent finite corroboration plus separately reviewed universal scalarization/equality proof. Five-type case remains open; no new kappa.')
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
