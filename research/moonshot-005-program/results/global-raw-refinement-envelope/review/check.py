#!/usr/bin/env python3
"""Independent decimal-seeded, integer-certified H4 envelope audit."""
import argparse,gzip,hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path

def need(v,m):
 if not v:raise ValueError(m)
def rank_binary(vectors):
 piv={}
 for v in vectors:
  while v:
   j=v.bit_length()-1
   if j not in piv:piv[j]=v;break
   v^=piv[j]
 return len(piv)
def main(a):
 raw=a.source.read_bytes();inv=a.invoice.read_bytes()
 need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin')
 need(hashlib.sha256(inv).hexdigest()=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248','invoice pin')
 s=json.loads(gzip.decompress(raw));bill=json.loads(inv);author=json.loads(a.author.read_text())
 fields=set(s['live'])|{r+112 for r in s['live']}|set(s['hosted']['X2'])|set(s['hosted']['Y2'])
 need(len(fields)==400,'400 physical routes')
 endpoints=[(r,rank_binary(s['frames'][s['initial'][r]]),rank_binary(s['frames'][s['final'][r]])) for r in sorted(fields)]
 need(all(b-a==8 for r,a,b in endpoints),'400 independently ranked endpoint gaps')
 old=Counter()
 for o in s['program']:
  if o[0]=='MOVE' and o[1] in fields:
   d=rank_binary(s['frames'][o[3]])-rank_binary(s['frames'][o[2]])
   need(d>0,'strict source raw ascent');old[d]+=1
 need(sum(old.values())==1710 and sum(k*v for k,v in old.items())==3200,'source count and mass')
 P=Counter({int(k):v for k,v in bill['P4'].items()});T=Counter({int(k):v for k,v in bill['T4'].items()});D=10**40;powers={}
 for r in set(P)|set(T)|{1,8,9}:
  with localcontext() as c:
   c.prec=100;v=(Decimal(r)**(Decimal(199)/200))*D;n=int(v)
  target=r**199*D**200
  while n**200>target:n-=1
  while (n+1)**200<=target:n+=1
  need(n**200<=target<(n+1)**200,'exact integer power enclosure')
  powers[r]=(F(n,D),F(n,D) if n**200==target else F(n+1,D))
 def interval(coeff):
  lo=hi=F(0)
  for r,n in coeff.items():
   a,b=powers[r];lo+=n*(a if n>=0 else b);hi+=n*(b if n>=0 else a)
  return lo,hi
 cases={}
 for name,straight,extra in [('direct_baseline',400,0),('all_unit',0,0),('all_unit_plus16',0,16),('24_direct_plus16',24,16),('25_direct_plus16',25,16)]:
  H=dict(P)
  for r,n in old.items():H[r]=H.get(r,0)-18*n
  H[1]=H.get(1,0)+18*(8*(400-straight)+extra)
  H[8]=H.get(8,0)+18*straight;H[9]=H.get(9,0)+144
  need(all(v>=0 for v in H.values()),'nonnegative caller')
  lo,hi=interval({r:T[r]-H.get(r,0) for r in T.keys()|H.keys()});lo/=18;hi/=18
  claimed=author['cases'][name];a0,a1=map(F,claimed['moment_per_native_exact_bounds'])
  need(a0<=lo<=hi<=a1,'independent narrower interval within author interval')
  need(H=={int(k):v for k,v in claimed['complete_paid_histogram'].items()},'complete substituted histogram')
  cases[name]={'bounds':[str(lo),str(hi)],'approximate':float(lo),'paid_count':sum(H.values()),'rank_surplus':sum(r*(T[r]-H.get(r,0)) for r in T.keys()|H.keys())}
 need(F(cases['25_direct_plus16']['bounds'][0])>0 and F(cases['24_direct_plus16']['bounds'][1])<0,'exact positive and negative controls')
 need(cases['25_direct_plus16']['paid_count']==176526 and cases['25_direct_plus16']['rank_surplus']==3472,'full caller aggregate')
 base=interval({r:T[r]-P[r] for r in T.keys()|P.keys()});rawint=interval(old)
 result={'status':'PASS_INDEPENDENT_GLOBAL_RAW_ENVELOPE','author_proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'author_script_sha256':hashlib.sha256(a.script.read_bytes()).hexdigest(),'author_result_sha256':hashlib.sha256(a.author.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(raw).hexdigest(),'invoice_sha256':hashlib.sha256(inv).hexdigest(),'all400_endpoint_rank_gaps':8,'old_raw_histogram':dict(sorted(old.items())),'base_H_bounds':[str(v/18) for v in base],'old_raw_moment_bounds':list(map(str,rawint)),'cases':cases,'scope':'Independent source/whole-invoice audit, no author imports or author numeric root routine. Monotone route envelope only; no actual global code or legal finishing rows supplied. No new kappa.'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'cases':cases},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['source','invoice','author','proof','script','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
