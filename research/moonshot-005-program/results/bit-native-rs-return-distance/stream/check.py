#!/usr/bin/env python3
"""Direct causal owner propagation with streaming exact column elimination."""
import argparse
from collections import defaultdict, Counter
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

def require(x,text):
    if not x:
        raise ValueError(text)

class Engine:
    def __init__(self,filename):
        self.lib=ctypes.CDLL(str(filename.resolve()))
        v,n=ctypes.c_void_p,ctypes.c_size_t
        self.lib.init_field.argtypes=[];self.lib.init_field.restype=ctypes.c_int
        require(self.lib.init_field()==1,"two field tables and complete SIMD polarity test")
        self.lib.multiply_direct.argtypes=[v,v,v,n,n,n];self.lib.multiply_direct.restype=None
        self.lib.begin.argtypes=[n];self.lib.begin.restype=v
        self.lib.consume.argtypes=[v,v,n];self.lib.consume.restype=ctypes.c_int
        self.lib.present_rank.argtypes=[v];self.lib.present_rank.restype=n
        self.lib.determinant.argtypes=[v];self.lib.determinant.restype=ctypes.c_uint8
        self.lib.finish.argtypes=[v];self.lib.finish.restype=None

    def mm(self,a,b):
        a=np.ascontiguousarray(a,dtype=np.uint8);b=np.ascontiguousarray(b,dtype=np.uint8)
        require(a.shape[1]==b.shape[0],"matrix multiplication over GF(64)")
        c=np.empty((a.shape[0],b.shape[1]),dtype=np.uint8)
        self.lib.multiply_direct(a.ctypes.data,b.ctypes.data,c.ctypes.data,len(a),len(b),b.shape[1])
        return c

class Cascade:
    def __init__(self,native,alg,engine,small):
        self.nat=native; self.alg=alg; self.kernel=engine
        self.small=small;self.width=96 if small else 384
        self.s=0 if small else 96
        n=9 if small else 36;k=n//3
        self.word={}; facets=defaultdict(list)
        self.vandermonde=np.array(alg.POWER[1:n+1,:n].T,order="C")
        for h,word in native.kwords["spread"].items():
            stripes=[];counts=Counter(); p=native.p[h];size=p["m"]
            for phase,src,dst in word["stripes"]:
                if len(src)!=n:continue
                stripe=counts[phase];counts[phase]+=1
                stripes.append((src,dst))
                for t,owner in enumerate(dst):
                    r=native.rt[owner];i=r[1] if phase=="Y" else r[7]
                    if i is None:continue
                    q=p["donor_early"][str(i)]
                    der=False;scale=1
                    if size==3 and q==30:
                        channel=t%k+stripe*k
                    elif size==2 and q==30:
                        channel=t
                    elif size==1:
                        der=t>=2*k;channel=t-2*k if der else t
                        scale=alg.SCALES_Y[i][n==36] if der else 1
                    else:
                        first=(h in native.half[i])==(phase=="Y")
                        channel=t%k+(0 if first else k)
                    row=alg.jet(native.node[i,h],der,scale)
                    facets[i,channel].append((owner,row))
            kept={t for _,d in stripes for t in d}
            cross=[(x,y) for x,y in word["early_cache_to_late"] if x in kept or y in kept]
            require(all(x in kept and y in kept for x,y in cross),"no cross-sector K cache")
            self.word[h]=stripes,cross
        self.facets={}
        for key,assignments in facets.items():
            owners=[x for x,r in assignments]
            m=np.array([r for x,r in assignments],dtype=np.uint8).T.copy()
            self.facets[key]=owners,m
        require(len(self.facets)==111*2*k,"complete output channel coverage")
        self.by_donor={j:sorted({h for d,D in enumerate(native.D) if j in D and ((d in native.mark)==small)
                                 for phase,arr in native.byd[d].items() for t in arr
                                 if (h:=native.rt[t][5]) is not None and h in self.word}) for j in range(111)}

    def columns(self,j):
        n=self.width;sl=slice(self.s,self.s+n);nat=self.nat;eng=self.kernel
        dv=nat.through_d(j,range(111),self.small)
        zero=np.zeros(n,dtype=np.uint8)
        other=slice(96,480) if self.small else slice(0,96)
        require(all(not v[other].any() for v in dv.values()),"inactive source sector")
        dv={t:v[sl] for t,v in dv.items()};physical={}
        for h in self.by_donor[j]:
            stripes,cross=self.word[h]
            for src,dst in stripes:
                mat=np.stack([dv.get(t,zero) for t in src])
                if not mat.any():continue
                rows=eng.mm(self.vandermonde,mat)
                physical.update(zip(dst,rows))
            for x,y in cross:
                if x in physical:
                    if y in physical:physical[y]^=physical[x]
                    else:physical[y]=physical[x].copy()
        col=np.zeros((n,111*n),dtype=np.uint8)
        col[:,j*n:(j+1)*n]=np.eye(n,dtype=np.uint8)
        for (i,ch),(owners,m) in self.facets.items():
            if not nat.orth[i,j]:continue
            hits=[p for p,t in enumerate(owners) if t in physical]
            if not hits:continue
            out=eng.mm(m[:,hits],np.stack([physical[owners[p]] for p in hits]))
            lo=i*n+16*ch
            col[:,lo:lo+16]=out.T
        return col

