#!/usr/bin/env python3
"""Exact independent source-row and two-sector dimension controls for the gate."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
PINS={'PROOF.md':'5eb77f12da9888d1efddf7ba444be788b9ab93b3652700775d3b464da34715ab','check.py':'cdd364c868ec12af8f735b0a78235cb82a5ff713ae6af33897c6677010cd67a8','RESULT.json':'d63476f60f1cbb61f7128120856360947f3b6feb1358819e27999640bca0b01d'}

def run(repo,positive,out):
 for name,h in PINS.items():assert hashlib.sha256((positive/name).read_bytes()).hexdigest()==h,name
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('prefix_column_gate_exact',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 def half(x):return m.M(x.a,x.k+1).norm()
 def tab(n,dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(n)]) for x in range(1<<n)],[phase(*[(x>>k)&1 for k in range(n)])%4 for x in range(1<<n)])
 i4=m.eye(4);i16=m.eye(16);xs=tab(2,lambda s,t:(s^1)+2*t,lambda s,t:0);xt=tab(2,lambda s,t:s+2*(t^1),lambda s,t:0);zs=tab(2,lambda s,t:s+2*t,lambda s,t:2*s);zt=tab(2,lambda s,t:s+2*t,lambda s,t:2*t)
 R=tab(4,lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);xb=m.monomial([x^2 for x in range(16)],[0]*16);a0=half(i16.scale((1,1))+xb.scale((1,-1)))@R
 s10=tab(4,lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0);g0=tab(4,lambda a,b,c,d:c+2*b+4*a+8*d,lambda a,b,c,d:0)
 reports=[]
 for W in [0,1]:
  tail=m.eye(16**W);I=m.eye(4*16**W);Z=m.zero(4*16**W);a=i4.tensor(a0.tp(W));T=zt.tensor(tail);X=xt.tensor(tail);S1=zs.tensor(s10.tp(W));G=xs.tensor(g0.tp(W));P=half(I+T);N=half(I+T.scale((-1,0)));P1=half(I+S1);N1=I+P1.scale((-1,0));w=X@G@P@P1;z=X@P@N1
  assert P@N==Z and a@P==P@a and a@N==N@a and w.star()@w==P@P1
  assert N@N==N and (P@P1)@(P@P1)==P@P1 and N@P@P1==Z
  n=N.trace()[0];quarter=(P@P1).trace()[0];D=I.n;assert n==D//2 and quarter==D//4
  # pi L C U=(0,0,P) uses only this literal third source row.
  assert P@N@a==P@N@a@a==Z and P@P==P
  assert z@N==w@N==z@P@P1==Z and w@P@P1==w
  kn=a@N;aw=a@w;assert kn.star()@kn==N and aw.star()@aw==P@P1
  # The two image sectors occupy disjoint output row supports. Their combined
  # Gram support is N+P P1, of rank3D/4; the active part has Gram2 P P1.
  support=N+P@P1;assert support@support==support and support.trace()[0]==3*D//4
  reports.append({'tail_width':W,'reduced_bank_dimension':D,'required_linear_projection_rank':D//2,'forced_kernel_sector_ranks':[n,quarter],'forced_total_linear_rank':5*D//4,'available_linear_rank':D,'strict_defect':D//4,'source_row_identity':True})
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_FIXED_PREFIX_COLUMN_ENDPOINT_DIMENSION_GATE','scope':'all ordinary completions of pinned last column under fixed finite prefix/tail catalogue and faithful rank-class separation','positive_units_and_exact_column_preserved':True,'all_width_kernel_fraction':'3/4','available_kernel_fraction':'1/2','required_linear_encoder_fraction':'5/4','width_controls':reports,'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');manifest={'engine':ENGINE,'engine_sha256':SHA,'positive_package_pins':PINS,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json']}};(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],'required5D/4> D')

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--positive',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();run(args.repo,args.positive,args.out)
