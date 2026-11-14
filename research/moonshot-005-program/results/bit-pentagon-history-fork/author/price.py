#!/usr/bin/env python3
"""Rigorous 199/200 movement intervals for one actual partial word only."""
import argparse,json,hashlib
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
BITS=176;SCALE=1<<BITS

def need(b,m):
 if not b:raise ValueError(m)
def iroot(n,k):
 x=1<<((n.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+n//pow(x,k-1))//k
  if y>=x:break
  x=y
 while pow(x,k)>n:x-=1
 while pow(x+1,k)<=n:x+=1
 return x
_cache={}
def pow_interval(r):
 if r not in _cache:
  n=pow(r,199)*pow(SCALE,200);x=iroot(n,200)
  need(pow(x,200)<=n<pow(x+1,200),'exact integer-root enclosure')
  _cache[r]=(F(x,SCALE),F(x+1,SCALE))
 return _cache[r]
def measure(H):
 lo=F(0);hi=F(0)
 for r,c in H.items():
  a,b=pow_interval(r)
  if c>=0:lo+=c*a;hi+=c*b
  else:lo+=c*b;hi+=c*a
 return lo,hi

def add(A,B,weight=F(1)):
 C=dict(A)
 for r,v in B.items():C[r]=C.get(r,F(0))+weight*v
 return {r:v for r,v in C.items() if v}
def show(x):
 with localcontext() as c:
  c.prec=64;return str(Decimal(x.numerator)/Decimal(x.denominator))
def pack(I):return {'lower':show(I[0]),'upper':show(I[1]),'lower_rational':[str(I[0].numerator),str(I[0].denominator)],'upper_rational':[str(I[1].numerator),str(I[1].denominator)]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--result',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();raw=a.result.read_bytes();x=json.loads(raw);Q={int(k):F(v) for k,v in x['closed_partial']['movement_profile'].items()};need(Q=={1:9,2:2,5:2,6:7,7:215},'literal fork invoice')
 B={127:F(37,6),64:F(37,3),1:-F(37,3)};B=add(B,{7*j+1:F(37,3) for j in range(1,9)});B=add(B,{7*j:-F(37,3) for j in range(1,9)})
 isolated={7:222,8:3};gain=measure(add(isolated,Q,-1));need(gain[0]>0,'strict movement saving against optimistic three-isolated-route lower bound')
 cases=[]
 for future in[6,7,8]:
  candidate=add(Q,{8:future});cases.append({'future_bare_full_routes':future,'total_full_routes':future+2,'limiting_remaining_movement_room':pack(measure(add(B,candidate,-1))),'qualification':'Arithmetic only for CONTINUABLE-PREFIX, whose106unserved original source lines stay live. Future acquisition, restoration, history, endpoints and ownership costs remain. Not applicable to the all-Hub control prefix.'})
 out={'status':'PASS_RIGOROUS_TWO_PACKET_FORK_MOVEMENT','result_sha256':hashlib.sha256(raw).hexdigest(),'target':'1/200','moment_power':'199/200','binary_interval_bits':BITS,'actual_closed_partial_moment':pack(measure(Q)),'isolated_three_route_optimistic_movement_lower_bound':pack(measure(isolated)),'strict_movement_saving_over_that_lower_bound':pack(gain),'retained_limiting_allowance':pack(measure(B)),'cases':cases,'new_kappa':None,'scope':'Exact partial movement and conditional lower-bound comparison only. Seven actual owned lifetimes still paid; no complete source or supplier.'}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'moment':out['actual_closed_partial_moment']['lower'],'isolated_lower_gap':out['strict_movement_saving_over_that_lower_bound']['lower'],'eight_future_room':cases[2]['limiting_remaining_movement_room']['lower']}))
if __name__=='__main__':main()
