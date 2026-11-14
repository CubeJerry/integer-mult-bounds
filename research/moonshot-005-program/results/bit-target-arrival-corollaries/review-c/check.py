#!/usr/bin/env python3
"""Exact arithmetic only; universal arguments are in REVIEW.md."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)

def eighth():
 scale=1<<128;goal=8**199*scale**200;lo=0;hi=8*scale+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=goal:lo=mid
  else:hi=mid
 need(lo**200<=goal<hi**200,'outward eighth bracket')
 return F(lo,scale),F(hi,scale)

def main():
 p=argparse.ArgumentParser();p.add_argument('--packet-review',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.packet_review.read_bytes();z=json.loads(raw)
 need(z['status']=='PASS_INDEPENDENT_MONOTONE_PACKET_CAP','review premise')
 m10=list(map(F,z['q10_margin_interval']));lo8,hi8=eighth();out={}
 for q,cap in [(8,19),(9,11),(10,3)]:
  lo=m10[0]+(10-q)*lo8;hi=m10[1]+(10-q)*hi8
  need(cap<lo<hi<cap+1,'strict integer arrival cap')
  ell=111+q+cap;need(ell<=138<197,'uniform rank gap applies')
  out[q]={'margin_interval':[str(lo),str(hi)],'maximum_additional_facet_arrivals':cap,
          'maximum_ell_sum':ell}
 deletion={d:str(F(9)-F(d,10)) for d in range(10)}
 need(all(F(x)>8 for x in deletion.values()),'strict deletion separation')
 need(F(9)-F(10,10)==8,'d10 is not strictly excluded by this bound')
 result={'status':'PASS_INDEPENDENT_TARGET_COROLLARY_ARITHMETIC',
         'packet_review_sha256':hashlib.sha256(raw).hexdigest(),'arrival_cases':out,
         'deletion_rank_factors':deletion,'negative_control_d10_factor':'8',
         'new_kappa':None}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'arrival_caps':[19,11,3],'maximum_ell':138}))

if __name__=='__main__':main()
