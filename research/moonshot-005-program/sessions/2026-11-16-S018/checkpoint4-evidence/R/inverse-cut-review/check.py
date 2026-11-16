#!/usr/bin/env python3
"""Independent ordered quotient, inverse-support and sharpness controls."""
import argparse, hashlib, json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser()
for key in ['repo','proof','out']: p.add_argument('--'+key,type=Path,required=True)
o=p.parse_args()
def add(*ds):
 out={}
 for d in ds:
  for k,v in d.items(): out[k]=out.get(k,0)+v
 return {k:v for k,v in out.items() if v}
def mul(d,e): return add(*({k+l:v*w} for k,v in d.items() for l,w in e.items()))
def neg(d): return {k:-v for k,v in d.items()}
def w(*letters): return {tuple(letters):1}
def mm(A,B): return [[add(*(mul(A[i][k],B[k][j]) for k in range(len(B)))) for j in range(len(B[0]))] for i in range(len(A))]
def norm(d):
 out={}
 for key,v in d.items():
  st=[]
  for x in key:
   if st and (st[-1],x) in [('a','ai'),('ai','a')]: st.pop()
   else: st.append(x)
  k=tuple(st);out[k]=out.get(k,0)+v
 return {k:v for k,v in out.items() if v}
def mn(A): return [[norm(z) for z in r] for r in A]
zero={};one=w();a=w('a');ai=w('ai')
L=[[a,zero],[one,a]];U=[[a,neg(w('a','a'))],[zero,a]]
Li=[[ai,zero],[neg(w('ai','ai')),ai]];Ui=[[ai,one],[zero,ai]]
I2=[[one,zero],[zero,one]]
assert mn(mm(L,Li))==mn(mm(Li,L))==I2
assert mn(mm(U,Ui))==mn(mm(Ui,U))==I2
Bi=[[w('v00'),w('v01')],[w('v10'),w('v11')]]
Qa=[[w('q00'),w('q01')],[w('q10'),w('q11')]]
Pinv=mm(mm(Ui,Bi),[[ai,zero],[zero,one]])
suffix=mm(Qa,L)
degree=lambda M,x:max(k.count(x) for row in M for d in row for k in d)
assert degree(Pinv,'ai')==2 and degree(suffix,'a')==1
L3=[[a,zero,zero],[one,a,zero],[zero,zero,one]]
U3=[[a,neg(w('a','a')),zero],[zero,a,zero],[zero,zero,one]]
C=[[w('s'),w('b'),zero],[w('t'),w('d'),w('e')],[w('u'),w('f'),zero]]
Q=[[w('q00'),w('q01'),zero],[w('q10'),w('q11'),zero],[w('q20'),w('q21'),w('q22')]]
E=mm(mm(mm(mm(L3,C),U3),Q),L3)
B=[[w('s'),w('b')],[w('u'),w('f')]]
M=mm(mm(mm(mm([[a,zero],[zero,one]],B),U),Qa),L)
assert [[E[i][j] for j in range(2)] for i in [0,2]]==M
assert E[0][2]==E[2][2]==zero
assert [C[i] for i in [0,2,1]]==[[w('s'),w('b'),zero],[w('u'),w('f'),zero],[w('t'),w('d'),w('e')]]
assert mm(mm(L,U),L)==[[zero,neg(w('a','a','a','a'))],[w('a','a'),zero]]
assert degree(mm(Ui,Li),'ai')==3
I=s.eye(16);R=s.zeros(16);X=s.zeros(16);D=s.eye(16)
for j in range(16):
 aa,bb,cc,dd=[(j>>k)&1 for k in range(4)]
 R[(j>>1)|((j&1)<<3),j]=1;X[j^2,j]=1;D[j,j]=(-1)**(aa*cc*dd)
tidy=lambda T:T.applyfunc(s.expand)
A=tidy(((1+s.I)*I+(1-s.I)*X)*D*R/2)
assert tidy(A*A.adjoint())==I
G=tidy(A**4)
support=lambda T:[sum(T[i,j]!=0 for i in range(16)) for j in range(16)]
assert support(A)==support(A.adjoint())==[2]*16 and support(G)==[16]*16
controls=[]
for k in range(8):
 H=s.zeros(16)
 for j in range(16): H[j^(k&3),j]=s.I**(((k>>2)+1)*(j&1)+2*((j>>2)&1))
 T=tidy(A.adjoint()*H*A.adjoint());TG=tidy(T*G)
 assert tidy(T.adjoint()*TG)==G
 inv_support=max(support(T.adjoint()));out_support=min(support(TG))
 assert inv_support<=4 and out_support>=4
 controls.append({'control':k,'inverse_max_support':inv_support,'product_min_support':out_support})
assert support(tidy(A.adjoint()**2*G))==[4]*16
assert support(tidy(A.adjoint()**3*G))==[2]*16
P=o.repo/'research/moonshot-005-program'
deps=['results/complex-inverse-native-coset/two-native/PROOF.md','results/complex-four-bit-cubic-source/author/PROOF.md']
result={'status':'PASS_ROOT_INVERSE_SUPPORT_CUT_AND_CLEAN_FIRST_TWO_EXCLUSION','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'ordered_two_sided_native_inverses':True,'formal_top_bottom_quotient':True,'ordinary_B_inverse_available_from_permuted_C_inverse':True,'prefix_inverse_degree':2,'suffix_degree':1,'maximum_independent_Gaussian_rank':3,'sharp_original_LUL_rank4':True,'sharp_original_prefix_inverse_degree':3,'literal_support_controls':controls,'negative_scope_control':'Allowing a third inverse rank1 factor reduces A^-3 A^4 to support2, so the claimed F2/F1 separation cannot be applied to the original LUL.','source_pins':{k:hashlib.sha256((P/k).read_bytes()).hexdigest() for k in deps},'review_scope':'Universal finite-catalogue tensor-separation proof independently read. Fixed finite ordinary recipes and faithful width threshold retained. Controls are not the all-width proof. No author execution code imported, no full arbitrary-three-native exclusion and no new kappa.'}
o.out.parent.mkdir(parents=True,exist_ok=True);o.out.write_text(json.dumps(result,indent=2)+'\n')
print(result['status'])
