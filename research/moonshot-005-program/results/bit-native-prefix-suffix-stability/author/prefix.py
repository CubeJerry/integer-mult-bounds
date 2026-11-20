#!/usr/bin/env python3
"""Compute the true isolated preimages on both recorded source stars."""
import argparse,hashlib,json,sys
from pathlib import Path
from collections import Counter
from functools import lru_cache
import numpy as np
import gzip

def prefix(args):
    a=Atlas(args.repo,args.k,args.d_charts,args.library)
    js=(1,8);obs=(0,3,5,6,16,17,18,19)
    graph=json.loads(gzip.decompress(args.weighted.read_bytes()) if args.weighted.suffix==".gz" else args.weighted.read_bytes());cost={tuple(z):0 for z in graph['tree']}
    for e,i,l,x,y,clique,c in graph['closure']: cost[divmod(e,111)]=c
    costs=[cost[i,js[0]]+cost[i,js[1]] for i in obs]
    assert sum(costs)==7
    labels=[(i,d) for i in obs for d,D in enumerate(a.D) if set(js)<=D and i in a.D[a.dual[d]]]
    sizes=Counter(d for i,d in labels)
    assert len(labels)==120 and len(sizes)==45
    AA=[]
    for j in js:
        left=a.left(j);pre={}
        for i in obs:
            ds=[d for d,D in enumerate(a.D) if j in D and i in a.D[a.dual[d]]];assert len(ds)==60
            base=[]
            for d in ds:
                M,ids=a.middle_matrix(d)
                ins=[r for r,t in enumerate(ids) if t in left];outs=[r for r,t in enumerate(ids) if a.route[t][5] in a.ks[i]]
                assert len(ins)==len(outs)==8
                B=np.stack([left[ids[r]] for r in ins])
                base.append(a.ops.matmul(M[np.ix_(outs,ins)],B))
            inverse_total=inv(np.vstack(base))
            for n,d in enumerate(ds):pre[i,d]=inverse_total[:,8*n:8*n+8].T.copy()
        AA.append(np.vstack([pre[k]for k in labels]))
    ranks=list(map(rank_fast,AA))+[rank_fast(np.hstack(AA))]
    assert ranks==[480,480,960]
    r={'donors':js,'receivers':obs,'weights':costs,'ranks':ranks,'matrix_sha256':[hashlib.sha256(x.tobytes()).hexdigest() for x in AA],
       'shared_D_label_multiplicities':dict(sizes),'minimum_h':549,'minimum_label_changes_at_h128':46,
       'minimum_actual_D_nodes_at_h128':next(k for k in range(46) if sum(sorted(sizes.values(),reverse=True)[:k])>=46)}
    other=json.loads((args.out/'RESULT.json').read_text());q={int(k):v for k,v in other['shared_45_D_label_multiplicities'].items()}
    common=sorted(q.keys()&sizes.keys());r['overlap_with_suffix_D']=common
    # If requirements overlap, each changed D counts toward both bounds.
    r['combined_D_count_lower']=r['minimum_actual_D_nodes_at_h128']+13-len(common)
    (args.out/'PREFIX.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','h-author','k','d-charts','weighted','out','fast-author','inverse-library','library'):p.add_argument('--'+n,type=Path,required=True)
    args=p.parse_args();sys.path.insert(0,str(args.h_author));sys.path.insert(0,str(args.fast_author))
    from transfer import Atlas,rank_fast
    from fast import Arithmetic
    inv=Arithmetic(args.inverse_library.resolve()).inverse
    prefix(args)
