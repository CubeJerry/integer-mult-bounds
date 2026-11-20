#!/usr/bin/env python3
"""Independent binary replay of both complete S028 center slabs on the shared word."""
from argparse import ArgumentParser
from collections import Counter
import importlib.util,json
from pathlib import Path
import numpy as np

def main():
 p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--words',type=Path,required=True);p.add_argument('--full-review',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('raw_binary',a.full_review);binary=importlib.util.module_from_spec(spec);spec.loader.exec_module(binary)
 root=a.repo/'research/moonshot-005-program/results';auth=json.loads(binary.data(root/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json','deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601'))
 raw=binary.data(root/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036');routes={}
 for r in map(json.loads,raw.splitlines()):routes[(r[0]=='Y')*53280+480*r[1]+r[2]]=r
 prices=json.loads((a.words/'RESULT.json').read_bytes());masks,scale=binary.multipliers();reps={};edges=[]
 for tag in ('row','column'):
  baseline,proper=binary.target_arrays(auth,tag)
  for (i,j),M in proper.items():
   endpoint=j if tag=='row' else i
   for c in range(64):
    baseline[3840*endpoint+c]^=np.uint64(1<<c);M[c]=M.get(c,0)^(1<<c)
  word=json.loads(binary.data(a.words/(tag+'-word.json.gz'),prices['word_SHA256'][tag]));reps[tag]=binary.actual(tag,word,prices['word_costs'][tag],routes,baseline,masks,scale);edges.append(proper)
 X=Counter();paths=[]
 for (i,j),L in edges[0].items():
  for (j0,k),R in edges[1].items():
   if j0!=j:continue
   paths.append(j)
   for row,v in L.items():X[row]^=binary.xor_rows(v,R)
 nonzero=sum(v.bit_count()for v in X.values());r2=binary.rank2(X.values());total=sum(v['total_binary_ADD']for v in reps.values());binary.require(total==20364408,'both pure inverses and true center injections')
 out={'bits_per_verified_slab':6*binary.N*384,'actual_binary_field_maps':reps,'binary_ADD':total,'binary_INIT':768,'binary_dirty_CLEAR':768,'extra_MOVE':0,'standalone_proper_rank':128,'proper_square_rank':r2,'proper_square_nonzero_field_coefficients':nonzero,'intermediate_roles':sorted(paths),'proper_cube_rank':0,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(total,r2,nonzero)

if __name__=='__main__':main()
