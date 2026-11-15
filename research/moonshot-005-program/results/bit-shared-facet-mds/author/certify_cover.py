"""Exact finite certificates excluding two proper real subspaces at every port."""
import json,hashlib,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];out=[]
for i,r in enumerate(R):
 drop=next(k for k,v in enumerate(r)if v);basis={};ids=[];det=1
 for j,x in enumerate(R):
  if j==i or sum(a*b for a,b in zip(r,x))!=0:continue
  z=[v for k,v in enumerate(x)if k!=drop];v=[z[a]*z[b]%101 for a in range(7)for b in range(a,7)]
  for pivot,w in sorted(basis.items()):
   factor=v[pivot];v=[(a-factor*b)%101 for a,b in zip(v,w)]
  if any(v):
   pivot=next(k for k,x in enumerate(v)if x);det=det*v[pivot]%101;inv=pow(v[pivot],-1,101);basis[pivot]=[x*inv%101 for x in v];ids.append(j)
 assert len(basis)==28
 out.append({'receiver':i,'deleted_coordinate':drop,'independent_foreign_roles':ids,'quadratic_rank_mod101':28,'elimination_pivot_product_mod101':det})
r={'status':'PASS_ALL111_NO_TWO_PROPER_SUBSPACE_COVERS','native_sha256':hashlib.sha256(raw).hexdigest(),'prime':101,'proof':'Deleting any coordinate where r_i is nonzero identifies F_i with R^7. The28 independent degree2 evaluation rows modulo101 give rational rank28. A product of two nonzero linear forms cannot vanish on every foreign root.','rows':out};(Path(__file__).parent/'NO-TWO-COVER.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS111 rank28 certificates')
