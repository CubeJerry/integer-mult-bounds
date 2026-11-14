#!/usr/bin/env python3
"""Independent signed moments from the actual reviewed complex words."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
def need(b,s):
 if not b:raise ValueError(s)
def main(a):
 raw=a.full.read_bytes();need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','retained complete caller pin');f=json.loads(raw)
 r=json.loads(a.source_review.read_text());need(r['status']=='PASS_INDEPENDENT_RESTORED_TRANSIENT_RECIPROCAL_CODEC','independent source result')
 ps={k:{int(j):F(v) for j,v in f[g][h].items()} for k,g,h in [('T','invoice','T'),('P','invoice','P'),('N','native','paid'),('H','native','helpers')]}
 rs=sorted(set().union(*(p.keys() for p in ps.values()),*(set(map(int,v['bill']['moves'])) for v in r['results'].values()),{1,2,6,8,9}));grid=1<<140;pw={}
 for j in rs:
  v=j**199*grid**200;lo=0;hi=j*grid+1
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**200<=v:lo=mid
   else:hi=mid
  need(lo**200<=v<hi**200,'outward rational root');pw[j]=(F(lo,grid),F(lo if lo**200==v else hi,grid))
 def mom(p):
  lo=hi=F(0)
  for j,c in p.items():
   x,y=pw[j];lo+=c*(x if c>=0 else y);hi+=c*(y if c>=0 else x)
  return lo,hi
 T,P,N,H=(ps[k] for k in ['T','P','N','H']);sl={j:(T.get(j,0)-P.get(j,0))/18 for j in rs}
 pen=mom({j:-c for j,c in sl.items()});need(pen[0]>0,'positive finite-m penalty')
 def room(Q):return mom({j:sl[j]+N.get(j,0)-H.get(j,0)-Q.get(j,0) for j in rs})
 out={}
 for name,z in r['results'].items():
  Q={int(j):F(v) for j,v in z['bill']['moves'].items()};delta={int(j):F(v) for j,v in z.get('move_delta',{}).items()};iv=room(Q)
  out[name]=dict(actual_source_profile={str(j):str(c) for j,c in Q.items()},limiting_remaining_moment=list(map(str,iv)),movement_change_against_actual_baseline=list(map(str,mom(delta))) if delta else None)
 delta=mom({1:F(8),2:F(36),6:F(40),8:F(-40)});need(F(92026,100000)<delta[0]<delta[1]<F(92027,100000),'actual small positive source refinement price')
 blank=room({8:400});forward=room({8:400,9:8,1:8});global8=room({8:400,9:16,1:8});need(global8[1]<0,'even optimistic global8 return envelope negative')
 result=dict(status='PASS_INDEPENDENT_TRANSIENT_COMPLETE_CALLER_TARIFF',source_review_sha256=hashlib.sha256(a.source_review.read_bytes()).hexdigest(),integer_root_grid='2^-140',target='1/200',positive_finite_m_penalty=list(map(str,pen)),finite_m_formula='room(m)=room(infinity)-penalty/(m-1), fixed integer m>=2',sources=out,codec_movement_delta_interval=list(map(str,delta)),optimistic_400_direct_raw=list(map(str,blank)),after_eight_forward_packets_and_eight_coupled_entries=list(map(str,forward)),after_eight_further_global_returns=list(map(str,global8)),scope='Movement-only actual partial-source prices and scoped optimistic completion exclusion; ordinary/ownership/compiler/precision and actual reverse acquisition remain owed.',new_kappa=None)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'codec_delta':float(delta[0]),'optimistic_global8_margin':float(global8[1])}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['full','source-review','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
