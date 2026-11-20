"""Emit genuine full-rank 24-bit terminal maps fixing all 840 modes per native body."""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from make_field import make,mul


def need(c,m):
    if not c:raise ValueError(m)


class Field:
    def __init__(self,lib):
        desc=make();need(desc['binary_modulus']==0x100001b,'binary modulus in C')
        self.poly=desc['binary_modulus'];self.fwd=self.lookup(desc['native_basis']);self.bwd=self.lookup(desc['inverse_basis'])
        self.lib=ctypes.CDLL(str(lib.resolve()));ptr=ctypes.c_void_p;s=ctypes.c_size_t
        self.lib.mm24.argtypes=[ptr,ptr,ptr,s,s,s];self.lib.mm24.restype=None
        self.lib.rank24.argtypes=[ptr,s,s,ptr,ptr];self.lib.rank24.restype=s
        self.lib.solve24.argtypes=[ptr,s,s];self.lib.solve24.restype=ctypes.c_int
        a=np.array([[(1<<i)^i for i in range(24)]],dtype=np.uint32);coeff=np.array([[1234567]],dtype=np.uint32)
        need(self.mm(coeff,a)[0].tolist()==[mul(1234567,int(v),self.poly) for v in a[0]],'CLMUL and all vector lanes')
        sample=np.array([[0,1,2,3],[4,17,21,57],[18,1,22,7]],dtype=np.uint8)
        need(np.array_equal(self.to_limbs(self.wrap(sample)),sample),'actual native polynomial basis')

    @staticmethod
    def lookup(bits):
        return np.asarray([[np.bitwise_xor.reduce([bits[8*k+i] for i in range(8) if (x>>i)&1],initial=0,dtype=np.uint32) for x in range(256)] for k in range(3)],dtype=np.uint32)
    @staticmethod
    def change(x,t):return t[0,x&255]^t[1,(x>>8)&255]^t[2,x>>16]
    def wrap(self,y):
        a=y.astype(np.uint32);x=a[...,0]^(a[...,1]<<6)^(a[...,2]<<12)^(a[...,3]<<18);return self.change(x,self.fwd)
    def to_limbs(self,x):
        a=self.change(x,self.bwd);return np.stack([(a>>(6*k))&63 for k in range(4)],axis=-1).astype(np.uint8)
    def mm(self,a,b):
        a=np.ascontiguousarray(a,dtype=np.uint32);b=np.ascontiguousarray(b,dtype=np.uint32);need(a.shape[1]==len(b),'matrix shape')
        c=np.zeros((len(a),b.shape[1]),dtype=np.uint32)
        if len(a) and len(b) and b.shape[1]:self.lib.mm24(a.ctypes.data,b.ctypes.data,c.ctypes.data,len(a),len(b),b.shape[1])
        return c
    def rank(self,a):
        a=np.array(a,dtype=np.uint32,copy=True,order='C');n,m=a.shape;ids=np.arange(n,dtype=np.uint32);p=np.zeros(min(n,m),dtype=np.uint32)
        r=self.lib.rank24(a.ctypes.data,n,m,ids.ctypes.data,p.ctypes.data);return r,ids[:r],p[:r]
    def right(self,a,t):
        n=len(a);need(a.shape==(n,n) and t.shape[1]==n,'invertible interpolation dimensions')
        aug=np.ascontiguousarray(np.hstack((a.T,t.T)),dtype=np.uint32)
        need(self.lib.solve24(aug.ctypes.data,n,len(t))==0,'exact interpolation solve')
        need(np.array_equal(aug[:,:n],np.eye(n,dtype=np.uint32)),'all pivots reduced')
        return aug[:,n:].T.copy()


def prg(label,shape):
    n=int(np.prod(shape));raw=hashlib.shake_256(label.encode()).digest(n)
    return (np.frombuffer(raw,dtype=np.uint8).reshape(shape)&63)


def native_z(tag,j,w,d):return prg(f'known-original-S029-four-copy-v1/{tag}/role-{j}',(w,d,4))


