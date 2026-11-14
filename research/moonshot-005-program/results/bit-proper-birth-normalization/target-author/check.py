#!/usr/bin/env python3
"""Independent exact target test for all proper-birth rank mixtures."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(b,s):
 if not b:raise ValueError(s)
def main(a):
 raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','paired source pin');z=json.loads(raw)
 N,H,P,T=({int(k):F(v) for k,v in z[s].items()} for s in ['native_paid','helper_target','paired_paid','paired_target'])
 def add(*terms):
  o={}
  for c,p in terms:
   for r,v in p.items():o[r]=o.get(r,0)+c*v
  return {r:v for r,v in o.items() if v}
 S=add((F(1,36),T),(F(-1,36),P));B=add((1,N),(-1,H),(1,S));explicit={127:F(37,6),64:F(37,3),1:F(-37,3)}
 for j in range(1,9):
  for r,c in [(7*j+1,F(37,3)),(7*j,F(-37,3))]:explicit[r]=explicit.get(r,0)+c
 need(B==explicit,'full caller cancellation')
 diff=add((1,H),(-1,N));need(all(v<0 and r<=7 or v>0 and r==8 for r,v in diff.items()),'finite-m normalized derivative signs')
 grid=1<<144;cache={}
 def power(r):
  if r not in cache:
   n=r**199*grid**200;l,h=0,r*grid+1
   while h-l>1:
    m=(l+h)//2
    if m**200<=n:l=m
    else:h=m
   need(l**200<=n<h**200,'outward dyadic root');cache[r]=F(l,grid),F(h,grid)
  return cache[r]
 def mom(p):
  l=h=F(0)
  for r,c in p.items():
   x,y=power(r);l+=c*(x if c>0 else y);h+=c*(y if c>0 else x)
  return l,h
 E=mom(add((1,B),(-222,{7:1})));need(82<E[0]<E[1]<83,'strict82-to83 allowance')
 si=mom(S);need(si[1]<0 and F(37,3)-F(80,49)>0,'all-target monotonicity constants')
 caps=[];margins={}
 for q in range(11):
  pair=mom(add((1,B),(-222,{7:1}),(-q,{8:1})));lo,hi=pair;cap=lo.numerator//lo.denominator
  need(cap==hi.numerator//hi.denominator and F(cap)<lo<hi<F(cap+1),'exact strict integer cap');caps.append(cap);margins[str(q)]=list(map(str,pair))
 need(caps==[82,74,66,59,51,43,35,27,19,11,3],'all explicit caps')
 need(sum(r*c for r,c in add((1,B),(-222,{7:1})).items())==F(629,6),'t1 out-of-target control')
 need(mom(add((1,B),(-222,{7:1}),(-10,{8:1}),(-3,{1:1})))[0]>0,'q10 plus3unit costs not falsely excluded')
 need(111+82==193<=196,'uniform rank-gap hypothesis follows')
 for v in range(1,100):need(9*v+(v+2)//3==(28*v+2)//3,'exact all-width ceiling identity')
 out=dict(status='PASS_TARGET_WIDE_PROPER_BIRTH_RANK_GAP_COMPOSITION',source_sha256=hashlib.sha256(raw).hexdigest(),dyadic_bits=144,E_star=list(map(str,E)),finite_m_S=list(map(str,si)),limiting_room_by_qH=margins,proper_birth_plus_extra_facet_arrival_caps=caps,facet_bound=193,rank_gap_threshold=196,rank_lower_bound='ceil(28V/3)',mode_upper_bound='(8q_H+sum_r r*p_r)V',qHub_lower_bound_assumed=False,controls=['t=1 allowance629/6 exceeds83','q10 plus3rank1 costs have positive limiting room','all-width ceiling checked1..99, algebraic identity in proof'],scope='Necessary retained-caller test on the explicit monotone proper-birth interface; universal argument in PROOF.md, no decoder or new supplier.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'E_star':float(E[0]),'facet_bound':193,'caps':caps}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
