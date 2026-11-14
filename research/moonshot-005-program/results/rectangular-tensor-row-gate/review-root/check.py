#!/usr/bin/env python3
"""Independent integer-root intervals from independently replayed profiles."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache

def need(ok,s):
    if not ok:raise ValueError(s)

def root(n,k):
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:break
        x=y
    while pow(x,k)>n:x-=1
    while pow(x+1,k)<=n:x+=1
    return x

@lru_cache(None)
def interval(r):
    D=10**30;n=pow(r,199)*pow(D,200);z=root(n,200)
    need(pow(z,200)<=n<pow(z+1,200),'directed integer-root bound')
    return F(z,D),F(z+1,D)

def add(*parts):
    out={}
    for c,h in parts:
        for k,v in h.items():out[int(k)]=out.get(int(k),F(0))+c*F(v)
    return {k:v for k,v in out.items()if v}

def moment(h):
    lo=hi=F(0)
    for r,c in h.items():
        a,b=interval(r)
        lo+=c*(a if c>0 else b);hi+=c*(b if c>0 else a)
    return lo,hi

def hist(b,a,rows=0,price=0,n=1):
    target=add((2,{1+2*a*b:1}),*[(4,{1+j*b:1}) for j in range(1,a+1)])
    paid=add((4,{1:1}),(8*a,{b:1}),*[(4,{j*b:1}) for j in range(1,a)])
    if rows:paid=add((1,paid),(F(4*a*rows,n),{price:1}))
    return add((1,target),(-1,paid))

def qrank(rows):
    from math import gcd
    a=[list(r) for r in rows]
    if not a:return 0
    r=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];v=a[r][j]
        for i in range(r+1,len(a)):
            w=a[i][j]
            if w:
                a[i]=[v*x-w*y for x,y in zip(a[i],a[r])]
                divisor=0
                for x in a[i]:divisor=gcd(divisor,x)
                if divisor:a[i]=[x//divisor for x in a[i]]
        r+=1
        if r==len(a):break
    return r
def brank(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return len(piv)

def main():
    p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='b5a732709aab1eec0bec173a7011f1e0509c4251ccc1159b1c06bbb5cf45fef0','frozen proof')
    reports=[];budgets=[];author=json.loads((a.package/'RESULT.json').read_text())
    for g,lam in [(2,F(1)),(3,F(4,3)),(4,F(3,2))]:
        labels=[v for v in range(1<<g) if v.bit_count()%2];n=len(labels)
        Q=[[(x&y).bit_count()%2 for y in labels] for x in labels]
        binary=[sum(v<<j for j,v in enumerate(row)) for row in Q]
        subsets=[[i for i in range(n) if mask>>i&1] for mask in range(1<<n)]
        count=0;maximum=F(0);witness=None
        for dm,D in enumerate(subsets):
            for sm,S in enumerate(subsets):
                r2=brank([binary[i]&sm for i in D]);r0=qrank([[Q[i][j] for j in S] for i in D]);count+=1
                need(r0<=lam*r2,'all ordered rectangles obey exact rank ratio')
                if r2 and F(r0,r2)>maximum:maximum=F(r0,r2);witness=dict(D=D,S=S,rational_rank=r0,binary_rank=r2)
        need(maximum==lam and count==2**(2*n),'sharp constant and complete ordered domain')
        reports.append(dict(g=g,ordered_rectangles=count,sharp_lambda=str(lam),witness=witness,rank_method='exact integer elimination with row gcd normalization'))
        lower={7*g:F(8,104*g)/lam};gap=moment(add((1,hist(9*g-1,9)),(-36,lower)))
        need(gap[1]<0,'strict retained-caller rejection')
        prev=list(map(F,author['budgets'][str(g)]['retained18_gap_upper_bound']['exact']))
        need(gap[0]<=prev[0]<=prev[1]<=gap[1],'independent budget encloses author')
        budgets.append(dict(g=g,h=9*g,upper_gap=list(map(str,gap)),upper_gap_decimal=float(gap[1])))
    changed=moment(hist(17,4,8,14,208));need(changed[0]>0,'changed eight-stage positive scope control')
    labels=[1,2,4,7];u=[F(1,3),F(2,3),F(2,3)]
    need(sum(x*x for x in u)==1 and all((labels[i]&7).bit_count()%2 and u[i]!=0 for i in range(3)),'unit Gram violates three forbidden pairs')
    report=dict(status='PASS_INDEPENDENT_RECTANGULAR_TENSOR_GATE',rectangle_certificates=reports,budgets=budgets,changed_eight_stage_interval=list(map(str,changed)),negative_control='three nonzero forbidden Gram pairs despite correct diagonal',scope='Direct tensor rows and retained18-stage caller; g>=5 uses separately reviewed free-decoder dimension gate. Changed callers and shared ascents remain open; no new kappa.')
    a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()

