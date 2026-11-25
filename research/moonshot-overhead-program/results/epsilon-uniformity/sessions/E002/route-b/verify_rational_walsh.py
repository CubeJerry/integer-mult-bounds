#!/usr/bin/env python3
"""Finite exact support for W1/W2, not physical tape execution."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json

def scale(a,b,x):
    assert b>0
    p=0
    for bit in range(abs(a).bit_length()):
        if (abs(a)>>bit)&1:p+=abs(x)<<bit
    quotient=remainder=0
    for bit in range(p.bit_length()-1,-1,-1):
        remainder=2*remainder+((p>>bit)&1)
        qbit=int(remainder>=b)
        if qbit:remainder-=b
        quotient=2*quotient+qbit
        assert 0<=remainder<b
    return -quotient-int(remainder!=0) if a*x<0 else quotient

def binom_integer(a,d):
    b=1
    for h in range(1,d+1):
        numerator=b*(a-h+1)
        assert numerator%h==0
        b=numerator//h
    return b

def inverse(a):
    n=len(a)
    z=[[Q(v) for v in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if z[i][j])
        z[j],z[pivot]=z[pivot],z[j]
        c=z[j][j];z[j]=[v/c for v in z[j]]
        for i in range(n):
            if i!=j:
                c=z[i][j];z[i]=[v-c*w for v,w in zip(z[i],z[j])]
    return [row[n:] for row in z]

def mv(a,x):return [sum((c*d for c,d in zip(row,x)),Q(0)) for row in a]
def transpose(a):return [list(col) for col in zip(*a)]

def spectral(m,u,d,bits):
    width=1<<m.bit_length();counts=[];values=[];z=(-1)**sum(bits)
    for seed in range(width):
        beta=[(j&seed).bit_count()%2 for j in range(1,m+1)]
        c=sum(k^b for k,b in zip(bits,beta))
        p=(-1)**((u-sum(beta))%2)*sum((-2)**h*binom_integer(c-u,h) for h in range(d+1))
        assert p%2==1
        counts.append(c);values.append(p)
    return counts,values,z

def main():
    counts=dict(signed_scalings=0,signed_grid_roundings=0,negative_binomials=0,
                predictor_cases=0,complete_repair_basis_identities=0,
                zero_gap_rejections=0,wrong_transpose_rejections=0,empty_defect_cases=0)
    for a in range(-25,26):
        for b in range(1,32):
            for x in range(-64,65):
                y=scale(a,b,x);exact=Q(a*x,b)
                assert y==exact.numerator//exact.denominator
                counts['signed_scalings']+=1
                for p in (0,3,9):
                    error=exact/(1<<p)-Q(y,1<<p)
                    assert 0<=error<Q(1,1<<p)
                    counts['signed_grid_roundings']+=1
    for a in range(-30,31):
        for d in range(21):
            expected=comb(a,d) if a>=0 else (-1)**d*comb(-a+d-1,d)
            assert binom_integer(a,d)==expected
            counts['negative_binomials']+=int(a<0)
    max_height=0
    # Toy windows use s=|J|, not the source asymptotic phase invoice.
    for m,u,d in [(3,1,1),(5,1,3),(7,2,3),(5,0,0)]:
        width=1<<m.bit_length();nodes=[Q(i,width) for i in range(width)]
        for code in range(1<<m):
            bits=[(code>>j)&1 for j in range(m)]
            cs,ps,z=spectral(m,u,d,bits);js=[i for i,p in enumerate(ps) if p!=z]
            counts['predictor_cases']+=1
            if not js:
                counts['empty_defect_cases']+=1
                assert all(p==z for p in ps)
                continue
            ell=len(js);h=[[node**row for node in nodes] for row in range(ell)]
            v=[[row[i] for i in js] for row in h];inv=inverse(v);invt=inverse(transpose(v))
            for row in inv+invt:
                for val in row:max_height=max(max_height,val.numerator.bit_length(),val.denominator.bit_length())
            for basis in range(width):
                x=[Q(i==basis) for i in range(width)];px=[p*xx for p,xx in zip(ps,x)]
                checks=mv(h,x);checks_p=mv(h,px)
                delta=[b-z*a for a,b in zip(checks,checks_p)];e=mv(inv,delta)
                needed=[ee/(ps[i]-z) for i,ee in zip(js,e)]
                aa=mv(invt,needed);zz=mv(transpose(h),aa)
                actual=[p*xx-p*c+z*c for p,xx,c in zip(ps,x,zz)]
                assert actual==[z*xx for xx in x]
                counts['complete_repair_basis_identities']+=1
                wrong=mv(inv,needed);badzz=mv(transpose(h),wrong)
                bad=[p*xx-p*c+z*c for p,xx,c in zip(ps,x,badzz)]
                counts['wrong_transpose_rejections']+=int(bad!=actual)
            if any(p==z for p in ps):
                try:[Q(1,p-z) for p in ps]
                except ZeroDivisionError:counts['zero_gap_rejections']+=1
                else:raise AssertionError('zero-gap division was not rejected')
    for code in range(32):
        _,ps,z=spectral(5,0,5,[(code>>j)&1 for j in range(5)])
        assert all(p==z for p in ps)
        counts['empty_defect_cases']+=1
    assert counts['zero_gap_rejections'] and counts['wrong_transpose_rejections']
    report=dict(status='PASS_FINITE_RATIONAL_WALSH_COMPONENTS',counts=counts,
                maximum_tested_inverse_coefficient_height=max_height,
                source_pin='3344da59991ed94f9ba711217b29c1d760badfa6',
                scope='Exact finite rounding, signed count and repair identities. Toy s=|J|; no phase-invoice, physical tape, full multiplier, asymptotic or Lean verification.')
    Path(__file__).with_name('rational-walsh-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
