#!/usr/bin/env python3
"""Independent support-filtration and all-clean first-column review controls."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser()
for n in ['repo','proof','out']:p.add_argument('--'+n,type=Path,required=True)
o=p.parse_args()
def add(*ds):
 out={}
 for d in ds:
  for k,v in d.items():out[k]=out.get(k,0)+v
 return{k:v for k,v in out.items()if v}
def mul(d,e):return add(*({k+l:v*w}for k,v in d.items()for l,w in e.items()))
def neg(d):return{k:-v for k,v in d.items()}
def w(*x):return{tuple(x):1}
def mm(A,B):return[[add(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
z={};a=w('a');one=w();L=[[a,z,z],[one,a,z],[z,z,one]];U=[[a,neg(w('a','a')),z],[z,a,z],[z,z,one]]
C=[[w('s'),w('b'),z],[w('t'),w('d'),w('e')],[w('u'),w('f'),z]];Q=[[w('q00'),w('q01'),z],[w('q10'),w('q11'),z],[w('q20'),w('q21'),w('q22')]]
E=mm(mm(mm(mm(L,C),U),Q),L)
def clean(d):
 out={}
 for key,v in d.items():
  key=list(key)
  for j in range(len(key)-1):
   if key[j]=='a'and key[j+1]in ['s','t','u']:key[j],key[j+1]=key[j+1]+'hat','a'
  out[tuple(key)]=v
 return out
degree4=lambda d:{k:v for k,v in d.items()if k.count('a')==4}
for j in [0,1]:
 assert degree4(clean(mul(a,E[2][j])))==neg(w('uhat','a','a','a',f'q1{j}','a'))
 assert degree4(clean(E[0][j]))==neg(w('shat','a','a','a',f'q1{j}','a'))
assert degree4(clean(mul(a,E[2][2])))=={}
# Literal source and an actual singular clean idle-first block.
I=s.eye(16);R=s.zeros(16);X=s.zeros(16);D=s.eye(16)
for j in range(16):
 aa,bb,cc,dd=[(j>>k)&1 for k in range(4)];R[(j>>1)|((j&1)<<3),j]=1;X[j^2,j]=1;D[j,j]=(-1)**(aa*cc*dd)
tidy=lambda M:M.applyfunc(s.expand);A=tidy(((1+s.I)*I+(1-s.I)*X)*D*R/2);Db=s.diag(*[s.I**((j>>1)&1)for j in range(16)]);Da=s.diag(*[s.I**(j&1)for j in range(16)])
u=(I-Db*Db)/2;uhat=tidy(A*u*A.adjoint());assert uhat==(I-Da*Da)/2 and u.rank()==uhat.rank()==8
# A rank2 Gaussian word has four entries per column; left A cannot create
# more than eight. Concrete normal forms verify the boundary, not universality.
G=tidy(A*A);support=lambda M:sorted({sum(z!=0 for z in row)for row in M.tolist()});assert support(G)==[4]
support_controls=[]
for T in [I,Db,Da,R,D,X]:
 v=tidy(A*T*G);supp=support(v);assert max(supp)<=8;support_controls.append(supp)
deps=['results/complex-first-interface-gates/ADMISSION.md','results/complex-source-square-controls/ADMISSION.md'];P=o.repo/'research/moonshot-005-program'
result={'status':'PASS_ROOT_ALL_CLEAN_FIRST_COLUMN_GATE_REVIEW','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'formal_left_multiplication_rank4_equations':True,'same_surjective_X_in_top_and_left_multiplied_bottom':True,'actual_singular_clean_idle_block_rank':8,'rank2_source_support':[4],'left_multiplication_support_controls':support_controls,'source_pins':{n:hashlib.sha256((P/n).read_bytes()).hexdigest()for n in deps},'scope':'Universal filtration/direct-image/surjectivity proof separately reviewed. No B execution code imported. Ordinary Q unrestricted; no all-width conclusion from these controls alone. No caller, supplier, foundation discharge or kappa.'}
o.out.parent.mkdir(parents=True,exist_ok=True);o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
