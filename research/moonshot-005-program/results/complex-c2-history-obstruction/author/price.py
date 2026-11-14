#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,json,gzip,hashlib

def need(c,m):
 if not c:raise ValueError(m)
def floor_root(x,n):
 lo=0;hi=1<<((x.bit_length()+n-1)//n)
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**n<=x:lo=mid
  else:hi=mid
 need(lo**n<=x<(lo+1)**n,'integer root');return lo
powers={}
def power(r):
 if r not in powers:
  den=10**35;z=r**199*den**200;t=floor_root(z,200);powers[r]=(F(t,den),F(t if t**200==z else t+1,den))
 return powers[r]
def moment(profile):
 a=b=F(0)
 for r,c in profile.items():
  x,y=power(r);a+=c*(x if c>=0 else y);b+=c*(y if c>=0 else x)
 return a,b
def combine(*terms):
 z=Counter()
 for scale,prof in terms:
  for k,v in prof.items():z[int(k)]+=scale*v
 return {k:v for k,v in z.items() if v}
def enc(obj):
 if isinstance(obj,F):return str(obj)
 if isinstance(obj,dict):return {str(k):enc(v) for k,v in obj.items()}
 if isinstance(obj,(list,tuple)):return [enc(v) for v in obj]
 return obj

def main(a):
 raw=a.full.read_bytes();need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','full source');f=json.loads(raw)
 r=json.loads(a.receipt.read_text());need(r['variant']=='parent' and r['status']=='PASS_C2_PASSIVE_HISTORY_ZERO_GRAM_INTERSECTION','parent receipt')
 raw_parent=a.parent.read_bytes();need(hashlib.sha256(raw_parent).hexdigest()=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','actual parent source');q=json.loads(gzip.decompress(raw_parent));actual=Counter(abs(len(q['frames'][o[2]])-len(q['frames'][o[3]])) for o in q['program'][:q['consumer']['begin']] if o[0]=='MOVE')
 Q={int(k):v for k,v in r['source_bill']['moves'].items()};need(Q==dict(actual),'actual stripped source profile');T=f['invoice']['T'];P=f['invoice']['P'];N=f['native']['paid'];H=f['native']['helpers']
 slope=combine((F(1,18),T),(F(-1,18),P));room=combine((1,slope),(1,N),(-1,H),(-1,Q));debit={1:16,7:8,9:-8}
 M=moment(room);D=moment(combine((-1,slope)));cost=moment({7:9});deficit=moment(combine((1,room),(-1,{7:9})));need(M[0]>0 and deficit[1]<0 and D[0]>0,'strict all-fixed-m exclusion')
 four=moment(combine((1,room),(-1,debit),(-1,{7:9})));need(four[1]<deficit[0],'four-ferry debit worsens limit')
 eight=moment(combine((1,room),(-1,{7:8})));need(eight[0]>0,'old eight-observation tariff positive control')
 out={'status':'PASS_NINE_C2_RETURNS_EXCEED_RETAINED_LIMIT','full_source_sha256':hashlib.sha256(raw).hexdigest(),'target_kappa':'1/200','stripped_parent_profile':Q,'limiting_allowance':M,'nine_rank7_moment':cost,'limiting_signed_margin':deficit,'four_ferry_limiting_signed_margin':four,'positive_finite_m_penalty_coefficient':D,'finite_m_formula':'limiting_margin-d/(m-1), m>=2 fixed independently of input size','eight_rank7_positive_control':eight,'display':{'allowance':float(M[0]),'nine_returns':float(cost[0]),'limiting_margin':float(deficit[0]),'four_ferry_margin':float(four[0])},'scope':'Only the retained full caller and one C2-to-Hub rank7 return per acquired whole-field observation. Arbitrary recoded/relayed sources, different target codes, and other invoices are not excluded. Forward/ordinary/physical duties granted free in this necessary test.'}
 a.output.write_text(json.dumps(enc(out),sort_keys=True,indent=2)+'\n');print(json.dumps(out['display'],indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
