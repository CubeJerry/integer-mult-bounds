#!/usr/bin/env python3
"""Separate root-gate review using B's formal ring and a direct input-indexed source."""
from pathlib import Path
import argparse,json,hashlib
import sympy as s
from check_triangular_first_interstage import add,mul,neg,atom,mm

def main():
 p=argparse.ArgumentParser();p.add_argument('--root-package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);o=p.parse_args()
 one,zero={():1},{};a,w,v,g,h,k=map(atom,('a','w','v','g','h','k'));a2=mul(a,a)
 L=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U=[[a,neg(a2),zero],[zero,a,zero],[zero,zero,one]];C=[[w,v,zero],[g,h,zero],[zero,zero,k]];Q=[[atom(f'q{i}{j}')for j in range(3)]for i in range(3)]
 E=mm(mm(mm(mm(L,C),U),Q),L)
 degree3=[{word:coef for word,coef in E[r][2].items()if word.count('a')==3}for r in range(3)]
 assert degree3==[neg(mul(mul(mul(a,w),a2),Q[1][2])),neg(mul(mul(mul(a,g),a2),Q[1][2])),zero]
 assert E[2]==[add(mul(mul(k,Q[2][0]),a),mul(k,Q[2][1])),mul(mul(k,Q[2][1]),a),mul(k,Q[2][2])]
 Qz=[[Q[0][0],Q[0][1],Q[0][2]],[Q[1][0],Q[1][1],zero],[Q[2][0],zero,zero]];Cz=[[zero,v,zero],[g,h,zero],[zero,zero,k]];Ez=mm(mm(mm(mm(L,Cz),U),Qz),L)
 assert Ez[0][1]==mul(mul(mul(mul(a,v),a),Q[1][1]),a)
 assert [Ez[r][2]for r in range(3)]==[zero,mul(mul(mul(a,g),a),Q[0][2]),zero]
 # Each source column is built from input phase(-1)^(a b d), independently
 # of root's output-phase-times-permutation construction.
 I=s.eye(16);A=s.zeros(16);S=s.zeros(16)
 for x in range(16):
  sign=-1 if(x&11)==11 else 1;y=(x>>1)|((x&1)<<3);A[y,x]=sign*(1+s.I)/2;A[y^2,x]=sign*(1-s.I)/2;S[y,x]=sign
 tidy=lambda M:M.applyfunc(s.expand);A2=tidy(A*A);A3=tidy(A2*A);Zb=s.diag(*[(-1)**((x>>1)&1)for x in range(16)]);Za=s.diag(*[(-1)**(x&1)for x in range(16)]);Db=s.diag(*[s.I**((x>>1)&1)for x in range(16)])
 P=(I+Zb)/2;M=(I-Zb)/2;assert P*P==P and M*M==M and P*M==s.zeros(16)and s.trace(P)==s.trace(M)==8
 Tw=tidy(A*P*A2);Tg=tidy(A*M*A2)
 assert tidy(Tw.conjugate().T*Tw+Tg.conjugate().T*Tg)==I
 assert tidy(A*Zb)==tidy(Za*A)
 assert Tw==tidy((I+Za)*A3/2)and Tg==tidy((I-Za)*A3/2)
 B=s.Matrix.vstack(s.Matrix.hstack(P,M),s.Matrix.hstack(M,P));assert B*B==s.eye(32)
 clock=S.conjugate().T*Db;bad=tidy(A*clock*A2);support=sorted({sum(z!=0 for z in row)for row in bad.tolist()});assert support==[4]and tidy(clock*clock.conjugate().T)==I
 proof=o.root_package/'PROOF.md';result={'status':'PASS_B_INDEPENDENT_STACKED_ACTIVE_FIRST_GATE_REVIEW','root_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'formal_checks':['whole_last_column_degree3_is_negative_stack_times_q12','full_idle_output_row','zero_w_unit_top_column1','zero_w_pure2_last_column_shape'],'source_checks':{'direct_input_phase_source':True,'individual_projector_traces':[8,8],'stack_Gram_equals_identity':True,'stack_injective':True,'both_individual_pivots_singular':True,'literal_forward_phase_transport':True,'conditional_swap_involution':True,'failed_hypothesis_unit_clock_support':support},'scope':'Independent proof review and separate exact source/formal controls. Universal faithful-width argument is mathematical; no finite search conclusion and no supplier/kappa.'}
 o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['root_proof_sha256'])
if __name__=='__main__':main()
