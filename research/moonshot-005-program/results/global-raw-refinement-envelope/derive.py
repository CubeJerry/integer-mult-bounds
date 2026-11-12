#!/usr/bin/env python3
"""Exact H4 envelope for arbitrary monotone refinement of all400 raw paths.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip,hashlib,json
from pathlib import Path

SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'

def need(ok,msg):
    if not ok:raise ValueError(msg)

def floor_root(n,k):
    lo,hi=0,1<<((n.bit_length()+k-1)//k)
    while lo+1<hi:
        m=(lo+hi)//2
        if m**k<=n:lo=m
        else:hi=m
    return lo

def main(a):
    source=a.source.read_bytes();invoice=a.invoice.read_bytes()
    need(hashlib.sha256(source).hexdigest()==SOURCE,'source pin')
    need(hashlib.sha256(invoice).hexdigest()==INVOICE,'invoice pin')
    w=json.loads(gzip.decompress(source));bill=json.loads(invoice)
    main=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
    need(len(main)==400,'complete raw domain')
    need(all(len(w['frames'][w['final'][r]])-len(w['frames'][w['initial'][r]])==8 for r in main),'each path has net rank8')
    old=Counter(abs(len(w['frames'][o[2]])-len(w['frames'][o[3]])) for o in w['program'] if o[0]=='MOVE' and o[1] in main)
    need(dict(old)=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'original raw census')
    need(sum(r*c for r,c in old.items())==3200,'complete raw rank mass')
    T={int(k):v for k,v in bill['T4'].items()};P0={int(k):v for k,v in bill['P4'].items()}
    denominator=10**30
    powers={}
    for r in set(T)|set(P0)|{9}:
        n=r**199*denominator**200;lo=floor_root(n,200)
        powers[r]=(lo,lo if lo**200==n else lo+1)
    cases={}
    for label,straight,extra in [('direct_baseline',400,0),('all_unit',0,0),('all_unit_plus16',0,16),('24_direct_plus16',24,16),('25_direct_plus16',25,16)]:
        replacement=Counter({8:straight,1:8*(400-straight)})
        replacement+=Counter() # remove zero counts
        paid=Counter(P0)
        for r,c in old.items():paid[r]-=18*c
        for r,c in replacement.items():paid[r]+=18*c
        paid[9]+=18*8;paid[1]+=18*extra
        need(all(c>=0 for c in paid.values()),'complete nonnegative histogram')
        lo=hi=0
        for r in set(T)|set(paid):
            d=T.get(r,0)-paid.get(r,0);u,v=powers[r]
            lo+=d*(u if d>=0 else v);hi+=d*(v if d>=0 else u)
        bounds=[F(lo,18*denominator),F(hi,18*denominator)]
        cases[label]={'raw_histogram':dict(sorted(replacement.items())),'extra_rank1_moves':extra,
                      'complete_paid_histogram':dict(sorted(paid.items())),
                      'paid_count':sum(paid.values()),'target_count':sum(T.values()),
                      'rank_surplus':sum(r*(T.get(r,0)-paid.get(r,0)) for r in set(T)|set(paid)),
                      'moment_per_native_exact_bounds':[str(x) for x in bounds]}
    bounds=lambda label:[F(x) for x in cases[label]['moment_per_native_exact_bounds']]
    need(F(13981043,10**6)<bounds('all_unit')[0]<bounds('all_unit')[1]<F(13981044,10**6),'unit route floor interval')
    need(bounds('all_unit_plus16')[1]<0 and bounds('24_direct_plus16')[1]<0,'unfunded controls')
    need(F(49711,10**6)<bounds('25_direct_plus16')[0]<bounds('25_direct_plus16')[1]<F(49712,10**6),'positive25-route envelope')
    need(cases['25_direct_plus16']['rank_surplus']==3472,'rank mass includes all16 finishing routes')
    out={'status':'PASS_EXACT_GLOBAL_RAW_REFINEMENT_ENVELOPE','source_sha256':SOURCE,'invoice_sha256':INVOICE,
         'power':'199/200','native_repetitions':18,'raw_public_fields':400,'raw_total_rank_mass':3200,
         'fixed_added_rank9_packets':8,'cases':cases,
         'scope':'Sufficient recursive moment envelope conditional on a correct global word, legal16 rank1 finishing MOVEs and all inherited interface obligations. It constructs no such word and discharges no supplier or foundation. No new kappa.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'all_unit_margin':str(float(bounds('all_unit')[0])),'25_direct_plus16_margin':str(float(bounds('25_direct_plus16')[0]))}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['source','invoice','output']:p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
