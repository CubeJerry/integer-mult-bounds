"""Exact rank, ordered pivots, invertible six-bit word price, and field matrix products."""
import ctypes
import numpy as np
class Arithmetic:
    def __init__(self,lib,f,helper):
        self.f=f;self.library=ctypes.CDLL(str(lib.resolve()));self.r=self.library.cert_reduce
        ptr=ctypes.c_void_p
        self.r.argtypes=[ptr,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ptr,ptr,ptr,ptr,ptr,ptr]
        self.r.restype=ctypes.c_uint64
        self.weights=np.asarray(helper.WEIGHT,dtype=np.int32)
        self.scales=np.asarray([len(helper.SCALES.get(q,[])) for q in range(64)],dtype=np.int32)
        self.mul=self.library.gf64_gemm;self.mul.argtypes=[ptr]*4+[ctypes.c_size_t]*3;self.mul.restype=None
    def mm(self,A,B):
        A,B=np.ascontiguousarray(A),np.ascontiguousarray(B)
        if A.shape[1]!=len(B):raise ValueError('product shape')
        C=np.zeros((len(A),B.shape[1]),dtype=np.uint8);self.mul(A.ctypes.data,B.ctypes.data,C.ctypes.data,self.f.MUL.ctypes.data,len(A),len(B),B.shape[1]);return C
    def reduce(self,A,invert=False):
        n,w=A.shape;B=np.ascontiguousarray(np.hstack([A,np.eye(n,dtype=np.uint8)]) if invert else A.copy())
        piv=np.empty(min(n,w),dtype=np.int32);r=ctypes.c_int(0)
        count=self.r(B.ctypes.data,n,w,B.shape[1],invert,piv.ctypes.data,self.f.MUL.ctypes.data,self.f.INVERSE.ctypes.data,self.weights.ctypes.data,self.scales.ctypes.data,ctypes.byref(r))
        if invert and (n!=w or r.value!=n):raise ValueError('invertible binary-priced native square')
        return (B[:,w:],count) if invert else piv[:r.value]
