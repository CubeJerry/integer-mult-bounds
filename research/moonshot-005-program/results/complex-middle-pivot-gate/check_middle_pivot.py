#!/usr/bin/env python3
"""Exact block-algebra diagnostics for MIDDLE-PIVOT-LEMMA.md, not a search theorem."""
import argparse,hashlib,importlib.util,json,sys,random
from pathlib import Path
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ar=ap.parse_args();base=Path(__file__).parent
 rng=random.Random(2026111509);cases=[]
 for n in (2,3):
  for trial in range(8):
   I=s.eye(n);E=s.zeros(n);E[0,1]=1
   D=I if trial%2 else s.diag(*([1]+[0]*(n-1)));H=-E
   assert D*H==-E
   def invmat():
    Q=s.eye(n)
    for k in range(5*n):
     i,j=rng.sample(range(n),2);Q[i,:]=Q[i,:]+rng.choice([-2,-1,1,2])*Q[j,:]
    return Q
   G=invmat();R=invmat();S=invmat();P=s.Matrix(n,n,[rng.randrange(-2,3) for _ in range(n*n)]);E0=s.Matrix(n,n,[rng.randrange(-2,3) for _ in range(n*n)]);Q=R+P*D;F=S+H*E0
   CL=P.row_join(Q).col_join(I.row_join(D));CR=E0.row_join(I).col_join(F.row_join(H));assert CL.det()!=0 and CR.det()!=0
   K=G+E;W=CL*s.diag(K,I)*CR;Waa=W[:n,:n];Wai=W[:n,n:];Wia=W[n:,:n];Wii=W[n:,n:]
   assert Wii==G and Wai==P*G+R*H and Wia==G*E0+D*S
   assert Waa-Wai*G.inv()*Wia==R*(I-H*G.inv()*D)*S
   cases.append({'block_dimension':n,'singular_D':D.det()==0,'singular_H':H.det()==0})
 # Genuine actual-source counterexample if ordinary elimination is omitted.
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
 sp=importlib.util.spec_from_file_location('middle_pivot_dyadic',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 i=m.eye(8);xb=m.monomial([j^2 for j in range(8)],[0]*8);cb=m.M((i.scale((1,1))+xb.scale((1,-1))).a,1).norm();perm=m.monomial([0,4,1,5,2,6,3,7],[0]*8);a=cb@perm;z=m.zero(8);G=m.diagonal([a,a]);Ii=m.eye(16);Zi=m.zero(16);H=m.block([[z,i],[z,z]]);E=H.scale((-1,0));K=G+E
 CL=m.block([[Zi,Ii],[Ii,Ii]]);CR=m.block([[Zi,Ii],[Ii,H]]);W=CL@m.diagonal([K,Ii])@CR;assert W==m.block([[Ii,H],[Ii,G]])
 inverseG=m.diagonal([a.star(),a.star()]);eliminator=H@inverseG;assert eliminator==m.block([[z,a.star()],[z,z]])
 # Its nonzero coefficient is a genuine rank-one Gaussian, so this elimination is not ordinary.
 assert m.gaussian_rank(a.star())==1;schur=Ii+eliminator.scale((-1,0));assert schur!=Ii
 out={'status':'PASS_EXACT_MIDDLE_GAUSSIAN_PIVOT_DIAGNOSTICS','noncommutative_rational_block_cases':len(cases),'singular_D_cases':sum(x['singular_D'] for x in cases),'singular_H_cases':sum(x['singular_H'] for x in cases),'actual_source_negative_control':'A pure full Gaussian idle pivot alone is insufficient; W=[[I,H],[I,G]] requires the nonordinary eliminator H G^-1, and Schur=I-H G^-1 retains a rank-one component.','proof_status':'Written lemma pending independent review; these checks do not prove the Gaussian filtration assertion by finite enumeration.','new_kappa':False}
 (base/'MIDDLE-PIVOT-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
