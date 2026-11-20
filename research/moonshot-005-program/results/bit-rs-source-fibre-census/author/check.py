#!/usr/bin/env python3
"""Find exact indexed inverse-fibre rank witnesses on the live RS source."""
import gzip
import hashlib
import json
from itertools import combinations
from pathlib import Path
import random
import time
import numpy as np

import argparse
cli=argparse.ArgumentParser(description=__doc__)
cli.add_argument('--repo',type=Path,required=True)
cli.add_argument('--out',type=Path,required=True)
args=cli.parse_args()
def need(ok, message):
    if not ok:
        raise ValueError(message)

REPO = args.repo
args.out.mkdir(parents=True,exist_ok=True)
BASE = REPO / 'research/moonshot-005-program/results'
raw = gzip.decompress((BASE / 'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
need(hashlib.sha256(raw).hexdigest() == '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72', 'authenticated native geometry')
geo = json.loads(raw)
roots = np.array(geo['root_table'], dtype=np.int16)
planes = [tuple(h) for h in geo['A2']]
orth = roots @ roots.T == 0
stars = [[h for h,H in enumerate(planes) if j in H] for j in range(111)]
nodes = [{h:i+1 for i,h in enumerate(st)} for st in stars]
singleton = {H[0]:h for h,H in enumerate(planes) if sum(j < 111 for j in H) == 1}
singleton = {next(j for j in planes[h] if j < 111):h for h in singleton.values()}
perp = [{i for i in range(111) if all(orth[i,j] for j in H)} for H in planes]

def mult(a,b):
    out=0
    while b:
        if b&1: out ^= a
        a <<= 1
        if a&64: a ^= 67
        b >>= 1
    return out
M = np.array([[mult(a,b) for b in range(64)] for a in range(64)],dtype=np.uint8)
INV = np.array([0]+[next(i for i in range(1,64) if M[a,i] == 1) for a in range(1,64)],dtype=np.uint8)

def rank(A):
    A=np.asarray(A,dtype=np.uint8).copy()
    if not A.size: return 0
    r=0
    for c in range(A.shape[1]):
        inds=np.flatnonzero(A[r:,c])
        if not len(inds): continue
        q=r+int(inds[0])
        A[[r,q]]=A[[q,r]]
        A[r] = M[INV[A[r,c]], A[r]]
        if r+1 < len(A):
            A[r+1:] ^= M[A[r+1:,c,None],A[r][None,:]]
        r+=1
        if r==len(A): break
    return r

def inv(A):
    A=np.asarray(A,dtype=np.uint8)
    n=len(A)
    R=np.concatenate([A.copy(),np.eye(n,dtype=np.uint8)],axis=1)
    for c in range(n):
        inds=np.flatnonzero(R[c:,c])
        if not len(inds): return None
        q=c+int(inds[0]);R[[c,q]]=R[[q,c]]
        R[c] = M[INV[R[c,c]],R[c]]
        coeff=R[:,c].copy();coeff[c]=0
        R ^= M[coeff[:,None],R[c][None,:]]
    need(np.array_equal(R[:,:n],np.eye(n,dtype=np.uint8)), 'exact inverse identity')
    return R[:,n:]

def matmul(A,B):
    return np.bitwise_xor.reduce(M[np.asarray(A)[:,:,None],np.asarray(B)[None,:,:]],axis=1)

def poly(xs):
    p=np.array([1],dtype=np.uint8)
    for a in xs:
        q=np.zeros(len(p)+1,dtype=np.uint8)
        q[:-1]^=M[a,p];q[1:]^=p;p=q
    return p

fibres={}
def fibre(j,h,i):
    key=j,h,i
    if key not in fibres:
        xs=[nodes[j][p] for p in stars[j] if p!=h and i in perp[p]]
        need(len(xs)==15, 'fifteen off-H source nodes')
        fibres[key]=poly(xs)
    return fibres[key]

def witness(j,k,h,rng,tries=40):
    ii=sorted(perp[h]-{80})
    # A singleton observation has a genuine extra derivative, so omit its
    # audience from this ordinary tight-source argument.
    for v in (j,k):
        if v in singleton:
            ii=[i for i in ii if i not in perp[singleton[v]]]
    A=np.array([fibre(j,h,i) for i in ii],dtype=np.uint8)
    B=np.array([fibre(k,h,i) for i in ii],dtype=np.uint8)
    ra,rb=rank(A),rank(B)
    if ra!=rb: return {'receivers':ii,'ranks':[ra,rb],'method':'whole_audience'}
    if ra<16: return {'unresolved':True,'audience':len(ii),'rank':ra}
    for attempt in range(tries):
        chosen=rng.sample(range(len(ii)),16)
        Ai=inv(A[chosen]);Bi=inv(B[chosen])
        if Ai is None or Bi is None:
            ra,rb=rank(A[chosen]),rank(B[chosen])
            if ra!=rb:
                return {'receivers':[ii[t] for t in chosen],'ranks':[ra,rb],'method':'basis_rank'}
            continue
        CA=matmul(A,Ai);CB=matmul(B,Bi)
        mismatch=np.argwhere((CA==0)!=(CB==0))
        if len(mismatch):
            u,v=map(int,mismatch[0])
            selected=chosen.copy();selected[v]=u
            need(len(set(selected))==16, 'sixteen distinct receivers')
            ra,rb=rank(A[selected]),rank(B[selected]);need(ra!=rb, 'basis exchange rank obstruction')
            return {'receivers':[ii[t] for t in selected],'ranks':[ra,rb],'method':'basis_exchange','attempt':attempt}
    return {'unresolved':True,'audience':len(ii),'rank':ra,'trials':tries}

def main():
    rng=random.Random(202611200630)
    records=[];unresolved=[]
    started=time.time()
    for h,H in enumerate(planes):
        for j,k in combinations([x for x in H if x<111 and x!=10],2):
            w=witness(j,k,h,rng)
            row={'donors':[j,k],'H':h,**w}
            (unresolved if 'unresolved' in w else records).append(row)
    ordinary=[r for r in records if not set(r['donors']) & set(singleton)]
    need(len(ordinary)==2281, 'all ordinary nonorthogonal pairs')
    need(not [r for r in unresolved if not set(r['donors']) & set(singleton)], 'no unresolved ordinary pair')
    old=json.loads(gzip.decompress((Path(__file__).parent/'WITNESSES.json.gz').read_bytes()))
    for row in ordinary:
        clean={k:v for k,v in row.items() if k not in {'method','attempt'}}
        need(clean in old['witnesses'], 'literal compact certificate reproduced')
    result={'witnesses':records,'unresolved':unresolved,'singleton_donors':sorted(singleton),
            'nodes':'1..28 in actual increasing H chart ID','excluded_donor':10,'excluded_receiver':80,
            'elapsed':time.time()-started}
    p=args.out/'CENSUS.json'
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'witnesses':len(records),'unresolved':len(unresolved),'singleton_donors':sorted(singleton),
                      'ordinary_unresolved':[r for r in unresolved if not set(r['donors'])&set(singleton)],
                      'elapsed':time.time()-started},indent=2),flush=True)

if __name__=='__main__':main()
