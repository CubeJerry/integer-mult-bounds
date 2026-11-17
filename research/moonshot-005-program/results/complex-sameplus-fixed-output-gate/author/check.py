#!/usr/bin/env python3
"""Exact source identities for the all-g,h fixed-output same-plus gate."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
ENGINE_SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
POSITIVE_PINS={'PROOF.md':'904a4a1b2d859661a3d3a832e476977f78e64907bce4aafb02e8a63d7fe6ea1a',
               'check.py':'92e1cf3bb50f15a9611c23d49473082001efcfb37b09200eb46708c70fd0f3b3'}

def run(repo,positive,out):
 assert hashlib.sha256((repo/ENGINE).read_bytes()).hexdigest()==ENGINE_SHA
 for name,pin in POSITIVE_PINS.items():assert hashlib.sha256((positive/name).read_bytes()).hexdigest()==pin
 spec=importlib.util.spec_from_file_location('sameplus_fixed_output_exact',repo/ENGINE)
 m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 def sc(x,v):
  v=F(v);assert not v.denominator&(v.denominator-1)
  q=x.scale((v.numerator,0));return m.M(q.a,q.k+v.denominator.bit_length()-1).norm()
 def tab(dest,phase):
  bs=[tuple((x>>k)&1 for k in range(4)) for x in range(16)]
  return m.monomial([dest(*x) for x in bs],[phase(*x)%4 for x in bs])
 I16=m.eye(16);R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
 Xb=m.monomial([x^2 for x in range(16)],[0]*16)
 A=sc(I16.scale((1,1))+Xb.scale((1,-1)),F(1,2))@R
 s=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
 s1=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
 s2=tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
 q=A.star()@s2@A
 assert q@q==I16 and {sum(v!=(0,0) for v in row) for row in q.a}=={4}
 assert m.gaussian_rank(q)==2 and q.trace()==(8,0)
 assert A.star()@s@A==s1 and A.power(-2)@s@A.power(2)==s2
 assert [m.gaussian_rank(A.power(-j)) for j in range(4)]==[0,1,2,3]
 I2=m.eye(2);Zsig=m.monomial([0,1],[0,2]);Xsig=m.monomial([1,0],[0,0])
 a=I2.tensor(A);S=Zsig.tensor(s);S1=Zsig.tensor(s1);S2=Zsig.tensor(s2)
 d=a.n;I=m.eye(d);Z=m.zero(d)
 P=sc(I+S,F(1,2));N=I+sc(P,-1)
 P1=sc(I+S1,F(1,2));N1=I+sc(P1,-1)
 P2=sc(I+S2,F(1,2));N2=I+sc(P2,-1)
 P3=sc(I+Zsig.tensor(q),F(1,2))
 assert P3@P3==P3 and P3.trace()==(16,0)
 assert P.trace()==(16,0) and P3!=Z
 def sm(xs):
  r=Z
  for x in xs:r=r+x
  return r
 def mm(x,y):return [[sm(x[i][k]@y[k][j] for k in range(len(y))) for j in range(len(y[0]))] for i in range(len(x))]
 def ident():return [[I if i==j else Z for j in range(3)] for i in range(3)]
 def shear(i,j,c):
  x=ident();x[i][j]=sc(I,c);return x
 C=[[P,Z,sc(N,-1)],[P,I,sc(N,-1)],[N,Z,P]]
 Cinv=mm([[P,Z,N],[Z,I,Z],[sc(N,-1),Z,P]],shear(1,0,-1))
 Oinv=mm(shear(2,1,1),shear(1,0,-1))
 L=[[a,Z,Z],[I,a,Z],[Z,Z,I]];U=[[a,sc(a.power(2),-1),Z],[Z,a,Z],[Z,Z,I]]
 Dinv=[[a.power(-[4,2,1][i]) if i==j else Z for j in range(3)] for i in range(3)]
 sbc=I2.tensor(tab(lambda a,b,c,d:a+2*c+4*b+8*d,lambda a,b,c,d:0))
 phase=I2.tensor(tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:b))
 pref=Xsig.tensor(I16)
 examples=[('zero',Z,Z),('return_and_phase',sbc,phase),
           ('nonunit_coefficients',I+S,phase+sc(I,-1)),
           ('prefix_noncommuting',pref,sbc),('dense_sum',sc(I+sbc,F(1,2)),pref+phase)]
 receipts=[]
 for name,g,h in examples:
  W=ident();W[0][2]=g;W[1][2]=h
  Wi=ident();Wi[0][2]=sc(g,-1);Wi[1][2]=sc(h,-1)
  assert mm(W,Wi)==mm(Wi,W)==ident()
  Cgh=mm(C,W);assert mm(Cgh,mm(Wi,Cinv))==ident()
  M=mm(mm(mm(Oinv,L),Cgh),U)
  f=P@g+sc(N,-1)
  want=[[a@P@a,sc(a@P@a.power(2),-1),a@f],
        [P@a,N@a.power(2),f+a@h],
        [a,Z,S+g+a@h]]
  assert M==want
  expected=[[a.power(-2)@P1,sc(a.star()@P2,-1),a.power(-3)@f],
            [a.star()@P1,N2,a.power(-2)@f+a.star()@h],
            [I,Z,a.star()@(S+g)+h]]
  assert mm(Dinv,M)==expected
  assert sc(a.star()@P1@h,-1)+a.star()@h==a.star()@N1@h
  assert N@f==sc(N,-1)
  receipts.append({'name':name,'source_equation3':True,'normalized_coefficients':True,
                   'g_commutes_S':g@S==S@g,'h_commutes_S':h@S==S@h})
 # Explicit guards: the range in (6) exists physically; the collective ordinary
 # coefficient restriction and nonordinary q are indispensable.
 assert (I+sc(Zsig.tensor(q),-1))@P3==Z
 assert (I+sc(Zsig.tensor(s2),-1))@P2==Z
 assert A.star()@s2@A!=s2
 result={'status':'PASS_SAMEPLUS_FIXED_OUTPUT_GATE',
  'scope':'fixed O and Gaussian heads a4,a2,a; arbitrary ordinary Q,Iin,g,h in fixed finite prefix/tail model',
  'source_repairs':'C(I+e02(g)+e12(h)), no commutation or invertibility assumptions on g,h',
  'finite_source_equation_checks':receipts,
  'q_nonzero_entries_per_row':4,'q_gaussian_rank':2,
  'physical_P3_rank_at_reduced_prefix_tail1':16,
  'physical_bank_dimension_at_check':32,
  'universal_second_Q_column_required_factorization':'(-h,0,I)^T w with w=P w',
  'universal_column_rank_upper_bound':'D_bank/2, contradicting a whole-bank left inverse',
  'positive_whole_column_identity_preserved':True,
  'changed_output_complements_excluded':False,
  'new_kappa':False}
 out.mkdir(parents=True,exist_ok=True)
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 witness={'denominator_power2':q.k,'nonzero_entries':[[i,j,v[0],v[1]] for i,row in enumerate(q.a) for j,v in enumerate(row) if v!=(0,0)]}
 (out/'NONORDINARY-WITNESS.json').write_text(json.dumps(witness,indent=2)+'\n')
 files={'PROOF.md':Path(__file__).with_name('PROOF.md'),'check.py':Path(__file__),
        'output/RESULT.json':out/'RESULT.json','output/NONORDINARY-WITNESS.json':out/'NONORDINARY-WITNESS.json'}
 (out/'MANIFEST.json').write_text(json.dumps({'engine':{ENGINE:ENGINE_SHA},'positive_package':POSITIVE_PINS,
       'files':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()}},indent=2)+'\n')
 print(result['status'],'five exact g,h controls; all coefficients ordinary; output complements open',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--positive',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args();run(a.repo,a.positive,a.out)
