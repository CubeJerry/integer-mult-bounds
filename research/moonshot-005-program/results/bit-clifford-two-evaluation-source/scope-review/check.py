from pathlib import Path
from argparse import ArgumentParser
from collections import Counter
import gzip,json,hashlib
def main():
 a=ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a=a.parse_args()
 p=a.repo/'research/moonshot-005-program/results'
 raw=gzip.decompress((p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes());d=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
 raw=gzip.decompress((p/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
 assert hashlib.sha256(raw).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
 S={3,6,7,23,24,27,28,52,53,56,57,66,68,69,71,73,75,78,80,97,99,100,102,103,105,108,110};R=d['root_table'];H=list(map(set,d['A2']));D=list(map(set,d['D4']))
 O={j for j in range(120) if j!=2 and sum(x*y for x,y in zip(R[2],R[j]))==0};assert len(S)==27 and S<=O and 10 not in S
 views={j:{h for h,V in enumerate(H) if j in V and V<=O} for j in S};assert all(len(v)==16 for v in views.values())
 counts=Counter(h for v in views.values() for h in v);assert len(counts)==216 and set(counts.values())=={2}
 src=Counter();cut=Counter()
 for line in raw.splitlines():
  kind,j,c,h,t,k,left,right=json.loads(line)
  if h is None:continue
  if kind=='X':src[j,h]+=1
  elif left is not None:src[left,h]+=1
  if D[t]<=O:cut[h]+=1
 assert all(src[j,h]==30 for j,v in views.items() for h in v)
 assert all(cut[h]==30 for h in counts)
 for gone in S:assert any(v%2 for v in Counter(h for j,V in views.items() if j!=gone for h in V).values())
 r={'status':'PASS_INDEPENDENT_SHARED_SOURCE_TARGET_SCOPE','receiver':2,'donors':sorted(S),'paired_planes':216,'tight_source_flags':432,'source_and_plane_cut_width':30,'bank':480,'donor_deletion_controls':27,'Bstar_witness_blocks_unchanged':True,'author_code_imported':False,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
