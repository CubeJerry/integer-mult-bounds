#!/usr/bin/env python3
"""Exact real geometry of the native chain's whole-block supports."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def need(ok,msg):
 if not ok:raise ValueError(msg)

def row_basis(rows,prime=None):
 piv={};chosen=[]
 for i,row in enumerate(rows):
  z=[(int(x.numerator)*pow(int(x.denominator),-1,prime))%prime if prime else Fraction(x) for x in row]
  for p,b in sorted(piv.items()):
   if z[p]:
    a=z[p];z=[(x-a*y)%prime if prime else x-a*y for x,y in zip(z,b)]
  p=next((j for j,x in enumerate(z) if x),None)
  if p is None:continue
  a=pow(z[p],-1,prime) if prime else 1/z[p]
  z=[x*a%prime if prime else x*a for x in z];piv[p]=z;chosen.append(i)
 return chosen

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def parity_xor(xs):
 x=0
 for a in xs:x^=a
 return x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw))
 roots=[list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 K=[sum(int(i==j or dot(x,y)==0)<<j for j,y in enumerate(roots)) for i,x in enumerate(roots)]
 changed=[7,24,25];T=[j for j in range(111) if j not in changed and all(K[i]>>j&1 for i in changed)]
 need(len(T)==36 and T[-4:]==[103,105,107,109],'native chain contacts')
 p=sum(1<<j for j in T[:-4]);h=[p^(1<<103),1<<105,1<<107,p^(1<<109)]
 H=[h[:2],h[1:3],h[2:]];selectors=[[1,4],[3,4],[1,6]]
 monomials=list(itertools.combinations_with_replacement(range(7),2));rows=[];canonical_minors=[];forms={
  24:[[1,-1,0,-1,0,0,-1],[1,-1,0,-1,0,0,1]],
  25:[[1,1,0,-1,0,0,-1],[1,1,0,-1,0,0,1]]}
 q_terms={(1,6):-2,(2,2):1,(2,5):-4,(3,3):-1,(4,4):-1,(5,5):1}
 q=[Fraction(q_terms.get(z,0)) for z in monomials]
 Q=[[Fraction(0) for _ in range(7)] for _ in range(7)]
 for (b,c),x in zip(monomials,q):Q[b][c]=Q[c][b]=x if b==c else x/2
 need(len(row_basis(Q))==6,'rank-six nonfactorable quadratic')
 for i,k in enumerate(K):
  pivot=next(j for j,x in enumerate(roots[i]) if x);free=[j for j in range(8) if j!=pivot]
  canonical=[j for j in range(111) if j!=i and k>>j&1]
  y={j:[roots[j][t] for t in free] for j in canonical};quad=lambda v:[v[b]*v[c] for b,c in monomials]
  full_basis=row_basis([quad(y[j]) for j in canonical],257)
  need(len(full_basis)==28,'canonical support has full real quadratic span by mod257 minor')
  canonical_minors.append({'receiver':i,'facet_free_coordinates':free,'basis_source_indices':[canonical[b] for b in full_basis]})
  U=selectors[changed.index(i)] if i in changed else [0,0]
  blocks=[[parity_xor(H[b][t] for b in range(3) if U[r]>>b&1)^(k if r==t else 0) for t in range(2)] for r in range(2)]
  active=blocks[0][0]|blocks[0][1]|blocks[1][0]|blocks[1][1];support=[j for j in canonical if active>>j&1]
  need(active&~k==0,'no forbidden support')
  linrank=len(row_basis([y[j] for j in support])) if i in changed else 7
  quadrank=len(row_basis([quad(y[j]) for j in support])) if i in changed else 28
  card=int(len(support)>36)+int(len(support)>52);gamma=int(linrank==7)+int(quadrank==28)
  cover_charge=2 if i not in changed else None
  extra={}
  if i==7:
   need(free==list(range(7)) and linrank==7 and quadrank==27,'first changed support exact ranks')
   need(all(dot(q,quad(y[j]))==0 for j in support),'unique quadratic vanishes on support')
   cover_charge=2;extra={'unique_quadratic_coefficients':[str(x) for x in q],'quadratic_matrix_rank':6,
                       'two_proper_subspace_cover':'impossible: unique vanishing quadratic has rank6, products have rank<=2'}
  if i in forms:
   need(free==list(range(1,8)) and linrank==7 and quadrank==(27 if i==24 else 26),'other changed support exact ranks')
   f,g=forms[i];need(all(dot(f,y[j])*dot(g,y[j])==0 for j in support),'explicit two-hyperplane cover')
   need(len(row_basis([list(map(Fraction,f)),list(map(Fraction,g))]))==2,'distinct proper hyperplanes')
   cover_charge=1;extra={'covering_hyperplane_forms':forms[i]}
  rows.append({'receiver':i,'foreign_support_count':len(support),'cardinality_charge':card,
               'linear_rank':linrank,'quadratic_rank':quadrank,'rank_proxy_gamma':gamma,
               'exact_capped_proper_cover_charge':cover_charge,**extra})
 need(sum(r['cardinality_charge'] for r in rows)==216,'cardinality total216')
 need(sum(r['rank_proxy_gamma'] for r in rows)==219,'linear/quadratic rank proxy219')
 need(sum(r['exact_capped_proper_cover_charge'] for r in rows)==220,'stronger cover charge220')
 need(all(r['foreign_support_count']==28 for r in rows if r['receiver'] in changed),'changed supports28')
 out={'status':'PASS_EXACT_CHAIN_GEOMETRY','native_sha256':PIN,'cardinality_charge':216,'rank_proxy_gamma':219,
      'exact_capped_proper_cover_charge':220,'quadratic_monomial_order':monomials,'changed_rows':[r for r in rows if r['receiver'] in changed],
      'canonical_mod257_quadratic_basis_certificates':canonical_minors,'all_rows':rows,
      'classification':'necessary support geometry; no physical acquisition, chronology, decoding or cost realization','new_kappa':None}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','cardinality_charge','rank_proxy_gamma','exact_capped_proper_cover_charge']}))
if __name__=='__main__':main()
