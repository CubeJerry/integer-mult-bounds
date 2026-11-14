#!/usr/bin/env python3
"""Exact interval arithmetic for the helper-aware cut and short-caller allowance."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,argparse
HERE=Path(__file__).resolve().parent;DEN=10**45
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
 need(x**200<=z<(x+1)**200,'exact root enclosure');return F(x,DEN),F(x+1,DEN)
def plus(*xs):return sum(x[0]for x in xs),sum(x[1]for x in xs)
def mul(c,x):
 c=F(c);return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def sub(x,y):return plus(x,mul(-1,y))
def show(x):return dict(exact=list(map(str,x)),approximate=[float(z)for z in x])
def moment(H):return plus(*(mul(c,p(int(r)))for r,c in H.items()))
def W(a):return plus(mul(2,p(1+16*a)),*(mul(4,p(1+8*j))for j in range(1,a+1)),mul(-4,p(1)),*(mul(-4,p(8*j))for j in range(1,a)))
def L(a):return mul(F(104,2*a),W(a))
def main(out):
 R=json.loads((HERE/'REPLAY.json').read_text());N=json.loads((HERE/'source/complete-receipt.json').read_text())['new_native']
 h5=sub(mul(5,W(6)),mul(6,W(5)));h6=sub(mul(6,W(7)),mul(7,W(6)))
 need(h5[0]>0 and h6[1]<0,'proved all-arm allowance maximum at a6')
 c=plus(p(1),p(9),mul(-1,p(8)));eta=mul(F(1,2),c)
 native=sub(moment(N['paid']),moment(N['helpers']));penalty=sub(native,L(6));need(penalty[0]>0,'positive finite-bridge penalty')
 sources={}
 for name in ['gram','parity']:
  rr=R['sources'][name];r=rr['residual_rank_forward'];Q=moment(rr['moves']);allow=sub(L(6),Q);cut=mul(r,c)
  need(sub(cut,allow)[0]>0,'closed handoff cannot complete after helpers')
  finite={str(m):show(sub(allow,mul(F(1,m-1),penalty)))for m in [2,4,6,8,16,64]}
  table={str(2*a):show(sub(L(a),Q))for a in [1,2,3,4,5,6,7,9]}
  sources[name]=dict(source_cost=show(Q),residual_rank_each_direction=r,limiting_allowance=show(allow),
   helper_aware_completion_lower_bound=show(cut),deficit_even_at_best_limiting_caller=show(sub(cut,allow)),
   limiting_allowance_by_stages=table,finite_even_bridge_allowance_at_twelve_stages=finite)
 # Distinct facet endpoints: a genuine nested two-MOVE route, but no granted nonnested productive job.
 hypothetical=sub(mul(2,p(1)),p(2));need(hypothetical[1]<c[0],'nonnested credit would invalidate nested tariff')
 scalar_controls=[]
 for a in range(9):
  for b in range(9):
   r=abs(a-b);route=sub(plus(p(9-a),p(9-b)),p(r));need(route[0]>=c[1]or (min(a,b)==0 and max(a,b)==8),'proper nested through-Hub endpoint tariff')
   scalar_controls.append((a,b))
 result=dict(status='PASS_HELPER_AWARE_CLOSED_HANDOFF_BUDGET',t='199/200',hub_rank=9,
  c_h=show(c),eta_h=show(eta),maximum_caller_stages=12,maximum_per_native_allowance=show(L(6)),
  complete_allhosted_native_net=show(native),finite_bridge_penalty_at_twelve_stages=show(penalty),
  optimizer_signs={'H5':show(h5),'H6':show(h6)},sources=sources,
  nested_endpoint_pairs_checked=len(scalar_controls),nonnested_two_facet_hypothetical_net=show(hypothetical),
  scope='Nested-endpoint independent clean helper jobs and whole-chart rank quantum only. Nonnested rank2 credit is a counterexample to extending the tariff, not an admitted productive job. No new kappa.')
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({n:{k:float(F(v[k]['exact'][0]))for k in ['limiting_allowance','helper_aware_completion_lower_bound']}for n,v in sources.items()}))
if __name__=='__main__':
 q=argparse.ArgumentParser();q.add_argument('--out',type=Path,default=HERE/'BUDGET.json');main(q.parse_args().out)
