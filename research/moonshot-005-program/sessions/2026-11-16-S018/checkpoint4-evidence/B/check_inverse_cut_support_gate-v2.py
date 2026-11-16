#!/usr/bin/env python3
"""Exact cut degrees, inverse identities and support-bound controls."""
from pathlib import Path
import argparse,hashlib,json
from check_triangular_first_interstage import add,mul,neg,atom,mm
from review_square_normalizer import mm as imat,adj,tm

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();one,zero={():1},{}
 def prod(*xs):
  z=one
  for x in xs:z=mul(z,x)
  return z
 def reduce(p):
  out={}
  for word,c in p.items():
   st=[]
   for x in word:
    if st and(st[-1],x)in(('a','ai'),('ai','a')):st.pop()
    else:st.append(x)
   w=tuple(st);out[w]=out.get(w,0)+c
  return{w:c for w,c in out.items()if c}
 def norm(M):return[[reduce(z)for z in row]for row in M]
 a,ai=atom('a'),atom('ai');a2=prod(a,a);ai2=prod(ai,ai);L=[[a,zero],[one,a]];U=[[a,neg(a2)],[zero,a]];Li=[[ai,zero],[neg(ai2),ai]];Ui=[[ai,one],[zero,ai]];Id=[[one,zero],[zero,one]]
 assert norm(mm(U,Ui))==norm(mm(Ui,U))==Id and norm(mm(L,Li))==norm(mm(Li,L))==Id
 Bi=[[atom(f'b{i}{j}')for j in range(2)]for i in range(2)];Qa=[[atom(f'q{i}{j}')for j in range(2)]for i in range(2)];Pinv=mm(mm(Ui,Bi),[[ai,zero],[zero,one]]);W=mm(Qa,L)
 invdeg=max(w.count('ai')for row in Pinv for block in row for w in block);fwdeg=max(w.count('a')for row in W for block in row for w in block);assert(invdeg,fwdeg)==(2,1)
 sharp=mm(mm(L,U),L);assert sharp==[[zero,neg(prod(a,a,a,a))],[a2,zero]];assert max(w.count('ai')for row in mm(Ui,Li)for block in row for w in block)==3
 # General clean-first normal-form quotient; no commuting symbols.
 s,b,t,d,e,u,f=map(atom,('s','b','t','d','e','u','f'));C=[[s,b,zero],[t,d,e],[u,f,zero]];Q=[[Qa[0][0],Qa[0][1],zero],[Qa[1][0],Qa[1][1],zero],[atom('q20'),atom('q21'),atom('q22')]];L3=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U3=[[a,neg(a2),zero],[zero,a,zero],[zero,zero,one]];E=mm(mm(mm(mm(L3,C),U3),Q),L3)
 B=[[s,b],[u,f]];M=mm(mm(mm(mm([[a,zero],[zero,one]],B),U),Qa),L);assert [[E[r][j]for j in range(2)]for r in(0,2)]==M and E[0][2]==E[2][2]==zero
 A=[[(0,0)for _ in range(16)]for _ in range(16)]
 for x in range(16):
  y=(x>>1)|((x&1)<<3);sgn=-1 if(x&11)==11 else 1;A[y][x]=(sgn,sgn);A[y^2][x]=(sgn,-sgn)
 def supports(M):return[sum(M[y][x]!=(0,0)for y in range(16))for x in range(16)]
 Ai=adj(A);A2=imat(A,A);A3=imat(A2,A);A4=imat(A3,A);assert supports(A4)==[16]*16 and supports(A)==supports(Ai)==[2]*16
 assert imat(A,Ai)==[[((4,0)if i==j else(0,0))for j in range(16)]for i in range(16)]
 examples=[]
 for q in range(64):
  H=tm([((x^((q>>4)&3)),((q&3)*(x&1)+((q>>2)&3)*((x>>2)&1)+2*int((x&3)==3))%4)for x in range(16)])
  T=imat(imat(Ai,H),Ai);TG=imat(T,A4);ss=supports(TG);assert min(ss)>=4
  Ti=adj(T);assert max(supports(Ti))<=4
  examples.append({'control':q,'min_TG_support':min(ss),'max_TG_support':max(ss),'max_inverse_T_support':max(supports(Ti))})
 two=imat(imat(Ai,Ai),A4);three=imat(imat(imat(Ai,Ai),Ai),A4);assert supports(two)==[4]*16 and supports(three)==[2]*16
 proof=Path(__file__).with_name('INVERSE-CUT-SUPPORT-GATE.md');normal=Path(__file__).with_name('CLEAN-FIRST-COLUMN-SQUARE-GATE-v1.md');prog=o.repo/'research/moonshot-005-program';deps=['results/complex-inverse-native-coset/two-native/PROOF.md','results/complex-four-bit-cubic-source/author/PROOF.md']
 result={'status':'PASS_AUTHOR_INVERSE_SUPPORT_CUT_AND_COMPLETE_CLEAN_FIRST_GATE','scope':'Universal finite-catalogue proof is in companion text. Exact checks cover ordered U/L inverses, F2/F1 cut, full clean-first normal-form quotient, source support controls and the sharp three-native rank4 identity; no failed finite search is used.','cut_inverse_degree':invdeg,'cut_forward_degree':fwdeg,'independent_endpoint_rank_bound':invdeg+fwdeg,'formal_U_inverse':True,'formal_L_inverse':True,'formal_general_top_bottom_quotient':True,'sharp_LUL_identity':True,'sharp_original_LU_inverse_degree':3,'literal_controls':examples,'sharp_support_controls':{'Aminus2_A4':4,'Aminus3_A4':2},'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'normal_form_proof_sha256':hashlib.sha256(normal.read_bytes()).hexdigest(),'source_pins':{x:hashlib.sha256((prog/x).read_bytes()).hexdigest()for x in deps}}
 o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['proof_sha256'])
if __name__=='__main__':main()
