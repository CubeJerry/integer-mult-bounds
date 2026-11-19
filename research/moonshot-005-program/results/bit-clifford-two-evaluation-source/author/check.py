#!/usr/bin/env python3
"""Exact two-vector visibility and restricted-source Hall certificate."""
from argparse import ArgumentParser
from collections import Counter
from itertools import combinations
from pathlib import Path
import gzip,hashlib,json
import numpy as np
from sympy import Matrix
from search import gf_tables,ranks

def main():
 ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
 ap.add_argument('--basis',type=Path,required=True);ap.add_argument('--witness',type=Path,required=True)
 ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 source=args.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
 raw=gzip.decompress(source.read_bytes());assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
 data=json.loads(raw);roots=data['root_table'];planes=data['A2'];cert=json.loads(args.basis.read_text());wit=json.loads(args.witness.read_text())
 B=Matrix.hstack(*map(Matrix,cert['lattice_basis_columns']));G=B.T*B/2;Bi=B.inv();masks=[]
 for root in roots:
  v=Bi*Matrix(root);assert all(x.q==1 for x in v);masks.append(sum((int(x)&1)<<i for i,x in enumerate(v)))
 polar=[sum((int(G[i,j])&1)<<j for j in range(8)) for i in range(8)]
 def bil(v,w):return sum((polar[i]&w).bit_count() for i in range(8) if v>>i&1)&1
 hyp=cert['hyperbolic_basis_masks'];coords={}
 for c in range(256):
  v=0
  for k in range(8):
   if c>>k&1:v^=hyp[k]
  coords[v]=c
 gamma=np.zeros((256,16,16),dtype=np.uint8)
 for v,c in coords.items():
  for s in range(16):
   for k in range(4):
    if c>>(2*k+int(bool(s>>k&1)))&1:gamma[v,s^(1<<k),s]^=1
 vectors=np.array([wit['v'],wit['w']],dtype=np.uint8);q,poly=wit['q'],wit['polynomial'];assert(q,poly)==(16,19)
 tab,inv=gf_tables(q,poly)
 def evaluation(mats):
  n,t,_,_=mats.shape;out=np.zeros((n,16,2*t),dtype=np.uint8)
  for k in range(16):
   for u in range(2):out[:,:,u*t:(u+1)*t]^=(mats[:,:,:,k]*vectors[u,k]).transpose(0,2,1)
  return out
 local=[]
 for H in planes:
  j,k,l=H;assert masks[j]^masks[k]==masks[l] and bil(masks[j],masks[k])==1
  local.append([np.eye(16,dtype=np.uint8),gamma[masks[j]],gamma[masks[k]],(gamma[masks[j]]@gamma[masks[k]])&1])
 local_eval=evaluation(np.array(local,dtype=np.uint8));single=ranks(local_eval,tab,inv);assert np.all(single==8)
 pair_hist=Counter();pair_count=0;bad_pairs=[];bad_degree_max=0
 for j in range(111):
  hs=[h for h,H in enumerate(planes) if j in H];assert len(hs)==28
  pairs=list(combinations(hs,2));a=np.array([np.concatenate([local_eval[h],local_eval[k]],axis=1) for h,k in pairs])
  rr=ranks(a,tab,inv);pair_hist.update(map(int,rr));pair_count+=len(rr)
  assert np.all(rr<=12)
  bad_degree=Counter()
  for (h,k),r in zip(pairs,rr):
   if r<12:bad_pairs.append([j,h,k,int(r)]);bad_degree[h]+=1;bad_degree[k]+=1
  local_max=max(bad_degree.values(),default=0);bad_degree_max=max(bad_degree_max,local_max)
  assert local_max<=7,(j,local_max)
 visible_hist=Counter();visible_count=0
 for i in range(111):
  adjacent={j for j in range(120) if j!=i and sum(x*y for x,y in zip(roots[i],roots[j]))==0}
  for j in sorted(adjacent&set(range(111))):
   hs=[h for h,H in enumerate(planes) if j in H and set(H)<=adjacent];assert len(hs)==16
   a=np.concatenate([local_eval[h] for h in hs],axis=1)[None,:,:]
   rr=int(ranks(a,tab,inv)[0]);assert rr==16;visible_hist[rr]+=1;visible_count+=1
 fanout=[sum(all(i!=j and sum(x*y for x,y in zip(roots[i],roots[j]))==0 for j in H) for i in range(111)) for H in planes]
 assert max(fanout)<=36
 j=77;normals=[v for v in range(1,256) if (v&masks[j]).bit_count()%2==0]
 hs=[h for h,H in enumerate(planes) if j in H];ks=[masks[next(k for k in planes[h] if k!=j)] for h in hs]
 six_hist=Counter();six_witness=None;six_max=-1
 for a,b in combinations(normals,2):
  if b>=a^b:continue
  count=sum((a&k).bit_count()%2==0 and (b&k).bit_count()%2==0 for k in ks)
  assert count<=12;six_hist[count]+=1
  if count>six_max:six_max=count;six_witness=[a,b]
 assert sum(six_hist.values())==2667 and six_witness is not None
 seven_hist=Counter(sum((a&k).bit_count()%2==0 for k in ks) for a in normals)
 assert sum(seven_hist.values())==127 and max(seven_hist)<=20
 atlas=args.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
 route_raw=gzip.decompress(atlas.read_bytes());assert hashlib.sha256(route_raw).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
 routes=[json.loads(line) for line in route_raw.splitlines()]
 early=Counter((r[1],r[3]) for r in routes if r[0]=='X')
 late=Counter((r[6],r[3]) for r in routes if r[0]=='Y' and r[6] is not None)
 source_types=Counter();late_totals=Counter();extra_total=0
 for j in range(111):
  hs=[h for h,H in enumerate(planes) if j in H];es=[early[j,h] for h in hs]
  assert sum(es)==480 and sum(e//15-1 for e in es)==4
  late_count=0
  for h,e in zip(hs,es):
   l=late[j,h];assert (e,l) in [(15,15),(30,0),(45,0)]
   source_types[e,l]+=1;late_count+=l*8//15;extra_total+=max(0,e*8//15-16)
  late_totals[late_count]+=1
 assert sum(k*v for k,v in late_totals.items())==21400 and extra_total==88
 bad=local_eval.copy();bad[:,:,4:]=0;assert max(ranks(bad,tab,inv))<=4
 result={'status':'PASS_COMMON_TWO_EVALUATION_AND_SOURCE_HALL','field':'GF(16), polynomial x^4+x+1','vectors_shared_by_all_donors':True,
  'A2_rank_histogram':dict(Counter(map(int,single))),'donor_plane_pair_histogram':dict(pair_hist),'plane_pairs_checked':pair_count,
  'rank_below_twelve_pairs':bad_pairs,'maximum_bad_pair_degree':bad_degree_max,
  'native_foreign_visible_histogram':dict(visible_hist),'foreign_pairs_checked':visible_count,'native_plane_fanout_histogram':dict(Counter(fanout)),
  'six_space_control_donor':77,'six_space_control_count':2667,'six_space_H_count_histogram':dict(six_hist),'maximum_six_space_count':six_max,'maximizer_normals':six_witness,
  'seven_space_H_count_histogram':dict(seven_hist),'source_route_type_counts':{str(k):v for k,v in source_types.items()},'late_fields_per_donor_at_b256':dict(late_totals),'extra_early_fields_at_b256_all_donors':88,
  'source_only_compression_field':'GF(256), degree bound <=37 including native early determinant','compressed_rows_per_H':16,'original_matrix_domain':256,
  'minimal_compatible_actual_bank':3840,'actual_atlas_replication':8,'matrix_module_copies':15,
  'D_K_compatibility_proved':False,'literal_source_word_emitted':False,'new_complete_kappa':False,'witness_sha256':hashlib.sha256(args.witness.read_bytes()).hexdigest()}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
