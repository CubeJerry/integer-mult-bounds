#!/usr/bin/env python3
"""Independent finite-field and information-collision checks of record counts."""
from itertools import product, combinations
import json, random
from pathlib import Path

def rref(A,p,width=None):
    A=[list(x) for x in A];n=width if width is not None else (len(A[0]) if A else 0);piv=[];r=0
    for c in range(n):
        i=next((i for i in range(r,len(A)) if A[i][c]%p),None)
        if i is None: continue
        A[r],A[i]=A[i],A[r];z=pow(A[r][c]%p,-1,p);A[r]=[(x*z)%p for x in A[r]]
        for j in range(len(A)):
            if j!=r and A[j][c]%p:
                z=A[j][c];A[j]=[(x-z*y)%p for x,y in zip(A[j],A[r])]
        piv.append(c);r+=1
        if r==len(A): break
    return A[:r],piv
def rank(A,p,width=None): return len(rref(A,p,width)[1])
def transpose(A,width=None):
    if not A: return [[] for _ in range(width or 0)]
    return [list(x) for x in zip(*A)]
def null(A,p,n):
    R,piv=rref(A,p,n);free=[j for j in range(n) if j not in piv];out=[]
    for j in free:
        v=[0]*n;v[j]=1
        for i,c in enumerate(piv): v[c]=-R[i][j]%p
        out.append(v)
    return out
def mul(A,B,p,outwidth=None):
    n=outwidth if outwidth is not None else (len(B[0]) if B else 0)
    return [[sum(a*b for a,b in zip(row,col))%p for col in transpose(B,n)] for row in A]
def add(A,B,p,sign=1): return [[(a+sign*b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def inverse(A,p):
    n=len(A);R,piv=rref([a+b for a,b in zip(A,eye(n))],p,2*n)
    if piv[:n]!=list(range(n)): raise ValueError('singular')
    return [r[n:] for r in R]
def left_rel(A,p,width): return null(transpose(A,width),p,len(A))
def solve_row(A,b,p):
    R,piv=rref([x+[v] for x,v in zip(transpose(A,len(b)),b)],p,len(A)+1)
    if len(A) in piv: return None
    x=[0]*len(A)
    for row,c in zip(R,piv): x[c]=row[-1]
    return x
def eval_rows(A,v,p): return tuple(sum(a*b for a,b in zip(r,v))%p for r in A)
def collision(O,T,p,n):
    table={}
    for v in product(range(p),repeat=n):
        y=eval_rows(O,v,p);z=eval_rows(T,v,p)
        if y in table and table[y][0]!=z: return [list(table[y][1]),list(v)]
        table[y]=(z,v)
    return None
def check_case(p,W,N,Q,R,D,Lam,Gamma,T):
    k=len(Q);q=len(Q[0]);u=len(W[0]);m=len(W)
    H=add(mul(Lam,W,p),mul(Gamma,N,p,outwidth=u),p)
    Z=[[rng.randrange(p) for _ in range(k)] for _ in range(m)]
    G=add(T,mul(Lam,Z,p),p,-1)
    delta=mul(inverse(T,p),[[-h%p for h in row]+Q[i] for i,row in enumerate(H)],p)
    Y=add([row+[0]*q for row in W],mul(Z,delta,p),p)
    O=Y+[row+[0]*q for row in N]+[[0]*u+row for row in R]
    targets=[row+[0]*q for row in W]+[[0]*u+row for row in D]
    gate=all(solve_row(Q+R,d,p) is not None for d in D)
    relations=left_rel(Q+R,p,q);U=[row[:k] for row in relations]
    common_rel=left_rel(W+N,p,u);J=[row[:m] for row in common_rel]
    C=mul(U,G,p,outwidth=k)+mul(J,Z,p,outwidth=k)
    expected=None
    if gate:
        A=[solve_row(Q+R,d,p)[:k] for d in D];M=Z+mul(A,G,p,outwidth=k)
        expected=rank(C+M,p,k)-rank(C,p,k)
    projective=[]
    for row in product(range(p),repeat=k):
        nz=next((v for v in row if v),None)
        if nz==1: projective.append(list(row))
    best=None;selected=None;previous=None
    for size in range(k+1):
        for indices in combinations(range(len(projective)),size):
            K=[projective[i] for i in indices]
            Obs=O+mul(K,delta,p,outwidth=u+q)
            if rank(Obs+targets,p,u+q)==rank(Obs,p,u+q): best=size;selected=K;break
            previous=K
        if best is not None: break
    if best!=expected: raise ValueError(('minimum mismatch',p,expected,best))
    full=D==eye(q)
    coordinate_best=None
    for size in range(k+1):
        for indices in combinations(range(k),size):
            K=[eye(k)[i] for i in indices];Obs=O+mul(K,delta,p,outwidth=u+q)
            if rank(Obs+targets,p,u+q)==rank(Obs,p,u+q): coordinate_best=size;break
        if coordinate_best is not None: break
    if full and gate:
        if best!=k-rank(C,p,k) or coordinate_best!=best: raise ValueError('full raw corollary')
    # Enumerate every physical input for the attained record set and one
    # smaller failing choice, independently of matrix span/rank comparisons.
    if selected is not None and collision(O+mul(selected,delta,p,outwidth=u+q),targets,p,u+q): raise ValueError('attained decoder collision')
    if best is None: bad=eye(k)
    elif best>0: bad=selected[:-1]
    else: bad=None
    witness=None if bad is None else collision(O+mul(bad,delta,p,outwidth=u+q),targets,p,u+q)
    if bad is not None and witness is None: raise ValueError('missing smaller-set collision')
    return dict(field=p,k=k,raw=q,common=u,gate=gate,record_minimum=best,coordinate_minimum=coordinate_best,full_raw=full,known_difference_rank=rank(C,p,k),negative_witness=witness)

rng=random.Random(2026111207)
def main():
    cases=[]
    for p in (2,3):
        for trial in range(18):
            u=2;q=1+trial%3;k=1+(trial//3)%3;m=1
            W=[[1,0]];N=[[0,1]] if trial%2 else [[1,0],[0,1]]
            Q=[[rng.randrange(p) for _ in range(q)] for _ in range(k)]
            R=[[rng.randrange(p) for _ in range(q)] for _ in range(trial%3)]
            D=eye(q) if trial%2==0 else [[rng.randrange(p) for _ in range(q)]]
            Lam=[[rng.randrange(p)] for _ in range(k)];Gamma=[[rng.randrange(p) for _ in N] for _ in range(k)]
            T=[[int(i==j) if j>=i else rng.randrange(p) for j in range(k)] for i in range(k)]
            cases.append(check_case(p,W,N,Q,R,D,Lam,Gamma,T))
    result=dict(status='PASS_INDEPENDENT_FINITE_FIELD_RECORD_MINIMA',cases=cases,case_count=len(cases),fields=[2,3],method='Independent pure-Python modular elimination; exhaustive projective-record subsets; exhaustive physical-input collision checks for attaining and failing records.',scope='Corroborates the separate universal field-linear proof, not a source construction or new kappa.')
    out=Path(__file__).with_name('RECORD-REVIEW-RESULT.json');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],len(cases))
if __name__=='__main__': main()
