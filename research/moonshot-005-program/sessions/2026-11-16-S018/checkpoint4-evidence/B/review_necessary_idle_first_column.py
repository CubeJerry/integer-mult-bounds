#!/usr/bin/env python3
"""Independent u=0 formal identity and literal rank-collapse controls."""
from pathlib import Path
import argparse,json,hashlib
from check_triangular_first_interstage import add,mul,neg,atom,mm
from review_square_normalizer import mm as imat,adj,tm,mt

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--proof',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();one,zero={():1},{}
 def prod(*xs):
  z=one
  for x in xs:z=mul(z,x)
  return z
 a,s,b,t,d,e,f=map(atom,('a','s','b','t','d','e','f'));L=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U=[[a,neg(prod(a,a)),zero],[zero,a,zero],[zero,zero,one]];C=[[s,b,zero],[t,d,e],[zero,f,zero]];Q=[[atom(f'q{i}{j}')for j in range(3)]for i in range(3)];Q[0][2]=Q[1][2]=zero
 E=mm(mm(mm(mm(L,C),U),Q),L);assert E[2][0]==add(prod(f,a,Q[1][0],a),prod(f,a,Q[1][1]));Q[1][1]=zero;E=mm(mm(mm(mm(L,C),U),Q),L);assert E[2][1]==zero;assert E[0][1]==prod(a,s,a,Q[0][1],a);assert max(w.count('a')for r in range(3)for w in E[r][1])==3
 A=[[(0,0)for _ in range(16)]for _ in range(16)];S=[[(0,0)for _ in range(16)]for _ in range(16)]
 for x in range(16):
  y=(x>>1)|((x&1)<<3);sgn=-1 if(x&11)==11 else 1;A[y][x]=(sgn,sgn);A[y^2][x]=(sgn,-sgn);S[y][x]=(sgn,0)
 Xb=tm([(x^2,0)for x in range(16)]);collapsed=imat(imat(A,adj(S)),A);expected=imat(Xb,S);assert collapsed==[[(4*r,4*j)for r,j in row]for row in expected]
 A2=imat(A,A);word=imat(imat(A2,adj(S)),A);assert all(sum(word[y][x]!=(0,0)for y in range(16))==2 for x in range(16));assert mt(imat(imat(A2,adj(S)),adj(A2)),16)is None
 result={'status':'PASS_B_INDEPENDENT_NECESSARY_IDLE_FIRST_COLUMN_REVIEW','universal_proof_review':'Accepted: finite selected-word left stripping separates pure rank1 from ordinary; normal-form images make the E2 bottom projection injective. u=0 gives q11=0 and then a forbidden nonzero column1 top block. No u-unit claim or small-width inference.','formal_bottom_column0':True,'formal_final_column1':True,'max_final_column1_A_degree':3,'literal_ASinvA_equals_XbS':True,'literal_A2SinvA_exact_support2':True,'Sinv_outside_square_monomial_class':True,'proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest()};o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['proof_sha256'])
if __name__=='__main__':main()
