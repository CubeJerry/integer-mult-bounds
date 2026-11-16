#!/usr/bin/env python3
"""Independent root formal product and noncommuting middle-pivot controls."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser()
for n in ['repo','proof','out']:p.add_argument('--'+n,type=Path,required=True)
o=p.parse_args()
def add(*xs):
 z={}
 for d in xs:
  for w,c in d.items():z[w]=z.get(w,0)+c
 return{k:c for k,c in z.items()if c}
def neg(x):return{k:-c for k,c in x.items()}
def mul(x,y):
 z={}
 for u,c in x.items():
  for v,d in y.items():z[u+v]=z.get(u+v,0)+c*d
 return{k:c for k,c in z.items()if c}
def mm(A,B):return[[add(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
def word(*w):return{tuple(w):1}
zero={};one=word();a=word('a');L=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U=[[a,neg(word('a','a')),zero],[zero,a,zero],[zero,zero,one]]
C=[[zero,word('b'),word('c')],[word('t'),word('d'),word('e')],[zero,word('f'),word('g')]];Q=[[word('q%d%d'%(i,j))for j in range(3)]for i in range(3)]
P=mm(mm(L,C),U);expected=[[zero,word('a','b','a'),word('a','c')],[word('a','t','a'),add(neg(word('a','t','a','a')),word('b','a'),word('a','d','a')),add(word('c'),word('a','e'))],[zero,word('f','a'),word('g')]];assert P==expected
E=mm(mm(P,Q),L);three=[{w:c for w,c in E[i][2].items()if w.count('a')==3}for i in range(3)];assert three==[zero,neg(word('a','t','a','a','q12')),zero]
Qr=[[Q[0][0],Q[0][1],Q[0][2]],[Q[1][0],Q[1][1],zero],[Q[2][0],Q[2][1],zero]];Er=mm(mm(P,Qr),L);assert[Er[i][2]for i in range(3)]==[zero,word('a','t','a','q02'),zero]
rowmax=[max((w.count('a')for d in row for w in d),default=0)for row in E];assert rowmax==[3,4,2]
# Independent literal source and a noncommuting actual first-interface control.
I=s.eye(16);R=s.zeros(16);Xb=s.zeros(16);Xa=s.zeros(16);D=s.eye(16)
for x in range(16):
 a0,b0,c0,d0=[(x>>j)&1 for j in range(4)];R[(x>>1)|((x&1)<<3),x]=1;Xb[x^2,x]=1;Xa[x^1,x]=1;D[x,x]=(-1)**(a0*c0*d0)
tidy=lambda X:X.applyfunc(s.expand);S=D*R;A=tidy(((1+s.I)*I+(1-s.I)*Xb)*S/2);Da=s.diag(*[s.I**(x&1)for x in range(16)]);Db=s.diag(*[s.I**((x>>1)&1)for x in range(16)])
assert tidy(A*Db*A.adjoint())==Da
pp=(I+Xa)/2;pm=(I-Xa)/2;bb=Da*pp;cc=Da*pm;ff=pm;gg=pp;tt=Db;dd=Xb;ee=Xa
r00=pp*Da.adjoint();r01=pm;r10=pm*Da.adjoint();r11=pp;Z=s.zeros(16)
B=Z.row_join(bb).row_join(cc).col_join(tt.row_join(dd).row_join(ee)).col_join(Z.row_join(ff).row_join(gg))
Bi=(-tt.adjoint()*(dd*r00+ee*r10)).row_join(tt.adjoint()).row_join(-tt.adjoint()*(dd*r01+ee*r11)).col_join(r00.row_join(Z).row_join(r01)).col_join(r10.row_join(Z).row_join(r11))
assert tidy(B*Bi)==tidy(Bi*B)==s.eye(48)
assert Da*pp!=pp*Da and tt*dd!=dd*tt
ranks=[cc.rank(),gg.rank(),cc.col_join(gg).rank()];assert ranks==[8,8,16]
AtA=tidy(A*Db*A);AtA2=tidy(A*Db*A*A);assert AtA==tidy(Da*A*A)and AtA2==tidy(Da*A*A*A)
assert set(sum(z!=0 for z in row)for row in AtA.tolist())=={4};assert set(sum(z!=0 for z in row)for row in AtA2.tolist())=={8}
# The material clean-forward premise is not automatic for ordinary t.
bad=tidy(S.adjoint()*Db);badj=tidy(A*bad*A.adjoint());bad_support=sorted(set(sum(z!=0 for z in row)for row in badj.tolist()));assert max(bad_support)>1
prog=o.repo/'research/moonshot-005-program';deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-middle-native-interface/author/PROOF.md']
r={'status':'PASS_ROOT_ALL_ORDINARY_MIDDLE_PIVOT_REVIEW','reviewed_proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'formal_LCU_and_last_column_verified':True,'unique_last_column_three_A_word':'-a t a² q12','maximum_A_factors_by_output_row':rowmax,'noncommuting_first_interface_control':{'two_sided_inverse_verified':True,'individual_c_g_ranks':ranks[:2],'stack_rank':ranks[2],'genuine_noncommutativity':True,'actual_clean_pivot':True,'rank2_rank3_word_supports':[4,8]},'failed_hypothesis_control':{'ordinary_t':True,'forward_conjugate_supports':bad_support,'not_a_positive_endpoint':True},'source_pins':{n:hashlib.sha256((prog/n).read_bytes()).hexdigest()for n in deps},'scope':'Universal proof independently reviewed in writing. Free noncommuting and literal controls import no B checker. Faithful-width hypothesis retained; no arbitrary isolated-width gate, supplier or new kappa.'}
o.out.parent.mkdir(parents=True,exist_ok=True);o.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
