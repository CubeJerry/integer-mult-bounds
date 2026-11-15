#!/usr/bin/env python3
"""Independent full28x28 modular determinant check of every native witness."""
import argparse,hashlib,json
from pathlib import Path
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'

def determinant(M,p=101):
 A=[r[:]for r in M];d=1
 for c in range(len(A)):
  k=next((k for k in range(c,len(A))if A[k][c]%p),None)
  if k is None:return 0
  if k!=c:A[k],A[c]=A[c],A[k];d=-d
  x=A[c][c]%p;d=d*x%p;q=pow(x,-1,p)
  for k in range(c+1,len(A)):
   s=A[k][c]*q%p
   for j in range(c,len(A)):A[k][j]=(A[k][j]-s*A[c][j])%p
 return d%p

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);raw=(a.repo/ROOT).read_bytes();R=json.loads(raw)['native_roots'];c=json.loads((a.source/'NO-TWO-COVER.json').read_text());assert hashlib.sha256(raw).hexdigest()==c['native_sha256'];res=[]
 for v in c['rows']:
  i=v['receiver'];drop=v['deleted_coordinate'];ids=v['independent_foreign_roles'];assert R[i][drop]!=0 and len(ids)==len(set(ids))==28
  assert all(j!=i and sum(x*y for x,y in zip(R[i],R[j]))==0 for j in ids)
  M=[]
  for j in ids:
   z=[x for k,x in enumerate(R[j])if k!=drop];M.append([z[k]*z[l]%101 for k in range(7)for l in range(k,7)])
  d=determinant(M);assert d
  bad=M[:];bad[1]=bad[0];assert determinant(bad)==0
  res.append({'receiver':i,'determinant_mod101':d,'rank':28})
 assert len(res)==111
 out={'status':'PASS_INDEPENDENT_ALL111_NO_TWO_SUBSPACE_COVER','certificate_sha256':hashlib.sha256((a.source/'NO-TWO-COVER.json').read_bytes()).hexdigest(),'all111_witnesses':res,'duplicate_row_controls_rejected':111,'real_geometry_consequence':'Each nonzero modular determinant is a nonzero integer minor. No nonzero real homogeneous quadratic vanishes on the entire foreign set, hence no product of two nonzero real linear forms can vanish there.'}
 (a.out/'COVER-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
