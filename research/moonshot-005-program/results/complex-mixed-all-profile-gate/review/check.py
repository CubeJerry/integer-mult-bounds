#!/usr/bin/env python3
"""Independent SymPy-rational review of the fixed-Cmix head-budget gate.

No B implementation or inherited source arithmetic engine is imported.
The finite calculations support the separate all-tail proof in REVIEW.md.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product,combinations_with_replacement
from functools import lru_cache
from collections import Counter
import argparse,hashlib,json
import sympy as sp
I=sp.I;F=sp.Rational;D=16

def need(x,s):
 if not x:raise ValueError(s)
def monomial(fn):
 M=sp.zeros(D)
 for j in range(D):
  bits=tuple((j>>k)&1 for k in range(4));out,p=fn(*bits);dest=sum(x<<k for k,x in enumerate(out));M[dest,j]=I**(p%4)
 return sp.ImmutableMatrix(M)
def clean(M):return sp.ImmutableMatrix(M.applyfunc(sp.expand))
def dagger(M):return clean(M.conjugate().T)
def qpair(z):return (sp.re(z),sp.im(z))
def encode(M):return tuple(qpair(z)for z in M)
def dump(M):
 return {'dimension':D,'entries':[[r,c,str(sp.re(M[r,c])),str(sp.im(M[r,c]))]for r in range(D)for c in range(D)if M[r,c]]}
def row_size(M):
 counts={sum(bool(M[r,c])for c in range(D))for r in range(D)}
 need(len(counts)==1,'common nonzero row count');return counts.pop()
def rankclass(M):
 n=row_size(M);need(n in [1,2,4,8,16],'dyadic source class');return n.bit_length()-1

# Formal collective-word algebra, quotiented only by root-four scalars.
MATS={}
@lru_cache(None)
def key(M):
 choices=[(encode(clean(u*M)),clean(u*M))for u in [1,I,-1,-I]]
 e,v=min(choices,key=lambda x:x[0]);MATS[e]=v;return e
def atom(M,c=1):return {key(M):F(c)}if c else{}
def add(*forms):
 o={}
 for f in forms:
  for k,c in f.items():o[k]=o.get(k,0)+c
 return {k:sp.cancel(c)for k,c in o.items()if c}
def scale(f,c):return{k:sp.cancel(c*x)for k,x in f.items()if c*x}
@lru_cache(None)
def kproduct(a,b):return key(clean(MATS[a]*MATS[b]))
def mul(a,b):return add(*({kproduct(x,y):c*d}for x,c in a.items()for y,d in b.items()))
def matrixmul(A,B):return[[add(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
def proj(f,r):return{k:c for k,c in f.items()if rankclass(MATS[k])==r}

def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/workers/B/mixed-interface-total-head-gate'))
 p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 E=sp.ImmutableMatrix(sp.eye(D));Z=sp.ImmutableMatrix(sp.zeros(D))
 R=monomial(lambda a,b,c,d:((b,c,d,a),2*a*b*d))
 X=monomial(lambda a,b,c,d:((a,b^1,c,d),0))
 A=clean(((1+I)*E+(1-I)*X)*R/2)
 s=monomial(lambda a,b,c,d:((a,c,b,d),0))
 h=monomial(lambda a,b,c,d:((a,c,b,d),b-c))
 need(clean(A*dagger(A))==clean(s*s)==clean(h*h)==E,'literal source unitary and involutions')
 A2=clean(A*A);A3=clean(A2*A);B=clean(A*s*A)
 m=clean(dagger(A)*h*A2);q=clean(dagger(A)*h*s*h*A)
 need(clean(q*q)==E,'q involution');need(row_size(m)==8 and row_size(q)==4,'nonmonomial source witnesses')
 need(sp.trace(q)==8,'q trace8');plus=clean((E+q)/2)
 need(clean(plus*plus)==plus and sp.trace(plus)==12 and clean((E-q)*plus)==Z,'nonzero physical fixed space control')
 expected_return=monomial(lambda a,b,c,d:((d,1-c,a,b),0))
 need(B==expected_return,'actual return monomial, including its phase')
 words={'A':A,'A2':A2,'A3':A3,'A_h_A':clean(A*h*A),'A_h_A2':clean(A*h*A2),'m':m,'q':q}
 classes={n:rankclass(M)for n,M in words.items()}
 need(classes=={'A':1,'A2':2,'A3':3,'A_h_A':1,'A_h_A2':2,'m':3,'q':2},'independent source classes')

 e=atom(E);a=atom(A);a2=atom(A2);a3=atom(A3);ss=atom(s);hh=atom(h);bb=atom(B);empty={}
 ps=scale(add(e,ss),F(1,2));ns=scale(add(e,scale(ss,-1)),F(1,2));ph=scale(add(e,hh),F(1,2));nh=scale(add(e,scale(hh,-1)),F(1,2))
 C=[[ph,scale(nh,-1),empty],[mul(ps,nh),mul(ps,ph),scale(ns,-1)],[mul(ns,nh),mul(ns,ph),ps]]
 L=[[a,empty,empty],[e,a,empty],[empty,empty,e]];U=[[a,scale(a2,-1),empty],[empty,a,empty],[empty,empty,e]]
 K=matrixmul(matrixmul(L,C),U)
 aha=atom(words['A_h_A']);aha2=atom(words['A_h_A2'])
 need(K[0]==[scale(add(a2,aha),F(1,2)),scale(add(scale(a2,-1),aha,scale(a3,-1),scale(aha2,-1)),F(1,2)),empty],'complete first row of L C U')
 expected0=[[empty,empty,empty],[scale(bb,F(1,4)),scale(bb,F(1,4)),empty],[empty,empty,ps]]
 need([[proj(x,0)for x in row]for row in K]==expected0,'complete class0 coefficient matrix')
 need([proj(x,3)for x in K[0]]==[empty,scale(a3,F(-1,2)),empty],'isolated class3 term')
 need([proj(x,2)for x in K[0]]==[scale(a2,F(1,2)),scale(add(a2,aha2),F(-1,2)),empty],'complete class2 row')
 need(proj(add(scale(K[2][0],-1),K[2][1]),1)==mul(mul(ns,hh),a),'class1 after p=-z')
 need(mul(atom(clean(dagger(A2))),aha2)==atom(m),'correct multiplication order for m')
 need(mul(atom(clean(dagger(A)*h)),mul(mul(ns,hh),a))==scale(add(e,scale(atom(q),-1)),F(1,2)),'correct noncommuting q reduction')

 # Build an actual ONE-WIDTH ordinary expansion of (I+q)/2 in all four-bit
 # Hermitian Pauli monomials. The same fixed catalogue does not solve the
 # collective equation at larger widths. This is an explicit negative control
 # against treating (I-q) as physically injective.
 expansion=[];rebuild=sp.zeros(D)
 for u,v in product(range(16),repeat=2):
  P=sp.zeros(D);phase=I**((u&v).bit_count()%4)
  for j in range(D):P[j^u,j]=phase*((-1)**((v&j).bit_count()))
  P=sp.ImmutableMatrix(P);coeff=sp.cancel(sp.trace(dagger(P)*plus)/D)
  if coeff:
   need(sp.im(coeff)==0,'Hermitian Pauli coefficients real');expansion.append((P,coeff));rebuild+=coeff*P
 need(clean(rebuild)==plus,'one-width ordinary Pauli expansion of fixed-space projector')
 signed=[(P,c)for P,c in expansion]+[(clean(q*P),-c)for P,c in expansion]
 def gram_norm(W):
  val=0
  for X,c in signed:
   for Y,d in signed:val+=sp.conjugate(c)*d*(sp.trace(dagger(X)*Y)/D)**W
  return sp.cancel(val)
 norm1,norm4=gram_norm(1),gram_norm(4)
 need(norm1==0 and norm4>0,'one-width kernel equation fails for the same collective catalogue at width4')
 # Projective class disjointness is true for ALL ordinary monomials G: if
 # qg=h then q=h g^-1 would be monomial, contradicting row_size(q)==4.
 # The finite example below provides a concrete asymptotic Gram separation
 # receipt without claiming that this particular catalogue is the only one.
 allops=[P for P,c in signed];unique={key(P):P for P in allops};ks=list(unique)
 mu2=F(0)
 for i,x in enumerate(ks):
  for y in ks[:i]:
   z=sp.trace(dagger(MATS[x])*MATS[y])/D;mu2=max(mu2,sp.cancel(z*sp.conjugate(z)))
 need(mu2<1,'projectively distinct unitary Gram off-diagonal modulus below1')
 W=4
 while(len(ks)-1)**2*mu2**W>=1:W+=4
 need((len(ks)-1)**2*mu2**W<1,'exact Gershgorin sufficient width')

 profiles=list(combinations_with_replacement(range(5),3));high=[x for x in profiles if sum(x)>6]
 for rs in high:
  if rs[0]>0:need(set(rs)!={1,2,3},'positive profile cannot contain every required distinct class')
  else:need(rs in [(0,3,4),(0,4,4)]and 1 not in rs and 2 not in rs,'zero-head exhaustive alternative')
 def power_interval(n):
  denominator=10**36;target=n**199*denominator**200;lo=0;hi=n*denominator+1
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**200<=target:lo=mid
   else:hi=mid
  need(lo**200<=target<hi**200,'outward integer root interval');return Fraction(lo,denominator),Fraction(hi,denominator)
 l=u=Fraction(0)
 for n,c in {1:3,7:6,8:3,23:-3}.items():
  a0,b0=power_interval(n);l+=c*(a0 if c>0 else b0);u+=c*(b0 if c>0 else a0)
 need(l>0,'strict full common-body deficit')
 # Explicit algebra controls independent of the author's assertions.
 need(add(K[0][1],scale(a3,F(1,2)))!=K[0][1],'cubic omission changes formal source')
 need(add(K[0][1],scale(aha2,F(1,2)))!=K[0][1],'clock2 omission changes formal source')
 need(rankclass(clean(A*s*A))==0!=rankclass(clean(A*h*A)),'phase deletion changes the clock class')
 result={'status':'PASS_INDEPENDENT_ALL_PROFILE_CMIX_GATE','sympy':sp.__version__,
  'author_pins':{f:hashlib.sha256((args.author/f).read_bytes()).hexdigest()for f in ['PROOF.md','check.py']},
  'one_column_source_classes':classes,'q_involution':True,'q_physical_plus_rank_at_width1':12,
  'literal_return_verified':True,'formal_coefficients_checked':['entire first output row','full ordinary-class matrix','class3 isolation','class2 matrix','class1 after p=-z','ordered m and q reductions'],
  'positive_profile_required':[1,2,3],'zero_head_high_profiles_excluded':[[0,3,4],[0,4,4]],
  'total_head_upper_bound':6,'complete_price':'3[1]+6[7]+3[8]','largest_concave_target':'3[23]',
  'price_deficit_t199_over200_interval':[str(l),str(u)],
  'physical_kernel_control':{'one_width_ordinary_Pauli_terms':len(expansion),'normalized_squared_norm_W1':str(norm1),'same_catalogue_normalized_squared_norm_W4':str(norm4)},
  'example_exact_Gram_control':{'projective_words':len(ks),'maximum_overlap_squared':str(mu2),'sufficient_width_multiple4':W},
  'proof_scope':'Arbitrary fixed-prefix matrix coefficients and arbitrary fixed finite root-four collective-tail catalogues, including W-dependent coefficients; uniform endpoints at arbitrarily large W multiples4. Finite physical kernels are retained; no finite-width injectivity assumed. Changed first interfaces and growing catalogues/prefixes are excluded from the theorem.'}
 (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 (args.out/'SOURCE-MATRICES.json').write_text(json.dumps({n:dump(M)for n,M in {'A':A,'s':s,'h':h,'return':B,'m':m,'q':q}.items()},indent=2)+'\n')
 print(result['status'],classes,'physical control',norm1,norm4,'head<=6','deficit',float(l),flush=True)
if __name__=='__main__':main()
