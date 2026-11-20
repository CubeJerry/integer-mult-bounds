#!/usr/bin/env python3
"""Verify the paid four output gauges on 460 genuine global original-column packets."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np

def verify(a):
    atlas=Atlas(a.repo,a.k_words,a.d_charts,a.library);mm=atlas.ops.matmul
    z=np.load(a.kernel);g=np.load(a.controls);W=g['W'];Wi=g['Winv']
    w=96;d=192;eye=np.eye(d,dtype=np.uint8);q=460
    controls=np.load(a.controls);act=controls['factor'];owners={}
    X=np.stack([z['one'],z['two']]);assert X.shape==(2,111*w,q)
    assert rank_fast(X.reshape(2*111*w,q))==q
    for A,B in zip(W,Wi):assert np.array_equal(mm(A,B),eye)
    vals=np.zeros((106560,2*q),dtype=np.uint8);eligible=set()
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
            updates.append((outs,mm(atlas.V[9].T,vals[ins])));present.update(outs);eligible.update(outs)
        for outs,z0 in updates:vals[outs]=z0
        for x,y in ch['early_cache_to_late']:
            if x in present:assert y in present;vals[y]^=vals[x]
    for i in range(111):
        e,E,y,Y=atlas.facet(i);answer=mm(E[:w],vals[e])^mm(Y[:w],vals[y]);old=np.vstack([answer[:,:q],answer[:,q:]])
        if i<6:
            early=[x for x in e if x in eligible];late=[x for x in y if x in eligible]
            assert len(early)==72 and len(late)==96
            assert late==list(controls['y'+str(i)]) and early==list(controls['e'+str(i)])
            input_rows=vals[early+late];coupled=np.vstack([input_rows[:,:q],input_rows[:,q:]])
            old^=mm(act[i],mm(controls[f'phi{i}'],coupled))
            owners[i]={'early':early,'late':late}
        new=mm(W[i],old)if i<4 else old
        assert np.array_equal(new,np.vstack([bank[w*i:w*(i+1)]for bank in X])),i
    info={'new_independent_global_null_columns':q,'true_source_rows_in_two_copies':2*111*w,'independently_checked_integer_coefficients':2*111*w*q,'six_genuine_visitor_orders_sha256':hashlib.sha256(json.dumps(owners,sort_keys=True).encode()).hexdigest(),'source_kernel_sha256':[hashlib.sha256(v.tobytes()).hexdigest()for v in X]}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('repo','h-author','k-words','d-charts','library','kernel','controls','out'):p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();sys.path.insert(0,str(a.h_author))
    from transfer import Atlas,rank_fast
    verify(a)
