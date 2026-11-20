import ctypes
from pathlib import Path
import numpy as np
from basis import Basis,change,lookup,product,RECIP
class Field:
    def __init__(self,path):
        self.b=Basis();lib=ctypes.CDLL(str(Path(path).resolve()));self.lib=lib
        p=ctypes.c_void_p;n=ctypes.c_size_t
        lib.detrec.argtypes=[p,n,n,p];lib.detrec.restype=n
        lib.price.argtypes=[p,n,p,p,p];lib.price.restype=ctypes.c_uint64
        lib.weightall.argtypes=[p,p,p,p];lib.weightall.restype=None
        lib.verify_mul.argtypes=[ctypes.c_uint32]*2;lib.verify_mul.restype=ctypes.c_uint32
        rng=np.random.default_rng(111)
        for x,y in rng.integers(0,1<<24,(2500,2)):
            assert lib.verify_mul(int(x),int(y))==product(int(x),int(y),RECIP)
        self.base=change(np.array(self.b.native,dtype=np.uint32),self.b.rec)
        self.to_native=lookup([int(change(change(np.uint32(1<<k),self.b.rr),self.b.inv))for k in range(24)])
    def init_price(self):
        self.costs=np.zeros(1<<24,dtype=np.uint16)
        w=np.array([sum(product(x,1<<k,67).bit_count()for k in range(6))for x in range(64)],dtype=np.uint8)
        self.lib.weightall(self.costs.ctypes.data,self.b.rr.ctypes.data,self.b.inv.ctypes.data,w.ctypes.data)
        assert self.costs[0]==0 and self.costs[1]==24
    def det(self,A):
        A=np.ascontiguousarray(np.array(A,copy=True,dtype=np.uint32));out=np.zeros(1,dtype=np.uint32);s=self.lib.detrec(A.ctypes.data,len(A),A.shape[1],out.ctypes.data)
        return s,int(out[0])
    def price(self,A):
        A=np.ascontiguousarray(np.array(A,copy=True,dtype=np.uint32));n=len(A)
        v=self.lib.price(A.ctypes.data,n,self.costs.ctypes.data,self.base.ctypes.data,self.to_native.ctypes.data)
        assert np.array_equal(A,np.eye(n,dtype=np.uint32))
        return int(v)
