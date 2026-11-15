#!/usr/bin/env python3
"""Independent free-polynomial and directed-integer invoice check."""
import json
from pathlib import Path
import sympy as s

def K(a):return s.Matrix([[1,0,a-1],[a,0,-a],[1,1,-1]])
def same(A,B):return all(s.expand(x-y)==0 for x,y in zip(A,B))
def iroot(N,k):
 x=1<<((N.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+N//pow(x,k-1))//k
  if y>=x:break
  x=y
 while pow(x,k)>N:x-=1
 while pow(x+1,k)<=N:x+=1
 assert pow(x,k)<=N<pow(x+1,k)
 return x

def main():
 x,y,z,a=s.symbols('x y z a',commutative=False)
 expected=s.Matrix([[-x+y+z*x,y-z,x-y],[-z*x+z*y,z*y,z*x-z*y],[-x+y,0,x-y+y*x]])
 assert same(K(z)*K(y)*K(x),expected);assert same(K(a)**3,s.diag(a*a,a*a,a*a))
 T=s.Matrix([[0,0,1],[1,0,-1],[1,1,-1]]);J=s.Matrix([[0,1,0],[1,0,0],[0,0,1]]);T0=J*T*J
 assert T0==s.Matrix([[0,1,-1],[0,0,1],[1,1,-1]]) and T0.det()==1
 A=s.eye(3);A[1,2]=-1;B=s.eye(3);B[0,1]=1;C=s.Matrix([[0,1,0],[0,0,1],[1,0,0]])
 assert C*B*A==T0 and T0.inv()==s.Matrix([[-1,0,1],[1,1,0],[0,1,0]])
 # Opposite signs do not give this word; preserving field-level signs is necessary.
 wrong=s.Matrix([[0,1,1],[0,0,1],[1,1,1]]);assert wrong!=T0
 # The explicit one-interstage control contains rank3 but not independent(3,2,2).
 p=s.Matrix([[a*a,0,0],[0,a*a,0],[a*a*a,a*a,a*a]])
 assert same(p-s.Matrix([[0,0,0],[0,0,0],[a*a*a,0,0]]),a*a*s.Matrix([[1,0,0],[0,1,0],[0,1,1]]))
 scale=1<<160;roots={r:iroot(pow(r,199)*pow(scale,200),200)for r in (1,7,8,23,24)}
 def interval(target,paid):
  lo=sum(n*roots[r]for r,n in target.items())-sum(n*(roots[r]+1)for r,n in paid.items());hi=sum(n*(roots[r]+1)for r,n in target.items())-sum(n*roots[r]for r,n in paid.items())
  return {'lower_numerator':str(lo),'upper_numerator':str(hi),'denominator':str(scale),'sign':1 if lo>0 else -1 if hi<0 else 0}
 price={1:3,7:6,8:3};baseline=interval({23:3},price);upgrade=interval({23:2,24:1},price);paid=interval({23:2,24:1},{1:4,7:6,8:3});assert baseline['sign']==-1 and upgrade['sign']==1 and paid['sign']==-1
 out={'status':'PASS_ROOT_THREE_ROLE_POLYNOMIAL_AND_FULL_INVOICE','free_noncommutative_polynomial_identity':True,'actual_lower_orientation_and_inplace_T0':True,'price_histogram':price,'independent_inputs':3,'target_base_rank':23,'exponent':'199/200','base_margin':baseline,'unbuilt_upgrade_margin':upgrade,'paid_upgrade_margin':paid,'negative_controls':['Incorrect field-level sign rejected','Rank3 appearance alone retains rank2 component on3 independent inputs','Paying the rank1 upgrade destroys the positive movement screen'],'scope':'Universal identity from free-polynomial expansion; exact movement screen only; no target caller, supplier or foundational discharge','new_complete_kappa':False}
 (Path(__file__).parent/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
