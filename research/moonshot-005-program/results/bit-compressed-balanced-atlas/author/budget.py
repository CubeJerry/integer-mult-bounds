#!/usr/bin/env python3
"""Exact movement thresholds and finite binary invoices for the compressed atlas."""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction as F
from functools import cache
from pathlib import Path
import json


@cache
def root(n):
    s=10**24;t=n**199*s**200;l=0;h=n*s+1
    while h-l>1:
        m=(l+h)//2
        if m**200<=t:l=m
        else:h=m
    assert l**200<=t<h**200
    return F(l,s),F(l if l**200==t else h,s)


def combine(*terms):
    out=defaultdict(F)
    for c,p in terms:
        for n,v in p.items():out[n]+=c*v
    return out


def interval(p):
    lo=hi=F(0)
    for n,c in p.items():
        l,h=root(n);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
    return lo,hi


def mod(a,b):
    while a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
    return a


def gcd(a,b):
    while b:a,b=b,mod(a,b)
    return a


def square_mod(x,p):
    a=0
    for k in range(x.bit_length()):
        if x>>k&1:a^=1<<(2*k)
    return mod(a,p)


def first_irreducible(n):
    factors={q for q in range(2,n+1) if n%q==0 and all(q%d for d in range(2,int(q**.5)+1))}
    tested=0
    for p in range((1<<n)+1,1<<(n+1),2):
        tested+=1;x=2;ok=True
        for k in range(1,n+1):
            x=square_mod(x,p)
            if k in {n//q for q in factors} and gcd(x^2,p)!=1:ok=False;break
        if ok and x==2:return {'degree':n,'modulus_integer':p,'modulus_hex':hex(p),'candidates_checked':tested}
    raise AssertionError('irreducible polynomial exists')


def main():
    ap=ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    P=combine((36,N),(1,{1:444}),*((1,{7*j:444}) for j in range(1,9)))
    T=combine((36,H),(1,{127:222}),*((1,{1+7*j:444}) for j in range(1,10)))
    Q={1:F(4451,8),2:F(7213,16),4:F(24),8:F(9)}
    limiting=combine((F(1,36),T),(-F(1,36),P),(1,N),(-1,H))
    room=interval(combine((1,limiting),(-1,Q)));b8=root(8)
    cap=[1920*room[0]/b8[1],1920*room[1]/b8[0]]
    assert 67<cap[0]<cap[1]<68
    cases=[]
    for r in [0,31,62,63,67,68]:
        profile=combine((1,Q),(F(r,1920),{8:1}));slack=interval(combine((1,limiting),(-1,profile)))
        if slack[1]<0:
            cases.append({'excess':r,'first_even_m':None,'limiting_room':list(map(str,slack))});continue
        assert slack[0]>0
        offset=interval(combine((18,N),(-18,H),(-18,profile)))
        slope=(18*slack[0],18*slack[1]);bound=offset[1]/slope[0]
        first=max(2,2*(bound//2)+2)
        def gap(m):return interval(combine((F(m,2),T),(-F(m,2),P),(-18*(m-1),H),(18*(m-1),N),(-18*(m-1),profile)))
        assert gap(first)[0]>0 and (first==2 or gap(first-2)[1]<0)
        cases.append({'excess':r,'first_even_m':first,'limiting_room':list(map(str,slack)),
                      'first_gap':list(map(str,gap(first))),'previous_gap':list(map(str,gap(first-2))) if first>2 else None})
    invoices={}
    for w in [5,27,28,30]:
        M=111*1920*w;C=9*1920*w
        invoices[w]={'M':M,'C':C,'ADD':17*M*M+50*M+111*C,'INIT':5*M+C,'dirty_CLEAR':5*M+C,
                     'peak_public_and_auxiliary':7*M+C,
                     'MOVE':{'1':1068240*w,'2':865560*w,'4':46080*w,'8':17280*w},
                     'generic_all_foreign_invertibility_proved':w>=27,
                     'twenty_three_common_rows_proved':w>=28}
    result={'status':'PASS_EXACT_COMPRESSED_ATLAS_BUDGET','base_bank':1920,
            'limiting_room':list(map(str,room)),'real_excess_threshold':list(map(str,cap)),
            'integer_excess_limit':67,'cases':cases,'invoices':invoices,
            'field_polynomials':[first_irreducible(27),first_irreducible(28)],
            'generic_degree':128486400,'mixed23_downstream_degree':220843360,
            'mixed23_per_donor_source_degree':120960,'normalization':'All1920 field coordinates and every binary extension copy.',
            'complete_native_map_constructed':False,'new_complete_kappa':False}
    assert result['generic_degree']<2**27 and result['mixed23_downstream_degree']<2**28
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'BUDGET.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print([(z['excess'],z['first_even_m']) for z in cases]);print(result['field_polynomials'])


if __name__=='__main__':main()
