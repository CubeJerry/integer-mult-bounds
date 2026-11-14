#!/usr/bin/env python3
"""Independent exact marked-budget and twisted-cubic controls. No author imports."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from collections import Counter
import itertools,json,hashlib
HERE=Path(__file__).resolve().parent;D=10**40
def need(ok,msg):
    if not ok:raise ValueError(msg)
@lru_cache(None)
def p(r):
    if r in(0,1):return F(r),F(r)
    z=r**199*D**200;x=1<<((z.bit_length()+199)//200)
    while True:
        y=(199*x+z//x**199)//200
        if y>=x:break
        x=y
    while x**200>z:x-=1
    while (x+1)**200<=z:x+=1
    need(x**200<=z<(x+1)**200,'root');return F(x,D),F(x+1,D)
def plus(*xs):return sum(x[0]for x in xs),sum(x[1]for x in xs)
def mul(c,x):
    c=F(c);return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def sub(x,y):return plus(x,mul(-1,y))
def divide(x,y):return min(a/b for a in x for b in y),max(a/b for a in x for b in y)
def ceil(x):return-((-x.numerator)//x.denominator)
def field(q,poly):
    def m(a,b):
        v=0
        while b:
            if b&1:v^=a
            a<<=1;b>>=1
            if a&q:a^=poly
        return v
    def power(a,n):
        z=1
        while n:
            if n&1:z=m(z,a)
            a=m(a,a);n>>=1
        return z
    def normalize(v):
        a=next(x for x in v if x);a=power(a,q-2);return tuple(m(x,a)for x in v)
    def rank(rows):
        A=[list(r)for r in rows];i=0
        for j in range(4):
            k=next((k for k in range(i,len(A))if A[k][j]),None)
            if k is None:continue
            A[i],A[k]=A[k],A[i];f=power(A[i][j],q-2);A[i]=[m(f,v)for v in A[i]]
            for k in range(i+1,len(A)):
                f=A[k][j]
                if f:A[k]=[x^m(f,y)for x,y in zip(A[k],A[i])]
            i+=1
        return i
    gamma=[(1,t,m(t,t),m(m(t,t),t))for t in range(q)]+[(0,0,0,1)]
    need(all(rank(vs)==4 for vs in itertools.combinations(gamma,4)),'all four cubic points independent')
    counts=Counter()
    for u,v in itertools.combinations(gamma,2):
        points={normalize(tuple(x^m(t,y)for x,y in zip(u,v)))for t in range(q)};points.add(normalize(v));need(len(points)==q+1,'complete pair plane')
        counts.update(points)
    gs=set(gamma);need(all(counts[v]==q for v in gs),'exceptional incidence');need(all(c==1 for v,c in counts.items()if v not in gs),'noncubic point lies in at most one pair plane')
    control=tuple(x^y for x,y in zip(gamma[0],gamma[1]));need(rank([gamma[0],gamma[1],gamma[-1],control])<4,'dependent four-point control')
    return dict(types=q+1,pairs=(q+1)*q//2,noncubic_pair_points=sum(v not in gs for v in counts),all_four_subsets_checked=len(list(itertools.combinations(gamma,4))))
def main():
    B=plus(mul(F(37,6),p(127)),mul(F(37,3),plus(p(64),mul(-1,p(1)),*(sub(p(7*j+1),p(7*j))for j in range(1,9)))))
    c=plus(p(1),p(8),mul(-1,p(7)));caps={}
    for q,b,fixed,want in[(8,0,False,138),(9,0,False,131),(10,0,False,124),(9,2,False,125),(9,2,True,124)]:
        R=plus(B,mul(-(222+q),p(7)),mul(-b,p(3)))
        if fixed:R=sub(R,mul(56,plus(p(1),p(6),mul(-1,p(7)))))
        z=divide(mul(2,R),c);need(ceil(z[0])==ceil(z[1]),'strict cap separated from integer')
        chi=111+ceil(z[1])-1;need(chi==want,'independent exact chi cap')
        caps[f'q{q}-b{b}-fixed{int(fixed)}']=dict(chi=chi,S=222-chi,Z_upper_exact=list(map(str,z)))
    weights={}
    for r in range(3,18):
        vals=[]
        for M in range(15):
            eligible=[w for w in range(M+1)if M+w<=14 and(not(M%2 or w%2)or M+w<=13)and(2*w<=14 and(w%2==0 or 2*w<=13))]
            if eligible:vals.append((M+(r-1)*max(eligible),M,max(eligible)))
        best=max(vals);need(best[0]==6*r+2,'A0 exact pair-weight optimum')
        N=r*(r-1)//2
        if r>=4:
            A2=(14*N-2*(N-r))//(r-1);A1=(13*N+1-(N-r))//(r-1)
            need(A2==6*r+2 and A1==6*r+1,'A1/A2 integer arithmetic')
        weights[str(r)]=dict(A0_max=best[0],witness=[8]+[6]*(r-1))
    fields={str(q):field(q,poly)for q,poly in[(2,3),(4,7),(8,11),(16,19)]}
    for q in(2,4):
        for z in caps.values():
            d=next(d for d in range(1,8)if z['S']*(q*q-1)<=14*(q**d-1));need(d==(5 if q==2 else 4),'finitefield quotient dimension')
    R=dict(status='PASS_INDEPENDENT_MARKED_CHAIN_COMPOSITION',marked_chi_caps=caps,fields=fields,integer_type_weights=weights,
      scope='Finite exact controls plus direct independent review of the universal proof; no source construction or new kappa.')
    (HERE/'RESULT.json').write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(R['status'])
if __name__=='__main__':main()
