import argparse,collections,gzip,hashlib,json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
FRAMES=[[2,10,13,25,41,51,62,106],[2,25,37,41,81,92,106,110],[4,7,13,28,31,46,70,109],[4,27,32,37,83,94,100,106],[5,7,20,29,35,53,72,100],[5,27,31,41,84,94,98,110],[10,28,44,53,83,89,98,109],[20,41,46,72,81,89,92,106],[29,32,35,44,51,62,70,84]]
def main(a):
 raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP;s=json.loads(gzip.decompress(raw));H=[s['live'][i] for i in s['hosted']['Dports']];normal={h:s['frames'][s['initial'][h]][0] for h in H}
 def root(h):
  n=normal[h];t=[i for i in range(9) if n>>i&1]
  if len(t)==3:return [2 if i in t else -1 for i in range(9)]
  assert len(t)==7;z=[i for i in range(9) if i not in t];return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
 R={h:root(h) for h in H};dot=lambda x,y:sum(v*w for v,w in zip(x,y))
 def check(frames):
  if len(frames)%2!=1:return False
  counts=collections.Counter()
  for f in frames:
   if len(f)!=8 or len(set(f))!=8 or not set(f)<=set(H):return False
   if any(dot(R[i],R[j])!=18*int(i==j) for i in f for j in f):return False
   counts.update(f)
  return all(c%2==0 for c in counts.values())
 assert check(FRAMES);counts=collections.Counter(h for f in FRAMES for h in f);assert len(FRAMES)==9 and set(counts.values())=={2,4} and sum(counts.values())==72
 bad=[f.copy() for f in FRAMES];bad[0][0]=bad[0][1];assert not check(bad)
 bad=[f.copy() for f in FRAMES];bad[0][0]=0;assert not check(bad)
 assert not check(FRAMES[:-1])
 out={'status':'PASS_EXACT_CHAR2_NINE_FRAME_CERTIFICATE','source_sha256':SP,'source_set':'hosted96 of complex native','frames_by_native_role':FRAMES,'frames_by_binary_normal':[[normal[h] for h in f] for f in FRAMES],'orthogonality_checks':576,'distinct_used_source_roots':len(counts),'root_multiplicities_by_role':dict(sorted(counts.items())),'q':9,'rank_bound_every_volume':'rank(K)>=9V in characteristic2','full104_bound':'Same bound by hosted96 principal restriction.','negative_controls':{'duplicate_ray_in_frame_rejected':True,'single_incidence_change_rejected':True,'one_frame_removed_rejected':True},'scope':'Same fixed complex-source forbidden-zero graph and identity V-block diagonals; every char2 field and V. This is not a statement about the distinct actual BIT native.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','distinct_used_source_roots','q','rank_bound_every_volume']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
