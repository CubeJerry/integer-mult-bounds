#!/usr/bin/env python3
"""Independent actual-root parity-family verification; no author import."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
import argparse,json,gzip,hashlib
def need(x,s):
 if not x:raise ValueError(s)
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','source pin');s=json.loads(gzip.decompress(raw));roots=[[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]] for i in range(111)]
 zero=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))==0
 need(all(any(j!=i and zero(i,j) for j in range(111)) for i in range(111)),'every root line has receiver partner')
 cert=json.loads(a.certificate.read_text())
 def check(configs):
  need(len(configs)==30,'30 groups');total=Counter()
  for group in configs:
   need(len(group)==9,'odd nine frames');inc=Counter()
   for frame in group:
    need(len(frame)==len(set(frame))==8 and all(0<=i<111 for i in frame),'frame indices')
    need(all(not zero(i,j) for i,j in combinations(frame,2)),'identity fitting subframe');inc.update(frame)
   need(sum(inc.values())==72 and all(v%2==0 for v in inc.values()),'even incidence');total.update(inc)
  need(sum(total.values())==2160 and max(total.values())==24,'balanced total');return total
 inc=check(cert['nine_frame_configurations']);controls=[]
 for name,bad in [('missing frame',json.loads(a.certificate.read_text())['nine_frame_configurations']),('duplicate role',json.loads(a.certificate.read_text())['nine_frame_configurations'])]:
  if name=='missing frame':bad[0].pop()
  else:bad[0][0][0]=bad[0][0][1]
  try:check(bad)
  except ValueError:controls.append(name+' rejected')
  else:raise ValueError('invalid certificate accepted')
 need(max(inc.values())>23,'understated incidence rejected');controls.append('incidence23 insufficient')
 need(F(2160-24*8,240)==F(41,5) and F(41,5)-8==F(1,5),'rank and shortening constants')
 # Deleting a vertex changes each incident frame's size, but keeps parity.
 for deleted in [set(),set(range(8)),set(sorted(inc,key=inc.get,reverse=True)[:8]),set(range(111))]:
  lost=sum(inc[i] for i in deleted);remain=sum(len(set(f)-deleted) for g in cert['nine_frame_configurations'] for f in g)
  need(remain==2160-lost and lost<=24*len(deleted),'arbitrary-deletion accounting')
  for g in cert['nine_frame_configurations']:
   cc=Counter(i for f in g for i in f if i not in deleted);need(all(x%2==0 for x in cc.values()),'deleted parity')
 out={'status':'PASS_INDEPENDENT_OPERATOR_SHORTENING_PREMISES','native_sha256':hashlib.sha256(raw).hexdigest(),'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'configurations':30,'frames':270,'total_incidences':2160,'maximum_vertex_incidence':24,'vertex_incidences':dict(inc),'rank_floor':'ceil((9-d/10)V)','q8_shortening_requirement':'ceil(V/5)','negative_controls':controls,'scope':'Exact finite parity premises; universal projector/quotient proofs read independently. Fixed C+U proper-predecessor shortening zero is independently verified in the receiver-geometry review. No general q8 impossibility.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','configurations','frames','maximum_vertex_incidence','q8_shortening_requirement']}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','certificate','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
