#!/usr/bin/env python3
"""Rebuild full original modes of the independent six-facet direct propagation."""
import argparse,ctypes,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
def go(a):
    repo=a.repo.resolve();base=repo/'research/moonshot-005-program/results';native=base/'bit-native-rs-return-distance/author';h=base/'bit-spread-rs-physical-word/author';here=Path(__file__).resolve().parent
    src=here.parent/'author/sources/SMALL.npz';art=np.load(src);k=base/'bit-gf64-actual-k-atlas/author/output';d=base/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz';out=a.out.resolve()
    def run(command):subprocess.run([str(t)for t in command],check=True)
    py=[sys.executable,'-I','-B']
    with tempfile.TemporaryDirectory(prefix='independent-true-field')as td:
        tmp=Path(td);cc=['cc','-std=c11','-O3','-march=native','-fPIC','-shared']
        run([*cc,'-I',native,here/'solve.c','-o',tmp/'solve.so']);run([*cc,h/'gf64_matmul.c','-o',tmp/'mul.so'])
        if a.matrix:mf=a.matrix.resolve()
        else:
            run([*py,native/'build_minor.py','--repo',repo,'--transfer',h,'--k-words',k,'--d-charts',d,'--mult',tmp/'mul.so','--rank-lib',tmp/'solve.so','--sector','small','--mode','all','--build-only','--out',tmp/'matrix']);mf=tmp/'matrix/M.raw'
        A=np.memmap(mf,np.uint8,mode='r',shape=(10656,10656));assert hashlib.sha256(memoryview(A)).hexdigest()=='8b6eccaf6c6e371b85473a48c89a6a5c1f14968b2687ff3f56f76a56e4e4d3c9'
        sys.path.insert(0,str(h));from transfer import TABLE,INV,Arithmetic
        mm=Arithmetic(tmp/'mul.so').matmul;w=96;n=8*w;N=len(A)-n;raw=art['kernel'];aug=np.ascontiguousarray(np.hstack([A[n:,n:],A[n:,:n]]));result=np.empty((N,n),np.uint8);rows=np.empty(N,np.uint32);cols=np.empty(N,np.uint32);diags=np.empty(N,np.uint8);p=ctypes.c_void_p
        f=ctypes.CDLL(str(tmp/'solve.so')).solve_many;f.argtypes=[p,ctypes.c_size_t,ctypes.c_size_t,p,p,p,p,p,p];f.restype=ctypes.c_int
        assert f(aug.ctypes.data,N,n,TABLE.ctypes.data,INV.ctypes.data,rows.ctypes.data,cols.ctypes.data,diags.ctypes.data,result.ctypes.data)==0
        Lift=np.vstack([np.eye(n,dtype=np.uint8),result]);assert not mm(A[n:],Lift).any()
        def extend(s):
            cond=np.vstack([raw[(2*i+s)*w:(2*i+s+1)*w]for i in range(8)]);return mm(Lift,cond)
        np.savez_compressed(tmp/'full.npz',one=extend(0),two=extend(1))
        run([*py,here/'check.py','--repo',repo,'--h-author',h,'--k-words',k,'--d-charts',d,'--library',tmp/'mul.so','--kernel',tmp/'full.npz','--controls',src,'--out',out])
    assert json.loads((out/'RESULT.json').read_bytes())==json.loads((here/'RESULT.json').read_bytes())
if __name__=='__main__':
    q=argparse.ArgumentParser(description=__doc__);q.add_argument('--repo',type=Path,required=True);q.add_argument('--out',type=Path,required=True);q.add_argument('--matrix',type=Path,help='optional pinned canonical small M.raw');go(q.parse_args())
