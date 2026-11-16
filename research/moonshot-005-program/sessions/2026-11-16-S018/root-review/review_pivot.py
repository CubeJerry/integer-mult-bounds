#!/usr/bin/env python3
"""Independent S018 column-propagation and ordered-product review."""
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as S
def tidy(m):return m.applyfunc(S.expand)
def main():
 p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 I=S.eye(16);P=S.zeros(16);J=S.zeros(16);phase=S.eye(16)
 for j in range(16):
  P[(j>>1)|((j&1)<<3),j]=1;J[j^2,j]=1;phase[j,j]=(-1)**int((j&13)==13)
 C=((1+S.I)*I+(1-S.I)*J)/2;A=tidy(C*phase*P);A2=tidy(A*A);Da=S.diag(*[S.I**(j&1)for j in range(16)]);Db=S.diag(*[S.I**((j>>1)&1)for j in range(16)])
 assert tidy(A*Db)==tidy(Da*A)
 column_support=[]
 for j in range(16):
  js=[i for i in range(16)if A2[i,j]!=0];assert len(js)==4 and {(i&1,(i>>1)&1)for i in js}==set(itertools.product([0,1],repeat=2));column_support.append(js)
 residues={v:sorted({sum(bits)%4 for bits in itertools.product([0,1],repeat=v)})for v in range(1,8)}
 assert residues[1]==[0,1]and residues[2]==[0,1,2]and all(residues[v]==[0,1,2,3]for v in range(3,8))
 z,h=S.symbols('a h',commutative=False);rb=S.Matrix(3,3,lambda i,j:S.Symbol(f'rb{i}{j}',commutative=False));ra=S.Matrix(3,3,lambda i,j:S.Symbol(f'ra{i}{j}',commutative=False));q=S.Matrix(3,3,lambda i,j:S.Symbol(f'q{i}{j}',commutative=False));L=S.Matrix([[z,0,0],[1,z,0],[0,0,1]]);U=S.Matrix([[z,-z*z,0],[0,z,0],[0,0,1]])
 raw=tidy(L*rb*S.diag(1,h,1)*U*q*L)
 def transported(term):
  fs=[]
  for f in S.Mul.make_args(term):
   if f.is_Pow and f.base==z:fs.extend([z]*int(f.exp))
   else:fs.append(f)
  for k in range(len(fs)-1):
   if fs[k]==z and fs[k+1]in rb:
    j=list(rb).index(fs[k+1]);fs[k:k+2]=[list(ra)[j],z]
  return S.Mul(*fs)
 def part(e,degree):
  ts=[]
  for t in S.Add.make_args(S.expand(e)):
   if t.has(h):continue
   d=sum(int(f.exp)if f.is_Pow and f.base==z else int(f==z)for f in S.Mul.make_args(t))
   if d==degree:ts.append(transported(t))
  return S.expand(sum(ts))
 v=S.Matrix([ra[0,0],ra[1,0],0]);w=S.Matrix([0,rb[0,0],rb[2,0]])
 e0=v*(z*z*q[0,0]*z-z**3*q[1,1])-w*z*z*q[1,0]*z;e1=v*z*z*q[0,1]*z-w*z*z*q[1,1]*z
 for r in range(3):
  assert S.expand(part(raw[r,0],3)-e0[r])==0;assert S.expand(part(raw[r,1],3)-e1[r])==0
  for c in range(3):assert S.expand(part(raw[r,c],4)-(-v[r]*z**3*q[1,c]*z if c<2 else 0))==0
 H=tidy(A2.conjugate().T*Da**2*A2);Q=(I-H)/2;PP=(I+Da**2)/2
 assert tidy(H*H)==I and H!=S.diag(*list(H.diagonal()))and all(sum(H[i,j]!=0 for i in range(16))==1 for j in range(16));assert Q.rank()==8 and tidy(PP*A2*Q)==S.zeros(16)
 # Residual first column: check the full ordered pre-Q matrix, including
 # the c(y) term essential to the ordinary-component argument.
 first=L*rb*S.diag(1,h,1)*U
 actual=first.applyfunc(lambda e:S.expand(sum(transported(t)for t in S.Add.make_args(S.expand(e)))))
 residual={rb[0,0]:0,ra[0,0]:0,rb[2,0]:0,ra[2,0]:0}
 actual=tidy(actual.subs(residual))
 expected=S.Matrix([[0,ra[0,1]*z*h*z,ra[0,2]*z],[ra[1,0]*z*z,-ra[1,0]*z**3+rb[0,1]*h*z+ra[1,1]*z*h*z,rb[0,2]+ra[1,2]*z],[0,rb[2,1]*h*z,rb[2,2]]])
 assert tidy(actual-expected)==S.zeros(3)
 support_controls=[];SS=phase*P
 for theta in range(4):
  hh=tidy(SS.conjugate().T*Db**theta);HH=tidy(hh*A);vv=tidy(A*HH)
  assert all(sum(HH[i,j]!=0 for j in range(16))==2 for i in range(16))
  count_v=2 if theta%2 else 1
  assert all(sum(vv[i,j]!=0 for j in range(16))==count_v for i in range(16))
  for name,M,want in [('H d A',HH,4),('v d A',vv,2*count_v)]:
   paths=[[sum(M[i,k]!=0 and A[k,j]!=0 for k in range(16))for j in range(16)]for i in range(16)]
   assert all(n in [0,1]for row in paths for n in row)and all(sum(row)==want for row in paths)
   support_controls.append({'theta':theta,'word':name,'unique_paths':True,'support':want})
 out={'status':'PASS_ROOT_INDEPENDENT_COHERENT_DIAGONAL_EXCLUSION_REVIEW','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'method':'Independent exact16-address source and literal full noncommutative L R diag(1,h,1) U Q L product; no author module imported. Universal tensor-separation, propagation and odd/even residual rank arguments reviewed in writing.','all16_square_columns_have_independent_ab_bits':column_support,'reachable_weight_residues':residues,'ordered8_and16_component_formulas':True,'residual_pre_Q_full_formula':True,'odd_even_unique_path_support':support_controls,'non_diagonal_projector_control':{'rank':8,'annihilation':True,'ordinary_monomial_involution':True},'scope':'Every coherent quarter-controlled R with fixed stated clock placement and diagonal Q is excluded. Non-diagonal Q, different clock placement and unrestricted first interfaces remain open. No supplier or new kappa.'};a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
