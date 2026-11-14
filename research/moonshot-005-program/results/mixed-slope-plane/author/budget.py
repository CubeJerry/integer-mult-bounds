#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,argparse
HERE=Path(__file__).resolve().parent;DEN=10**45
@lru_cache(None)
def power(r):
 z=r**199*DEN**200;x=1<<((z.bit_length()+199)//200)
 while True:
  y=(199*x+z//x**199)//200
  if y>=x:break
  x=y
 while x**200>z:x-=1
 while(x+1)**200<=z:x+=1
 if not x**200<=z<(x+1)**200:raise ValueError('root bracket')
 return F(x,DEN),F(x if x**200==z else x+1,DEN)
def moment(p):
 lo=hi=F(0)
 for r,c in p.items():
  a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
def main(out):
 native={2:112,3:112,5:112,6:112};T={17:224};P={1:112,2:224,3:224,5:224,6:224};delta={r:T.get(r,0)-P.get(r,0)for r in set(T)|set(P)};M=moment(delta)
 if M[0]<=0:raise ValueError('positive stipulated room')
 result={'status':'PASS_OPTIMISTIC_MIXED_SLOPE_TWO_HALF_BUDGET','t':'199/200','actual_half_source_profile':native,'stipulated_target':T,'complete_stipulated_paid':P,
 'strict_remaining_moment_interval':list(map(str,M)),'approximate_room':[float(x)for x in M],
 'scope':'Only source half invoices are established. Two rank17 whole targets from two mixed-slope calls plus one rank1 query are an unproved design premise, not a caller identity. All additional paid/ordinary/precision/compiler costs remain.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],float(M[0]))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'BUDGET.json');main(a.parse_args().out)
