#!/usr/bin/env python3
"""Exact optimistic caller remainder for the support-span capture schedule."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def linear(*terms):
 result={}
 for c,pr in terms:
  for r,a in pr.items():result[r]=result.get(r,F(0))+c*a
 return {r:a for r,a in result.items() if a}
def bracket(r):
 scale=1<<128;target=r**199*scale**200;lo,hi=0,r*scale+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 need(lo**200<=target<hi**200,'outward power bounds')
 return F(lo,scale),F(hi,scale)
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'paired receipt')
 z=json.loads(raw);N,H,P,T=[{int(r):F(c) for r,c in z[k].items()} for k in ['native_paid','helper_target','paired_paid','paired_target']]
 S=linear((F(1,36),T),(F(-1,36),P));B=linear((1,N),(-1,H),(1,S))
 ranks=set(S)|set(B)|set(range(1,9));intervals={r:bracket(r) for r in ranks}
 def ev(pr):
  lo=hi=F(0)
  for r,c in pr.items():
   l,h=intervals[r];lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
  return lo,hi
 capture={1:4,2:15,3:84,4:84,5:15,6:4,7:8}
 extra=ev(linear((1,capture),(-1,{7:111})))
 records={}
 for q in [8,9,10]:
  lower=linear((1,capture),(1,{7:111,8:q}));lim=linear((1,B),(-1,lower))
  records[str(q)]={'schedule_profile':{str(r):str(c) for r,c in lower.items()},
                   'limiting_remainder_interval':list(map(str,ev(lim))),
                   'finite_m_remainder_intervals':{str(m):list(map(str,ev(linear((1,lim),(F(1,m-1),S))))) for m in [2,4,6,8]}}
 need(F(records['9']['limiting_remainder_interval'][0])>0,'q9 optimistic room')
 need(F(records['10']['limiting_remainder_interval'][0])>0,'q10 optimistic room')
 out={'status':'PASS_HALFCLASS_CAPTURE_SCHEDULE_ALLOWANCE','paired_source_sha256':PIN,'t':'199/200',
      'X_capture_profile':capture,'capture_overhead_interval':list(map(str,extra)),
      'q_profiles':records,'scope':'Support-span capture schedule plus optimistic direct Y and packet routes; future decoder movement and ordinary/owned/compiler costs remain.',
      'new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'capture_extra_approx':float(extra[0]),
                   'limiting_remainder_approx':{q:float(F(v['limiting_remainder_interval'][0])) for q,v in records.items()}}))
if __name__=='__main__':main()
