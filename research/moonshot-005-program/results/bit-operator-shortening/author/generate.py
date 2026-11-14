#!/usr/bin/env python3
"""Exploratory balanced parity-witness search; final verifier is separate."""
import argparse
import json
import random
from pathlib import Path


def xor(values):
    z=0
    for value in values:z^=value
    return z


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frames',type=Path,required=True)
    ap.add_argument('--parity',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();f=json.loads(args.frames.read_text());v=f['vectors'];frames=f['frames']
    parity=json.loads(args.parity.read_text())['frames_pairwise_REAL_NONorthogonal']
    used=sorted(set(i for row in parity for i in row));lookup={z:i for i,z in enumerate(v)}
    rng=random.Random(771143);pool=[];seen=set();tries=0
    while len(pool)<3000 and tries<300000:
        tries+=1;frame=list(rng.choice(frames));rng.shuffle(frame)
        image_basis=[v[i] for i in frame];image_basis.append(511^xor(image_basis))
        image={i:lookup.get(xor(image_basis[t] for t in range(9) if v[i]>>t&1)) for i in used}
        if any(z is None for z in image.values()):continue
        transformed=sorted(tuple(sorted(image[i] for i in row)) for row in parity)
        key=tuple(transformed)
        if key in seen:continue
        seen.add(key);counts=[0]*111
        for row in transformed:
            for i in row:counts[i]+=1
        pool.append((transformed,counts))
    # Greedy balancing minimises the squared final incidence vector; stop
    # once its maximum gives a useful robust eight-deletion gap.
    chosen=[];load=[0]*111
    for step in range(150):
        idx=min(range(len(pool)),key=lambda k:sum((x+y)**2 for x,y in zip(load,pool[k][1])))
        witness,inc=pool.pop(idx);chosen.append(witness);load=[x+y for x,y in zip(load,inc)]
        if len(chosen)>=30 and max(load)*5<=len(chosen)*4:break
    out={'kind':'balanced_nine_frame_parity_family','witnesses':chosen,
         'count':len(chosen),'incidence_by_role':load,'max_incidence':max(load),
         'trials':tries,'candidate_pool_initial':3000,'source_of_search':'native actual frame enumeration',
         'proof_status':'witness premises require independent native verification; no search completeness claim'}
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'trials':tries,'witnesses':len(chosen),'max_incidence':max(load),
                      'partial_rank_lower_bound':f'(9-{max(load)}/{len(chosen)}) V for at most8deletedports'}))


if __name__=='__main__':main()
