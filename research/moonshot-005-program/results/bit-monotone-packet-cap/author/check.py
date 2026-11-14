#!/usr/bin/env python3
"""Exact paired-caller identities and outward interval endpoint signs."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
PIN='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2'
def need(x,s):
 if not x:raise ValueError(s)
def main(a):
 raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'paired source pin');z=json.loads(raw)
 def profile(k):return {int(r):F(c) for r,c in z[k].items()}
 N,H,P,T=map(profile,['native_paid','helper_target','paired_paid','paired_target'])
 def linear(*terms):
  d=Counter()
  for c,x in terms:
   for r,v in x.items():d[r]+=c*v
  return {r:v for r,v in sorted(d.items()) if v}
 pe=linear((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
 te=linear((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
 need(pe==P and te==T,'exact paired profiles')
 S=linear((F(1,36),T),(F(-1,36),P));B=linear((1,S),(1,N),(-1,H))
 simple=linear((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}),(F(37,3),{7*j+1:1 for j in range(1,9)}),(F(-37,3),{7*j:1 for j in range(1,9)}))
 need(B==simple,'native-cancellation formula')
 D=linear((1,H),(-1,N));need(D=={1:F(-1386),2:F(-1252),3:F(-62),4:F(-22),5:F(-9),6:F(-103),7:F(-10),8:F(410)},'monotonicity coefficient signs')
 ranks=set(B)|set(S)|{7,8};powers={};den=10**30
 for r in ranks:
  u=r**199*den**200;lo,hi=0,r*den+1
  while hi-lo>1:
   m=(hi+lo)//2
   if m**200<=u:lo=m
   else:hi=m
  need(lo**200<=u<hi**200,'endpoint root');powers[r]=(F(lo,den),F(lo if lo**200==u else hi,den))
 def moment(x):
  lo=hi=F(0)
  for r,c in x.items():
   l,u=powers[r];lo+=c*(l if c>=0 else u);hi+=c*(u if c>=0 else l)
  return lo,hi
 cap={q:moment(linear((1,B),(-1,{7:222,8:q}))) for q in [8,9,10,11,12,14,15]}
 ss=moment(S);need(ss[1]<0 and cap[11][1]<0 and cap[10][0]>0,'packet boundary signs')
 need(F(37,3)>F(88,49),'strict derivative bound')
 one=sum(r*c for r,c in B.items())-222*7-11*8;need(one>0,'t1 negative control')
 out={'status':'PASS_EXACT_MONOTONE_PACKET_CAP_ENDPOINTS','source_sha256':PIN,'target_t':'199/200','limiting_allowance':list(map(str,moment(B))),'finite_m_correction_S':list(map(str,ss)),'limiting_margins_by_q':{str(q):list(map(str,v)) for q,v in cap.items()},'simplified_allowance_profile':{str(r):str(c) for r,c in B.items()},'H_minus_N':{str(r):str(c) for r,c in D.items()},'derivative_positive_lower_bound':str(F(37,3)-F(88,49)),'t1_q11_positive_control':str(one),'proved_interval_by_written_monotonicity':'0<=t<=199/200 (1/200<=k<=1)','scope':'Retained signed-moment tests for monotone whole-V routes; q<=10 necessary only. No supplier or kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'allowance':float(moment(B)[0]),'S':float(ss[0]),'q_margins':{q:float(v[0]) for q,v in cap.items()}}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
