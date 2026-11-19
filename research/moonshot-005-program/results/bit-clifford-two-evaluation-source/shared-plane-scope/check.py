#!/usr/bin/env python3
"""Re-establish the exact old odd witness on unchanged Bstar blocks."""
from argparse import ArgumentParser
from pathlib import Path
from collections import Counter
from hashlib import sha256
import gzip,json

def main():
 ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 p=a.repo/'research/moonshot-005-program/results'
 layout_path=p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
 raw=gzip.decompress(layout_path.read_bytes());assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
 d=json.loads(raw);roots=d['root_table'];planes=list(map(set,d['A2']));i=2
 old=p/'bit-native-plane-asymmetry/author/output/WITNESSES.json.gz';stored=json.loads(gzip.decompress(old.read_bytes()))
 witness=next(w for w in stored['witnesses']if w['receiver']==i);S=set(witness['odd_donors'])
 expected={3,6,7,23,24,27,28,52,53,56,57,66,68,69,71,73,75,78,80,97,99,100,102,103,105,108,110}
 assert S==expected and len(S)==27 and i!=80 and 10 not in S
 native=set(range(111));adj={j for j,r in enumerate(roots)if i!=j and sum(x*y for x,y in zip(roots[i],r))==0}
 assert S<=adj
 visible=[h for h,H in enumerate(planes)if H<=adj];pairs=[]
 for h in visible:
  meet=planes[h]&S;assert len(meet)in[0,2]
  if meet:pairs.append([h,sorted(meet)])
 assert len(pairs)==216 and pairs==witness['paired_planes']
 assert all(sum(j in planes[h]for h in visible)==16 for j in S)
 assert all(len(planes[h]&native)>=2 for h in visible if planes[h]&S)
 # All inherited modified block locations miss the required row/S rectangle.
 assert all(not(i==80 or j==10)for j in S)
 assignment=p/'bit-irreducible-low-excess-target/author/output/ASSIGNMENT.json'
 target=json.loads(assignment.read_text())
 target_result=p/'bit-irreducible-low-excess-target/author/output/RESULT.json';target_meta=json.loads(target_result.read_text())
 assert target_meta['row_center']==80 and target_meta['column_center']==10
 star_adj={a:sorted(j for j in range(111)if a!=j and sum(x*y for x,y in zip(roots[a],roots[j]))==0)for a in [80,10]}
 for b,A in target.items():
  assert A['row_neighbors_in_generator_order']==star_adj[80]
  assert A['column_neighbors_in_transposed_generator_order']==star_adj[10]
 # Deleting a selected donor destroys the required 0-or-2 parity pattern.
 deletion_rejects=0
 for j in S:
  T=S-{j}
  assert any(len(planes[h]&T)==1 for h in visible);deletion_rejects+=1
 proofs=[p/'bit-native-plane-asymmetry/author/PROOF.md',p/'bit-native-plane-asymmetry/ADMISSION.md',p/'bit-irreducible-low-excess-target/author/PROOF.md']
 pins=[layout_path,old,assignment,target_result]+proofs
 result={'status':'PASS_SHARED_PLANE_SOURCE_BSTAR_ODD_WITNESS','receiver':2,'odd_donors':sorted(S),'paired_planes':216,'source_planes_per_donor':16,'all_target_blocks_identity':True,'modified_receiver':80,'modified_donor':10,'donor_deletion_faults_rejected':deletion_rejects,'scope':'common original plane kernels and fixed proper Bstar; no general changed-return exclusion','new_complete_kappa':False,'pins':[{'path':str(x.relative_to(a.repo)),'sha256':sha256(x.read_bytes()).hexdigest()}for x in pins]}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':main()
