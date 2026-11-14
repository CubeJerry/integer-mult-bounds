#!/usr/bin/env python3
"""Finite proper-cover decision by exact-certified modular span branching."""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"quadratic-exterior"/"author"))
from check import basis, members, load_native

def extend(B,x,p=101):
    x=[a%p for a in x]
    for row in B:
        j=next(j for j,a in enumerate(row) if a);c=x[j]
        if c:x=[(a-c*b)%p for a,b in zip(x,row)]
    if not any(x):return B
    j=next(j for j,a in enumerate(x) if a);inv=pow(x[j],-1,p);x=tuple(a*inv%p for a in x)
    out=[tuple((a-row[j]*b)%p for a,b in zip(row,x)) for row in B]+[x]
    return tuple(sorted(out,key=lambda r:next(j for j,a in enumerate(r) if a)))

def span(rows):
    B=()
    for x in rows:B=extend(B,x)
    return B

def rational_rank(rows):
    B=[]
    for original in rows:
        x=list(map(Fraction,original))
        for pivot,r in B:
            q=x[pivot]
            if q:x=[a-q*b for a,b in zip(x,r)]
        if any(x):
            pivot=next(j for j,q in enumerate(x) if q);q=x[pivot];B.append((pivot,[a/q for a in x]))
    return len(B)

def cover(rows):
    full=(1<<len(rows))-1
    if len(span(rows))<=6:
        if rational_rank(rows)<=6:return 0,[list(range(len(rows)))],0
        raise ValueError('modular rank collision')
    nodes=0
    @lru_cache(None)
    def closed(B):return sum(int(extend(B,row)==B)<<i for i,row in enumerate(rows))
    @lru_cache(None)
    def solve(U,W):
        nonlocal nodes
        nodes+=1;remaining=full&~(closed(U)|closed(W))
        if not remaining:return U,W
        i=(remaining&-remaining).bit_length()-1
        for side in (0,1):
            target=U if side==0 else W
            if len(target)==6 or (side==1 and U==W):continue
            enlarged=extend(target,rows[i]);a,b=(enlarged,W) if side==0 else (U,enlarged)
            if b<a:a,b=b,a
            found=solve(a,b)
            if found is not None:return found
        return None
    answer=solve((),())
    if answer is None:return 2,None,nodes
    U,W=answer;left=list(members(closed(U)));right=list(members(full&~closed(U)))
    if rational_rank([rows[i] for i in left])>6 or rational_rank([rows[i] for i in right])>6:
        raise ValueError('modular cover failed rational replay')
    return 1,[left,right],nodes

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--pivot',type=int,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    R,K=load_native(args.repo);pivot=args.pivot;C=basis(K)
    F=[row&(K[pivot] if K[pivot]>>i&1 else ~K[pivot]) for i,row in enumerate(K)]
    data=[]
    for j,row in enumerate(F):
        S=list(members(row&~(1<<j)));drop=next(a for a,x in enumerate(R[j]) if x)
        rows=[tuple(x for a,x in enumerate(R[t]) if a!=drop) for t in S]
        chi,partition,nodes=cover(rows)
        data.append(dict(receiver=j,orthogonal_to_pivot=bool(j!=pivot and K[pivot]>>j&1),foreign_size=len(S),chi=chi,search_nodes=nodes,cover=[[S[t] for t in part] for part in partition] if partition else None))
    out=dict(status='EXACT_NATIVE_PIVOT_COVER_CENSUS',pivot=pivot,fitting_rank=len(basis(F)),canonical_enlargement_rank=len(basis(C+F)),chi=sum(d['chi'] for d in data),chi_histogram=dict(Counter(d['chi'] for d in data)),rows=data)
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))

if __name__=='__main__':main()
