"""Exact consequence of the reviewed S8 price and static 46-mode cut."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PRICE='b5c4a118bb7e72a31d7ba90a8cd4b72884f9fa6470710850119d709ad3f21f40'
def need(x,label):
 if not x:raise ValueError(label)
def run(root):
 p=root/'research/moonshot-005-program/results/relay-acquisition-budget/RESULT.json'
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==PRICE,'reviewed price pin');d=json.loads(b)
 n=d['native_repetitions'];need(n==18,'complete repetition count')
 lo,hi=[F(x)/n for x in d['S8_raw_margin_interval']]
 need(20<lo<=hi<21,'S8 unacquired ceiling20')
 cases={'none':{'supplied_scalar_rank':0,'remaining_interval':[str(lo),str(hi)],'new_call_ceiling':20,'further_original_crossings_necessary':26}}
 for name,key in [('facet','eight_facet_copies'),('direct','four_aggregates')]:
  v=d['variants'][key];c0,c1=map(F,v['per_native_added_paid_moment_interval']);r0,r1=map(F,v['remaining_paid_moment_per_native_interval'])
  cap=r1.numerator//r1.denominator
  need(r0>=lo-c1 and r1<=hi-c0,'compatible signed intervals')
  need(2<=c0 and cap==(8 if name=='facet' else 2),'paid-only acquisition information and call ceiling')
  cases[name]={'supplied_scalar_rank':2,'acquisition_moment_interval':[str(c0),str(c1)],'remaining_interval':[str(r0),str(r1)],'new_call_ceiling':cap,'further_original_crossings_necessary':46-2-cap}
 need(F(21)>hi,'twenty-first new call excluded')
 need(F(60)>F(cases['facet']['acquisition_moment_interval'][1]),'support60 is not supplied rank')
 return {'status':'PASS_PREACQUISITION_S8_26_CROSSING_COROLLARY','price_sha256':PRICE,'native_repetitions':n,'required_static_cut_rank':46,'S8_headroom_interval':[str(lo),str(hi)],'cases':cases,'negative_controls':['21 new complete calls exceed S8 headroom','60 support coordinates are not 60 paid-acquired independent forms'],'scope':'Fixed S8 complete-field price and static cut. At least26 informative original crossing occurrences are necessary; no native, cost admission or new kappa.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repository',type=Path,required=True);a.add_argument('--output',type=Path,required=True);x=a.parse_args();r=run(x.repository);x.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
