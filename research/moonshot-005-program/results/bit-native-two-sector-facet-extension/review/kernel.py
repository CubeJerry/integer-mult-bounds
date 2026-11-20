"""Direct action and rank of an independently reconstructed two-copy anchor matrix."""
import argparse,ctypes,hashlib,json,sys
from pathlib import Path
import numpy as np
def run(a):
    mm=Arithmetic(a.library).matmul;w=384;q=768;K=np.load(a.data/'K.npz')['K'];record=np.load(a.data/f'NEW-{a.h}.npz');W=np.load(a.old)['actual'];act=record['acts'];X=record['allk']
    def parts(M):
        wide=np.zeros((2*len(M),16*w),np.uint8)
        for role in range(8):
            for replica in range(2):
                wide[replica*len(M):(replica+1)*len(M),role*q+replica*w:role*q+(replica+1)*w]=M[:,role*w:(role+1)*w]
        return wide
    blocks=[]
    for i in range(8):
        block=parts(K[i*w:(i+1)*w])
        if i<4:block[:,i*q:(i+1)*q]^=W[i]^np.eye(q,dtype=np.uint8)
        if i<6:
            S=np.load(a.data/f'S{i}.npz')['sens'];raw=parts(S);U=mm(act[i],record[f'phi{i}']);block^=mm(U,raw)
        assert not mm(block,X).any();blocks.append(block)
    T=np.vstack(blocks);lib=ctypes.CDLL(str(a.rank.resolve()));fn=lib.field_rank;v=ctypes.c_void_p;fn.argtypes=[v,ctypes.c_int,ctypes.c_int,v,v];fn.restype=ctypes.c_int
    def rank(M):
        m=np.array(M,copy=True,order='C');return fn(m.ctypes.data,*m.shape,TABLE.ctypes.data,INV.ctypes.data)
    xr=rank(X);r=rank(T);assert xr==X.shape[1]==6144-r==1536+a.h
    total=4*(20852+103*768+r);a.out.mkdir(exist_ok=True,parents=True)
    z={'paired_anchor_dimension':6144,'independently_checked_nullity':xr,'independently_checked_rank':r,'true_native_return_with_460_column_small':total,'all_new_zero_equations':6144*xr,'reconstructed_operator_SHA256':hashlib.sha256(T.tobytes()).hexdigest()};(a.out/f'KERNEL-{a.h}.json').write_text(json.dumps(z,indent=2)+'\n');print(z)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--h',type=int,required=True)
 for f in ('data','old','library','rank','native','out'):p.add_argument('--'+f,type=Path,required=True)
 a=p.parse_args();sys.path.insert(0,str(a.native));from transfer import Arithmetic,INV,TABLE;run(a)
