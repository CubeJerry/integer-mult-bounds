#!/usr/bin/env python3
"""Exact complete vertex proof and finite ratio-subgroup controls."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
import hashlib,json


def convolution(a,b,r):
    out=Counter()
    for i,x in a.items():
        for j,y in b.items():
            out[(i+j)%r]+=x*y
    return out


def main():
    counts=Counter()
    expected={0:[96,16,64,64,16],1:[48,56,48,48,56],
              2:[56,52,48,48,52],3:[60,54,44,44,54],4:[70,57,36,36,57]}
    vertices=[]
    for r,ell,minimum in ((5,4,Fraction(1,16)),(3,2,Fraction(1,4))):
        for ps in product((Fraction(0),Fraction(1,2)),repeat=ell):
            dist=Counter({0:Fraction(1)})
            for p in ps:
                dist=convolution(dist,{0:p,1:(1-p)/2,r-1:(1-p)/2},r)
            assert sum(dist.values())==1
            assert all(dist[i]>=minimum for i in range(r))
            counts['complete_multiaffine_vertices']+=1
            counts['individual_vertex_root_masses']+=r
            if r==5:
                h=sum(bool(p) for p in ps)
                assert [dist[i]*256 for i in range(5)]==expected[h]
                vertices.append({'p':[str(p) for p in ps], 'numerators_over_256':expected[h]})
    for qs in product((2,4,8,16),repeat=4):
        dim=1
        dist=Counter({0:1})
        for q in qs:
            dist=convolution(dist,{0:q,1:q*(q-1)//2,4:q*(q-1)//2},5)
            dim*=q*q
        g=min(dist[i] for i in range(5))
        assert 16*g>=dim
        assert sum(dist.values())==dim
        residual={i:dist[i]-g for i in range(5)}
        assert all(v>=0 for v in residual.values())
        assert 5*g+sum(residual.values())==dim
        counts['actual_integer_multiplicity_matchings']+=1
    # Every normalized subset T contains zero. Exhaust all up to C_12.
    for ambient in range(2,13):
        for rest in range(1<<(ambient-1)):
            t={0}|{j+1 for j in range(ambient-1) if rest>>j&1}
            step=ambient
            for j in t:
                step=gcd(step,j)
            d=ambient//step
            subgroup=set(range(0,ambient,step))
            powers={0:()}
            for k in range(d-1):
                nxt={}
                for a,word in powers.items():
                    for b in t:
                        nxt.setdefault((a+b)%ambient,word+(b,))
                if len(powers)<d:
                    assert len(nxt)>len(powers)
                    counts['strict_growth_before_subgroup_completion']+=1
                assert set(powers)<=set(nxt)
                powers=nxt
                counts['set_product_expansion_steps']+=1
            assert set(powers)==subgroup
            assert all(len(word)==d-1 and sum(word)%ambient==a for a,word in powers.items())
            counts['all_normalized_subsets_through_order_12']+=1
            counts['explicit_distinct_product_witness_words']+=len(powers)
    # Ambient order four pair exposes only a ratio subgroup of order two.
    distribution=Counter({0:1})
    for _ in range(6):
        distribution=convolution(distribution,{1:1,3:1},4)
    assert len(distribution)==2 and max(distribution.values())==32
    actual_error=Fraction(64-max(distribution.values()),64)
    assert actual_error==Fraction(1,2)<Fraction(3,4)
    result={'status':'passed','arithmetic':'exact integer and rational',
            'counts':dict(counts),'all_order_five_vertices':vertices,
            'negative_control':'ambient order4 pair has degree-zero error1/2, rejecting3/4',
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Complete16-vertex physical proof; general ratio-subgroup result has the separate set-growth proof'}
    Path('subset-spectrum-refinements-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='all_order_five_vertices'},indent=2))


if __name__=='__main__':
    main()
