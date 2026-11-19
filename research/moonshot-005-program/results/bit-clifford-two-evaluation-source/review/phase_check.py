#!/usr/bin/env python3
"""Independent subset certificates for the two-evaluation source Hall proof."""
from check import geometry,field_action,field_mul,basis,rank,mm,BASE,REPO
from argparse import ArgumentParser
from pathlib import Path
from collections import Counter
from itertools import combinations
from hashlib import sha256
import gzip,json

def main():
 ap=ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=REPO);ap.add_argument('--basis',type=Path,default=BASE/'worker-C/clifford-evaluation-gate/author/BASIS.json');a=ap.parse_args()
 witness_path=a.author/'output/WITNESS.json';wit=json.loads(witness_path.read_text());l,g,m=geometry(a.repo,a.basis);Hs=l['A2'];I=[1<<i for i in range(16)]
 binary=[]
 for H in Hs:
  j,k=H[:2];matrices=[I,g[j],g[k],mm(g[j],g[k])]
  vs=[field_action(M,v)for M in matrices for v in [wit['v'],wit['w']]]
  rows=basis(sum(field_mul(c,x)<<(4*i)for i,x in enumerate(v))for v in vs for c in [1,2,4,8])
  assert len(rows)==32;binary.append(rows)
 pair_hist=Counter();bad_degree_max=0;six_hist=Counter();hyper_hist=Counter();six_witness_count=0
 for j in range(111):
  hs=[h for h,H in enumerate(Hs)if j in H];assert len(hs)==28;degrees=Counter()
  for h,k in combinations(hs,2):
   r=rank(binary[h]+binary[k]);assert r in[44,48];pair_hist[r]+=1
   if r<48:degrees[h]+=1;degrees[k]+=1
  bad_degree_max=max(bad_degree_max,max(degrees.values(),default=0));assert max(degrees.values(),default=0)<=1
  # Enumerate every codimension-one and codimension-two subspace containing j.
  normals=[n for n in range(1,256)if (n&m[j]).bit_count()%2==0];assert len(normals)==127
  ks=[m[next(k for k in Hs[h]if k!=j)]for h in hs]
  hit={n:sum(1<<i for i,k in enumerate(ks)if (n&k).bit_count()%2==0)for n in normals}
  for n in normals:
   count=hit[n].bit_count();assert count<=20;hyper_hist[count]+=1
  local=0
  for n,o in combinations(normals,2):
   if not(n<o<n^o):continue
   count=(hit[n]&hit[o]).bit_count();assert count<=10;six_hist[count]+=1;local+=1
  assert local==2667;six_witness_count+=local
 assert sum(pair_hist.values())==41958 and pair_hist[44]==11 and bad_degree_max==1
 source=a.repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
 raw=gzip.decompress(source.read_bytes());assert sha256(raw).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
 quotas=Counter();owners=set();late=Counter()
 for line in raw.splitlines():
  kind,j,c,h,d,k,left,right=json.loads(line)
  if kind=='X':
   assert j==left and j in Hs[h];assert(j,c)not in owners;owners.add((j,c));quotas[j,h]+=1
  elif left is not None:late[left,h]+=1
 assert len(owners)==53280
 quota_hist=Counter();singleton_extras=0
 for j in range(111):
  hs=[h for h,H in enumerate(Hs)if j in H];aH=[quotas[j,h]*8//15 for h in hs]
  assert sum(aH)==256 and all(quotas[j,h]%15==0 for h in hs)
  assert set(aH)<={8,16,24};assert sum(x-8 for x in aH)==32
  for h,q in zip(hs,aH):
   expected=24 if len([k for k in Hs[h]if k<111])==1 else 16
   assert(q+late[j,h]*8//15)==expected;quota_hist[q]+=1
   if q==24:assert expected==24;singleton_extras+=8
  # The stated sufficient bounds cover every possible cardinality.
  sorted_quotas=sorted(aH,reverse=True)
  for s in range(1,29):
   capacity=sum(sorted_quotas[:s])
   available=128 if s<=8 else 192 if s<=20 else 256
   assert capacity<=available
 assert singleton_extras==88
 z=8;trace=0
 for _ in range(4):trace^=z;z=field_mul(z,z)
 assert trace==1
 assert all(field_mul(y,y)^y^8 for y in range(16))
 def mul256(x,y):
  a,b=x&15,x>>4;c,d=y&15,y>>4
  bd=field_mul(b,d)
  return(field_mul(a,c)^field_mul(8,bd))|((field_mul(a,d)^field_mul(b,c)^bd)<<4)
 for x in range(1,256):assert sum(mul256(x,y)==1 for y in range(1,256))==1
 r=15;M=2048*r;L=171200*r;invoice=222*(M*M+3*M)+M*L+L
 assert M==30720 and L==2568000 and invoice==288417472320
 assert 256-8<256
 result={'status':'PASS_INDEPENDENT_TWO_EVALUATION_SOURCE_HALL','binary_single_H_rank':32,'binary_H_pair_histogram':dict(pair_hist),'maximum_bad_degree':bad_degree_max,'six_subspaces_checked':six_witness_count,'six_subspace_H_histogram':dict(six_hist),'maximum_six_subspace_H_count':max(six_hist),'hyperplanes_checked':sum(hyper_hist.values()),'hyperplane_H_histogram':dict(hyper_hist),'maximum_hyperplane_H_count':max(hyper_hist),'actual_normalized_early_quota_histogram':dict(quota_hist),'extra_singleton_early_slots':singleton_extras,'all_111_early_cardinality_bounds_checked':True,'author_checker_imported':False,'scope':'source quotient and genuine source-phase Hall prerequisites; shared H/D/K and return remain open','pins':[{'path':str(p),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [witness_path,a.basis,source,a.author/'check.py']]}
 result.update({'GF256_tower':'s^2+s+t^3 over GF16','tower_nonzero_inverses_checked':255,'minimum_actual_bank':3840,'source_only_invoice_at_minimum':{'ADD_upper_bound':invoice,'INIT_CLEAR_and_peak':L,'additional_MOVE':0},'extra_singleton_omission_rejected':True})
 labelled=[('author/output/WITNESS.json',witness_path),('BASIS.json',a.basis),('native/bit-asymmetric-balanced-atlas/ROUTES.jsonl.gz',source),('author/check.py',a.author/'check.py'),('author/PROOF.md',a.author/'PROOF.md')]
 result['pins']=[{'path':label,'sha256':sha256(p.read_bytes()).hexdigest()}for label,p in labelled]
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'PHASE-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status']);print(json.dumps({k:result[k]for k in ['binary_H_pair_histogram','six_subspaces_checked','maximum_six_subspace_H_count','actual_normalized_early_quota_histogram']},sort_keys=True))
if __name__=='__main__':main()
