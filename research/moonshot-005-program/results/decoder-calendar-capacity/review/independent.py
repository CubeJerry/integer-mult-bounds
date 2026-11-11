"""Independent finite-field lower certificate; no author scientific imports."""
import argparse,gzip,hashlib,json,math
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
P=1000003;PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,s):
 if not b:raise ValueError(s)
def add(a,b,c):
 for j,x in b.items():
  z=(a.get(j,0)+c*x)%P
  if z:a[j]=z
  else:a.pop(j,None)
def insert(row,b):
 a=row.copy()
 while a:
  j=max(a)
  if j not in b:
   u=pow(a[j],-1,P);b[j]={k:x*u%P for k,x in a.items()};return 1
  add(a,b[j],-a[j])
 return 0
def c(x):
 f=Fraction(x);need(f.denominator%P!=0,'source denominator invertible');return f.numerator*pow(f.denominator,-1,P)%P
def canon(vs):
 b={}
 for x in vs:
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 for j in sorted(b):
  for k in b:
   if k>j and (b[k]>>j)&1:b[k]^=b[j]
 return tuple(b[j] for j in sorted(b))
def run(source,author):
 need(all(P%d for d in range(2,math.isqrt(P)+1)),'prime');raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));expected=json.loads(author.read_text());n=w['public'];m=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 rows=[[{r:1} if r<n else {} for r in range(n+w['owned_fields'])],[{r:1} if r in m else {} for r in range(n+w['owned_fields'])]];groups={};key=[groups.setdefault(canon(f),i) for i,f in enumerate(w['frames'])];need(len(groups)==1094,'frame aliases');frame=w['initial'][:]+[None]*w['owned_fields'];bases=[defaultdict(dict),defaultdict(dict)]
 for j in (0,1):
  for r in range(n):insert(rows[j][r],bases[j][key[frame[r]]])
 initial={f:len(bases[0][f])+len(bases[1][f]) for f in set(bases[0])|set(bases[1])};need(sum(initial.values())==1880,'exact initial unit rows')
 net={k:Counter() for k in (1,2)};peak={k:Counter() for k in (1,2)};argmax={k:{} for k in (1,2)};records=[];prefix={}
 for i,e in enumerate(w['program']):
  op,r=e[:2]
  if op in ('INIT','CLEAR'):
   need(r>=n and (frame[r] is None if op=='INIT' else frame[r]==e[2]),'owned lifetime');frame[r]=e[2] if op=='INIT' else None;rows[0][r]={};rows[1][r]={}
  elif op=='MOVE':
   need(frame[r]==e[2] and bool(e[4])==(r>=n),'typed MOVE');frame[r]=e[3];f=key[e[3]];fresh=[insert(rows[j][r],bases[j][f]) for j in (0,1)];kind='main' if r in m else 'helper' if r<n else 'owned';records.append([i,r,f,kind,*fresh])
   for k in (1,2):
    funded=2 if kind=='main' else k if kind=='owned' else 1;net[k][f]+=sum(fresh)-funded
    if net[k][f]>peak[k][f]:peak[k][f]=net[k][f];argmax[k][f]=i
  elif op=='SCALE':
   need(frame[r]==e[3] and c(e[2])!=0,'SCALE')
   for j in (0,1):rows[j][r]={a:x*c(e[2])%P for a,x in rows[j][r].items()}
  elif op in ('ADD','COPY'):
   s=e[2];need(r!=s and frame[r]==frame[s]==e[4],'cochart scalar')
   for j in (0,1):
    if op=='COPY':need(not rows[j][r],'COPYzero')
    add(rows[j][r],rows[j][s],c(e[3]))
  if i+1 in (25489,25490,25728,26226,36961,71261):prefix[str(i+1)]={str(k):sum(peak[k].values()) for k in (1,2)}
 floors={str(k):sum(peak[k].values()) for k in (1,2)};charts={str(k):{str(f):{'floor':v,'maximizing_event':argmax[k][f]} for f,v in sorted(peak[k].items()) if v>0} for k in (1,2)}
 need(records==expected['arrival_innovations'],'all6310 innovation records agree');need(floors==expected['extra_arrival_floor'] and charts==expected['by_chart'],'all chart maxima agree');need(prefix==expected['prefix_lower_bounds'],'all prefix bounds agree')
 need(all(a+b<=2 and a<=1 for _,_,_,_,a,b in records),'two-fields/zero-difference relaxed controls')
 return {'status':'PASS_INDEPENDENT_MODULAR_ALL_LIVE_CAPACITY_LOWER_BOUND','method':'Independent sparse finite-field max-pivot replay with GF2 RREF aliases','prime':P,'source_sha256':PIN,'author_result_sha256':hashlib.sha256(author.read_bytes()).hexdigest(),'source_events':len(w['program']),'arrival_records_compared':len(records),'extra_arrival_floor':floors,'prefix_lower_bounds':prefix,'proof':'Source denominators invertible modulo prime; initial unit-row ranks exact; rational history rank is at least modular history rank. Per-chart prefix deficits are rigorous rational lower bounds.','scope':'Fixed funded arrival calendar and all-live current-cochart two-copy decoder; pointwise/future-demand decoders and changed calendars remain open.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();z=run(a.source,a.author);a.output.write_text(json.dumps(z,indent=2)+'\n');print(json.dumps(z,indent=2))
