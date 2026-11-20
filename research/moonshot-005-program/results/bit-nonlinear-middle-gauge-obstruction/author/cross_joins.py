#!/usr/bin/env python3
"""Check mixed-receiver/mixed-D partitions for every fixed ordinary donor pair."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
import gzip,importlib.util,itertools,json
from pathlib import Path
import numpy as np

def mod(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def require(v,why):
 if not v:raise ValueError(why)

def main():
 p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--fibres',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--library',type=Path);p.add_argument('--packing-review',type=Path);p.add_argument('--field-review',type=Path);a=p.parse_args();b=a.repo/'research/moonshot-005-program/results';here=Path(__file__).parent
 r=mod(a.packing_review or b/'bit-spread-overlap-source/review/check.py','native');f=mod(a.field_review or b/'bit-spread-h263-source/review/check.py','field');c=mod(here/'census.py','census');elim=c.Elim(f,a.library);n=r.Native(a.repo,f)
 raw=gzip.decompress((here/'PAIR-WITNESSES.json.gz').read_bytes());pin=sha256(raw).hexdigest();require(pin=='1fcf79b047bce11a15fee48a5932bb478f212db1c22cfcab4184796c2e7bd2cb','literal finite witness')
 Q=np.load(a.fibres);M=defaultdict(dict);digest=sha256()
 for v,X in zip(Q['indices'],Q['matrices']):
  d,j,i=map(int,v);M[j][d,i]=X;digest.update(v.astype('>i2').tobytes());digest.update(X.tobytes())
 require(digest.hexdigest()=='c87f3ff6cd51c57af1fe3dd1a444f864631bd146363a92aad17409afe3acb47f' and len(Q['indices'])==74088,'genuine isolated fibre inventory')
 donors=set(range(111))-{0,10,61,62};pairs=set(itertools.combinations(sorted(donors),2));counts=Counter();across=Counter();controls=0
 for idx,(j,k,r0,r1,flags) in enumerate(json.loads(raw)):
  require((j,k) in pairs,'each unordered fixed ordinary donor pair appears once');pairs.remove((j,k));labels=[tuple(v) for v in flags];require(len(labels)==len(set(labels))==12,'twelve labelled receiver/D separators')
  for d,i in labels:require(d in n.marked and j in n.D[d] and k in n.D[d] and i<111 and i!=80 and n.D[d]<=n.adj[i],'both proper native identity equations at the same cut')
  A=np.vstack([M[j][v] for v in labels]);B=np.vstack([M[k][v] for v in labels]);u,v=elim.reduce(A),elim.reduce(B);require(u==r0 and v==r1 and u!=v,'different genuine join cardinalities')
  if idx%127==0:
   require(f.eliminate(A)[0]==u and f.eliminate(B)[0]==v,'independent NumPy native-field reduction');controls+=1
  counts[f'{min(u,v)},{max(u,v)}']+=1;across[len(set(d for d,i in labels))]+=1
 require(not pairs,'complete native conflict clique');out={'native_regular_donors':sorted(donors),'native_regular_donor_count':107,'complete_pairwise_incompatibility_count':5671,'minimum_number_of_fixed_left_star_maps_that_must_change':106,'maximum_unmodified_stars_in_this_family':1,'labels_per_complete_clique_witness':12,'rank_pairs':dict(counts),'distinct_D_counts_per_witness':dict(across),'cross_checked_probe_ranks':controls,'all_native_source_fibre_sha256':digest.hexdigest(),'literal_pair_witness_sha256':pin,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CROSS-JOINS.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(5671,'exact pairwise obstructions;',106,'necessary donor-star changes')

if __name__=='__main__':main()
