#!/usr/bin/env python3
"""Exact 480-coordinate response of the all-RS spread proper word."""
from __future__ import annotations
import argparse,ctypes,gzip,hashlib,json
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import numpy as np
from build import COPIES,PRODUCT,field_rank,grouped_sources,power,require,unpack
from rs_source import SINGLETON_SCALE,coefficients,source_slot
from terminal import K_PINS,k_row,payload

TABLE=np.asarray(PRODUCT,dtype=np.uint8)
D_PIN="9e2fbdb0a1ec95926903b65acea48b7428f1a2bf0c8233271ac655d76e630e15"
INV=np.array([0]+[power(x,62) for x in range(1,64)],dtype=np.uint8)
BODY=480


class Arithmetic:
    def __init__(self,library=None):
        self.native=None
        if library:
            self.native=ctypes.CDLL(str(Path(library).resolve())).gf64_gemm
            self.native.argtypes=[ctypes.c_void_p]*4+[ctypes.c_size_t]*3
            self.native.restype=None

    def matmul(self,a,b):
        a=np.ascontiguousarray(a,dtype=np.uint8)
        b=np.ascontiguousarray(b,dtype=np.uint8)
        require(a.ndim==2 and b.ndim==2 and a.shape[1]==b.shape[0],"compatible GF factors")
        out=np.zeros((len(a),b.shape[1]),dtype=np.uint8)
        if self.native is not None:
            self.native(a.ctypes.data,b.ctypes.data,out.ctypes.data,TABLE.ctypes.data,
                        len(a),a.shape[1],b.shape[1])
        else:
            for k in range(a.shape[1]):
                out^=TABLE[a[:,k,None],b[k,None,:]]
        return out


class Atlas:
    """Use factors(i,j) for R, D[60,8,8], L in the same actual D boundary orders."""
    def __init__(self,repo,k_words,d_charts,library=None):
        self.ops=Arithmetic(library)
        base=Path(repo)/"research/moonshot-005-program/results"
        geo=json.loads(unpack(base,"geometry")); self.H=list(map(set,geo["A2"])); self.D=list(map(set,geo["D4"]))
        self.dual=geo["dual_D4"];roots=geo["root_table"]
        self.orth=[{j for j,y in enumerate(roots)if sum(a*b for a,b in zip(x,y))==0}for x in roots]
        self.marked=set(json.loads(unpack(base,"spread"))["selected_D"])
        self.phase=json.loads(unpack(base,"phases"))
        self.ks={i:[h for h,p in enumerate(self.H)if i in p]for i in range(111)}
        self.nodes={(i,h):s+1 for i,hs in self.ks.items()for s,h in enumerate(hs)}
        self.colours={}
        for j,hs in self.ks.items():
            self.colours[j]={"singleton":{h for h in hs if self.phase[str(h)]["m"]==1},
                             "first":set([h for h in hs if self.phase[str(h)]["donor_early"][str(j)]==15][:12])}
        self.route={};self.left_flags=defaultdict(list);self.middle=defaultdict(list)
        for l in unpack(base,"routes").splitlines():
            r=json.loads(l); phase,role,local,h,d,k,_,_=r
            fid=(53280 if phase=="Y" else 0)+480*role+local
            self.route[fid]=r; self.middle[d,phase].append(fid)
            if h is not None:self.left_flags[h,d,phase].append(fid)
        for flags in (self.left_flags,self.middle):
            for owners in flags.values():owners.sort()
        ds=defaultdict(set)
        for h,d,_ in self.left_flags:ds[h].add(d)
        self.h_ports={h:([d for d in sorted(ports)if d in self.marked],
                         [d for d in sorted(ports)if d not in self.marked]) for h,ports in ds.items()}
        self.kr=payload(Path(k_words)/"SPREAD-OWNERS.json.gz",K_PINS["spread"])
        self.dp=payload(Path(d_charts),D_PIN)
