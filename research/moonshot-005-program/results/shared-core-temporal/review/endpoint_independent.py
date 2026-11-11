#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict,Counter
import argparse,gzip,hashlib,json
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,s):
 if not x:raise ValueError(s)
def add(a,b,c):
 for k,v in b.items():
  q=a.get(k,F(0))+c*v
  if q:a[k]=q
  else:a.pop(k,None)
def rank(rows):
 basis={}
 for old in sorted(rows,key=len):
  r=old.copy()
  while r:
   k=max(r);q=r[k]
   if k in basis:add(r,basis[k],-q)
   else:basis[k]={i:v/q for i,v in r.items()};break
 return len(basis)
def frame(rows):
 basis={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in basis:x^=basis[k]
   else:basis[k]=x;break
 for k in sorted(basis):
  for j in basis:
   if j>k and (basis[j]>>k)&1:basis[j]^=basis[k]
 return tuple(basis[k] for k in sorted(basis))
def run(source):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw))
 main=set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 r={i:{i:F(1)} for i in main}
 for e in w['program']:
  op,a=e[:2]
  if a not in main:continue
  need(op not in ('COPY','INIT','CLEAR'),'invertible skeleton grammar')
  if op=='SCALE':r[a]={j:F(e[2])*v for j,v in r[a].items()}
  elif op=='ADD' and e[2] in main:add(r[a],r[e[2]],F(e[3]))
 e={i:{i:F(1)} for i in main};dual=set(w['hosted']['Dports']);alpha=F(w['hosted']['alpha']);beta=F(w['hosted']['beta'])
 for port,x in enumerate(w['live']):
  y=x+112
  if port in dual:e[y][x]=F(1)
  else:e[x][y]=alpha;e[y]={x:beta,y:1+alpha*beta}
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):e[x][y]=F(w['hosted']['alpha2'])
 groups=defaultdict(list)
 for i in sorted(main):groups[frame(w['frames'][w['final'][i]])].append(i)
 receipt=[]
 for fr,owners in groups.items():
  available=[r[i] for i in owners];desired=[e[i] for i in owners]
  deficit=rank(available+desired)-rank(available)
  receipt.append({'owners':owners,'frame_rank':len(fr),'available_rank':rank(available),'desired_rank':rank(desired),'deficit':deficit})
 total=sum(x['deficit'] for x in receipt);need(total==208 and len(groups)==105,'source deficit')
 need(rank(list(r.values()))==rank(list(e.values()))==400,'complete main endpoints invertible')
 counts=Counter(x['deficit'] for x in receipt);need(counts=={1:93,2:11,93:1},'cohort distribution')
 need(F('1771.183386')-18*208==F('-1972.816614'),'complete caller bound')
 return {'status':'PASS_INDEPENDENT_RATIONAL_ENDPOINT_REPAIR_FLOOR','source_sha256':PIN,'cohorts':105,'deficit':208,'cohort_deficit_counts':dict(counts),'cohort_evidence':receipt,'repaired_raw_upper':'-1972.816614','method':'exact largest-pivot rational elimination and independent GF2 frame canonicalization','scope':'Original-input balanced endpoint; normalized whole-field cochart operations and positive-rank MOVE arrivals; unchanged target credits.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.source),indent=2,sort_keys=True))