def main():
    ap=argparse.ArgumentParser()
    for t in ('repo','transfer','k-words','d-charts','mult','packed','out'):ap.add_argument('--'+t,type=Path,required=True)
    ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int,default=111)
    ap.add_argument('--sector',choices=('small','large'),required=True);ap.add_argument('--seed',default='zero-slack-0');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(a.transfer.resolve()));from transfer import Atlas
    at=Atlas(a.repo,a.k_words,a.d_charts,a.mult);mm=at.ops.matmul;field=Field(a.packed);tag=a.sector+'/'+a.seed
    lo,hi,d=(0,96,168) if a.sector=='small' else (96,480,672);w=hi-lo
    Z=[native_z(tag,j,w,d) for j in range(111)];start=time.time()
    for i in range(a.start,a.stop):
        receipt=a.out/f'F{i:03}.json';word=a.out/f'F{i:03}.bin'
        if receipt.exists() and word.exists():continue
        early,ec,late,yc=at.facet(i);es=np.flatnonzero(np.any(ec[lo:hi],axis=0));ys=np.flatnonzero(np.any(yc[lo:hi],axis=0));m=len(es)+len(ys)
        rhs=np.zeros((m,d,4),dtype=np.uint8);blocks=[];donors=sorted(j for j in at.orth[i] if j<111)
        for j in donors:
            _,A,_,B=at.terminal_inputs(i,j);M=np.vstack((A[es,lo:hi],B[ys,lo:hi]));blocks.append(M)
            rhs^=mm(M,Z[j].reshape(w,4*d)).reshape(m,d,4)
        rhs=field.wrap(rhs);target=field.wrap(Z[i]);r,idx,_=field.rank(rhs);need(r==d,f'{tag} actual input kernel rank at F{i}')
        rest=np.asarray([u for u in range(m) if u not in set(map(int,idx))],dtype=np.int64)
        solution=field.right(rhs[idx],np.vstack((target,rhs[rest])));fixed=solution[:w];part=solution[w:]
        for trial in range(12):
            extra=field.wrap(prg(f'extra/{tag}/{i}/{trial}',(w,len(rest),4)))
            F=np.zeros((w,m),dtype=np.uint32);F[:,rest]=extra;F[:,idx]=fixed^field.mm(extra,part)
            if field.rank(F[:,len(es):])[0]!=w:continue
            fp=field.to_limbs(F).transpose(2,0,1).reshape(4*w,m);det=[]
            for M in blocks:
                prod=field.wrap(mm(fp,M).reshape(4,w,w).transpose(1,2,0));rk,_,piv=field.rank(prod)
                if rk!=w:break
                value=1
                for q in piv:value=mul(value,int(q),field.poly)
                det.append(value)
            if len(det)==len(donors):break
        else:raise ValueError(f'foreign protection failed seed {tag} F{i} after {len(det)} of {len(donors)}')
        need(np.array_equal(field.mm(F,rhs),target),'every exact native kernel mode')
        packed=np.ascontiguousarray(F,dtype='<u4').view(np.uint8).reshape(w,m,4)[:,:,:3].tobytes();word.write_bytes(packed)
        data={'facet':i,'sector':a.sector,'PRG_seed':a.seed,'extension':0x100001b,'real_native_copies_per_field':4,
              'mode_dimension':d,'preterminal_count':m,'early_count':len(es),'late_count':len(ys),'full_prescribed_mode_rank':r,
              'all_mode_identity_SHA256':hashlib.sha256(target.tobytes()).hexdigest(),'actual_GF24_terminal_word_SHA256':hashlib.sha256(packed).hexdigest(),
              'terminal_pure_late_GL':True,'actual_foreign_nonzero_determinants':dict(zip(donors,det)),'extension_trial':trial}
        receipt.write_text(json.dumps(data,sort_keys=True)+'\n')
        if i%4==0:print(a.sector,i,round(time.time()-start,1),flush=True)


if __name__=='__main__':main()
