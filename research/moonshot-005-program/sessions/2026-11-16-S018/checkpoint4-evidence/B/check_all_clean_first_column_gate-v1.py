#!/usr/bin/env python3
"""Formal extra-source filtration and literal failed-hypothesis controls."""
from pathlib import Path
import argparse,hashlib,json
from check_triangular_first_interstage import add,mul,neg,atom,mm
from review_square_normalizer import mm as imat,adj,tm,mt

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();one,zero={():1},{}
 def prod(*xs):
  z=one
  for x in xs:z=mul(z,x)
  return z
 def clean(p):
  out={}
  for w,c in p.items():
   w=list(w);j=0
   while j+1<len(w):
    if w[j]=='a'and w[j+1]in('s','t','u'):w[j:j+2]=[w[j+1]+'hat','a']
    j+=1
   w=tuple(w);out[w]=out.get(w,0)+c
  return{w:c for w,c in out.items()if c}
 a,s,b,t,d,e,u,f=map(atom,('a','s','b','t','d','e','u','f'));a2=prod(a,a);a3=prod(a,a,a);L=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U=[[a,neg(a2),zero],[zero,a,zero],[zero,zero,one]];C=[[s,b,zero],[t,d,e],[u,f,zero]];Q=[[atom(f'q{i}{j}')for j in range(3)]for i in range(3)];Q[0][2]=Q[1][2]=zero
 E=mm(mm(mm(mm(L,C),U),Q),L);bottom=[clean(prod(a,x))for x in E[2]];highest=[{w:c for w,c in z.items()if w.count('a')==4}for z in bottom];assert highest==[neg(prod(atom('uhat'),a3,Q[1][0],a)),neg(prod(atom('uhat'),a3,Q[1][1],a)),zero]
 C[2][0]=zero;Q[1][1]=zero;Ef=mm(mm(mm(mm(L,C),U),Q),L);assert Ef[2][1]==zero;assert clean(Ef[0][1])==prod(atom('shat'),a2,Q[0][1],a);assert max(w.count('a')for r in range(3)for w in Ef[r][1])==3
 # Check the minimal nonclean clock and both directions of its ordinary coupling.
 A=[[(0,0)for _ in range(16)]for _ in range(16)];S=[[(0,0)for _ in range(16)]for _ in range(16)]
 for x in range(16):
  y=(x>>1)|((x&1)<<3);sgn=-1 if(x&11)==11 else 1;A[y][x]=(sgn,sgn);A[y^2][x]=(sgn,-sgn);S[y][x]=(sgn,0)
 Db=tm([(x,(x>>1)&1)for x in range(16)]);H=imat(adj(S),Db);assert mt(H,1)is not None;bad=imat(imat(A,H),adj(A));assert mt(bad,4)is None
 # Noncommutative formal inverse of C=[[1,0,0],[0,1,1],[h,1,0]].
 h=atom('h');Cc=[[one,zero,zero],[zero,one,one],[h,one,zero]];Ci=[[one,zero,zero],[neg(h),zero,one],[h,one,neg(one)]];Id=[[one if i==j else zero for j in range(3)]for i in range(3)];assert mm(Cc,Ci)==mm(Ci,Cc)==Id
 p,q,r,z=map(atom,('p','q','r','z'));Qr=[[p,q,zero],[r,z,zero],[neg(p),neg(q),one]];Ec=mm(mm(mm(mm(L,Cc),U),Qr),L);assert Ec[1]==[zero,zero,a]
 proof=Path(__file__).with_name('ALL-CLEAN-FIRST-COLUMN-GATE.md');base=Path(__file__).with_name('CLEAN-FIRST-COLUMN-SQUARE-GATE-v1.md');result={'status':'PASS_AUTHOR_ALL_CLEAN_FIRST_COLUMN_UNRESTRICTED_Q_GATE','scope':'Formal ordered product, additional rank1 multiplication degree filter, column1 support bound and exact nonclean-clock/ordinary inverse controls. Universal proof is finite tensor separation plus component-image directness and the ordinary left-coset argument.','highest_degree_terms_in_a_Ebottom':['-uhat a³q10a','-uhat a³q11a','0'],'last_column1_after_u_q11_zero':{'bottom_zero':True,'top':'shat a²q01a','maximum_A_degree':3},'nonclean_clock_control':{'h':'S^-1D_b','ordinary_unit':True,'a_h_ainverse_nonmonomial':True,'minimal_idle_coupling_two_sided_inverse':True,'rank1_job_exactly_isolated_with_Qrow2_minus_Qrow0':True,'not_a_positive_caller':True},'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'normal_form_proof_sha256':hashlib.sha256(base.read_bytes()).hexdigest()};o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['proof_sha256'])
if __name__=='__main__':main()
