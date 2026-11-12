#!/usr/bin/env python3
"""Independent all-matrix small-field test for the shared column-lift theorem."""
import argparse,hashlib,itertools,json
from pathlib import Path

def rank(M,p):
 if not M:return 0
 a=[list(r) for r in M];i=0
 for j in range(len(a[0])):
  k=next((k for k in range(i,len(a)) if a[k][j]%p),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i];v=pow(a[i][j],-1,p);a[i]=[x*v%p for x in a[i]]
  for k in range(i+1,len(a)):
   v=a[k][j]
   if v:a[k]=[(x-v*y)%p for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i

def matrices(m,n,p):
 for flat in itertools.product(range(p),repeat=m*n):yield tuple(tuple(flat[i*n:(i+1)*n]) for i in range(m))
def product(A,V):return tuple(tuple(sum(x*y for x,y in zip(row,col))%p for col in zip(*V)) for row in A)
ap=argparse.ArgumentParser();ap.add_argument('--proof',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();cases=0;domains=[]
for p,r in [(2,0),(2,1),(2,2),(2,3),(3,1),(3,2)]:
 m=2;count=0
 for d in range(r+2):
  lifts=[V for V in matrices(r,d,p) if rank(V,p)==d]
  for A in matrices(m,r,p):
   ra=rank(A,p);actual=set()
   for V in lifts:
    if r:actual.add(product(A,V))
    elif not d:actual.add(tuple(() for _ in range(m)))
   for B in matrices(m,d,p):
    rb=rank(B,p);joined=tuple(a+b for a,b in zip(A,B));criterion=rank(joined,p)==ra and d-rb<=r-ra
    assert (B in actual)==criterion,(p,r,d,A,B)
    count+=1
 domains.append({'field':p,'rows':m,'existing_width':r,'tested_pairs':count});cases+=count
# The second condition alone does not reject every over-width request.
p=3;A=((0,0),(0,0),(0,0));B=((1,0,0),(0,1,0),(0,0,1));assert 3-rank(B,p)<=2-rank(A,p);assert rank(tuple(a+b for a,b in zip(A,B)),p)>rank(A,p)
# Exact duplication requires two, not one, zero padding columns.
p=2;A=((1,0),(0,1));B=((1,1,1),(0,0,0));ra=rank(A,p);rb=rank(B,p);assert max(0,3-rb-(2-ra))==2
out={'status':'PASS_INDEPENDENT_COLUMN_LIFT_REVIEW','proof_sha256':hashlib.sha256(args.proof.read_bytes()).hexdigest(),'domains':domains,'checked_matrix_pairs':cases,'negative_controls':['Image containment cannot be dropped.','Over-width second-inequality failure needs image containment.','Repeated coefficient columns need exact additional kernel width.'],'classification':'Finite coverage complements the independent universal proof review; no physical source or asymptotic theorem is inferred.'}
args.output.mkdir(parents=True,exist_ok=True);(args.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'],cases)
