#!/usr/bin/env python3
"""Exact rational end-repair deficit in the retained normalized field grammar."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE='research/shared-wire-split-composition/data/final.json.gz'
def need(p,m):
 if not p:raise ValueError(m)
def add(a,b,c):
 for k,x in b.items():
  y=a.get(k,Q(0))+c*x
  if y:a[k]=y
  else:a.pop(k,None)
def rank(rows):
 basis={}
 for x in rows:
  a=x.copy()
  while a:
   c=min(a);q=a[c]
   if c not in basis:basis[c]={k:x/q for k,x in a.items()};break
   add(a,basis[c],-q)
 return len(basis)
def span(b):
 s={0}
 for x in b:s|={a^x for a in s}
 return frozenset(s)
def run(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw))
 M=set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);R={r:{r:Q(1)}for r in M}
 for e in w['program']:
  if e[0]=='SCALE'and e[1]in M:R[e[1]]={k:x*Q(e[2])for k,x in R[e[1]].items()}
  elif e[0]in('ADD','COPY')and e[1]in M and e[2]in M:
   need(e[0]=='ADD','main skeleton has no COPY');add(R[e[1]],R[e[2]],Q(e[3]))
 E={r:{r:Q(1)}for r in M};D=set(w['hosted']['Dports'])
 for i,x in enumerate(w['live']):
  if i in D:E[x+112][x]=Q(1)
  else:E[x][x+112]=Q(-1);E[x+112]={x:Q(1,2),x+112:Q(1,2)}
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):E[x][y]=Q(-1)
 need(rank(list(R.values()))==rank(list(E.values()))==400,'full endpoint ranks')
 groups=collections.defaultdict(list)
 for r in sorted(M):groups[span(w['frames'][w['final'][r]])].append(r)
 rows=[];control=False
 for fr,rs in groups.items():
  a=[R[r]for r in rs];desired=[E[r]for r in rs];d=rank(a+desired)-rank(a)
  rows.append({'roles':rs,'frame_dimension':len(fr).bit_length()-1,'deficit':d})
  if d>0 and not control:
   for er in desired:
    if rank(a+[er])>rank(a):
     need(rank(a+[er]+desired)-rank(a+[er])==d-1,'one paid arrival reduces one deficit');control=True;break
 total=sum(z['deficit']for z in rows);need(total==208 and len(rows)==105,'exact deficit')
 need(rank(list(R.values())+list(E.values()))-rank(list(R.values()))==0,'illegally forgetting frames destroys barrier')
 upper=Q(1771183386,1000000);repaired=upper-18*total;need(repaired<0,'full caller loses target raw margin')
 return {'status':'PASS_EXACT_ENDPOINT_REPAIR_FLOOR','source_sha256':PIN,'rational_deficit':total,'frame_cohorts':len(rows),'cohort_deficits':rows,'paid_arrivals_per_native_lower':total,'extra_paid_moment_per_native_lower':str(total),'target_exponent':'199/200','hypothetical_H4_raw_upper':'1771.183386','repaired_raw_upper':str(repaired),'controls':['one new independent arrival lowers deficit by exactly one','collapsing all frame cohorts incorrectly makes deficit zero'],'scope':'Fixed-input balanced shared-core endpoint and retained normalized scalar/cochart-MOVE repair grammar, unchanged productive credits; no global shared-core impossibility or new kappa.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',type=Path);args=a.parse_args();src=args.source
 if src is None:src=next((d/SOURCE for d in Path(__file__).resolve().parents if(d/SOURCE).is_file()),None)
 need(src is not None,'provide source path');print(json.dumps(run(src),indent=2))
