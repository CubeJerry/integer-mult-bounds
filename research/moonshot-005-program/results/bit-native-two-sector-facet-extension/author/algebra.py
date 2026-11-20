import os
from pathlib import Path
import ctypes,sys,time,itertools,json,hashlib,argparse
import numpy as np
base=Path(os.environ['FE_REPO'])/'research/moonshot-005-program/results';sys.path.insert(0,str((base/'bit-spread-rs-physical-word/author').resolve()));from transfer import Atlas,TABLE,INV,Arithmetic
folder=Path(os.environ['FE_DIR']);shared=ctypes.CDLL(str((folder/'field.so').resolve()));f=shared.right_kernel;p=ctypes.c_void_p;f.argtypes=[p,ctypes.c_size_t,ctypes.c_size_t,p,p,p];f.restype=ctypes.c_size_t
mm=Arithmetic(folder/'mul.so').matmul
def kernel(A):
 m=np.array(A,order='C',copy=True,dtype=np.uint8);n=m.shape[1];o=np.empty(n*n,np.uint8);d=f(m.ctypes.data,*m.shape,TABLE.ctypes.data,INV.ctypes.data,o.ctypes.data);assert d<=n;return o[:n*d].reshape(n,d).copy()
direct=ctypes.CDLL(str((folder/'stream.so').resolve()));assert direct.init_field();vi=direct.inverse_direct;vi.argtypes=[p,ctypes.c_size_t,p];vi.restype=ctypes.c_int
rf=shared.exact_rank;rf.argtypes=[p,ctypes.c_size_t,ctypes.c_size_t,p,p,p,p,p];rf.restype=ctypes.c_size_t
def rank(A):
 m=np.array(A,dtype=np.uint8,order='C',copy=True);mn=min(m.shape);rr=np.empty(len(m),np.uint32);co=np.empty(mn+1,np.uint32);dg=np.empty(mn+1,np.uint8);return int(rf(m.ctypes.data,*m.shape,TABLE.ctypes.data,INV.ctypes.data,rr.ctypes.data,co.ctypes.data,dg.ctypes.data))

def inverse(A):
 a=np.ascontiguousarray(A);out=np.empty_like(a);assert vi(a.ctypes.data,len(a),out.ctypes.data);return out
def pair(A,w):
 zz=np.zeros_like(A);b=np.block([[A,zz],[zz,A]]);ind=np.array([j*w+t+s*A.shape[1] for j in range(A.shape[1]//w)for s in range(2)for t in range(w)]);return b[:,ind]
w=384;d=2*w;n=8*d;ids=list(range(8));K=np.load(folder/'K.npz')['K'];obs=[np.load(folder/f'S{i}.npz')['sens']for i in range(6)];oldW=np.load(folder/'old.npz')['actual'];K0=np.vstack([pair(K[i*w:(i+1)*w],w)for i in ids]);
for i in range(4):K0[i*d:(i+1)*d,i*d:(i+1)*d]^=oldW[i]^np.eye(d,dtype=np.uint8)
Z=kernel(K0);assert Z.shape==(n,2*d) and not mm(K0,Z).any();S=[pair(x,w)for x in obs];H=[mm(s,Z)for s in S];nulls=[kernel(h)for h in H]
