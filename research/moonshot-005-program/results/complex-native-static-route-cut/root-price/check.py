#!/usr/bin/env python3
"""Separate directed-price review of the exact static complex route cut."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import gzip,importlib.util,json
from pathlib import Path

def need(x,s):
 if not x:raise ValueError(s)
def decimal(z,p=20):
 grid=10**p;out=[]
 for v in (z[0].numerator*grid//z[0].denominator,-((-z[1].numerator*grid)//z[1].denominator)):
  a,b=divmod(abs(v),grid);out.append(('-'if v<0 else'')+str(a)+'.'+str(b).zfill(p))
 return out

def main():
 cli=ArgumentParser();cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True);a=cli.parse_args()
 base=a.repo/'research/moonshot-005-program/results';here=base/'complex-native-static-route-cut';source=base/'complex-native-contested-restoration/rail/sources'
 pricefile=base/'kappa-significant-gain-screen/root-review/check.py';spec=importlib.util.spec_from_file_location('episode_independent_price',pricefile);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
 pins=json.loads((here/'SOURCE-PINS.json').read_text())['files']
 for name,digest in pins.items():need(sha256((a.repo/name).read_bytes()).hexdigest()==digest,'source pin '+name)
 read=lambda name:json.loads(gzip.decompress((source/name).read_bytes()))
 w,app=read('rail-base.json.gz'),read('DOUBLE-APPLICATION.json.gz')
 inside=set(json.loads((here/'CUT.json').read_text())['inside_canonical_chart_ids'])
 spanids={};canonical=[]
 for i,frame in enumerate(w['frames']):
  s={0}
  for v in frame:s|={x^v for x in s}
  key=tuple(sorted(s));spanids.setdefault(key,i);canonical.append(spanids[key])
 need(all(canonical[i]==i for i in inside),'cut uses canonical binary spaces')
 paid=Counter();crossings=Counter();grade_nine=0
 for op in w['program']:
  if op[0]!='MOVE':continue
  r=abs(len(w['frames'][op[2]])-len(w['frames'][op[3]]));cross=(canonical[op[2]]in inside)!=(canonical[op[3]]in inside);paid[r]+=1
  if cross:crossings[r]+=1
  if r==9:need(cross,'every grade-nine movement loses one crossing unit');grade_nine+=1
 need(sum(paid.values())==803 and sum(crossings.values())==72 and grade_nine==8 and max(paid)==9,'original movement and crossing census')
 c=app['caller_census'];need(c['calls']==48,'complete complex caller')
 cap=p.hist((F(1,48),c['fixed_root_targets']),(-F(1,48),c['fixed_caller_paid']))
 native=app['native'];d=p.hist((1,native['paid_native_ranks']),(-1,native['positive_helper_ranks']),(-1,cap))
 gap=p.hist((1,paid),(164,{1:1}),(-1,cap))
 results={}
 for sk,expected in [('.004',12),('.0043',12),('.005',13)]:
  k=F(sk);delta=p.moment(gap,k);penalty=p.moment(d,k);unit=p.power(8,k)
  need(delta[0]>0 and penalty[0]>0,'strict deficit for every finite multiplicity')
  need((expected-1)*unit[1]<delta[0] and expected*unit[0]>delta[1],'strict minimum number of changed old occurrences')
  results[sk]={'old_private_moment':decimal(p.moment(paid,k)),'limiting_private_allowance':decimal(p.moment(cap,k)),'minimum_fixed_route_shortfall':decimal(delta),'finite_m_native_penalty':decimal(penalty),'maximum_discount_per_changed_old_occurrence':decimal(unit),'minimum_changed_old_occurrences':expected}
 need(p.moment(gap,F(0))==(F(49),F(49)),'limiting zero-saving shortfall')
 result={'status':'PASS_INDEPENDENT_STATIC_CUT_PRICE_REVIEW','power_method':'Rational logarithm and outward-rounded alternating exponential, separate from author integer-root prices.','source_pins':pins,'price_engine_sha256':sha256(pricefile.read_bytes()).hexdigest(),'paid_profile':dict(paid),'crossing_profile':dict(crossings),'new_movement_lower_bound_dependency':'Independently reviewed 82+82 static cut in review-b.','targets':results,'limiting_zero_saving_shortfall':49,'finite_zero_saving_penalty':decimal(p.moment(d,F(0))),'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status']);print(json.dumps(results,sort_keys=True))
if __name__=='__main__':main()
