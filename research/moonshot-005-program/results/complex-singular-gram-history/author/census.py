#!/usr/bin/env python3
"""Exact authenticated orthogonal-frame census and coupled-four-set witnesses."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from pathlib import Path
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,message):
    if not ok:raise ValueError(message)
def root(v):
    if v.bit_count()==3:return tuple(2 if v>>i&1 else -1 for i in range(9))
    need(v.bit_count()==7,'root normal weight3 or7');zero=[i for i in range(9)if not(v>>i&1)]
    return tuple(3*(int(i==zero[0])-int(i==zero[1]))for i in range(9))
def main(args):
    raw=args.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==NATIVE,'native pin');n=json.loads(gzip.decompress(raw))
    ports=n['live'];v={h:n['frames'][n['initial'][h]][0]for h in ports};byv={z:h for h,z in v.items()}
    H={ports[i]for i in n['hosted']['Dports']};U=sorted(set(ports)-H);vs=[z for z in range(512)if z.bit_count()in(3,7)]
    roots={z:root(z)for z in vs};inner={(a,b):sum(x*y for x,y in zip(roots[a],roots[b]))for a in vs for b in vs}
    masks=[sum(1<<j for j,b in enumerate(vs)if a!=b and inner[a,b]==0)for a in vs]
    frames=[]
    def extend(chosen,available):
        if len(chosen)==8:frames.append([vs[i]for i in chosen]);return
        if available.bit_count()<8-len(chosen):return
        while available:
            bit=available&-available;available^=bit;i=bit.bit_length()-1
            extend(chosen+[i],available&masks[i])
    extend([],(1<<len(vs))-1)
    need(len(vs)==120 and len(frames)==2025,'complete finite root-direction and frame census')
    need(len({tuple(z)for z in frames})==2025,'no duplicate enumerated frames')
    need(all(inner[a,b]==0 for z in frames for a,b in itertools.combinations(z,2)),'every frame is authentically orthogonal')
    native_frames=[sorted(byv[z]for z in frame)for frame in frames if all(z in byv for z in frame)]
    native_census=Counter(len(set(frame)&set(U))for frame in native_frames)
    need(len(native_frames)==759 and native_census==Counter({0:369,1:308,2:80,3:2}),'source-native frame intersections')
    witnesses=[]
    for subset in itertools.combinations(U,4):
        bad=next(((h,j)for h,j in itertools.combinations(subset,2)if inner[v[h],v[j]]),None)
        need(bad is not None,'every four coupled ports contain a nonorthogonal pair')
        witnesses.append({'four_ports':subset,'nonorthogonal_pair':bad,'root_inner_product':inner[v[bad[0]],v[bad[1]]]})
    need(len(witnesses)==70,'all coupled four-subsets covered, independent of full frame census')
    witness=[26,33,40,47,52,57,72,82]
    need(witness in native_frames and set(witness)&set(U)=={40,47,52},'maximal coupled intersection is attained')
    result={'status':'PASS_EXACT_HYBRID_AND_NATIVE_FRAME_CENSUS','native_sha256':NATIVE,
            'normal_by_port':v,'coupled_ports':U,'all_root_frames':frames,'all_native_frames':native_frames,
            'all_root_frame_count':len(frames),'native_frame_count':len(native_frames),
            'actual_native_count_census':dict(Counter(sum(z in byv for z in frame)for frame in frames)),
            'native_frame_coupled_intersection_census':dict(native_census),'maximum_coupled_intersection':3,
            'attaining_native_frame':witness,'coupled_four_subset_obstructions':witnesses,
            'scope':'Exhaustive exact certificate for this pinned finite native source. Enumeration by increasing indices and successive adjacency intersections covers every orthogonal eight-subset exactly once.'}
    payload=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(blob)
    receipt={'status':result['status'],'native_sha256':NATIVE,'certificate_sha256':hashlib.sha256(blob).hexdigest(),
             'all_root_frame_count':len(frames),'native_frame_count':len(native_frames),
             'actual_native_count_census':result['actual_native_count_census'],
             'native_frame_coupled_intersection_census':dict(native_census),'coupled_four_subset_witnesses':70,
             'maximum_coupled_intersection':3}
    args.receipt.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps(receipt,sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--receipt',type=Path,required=True);main(p.parse_args())
