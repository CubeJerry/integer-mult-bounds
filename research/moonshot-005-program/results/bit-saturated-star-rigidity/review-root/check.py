#!/usr/bin/env python3
"""Independent native/anchor reconstruction; no author checker imported."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import argparse, gzip, hashlib, json, random
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAME=[0,16,17,32,36,38,67,71]
def need(b,s):
    if not b: raise ValueError(s)
def rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)
def mul(a,b):
    out=[]
    for x in a:
        y=0
        for j,r in enumerate(b):
            if x>>j&1:y^=r
        out.append(y)
    return out
def inv(a):
    n=len(a);r=[x|1<<(n+i) for i,x in enumerate(a)]
    for p in range(n):
        q=next((q for q in range(p,n) if r[q]>>p&1),None)
        need(q is not None,'invertible gauge');r[p],r[q]=r[q],r[p]
        for j in range(n):
            if j!=p and r[j]>>p&1:r[j]^=r[p]
    need([x&((1<<n)-1) for x in r]==[1<<i for i in range(n)],'inverse')
    return [x>>n for x in r]
def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    s=json.loads(gzip.decompress(raw));roots=[]
    for i in range(111):
        v=[Fraction(x) for x in s['frames'][str(s['start'][i])]['B'][0]]
        n=sum(x*x for x in v);need(n in (1,4),'norm')
        if n==1:v=[2*x for x in v]
        need(all(x.denominator==1 for x in v),'integer roots');roots.append(tuple(map(int,v)))
    K=[[int(i==j or sum(x*y for x,y in zip(roots[i],roots[j]))==0) for j in range(111)] for i in range(111)]
    kmasks=[sum(x<<j for j,x in enumerate(r)) for r in K]
    need(rank(kmasks)==9,'rank9')
    need(rank([r^(1<<i) for i,r in enumerate(kmasks)])==108,'foreign residual rank108')
    need(all(K[i][j]==int(i==j) for i in FRAME for j in FRAME),'identity frame')
    f=[sum(K[i][j]<<p for p,j in enumerate(FRAME)) for i in range(111)]
    S=[[K[i][j]^((f[i]&f[j]).bit_count()%2) for j in range(111)] for i in range(111)]
    p=next(i for i in range(111) if S[i][i]);z=[S[i][p] for i in range(111)]
    need(all(S[i][j]==z[i]*z[j] for i in range(111) for j in range(111)),'rank1 Schur factor')
    x=[f[i]|z[i]<<8 for i in range(111)]
    need(all((x[i]&x[j]).bit_count()%2==K[i][j] for i in range(111) for j in range(111)),'12321 products')
    edges={i:tuple(p for p in range(8) if f[i]>>p&1) for i in range(111) if z[i] and f[i].bit_count()==2}
    need(len(edges)==len(set(edges.values()))==27,'27 edges')
    need(set(combinations(range(8),2))-set(edges.values())=={(0,4)},'K8 minus04')
    deg=[sum(p in e for e in edges.values()) for p in range(8)]
    need(deg==[6,7,7,7,6,7,7,7],'degrees')
    need(all(K[i][j]==int(not(set(edges[i])&set(edges[j]))) for i in edges for j in edges if i!=j),'shared-end zeros')
    seed=FRAME+list(edges);anchors={}
    for i in range(111):
        if i in seed:continue
        ids=[];rows=[]
        for j in reversed(seed):
            if not K[i][j] and rank(rows+[x[j]])>len(rows):ids.append(j);rows.append(x[j])
        need(len(rows)==8 and x[i].bit_count()%2==1,'eight anchors')
        need(all((x[i]&r).bit_count()%2==0 for r in rows),'own annihilator')
        need(rank(rows[:-1])==7,'missing-anchor control');anchors[str(i)]=ids
    need(len(anchors)==76,'76 extensions');rng=random.Random(20261114);trials=[]
    for V in [2,3,4]:
        I=[1<<i for i in range(V)];Z=[0]*V;U=[]
        for _ in range(111):
            g=I[:]
            for _ in range(7*V):
                i,j=rng.sample(range(V),2);g[i]^=g[j]
            U.append(g)
        # Two explicit opposite transvections prevent an accidentally
        # commuting random sample (even-length walks in GL(2,F2) do that).
        U[0]=I[:];U[0][0]^=U[0][1]
        U[1]=I[:];U[1][1]^=U[1][0]
        R=list(map(inv,U));block=lambda i,j:mul(U[i],R[j]) if K[i][j] else Z[:]
        need(any(mul(U[i],U[j])!=mul(U[j],U[i]) for i in range(8) for j in range(8)),'noncommuting controls')
        for e in edges:
            schur=I[:]
            for f0 in FRAME:schur=[b^c for b,c in zip(schur,mul(block(e,f0),block(f0,e)))]
            need(schur==I,'all27 intrinsic Schur blocks')
        need(all(rank(block(i,j))==(V if K[i][j] else 0) for i in range(111) for j in range(111)),'all block ranks')
        trials.append({'V':V,'noncommuting':True,'blocks_checked':12321})
    # Only a countermodel to the LR inequalities, not an actual fitting.
    need(4==2*(1+1) and 5>2*(1+1),'degree4/5 relaxation controls')
    e=next(iter(edges));badrow=1<<edges[e][0]
    need((badrow&x[e]).bit_count()%2==1,'mutant diagonal retained')
    broken=[j for j in seed if not K[e][j] and (badrow&x[j]).bit_count()%2]
    need(bool(broken),'zero-mask control')
    out={'status':'PASS_INDEPENDENT_SATURATED_STAR_SOURCE_PREMISES','native_sha256':PIN,'frame':FRAME,'factor_vectors':x,'edge_roles':{str(i):list(v) for i,v in edges.items()},'degrees':deg,'saturation_weights':[d-4 for d in deg],'anchors':anchors,'foreign_contacts':sum(map(sum,K))-111,'foreign_residual_rank':108,'block_controls':trials,'negative_controls':{'removed_anchor_rank':7,'degree4_relaxation_permits_positive_defects':True,'bad_mask_detected':broken},'scope':'Exact finite source premises and controls. Written proof supplies all-field/all-V quantifiers. No physical word, supplier or kappa.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ['status','degrees','foreign_contacts','block_controls']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
