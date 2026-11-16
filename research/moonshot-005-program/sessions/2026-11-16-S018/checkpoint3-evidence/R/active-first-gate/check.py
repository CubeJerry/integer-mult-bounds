#!/usr/bin/env python3
"""Root formal-product and literal-source controls for stacked first-column gate."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser()
for n in ['repo','proof','out']:p.add_argument('--'+n,type=Path,required=True)
o=p.parse_args()
def plus(*xs):
 d={}
 for x in xs:
  for w,c in x.items():d[w]=d.get(w,0)+c
 return{k:c for k,c in d.items()if c}
def neg(x):return{w:-c for w,c in x.items()}
def mul(x,y):
 d={}
 for u,c in x.items():
  for v,e in y.items():d[u+v]=d.get(u+v,0)+c*e
 return{k:c for k,c in d.items()if c}
def mm(A,B):return[[plus(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
def atom(x):return{(x,):1}
def times(*xs):
 d={():1}
 for x in xs:d=mul(d,x)
 return d
I0={():1};Z={};a,w,v,g,h,k=map(atom,['a','w','v','g','h','k']);a2=times(a,a)
L=[[a,Z,Z],[I0,a,Z],[Z,Z,I0]];U=[[a,neg(a2),Z],[Z,a,Z],[Z,Z,I0]];C=[[w,v,Z],[g,h,Z],[Z,Z,k]]
Q=[[atom('q%d%d'%(i,j))for j in range(3)]for i in range(3)];P=mm(mm(L,C),U);E=mm(mm(P,Q),L)
expected=[[times(a,w,a),plus(times(a,v,a),neg(times(a,w,a2))),Z],[plus(times(w,a),times(a,g,a)),plus(times(v,a),times(a,h,a),neg(times(w,a2)),neg(times(a,g,a2))),Z],[Z,Z,k]]
assert P==expected
assert E[2]==[plus(times(k,Q[2][0],a),times(k,Q[2][1])),times(k,Q[2][1],a),times(k,Q[2][2])]
Qred=[[Q[0][0],Q[0][1],Q[0][2]],[Q[1][0],Q[1][1],Z],[Q[2][0],Z,Z]];Er=mm(mm(P,Qred),L)
assert [Er[i][2]for i in range(3)]==[times(a,w,a,Q[0][2]),times(plus(times(w,a),times(a,g,a)),Q[0][2]),Z]
Czero=[[Z,v,Z],[g,h,Z],[Z,Z,k]];Ez=mm(mm(mm(mm(L,Czero),U),Qred),L)
assert Ez[0][1]==times(a,v,a,Q[1][1],a)
assert [Ez[i][2]for i in range(3)]==[Z,times(a,g,a,Q[0][2]),Z]
# Literal root-four source, without importing either worker's checker.
Id=s.eye(16);perm=s.zeros(16);flip=s.zeros(16);phase=s.eye(16)
for x in range(16):
 aa,bb,cc,dd=[(x>>j)&1 for j in range(4)];perm[(x>>1)|((x&1)<<3),x]=1;flip[x^2,x]=1;phase[x,x]=(-1)**(aa*cc*dd)
tidy=lambda X:X.applyfunc(s.expand)
S=phase*perm;A=tidy(((1+s.I)*Id+(1-s.I)*flip)*S/2);A2=tidy(A*A);A3=tidy(A2*A)
Za=s.diag(*[(-1)**(x&1)for x in range(16)]);Zb=s.diag(*[(-1)**((x>>1)&1)for x in range(16)]);Db=s.diag(*[s.I**((x>>1)&1)for x in range(16)])
assert tidy(A*A.adjoint())==Id and tidy(A*Zb*A.adjoint())==Za
pp=(Id+Zb)/2;pm=(Id-Zb)/2;B=pp.row_join(pm).col_join(pm.row_join(pp));assert B*B==s.eye(32)
Tw=tidy(A*pp*A2);Tg=tidy(A*pm*A2);assert Tw==tidy((Id+Za)*A3/2)and Tg==tidy((Id-Za)*A3/2)
ranks=[Tw.rank(),Tg.rank(),Tw.col_join(Tg).rank()];assert ranks==[8,8,16]
# Deleting a complementary row block destroys the required full-column rank.
assert Tw.rank()<16 and Tg.rank()<16
clock=tidy(S.adjoint()*Db);bad=tidy(A*clock*A2);support=sorted(set(sum(x!=0 for x in row)for row in bad.tolist()));assert max(support)<=4
assert tidy(clock*clock.adjoint())==Id
# Both native operators use the same literal a; source-cube support is eight.
assert set(sum(x!=0 for x in row)for row in A3.tolist())=={8}
deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-middle-native-interface/author/PROOF.md','results/complex-source-square-controls/ADMISSION.md'];prog=o.repo/'research/moonshot-005-program'
r={'status':'PASS_ROOT_STACKED_FIRST_COLUMN_GATE_CONTROLS','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'formal_noncommutative_identities':['full_active_LCU','full_idle_output_row','last_column_after_q12_q21_q22_zero','zero_w_top_column1','zero_w_rank2_last_column'],'literal_source_cube_support':8,'nontriangular_complementary_projector_control':{'active_interface_involution':True,'individual_T_ranks':ranks[:2],'stack_rank':ranks[2],'both_individual_pivots_singular':True,'literal_forward_sign_transport':True,'all_width_stack_injectivity_identity':'diag(a,a)[w;g]a²; complementary actual projectors'},'negative_controls':{'either_pivot_alone_not_injective':True,'ordinary_clock_first_column_has_zero_rank3_component':True,'clock_word_row_supports':support,'clock_is_an_actual_unit':True,'not_a_positive_caller':True},'source_pins':{n:hashlib.sha256((prog/n).read_bytes()).hexdigest()for n in deps},'scope':'Universal fixed-template proof separately reviewed; finite controls do not establish faithful-width separation. Arbitrary ordinary second interface; idle-preserving first interface and injective forbidden-component stack required. No new supplier or kappa.'}
o.out.parent.mkdir(parents=True,exist_ok=True);o.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
