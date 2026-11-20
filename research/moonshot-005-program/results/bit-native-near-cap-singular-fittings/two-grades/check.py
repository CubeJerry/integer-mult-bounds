import argparse,gzip,json
from pathlib import Path
from collections import Counter
from hashlib import sha256

p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--partitions',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=gzip.decompress(a.layout.read_bytes());assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72';v=json.loads(raw)['root_table'][:111];O={(i,j) for i in range(111) for j in range(111) if sum(x*y for x,y in zip(v[i],v[j]))==0};z=json.loads(a.partitions.read_bytes());counts=Counter();sz=[]
for part in z:
 assert sorted(j for S in part for j in S)==list(range(111));sz.append(len(part))
 for S in part:
  for i in S:
   for j in S:
    if i!=j:assert (i,j) in O;counts[i,j]+=1
assert len(z)==2 and max(counts.values())==1 and len(O)==6470
h=Counter(2-counts[e] for e in O);out={'clique_partition_sizes':sz,'rank_of_two_grades':sum(sz),'exact_rank_with_3838_canonical_grades':9*3838+sum(sz),'b':3840,'native_proper_corank_histogram':dict(sorted(h.items())),'all_6470_singular':True};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
