#!/usr/bin/env python3
"""Small-factor rank certificates and rectangular tensor caller gate.

No imported scientific implementation. All characteristic-zero ranks are
proved by a prime larger than a uniform Hadamard bound for every minor.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from collections import Counter
import argparse,json
P=65537
DEN=10**45
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def rank2(rows):
    basis={}
    for x in rows:
        while x:
            i=x.bit_length()-1
            if i in basis:x^=basis[i]
            else:basis[i]=x;break
    return len(basis)

def rank0(a):
    """Exact Q rank for binary matrices with <=8 rows and columns."""
    if not a or not a[0]:return 0
    need(len(a)<=8 and len(a[0])<=8 and all(v in (0,1)for row in a for v in row),'binary rank domain')
    # Every integer k-minor has |det|<=k^(k/2)<=8^4=4096<P.
    need(8**4<P,'uniform determinant bound')
    a=[row[:]for row in a];r=0
    for c in range(len(a[0])):
        k=next((i for i in range(r,len(a))if a[i][c]%P),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        u=pow(a[r][c],-1,P)
        a[r]=[(z*u)%P for z in a[r]]
        for i in range(r+1,len(a)):
            q=a[i][c]
            if q:a[i]=[(x-q*y)%P for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def rectangle_certificate(g,lambda_):
    labels=[q for q in range(1<<g)if q.bit_count()%2]
    n=len(labels);Q=[[(x&y).bit_count()%2 for y in labels]for x in labels]
    bitrows=[sum(v<<j for j,v in enumerate(row))for row in Q]
    subsets=[[i for i in range(n)if m>>i&1]for m in range(1<<n)]
    maximum=F(0);witness=None;checked=0;dist=Counter()
    for dm,D in enumerate(subsets):
        for sm in range(dm,1<<n):
            S=subsets[sm]
            b=rank2([bitrows[i]&sm for i in D])
            r=rank0([[Q[i][j]for j in S]for i in D])
            need(F(r)<=lambda_*b,'rank certificate fails')
            checked+=1;dist[f'{b},{r}']+=1
            if b and F(r,b)>maximum:
                maximum=F(r,b);witness={'D':[labels[i]for i in D],'S':[labels[j]for j in S],'binary_rank':b,'rational_rank':r}
    need(maximum==lambda_,'sharp certificate constant')
    return dict(g=g,odd_labels=labels,lambda_=str(maximum),cost_mass_lower_bound=str(1/maximum),
                rectangles_checked_up_to_transpose=checked,ordered_rectangles=(1<<n)**2,
                witness=witness,rank_pair_census=dict(sorted(dist.items())))

def root_floor(z,k):
    if z<2:return z
    x=1<<((z.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+z//x**(k-1))//k
        if y>=x:break
        x=y
    while x**k>z:x-=1
    while (x+1)**k<=z:x+=1
    need(x**k<=z<(x+1)**k,'certified integer root')
    return x

@lru_cache(None)
def power(r):
    if r==1:return F(1),F(1)
    z=r**199*DEN**200;a=root_floor(z,200)
    return F(a,DEN),F(a+1,DEN)

def plus(*xs):return sum(x[0]for x in xs),sum(x[1]for x in xs)
def scale(q,x):
    q=F(q);return (q*x[0],q*x[1])if q>=0 else(q*x[1],q*x[0])
def show(x):return dict(exact=[str(z)for z in x],decimal=[float(z)for z in x])
def free(b,a):
    return plus(scale(2,power(1+2*a*b)),scale(4,power(1+a*b)),scale(-4,power(1)),scale(-8*a,power(b)),
                *(plus(scale(4,power(1+j*b)),scale(-4,power(j*b)))for j in range(1,a)))

def main(out):
    certs={str(g):rectangle_certificate(g,lam)for g,lam in [(2,F(1)),(3,F(4,3)),(4,F(3,2))]}
    budgets={}
    for g,c in [(2,F(1)),(3,F(3,4)),(4,F(2,3))]:
        # R(P104)/104 * (g^(t-1)*c) = (8c/(104g))*(7g)^t.
        lower=scale(F(8,104)*c/g,power(7*g))
        gap=plus(free(9*g-1,9),scale(-36,lower))
        need(gap[1]<0,'all direct rectangular factors fail retained caller')
        budgets[str(g)]=dict(h=9*g,mass_density_floor=str(c),owned_moment_density_lower_bound=show(lower),
                            retained18_gap_upper_bound=show(gap))
    # A legal factor: the three axis ports share one decoder direction,
    # while111 is orthogonal. The price is3+1, not3.
    labels=[1,2,4,7];Q=[[(x&y).bit_count()%2 for y in labels]for x in labels]
    legal=[[1 if i<3 and j<3 else int(i==j)for j in range(4)]for i in range(4)]
    need(all(Q[i][j]*legal[i][j]==int(i==j)for i in range(4)for j in range(4)),'legal four-label control')
    need(rank2([sum(Q[i][j]<<j for j in range(3))for i in range(3)])==3,'legal leaf row price3')
    u=[F(1,3),F(2,3),F(2,3)]
    need(sum(x*x for x in u)==1,'rejected rational Gram has correct diagonal')
    G=[[F(int(i==j))for j in range(4)]for i in range(4)]
    for i in range(3):G[i][3]=G[3][i]=u[i]
    faults=[dict(i=i,j=j,value=str(G[i][j]))for i in range(4)for j in range(4)if i!=j and Q[i][j]and G[i][j]]
    need(len(faults)==6,'six forbidden odd-cell entries reject Gram proposal')
    need(rank0(Q)==4 and rank2([sum(v<<j for j,v in enumerate(row))for row in Q])==3,'characteristic-zero/binary rank control')
    # Retain an escape: a changed shorter caller is not excluded by this theorem.
    changed=plus(free(17,4),scale(-16,scale(F(8,208),power(14))))
    need(changed[0]>0,'changed eight-stage invoice remains arithmetically open')
    result=dict(status='PASS_RECTANGULAR_TENSOR_ROW_GATE',small_factor_certificates=certs,
        budgets=budgets,rejected_four_label_Gram=dict(unit_vector=list(map(str,u)),forbidden_entries=faults),
        legal_four_label_control=dict(decoder=legal,row_prices=[3,1],mass=4),
        changed_eight_stage_relaxation=show(changed),
        scope='For direct tensoring of the displayed P104 rows with any characteristic-zero row decoder on odd labels spanning F2^g, every g>=2 fails the retained18-stage caller. g>=5 uses the separately proved free-decoder h>=38 gate. Shared ascents, different callers and other native constructions are not excluded.',
        kappa_status='No new kappa.')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'rectangles':sum(x['rectangles_checked_up_to_transpose']for x in certs.values()),'out':str(out)},sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();main(a.output)
