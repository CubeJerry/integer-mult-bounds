#!/usr/bin/env python3
"""Directed exact fixed-m price for the all-time D-control return bound."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,json
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def need(c,m):
 if not c:raise ValueError(m)
def root(a,n):
 lo=0;hi=1<<((a.bit_length()+n-1)//n)
 while hi-lo>1:
  x=(hi+lo)//2
  if x**n<=a:lo=x
  else:hi=x
 need(lo**n<=a<(lo+1)**n,'directed root bracket');return lo
powers={}
def power(r):
 if r not in powers:
  d=10**35;a=r**199*d**200;z=root(a,200);powers[r]=F(z,d),F(z if z**200==a else z+1,d)
 return powers[r]
def add(*terms):
 ans=Counter()
 for c,p in terms:
  for r,v in p.items():ans[int(r)]+=c*v
 return {r:v for r,v in ans.items() if v}
def moment(p):
 a=b=F(0)
 for r,c in p.items():
  lo,hi=power(r);a+=c*(lo if c>=0 else hi);b+=c*(hi if c>=0 else lo)
 return a,b
def enc(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {str(k):enc(z) for k,z in v.items()}
 if isinstance(v,(list,tuple)):return [enc(z) for z in v]
 return v
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--four',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.full.read_bytes();need(hashlib.sha256(raw).hexdigest()==FULL,'full caller source');f=json.loads(raw)
 slope=add((F(1,18),f['invoice']['T']),(F(-1,18),f['invoice']['P']));penalty=moment(add((-1,slope)));need(penalty[0]>0,'finite-m penalty positive')
 rr=[]
 for name,path,count in [('parent',a.parent,74),('four',a.four,66)]:
  raw=path.read_bytes();r=json.loads(raw);need(r['status']=='PASS_EXACT_ALL_TIME_D_STATION_B_INFLUENCE' and r['word_variant']==name and r['protected_D_count']==count,'exact control receipt')
  q={int(k):v for k,v in r['actual_source_bill']['moves'].items()};room=add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,q));R=moment(room);margin=moment(add((1,room),(-1,{1:count})));need(margin[1]<0,'whole-field return lower bound exceeds limiting room')
  rr.append({'source':name,'receipt_sha256':hashlib.sha256(raw).hexdigest(),'actual_stripped_MOVE_profile':q,'whole_field_return_lower_bound':count,'limiting_additional_moment_room':R,'limiting_margin_after_rank1_returns':margin,'display':{'limiting_room':float(R[0]),'limiting_margin':float(margin[0])}})
 blank=moment(add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,{8:400})))
 out={'status':'PASS_BOTH_ALL_FIXED_M_WHOLE_FIELD_RETURN_EXCLUSIONS','full_caller_sha256':FULL,'kappa':'1/200','finite_m_penalty_coefficient':penalty,'finite_m_formula':'limiting margin - d/(m-1), d>0, fixed integer m>=2','sources':rr,'optimistic_new_architecture_limit_after400_direct_rank8_raws':blank,'scope':'Necessary retained whole-field MOVE tariff only; every other added expense granted free. Fragmented or history-distributing travelling fields require their own invoices. No forward completion, supplier admission or new kappa.'}
 a.output.write_text(json.dumps(enc(out),sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'sources':[x['display'] for x in rr],'blank_limit':float(blank[0])},indent=2))
