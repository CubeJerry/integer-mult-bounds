#!/usr/bin/env python3
"""Independent integer-root complete tariffs for control-gate returns."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib
def need(b,s):
 if not b:raise ValueError(s)
def main(a):
 raw=a.full.read_bytes();need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','full caller pin');f=json.loads(raw);rec=json.loads(a.source_review.read_text());need(rec['status']=='PASS_INDEPENDENT_ALL_TIME_SOURCE_CONTROL','independent source receipt')
 profiles={k:{int(r):F(v) for r,v in f[group][key].items()} for k,group,key in [('T','invoice','T'),('P','invoice','P'),('N','native','paid'),('H','native','helpers')]}
 ranks=sorted(set().union(*(v.keys() for v in profiles.values()),*(set(map(int,z['bill']['moves'])) for z in rec['results'].values())));den=2**140;powers={}
 for r in ranks:
  target=r**199*den**200;lo=0;hi=r*den+1
  while hi-lo>1:
   m=(lo+hi)//2
   if m**200<=target:lo=m
   else:hi=m
  need(lo**200<=target<hi**200,'exact outward roots');powers[r]=(F(lo,den),F(lo if lo**200==target else hi,den))
 def moment(z):
  lo=hi=F(0)
  for r,c in z.items():
   x,y=powers[r];lo+=c*(x if c>=0 else y);hi+=c*(y if c>=0 else x)
  return lo,hi
 T,P,N,H=(profiles[k] for k in ['T','P','N','H']);slope={r:(T.get(r,0)-P.get(r,0))/18 for r in ranks};pen=moment({r:-c for r,c in slope.items()});need(pen[0]>0,'finite-m penalty positive');out={}
 for variant,v in rec['results'].items():
  paid={int(r):F(c) for r,c in v['bill']['moves'].items()};room={r:slope[r]+N.get(r,0)-H.get(r,0)-paid.get(r,0) for r in ranks};q=v['protected_count'];iv=moment(room);margin=(iv[0]-q,iv[1]-q);need(margin[1]<0,'all whole-field return room insufficient');out[variant]=dict(whole_field_floor=q,limiting_room=list(map(str,iv)),optimistic_rank1_margin=list(map(str,margin)),source_MOVE_profile={str(r):str(c) for r,c in paid.items()})
 need(F(out['four']['limiting_room'][1])<F(out['parent']['limiting_room'][0]),'four-ferry true debit')
 result=dict(status='PASS_INDEPENDENT_STATION_CONTROL_TARIFF',grid='2^-140 integer200th-root brackets',source_review_sha256=hashlib.sha256(a.source_review.read_bytes()).hexdigest(),positive_finite_m_penalty=list(map(str,pen)),cases=out,formula='margin(m)=margin(infinity)-penalty/(m-1), every fixed integer m>=2',scope='Actual whole-V capture/return interface only; fragments, changed recoding and travelling distributors require new invoices.',new_kappa=None)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'margins':{k:float(F(v['optimistic_rank1_margin'][1])) for k,v in out.items()}}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['full','source-review','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
