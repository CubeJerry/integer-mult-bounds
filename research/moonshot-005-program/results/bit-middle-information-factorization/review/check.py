#!/usr/bin/env python3
"""Separate finite fields/nonlinear controls; no author code imported."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

def need(value,label):
 if not value:raise ValueError(label)
def span(vectors,p,n):
 out={(0,)*n}
 for v in vectors:out={tuple((x[i]+c*v[i])%p for i in range(n))for x in out for c in range(p)}
 return frozenset(out)
def spaces(p,n):
 zero=span([],p,n);seen={zero};todo=[zero];vecs=list(product(range(p),repeat=n))
 while todo:
  U=todo.pop()
  for v in vecs:
   if v not in U:
    V=span(list(U)+[v],p,n)
    if V not in seen:seen.add(V);todo.append(V)
 return sorted(seen,key=lambda s:(len(s),sorted(s)))
def dim(U,p):
 n=len(U);d=0
 while n>1:need(n%p==0,'vector-space cardinality');n//=p;d+=1
 return d
def observation(U,p,n):return [tuple(sum(a*b for a,b in zip(x,r))%p for r in sorted(U))for x in product(range(p),repeat=n)]
def ternary():
 SS=spaces(3,2);need(len(SS)==6,'ternary subspaces');cases=0;reps=0
 for U,V in product(SS,repeat=2):
  a,b,c=observation(U,3,2),observation(V,3,2),observation(U&V,3,2)
  for mask in range(512):
   f=[(mask>>i)&1 for i in range(9)]
   def factors(obs):
    table={}
    for x,y in zip(obs,f):
     if x in table and table[x]!=y:return False
     table[x]=y
    return True
   need((factors(a)and factors(b))==factors(c),'ternary common functions');cases+=1
  hall=dim(U,3)>=1 and dim(V,3)>=1 and dim(span(U|V,3,2),3)>=2
  brute=any(dim(span([u,v],3,2),3)==2 for u in U for v in V)
  need(hall==brute,'ternary representatives');reps+=1
 return {'spaces':6,'boolean_common_function_cases':cases,'representative_cases':reps}
def compression():
 SS=spaces(2,2);need(len(SS)==5,'binary subspaces')
 fs={s:list(product(range(1<<s),repeat=4))for s in range(3)};cases=positive=searched=0
 for V,E in product(SS,repeat=2):
  t,eobs=observation(V,2,2),observation(E,2,2)
  for e,l in product(range(3),repeat=2):
   legal=[f for f in fs[e]if all(eobs[i]!=eobs[j]or f[i]==f[j]for i in range(4)for j in range(i))]
   found=False
   for first in legal:
    for second in fs[l]:
     searched+=1
     if all((first[i],second[i])!=(first[j],second[j])or t[i]==t[j]for i in range(4)for j in range(i)):
      found=True;break
    if found:break
   r=dim(V,2);criterion=r<=e+l and r-dim(V&E,2)<=l
   need(found==criterion,'all deterministic compression encoders');cases+=1;positive+=found
 return {'cases':cases,'actual_encoder_pairs_examined':searched,'positive_cases':positive,
         'domain':'all functions on four input points with zero/one/two-bit messages'}
def add9(x,y):return ((x%3+y%3)%3)+3*((x//3+y//3)%3)
def mul9(x,y):
 a,b=x%3,x//3;c,d=y%3,y//3
 return ((a*c-b*d)%3)+3*((a*d+b*c)%3)
def smallfield():
 points=list(product(range(3),repeat=2))
 private=[[x for x,y in points],[y for x,y in points],[(x+y)%3 for x,y in points],[(x+2*y)%3 for x,y in points]]
 solutions=0
 for f in product(range(3),repeat=9):
  if all(len(set(zip(f,g)))==9 for g in private):solutions+=1
 need(solutions==0,'four-audience ternary failure')
 need(mul9(3,3)==2,'GF9 relation')
 need(all(any(mul9(x,y)==1 for y in range(1,9))for x in range(1,9)),'GF9 inverses')
 ranges=[]
 for kind in range(4):
  out=set()
  for x,y in product(range(9),repeat=2):
   shared=add9(x,mul9(3,y));priv=[x,y,add9(x,y),add9(x,mul9(2,y))][kind];out.add((shared,priv))
  need(len(out)==81,'extension simultaneous assignment');ranges.append(len(out))
 return {'fanout':4,'ternary_functions_examined':3**9,'ternary_nonlinear_solutions':solutions,'GF9_pair_ranges':ranges}
def main():
 ap=ArgumentParser();ap.add_argument('--author',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
 result={'status':'PASS_INDEPENDENT_MIDDLE_INFORMATION_REVIEW','author_code_imported':False,'ternary':ternary(),
         'nonlinear_compression':compression(),'small_field':smallfield(),
         'scope':'saturated local information interface only; no physical source or pure-wave invertibility'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 pins={str(p.relative_to(a.author)):sha256(p.read_bytes()).hexdigest()for p in [a.author/'PROOF.md',a.author/'check.py',a.author/'output/RESULT.json']}
 (a.out/'REVIEW-PINS.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n');print(result['status']);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
