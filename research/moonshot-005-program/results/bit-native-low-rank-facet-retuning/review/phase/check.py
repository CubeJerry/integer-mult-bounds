#!/usr/bin/env python3
"""Verify the paid four output gauges on 384 genuine global original-column packets."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np

def verify(a):
    atlas=Atlas(a.repo,a.k_words,a.d_charts,a.library);mm=atlas.ops.matmul
    z=np.load(a.kernel);g=np.load(a.gauges);W=g['W'];Wi=g['actual'] if 'actual' in g.files else g['Winv'];cut=np.load(a.quotient)
    assert list(cut['roles'])==list(range(8))
    w=96;d=192;eye=np.eye(d,dtype=np.uint8);q=384
    X=np.stack([z['one'],z['two']]);assert X.shape==(2,111*w,q)
    assert rank_fast(X.reshape(2*111*w,q))==q
    for A,B in zip(W,Wi):assert np.array_equal(mm(A,B),eye)
    vals=np.zeros((106560,2*q),dtype=np.uint8)
    for j in range(111):
        left=atlas.left(j);ids=[t for t in left if atlas.route[t][4] in atlas.marked]
        src=np.hstack([bank[w*j:w*(j+1)]for bank in X])
        vals[ids]^=mm(np.stack([left[t][:w]for t in ids]),src)
    for d0 in sorted(atlas.marked):
        M,ids=atlas.middle_matrix(d0);vals[ids]=mm(M,vals[ids])
    for ch in atlas.kr.values():
        present=set();updates=[]
        for phase,ins,outs in ch['stripes']:
            if len(ins)!=9:continue
            updates.append((outs,mm(atlas.V[9].T,vals[ins])));present.update(outs)
        for outs,z0 in updates:vals[outs]=z0
        for x,y in ch['early_cache_to_late']:
            if x in present:assert y in present;vals[y]^=vals[x]
    for i in range(111):
        e,E,y,Y=atlas.facet(i);answer=mm(E[:w],vals[e])^mm(Y[:w],vals[y]);old=np.vstack([answer[:,:q],answer[:,q:]])
        new=mm(W[i],old)if i<4 else old
        assert np.array_equal(new,np.vstack([bank[w*i:w*(i+1)]for bank in X])),i
    # Work directly on the squared eight-anchor quotient after genuine local diagonals.
    O=alg.inverse(cut['qe']);K=mm(O,cut['qa']);two=np.zeros((8*d,8*d),dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            block=K[i*w:(i+1)*w,j*w:(j+1)*w]
            for c in range(2):
                r=i*d+c*w;s=j*d+c*w;two[r:r+w,s:s+w]=block
        if i<4:two[i*d:(i+1)*d,i*d:(i+1)*d]^=eye^Wi[i]
    r=rank_fast(two);assert r==8*d-q
    fault=W[0].copy();fault[0]=0;assert rank_fast(fault)==d-1
    info={'source_kernel_columns':q,'all_native_rows_compared':2*111*w,'native_integer_equalities':2*111*w*q,'paired_8_anchor_quotient_rank':r,'physical_total_one_pair':(111-2)*d,'true_gauge_sha256':hashlib.sha256(W.tobytes()).hexdigest(),'zero_row_fault_rank':d-1}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('repo','h-author','fast-author','k-words','d-charts','library','inv-lib','kernel','gauges','quotient','out'):p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();sys.path.insert(0,str(a.fast_author));sys.path.insert(0,str(a.h_author))
    from transfer import Atlas,rank_fast
    from fast import Arithmetic
    alg=Arithmetic(a.inv_lib.resolve());verify(a)
