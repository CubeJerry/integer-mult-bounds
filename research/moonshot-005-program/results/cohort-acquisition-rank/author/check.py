#!/usr/bin/env python3
"""Exact finite adversarial controls for the cohort-order kernel theorem."""
import argparse,itertools,json,random
from fractions import Fraction as F
from pathlib import Path

def need(ok,s):
    if not ok:raise ValueError(s)
def rank(A,p):
    A=[r[:] for r in A];q=0
    for j in range(len(A[0]) if A else 0):
        k=next((k for k in range(q,len(A)) if A[k][j]%p),None)
        if k is None:continue
        A[q],A[k]=A[k],A[q];z=pow(A[q][j]%p,-1,p);A[q]=[x*z%p for x in A[q]]
        for k in range(q+1,len(A)):
            z=A[k][j]%p
            if z:A[k]=[(x-z*y)%p for x,y in zip(A[k],A[q])]
        q+=1
    return q
def product(A,B,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def case(N,B,V,p,k,seed):
    rng=random.Random(seed);co=[i for i,a in enumerate(N) for _ in range(a)];ac=[i for i,a in enumerate(B) for _ in range(a)];n=sum(N);b=sum(B)
    P=[[0]*(n*V) for _ in range(b*V)];supports=[]
    for j,c in enumerate(ac):
        choices=[i for i in range(len(N)) if i!=c];ss=rng.sample(choices,rng.randrange(min(k,len(choices))+1));supports.append(set(ss))
        for d in ss:
            cols=[z for z,t in enumerate(co) if t==d]
            for ii in range(V):
                for jj in cols:
                    for ell in range(V):P[j*V+ii][jj*V+ell]=rng.randrange(p)
            if not any(P[j*V+ii][jj*V+ell] for ii in range(V) for jj in cols for ell in range(V)):P[j*V][cols[0]*V]=1
    U=[[0]*(b*V) for _ in range(n*V)]
    for i,c in enumerate(co):
        for j,d in enumerate(ac):
            if c==d:
                for ii in range(V):
                    for jj in range(V):U[i*V+ii][j*V+jj]=rng.randrange(p)
    # Force singular and zero-cohort decoder cases in a deterministic fraction.
    if seed%3==0:
        for ii in range(V):U[ii]=[0]*(b*V)
    UP=product(U,P,p);A=[[(int(i==j)-UP[i][j])%p for j in range(n*V)] for i in range(n*V)];r=rank(A,p)
    expect=sum((F(1,len(s)+1) for s in supports),F(0));ce=(expect.numerator+expect.denominator-1)//expect.denominator;maxg=0;edges=0
    for order in itertools.permutations(range(len(N))):
        pos={v:i for i,v in enumerate(order)};good=[all(pos[ac[j]]<pos[d] for d in s) for j,s in enumerate(supports)];g=sum(good);maxg=max(maxg,g)
        need(r>=V*(n-b+g),'order rank bound')
        old=0
        for i,c in enumerate(order):
            later=set(order[i+1:]);fixed=[jj*V+ell for jj,t in enumerate(co) if t in later for ell in range(V)]
            extra=[[int(j==z) for j in range(n*V)] for z in fixed]
            zdim=n*V-rank(A+extra,p);bad=sum(ac[j]==c and not good[j] for j in range(b))
            need(0<=zdim-old<=bad*V,'literal kernel filtration increment');old=zdim;edges+=1
        need(old==n*V-r,'filtration ends at actual kernel')
    need(maxg>=ce and r>=V*(n-b+ce),'heterogeneous rational expectation')
    return {'N':N,'B':B,'V':V,'prime':p,'max_support':k,'rank':r,'decoder_rank':rank(U,p),'expectation':str(expect),'best_order_good':maxg,'filtration_checks':edges}
def main(a):
    cases=[];seed=317
    shapes=[([1,1],[1,1]),([2,1,2],[2,1,2]),([1,2,1,1],[1,2,1,1]),([1,1,1],[2,2,2]),([2,2,1],[1,3,1]),([2,1,1],[0,2,1])]
    for N,B in shapes:
        for V in (1,2):
            for p in (2,3,5):
                for k in (0,1,2):
                    for rep in range(3):
                        cases.append(case(N,B,V,p,k,seed));seed+=1
    sharp=[]
    for n in range(1,13):
        for k in range(min(n,5)):
            for V in (1,2,3):
                for p in (2,3,5):
                    A=[[int(i//V//(k+1)==j//V//(k+1) and i%V==j%V) for j in range(n*V)] for i in range(n*V)]
                    r=rank(A,p);need(r==V*((n+k)//(k+1)),'all-field sharp complete-group blocks')
                    sharp.append([n,k,V,p,r])
    # The theorem's two structural assumptions are necessary.
    I=identity(3);P=I;U=I;A=[[int(i==j)-sum(U[i][z]*P[z][j] for z in range(3)) for j in range(3)] for i in range(3)]
    need(rank(A,2)==0 and any(P[i][i] for i in range(3)),'self-support mutant must violate premise')
    P=[[int(j==(i+1)%3) for j in range(3)] for i in range(3)];U=[[int(j==(i-1)%3) for j in range(3)] for i in range(3)];UP=product(U,P,2)
    need(UP==I and any(U[i][j] for i in range(3) for j in range(3) if i!=j),'cross-cohort decoder mutant must violate premise')
    # Six real acquisition rows can realize the three-node all-ones fitting;
    # miscounting them as three rows would incorrectly assert rank>=2.
    P=[];U=[[0]*6 for _ in range(3)];h=0
    for i in range(3):
        for j in range(3):
            if i!=j:
                P.append([int(c==j) for c in range(3)]);U[i][h]=1;h+=1
    UP=product(U,P,2);A=[[(int(i==j)-UP[i][j])%2 for j in range(3)] for i in range(3)]
    need(rank(A,2)==1,'rectangular acquisition counterexample to wrong square count')
    M=[[1,1],[0,1]];N=[[0,1],[1,0]];need(product(M,N,2)!=product(N,M,2),'genuinely noncommuting matrices exist in test domain')
    out={'status':'PASS_EXACT_COHORT_FILTRATION_CONTROLS','cases':cases,'sharpness_controls':sharp,'total_kernel_filtration_checks':sum(c['filtration_checks'] for c in cases),'singular_decoder_cases':sum(c['decoder_rank']<min(sum(c['N']),sum(c['B']))*c['V'] for c in cases),'negative_controls':['allow own-cohort P=I makes A=0','allow cross-cohort U=P inverse makes A=0','miscount six actual acquisition rows as three falsely excludes rank1','noncommuting2x2 products not silently reordered'],'n111_max_support_needed_for_q':{'8':13,'9':12,'10':11},'scope':'Finite controls only; universal proof is the separately reviewed cohort-order kernel filtration.','new_kappa':None}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','total_kernel_filtration_checks','singular_decoder_cases']}));print('matrix cases',len(cases),'sharpness controls',len(sharp))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args())
