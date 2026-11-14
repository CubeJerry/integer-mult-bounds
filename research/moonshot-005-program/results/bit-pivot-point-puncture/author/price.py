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
 ap=argparse.ArgumentParser();ap.add_argument('--result',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();raw=a.result.read_bytes();x=json.loads(raw);Q={int(k):F(v) for k,v in x['closed_partial']['profile'].items()}
 need(Q=={1:31,2:32,5:32,6:27,7:164},'literal partial source invoice')
 N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
 P2={r:F(36*v) for r,v in N.items()};P2=add(P2,{1:444});P2=add(P2,{7*j:444 for j in range(1,9)})
 T2={r:F(36*v) for r,v in H.items()};T2=add(T2,{127:222});T2=add(T2,{1+7*j:444 for j in range(1,10)})
 signed=add(T2,P2,-1); correction={r:v/36 for r,v in signed.items()};B=add(add(N,H,-1),correction)
 other={127:F(37,6),64:F(37,3),1:-F(37,3)}
 other=add(other,{7*j+1:F(37,3) for j in range(1,9)});other=add(other,{7*j:-F(37,3) for j in range(1,9)})
 need(B==other,'independent caller formula agrees as signed measures')
 cases=[]
 for future in (7,8,9):
  candidate=add(Q,{8:future});margin_measure=add(B,candidate,-1);lim=measure(margin_measure);first=None;finite=[]
  for m in range(2,102,2):
   net=measure(add(margin_measure,correction,F(1,m-1)))
   if m<=10:finite.append({'m':m,'normalized_margin':pack(net)})
   if net[0]>0 and first is None:first=m
  cases.append({'future_bare_rank8_routes':future,'total_marked_Hub_ground_routes':future+1,'hypothetical_movement_profile':{str(k):int(v) for k,v in sorted(candidate.items())},'limiting_remaining_movement_room':pack(lim),'first_positive_even_m_in_tested_range':first,'finite_normalized_margins':finite,'qualification':'Bare future routes only; seven or eight bare future transfers fail the strict-capacity theorem; no complete source, compiler or remaining physical duties supplied.'})
 need(cases[1]['first_positive_even_m_in_tested_range']==4,'eight-future arithmetic firstm4');need(measure(correction)[1]<0,'finite-m correction negative')
 out={'status':'PASS_RIGOROUS_TWO_POINT_PRELOAD_PRICE','result_sha256':hashlib.sha256(raw).hexdigest(),'target':'1/200','moment_power':'199/200','binary_interval_bits':BITS,'actual_closed_partial_moment':pack(measure(Q)),'retained_limiting_allowance':pack(measure(B)),'finite_m_correction':pack(measure(correction)),'cases':cases,'new_kappa':None,'scope':'Optimistic complete-caller movement screen of a known partial source; no complete source or supplier.'}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'partial':out['actual_closed_partial_moment']['lower'],'limiting_allowance':out['retained_limiting_allowance']['lower'],'eight_future_room':cases[1]['limiting_remaining_movement_room']['lower'],'eight_future_first_even_m':4}))
if __name__=='__main__':main()
