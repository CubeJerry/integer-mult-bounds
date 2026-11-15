#!/usr/bin/env python3
"""Exact CZ/CNOT source phases and arbitrary independent input columns."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path(__file__).with_name('ENTANGLING-RESULT.json'));ar=ap.parse_args();base=Path(__file__).parent
 deps=json.loads((base/'DEPENDENCIES.json').read_text())
 for d in deps['sources']:assert hashlib.sha256((ar.repo/d['path']).read_bytes()).hexdigest()==d['sha256']
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sp=importlib.util.spec_from_file_location('entangled_actual',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);Z=m.zero(8);X={v:m.monomial([j^v for j in range(8)],[0]*8)for v in[1,2,4]};C={v:m.M((I.scale((1,1))+X[v].scale((1,-1))).a,1).norm()for v in[1,2,4]}
 P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);D=m.monomial(list(range(8)),[(((x>>1)&1)+2*(x&1)*((x>>2)&1))%4 for x in range(8)]);S=D@P;A=C[2]@S;J=m.monomial([x^((x>>2)&1)for x in range(8)],[(x>>2)&1 for x in range(8)]);R=J@S.power(2)
 assert R==C[1].star()@S@C[2]@S and m.gaussian_rank(R)==0 and A.power(15)==I
 ranks=[m.gaussian_rank(A.power(k))for k in range(15)];assert ranks==[0,1,2,3,3,2,3,3,3,3,2,3,3,2,1]
 traces=[]
 for k in range(15):
  M=A.power(k);v=8 if k==0 else(-4 if k%5==0 else(-2 if k%3==0 else 1));assert sum(M.a[j][j][0]for j in range(8))==v*2**M.k and sum(M.a[j][j][1]for j in range(8))==0;traces.append(v)
 for V in[1,2]:
  a,s,r,si,ca,cb=(M.tp(V)for M in[A,S,R,S.star(),C[1],C[2]]);iv=m.eye(8**V);z=m.zero(8**V)
  assert cb@s==a and si@s==iv and si@ca@r==a and ca@cb@r==a.power(2)
  before=m.diagonal([s,r]);after=m.diagonal([iv,si]);n0=m.block([[cb,z],[iv,ca]]);n1=m.block([[cb,(ca@cb).scale((-1,0))],[z,ca]])
  assert after@n0@before==m.block([[a,z],[iv,a]]) and after@n1@before==m.block([[a,a.power(2).scale((-1,0))],[z,a]])
  assert m.gaussian_rank(a.power(3))==3*V and a.power(15)==iv
 coeff={8:1,7:-1,5:1,4:-1,3:1,1:-1,0:1};poly=Z;poly2=m.zero(64);a2=A.tp(2)
 for k,c in coeff.items():poly=poly+A.power(k).scale((c,0));poly2=poly2+a2.power(k).scale((c,0))
 assert poly==Z and poly2!=m.zero(64)
 total=m.zero(64)
 for k in range(15):total=total+a2.power(k)
 assert total@total==total.scale((15,0)) and sum(total.a[j][j][0]for j in range(64))==120*2**total.k
 assert S@X[2]@S.star()==m.monomial([x^1 for x in range(8)],[2*((x>>2)&1)for x in range(8)])
 assert R!=S.power(2) and C[1]@C[2]@S.power(2)!=A.power(2)
 assert not [ell for ell in range(1,8)if [min(k,15-k,ell)for k in range(15)]==ranks]
 out={'status':'PASS_EXACT_ENTANGLING_ORDER_FIFTEEN_SOURCE','proof_sha256':hashlib.sha256((base/'ENTANGLING-ORDER-FIFTEEN-SOURCE.md').read_bytes()).hexdigest(),'source_proof_sha256':hashlib.sha256((base/'PROOF.md').read_bytes()).hexdigest(),'exact_order':15,'gaussian_power_ranks':ranks,'power_traces':traces,'native_input_column_widths':[1,2],'ordinary_controlled_gauge_verified':True,'cyclic_faithfulness_all_V_at_least':2,'width2_cyclic_projector_rank':8,'single_regular_cyclic_cut_fits':[],'negative_controls':['omitted controlled-X gauge fails','width-one cyclotomic identity fails at width2','ordinary S2 cannot replace R'],'scope':'Exact source and scoped regular-cut obstruction; no profitable caller or new kappa.'}
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
