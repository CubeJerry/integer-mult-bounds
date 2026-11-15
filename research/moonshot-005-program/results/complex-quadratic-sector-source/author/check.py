#!/usr/bin/env python3
"""Exact actual-phase source controls. Universal statement is in PROOF.md."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);args=ap.parse_args();here=Path(__file__).resolve().parent
 deps=json.loads((here/'DEPENDENCIES.json').read_text())
 for d in deps['sources']:assert hashlib.sha256((args.repo/d['path']).read_bytes()).hexdigest()==d['sha256'],d['path']
 hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sp=importlib.util.spec_from_file_location('sector_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);Xb=m.monomial([j^2 for j in range(8)],[0]*8);Cb=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm()
 P=m.monomial([0,4,1,5,2,6,3,7],[0]*8)
 D=m.monomial(list(range(8)),[(((x>>1)&1)+2*(x&1)*((x>>2)&1))%4 for x in range(8)])
 A=Cb@D@P;H=m.monomial(list(range(8)),[2*(x&1)*((x>>2)&1)for x in range(8)]);J=m.monomial(list(range(8)),[2*(x&1)*((x>>1)&1)for x in range(8)])
 assert H@A==A@J and H.power(2)==J.power(2)==I
 cubic=A.power(2)@J@A;quad=A@J@A
 assert [m.gaussian_rank(x)for x in [A,A.power(2),A.power(3),quad,cubic]]==[1,2,3,2,3]
 assert all(cubic!=A.power(3).scale(z)for z in[(1,0),(0,1),(-1,0),(0,-1)])
 def sub(a,b):return a+b.scale((-1,0))
 def half(a):return m.M(a.a,a.k+1).norm()
 widths=[]
 for V in[1,2]:
  a,h,k=A.tp(V),H.tp(V),J.tp(V);n=8**V;iv=m.eye(n);zero=m.zero(n);neg=iv.scale((-1,0))
  p=half(iv+h);q=half(sub(iv,h));v=half(sub(iv,k));b=a@k@a;a2=a.power(2)
  K=m.block([[iv,zero,sub(a,iv)],[a,zero,a.scale((-1,0))],[iv,iv,neg]])
  C=m.block([[p,zero,q],[zero,iv,zero],[q,zero,p]])
  Q=m.block([[iv,zero,sub(iv,k)],[zero,iv,zero],[iv,zero,iv]])
  W=K@C@K@Q@K
  W2=m.block([[a2@(iv+v),a2@v,sub(b,a2@(iv+v))],[a2@k,a2@k,(a2@k).scale((-1,0))],[zero,zero,b]])
  W3=m.block([[zero,zero,a2@v@a],[zero,zero,a2@k@a],[zero,zero,zero]])
  assert W==W2+W3
  assert (a2@k@a).star()@(a2@k@a)==iv
  assert C@C==m.eye(3*n) and C.star()==C
  # Direct conditional role permutation, all independent input columns.
  perm=[]
  for role in range(3):
   for x in range(n):
    y=x;par=0
    for _ in range(V):digit=y%8;y//=8;par^=(digit&1)*((digit>>2)&1)
    out=2-role if role in(0,2) and par else role
    perm.append(out*n+x)
  assert C==m.monomial(perm,[0]*(3*n))
  # Fully primitive C circuit: S^-1 diag(I,h) S on roles0/2.
  addxz=m.block([[iv,zero,iv],[zero,iv,zero],[zero,zero,iv]])
  addzx=m.block([[iv,zero,zero],[zero,iv,zero],[iv,zero,iv]])
  subzx=m.block([[iv,zero,zero],[zero,iv,zero],[neg,zero,iv]])
  subxz=m.block([[iv,zero,neg],[zero,iv,zero],[zero,zero,iv]])
  scale2=m.diagonal([iv,iv,iv.scale((-2,0))])
  scalehalf=m.diagonal([iv,iv,half(neg)])
  hp=m.diagonal([iv,iv,h])
  assert C==subxz@scalehalf@subzx@hp@addzx@scale2@addxz
  assert subxz@subzx@hp@addzx@scale2@addxz!=C
  # Literal Q circuit: add, phase, subtract, add.
  e02=m.block([[iv,zero,iv],[zero,iv,zero],[zero,zero,iv]])
  phase=m.diagonal([iv,iv,k])
  em02=m.block([[iv,zero,neg],[zero,iv,zero],[zero,zero,iv]])
  e20=m.block([[iv,zero,zero],[zero,iv,zero],[iv,zero,iv]])
  assert Q==e20@em02@phase@e02
  Qinv=m.block([[k,zero,sub(iv,k)],[zero,iv,zero],[k.scale((-1,0)),zero,k]])
  assert Q@Qinv==Qinv@Q==m.eye(3*n)
  R=m.block([[iv+v,v,(iv+v).scale((-1,0))],[k,k,k.scale((-1,0))],[zero,zero,iv]])
  Rinv=m.block([[iv,(v@k).scale((-1,0)),iv],[neg,(iv+v)@k,zero],[zero,zero,iv]])
  assert R@Rinv==Rinv@R==m.eye(3*n)
  D2=m.diagonal([a2,a2,b]);Dinv=m.diagonal([a2.star(),a2.star(),b.star()])
  W2inv=Rinv@Dinv@em02
  assert W2@W2inv==W2inv@W2==m.eye(3*n)
  shear=m.block([[iv,zero,zero],[zero,iv,a],[zero,zero,iv]])
  assert em02@W==D2@R@shear
  # Global role relabelling gives three literal forward lower natives.
  swap=m.block([[zero,iv,zero],[iv,zero,zero],[zero,zero,iv]])
  L0=m.block([[a,zero,zero],[iv,a,zero],[zero,zero,iv]])
  T0=m.block([[zero,iv,neg],[zero,zero,iv],[iv,iv,neg]])
  K0=L0@T0
  assert K0==swap@K@swap
  assert swap@W@swap==K0@(swap@C@swap)@K0@(swap@Q@swap)@K0
  # Direct T0 instruction circuit; two ADDs then one bank cycle.
  addy=m.block([[iv,zero,zero],[zero,iv,neg],[zero,zero,iv]])
  addx=m.block([[iv,iv,zero],[zero,iv,zero],[zero,zero,iv]])
  cyc=m.block([[zero,iv,zero],[zero,zero,iv],[iv,zero,zero]])
  assert T0==cyc@addx@addy
  assert K@m.eye(3*n)@K@Q@K!=W
  assert K@C@K@(e20@phase@e02)@K!=W
  assert W!=m.diagonal([a.power(3),a2,a2])
  assert h@a!=a # dropping J violates transport
  widths.append({'width':V,'head_dimension':n,'independent_columns':3*n,'identities_4_to_7':True,'W2_invertible':True,'W3_rank':n,'literal_forward_source':True,'conditional_permutation':True})
 # The odometer's exact finite controls supplement its geometric-series bound.
 odos=[]
 for V in range(1,6):
  digits=[0]*V;par=0;updates=0
  for x in range(8**V):
   direct=0;y=x
   for _ in range(V):s=y%8;y//=8;direct^=(s&1)*((s>>2)&1)
   assert par==direct
   if x==8**V-1:break
   j=0
   while True:
    old=digits[j];new=(old+1)%8;digits[j]=new
    par^=((old&1)*((old>>2)&1))^((new&1)*((new>>2)&1));updates+=1
    if new:break
    j+=1
  assert 7*updates<=8*(8**V)
  odos.append({'width':V,'coordinates':8**V,'digit_updates':updates})
 result={'status':'PASS_EXACT_QUADRATIC_SECTOR_SOURCE','all_width_basis':'universal word identity plus exact multiplicative tensor transport','width_controls':widths,'ordinary_counts':{'native_add':3,'T0_add':6,'Q_add':3,'C_add':4,'total_add':16,'C_scale':2,'native_head_services':9,'T0_bank_cycles':3,'Q_quadratic_phase':1,'C_quadratic_phase':1,'new_owners':0,'new_gaussian_queries':0},'gaussian_profile':{'1':3,'7':6,'8':3},'ambient_axes_per_column':24,'odometer_controls':odos,'negative_controls':['missing quadratic control','omitted Q subtraction','wrong transport phase','omitted sector half scale','partial source misidentified as independent endpoint'],'scope':'actual mixed rank2/rank3 source; no complete Gaussian endpoints, supplier or new kappa'}
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'widths':widths,'gaussian_profile':result['gaussian_profile'],'total_add':16}))
if __name__=='__main__':main()
