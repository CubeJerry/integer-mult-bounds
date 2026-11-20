#!/usr/bin/env python3
"""Target-price and repair-weight comparison from the captured input geometry."""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--repo',required=True,type=Path)
p.add_argument('--cut',required=True,type=Path)
p.add_argument('--out',required=True,type=Path)
a=p.parse_args()
sm=json.loads((a.cut/'SMALL.json').read_text())
lg=json.loads((a.cut/'LARGE.json').read_text())
assert sm['rows']==lg['rows'] and sm['donors']==lg['donors']
assert sm['rank']+lg['rank']==sm['all_K_inputs']==36090 and len(sm['rows'])==19
base=a.repo/'research/moonshot-005-program/results'
geo=gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
rr=gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
assert hashlib.sha256(geo).hexdigest()==sm['pins']['source_geometry']
assert hashlib.sha256(rr).hexdigest()==sm['pins']['native_routes']
routes=[json.loads(line) for line in rr.splitlines()]
region=set(sm['rows'])
ks={k for k,plane in enumerate(json.loads(geo)['A2']) if region & set(plane)}
ds=Counter(r[4] for r in routes if r[5] in ks)
hs=Counter(r[3] for r in routes if r[3] is not None and r[4] in ds)
def cutsize(hist,number):
    v=sorted(hist.values(),reverse=True)
    return next(t for t in range(1,len(v)+1) if sum(v[:t])>=number)
def linear_gap(m,ret):
    paid=18*sum(r*c for r,c in {1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}.items())
    productive=18*sum(r*c for r,c in {2:1,4:25,6:1,8:410}.items())
    paid+=222*m*(1+sum(7*j for j in range(1,9)))
    productive+=111*m*127+222*m*sum(1+7*j for j in range(1,10))
    paid+=18*(m-1)*(Fraction(4451,8)+2*Fraction(7213,16)+4*24+8*ret)
    return productive-paid
for m in (2,4,870):
    assert linear_gap(m,19)==1602-849*m
    assert linear_gap(m,9+Fraction(197,48)+Fraction(251,48*(m-1)))==0
b=3840
records={"status":"PASS_ALL_K_AND_F_CUT_FIXED_S_H_D","q_lower_GF64":19*b,"excess_lower_GF64":10*b,
         "binary_return_lower":19*b*6,"restriction_rank_change_needed_m870":10*b-128,
         "restriction_rank_change_needed_limit":10*b-134,"cardinality_K":len(ks),
         "paid_gap_at_zero_saving":"T-P=1602-849m at q=19b",
         "H_region_holder_histogram":dict(sorted(Counter(hs.values()).items())),
         "D_region_holder_histogram":dict(sorted(Counter(ds.values()).items())),
         "minimum_only_D_changed":cutsize(ds,(10*b-128)//8),
         "minimum_only_H_changed":cutsize(hs,(10*b-128)//8),"minimum_only_donors_changed":10}
assert (records["minimum_only_D_changed"],records["minimum_only_H_changed"])==(200,59)
a.out.mkdir(parents=True,exist_ok=True)
(a.out/'GATE.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
