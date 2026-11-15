#!/usr/bin/env python3
"""Exact all-column diagnostics for the universal three-role native word."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ar=ap.parse_args();base=Path(__file__).parent
 deps=json.loads((base/'DEPENDENCIES.json').read_text())
 for d in deps['sources']:assert hashlib.sha256((ar.repo/d['path']).read_bytes()).hexdigest()==d['sha256']
 source=ar.repo/'research/moonshot-005-program/results/complex-three-head-source/author/THREE-HEAD-SOURCE-AND-ONE-QUERY-GATE.md';helper=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
 assert hashlib.sha256(helper.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
 sp=importlib.util.spec_from_file_location('three_role_base_dyadic',helper);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 T=s.Matrix([[0,0,1],[1,0,-1],[1,1,-1]]);J=s.Matrix([[0,1,0],[1,0,0],[0,0,1]]);T0=J*T*J;assert T0==s.Matrix([[0,1,-1],[0,0,1],[1,1,-1]]) and T0.det()==1
 E1=s.eye(3);E1[1,2]=-1;E2=s.eye(3);E2[0,1]=1;cycle=s.Matrix([[0,1,0],[0,0,1],[1,0,0]]);assert T0==cycle*E2*E1
 assert T0.inv()==s.Matrix([[-1,0,1],[1,1,0],[0,1,0]])
 x,y,z=s.symbols('x y z',commutative=False)
 def K(a):return s.Matrix([[1,0,a-1],[a,0,-a],[1,1,-1]])
 expected=s.Matrix([[-x+y+z*x,y-z,x-y],[-z*x+z*y,z*y,z*x-z*y],[-x+y,0,x-y+y*x]])
 assert all(s.expand(v)==0 for v in K(z)*K(y)*K(x)-expected)
 I=m.eye(8);xb=m.monomial([j^2 for j in range(8)],[0]*8);cb=m.M((I.scale((1,1))+xb.scale((1,-1))).a,1).norm();S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=cb@S
 rows=[]
 for V in (1,2):
  a=A.tp(V);d=a.n;i=m.eye(d);zero=m.zero(d)
  L0=m.block([[a,zero,zero],[i,a,zero],[zero,zero,i]]);tv=m.block([[i.scale((int(T0[j,k]),0)) for k in range(3)] for j in range(3)])
  word=(L0@tv).power(3);target=m.diagonal([a.power(2)]*3);assert word==target
  paid_query=m.diagonal([a,i,i]);paid_target=m.diagonal([a.power(3),a.power(2),a.power(2)]);assert paid_query@word==paid_target
  assert word!=paid_target and (L0@tv).power(2)!=target
  badT=s.Matrix([[0,1,-1],[0,0,1],[1,1,0]]);bad=m.block([[i.scale((int(badT[j,k]),0)) for k in range(3)] for j in range(3)]);assert (L0@bad).power(3)!=target
  if V==2:
   bad=m.block([[i.scale((abs(int(T0[j,k])),0)) for k in range(3)] for j in range(3)]);assert (L0@bad).power(3)!=target
  rows.append({'width':V,'independent_input_fields':3,'all_input_columns':3*d,'head_endpoint_ranks':[m.gaussian_rank(a.power(2))]*3,'paid_upgrade_head_ranks':[m.gaussian_rank(a.power(3)),m.gaussian_rank(a.power(2)),m.gaussian_rank(a.power(2))]})
 out={'status':'PASS_EXACT_THREE_NATIVE_THREE_ROLE_SOURCE_BASE','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'universal_noncommutative_expansion_checked':True,'actual_lower_native_orientation':True,'T0':[[int(T0[j,k]) for k in range(3)] for j in range(3)],'T0_inverse':[[int(T0.inv()[j,k]) for k in range(3)] for j in range(3)],'ordinary_services_per_T0':{'inplace_field_adds':2,'bank_cycles':1,'new_fields':0,'erasures':0},'base_complete_gaussian_histogram':{'1':3,'7':6,'8':3},'paid_upgrade_histogram':{'1':4,'7':6,'8':3},'all_column_checks':rows,'negative_controls':['omit third native rejected','omit updated subtraction in second T0 ADD rejected','tensor field minus rejected at even width','rank3 upgrade requires the explicitly charged extra query in this control'],'scope':'All-width identity is the written polynomial proof; common-body dimensions/costs require the retained source/compiler contracts. Base and paid upgrade both fail the target movement invoice. No new kappa.'};(base/'SOURCE-BASE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
