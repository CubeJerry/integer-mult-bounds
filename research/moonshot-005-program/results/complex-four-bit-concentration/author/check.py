#!/usr/bin/env python3
"""Exact concentration, K embedding, and complete Gaussian invoice controls."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());args=ap.parse_args();base=Path(__file__).parent
hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';sp=importlib.util.spec_from_file_location('conc_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
N=16;e=m.eye(N);x=m.monomial([j^2 for j in range(N)],[0]*N);cb=m.M((e.scale((1,1))+x.scale((1,-1))).a,1).norm();p=m.monomial([(j>>1)|((j&1)<<3)for j in range(N)],[0]*N);df=m.monomial(list(range(N)),[2*int(j&13==13)for j in range(N)]);A=cb@df@p;checks=[]
for V in[1,2]:
 a=A.tp(V);I=m.eye(N**V);Z=m.zero(N**V);neg=lambda g:g.scale((-1,0));L=m.block([[a,Z],[I,a]]);U=m.block([[a,neg(a.power(2))],[Z,a]])
 expected=m.block([[Z,neg(a.power(4))],[a.power(2),Z]]);assert L@U@L==expected
 swap=m.block([[Z,I],[I,Z]]);sign=m.diagonal([neg(I),I]);assert sign@expected@swap==m.diagonal([a.power(4),a.power(2)])
 if V==1:
  scalar=lambda data:m.block([[I.scale((v,0))if v else Z for v in row]for row in data])
  T=scalar([[0,0,1],[1,0,-1],[1,1,-1]]);Ti=scalar([[1,1,0],[0,-1,1],[1,0,0]]);J=scalar([[0,1,0],[1,0,0],[0,0,1]]);P0=scalar([[1,1,0],[-1,0,1],[0,1,0]])
  assert T@Ti==m.eye(3*N) and Ti@J==P0
  K0=m.block([[I,Z,a+neg(I)],[a,Z,neg(a)],[I,I,neg(I)]]);K2=m.block([[neg(a.power(2)),Z,a+a.power(2)],[a,Z,neg(a)],[I,I,neg(I)]])
  target=m.block([[Z,neg(a.power(4)),Z],[a.power(2),Z,Z],[Z,Z,I]])
  assert J@K0@P0@K2@P0@K0@Ti@J==target
  assert J@K0@K2@K0@Ti@J!=target
 checks.append({'V':V,'two_role_matrix_dimension':2*N**V,'all_columns':True,'source_embedding_checked':V==1})
scale=10**40
def rootlo(n):
 z=n**199*scale**200;lo=0;hi=n*scale+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=z:lo=mid
  else:hi=mid
 assert lo**200<=z<(lo+1)**200
 return lo
vals={r:rootlo(r)for r in[7,8,21,22,23,24,25]}
def margin(target,roles,query=0):
 plo=(3+query)*scale+3*(roles-1)*vals[7]+3*vals[8];phi=plo+3*roles
 tl=sum(vals[r]for r in target);th=tl+len(target)
 return {'lo':str(tl-phi),'hi':str(th-plo),'scale':str(scale)}
prices={'two_role42':margin([25,23],2),'three_role420':margin([25,23,21],3),'two_role43_with_paid_query':margin([25,24],2,1),'three_role421_with_paid_query':margin([25,23,22],3,1)}
assert all(int(v['hi'])<0 for v in prices.values())
result={'status':'PASS_EXACT_FOUR_BIT_CONCENTRATION_BASE','width_checks':checks,'head_endpoint':[4,2],'retained_idle_extension':[4,2,0],'source_and_endpoint_monomial_services':12,'source_and_endpoint_recipe':{'coordinate_SWAPS':26,'Toffoli':6,'phase_passes':12},'ordinary_base_invoice':{'native_add_subtract':3,'input_bank_SWAP':1,'output_unit_sign':1},'gaussian_margin_intervals':prices,'negative_controls':{'omitted_P0_factors_rejected':True,'paid_query_repairs_fail_price':True},'universal_last_interstage_gate':'Written pi0/pi1/pi3 block-rank proof, not a finite search conclusion','no_profitable_caller':True,'new_kappa':False};(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
