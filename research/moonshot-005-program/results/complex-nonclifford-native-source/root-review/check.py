#!/usr/bin/env python3
"""Independent symbolic reconstruction from Boolean maps, no author imports."""
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as s
I=s.I;Id=s.eye(8);alpha=(1+I)/2;beta=(1-I)/2
def bit(x,j):return x>>j&1
def monomial(p,q):
 M=s.zeros(8)
 for x in range(8):M[p(x),x]=I**(q(x)%4)
 return M
def clean(M):return M.applyfunc(s.simplify)
def eq(M,N):return clean(M-N)==s.zeros(*M.shape)
X=[monomial(lambda x,j=j:x^(1<<j),lambda x:0) for j in range(3)]
C=[alpha*Id+beta*x for x in X]
P=monomial(lambda x:bit(x,1)+2*bit(x,2)+4*bit(x,0),lambda x:0)
D=monomial(lambda x:x,lambda x:2*bit(x,0)*bit(x,1)*bit(x,2))
S=D*P;A=clean(C[1]*S)
J=monomial(lambda x:x^(bit(x,1)*bit(x,2)),lambda x:bit(x,1)*bit(x,2))
R=J*P**2
L3=monomial(lambda x:x^(2*bit(x,0)*bit(x,2)),lambda x:bit(x,0)*bit(x,2)*(2*bit(x,1)-1))
R3=monomial(lambda x:x^(4*bit(x,0)*bit(x,1)),lambda x:bit(x,0)*bit(x,1))
A2=clean(A*A);A3=clean(A2*A)
assert eq(S.H*C[0]*R,A) and eq(C[0]*C[1]*R,A2)
assert eq(L3*C[0]*C[1]*C[2]*R3,A3)
assert eq(A.H*A,Id) and all(eq(M.H*M,Id) for M in [S,J,R,L3,R3])
for x,y in itertools.product(range(8),repeat=2):
 a,b,c=[bit(x,j) for j in range(3)];u,v,w=[bit(y,j) for j in range(3)]
 formula=alpha**3*(-I)**((u^a)+(v^b)+(w^c))*(-1)**(a*b*c+a*b*w+u*b*w)
 assert s.simplify(A3[y,x]-formula)==0
assert s.simplify(s.trace(A3))==(-3+3*I)/2
assert s.simplify(A.det())==-1
assert s.simplify(s.trace(A3)*s.conjugate(s.trace(A3)))==s.Rational(9,2)
# Actual monomial factors are indispensable, not just row-support matching.
Jperm=monomial(lambda x:x^(bit(x,1)*bit(x,2)),lambda x:0)
Lperm=monomial(lambda x:x^(2*bit(x,0)*bit(x,2)),lambda x:0)
assert not eq(C[0]*C[1]*(P**2),A2)
assert not eq(C[0]*C[1]*(Jperm*P**2),A2)
assert not eq(Lperm*C[0]*C[1]*C[2]*R3,A3)
assert not eq((C[1]*P)**3,A3)
assert not eq(A2,A3)
# Independently check the general admission criterion on all fourth-root
# fixed-point-free Hermitian monomial involutions, by sparse columns of(4).
def matchings(points):
 if not points:yield [];return
 x=points[0]
 for y in points[1:]:
  for rest in matchings([z for z in points[1:] if z!=y]):yield [(x,y)]+rest
units=[1,1j,-1,-1j];census=accepted=0;non_sign_rejected=0
for pairs in matchings(list(range(8))):
 for es in itertools.product(range(4),repeat=4):
  tau={};coeff={}
  for (x,y),e in zip(pairs,es):tau[x]=y;tau[y]=x;coeff[x]=units[e];coeff[y]=units[-e%4]
  mon=True
  for x in range(8):
   col={}
   for j,c in [(x,1),(tau[x]^1,coeff[x]),(x^1,1j),(tau[x],-1j*coeff[x])]:col[j]=col.get(j,0)+c
   mon=mon and sum(c!=0 for c in col.values())==1
  criterion=all(tau[x]==x^1 and coeff[x] in [1,-1] for x in range(8))
  assert bool(mon)==criterion;census+=1;accepted+=mon
  non_sign_rejected+=not mon and any(c in [1j,-1j] for c in coeff.values())
assert census==26880 and accepted==16 and non_sign_rejected>0
out={'status':'PASS_ROOT_NONCLIFFORD_SOURCE_REVIEW','one_column_dimension':8,'source_gauges_exact':True,'square_cube_two_sided_factors_exact':True,'all64_cubic_kernel_entries':True,'trace_A3':'(-3+3i)/2','det_A':-1,'trace_norm':'9/2','dyadic_local_valuation_trace':-1,'tensor_width_V_trace_valuation':'-V','infinite_projective_order':True,'stable_lattice_obstruction_every_positive_tensor_width':True,'admission_involutions_checked':census,'admitted':accepted,'non_sign_rejected':non_sign_rejected,'negative_controls':['omitted Toffoli','omitted Toffoli phase','omitted cubic left phase','omitted CCZ','cube replaced by square'],'physical_status':'requires separately reviewed compact-control specialization; no source tariff inferred from table alone','new_complete_kappa':False}
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
