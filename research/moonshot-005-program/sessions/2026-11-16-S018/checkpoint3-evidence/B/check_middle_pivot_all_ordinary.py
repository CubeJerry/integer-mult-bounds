#!/usr/bin/env python3
"""Exact formal prefix, arbitrary-block support degrees and source controls."""
from pathlib import Path
import argparse,json,hashlib
import sympy as s
from check_triangular_first_interstage import add,mul,neg,atom,mm

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();one,zero={():1},{}
 a,b,c,t,d,e,f,g=map(atom,('a','b','c','t','d','e','f','g'));a2=mul(a,a);L=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U=[[a,neg(a2),zero],[zero,a,zero],[zero,zero,one]];C=[[zero,b,c],[t,d,e],[zero,f,g]];Q=[[atom(f'q{i}{j}')for j in range(3)]for i in range(3)]
 def prod(*xs):
  z=one
  for x in xs:z=mul(z,x)
  return z
 P=mm(mm(L,C),U)
 expected=[[zero,prod(a,b,a),prod(a,c)],[prod(a,t,a),add(neg(prod(a,t,a2)),prod(b,a),prod(a,d,a)),add(c,prod(a,e))],[zero,prod(f,a),g]]
 assert P==expected;E=mm(mm(P,Q),L)
 assert [{w:z for w,z in E[r][2].items()if w.count('a')==3}for r in range(3)]==[zero,neg(prod(a,t,a2,Q[1][2])),zero]
 degree_bounds=[max((w.count('a')for block in E[r]for w in block),default=0)for r in (0,2)];assert degree_bounds==[3,2]
 Qred=[[Q[0][0],Q[0][1],Q[0][2]],[Q[1][0],Q[1][1],zero],[Q[2][0],Q[2][1],zero]];Er=mm(mm(P,Qred),L);assert [Er[r][2]for r in range(3)]==[zero,prod(a,t,a,Q[0][2]),zero]
 # Source built from input phase abd and its two literal amplitudes.
 I=s.eye(16);A=s.zeros(16);S=s.zeros(16);X=s.zeros(16);Sw=s.zeros(16)
 for x in range(16):
  y=(x>>1)|((x&1)<<3);sgn=-1 if(x&11)==11 else 1;A[y,x]=sgn*(1+s.I)/2;A[y^2,x]=sgn*(1-s.I)/2;S[y,x]=sgn;X[x^1,x]=1;Sw[((x&1)<<1)|((x&2)>>1)|(x&12),x]=1
 tidy=lambda M:M.applyfunc(s.expand);A2=tidy(A*A);A3=tidy(A2*A);Da=s.diag(*[s.I**(x&1)for x in range(16)]);Db=s.diag(*[s.I**((x>>1)&1)for x in range(16)]);Dc=s.diag(*[s.I**((x>>2)&1)for x in range(16)]);F=s.diag(*[-1 if x==15 else 1 for x in range(16)])
 controls=[]
 for name,T in [('I',I),('quarter_D_b',Db),('quartic_sign',F)]:
  J=tidy(A*T*A.conjugate().T);assert all(sum(J[i,j]!=0 for i in range(16))==1 for j in range(16));assert tidy(A*T*A)==tidy(J*A2)and tidy(A*T*A2)==tidy(J*A3);controls.append(name)
 pp=(I+Db**2)/2;pm=(I-Db**2)/2;Z=s.zeros(16);Cnum=s.Matrix.vstack(s.Matrix.hstack(Z,pp,pm),s.Matrix.hstack(Db,Sw,Dc),s.Matrix.hstack(Z,pm,pp));Di=Db**3
 Cinv=s.Matrix.vstack(s.Matrix.hstack(-Di*(Sw*pp+Dc*pm),Di,-Di*(Sw*pm+Dc*pp)),s.Matrix.hstack(pp,Z,pm),s.Matrix.hstack(pm,Z,pp));assert tidy(Cinv*Cnum)==s.eye(48)and tidy(Cnum*Cinv)==s.eye(48)
 assert pm.conjugate().T*pm+pp.conjugate().T*pp==I and s.trace(pp)==s.trace(pm)==8
 clock=S.conjugate().T*Db;bad=tidy(A*clock*A2);support=sorted({sum(z!=0 for z in row)for row in bad.tolist()});assert support==[4]and tidy(clock*clock.conjugate().T)==I
 prog=o.repo/'research/moonshot-005-program';deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-boolean-sign-family/author/PROOF.md','results/complex-inverse-native-coset/two-native/PROOF.md'];proof=Path(__file__).with_name('MIDDLE-PIVOT-ALL-ORDINARY-GATE.md')
 result={'status':'PASS_AUTHOR_MIDDLE_PIVOT_ALL_ORDINARY_GATE_CONTROLS','scope':'Formal identities and literal source/unit controls support the universal faithful-width image-rank proof. Arbitrary Q and arbitrary remaining C blocks; no finite failure theorem.','formal_prefix':True,'last_column_only_degree3_term':'-a t a² q12 in middle row','top_bottom_word_degree_bounds':degree_bounds,'last_column_after_q12_q22_zero':'(0,a t a q02,0)','transport_controls':controls,'noncommuting_C_control':{'explicit_two_sided_inverse':True,'both_c_g_singular_rank8':True,'stack_c_g_Gram_identity':True},'failed_transport_clock_control':{'unit':True,'a_t_a2_column_supports':support,'not_a_positive_caller':True},'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'source_pins':{d:hashlib.sha256((prog/d).read_bytes()).hexdigest()for d in deps}}
 o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['proof_sha256'])
if __name__=='__main__':main()
