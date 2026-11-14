"""Complete rank3 threshold15 census; adapted with credit from the admitted scalar17 verifier. Exact bounded integer Gram arithmetic."""
from pathlib import Path
import json,gzip,itertools,hashlib,time
from fractions import Fraction as F
import numpy as np
import argparse,collections
if not __debug__:raise SystemExit("Assertions are required; do not use python -O")
p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--output",type=Path,required=True);args=p.parse_args()
native=args.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';blob=native.read_bytes();assert hashlib.sha256(blob).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
s=json.loads(gzip.decompress(blob));roots=[]
for i in range(111):
 v=[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]];n=sum(x*x for x in v);v=[x*(2 if n==1 else 1) for x in v];assert all(x.denominator==1 for x in v);v=list(map(int,v));assert sum(x*x for x in v)==4;roots.append(v)
R=np.array(roots,dtype=np.int64);D=R@R.T;A=D//2;assert np.all(D%2==0);deg=(D==0).sum(axis=1)
# Every rank-three span has a triple basis from the actual source. Exact Gram determinants and membership, without numerical rank.
triples=np.array(list(itertools.combinations(range(111),3)));flats={};t0=time.time();independent=0
for start in range(0,len(triples),2048):
 ids=triples[start:start+2048];x=A[ids[:,0],ids[:,1]];y=A[ids[:,0],ids[:,2]];z=A[ids[:,1],ids[:,2]];det=8-2*(x*x+y*y+z*z)+2*x*y*z;assert np.all(det>=0);ok=det>0;ids=ids[ok];x=x[ok];y=y[ok];z=z[ok];det=det[ok];independent+=len(ids)
 d0=A[ids[:,0]];d1=A[ids[:,1]];d2=A[ids[:,2]]
 val=(4-z*z)[:,None]*d0*d0+(4-y*y)[:,None]*d1*d1+(4-x*x)[:,None]*d2*d2+2*(y*z-2*x)[:,None]*d0*d1+2*(x*z-2*y)[:,None]*d0*d2+2*(x*y-2*z)[:,None]*d1*d2
 membership=val==2*det[:,None]
 for ids0,m in zip(ids,membership):
  key=np.packbits(m).tobytes()
  if key not in flats:flats[key]=tuple(map(int,ids0))
rows=[]
for key,ids in flats.items():
 V=np.flatnonzero(np.unpackbits(np.frombuffer(key,dtype=np.uint8))[:111]).tolist()
 if len(V)<5:continue
 U=np.flatnonzero(np.all(D[:,ids]==0,axis=1)).tolist()
 for width in [5,6]:
  if width>len(V):continue
  potential=sum(int(deg[i])<=52+width for i in U)
  rows.append({'basis':ids,'flat':V,'width':width,'orthogonal_roots':U,'eligible_count':potential,'total_orthogonal':len(U)})
max3=max(r['eligible_count'] for r in rows)
critical=[r for r in rows if r['eligible_count']>=15]
print('rank3critical',len(critical),flush=True)
args.output.mkdir(parents=True,exist_ok=True)
(args.output/'RANK3-CASES.json').write_text(json.dumps({'independent':independent,'flat_count':len(flats),'width_cases':len(rows),'critical':critical},indent=2)+'\n')
