#!/usr/bin/env python3
"""Construct exact native return submatrices in the physical field basis."""
import argparse
import ctypes
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

def digest(a):
    h=hashlib.sha256()
    for row in a:h.update(row.tobytes())
    return h.hexdigest()

def rank_certificate(a,mod,field):
    h,w=a.shape
    inv=np.array([0]+[int(np.flatnonzero(field[j]==1)[0]) for j in range(1,64)],dtype=np.uint8)
    rows=np.empty(h,dtype=np.uint32);cols=np.empty(min(h,w),dtype=np.uint32);diag=np.empty(min(h,w),dtype=np.uint8)
    f=ctypes.CDLL(str(Path(mod).resolve())).exact_rank
    ptr=ctypes.c_void_p;f.argtypes=[ptr,ctypes.c_size_t,ctypes.c_size_t,ptr,ptr,ptr,ptr,ptr];f.restype=ctypes.c_size_t
    rk=f(a.ctypes.data,h,w,field.ctypes.data,inv.ctypes.data,rows.ctypes.data,cols.ctypes.data,diag.ctypes.data)
    det=1
    for z in diag[:rk]:det=int(field[det,z])
    return {'rank':rk,'pivot_minor_determinant_GF64':det,'selected_rows':rows[:rk].tolist(),'pivot_columns':cols[:rk].tolist()}

def main():
    p=argparse.ArgumentParser()
    for f in ('repo','transfer','k_words','d_charts','mult','rank_lib','out'):
        p.add_argument('--'+f.replace('_','-'),type=Path,required=True,dest=f)
    p.add_argument('--mode',choices=('disjoint','all'),default='disjoint')
    p.add_argument('--sector',choices=('small','large'),required=True)
    p.add_argument('--count',type=int,default=12);p.add_argument('--build-only',action='store_true')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(a.transfer.resolve()))
    from transfer import Atlas,TABLE
    atlas=Atlas(a.repo,a.k_words,a.d_charts,a.mult)
    if a.mode=='all':left=right=list(range(111))
    else:
        if not 1<=a.count<=55:raise ValueError('disjoint size')
        left=list(range(a.count));right=list(range(111-a.count,111))
    small=a.sector=='small';sl=slice(0,96) if small else slice(96,480)
    alt=slice(96,480) if small else slice(0,96)
    width=96 if small else 384;size=len(left)*width
    matrix=np.memmap(a.out/'M.raw',dtype=np.uint8,shape=(size,size),mode='w+')
    lc={j:atlas.left(j) for j in right};rc={i:atlas.right(i) for i in left}
    atlas.left=lc.__getitem__;atlas.right=rc.__getitem__;pairs=0
    for ri,i in enumerate(left):
        for cj,j in enumerate(right):
            block=matrix[ri*width:(ri+1)*width,cj*width:(cj+1)*width]
            if i==j:
                block[:]=np.eye(width,dtype=np.uint8);continue
            if j not in atlas.orth[i]:continue
            pairs+=1;R,D,L=atlas.factors(i,j)
            ds=[d for d,S in enumerate(atlas.D) if j in S and i in atlas.D[atlas.dual[d]]]
            ix=[x for x,d in enumerate(ds) if (d in atlas.marked)==small]
            other=[x for x,d in enumerate(ds) if (d in atlas.marked)!=small]
            if len(ix)*8!=width:raise ValueError('sector dimensions')
            l=L.reshape(60,8,480);r=R.T.reshape(60,8,480)
            if np.any(l[ix,:,alt]) or np.any(r[ix,:,alt]) or np.any(l[other,:,sl]) or np.any(r[other,:,sl]):
                raise ValueError('cross-component transfer')
            middle=np.vstack([atlas.ops.matmul(D[x],l[x,:,sl]) for x in ix])
            block[:]=atlas.ops.matmul(r[ix,:,sl].reshape(width,width).T,middle)
        if ri%10==0:print('generated roles',ri+1,'of',len(left),flush=True)
    matrix.flush()
    result={'rows':left,'columns':right,'mode':a.mode,'sector':a.sector,'width':width,'size':size,'foreign_pairs':pairs,'matrix_sha256':digest(matrix)}
    if not a.build_only:result.update(rank_certificate(matrix,a.rank_lib,TABLE))
    (a.out/'RESULT.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print({k:v for k,v in result.items() if not isinstance(v,list)},flush=True)

if __name__=='__main__':main()
