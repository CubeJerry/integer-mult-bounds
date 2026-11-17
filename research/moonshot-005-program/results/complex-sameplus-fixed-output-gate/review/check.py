#!/usr/bin/env python3
"""Free noncommutative source identity plus independent fixed-prefix kernel guard."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib,argparse
import sympy as sp

def need(x,s):
 if not x:raise ValueError(s)
def sym(name):return{(name,):F(1)}
def add(*xs):
 z={}
 for x in xs:
  for w,c in x.items():z[w]=z.get(w,F(0))+c
 return{w:c for w,c in z.items()if c}
def scale(x,c):return{w:c*v for w,v in x.items()if c*v}
def mul(*xs):
 z={():F(1)}
 for x in xs:z=add(*({w+v:c*d}for w,c in z.items()for v,d in x.items()))
 return z
def mm(A,B):return[[add(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
def clean(M):return sp.ImmutableSparseMatrix(M.applyfunc(sp.expand))
def tab(fn):
 entries={}
 for j in range(16):
  x=tuple((j>>k)&1 for k in range(4));out,p=fn(*x);entries[sum(b<<k for k,b in enumerate(out)),j]=sp.I**(p%4)
 return sp.ImmutableSparseMatrix(16,16,entries)
def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/workers/B/sameplus-fixed-output-gate'));p.add_argument('--out',type=Path,default=Path(__file__).with_name('output'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 pins={f:hashlib.sha256((a.author/f).read_bytes()).hexdigest()for f in ['PROOF.md','check.py']}
 need(pins=={'PROOF.md':'5d34d4e386aab40e82722a8b118ec67b5deda56cf38eb46d93f6caa7985080a5','check.py':'e202ab0a202d49aceba8981075962dcbf1a679d8fb5cde7f69c52db5780d285d'},'frozen gate files')
 one={():F(1)};zero={};aa=sym('a');ss=sym('S');gg=sym('g');hh=sym('h');a2=mul(aa,aa)
 pp=scale(add(one,ss),F(1,2));nn=scale(add(one,scale(ss,-1)),F(1,2))
 C=[[pp,zero,scale(nn,-1)],[pp,one,scale(nn,-1)],[nn,zero,pp]]
 repair=[[one,zero,gg],[zero,one,hh],[zero,zero,one]]
 L=[[aa,zero,zero],[one,aa,zero],[zero,zero,one]];U=[[aa,scale(a2,-1),zero],[zero,aa,zero],[zero,zero,one]]
 # O^-1=E21(+I)E10(-I), represented directly; g,h remain opaque free symbols.
 Oinv=[[one,zero,zero],[scale(one,-1),one,zero],[scale(one,-1),one,one]]
 actual=mm(mm(mm(mm(Oinv,L),C),repair),U)
 expected=[[mul(aa,pp,aa),scale(mul(aa,pp,a2),-1),mul(aa,add(mul(pp,gg),scale(nn,-1)))],
           [mul(pp,aa),mul(nn,a2),add(mul(pp,gg),scale(nn,-1),mul(aa,hh))],
           [aa,zero,add(ss,gg,mul(aa,hh))]]
 need(actual==expected,'universal equation3 in free associative algebra')
 # Noncommuting matrix order matters: replacing Pg by gP fails the free identity.
 wrong=[[dict(x)for x in row]for row in expected];wrong[0][2]=mul(aa,add(mul(gg,pp),scale(nn,-1)))
 need(actual!=wrong,'illegal commutation is rejected')
 no_h=[[dict(x)for x in row]for row in expected];no_h[2][2]=add(ss,gg)
 need(actual!=no_h,'omitted h repair term is rejected')
 # The source repair preserves every whole column with zero third component
 # at its input, and is an actual nilpotent shear unit for arbitrary g,h.
 inverse=[[one,zero,scale(gg,-1)],[zero,one,scale(hh,-1)],[zero,zero,one]]
 identity=[[one if i==j else zero for j in range(3)]for i in range(3)]
 need(mm(repair,inverse)==mm(inverse,repair)==identity,'universal repair unit/inverse')
 need(mm(repair,[[sym('p')],[sym('z')],[zero]])==[[sym('p')],[sym('z')],[zero]],'retained whole input column preserved')

 E=sp.ImmutableSparseMatrix(sp.eye(16));R=tab(lambda aa,b,c,d:((b,c,d,aa),2*aa*b*d));Xb=tab(lambda aa,b,c,d:((aa,b^1,c,d),0));A=clean(((1+sp.I)*E+(1-sp.I)*Xb)*R/2)
 swapab=tab(lambda aa,b,c,d:((b,aa,c,d),0));swapcd=tab(lambda aa,b,c,d:((aa,b,d,c),0));q=clean(A.conjugate().T*swapab*A)
 need({sum(bool(z)for z in clean(A.conjugate().T)[i,:])for i in range(16)}=={2},'inverse head class1')
 need({sum(bool(z)for z in clean((A.conjugate().T)**2)[i,:])for i in range(16)}=={4},'inverse square class2')
 need(clean(q*q)==E and clean(q.conjugate().T)==q,'exact nonmonomial involution')
 need({sum(bool(q[i,j])for j in range(16))for i in range(16)}=={4},'four nonzero entries per row')
 need(clean((A.conjugate().T)**3*swapcd*A**3)==q,'third conjugate really q')
 Zsig=sp.ImmutableSparseMatrix([[1,0],[0,-1]]);E2=sp.ImmutableSparseMatrix(sp.eye(2));P3=clean((sp.eye(32)+sp.kronecker_product(Zsig,q))/2)
 need(clean(P3*P3)==P3 and sp.trace(P3)==16,'actual physical half-bank projector')
 need(clean((sp.eye(32)-sp.kronecker_product(Zsig,q))*P3)==sp.zeros(32),'physical injectivity claim would be false')
 # A physically ordinary one-width expansion of P3, with fixed prefix matrices.
 recipe=[]
 for u,v in product(range(16),repeat=2):
  data={};phase=sp.I**((u&v).bit_count()%4)
  for j in range(16):data[j^u,j]=phase*((-1)**((v&j).bit_count()))
  G=sp.ImmutableSparseMatrix(16,16,data);c=sp.cancel(sp.trace(G.conjugate().T*q)/16)
  if c:recipe.append((G,clean(c*Zsig/2)))
 recipe.append((E,clean(E2/2)))
 reconstruct=clean(sum((sp.kronecker_product(B,G)for G,B in recipe),sp.zeros(32)))
 need(reconstruct==P3,'one-width ordinary expansion with arbitrary fixed prefix coefficients')
 terms=recipe+[(clean(q*G),clean(-Zsig*B))for G,B in recipe]
 def normsq(W):
  z=0
  for G,B in terms:
   for H,C0 in terms:z+=sp.trace(B.conjugate().T*C0)/2*(sp.trace(G.conjugate().T*H)/16)**W
  return sp.cancel(z)
 n1,n4=normsq(1),normsq(4);need(n1==0 and n4>0,'same fixed ordinary catalogue ceases to solve the physical projector at width4')
 result={'status':'PASS_INDEPENDENT_SAMEPLUS_FIXED_OUTPUT_GATE','author_pins':pins,
  'free_noncommutative_equation3':True,'free_symbols':['a','S','g','h'],'no_g_h_invertibility_or_commutation_used':True,
  'universal_shear_repair_inverse':True,'positive_column_preserved':True,'q_nonmonomial_row_support':4,
  'q_involution':True,'q_is_exact_third_source_conjugate':True,'P3_physical_rank':16,'physical_bank_dimension':32,
  'fixed_prefix_one_width_ordinary_kernel_control':{'recipe_terms_before_combining':len(recipe),'norm_squared_W1':str(n1),'norm_squared_W4':str(n4)},
  'universal_elimination_reviewed':['u=-hw','N2v=0','(Pg-N)w=0','P1hw=0','t=a^-1va ordinary','t=P3t implies t=0 by eventual coset separation','v=0 and w=Pw','Q column=(-h,0,I)^T w has rank at most half-bank'],
  'negative_controls':['swap Pg to gP changes exact source','delete ah term changes source','physical I-P3 injectivity is false','same one-width ordinary kernel does not extend collectively'],
  'scope':'Fixed O and literal heads a4,a2,a; arbitrary actual ordinary Q/input unit and source repair g,h in fixed finite collective-tail catalogue with arbitrary fixed-prefix matrices and W-dependent coefficients. Changed output complements remain open.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.out/'FREE-SOURCE-EQUATION.json').write_text(json.dumps([[{','.join(w):str(c)for w,c in sorted(x.items())}for x in row]for row in actual],indent=2)+'\n')
 print(result['status'],'free equation, physical prefix guard',n1,n4,flush=True)
if __name__=='__main__':main()
