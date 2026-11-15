#!/usr/bin/env python3
"""Exact finite diagnostics; the general theorem is the accompanying written proof."""
import importlib.util,json,sys
from pathlib import Path
import sympy as S
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('inverse_gate_exact',here/'check.py')
b=importlib.util.module_from_spec(spec);sys.modules[spec.name]=b;spec.loader.exec_module(b)
I8=b.eye(8);Xb=b.monomial([j^2 for j in range(8)],[0]*8)
Cb=b.M((I8.scale((1,1))+Xb.scale((1,-1))).a,1).norm()
cycle=b.monomial([0,4,1,5,2,6,3,7],[0]*8);A=Cb@cycle
widths=[]
for v in (1,2):
 a=A.tp(v);ii=b.eye(a.n);zz=b.zero(a.n)
 n=b.block([[a,a.power(2).scale((-1,0))],[zz,a]])
 ni=b.block([[a.star(),ii],[zz,a.star()]])
 assert n@ni==b.eye(2*a.n) and ni@n==b.eye(2*a.n)
 wrong=b.block([[a.star(),ii.scale((-1,0))],[zz,a.star()]])
 assert n@wrong!=b.eye(2*a.n)
 widths.append({'V':v,'inverse_both_sides':True,'wrong_cross_sign_rejected':True})
z=S.symbols('z');I=S.eye(2);O=S.zeros(2);P=S.diag(1,0);Q=I-P
X=S.Matrix([[0,1],[1,0]]);J=S.Matrix([[1,1],[0,1]])
def block(a,b,c,d):return a.row_join(b).col_join(c.row_join(d))
C=block(P,Q,Q,P);D=block(I,J,O,I)
assert C.det()!=0 and D.det()!=0 and P.rank()==Q.rank()==1
L=block(z*I,I,O,z*I)
def query(i,j,T):
 m=S.eye(4);q=z*T-(I if i==j else O)
 for a in range(2):
  for c in range(2):m[2*i+a,2*j+c]+=q[a,c]
 return m

def coeff(m,k):return m.applyfunc(lambda x:S.expand(x).coeff(z,k))
def support(m):
 return [[i,j] for i in range(2) for j in range(2) if m[2*i:2*i+2,2*j:2*j+2]!=O]
checks=0
for i1,j1,i2,j2 in __import__('itertools').product(range(2),repeat=4):
 q1=query(i1,j1,X);q2=query(i2,j2,J)
 split=q2*C*L*D*q1
 assert all(x==[i2,j1] for x in support(coeff(split,3)))
 w=q1*D*L;after=q2*C*w
 assert all(x[0]==i1 for x in support(coeff(w,2)))
 assert all(x[0]==i2 for x in support(coeff(after,3)))
 before=L.T*D.T*q1.T*C.T*q2.T
 assert coeff(before,3)==coeff(after,3).T
 checks+=3
# Deliberately invalid controls show why each structural hypothesis is needed.
allbank=z*S.eye(4);base=z*S.eye(4)
assert coeff(allbank*base*allbank,3).rank()==4
shared=block(z**3*I,z**3*J,z**2*I,z**2*J)
assert coeff(shared,3).rank()==coeff(shared,2).rank()==2
assert shared.subs(z,2).rank()==2
rank2query=block(z*z*I,O,O,I);rank1query=block(I,O,O,z*I)
valid_out=rank2query*base*rank1query
assert valid_out==block(z**3*I,O,O,z**2*I)
out={'status':'PASS_EXACT_FINITE_DIAGNOSTICS','source_inverse':widths,'formal_noncommuting_ordinary_zero_divisors':True,'query_placement_coefficient_checks':checks,'negative_controls':{'two_bank_query_can_make_two_rank3_jobs':True,'shared_input_rank_components_do_not_make_two_independent_jobs':True,'rank2_query_invalidates_rank1_gate_and_allows_32_in_formal_model':True},'scope':'Exact finite diagnostics of source and filtration mechanisms; universal theorem is INVERSE-NATIVE-TWO-QUERY-GATE.md','new_kappa':False}
(here/'INVERSE-TWOQUERY-RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
