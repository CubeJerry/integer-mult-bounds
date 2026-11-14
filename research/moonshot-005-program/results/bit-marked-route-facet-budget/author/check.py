#!/usr/bin/env python3
"""Exact rational endpoint and finite rank-tariff controls."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)

def add(*terms):
 out={}
 for factor,measure in terms:
  for rank,count in measure.items():out[rank]=out.get(rank,F(0))+factor*count
 return {r:c for r,c in out.items() if c}

POWER={}
def power(rank,t,bits=184):
 key=(rank,t,bits)
 if key not in POWER:
  scale=1<<bits;target=(rank**t.numerator)*scale**t.denominator
  lo=0;hi=max(1,rank)*scale+1
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**t.denominator<=target:lo=mid
   else:hi=mid
  POWER[key]=(F(lo,scale),F(lo if lo**t.denominator==target else hi,scale))
 return POWER[key]

def interval(measure,t):
 lo=hi=F(0)
 for rank,count in measure.items():
  a,b=power(rank,t)
  lo+=count*(a if count>=0 else b);hi+=count*(b if count>=0 else a)
 return lo,hi

def encode(bounds):
 lo,hi=bounds
 return {'lower_rational':str(lo),'upper_rational':str(hi),'display':[float(lo),float(hi)]}

def incidence(u,v):
 return int(v==7 and u<7 or u==7 and v<7)

def tariff_controls():
 checked=sharp=0
 for t in map(F,('0','1/4','1/2','3/4','199/200','1')):
  potential={0:{},7:{7:1,1:-1},8:{7:1}}
  for r in range(1,7):
   direct={r:1};via=add((1,{7:1}),(1,{7-r:1}),(-2,{1:1}))
   dlo,dhi=interval(direct,t);vlo,vhi=interval(via,t)
   if dhi<=vlo:potential[r]=direct
   elif vhi<=dlo:potential[r]=via
   else:raise ValueError('ambiguous exact potential choice')
  for u in range(9):
   for v in range(9):
    if u==v:continue
    residual=add((1,{abs(u-v):1}),(-incidence(u,v),{1:1}),
                 (1,potential[v]),(-1,potential[u]))
    lo,hi=interval(residual,t)
    need(lo>=0,'exact adjusted rank-edge potential')
    checked+=1
  for repetitions in range(7):
   path=[8,7]+[r for unused in range(repetitions) for r in (6,7)]+[0]
   price={};I=0
   for u,v in zip(path,path[1:]):
    price[abs(u-v)]=price.get(abs(u-v),0)+1;I+=incidence(u,v)
   residual=add((1,price),(-I,{1:1}),(-1,{7:1}))
   need(interval(residual,t)==(0,0),'sharp arbitrary-turn tariff route')
   sharp+=1
 return {'exact_rank_edge_checks':checked,'sharp_route_checks':sharp}

def main():
 p=argparse.ArgumentParser();p.add_argument('--caller',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.caller.read_bytes();pin=hashlib.sha256(raw).hexdigest()
 need(pin=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','retained caller pin')
 receipt=json.loads(raw)
 measure=lambda name:{int(r):F(c) for r,c in receipt[name].items()}
 N=measure('native_paid');H=measure('helper_target')
 S=add((F(1,36),measure('paired_target')),(-F(1,36),measure('paired_paid')))
 B=add((1,N),(-1,H),(1,S));c={1:1,8:1,7:-1}
 delta={1:56,6:56,7:-56};t=F(199,200)
 cases=[('eight_Hub',8,0,28,0,138),('nine_Hub',9,0,21,0,131),
        ('ten_Hub',10,0,14,0,124),('nine_Hub_two_rank3',9,2,15,0,125),
        ('fixed_pivot_nine_Hub_two_rank3',9,2,14,1,124)]
 certificates={}
 for name,q,b,z,use_delta,ell in cases:
  gap=add((1,B),(-(222+q),{7:1}),(-b,{3:1}),(-F(z,2),c),(-use_delta,delta))
  bounds=interval(gap,t);need(bounds[1]<0,'strict target exclusion '+name)
  certificates[name]={'forbidden_Z_at_least':z,'maximum_ell':ell,'gap':encode(bounds),
                      'signed_measure':{str(r):str(v) for r,v in sorted(gap.items())}}
 need(interval(S,t)[1]<0,'negative finite-m endpoint correction')
 controls=tariff_controls()
 # The sharper124 cap needs the actual capture stops, not just the generic tariff.
 generic_remaining=add((1,B),(-231,{7:1}),(-2,{3:1}))
 need(interval(generic_remaining,t)[0]>14,'generic relaxed count Z14 remains affordable')
 # A proper-born turning record cannot be treated as a monotone bank for free.
 false_bank_claim=add((1,{7:1}),(-1,{6:1}),(-1,{1:1}))
 need(interval(false_bank_claim,t)[1]<0,'proper6-to7-to0 scope counterexample')
 false_hub_credit=add((1,{7:1}),(-1,{8:1}))
 need(interval(false_hub_credit,t)[1]<0,'8^t-plus-I tariff overclaim counterexample')
 out={'status':'PASS_EXACT_FULL_ROUTE_FACET_TARIFF_AND_TARGET_CAPS','caller_sha256':pin,
      'endpoint_t':str(t),'endpoint_c':encode(interval(c,t)),
      'endpoint_capture_premium':encode(interval(delta,t)),
      'target_certificates':certificates,'finite_tariff_controls':controls,
      'negative_controls':['generic125_not124_without_capture_premium',
                           'proper_born_turn_not_a_free_monotone_bank',
                           'Hub_baseline8_to_power_t_cannot_be_added_to_every_incidence'],
      'proof_scope':'Universal rank-walk proof and inherited all-route model; finite endpoints use exact rational bounds. No source construction or kappa.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'caps':{k:v['maximum_ell'] for k,v in certificates.items()},**controls}))

if __name__=='__main__':main()
