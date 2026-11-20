#!/usr/bin/env python3
"""Solve the ordinary and low-rank S028 fittings jointly with one in-memory native elimination."""
from argparse import ArgumentParser
from hashlib import sha256
import ctypes,json
from pathlib import Path
import numpy as np
from check import mod,req
def main(a):
    b=a.repo/'research/moonshot-005-program/results';f=mod(b/'bit-spread-h263-source/review/check.py','gf');geo=mod(b/'bit-spread-overlap-source/review/check.py','geometry').Native(a.repo,f);h=mod(b/'bit-spread-source-owner-compiler/author/compile_source.py','source')
    ar=mod(a.field_code,'cost').Arithmetic(a.library,f,h);base=json.loads(a.parameters.read_bytes());prior=json.loads(a.prior.read_bytes());R=np.load(a.ranges)
    axes=sorted(map(int,R.files));offset=0;extras=[]
    for i in axes:
        v=R[str(i)]
        for e in range(8):
            for t in range(v.shape[2]):
                if v[e,:,t].any():extras.append((e,offset+t,i,v[e,:,t]))
        offset+=v.shape[2]
    req(offset==369 and len(extras)<=8*369,'all 369 native output dimensions distributed among physical copies')
    n=480*111;width=n+len(extras)
    A=np.lib.format.open_memmap(a.scratch_matrix,mode='w+',shape=(n,width),dtype=np.uint8) if a.scratch_matrix else np.zeros((n,width),dtype=np.uint8)
    for q,(e,col,i,v) in enumerate(extras):A[i*480:i*480+480,n+q]=v
    for i in range(111):
        E,B=(np.load(a.cache/f'{tag}{i}.npy',mmap_mode='r')for tag in ('E','B'));js=sorted(geo.adj[i]&set(range(111)))
        g=np.load(a.gauges/f'F{i}.npz');S,V=g['S'],g['V']
        req(sha256(S).hexdigest()==base['expected'][str(i)]['S'] and sha256(V).hexdigest()==base['expected'][str(i)]['V'],'actual old gauges')
        sl=slice(i*480,i*480+480);A[sl,sl]=ar.reduce(V,True)[0]
        for j,U,W in zip(js,E,B):A[sl,j*480:j*480+480]=W^ar.mm(S,U)
    hash0=sha256()
    for v in A:hash0.update(v[:n].tobytes())
    req(hash0.hexdigest()==prior['larger_minor_sha256'],'full old true fitting in the prior independent row order')
    appr=sha256(A).hexdigest()
    if a.reorder:
        # This deterministic field-column permutation gives a distinct pivot sequence.
        perm=np.random.default_rng(4831021).permutation(n)
        req(len(set(map(int,perm)))==n,'bijective independent column control')
        for start in range(0,n,64):
            block=A[start:start+64,:n];block[:]=block[:,perm]
    lib=ctypes.CDLL(str(a.rank_library.resolve()));rank=lib.native_augmented_rank
    rank.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int];rank.restype=ctypes.c_int
    print('assembled',n,width,flush=True)
    r=rank(A.ctypes.data,n,width,n,f.MUL.ctypes.data,f.INVERSE.ctypes.data,a.panel,a.threads)
    req(r>0 and not A[r:,:n].any(),'complete bottom null rows after original pivot columns')
    # Under the same invertible row operations, the remaining entries are coordinates in coker(A).
    co=np.zeros((8,n-r,offset),dtype=np.uint8)
    for q,(e,c,i,w) in enumerate(extras):co[e,:,c]=A[r:,n+q]
    left=co.reshape(8*(n-r),offset);gained=len(ar.reduce(left))
    res={'complete_true_predecessor_matrix':hash0.hexdigest(),'augmented_original_field_matrix':appr,'one_copy_old_return_dimension':n,'one_copy_old_rank':r,
         'native_old_rank':8*r,'exact_native_old_kernel':8*(n-r),'total_new_correction_rank':offset,'additional_image_modulo_old_image_rank':gained,
         'rank_of_whole_physical_S028_partial_realization':8*r+gained,'exact_native_modified_kernel':8*(n-r)-gained,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/('PERMUTED-NATIVE-RETURN.json' if a.reorder else 'EXACT-NATIVE-RETURN.json')).write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(res,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for t in ('repo','parameters','prior','ranges','gauges','cache','field-code','library','rank-library','out'):p.add_argument('--'+t,type=Path,required=True)
    p.add_argument('--scratch-matrix',type=Path,help='use a generated disk-backed matrix on memory-constrained hosts');p.add_argument('--reorder',action='store_true');p.add_argument('--panel',type=int,default=64);p.add_argument('--threads',type=int,default=5);main(p.parse_args())
