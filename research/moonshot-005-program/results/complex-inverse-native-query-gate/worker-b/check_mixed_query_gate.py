#!/usr/bin/env python3
"""Finite exact controls of the rank band and the strict threshold, not a universal proof."""
import itertools,json,random
from pathlib import Path
par=lambda x:x.bit_count()%2
def omega(a,b):return par((a&7)&(b>>3))^par((a>>3)&(b&7))
I=tuple(1<<i for i in range(6))
def apply(g,v):
 w=0
 for i in range(6):
  if v>>i&1:w^=g[i]
 return w
mul=lambda g,h:tuple(apply(g,v) for v in h)
def rank3(cols):
 basis={}
 for v in cols:
  while v:
   i=v.bit_length()-1
   if i not in basis:basis[i]=v;break
   v^=basis[i]
 return len(basis)
def gr(g):return rank3([g[i]&7 for i in range(3,6)])
trans=[tuple(v^(a if omega(v,a) else 0) for v in I) for a in range(1,64)]
rng=random.Random(141530);catalog=[I];g=I
for k in range(255):
 g=mul(rng.choice(trans),g);catalog.append(g)
counts={r:sum(gr(g)==r for g in catalog) for r in range(4)}
assert all(counts.values())
assert all(omega(g[i],g[j])==omega(I[i],I[j]) for g in catalog for i in range(6) for j in range(6))
checks=0
for g,h in itertools.product(catalog,repeat=2):
 a,b,c=gr(g),gr(h),gr(mul(g,h))
 assert abs(a-b)<=c<=a+b
 checks+=1
# Exact abstract graded model threshold: base diag(z,z), one z^2 query per role.
# Endpoint diag(z^3,z^3) exists when h=s+b=3; this is not an actual native caller.
base_exponents=(1,1); query_a_exponents=(2,0); query_b_exponents=(0,2)
endpoint_exponents=tuple(sum(v) for v in zip(base_exponents,query_a_exponents,query_b_exponents))
assert endpoint_exponents==(3,3) and 3==1+2
out={'status':'PASS_FINITE_RANK_BAND_CONTROLS','symplectic_dimension':6,'catalog_size':len(catalog),'rank_counts':counts,'exact_product_pairs':checks,'negative_controls':{'strict_threshold_is_essential_formal_base1_queries22_can_give33':True,'formal_control_is_not_an_actual_native_identity':True},'proof':'MIXED-QUERY-PURE-ENDPOINT-GATE.md','new_kappa':False}
Path(__file__).with_name('MIXED-QUERY-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
