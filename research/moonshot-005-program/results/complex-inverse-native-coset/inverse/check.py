#!/usr/bin/env python3
"""Exact finite controls; the universal source proof is PROOF.md."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());args=ap.parse_args();base=Path(__file__).parent
hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
sp=importlib.util.spec_from_file_location('inv_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
I=m.eye(8);Xb=m.monomial([x^2 for x in range(8)],[0]*8);C=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm();P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);Q=m.monomial([((x&1)<<2)+(x&2)+((x&4)>>2)for x in range(8)],[0]*8)
units=[(1,0),(0,1),(-1,0),(0,-1)];cases=[];omitted=0;wrong_inv=0
for mask,J,B in[(128,0,0),(64,0,1),(112,1,0),(176,1,1)]:
 f=lambda x:J*((x>>2)&1)^B*((x>>1)&1)*((x>>2)&1)^(x==7)
 assert sum(int(f(x))<<x for x in range(8))==mask
 D=m.monomial(list(range(8)),[2*int(f(x))for x in range(8)]);S=D@P;A=C@S
 Z=m.monomial(list(range(8)),[2*((x.bit_count()%2)^(B*(x&1)*((x>>2)&1)))for x in range(8)]);T=Z@Q@S
 phases=[2*(((J+1)%2*(x&1))^((x>>1)&1)^((x>>2)&1)^(B*((x&1)*((x>>1)&1)^(x&1)*((x>>2)&1)))^(x==7))for x in range(8)]
 direct=m.monomial([0,1,4,5,2,3,6,7],phases);assert T==direct
 assert T@A.star()@T.star()==A.scale((0,-1))
 assert T.power(2)==I
 if Q@S@A.star()@S.star()@Q!=A.scale((0,-1)):wrong_inv+=1
 for V in[1,2]:
  a=A.tp(V);t=T.tp(V);e=m.eye(8**V);z=m.zero(8**V);lam=units[(-V)%4];neg=lambda g:g.scale((-1,0))
  assert a.star()==(t.star()@a@t).scale(lam)
  N0=lambda b:m.block([[b,z],[e,b]])
  N2=lambda b:m.block([[b,neg(b.power(2))],[z,b]])
  swap=m.block([[z,e],[e,z]]);tt=m.diagonal([t,t]);d=m.diagonal([e.scale(lam),e]);ef=m.diagonal([e,e.scale(lam)])
  n0=N0(a);n2=N2(a)
  for typ,native,other in[(0,n0,N2),(2,n2,N0)]:
   wrapped=swap@tt.star()@d@other(a)@ef@tt@swap
   assert native@wrapped==m.eye(2*8**V) and wrapped@native==m.eye(2*8**V)
   assert wrapped==swap@other(a.star())@swap
   if swap@tt.star()@other(a)@tt@swap!=wrapped:omitted+=1
  cases.append({'mask':mask,'V':V,'dimension':2*8**V,'all_native_columns_checked':True})
 # All four lambda residues are checked directly on one-column block identities.
 z=m.zero(8)
 for lam in units:
  aa=A.scale(lam);d=m.diagonal([I.scale(lam),I]);e=m.diagonal([I,I.scale(lam)])
  for n in [lambda b:m.block([[b,z],[I,b]]),lambda b:m.block([[b,b.power(2).scale((-1,0))],[z,b]])]:assert d@n(A)@e==n(aa)
assert omitted==16,omitted
assert wrong_inv==4,wrong_inv
result={'status':'PASS_EXACT_NONCLIFFORD_INVERSE_NATIVE','cases':cases,'phase_scalar_controls':32,'omitted_width_scalar_rejections':omitted,'omitted_sign_gauge_rejections':wrong_inv,'tables':4,'physical_scope':'Exact head inverse; forward fresh body retained. Literal full inverse additionally owes two body translation services.','additional_wrapper_invoice':{'monomial_tables':4,'unit_scalar_passes_before_fusion':2,'bank_role_swaps':2,'new_gaussian_queries':0,'new_owners':0},'classification':'Proved written all-width algebra; finite checker supplementary; physical tariff inherited conditionally','new_kappa':False};(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
