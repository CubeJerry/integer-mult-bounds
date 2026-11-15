#!/usr/bin/env python3
"""Literal sources, phases, symplectic ranks and tensor controls, independently."""
import argparse,hashlib,json
from pathlib import Path
from exact import *
def table(A):
 p=[];q=[]
 for j in range(A.n):
  hits=[(i,v)for(i,k),v in A.x.items()if k==j];assert len(hits)==1;i,v=hits[0];p.append(i);q.append(next(t for t in range(4)if v==phasepower(t)))
 return {'permutation':p,'phase_mod4':q}
def symplectic(A):return [sum(1<<k for k in [])^ (lambda z:z[0]|(z[1]<<3))(pauli_image(A,x,z))for x,z in [(1<<i,0)for i in range(3)]+[(0,1<<i)for i in range(3)]]
def compose(a,b):return [xor(a[i]for i in range(6)if v>>i&1)for v in b]
def xor(xs):
 z=0
 for x in xs:z^=x
 return z

def check_source(A,G1,G2,H2,Ca,Cb,order,pattern,trace_expected):
 E=ident(8);powers=A.powers(order);assert powers[order]==E and A.adj()*A==E
 assert [B.row_support()for B in powers[:-1]]==[[2**r]*8 for r in pattern]
 symrank=[mixing_rank(B)[0]for B in powers[:-1]];assert symrank==pattern
 assert [B.trace()for B in powers[:-1]]==[(F(x),F(0))for x in trace_expected]
 assert Cb*G1==A and H2*G1==E and H2*Ca*G2==A and Ca*Cb*G2==A*A
 widths=[]
 for V in [1,2]:
  def lift(B):return B if V==1 else B.tensor(B)
  ca,cb,g1,g2,h2,a=map(lift,[Ca,Cb,G1,G2,H2,A]);e=ident(8**V)
  coeff={'X_X':cb*g1,'Y_X':h2*g1,'Y_Y':h2*ca*g2,'U_U':cb*g1,'U_V':-(ca*cb*g2),'V_V':h2*ca*g2}
  assert coeff=={'X_X':a,'Y_X':e,'Y_Y':a,'U_U':a,'U_V':-(a*a),'V_V':a}
  widths.append({'V':V,'head_dimension':8**V,'all_four_independent_role_input_columns_verified':True,'all_six_nonzero_coefficient_blocks_verified':True})
 a2=A.tensor(A);cyclic=M(64,{})
 for B in a2.powers(order-1):cyclic=cyclic+B
 assert cyclic*cyclic==cyclic.scale((F(order),F(0))) and cyclic.trace()==(F(8*order),F(0))
 s=symplectic(A);r=[1<<i for i in range(6)];so=None
 for k in range(1,order+1):
  r=compose(s,r)
  if r==[1<<i for i in range(6)]:so=k;break
 assert so==order
 return {'order':order,'Gaussian_power_ranks_via_independent_Pauli_mixing_block':symrank,'power_traces':trace_expected,'actual_symplectic_columns':s,'actual_symplectic_order':so,'boundary_tables':{n:table(B)for n,B in [('pre_first',G1),('pre_second',G2),('post_second',H2)]},'widths':widths,'width2_cyclic_projector_rank':8}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 for f in ['DEPENDENCIES.json','LOCAL-WREATH-DEPENDENCIES.json']:
  for d in json.loads((a.source/f).read_text())['sources']:assert hashlib.sha256((a.repo/d['path']).read_bytes()).hexdigest()==d['sha256']
 E=ident(8);P=permutation([0,4,1,5,2,6,3,7]);D=phase(1);Ca=E.scale((F(1,2),F(1,2)))+X(0).scale((F(1,2),-F(1,2)));Cb=E.scale((F(1,2),F(1,2)))+X(1).scale((F(1,2),-F(1,2)));S=D*P;L=(Cb*D).scale(I);B=(Cb*S).scale(I)
 assert L*L+L+E==M(8,{})and L*L*L==E
 out={'status':'PASS_INDEPENDENT_ORDER9_AND_ENTANGLING_ORDER15','arithmetic':'Separate sparse Gaussian-rational matrices and actual Pauli conjugation; no author implementation imported.','pins':{n:hashlib.sha256((a.source/n).read_bytes()).hexdigest()for n in ['PROOF.md','ENTANGLING-ORDER-FIFTEEN-SOURCE.md','LOCAL-WREATH-CONSERVATION.md','LOCAL-WREATH-SCOPE.md']}}
 out['order9']=check_source(B,S.scale(I),-(S*S),S.adj().scale(neg(I)),Ca,Cb,9,[0,1,2,3,3,3,3,2,1],[8]+[-1]*8)
 bp=B.powers(9);assert bp[5]*D*bp[3]==S.adj().scale(neg(I));assert S*Cb*S.adj()==Ca
 assert xor([])==0
 total=M(8,{})
 for q in bp[:9]:total=total+q
 assert total==M(8,{})
 # Phase/sign controls: the wrong lifted G2 sign and tensoring the upper
 # field-level minus fail on all-column coefficient matrices at V2.
 assert Cb*S!=B
 assert S.adj().scale(neg(I)).tensor(S.adj().scale(neg(I)))*Ca.tensor(Ca)*(-(S.tensor(S)*S.tensor(S)))!=B.tensor(B)
 assert (-(B*B)).tensor(-(B*B))!=-(B.tensor(B)*B.tensor(B))
 assert bp[5]*D.adj()*bp[3]!=S.adj().scale(neg(I))
 CZ=monomial(list(range(8)),[2*(x&1)*((x>>2)&1)for x in range(8)]);S15=D*CZ*P;A=Cb*S15;J=monomial([x^((x>>2)&1)for x in range(8)],[(x>>2)&1 for x in range(8)]);R=J*S15*S15
 assert R==Ca.adj()*S15*Cb*S15
 assert S15*X(1)*S15.adj()==X(0)*ZZ(2)
 traces=[8 if k==0 else -4 if k%5==0 else -2 if k%3==0 else 1 for k in range(15)]
 out['order15']=check_source(A,S15,R,S15.adj(),Ca,Cb,15,[0,1,2,3,3,2,3,3,3,3,2,3,3,2,1],traces)
 assert table(S15)=={'permutation':[0,4,1,5,2,6,3,7],'phase_mod4':[0,0,0,2,1,1,1,3]}
 assert table(R)=={'permutation':[0,2,5,7,1,3,4,6],'phase_mod4':[0,1,1,0,1,2,0,3]}
 assert table(S15.adj())=={'permutation':[0,2,4,6,1,3,5,7],'phase_mod4':[0,0,3,3,0,2,3,1]}
 assert R!=S15*S15 and Ca*Cb*S15*S15!=A*A
 coeff={8:1,7:-1,5:1,4:-1,3:1,1:-1,0:1};poly=M(8,{});poly2=M(64,{});ps=A.powers(8);ps2=A.tensor(A).powers(8)
 for k,c in coeff.items():poly=poly+ps[k].scale((F(c),F(0)));poly2=poly2+ps2[k].scale((F(c),F(0)))
 assert poly==M(8,{})and poly2!=M(64,{})
 assert 1296%5!=0
 assert all([min(k,15-k,ell)for k in range(15)]!=out['order15']['Gaussian_power_ranks_via_independent_Pauli_mixing_block']for ell in range(1,8))
 out['negative_controls']=['drop_i_from_order9_G1','width_independent_order9_G2_minus','put_field_cross_minus_inside_tensor','invert_D_in_order9_bridge','omit_order15_controlled_J','order15_width1_cyclotomic_relation_at_width2'];out['new_complete_kappa']=False
 (a.out/'SOURCE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
