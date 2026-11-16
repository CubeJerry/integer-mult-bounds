#!/usr/bin/env python3
from pathlib import Path
import argparse,itertools,json,hashlib
import sympy as s

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();tidy=lambda M:M.applyfunc(s.expand)
 c=s.Matrix([[1+s.I,1-s.I],[1-s.I,1+s.I]])/2;U=s.kronecker_product(c,c)
 table=[]
 for mask in range(16):
  vals=[(mask>>j)&1 for j in range(4)];D=s.diag(*[(-1)**v for v in vals]);H=tidy(U.conjugate().T*D*U)
  affine=vals[0]^vals[1]^vals[2]^vals[3]==0
  sizes=[sum(z!=0 for z in row)for row in H.tolist()]
  assert sizes==([1]*4 if affine else [4]*4)
  table.append({'mask':mask,'affine':affine,'row_support':sizes[0]})
 I=s.eye(16);P=s.zeros(16);D=s.eye(16);Xb=s.zeros(16)
 for j in range(16):P[(j>>1)|((j&1)<<3),j]=1;D[j,j]=-1 if(j&13)==13 else 1;Xb[j^2,j]=1
 A=tidy(((1+s.I)*I+(1-s.I)*Xb)*D*P/2);A2=tidy(A*A)
 # Literal R2=P²R4 table, including the retained phase.
 R=s.zeros(16)
 for x in range(16):
  aa,bb,cc,dd=[x>>j&1 for j in range(4)];y=(cc^(aa*bb))+2*dd+4*aa+8*bb;R[y,x]=s.I**(aa*bb*(1+2*cc+2*dd))
 examples=[]
 for controls in[(0,1,2),(9,6,10),(15,15,15),(3,12,5)]:
  g0,g1,g2=controls;fv=[];Mf=s.zeros(16)
  for z in range(16):
   aa,bb,cc,dd=[z>>j&1 for j in range(4)];j=cc+2*dd;ee=(g0>>j)&1;rr=(g1>>j)&1;ss=(g2>>j)&1
   fv.append(ee^(aa*rr)^(bb*ss));out=(aa^rr)+2*(bb^ss)+4*cc+8*dd;Mf[out,z]=(-1)**ee*s.I**(rr+ss+2*(rr*aa+ss*bb))
  Df=s.diag(*[(-1)**z for z in fv]);H=tidy(A2.conjugate().T*Df*A2);recipe=tidy(R.conjugate().T*Mf*R)
  assert H==recipe and tidy(H*H)==I and tidy(A2*H)==tidy(Df*A2)
  assert all(sum(H[i,j]!=0 for i in range(16))==1 for j in range(16))
  # Actual conditional bank swap has exact squareI on all three banks.
  pp=(I+H)/2;pm=(I-H)/2;Z=s.zeros(16);Q=s.Matrix.vstack(s.Matrix.hstack(pp,pm,Z),s.Matrix.hstack(pm,pp,Z),s.Matrix.hstack(Z,Z,I))
  assert tidy(Q*Q)==s.eye(48)
  examples.append({'controls':controls,'phase_table':[[i,j,str(H[i,j])]for j in range(16)for i in range(16)if H[i,j]!=0],'involution':True,'source_transport':True,'actual_bank_route_involution':True})
 # All16-bit Boolean tables: four disjoint fibre parity tests give the count.
 admitted=0
 for mask in range(65536):
  if all(not(sum((mask>>(aa+2*bb+4*cc+8*dd))&1 for aa,bb in itertools.product(range(2),repeat=2))%2)for cc,dd in itertools.product(range(2),repeat=2)):admitted+=1
 assert admitted==4096
 # Every conditional-Y core has exact inverse phases on all paired inputs.
 core_pairs=0
 for g0,g1,g2 in itertools.product(range(16),repeat=3):
  for z in range(16):
   aa,bb,cc,dd=[z>>j&1 for j in range(4)];j=cc+2*dd;ee=(g0>>j)&1;rr=(g1>>j)&1;ss=(g2>>j)&1
   phase1=2*ee+rr+ss+2*(rr*aa+ss*bb)
   phase2=2*ee+rr+ss+2*(rr*(aa^rr)+ss*(bb^ss))
   assert (phase1+phase2)%4==0;core_pairs+=1
 # Literal source-restoring conditional bank swap, checked over Q[z]/(z²-1).
 z=s.Symbol('z');schedule=[s.Matrix([[1,1],[0,1]]),s.diag(1,-2),s.Matrix([[1,0],[1,1]]),s.diag(1,z),s.Matrix([[1,1],[0,1]]),s.diag(s.Rational(1,2),1),s.diag(1,-1),s.Matrix([[1,0],[1,1]])]
 route=s.eye(2)
 for op in schedule:route=op*route
 expected=s.Matrix([[1+z,1-z],[1-z,1+z]])/2
 assert tidy(route)==expected and (tidy(route*route)-s.eye(2)).applyfunc(lambda x:s.rem(x,z*z-1,z))==s.zeros(2)
 bad=s.diag(*[(-1)**(((j&1)*((j>>1)&1)))for j in range(16)]);Hb=tidy(A2.conjugate().T*bad*A2)
 assert any(sum(z!=0 for z in row)>1 for row in Hb.tolist())
 prog=a.repo/'research/moonshot-005-program';deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-nondiagonal-cyclic/author/NONDIAGONAL-CYCLIC-IMPLEMENTATION.md']
 result={'status':'PASS_AUTHOR_SHARP_SQUARE_CONTROL_CLASSIFICATION_AND_ROUTES','scope':'Exact finite source/recipe checks support the universal Boolean-character proof; independent review pending. No complete endpoint or kappa.','fibre_cases':table,'all_boolean_tables':65536,'admitted_tables':admitted,'examples':examples,'negative_control_ab_not_monomial':True,'conditional_Y_inverse_phase_cases':core_pairs,'all_width_phase_rule':'i^(sum of actual input-indexed column exponents), never replace i^V by i or discard parity','conservative_monomial_recipe_per_direction':{'coordinate_SWAP':4,'X':2,'CNOT':4,'Toffoli':4,'phase_pass':3},'conditional_swap_recipe_per_direction':{'ADD':4,'SCALE':3,'H_f_monomial_service':1,'extra_whole_field_owner':0,'prefix_coordinate_norm_bound':32},'general_common_determinant_sector_recipe_per_direction':{'ADD':108,'SCALE':217,'H_f_monomial_service':108,'extra_whole_field_owner':0},'source_pins':{f:hashlib.sha256((prog/f).read_bytes()).hexdigest()for f in deps},'proof_sha256':hashlib.sha256(Path(__file__).with_name('SOURCE-SQUARE-CONTROLS.md').read_bytes()).hexdigest()}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in('status','all_boolean_tables','admitted_tables','negative_control_ab_not_monomial')},indent=2))
if __name__=='__main__':main()
