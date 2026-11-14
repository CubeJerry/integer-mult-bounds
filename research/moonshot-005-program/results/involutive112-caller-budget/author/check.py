#!/usr/bin/env python3
"""Conditional full112 involutive-source invoice. No physical admission implied."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json,argparse,hashlib
HERE=Path(__file__).resolve().parent;DEN=10**45;t=F(199,200)
def need(ok,msg):
 if not ok:raise ValueError(msg)
@lru_cache(None)
def p(r):
 if r in(0,1):return F(r),F(r)
 z=r**199*DEN**200;x=1<<((z.bit_length()+199)//200)
 while True:
  y=(199*x+z//x**199)//200
  if y>=x:break
  x=y
 while x**200>z:x-=1
 while (x+1)**200<=z:x+=1
 need(x**200<=z<(x+1)**200,'integer root enclosure');return F(x,DEN),F(x+1,DEN)
def add(*xs):return sum(x[0]for x in xs),sum(x[1]for x in xs)
def mul(c,x):
 c=F(c);return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def sub(x,y):return add(x,mul(-1,y))
def show(x):return dict(exact=list(map(str,x)),approximate=[float(z)for z in x])
def moment(H):return add(*(mul(c,p(r))for r,c in H.items()))
def W(a):return add(mul(2,p(1+16*a)),*(mul(4,p(1+8*j))for j in range(1,a+1)),mul(-4,p(1)),*(mul(-4,p(8*j))for j in range(1,a)))
def dW(a):return add(mul(2,sub(p(1+16*(a+1)),p(1+16*a))),mul(4,sub(p(9+8*a),p(8*a))))
def gain(a,Q):return sub(mul(112,W(a)),mul(2*a,Q))
def dgain(a,Q):return sub(mul(112,dW(a)),mul(2,Q))
def sum_increment_enclosure(M):
 # Convex g(x)=(8x+1)^t−(8x)^t. Composite trapezoid error is between0
 # and(1/8) integral(g''), since each unit-interval Green kernel<=1/8.
 def g(x):return sub(p(8*x+1),p(8*x))
 def gp(x):return mul(8*t,sub(mul(F(1,8*x+1),p(8*x+1)),mul(F(1,8*x),p(8*x))))
 def J(x):return mul(F(1,8*(t+1)),sub(mul(8*x+1,p(8*x+1)),mul(8*x,p(8*x))))
 base=add(sub(J(M),J(1)),mul(F(1,2),add(g(1),g(M))))
 err=mul(F(1,8),sub(gp(M),gp(1)));need(err[0]>=0,'convex trapezoid error')
 return base[0],base[1]+err[1]
def large_gain(a,Q):
 w=add(mul(2,p(1+16*a)),mul(4,p(1+8*a)),mul(-4,p(1)),mul(4,sum_increment_enclosure(a-1)))
 return sub(mul(112,w),mul(2*a,Q))
def main(out):
 raw=(HERE/'source/GEOMETRY.json').read_bytes();need(hashlib.sha256(raw).hexdigest()=='e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6','full112 geometry pin')
 profiles={'R':{1:336,2:112,3:336,4:224,5:224,8:16},'R0':{3:224,4:448,5:224}}
 result={}
 # All-arm maximum of W_a/a is source-independent.
 need(sub(mul(5,W(6)),mul(6,W(5)))[0]>0 and sub(mul(6,W(7)),mul(7,W(6)))[1]<0,'all-arm source allowance maximum at a6')
 for name,H in profiles.items():
  Q=moment(H);targetopt=7 if name=='R'else 10;queryopt=19 if name=='R'else 24812
  def Tsign(a):return sub(mul(4*a+2,gain(a+1,Q)),mul(4*a+6,gain(a,Q)))
  need(Tsign(targetopt-1)[0]>0 and Tsign(targetopt)[1]<0,'all-arm uniform target-debit optimizer')
  need(dgain(queryopt-1,Q)[0]>0 and dgain(queryopt,Q)[1]<0,'all-arm query-debit optimizer')
  maxquery=mul(F(1,4),gain(queryopt,Q)if queryopt<100 else large_gain(queryopt,Q))
  table={str(2*a):{'total_margin':show(gain(a,Q)),'per_native_margin':show(mul(F(1,2*a),gain(a,Q))),
   'query_only_debit_ceiling':show(mul(F(1,4),gain(a,Q))),
   'uniform_target_only_debit_ceiling':show(mul(F(1,4*a+2),gain(a,Q)))}for a in [1,2,3,4,5,6,7,9,10,19]}
  result[name]=dict(stipulated_profile=H,profile_moment=show(Q),per_native_optimum_stages=12,
   largest_per_native_margin=show(mul(F(1,12),gain(6,Q))),
   uniform_target_debit_optimum_stages=2*targetopt,largest_uniform_target_debit=show(mul(F(1,4*targetopt+2),gain(targetopt,Q))),
   query_debit_optimum_stages=2*queryopt,largest_query_only_debit=maxquery and show(maxquery),
   query_optimizer_signs=[show(dgain(queryopt-1,Q)),show(dgain(queryopt,Q))],
   target_optimizer_signs=[show(Tsign(targetopt-1)),show(Tsign(targetopt))],stages=table)
  need(sub(Q,mul(448,p(8)))[0]>0,'source costs exceed four direct raw routes')
 q0=moment(profiles['R0']);both56=sub(gain(6,q0),mul(30*56,p(1)));need(both56[0]>0,'conditional56-unit query and target scenario')
 need(sub(p(2),mul(2,p(1)))[1]<0 and sub(add(mul(2,p(4)),mul(4,p(2))),mul(16,p(1)))[1]<0,'strict all-arm doublecaller constants')
 R=dict(status='PASS_CONDITIONAL_112_INVOLUTIVE_CALLER_INVOICE',t='199/200',sources=result,
  R0_twelve_stage_both_debits56_margin=show(both56),
  general_extra_invoice='4 delta_query + (4a+2) delta_target + other_net_expenses',
  doublecaller_status='Excluded for every positive a even with free queries and only four raw rises per native; see proof.',
  scope='Profiles and a hypothetical physically compatible involutive caller are stipulated. Actual operator centrality, coefficient service, query/target normalizers, whole source and compiler admission remain open. No new kappa.')
 out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(R['status'])
if __name__=='__main__':
 q=argparse.ArgumentParser();q.add_argument('--out',type=Path,default=HERE/'RESULT.json');main(q.parse_args().out)
