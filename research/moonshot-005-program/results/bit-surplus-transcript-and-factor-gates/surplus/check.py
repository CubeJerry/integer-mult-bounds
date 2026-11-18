#!/usr/bin/env python3
"""Exact two surplus-transcript duals at t=199/200. No optimizer is used."""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

PRICES=Path('research/moonshot-005-program/results/bit-low-exterior-formation-gate/author/output/RESULT.json')
SOURCE_PRICE_PIN='befef29e616a3adebe070251a87c6f85c94a81bf687db2dceafdbbf067017145'
WITNESS_CAP_PIN='53c24f54797de879e48c459fe804e1a9a18b96a75e55d6954800784411319912'
DUALS=[
    ([Q('.99308'),Q('.72026'),Q('.33149'),Q('.92753')],Q('.73402'),Q('4.46267')),
    ([Q('.99308'),Q('.58187'),Q('.26856'),Q('.74999')],Q('.58717'),Q('2.51092'))]

def need(ok,why):
    if not ok:raise ValueError(why)

def pinned(path,expected):
    b=path.read_bytes();need(hashlib.sha256(b).hexdigest()==expected,str(path));return json.loads(b)

def price(g):
    if g in (0,1):return Q(g),Q(g)
    scale=10**40;v=g**199*scale**200;lo=0;hi=8*scale+1
    while hi-lo>1:
        m=(lo+hi)//2
        if m**200<=v:lo=m
        else:hi=m
    return Q(lo,scale),Q(hi,scale)

def validate(cap,dual):
    w,beta,eta=dual;tariffs=[price(n)for n in range(9)]
    layers=dict(zip((2,3,4,5),w));own=[];pub=[];du=[];ex=[];negative=[]
    for s in range(1,9):
        for d in range(s):
            crossing=sum(v for r,v in layers.items() if d<=r<s)
            need(crossing**200<=(s-d)**199,'exterior crossing price')
            ex.append([s,d,str(crossing)])
            vdest=min(d,1)
            high=sum(v for r,v in layers.items() if r<s)
            tail=sum(v for r,v in layers.items() if r>=s)
            for inside in (False,True):
                a=cap[s] if s<len(cap) else Q(1)
                charge=1+high+(a*tail if inside else 0)
                slack=eta*(1-a) if inside else Q(0)
                net=charge-slack
                need(net<=0 or net**200<=(s-vdest)**199,'virtual DU gap+miss bound')
                du.append([s,d,inside,str(net)])
                if inside and charge>tariffs[s-vdest][1]:negative.append([s,d])
    need(negative,'omitting the entropy-deficit budget must fail')
    for s in range(1,6):
        for a in range(s):
            demand=cap[a]*sum(v for r,v in layers.items()if r>=s)
            need(demand**200<=(s-a)**199,'owned inlet')
            premium=tariffs[a][0]+tariffs[s-a][0]+tariffs[7-s][0]-tariffs[7][1]
            need(demand<=beta+premium,'axis inlet and split premium')
            own.append([a,s,str(demand)]);pub.append([a,s,str(premium)])
    return {'weights_by_rank_2_to_5':list(map(str,w)),'axis_allowance':str(beta),'entropy_deficit_multiplier':str(eta),
            'all_virtual_DU_and_inside_source_prices':du,'all_exterior_down_prices':ex,
            'all_owned_inlet_loads':own,'all_public_premium_lower_bounds':pub,
            'deleting_miss_credit_breaks_some_price':negative[:3]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--coverage',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    prices=pinned(a.repo/PRICES,SOURCE_PRICE_PIN);geo=pinned(a.coverage,WITNESS_CAP_PIN)
    num=geo['total_witness_weight'];cap=[Q(0)]+[Q(z[2],num)for z in geo['ternary_outer_flat_counts_and_maximum_hits'][:4]]+[Q(1)]*4
    need(cap[1:5]==[Q(x,999993)for x in [191805,387630,610722,827177]],'reviewed geometric caps')
    result={'status':'PASS_NONLINEAR_SURPLUS_TRANSCRIPT_AND_DESTINATION_TARIFF','coverage_sha256':WITNESS_CAP_PIN,
            'caps_by_origin_rank':list(map(str,cap)),'duals':[validate(cap,d)for d in DUALS],
            'symbolic_bill':'9b sum(w)+(9b+s)+8b-8b beta-eta*s-Delta_destination',
            'Delta_destination':'sum over receiver-downset MOVEs of [origin-min(destination,1)]-[origin-destination]',
            'strict_scalar_cases':[]}
    roomlo,roomhi=map(Q,prices['sources'][0]['normalized_room']['rational'])
    for s,allowed in [(1,3),(2,1),(3,0)]:
        best=max(9*sum(w)+9+s+8-8*beta-eta*s for w,beta,eta in DUALS)
        need(best-allowed>roomhi,'integer rank-excess strict exclusion')
        result['strict_scalar_cases'].append({'transcript_events':9+s,'all_rank_one_or_ground_lower_bill':str(best),
            'largest_certified_integer_endpoint_rank_excess':allowed,'remaining_strict_margin':str(best-allowed-roomhi),
            'exact_destination_adjustment_limiting_margin':[str(best-roomhi),str(best-roomlo)]})
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS 10/11/12 nonlinear scalar bills 34.41641, 32.62230, 31.11138 before exact endpoint correction')

if __name__=='__main__':main()
