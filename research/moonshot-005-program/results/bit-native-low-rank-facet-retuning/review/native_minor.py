#!/usr/bin/env python3
"""Check the declared four-role Schur value against an independently built actual square matrix."""
from pathlib import Path
import argparse,ctypes,gzip,hashlib,json,subprocess,tempfile
import numpy as np

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('repo','matrix','out'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--sector',choices=('small','large'),default='small');a=p.parse_args()
    root=a.repo/'research/moonshot-005-program/results';here=Path(__file__).resolve().parents[1]
    actual=root/'bit-native-rs-return-distance/author';pin=json.loads(gzip.decompress((actual/'output'/(a.sector+'-all.json.gz')).read_bytes()))['matrix_sha256']
    m=json.loads((here/'author/sources/MANIFEST.json').read_text())[a.sector];raw=gzip.decompress((here/'author/sources'/(a.sector+'-four-schur.bin.gz')).read_bytes());size=m['matrix_size']
    require(hashlib.sha256(raw).hexdigest()==m['sha256'],'four-role Schur digest');K=np.frombuffer(raw,np.uint8).reshape(size,size);w=size//4;n=111*w
    A=np.memmap(a.matrix,dtype=np.uint8,mode='r',shape=(n,n));h=hashlib.sha256();h.update(memoryview(A));require(h.hexdigest()==pin,'separate native row-by-row proper-matrix digest')
    # Form an independent binary polynomial-basis product table.
    product=np.zeros((64,64),np.uint8)
    for x in range(64):
        for y in range(64):
            v=0
            for j in range(6):
                if y>>j&1:v^=x<<j
            while v>=64:v^=67<<(v.bit_length()-7)
            product[x,y]=v
    inv=np.array([0]+[int(np.flatnonzero(product[j]==1)[0])for j in range(1,64)],dtype=np.uint8)
    with tempfile.TemporaryDirectory() as tmp:
        lib=Path(tmp)/'r.so';subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared',str(actual/'field_rank.c'),'-o',str(lib)],check=True)
        f=ctypes.CDLL(str(lib)).exact_rank;ptr=ctypes.c_void_p;f.argtypes=[ptr,ctypes.c_size_t,ctypes.c_size_t,ptr,ptr,ptr,ptr,ptr];f.restype=ctypes.c_size_t
        def rank(x):
            yy=np.ascontiguousarray(x).copy();b=min(yy.shape);rows=np.empty(len(yy),np.uint32);cols=np.empty(b,np.uint32);diag=np.empty(b,np.uint8)
            r=f(yy.ctypes.data,*yy.shape,product.ctypes.data,inv.ctypes.data,rows.ctypes.data,cols.ctypes.data,diag.ctypes.data);det=1
            for j in diag[:r]:det=int(product[det,j])
            return int(r),det
        # Reverse order outright to avoid sharing the source-column pivot order.
        outside,do=rank(A[size:,size:][::-1,::-1]);require(outside==n-size,'outside principal square is invertible')
        D=np.array(A[::-1,::-1],copy=True);D[-size:,-size:]^=K[::-1,::-1]
        rr,dd=rank(D);require(rr==outside,'unique four-role Schur transfer')
    info={'source_matrix_sha256':pin,'schur_sha256':m['sha256'],'original_dimensions':n,'untouched_outside_rank':outside,'outside_determinant':do,'rank_after_removing_declared_schur':rr,'pivot_minor_determinant':dd,'original_rows_and_columns_reversed':True}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/(a.sector.upper()+'.json')).write_text(json.dumps(info,indent=2)+'\n');print(info,flush=True)
if __name__=='__main__':main()