def load_replay(path):
    sys.path.insert(0,str(path.resolve()))
    spec=importlib.util.spec_from_file_location("causal_replay",path/"check.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def main():
    p=argparse.ArgumentParser()
    for name in ("repo","replay","h-words","d-words","k-words","stream-lib","out"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--sector",choices=("small","large"),required=True)
    p.add_argument("--external-blocks",type=Path)
    p.add_argument("--expected",type=int)
    p.add_argument("--batch",type=int,default=32)
    a=p.parse_args();alg=load_replay(a.replay)
    e=Engine(a.stream_lib);alg.mm=e.mm;nat=alg.Native(a)
    cascade=Cascade(nat,alg,e,a.sector=="small");w=cascade.width
    n=111*w
    state=e.lib.begin(n);require(state,"streamed echelon allocation")
    h=hashlib.sha256();checkpoints={};block_digest=hashlib.sha256()
    a.out.mkdir(exist_ok=True,parents=True)
    try:
        for j in range(111):
            pkt=cascade.columns(j)
            h.update(memoryview(pkt))
            if a.external_blocks:
                for file in sorted(a.external_blocks.glob(f"B-*-{j}.npy")):
                    i=int(file.stem.split("-")[1]);sl=slice(cascade.s,cascade.s+w)
                    ref=np.load(file)
                    require(np.array_equal(pkt[:,i*w:(i+1)*w].T,ref[sl,sl]),f"independent proper {i}/{j}")
                    block_digest.update(file.name.encode());block_digest.update(memoryview(np.ascontiguousarray(ref[sl,sl])))
            for t in range(0,w,a.batch):
                group=pkt[t:t+a.batch]
                require(e.lib.consume(state,group.ctypes.data,len(group)),"streamed reciprocal-basis elimination")
            if j in (0,9,19,29,39,49,59,69,79,89,99,110):
                checkpoints[j]=e.lib.present_rank(state)
                print(a.sector,j+1,checkpoints[j],flush=True)
        r=e.lib.present_rank(state);det=e.lib.determinant(state)
        if a.expected is not None:require(det==a.expected,"independent determinant prediction")
        res={"sector":a.sector,"width":w,"roles":111,"size":n,"rank":r,"determinant_GF64":det,
             "original_polynomial":67,"reciprocal_polynomial":97,"eliminated":"transposed rows in input-column order",
             "transpose_sha256":h.hexdigest(),"external_blocks_digest":block_digest.hexdigest() if a.external_blocks else None,
             "rank_checkpoints":checkpoints}
        (a.out/(a.sector.upper()+".json")).write_text(json.dumps(res,indent=2,sort_keys=True)+"\n");print(res,flush=True)
    finally:e.lib.finish(state)
if __name__=="__main__":main()
