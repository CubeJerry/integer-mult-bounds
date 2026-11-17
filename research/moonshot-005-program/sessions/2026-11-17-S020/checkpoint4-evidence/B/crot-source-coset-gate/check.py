#!/usr/bin/env python3
"""Exact controls for the strengthened Crot source-coset proof."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F

def run(repo,out):
 ep=repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sha='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';assert hashlib.sha256(ep.read_bytes()).hexdigest()==sha
 spec=importlib.util.spec_from_file_location('crot_coset_engine',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 I=m.eye(16);Z=m.zero(16)
 def frac(x,c):
  c=F(c);y=x.scale((c.numerator,0));return m.M(y.a,y.k+c.denominator.bit_length()-1).norm()
 def tab(dest,ph):return m.monomial([dest(*[(x>>j)&1 for j in range(4)]) for x in range(16)],[ph(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
 R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);Xb=m.monomial([x^2 for x in range(16)],[0]*16);A=frac(I.scale((1,1))+Xb.scale((1,-1)),F(1,2))@R
 s=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
 assert [m.gaussian_rank(A.power(j)) for j in [1,2,3,4]]==[1,2,3,4]
 controls=[]
 for sign in [1,-1]:
  T=frac(I+s.scale((sign,0)),F(1,2));N=I+T.scale((-1,0));T1=A.star()@T@A;T2=A.power(-2)@T@A.power(2)
  assert T@T==T and N@N==N and T@N==N@T==Z
  assert A@T@A==A.power(2)@T1 and A@T@A.power(2)==A.power(3)@T2
  C=m.block([[T,Z,N.scale((-1,0))],[Z,I,Z],[N,Z,T]]);Ci=m.block([[T,Z,N],[Z,I,Z],[N.scale((-1,0)),Z,T]])
  L=m.block([[A,Z,Z],[I,A,Z],[Z,Z,I]]);U=m.block([[A,A.power(2).scale((-1,0)),Z],[Z,A,Z],[Z,Z,I]])
  B=m.block([[A@T@A,(A@T@A.power(2)).scale((-1,0)),(A@N).scale((-1,0))],[T@A,N@A.power(2),N.scale((-1,0))],[N@A,(N@A.power(2)).scale((-1,0)),T]])
  assert L@C@U==B and C@Ci==Ci@C==m.eye(48)
  Rot=m.block([[T,N.scale((-1,0))],[N,T]]);Roti=m.block([[T,N],[N.scale((-1,0)),T]]);assert Rot@Roti==m.eye(32)
  # q20 is a noncommuting unit, H is arbitrary ordinary. The identity does not
  # assume that either commutes with T, or that H is itself a unit.
  q=R;qi=R.star();H=s+Xb
  K1=(N@q).scale((-1,0))+T@H;K2=T@q+N@H
  assert (qi@N@K1).scale((-1,0))+qi@T@K2==I
  assert N@K1==(N@q).scale((-1,0)) and T@K2==T@q
  assert (N@K1).scale((-1,0))+T@K2==q
  # Dropping the sign or q inverse breaks the claimed retraction.
  assert qi@N@K1+qi@T@K2!=I
  assert N@K1+T@K2!=I
  controls.append({'spectator_sign':sign,'Crot_and_inverse':True,'source_block_identity':True,'ordinary_zero_component_unit':True,'free_coset_frame_retraction':True,'transversality':True})
 # Word-family exclusions depend only on A,A2,A3 being distinct Gaussian ranks.
 # These sharp return directions are retained: lower source count alone does
 # NOT distinguish every Gaussian class, while the left-coset test does.
 g=R.star()@Xb;clock=R.star()@tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:b)
 assert A@g@A==R
 assert m.gaussian_rank(A.power(2)@g@A)==1
 assert m.gaussian_rank(A@clock@A)==1
 assert m.gaussian_rank((A.power(2)@g@A)@A.star())==2
 assert m.gaussian_rank((A@clock@A)@A.star())==1
 out.mkdir(parents=True,exist_ok=True)
 res={'status':'PASS_CROT_SOURCE_COSET_FRAME_GATE','scope':'fixed finite collective tail catalogue, with arbitrary finite matrix prefix; T nonzero ordinary idempotent and both backward transports ordinary','controls':controls,'return_coset_controls':{'A_g_A_ordinary':True,'A2_g_A_Gaussian1_but_not_left_coset_GA':True,'A_clock_A_Gaussian1_but_not_left_coset_GA':True},'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');mf={'engine_sha256':sha,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json']}};(out/'MANIFEST.json').write_text(json.dumps(mf,indent=2)+'\n');print(res['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.repo,a.out)
