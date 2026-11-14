#!/usr/bin/env python3
"""Independent GF(4) controls for the operator proof. @CubeJerry/OpenAI; Apache-2.0."""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

def need(x,msg):
    if not x: raise ValueError(msg)

def times(a,b):
    c=0
    for _ in range(2):
        if b&1:c^=a
        b>>=1
        a<<=1
        if a&4:a^=7
    return c

def echelon(rows):
    basis={}
    for v in rows:
        w=list(v)
        for i in sorted(basis):
            c=w[i]
            if c:w=[a^times(c,b) for a,b in zip(w,basis[i])]
        pivot=next((i for i,x in enumerate(w) if x),None)
        if pivot is not None:
            c=times(w[pivot],w[pivot])
            basis[pivot]=[times(c,x) for x in w]
    return basis

def residue(row,basis):
    w=list(row)
    for i in sorted(basis):
        c=w[i]
        if c:w=[a^times(c,b) for a,b in zip(w,basis[i])]
    return w

def prod(a,b):
    return [[times(a[i][0],b[0][j])^times(a[i][1],b[1][j]) for j in range(2)] for i in range(2)]

def flat(blocks):
    return [[x for block in blocks for x in block[i]] for i in range(2)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=a.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    n=json.loads(gzip.decompress(raw))
    roots=[list(map(Q,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
    K=[[int(i==j or sum(x*y for x,y in zip(roots[i],roots[j]))==0) for j in range(111)] for i in range(111)]
    I=[[1,0],[0,1]];Z=[[0,0],[0,0]]
    C=echelon([row for kr in K for row in flat([I if x else Z for x in kr])])
    need(len(C)==18,'GF4 canonical rank18')
    S=[0,2,38,41,42,45]
    U=[i for i in range(111) if i not in S and all(K[i][j] for j in S)]
    P=[[1,2],[0,1]];R=[[1,0],[2,1]]
    need(prod(P,R)!=prod(R,P),'noncommuting GF4 matrices')
    reports=[]
    for variant in ['sharp','mixed','singular']:
        G=[Z for _ in range(111)]
        for j in S:G[j]=I
        if variant=='mixed':G[S[1]]=P;G[S[2]]=R
        M=I if variant!='singular' else [[2,0],[0,0]]
        quotient=[];deletion=[];weights=[]
        for i in range(111):
            row=[]
            for j in range(111):
                correction=prod(M,G[j]) if i in U else Z
                base=I if K[i][j] else Z
                row.append([[base[r][s]^correction[r][s] for s in range(2)] for r in range(2)])
            need(row[i]==I and all(row[j]==Z for j in range(111) if not K[i][j]),'fitting')
            residual=[residue(v,C) for v in flat(row)]
            quotient.extend(residual)
            size=sum(row[j]!=Z for j in range(111) if j!=i)
            weights.append(int(size>36)+int(size>52))
            if size<sum(K[i])-1:
                deletion.append(i)
                need(len(echelon(residual))==2,'every deletion injects width2')
        d=len(echelon(quotient));ell=sum(weights)
        need(d<=2 and ell>=205,'one-width result in GF4')
        if variant=='sharp':need(d==2 and ell==205,'sharp extension-field tensor witness')
        if variant=='singular':need(d==1 and not deletion and ell==222,'subwidth cannot delete')
        reports.append(dict(variant=variant,quotient=d,ell=ell,deletion_count=len(deletion)))
    out=dict(status='PASS_INDEPENDENT_GF4_OPERATOR_QUOTIENT_REVIEW',author_proof_sha256=hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),native_sha256=hashlib.sha256(raw).hexdigest(),GF4_reports=reports,commutator_nonzero=True,universal_argument='Direct proof review in REVIEW.md; finite GF4 checks are corroboration.',inherited_geometric_census='Reused pinned source evidence; no new claim of replay.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
