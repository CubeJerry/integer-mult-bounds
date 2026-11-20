import ctypes,numpy as np
from transfer import TABLE,INV
class Arithmetic:
    def __init__(self,path):
        self.f=ctypes.CDLL(str(path)).invert;self.f.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p];self.f.restype=ctypes.c_int
    def inverse(self,mat):
        n=len(mat);z=np.hstack([mat,np.eye(n,dtype=np.uint8)])
        if not self.f(z.ctypes.data,n,TABLE.ctypes.data,INV.ctypes.data):raise ValueError('singular field matrix')
        assert np.array_equal(z[:,:n],np.eye(n,dtype=np.uint8));return z[:,n:].copy()
