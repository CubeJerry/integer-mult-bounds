#!/usr/bin/env python3
"""Exact binary controls for masked source completion; imports no author tile code."""
from argparse import ArgumentParser
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

@lru_cache(None)
def span(vectors):
    s={0}
    for v in vectors:s|={x^v for x in tuple(s)}
    return frozenset(s)

def rank(vectors):return len(span(tuple(vectors))).bit_length()-1

def apply(columns,x):
    out=0
    for k,c in enumerate(columns):
        if x>>k&1:out^=c
    return out

def compose(A,B):return tuple(apply(A,x)for x in B)
def add(A,B):return tuple(x^y for x,y in zip(A,B))
def criterion(C,D,B,b):return len(C)<=b and span(C+D)==span(B+D)

def solve(columns,value):
    # Exhaustive coefficient enumeration here is independent of the proof's
    # general Gaussian-elimination implementation; dimensions are at most two.
    for c in range(1<<len(columns)):
        if apply(columns,c)==value:return c
    raise ValueError('not in column image')

def construct(C,D,B,b):
    assert criterion(C,D,B,b)
    m=len(C);Ds=span(D)
    # Canonical representatives of quotient by im D, not rank alone.
    red=lambda v:min(v^d for d in Ds)
    Cq=tuple(red(c)for c in C);Bq=tuple(red(c)for c in B)
    piv=[];basis=[]
    for j,c in enumerate(Cq):
        if c not in span(tuple(basis)):piv.append(j);basis.append(c)
    r=len(basis);Tcols=tuple(solve(tuple(basis),v)for v in Bq)
    Trows=[sum(((v>>k)&1)<<j for j,v in enumerate(Tcols))for k in range(r)]
    assert rank(tuple(Trows))==r
    N=[]
    for j,c in enumerate(Cq):
        if j not in piv:
            coefficients=solve(tuple(basis),c)
            N.append((1<<j)^sum(((coefficients>>k)&1)<<piv[k]for k in range(r)))
    assert len(N)==m-r and all(apply(Cq,x)==0 for x in N)
    rows=Trows[:];M=[]
    for j in range(b):
        if len(rows)==m:break
        v=1<<j
        if v not in span(tuple(rows)):rows.append(v);M.append(v)
    assert len(rows)==m and rank(tuple(rows))==m
    F=[]
    for j in range(b):
        z=sum(((Tcols[j]>>k)&1)<<piv[k]for k in range(r))
        for k,v in enumerate(M):
            if v>>j&1:z^=N[k]
        F.append(z)
    F=tuple(F);assert rank(F)==m and compose(Cq,F)==Bq
    residual=add(B,compose(C,F));L=tuple(solve(D,z)for z in residual)
    assert add(compose(C,F),compose(D,L))==B
    return F,L

def main():
    ap=ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    counts={'complete_targets':0,'constructive_sources':0,'minimum_rank_projections':0,'leakage_cases':0}
    # Entire domain: n=3 output fields, m=2 independent early rows,
    # l=1 arbitrary late row, b=3 original input fields, over F2.
    b=3;m=2;q=3
    full_F=[f for f in product(range(1<<m),repeat=b)if rank(f)==m]
    all_L=list(product(range(2),repeat=b));all_B=list(product(range(1<<q),repeat=b))
    assert len(full_F)==42
    projections=[(),(1,),(2,),(3,),(4,),(5,),(6,),(7,),(1,2),(3,5)]
    for C in product(range(1<<q),repeat=m):
        CF={f:compose(C,f)for f in full_F}
        for D in product(range(1<<q),repeat=1):
            DL=[compose(D,l)for l in all_L]
            possible={add(c,d)for c in CF.values()for d in DL}
            for B in all_B:
                pred=criterion(C,D,B,b);assert pred==(B in possible)
                counts['complete_targets']+=1
                if pred:
                    construct(C,D,B,b);counts['constructive_sources']+=1
            r0=rank(C+D)-rank(D)
            for P in projections:
                project=lambda x:sum(((p&x).bit_count()%2)<<k for k,p in enumerate(P))
                observed={}
                for G in possible:
                    B=tuple(project(v)for v in G);observed[B]=min(observed.get(B,99),rank(G))
                Cp=tuple(project(v)for v in C);Dp=tuple(project(v)for v in D)
                for B in product(range(1<<len(P)),repeat=b):
                    pred=criterion(Cp,Dp,B,b);assert pred==(B in observed)
                    if pred:assert observed[B]==max(rank(B),r0)
                    counts['minimum_rank_projections']+=1
        # Exact leakage on every input-kernel vector, all listed projections.
        for F,G in CF.items():
            for P in projections:
                project=lambda x:sum(((p&x).bit_count()%2)<<k for k,p in enumerate(P))
                Cs=tuple(project(v)for v in C);Bs=tuple(project(v)for v in G)
                null=[x for x in range(1<<b)if apply(Bs,x)==0]
                leakage=rank(tuple(apply(G,x)for x in null))
                assert leakage==rank(C)-rank(Cs);counts['leakage_cases']+=1
    # Distinct source dimensions and zero boundary cases.
    zero_cases=0
    for b in range(0,4):
        for m in range(0,b+1):
            for C in product(range(4),repeat=m):
                for D in [(),(0,),(1,),(2,),(3,)]:
                    for B in product(range(4),repeat=b):
                        if criterion(C,D,B,b):construct(C,D,B,b);zero_cases+=1
    controls={}
    C=(1,2);B=(3,0)
    assert not criterion(C,(),B,2)
    assert all(criterion(tuple((c>>i)&1 for c in C),(),tuple((z>>i)&1 for z in B),2)for i in range(2))
    controls['individual_receiver_pass_joint_fail']=True
    assert span((1,1))==span((1,))and not criterion((1,1),(),(1,),1)
    controls['too_many_genuine_early_rows']=True
    assert rank((1,))==rank((2,))and not criterion((1,),(),(2,),1)
    controls['equal_dimension_wrong_image']=True
    F,L=construct((1,2),(2,),(1,0),2)
    assert rank(F)==2 and add(compose((1,2),F),compose((2,),L))==(1,0)
    controls['late_compensation_removes_real_extra_mode']={'F_columns':F,'L_columns':L}
    assert rank((1,1))==1 and rank((1,2))==2
    controls['duplicate_early_rows_are_not_independent']=True
    I=(1,2);E=(1,0)
    assert rank(add(I,E))==1 and rank(E)==1 and rank(add((0,0),E))==1
    controls['same_rank_one_perturbation_can_raise_or_lower_return_rank']=True
    out={'status':'PASS_EXACT_MASKED_SOURCE_OUTPUT_CRITERION','field':2,'main_domain':{'outputs':3,'early_rows':2,'late_rows':1,'source_bank':3},
         'counts':counts,'additional_zero_boundary_constructive_cases':zero_cases,'controls':controls,
         'finite_checks_only':True,'general_proofs':'PROOF.md','field_extension_required':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print(json.dumps(counts,sort_keys=True))
if __name__=='__main__':main()
