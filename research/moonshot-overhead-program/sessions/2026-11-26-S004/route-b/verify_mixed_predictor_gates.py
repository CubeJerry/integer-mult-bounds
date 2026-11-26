#!/usr/bin/env python3
"""Exact mixed-error supplier checks, including rounding and adaptive sets."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
import json

COUNTS={}

def count(name,n=1):
    COUNTS[name]=COUNTS.get(name,0)+n

def rank(matrix):
    a=[list(map(F,row)) for row in matrix]
    rows,cols=len(a),len(a[0])
    r=0
    for j in range(cols):
        p=next((i for i in range(r,rows) if a[i][j]),None)
        if p is None:
            continue
        a[r],a[p]=a[p],a[r]
        z=a[r][j]
        a[r]=[x/z for x in a[r]]
        for i in range(rows):
            if i!=r and a[i][j]:
                z=a[i][j]
                a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==rows:
            break
    return r

def nearest(x):
    y=x+F(1,2)
    return y.numerator//y.denominator

def form(matrix,a,b):
    return sum(matrix[j][k]*a[j]*b[k] for j in range(len(a)) for k in range(len(b)))

def main():
    rng=Random(2026112611)
    u=8
    for n in range(1,9):
        corners=list(product((0,1),repeat=n))
        for repetition in range(8):
            permutation=list(range(n))
            rng.shuffle(permutation)
            tables=[]
            positive_tables=[]
            for i,j in enumerate(permutation):
                tables.append({key:rng.choice((-u,0,F(u,2),u,2*u))
                               for key in product((0,1),repeat=n-1)})
                positive_tables.append({key:rng.choice((-u,0))
                                        for key in product((0,1),repeat=n-1)})
            for modulus in (u//2,u):
                maxima=[0,0]
                failures=[[0]*n,[0]*n]
                for x in corners:
                    bad=[0,0]
                    for i,j in enumerate(permutation):
                        key=x[:j]+x[j+1:]
                        error=u*x[j]-tables[i][key]
                        is_bad=abs(error)>=F(modulus,2)
                        bad[0]+=is_bad
                        failures[0][i]+=is_bad
                        positive_error=u*x[j]-positive_tables[i][key]
                        assert positive_error>=0
                        is_bad=positive_error>=modulus
                        bad[1]+=is_bad
                        failures[1][i]+=is_bad
                    maxima=[max(m,b) for m,b in zip(maxima,bad)]
                    count('missing_input_corner_profiles')
                for side in range(2):
                    assert all(2*v>=len(corners) for v in failures[side])
                    assert maxima[side]>=(n+1)//2
                    count('adaptive_outlier_missing_input_bounds')
    assert all(abs(x*u-F(u,2))<F(u+1,2) for x in (0,1))
    count('oversized_interval_negative_control')

    for h in (1,2,3):
        for trial in range(25):
            u=8
            exact=[[[F(j+k==i) for k in range(h)] for j in range(h)] for i in range(2*h-1)]
            candidates=[]
            for i,matrix in enumerate(exact):
                if trial%3==0:
                    g=[row.copy() for row in matrix]
                    pairs=[(j,k) for j in range(h) for k in range(h) if j+k==i]
                    j,k=rng.choice(pairs)
                    g[j][k]=0
                else:
                    g=[[matrix[j][k]-F(rng.randrange(-3,4),4) for k in range(h)] for j in range(h)]
                candidates.append(g)
            differences=[[[x-y for x,y in zip(a,b)] for a,b in zip(hm,gm)]
                         for hm,gm in zip(exact,candidates)]
            values=[[] for _ in exact]
            rounded=[[] for _ in exact]
            corners=list(product((0,u),repeat=h))
            for a in corners:
                for b in corners:
                    for i in range(len(exact)):
                        truth=form(exact[i],a,b)
                        raw=form(candidates[i],a,b)
                        residual=truth-raw
                        rounded_residual=truth-nearest(raw)
                        assert abs(residual-rounded_residual)<=F(1,2)
                        values[i].append(residual)
                        rounded[i].append(rounded_residual)
                        count('bilinear_corner_and_rounding_values')
            samples=len(values[0])
            mu=[sum(x*x for x in row)/samples for row in values]
            fourth=[sum(x**4 for x in row)/samples for row in values]
            for i,difference in enumerate(differences):
                frobenius=sum(x*x for row in difference for x in row)
                assert mu[i]>=F(u**4,16)*frobenius
                assert fourth[i]<=9*mu[i]**2
                if rank(candidates[i])<rank(exact[i]):
                    assert frobenius>=1
                    count('rank_deficiency_distance_controls')
                count('bilinear_second_and_fourth_moments')
            for threshold in (1,4,8):
                radius=F(threshold)+F(1,2)
                outlier_budget=max(sum(abs(rounded[i][j])>=threshold for i in range(len(exact)))
                                   for j in range(samples))
                invoice=F(0)
                for i in range(len(exact)):
                    probability=F(sum(abs(x)>radius for x in values[i]),samples)
                    if mu[i]>radius**2:
                        term=(1-radius**2/mu[i])**2
                        assert probability>=term/9
                        invoice+=term
                        count('strict_tail_probability_bounds')
                assert invoice<=9*outlier_budget
                assert sum(m>=4*radius**2 for m in mu)<=16*outlier_budget
                if radius<F(u*u,4):
                    deficient=sum(rank(g)<rank(hm) for g,hm in zip(candidates,exact))
                    denominator=(1-F(16)*radius**2/u**4)**2
                    assert deficient*denominator<=9*outlier_budget
                    count('mixed_rank_defect_invoices')
                count('mixed_energy_invoices')

    result={'status':'all exact finite controls passed','seed':2026112611,
            'scope':'direct mixed-promise implications; no unrestricted multiplication lower bound',
            'counts':COUNTS}
    Path(__file__).with_name('mixed-predictor-gates-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
