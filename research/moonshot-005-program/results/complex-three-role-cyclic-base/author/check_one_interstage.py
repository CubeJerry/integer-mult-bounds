#!/usr/bin/env python3
"""Exact formula and independence controls for the one-interstage theorem."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ar=ap.parse_args();base=Path(__file__).parent
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';sp=importlib.util.spec_from_file_location('one_interstage_dyadic',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);xb=m.monomial([j^2 for j in range(8)],[0]*8);cb=m.M((I.scale((1,1))+xb.scale((1,-1))).a,1).norm();S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=cb@S;CZ=m.monomial(list(range(8)),[2*(j&1)*((j>>1)&1) for j in range(8)]);CNOT=m.monomial([j^((j&1)<<1) for j in range(8)],[0]*8);rows=[]
 for V in (1,2):
  a=A.tp(V);d=a.n;i=m.eye(d);z=m.zero(d);a2=a.power(2);L=m.block([[a,i,z],[z,a,z],[z,z,i]]);Li=m.block([[a.star(),a.power(-2).scale((-1,0)),z],[z,a.star(),z],[z,z,i]]);assert Li@L==m.eye(3*d)
  T=m.block([[z,z,i],[i,z,i.scale((-1,0))],[i,i,i.scale((-1,0))]])
  # Compute T^-1 from its known scalar matrix, avoiding any physical inverse primitive.
  import sympy as sy
  ts=sy.Matrix([[0,0,1],[1,0,-1],[1,1,-1]]);ti=ts.inv();Ti=m.block([[i.scale((int(ti[j,k]),0)) for k in range(3)] for j in range(3)]);assert T@Ti==m.eye(3*d);K=L@T
  E=m.M((i+a.power(6)).a,1).norm();F=i+E.scale((-1,0));assert E@E==E and F@F==F and E!=z and F!=z
  catalog=[[[i,z,CZ.tp(V)],[z,i,z],[z,z,i]],[[i,z,z],[z,i,CNOT.tp(V)],[z,z,i]],[[F,z,E],[z,i,z],[E,z,F]],[[i,z,z],[z,i,z],[i,z,i]]]
  for n,p in enumerate(catalog):
   P=m.block(p);p11,p12,p13=p[0];p21,p22,p23=p[1];p31,p32,p33=p[2]
   explicit=m.block([[a@p11@a+(p21@a).scale((-1,0)),a@p11+a@p12@a+p21.scale((-1,0))+(p22@a).scale((-1,0)),a@p13+p23.scale((-1,0))],[a@p21@a,a@p21+a@p22@a,a@p23],[a2@p31@a,a2@p31+a2@p32@a,a2@p33]])
   M=m.diagonal([a2]*3)@Li@P@L;assert M==explicit and T@(K.power(2)@P@K)@Ti==M
   if n==2:assert P@P==m.eye(3*d) and a@p13+p23.scale((-1,0))!=z
   if n==3:
    assert M==m.block([[a2,z,z],[z,a2,z],[a.power(3),a2,a2]])
    pi2=m.block([[a2,z,z],[z,a2,z],[z,a2,a2]]);pi2inv=m.block([[a.power(-2),z,z],[z,a.power(-2),z],[z,a.power(-2).scale((-1,0)),a.power(-2)]]);assert pi2@pi2inv==m.eye(3*d)
   rows.append({'width':V,'ordinary_case':n,'all_input_columns':3*d})
 out={'status':'PASS_EXACT_ONE_INTERSTAGE_FORMULA_AND_INDEPENDENCE_CONTROLS','cases':rows,'zero_divisor_control':'A conditional active-idle swap is invertible with singular diagonal ordinary blocks; its forbidden low-rank idle-input entry remains nonzero.','independence_control':'P=I+e31 I gives M=[[a²,0,0],[0,a²,0],[a³,a²,a²]], with pi3 rankD but pi2 invertible of rank3D. It is not independent endpoint ranks(3,2,2).','scope':'The universal obstruction is the written row-space proof. Exact finite matrix controls validate its source formula, tensor phases and adversarial cases; they are not independent review.','new_kappa':False};(base/'ONE-INTERSTAGE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
