#!/usr/bin/env python3
"""Independent complete-caller rational-interval comparison."""
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
def need(b,s):
 if not b:raise ValueError(s)
def main(a):
 b=a.full.read_bytes();need(hashlib.sha256(b).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','caller pin');f=json.loads(b)
 b=a.parent.read_bytes();need(hashlib.sha256(b).hexdigest()=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','parent pin');q=json.loads(gzip.decompress(b))
 paid=Counter(abs(len(q['frames'][o[2]])-len(q['frames'][o[3]])) for o in q['program'][:q['consumer']['begin']] if o[0]=='MOVE')
 T={int(k):F(v) for k,v in f['invoice']['T'].items()};P={int(k):F(v) for k,v in f['invoice']['P'].items()};N={int(k):F(v) for k,v in f['native']['paid'].items()};H={int(k):F(v) for k,v in f['native']['helpers'].items()}
 ranks=sorted(set(T)|set(P)|set(N)|set(H)|set(paid)|{1,7,9});powers={};den=10**24
 for r in ranks:
  target=r**199*den**200;lo=0;hi=r*den+1
  while hi-lo>1:
   m=(hi+lo)//2
   if m**200<=target:lo=m
   else:hi=m
  need(lo**200<=target<hi**200,'outward interval');powers[r]=(F(lo,den),F(lo if lo**200==target else hi,den))
 slope={r:(T.get(r,0)-P.get(r,0))/18 for r in ranks};room={r:slope[r]+N.get(r,0)-H.get(r,0)-paid.get(r,0) for r in ranks}
 def moment(profile):
  l=u=F(0)
  for r,c in profile.items():
   x,y=powers[r];l+=c*(x if c>=0 else y);u+=c*(y if c>=0 else x)
  return l,u
 def deficit(n,four=False):
  x=dict(room);x[7]-=n
  if four:
   for r,v in {1:16,7:8,9:-8}.items():x[r]-=v
  return moment(x)
 d=moment({r:-v for r,v in slope.items()});r8=deficit(8);r9=deficit(9);r94=deficit(9,True)
 need(d[0]>0 and r8[0]>0 and r9[1]<0 and r94[1]<r9[0],'strict all-fixed-m controls')
 out={'status':'PASS_INDEPENDENT_NINE_C2_COMPLETE_TARIFF','interval_grid':'1e-24','limiting_allowance':list(map(str,moment(room))),'eight_return_margin':list(map(str,r8)),'nine_return_margin':list(map(str,r9)),'four_ferry_nine_margin':list(map(str,r94)),'positive_finite_m_penalty':list(map(str,d)),'finite_m_formula':'margin(m)=margin(infinity)-d/(m-1), fixed integer m>=2','source_profile':dict(paid),'scope':'Retained complete caller with rank7 returns; other completion costs optimistically zero. Changed sources/codes/invoices not excluded.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'margin9':float(r9[0]),'margin8':float(r8[0]),'penalty':float(d[0])}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['full','parent','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
