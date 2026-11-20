"""In-place blocked exact rank of the authenticated complete native return matrix."""
from argparse import ArgumentParser
from hashlib import sha256
import ctypes,json,time
from pathlib import Path
import numpy as np
from rebuild import mod,req

def runner(lib,f):
    op=ctypes.CDLL(str(lib.resolve())).native_block_rank;op.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int];op.restype=ctypes.c_int
    def reduce(A,w,t):
        if not(A.flags.c_contiguous and A.dtype==np.uint8):raise ValueError('mutable contiguous byte matrix')
        return op(A.ctypes.data,*A.shape,f.MUL.ctypes.data,f.INVERSE.ctypes.data,w,t)
    return reduce
def main(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','field');rank=runner(a.library,f)
    rng=np.random.default_rng(27834);tested=0
    for n,m in [(1,48),(93,75),(61,90),(75,75),(141,211),(6,211),(121,111),(103,563),(310,911)]:
        A=rng.integers(64,size=(n,m),dtype=np.uint8)
        for sparse in (False,True):
            Q=A.copy()
            if sparse:
                Q[::3]=0;Q[:,::5]=0;Q[-1]=Q[0]
                Q[n//2]=Q[n//3];Q[:,m//2]=Q[:,m//3]
            rr=f.eliminate(Q)[0]
            for b in (1,5,17,48,79):
                req(rank(Q.copy(),b,2)==rr,'exact rectangular and singular native controls');tested+=1
    for n,m,d in [(211,763,34),(412,769,71)]:
        B=rng.integers(64,size=(n,d),dtype=np.uint8);C=rng.integers(64,size=(d,m),dtype=np.uint8);L=f.matmul(B,C)
        rr=f.eliminate(L)[0];req(rr==d,'known low-rank finite product')
        for b in (13,48,63):req(rank(L.copy(),b,2)==rr,'wide optimized tile and singular partial rows');tested+=1
    if a.controls_only:print('PASS',tested);return
    A=np.load(a.matrix,mmap_mode='r+');claim=json.loads(a.receipt.read_bytes());pin=sha256(A).hexdigest();req(pin==claim['larger_minor_sha256'],'input global native fitting digest')
    t0=time.monotonic();r=rank(A,a.panel,a.threads);elapsed=time.monotonic()-t0
    out={'mutated_original_matrix_sha256':pin,'one_copy_rows':len(A),'one_copy_columns':A.shape[1],'exact_one_copy_rank':r,'eight_copy_rank':8*r,'one_copy_nullity':A.shape[1]-r,'eight_copy_nullity':8*(A.shape[1]-r),'one_copy_true_controls':tested,'host_elapsed_seconds':elapsed,'panel_width':a.panel,'threads':a.threads}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'COMPLETE-RANK.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print('PASS all',len(A),'row & col rank',r,'elapsed',elapsed)
if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--library',type=Path,required=True);p.add_argument('--matrix',type=Path);p.add_argument('--receipt',type=Path);p.add_argument('--out',type=Path);p.add_argument('--panel',type=int,default=48);p.add_argument('--threads',type=int,default=3);p.add_argument('--controls-only',action='store_true');main(p.parse_args())
