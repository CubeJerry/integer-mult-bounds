#!/usr/bin/env python3
"""Independent symbolic necessity and actual8-column source controls."""
from pathlib import Path
import json,sympy as s
q=s.symbols('q0:9');t=s.symbols('t0:9');Q=s.Matrix(3,3,q);T=s.Matrix(3,3,t);K0=s.Matrix([[1,0,-1],[0,0,0],[1,1,-1]]);K1=s.Matrix([[0,0,1],[1,0,-1],[0,0,0]]);M=K0*Q*K0+K1*T*K1
# The full zero-ordinary equation, before assuming any block commutation.
solutions=s.linsolve(list(M),list(q)+list(t));sol=next(iter(solutions))
assert s.linear_eq_to_matrix(list(M),list(q)+list(t))[0].rank()==7
# Derive every required relation directly from the9 equations as linear rows.
polys=list(M);variables=list(q)+list(t)
def follows(expr):
 A=s.linear_eq_to_matrix(polys,variables)[0];v=s.linear_eq_to_matrix([expr],variables)[0]
 return A.col_join(v).rank()==A.rank()
for e in [q[2]-q[8],q[5],q[0]+q[3]-q[6],q[3]-t[7],t[6],t[1]-t[7],t[0]-t[6]]:assert follows(e)
# Given linearity of tau, these are q02=q22=c,q12=0,q00=r-s,
# s=tau(q),tau(r)=0,tau(u)=0,tau(s)=0. No tau inverse assumed.
r,u,c,d,ss,qq,a=s.symbols('r u c d ss qq a',commutative=False)
Qf=s.Matrix([[r-ss,qq+u,c],[ss,d,0],[r,qq,c]]);K=K0+a*K1
expected=s.Matrix([[a*r-ss,a*qq+u,a*c],[-a*ss,a*u,0],[0,d+u,0]])
assert all(s.expand(x)==0 for x in K*Qf-expected)
R1=s.eye(3);R1[0,2]=-1;R2=s.eye(3);R2[1,0]=1
assert R2*R1*Qf==s.Matrix([[-ss,u,0],[0,d+u,0],[r,qq,c]])
def perm(v):
 A=s.zeros(len(v))
 for j,i in enumerate(v):A[i,j]=1
 return A
I=s.eye(8);X=[perm([j^(1<<i)for j in range(8)])for i in range(3)];C=[((1+s.I)*I+(1-s.I)*x)/2 for x in X];S=perm([0,4,1,5,2,6,3,7]);A=C[1]*S;H=S.T;SS=X[1]*S
assert (A*H*A-SS).applyfunc(s.simplify)==s.zeros(8);assert s.simplify(A*SS*A-C[1]*C[2]*X[0])==s.zeros(8)
# Exact Gaussian support scales: each nonzero entry modulus^2 is 2^-rank.
for name,Z,rank in [('a',A,1),('a2',A*A,2),('asa',A*SS*A,2)]:
 nonzero=[s.simplify(x*s.conjugate(x))for x in Z.applyfunc(s.simplify) if x!=0];assert set(nonzero)=={s.Rational(1,2**rank)}
zero=s.zeros(8);KK=s.BlockMatrix([[I,zero,A-I],[A,zero,-A],[I,I,-I]]).as_explicit();QI=s.BlockMatrix([[I-SS,H+I,I],[SS,zero,zero],[I,H,I]]).as_explicit()
def add(dst,src,coeff):
 B=s.eye(24);B[8*dst:8*(dst+1),8*src:8*(src+1)]=coeff;return B
scale=s.diag(SS,I,I);swap=s.BlockMatrix([[zero,I,zero],[I,zero,zero],[zero,zero,I]]).as_explicit()
assert swap*add(1,0,-I)*add(1,2,I)*scale*add(2,1,H)*add(2,0,I)==QI
assert QI.det()!=0
out={'status':'PASS_ROOT_ZERO_ORDINARY_MIDDLE_REVIEW','necessity_relations':7,'all_noncommutative_block_identities':True,'actual_source_h_s_relations':True,'rank_components':[1,2,2],'explicit_QII_chronology':True,'scope':'Universal written ordinary-left-kernel proof reviewed separately; finite checks are controls, not extrapolation; no new kappa'};Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
