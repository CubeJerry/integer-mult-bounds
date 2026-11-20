"""Regenerate native eight-role reductions by source-first field elimination."""
import ctypes
import importlib.util
from types import SimpleNamespace
import numpy as np

def replay(repo,base,folder,atlas,reference):
    source=base/'bit-spread-rs-physical-word/author';directory=base/'bit-native-rs-return-distance/stream'
    spec=importlib.util.spec_from_file_location('native_stream',directory/'check.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);engine=mod.Engine(folder/'stream.so')
    alg=mod.load_replay(base/'bit-physical-terminal-quotient/author');alg.mm=engine.mm
    settings=SimpleNamespace(repo=repo,h_words=source/'output',d_words=base/'bit-minimum-cache-d-atlas/author/output',k_words=base/'bit-gf64-actual-k-atlas/author/output')
    native=alg.Native(settings);c=mod.Cascade(native,alg,engine,True)
    w=96;zero=np.zeros(w,np.uint8);wanted=[int(t) for i in range(6)for kind in ('e','y')for t in reference[kind+str(i)]]
    def columns(j):
        dv=native.through_d(j,range(111),True)
        assert all(not row[w:].any()for row in dv.values())
        physical={}
        for k in c.by_donor[j]:
            stripes,cross=c.word[k]
            for src,dest in stripes:
                M=np.stack([dv[t][:w] if t in dv else zero for t in src])
                if M.any():physical.update(zip(dest,engine.mm(c.vandermonde,M)))
            for i,o in cross:
                if i in physical:physical[o]=physical.get(o,zero)^physical[i]
        returns=np.zeros((w,111*w),np.uint8);returns[:,j*w:(j+1)*w]=np.eye(w,dtype=np.uint8)
        for (i,ch),(ids,b) in c.facets.items():
            if not native.orth[i,j]:continue
            hit=[q for q,t in enumerate(ids)if t in physical]
            if hit:
                off=i*w+ch*16;returns[:,off:off+16]=engine.mm(b[:,hit],np.stack([physical[ids[q]]for q in hit])).T
        obs=np.stack([physical.get(t,zero)for t in wanted]).T
        return np.ascontiguousarray(np.hstack([returns[:,8*w:],returns[:,:8*w],obs]))
    f=engine.lib;v=ctypes.c_void_p;f.quotient.argtypes=[v,v,ctypes.c_size_t,v];f.quotient.restype=ctypes.c_int
    extra=8*w+len(wanted);st=f.begin(103*w+extra)
    try:
        for j in range(8,111):
            a=columns(j)
            for k in range(0,w,32):assert f.consume(st,a[k:].ctypes.data,min(32,w-k))
        assert f.present_rank(st)==103*w
        payload=[]
        for j in range(8):
            a=columns(j);q=np.empty((w,extra),np.uint8)
            for k in range(0,w,32):assert f.quotient(st,a[k:].ctypes.data,min(32,w-k),q[k:].ctypes.data)
            payload.append(q)
        response=np.vstack(payload).T
        assert np.array_equal(response[:8*w],reference['K'])
        start=8*w
        for i in range(6):
            name='sens'+str(i);n=len(reference[name]);assert np.array_equal(response[start:start+n],reference[name]),i;start+=n
        assert start==len(response)
    finally:f.finish(st)
