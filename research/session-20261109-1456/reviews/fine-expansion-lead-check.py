"""Independent exact checks of the full-period expansion admission.

This is an arithmetic/source review, not a production Tile execution.
Prepared for @CubeJerry with substantial OpenAI assistance.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib,importlib.util,json
from math import isqrt,prod
from pathlib import Path
import sys

ROOT=Path('/workspace/scratch/a365d332d434/worker-analytic-wave9')
PKG=ROOT/'research/fine-expansion-page-admission';sys.path.insert(0,str(PKG))
from admission import Certificate

headers=blocks=quadratics=halo_cases=fine_theta_cases=0
for q in (101,127,256,509):
    c=isqrt(q);c+=c*c<q
    for alpha in sorted({2,3,isqrt(q-1)}):
        for s in (2,3,5,11,37,101,1009):
            for e in sorted({1,s//2,s-1}):
                t=s+e;b=alpha*c;P=32768*q;sigma=4096*q
                cert=Certificate.make(s,t,alpha,q)
                assert (cert.b,cert.P,cert.sigma,cert.source_start,cert.source_count)==(b,P,sigma,-b-1,s+2*b+3)
                assert 3*b+3<4*q and 4*b+2<5*q
                assert P>=2*sigma+q+(32*(3*b+4)-1).bit_length()+12
                assert P-4256*q>=2 and 3936*q>=2 and P-96*q>=2
                windows=[]
                for v in range(0,t,b):
                    m=min(b,t-v);j0=s*v//t;gamma=F(j0)-F(s*v,t)
                    lo=j0-b-1;hi=-(-s*(v+m-1)//t)+b+2
                    row=cert.block(v,m)
                    assert (row['start'],row['end'],row['n'],row['nc'])==(lo,hi,hi-lo,hi-lo+m-1)
                    assert -b-1<=lo<hi<=s+b+2
                    assert hi-lo<=3*b+3 and hi-lo+m-1<=4*b+2
                    h0,h1=lo-j0,hi-j0-1;k=F(s,t);u=alpha*alpha
                    assert h1<=m+b+1<=2*b+1
                    for h in sorted({h0,h1,0}):
                        for z in sorted({0,m//2,m-1}):
                            U=((1-k)*h*h+2*gamma*h+gamma*gamma)/u
                            V=((k*k-k)*z*z-2*gamma*k*z)/u
                            K=k*(h-z)*(h-z)/u
                            assert U+V+K==(h-k*z+gamma)**2/u
                            assert abs(U)<20*q and abs(V)<3*q and 0<=K<12*q
                            quadratics+=1
                    windows.append((lo,hi));blocks+=1
                assert windows[0][0]==-b-1 and windows[-1][1]==s+b+2
                assert all(a[0]<=b_[0]<=a[1] and a[1]<=b_[1] for a,b_ in zip(windows,windows[1:]))
                counts=Counter(j%s for j in range(-b-1,s+b+2))
                for residue in (0,s//2,s-1):
                    lower=-((-b-1-residue)//s)
                    # Direct floor count of integer lifts in the half-open halo.
                    direct=(s+b+1-residue)//s-((-b-2-residue)//s)
                    assert counts[residue]==direct;halo_cases+=1
                fine_theta_cases+=alpha*alpha*e<s;headers+=1

# The all-q reasoning uses c<=1.1sqrt(q), H=2c+1<=2.3sqrt(q).
# These independent integer checks are support, not the universal proof.
width_checks=0
for q in range(101,10001):
    c=isqrt(q);c+=c*c<q;H=2*c+1
    assert 100*c*c<=121*q and 100*H*H<=529*q
    assert F(H*H,2)+H+F(1,4)<3*q
    assert F(c*c,4)+c<F(q,2) and H*H<6*q
    width_checks+=1

unit_cases=0
for R in range(1,33):
    unit=1<<R
    for factor in (1,2,3,7,29):
        lower=unit*factor
        assert (lower*lower)//unit>=unit
        ceiling=-(-(unit*unit)//lower)
        assert ceiling<=unit
        for P in (0,R//2,R):
            shift=R-P;out=-(-ceiling//(1<<shift))
            assert out<=1<<P;unit_cases+=1

budget_cases=route_cases=0
for D in range(1,65):
    for J in (0,1,7,100):
        Kf=D+J;Kc=3*D;Gamma=Kf+Kc
        for tau in (1,7,40):
            q=Gamma+tau+5
            bound=F(3,2)*(1<<Gamma)*(12*F(1,1<<J)+2)*F(1,1<<q)
            assert bound<F(1,1<<tau);budget_cases+=1
for D in range(1,31):
    t=[1<<(6+(i%3)) for i in range(D)];s=[n-1 for n in t]
    S,T=prod(s),prod(t);assert T<2*S
    volumes=[prod(t[:i])*prod(s[i:]) for i in range(D+1)]
    assert 2*sum(volumes[1:])>D*T
    ell=[n.bit_length()-1 for n in t]
    assert sum(e*v for e,v in zip(ell,volumes[1:]))>=S*sum(ell)
    route_cases+=1

helper=Path('/workspace/scratch/a365d332d434/query-optimum/scripts');sys.path.insert(0,str(helper))
sp=importlib.util.spec_from_file_location('gate',helper/'check_research_commit.py');gate=importlib.util.module_from_spec(sp);sp.loader.exec_module(gate)
gate.check(ROOT,'research/fine-expansion-page-admission','HEAD',False,True)
result=dict(local_commit='5ce120aa71b3133f98a89203c4e2b95d054b04d5',proof_sha256=hashlib.sha256((PKG/'PROOF.md').read_bytes()).hexdigest(),header_cases=headers,block_cases=blocks,quadratic_cases=quadratics,halo_lift_count_cases=halo_cases,u_theta_below_one_headers=fine_theta_cases,integer_envelope_checks=width_checks,reciprocal_unit_cases=unit_cases,source_first_budget_cases=budget_cases,route_lower_bill_cases=route_cases,source_byte_mode_gate=True,limits=['production coefficient/Tile execution not repeated','actual return-codec evidence separately reviewed','canonical Poisson/permutation/S-squared identity already in#4320','source-relative slow reference; no fast prefix, global closure or new kappa'])
Path(__file__).with_name('fine-expansion-lead-review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
