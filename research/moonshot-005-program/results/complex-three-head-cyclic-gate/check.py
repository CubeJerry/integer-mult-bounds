#!/usr/bin/env python3
"""Exact diagnostics; the all-width conservation theorem is the written proof."""
import argparse,hashlib,importlib.util,json,sys
import sympy as sym
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ar=ap.parse_args();base=Path(__file__).parent
 deps=json.loads((base/'DEPENDENCIES.json').read_text())
 for s in deps['sources']:assert hashlib.sha256((ar.repo/s['path']).read_bytes()).hexdigest()==s['sha256']
 helper=ar.repo/deps['sources'][-1]['path'];sp=importlib.util.spec_from_file_location('cyclic_dyadic_helper',helper);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);Xb=m.monomial([j^2 for j in range(8)],[0]*8);Cb=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm();S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=Cb@S
 Z=m.monomial([j^7 for j in range(8)],[0]*8);assert A.power(6)==Z and A.power(12)==I and Z!=I
 ranks=[]
 for k in range(12):
  B=A.power(k);rowcounts=[sum(v!=(0,0) for v in row) for row in B.a];assert len(set(rowcounts))==1
  r=rowcounts[0].bit_length()-1;assert 2**r==rowcounts[0];ranks.append(r)
 assert ranks==[0,1,2,3,2,1]*2
 for j in range(12):
  for k in range(j):assert all(A.power(j)!=A.power(k).scale(u) for u in [(1,0),(0,1),(-1,0),(0,-1)])
 def rank(M):return sym.Matrix([[x+sym.I*y for x,y in row] for row in M.a]).rank()
 R=m.monomial([(j+1)%6 for j in range(6)],[0]*6);P=m.monomial(list(range(6)),[0,0,0,2,2,2]);E=R+ (P@R@P).scale((-1,0));assert rank(E)==2
 diffranks=[]
 for k in range(12):
  X=R.power(k);dr=rank(X+(P@X@P).scale((-1,0)));assert dr==2*ranks[k];diffranks.append(dr)
 assert R.power(6)==m.eye(6) and P@R.power(6)==R.power(6)@P
 Y=P@R@P;F=R.power(2)+Y.power(2).scale((-1,0));assert F==R@E+E@Y
 Q=m.block([[E,F.scale((-1,0))],[m.zero(6),E]]);assert rank(Q)==4
 source_checks=[]
 for V in (1,2):
  a=A if V==1 else A.tp(2);z=Z if V==1 else Z.tp(2);d=a.n;i=m.eye(d);zero=m.zero(d)
  low=m.block([[a,zero],[i,a]]);swap=m.block([[zero,i],[i,zero]]);L=m.block([[a,i],[zero,a]]);assert swap@low@swap==L
  U=m.block([[a,a.power(2).scale((-1,0))],[zero,a]]);Ui=m.block([[a.star(),i],[zero,a.star()]]);assert U@Ui==m.eye(2*d)
  assert a.power(6)==z and z!=i
  if V==2:
   wrong=A.power(2).scale((-1,0)).tp(2);assert wrong!=a.power(2).scale((-1,0))
  source_checks.append({'width':V,'all_columns':2*d,'role_swap_actual_lower_half':True,'physical_inverse_identity_only':True,'nontrivial_sixth_power':True})
 out={'status':'PASS_EXACT_THREE_HEAD_CYCLIC_CONSERVATION_DIAGNOSTICS','power_gaussian_ranks':ranks,'auxiliary_difference_ranks':diffranks,'native_auxiliary_difference_rank':4,'all_column_source_checks':source_checks,'negative_controls':['A^6 replaced by identity rejected at widths1,2','field minus tensoring rejected at width2'],'proof_scope':'C[A^6] ordinary interstages and cyclic Gaussian endpoint/query powers; all-width result is written tensor separation plus exact rank telescoping','dependency_helper_reuse':'Exact dyadic arithmetic only; these author checks are not independent review','new_kappa':False}
 (base/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
