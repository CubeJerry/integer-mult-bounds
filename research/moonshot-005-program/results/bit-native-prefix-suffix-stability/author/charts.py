#!/usr/bin/env python3
"""Reproduce every weighted chart inequality from the actual RS spread and primary data."""
import argparse,ctypes,gzip,json,sys
from collections import Counter
from functools import lru_cache
from pathlib import Path
import numpy as np

def replay(a):
    atlas=Atlas(a.repo,a.k,a.d_charts,a.library);alg=Arithmetic(a.rank_library.resolve())
    lib=ctypes.CDLL(str(a.rank_library.resolve()));f=lib.field_rank
    f.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p];f.restype=ctypes.c_int
    def rank(matrix):
        data=np.array(matrix,copy=True,dtype=np.uint8,order='C')
        return f(data.ctypes.data,len(data),data.shape[1],TABLE.ctypes.data,INV.ctypes.data)
    w=json.loads(gzip.decompress(a.weighted.read_bytes()));cost={tuple(x):0 for x in w['tree']}
    for i,*_,c in w['closure']:cost[divmod(i,111)]=c
    native=set(range(111));other=[atlas.D[atlas.dual[d]]for d in range(len(atlas.D))]
    atlas.left=lru_cache(111)(atlas.left);atlas.right=lru_cache(111)(atlas.right)
    @lru_cache(maxsize=800)
    def inverse_cut(side,u,j,small):
        s,g=(atlas.D,other)if side=='L'else(other,atlas.D)
        ids=[d for d,ss in enumerate(s) if u in ss and j in g[d] and (d in atlas.marked)==small]
        table=atlas.left(u) if side=='L' else atlas.right(u)
        part=slice(0,96) if small else slice(96,480)
        mat=np.stack([table[t][part] for d in ids for t in atlas.middle[d,'X']+atlas.middle[d,'Y'] if t in table])
        iv=alg.inverse(mat);return {d:iv[:,8*k:8*k+8]for k,d in enumerate(ids)}
    seen=set();records=json.loads(gzip.decompress(a.charts.read_bytes()))
    for w in records:
        side=w['side'];h=w['plane']
        if a.side and side!=a.side:continue
        audit=(side,h,tuple(w['pair']));assert audit not in seen;seen.add(audit);s,g=(atlas.D,other)if side=='L'else(other,atlas.D)
        u,v=w['pair'];J=w['opposite'];assert len(J)==len(set(J))==8 and u!=v and {u,v}<=atlas.H[h]&native
        assert set(J)<=atlas.orth[u]&atlas.orth[v]&native
        def edge(z,j):return cost[j,z] if side=='L'else cost[z,j]
        assert sum(edge(u,j)+edge(v,j)for j in J)==w['cost']
        ds=[d for d,S in enumerate(s)if u in S and v in S]
        labels=[(j,d)for j in J for d in ds if j in g[d]]
        assert len(labels)==120 and Counter(d for j,d in labels)=={int(k):m for k,m in w['chart_multiplicities'].items()}
        rows=[]
        for small in (True,False):
            AA=[]
            for z in (u,v):
                data=[]
                for j,d in labels:
                    if (d in atlas.marked)!=small:continue
                    rec,don=(j,z)if side=='L'else(z,j);B,owners=atlas.middle_matrix(d)
                    rx=[k for k,t in enumerate(owners) if atlas.route[t][5]in atlas.ks[rec]]
                    tx=[k for k,t in enumerate(owners) if atlas.route[t][3]in atlas.ks[don]];assert len(rx)==len(tx)==8
                    invC=alg.inverse(B[np.ix_(rx,tx)]);Z=inverse_cut(side,z,j,small)[d]
                    data.append(atlas.ops.matmul(Z,invC).T if side=='L'else atlas.ops.matmul(invC,Z.T))
                AA.append(np.vstack(data))
            rows.append([rank(AA[0]),rank(AA[1]),rank(np.hstack(AA))])
        assert rows==w['sector_ranks'],(side,h,rows)
    print('Replayed',len(seen),'actual chart constraints')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','h-author','k','d-charts','library','rank-library','weighted','charts','fast-author'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--side',choices=('L','R'));a=p.parse_args();sys.path.insert(0,str(a.fast_author));sys.path.insert(0,str(a.h_author))
    from transfer import Atlas,TABLE,INV
    from fast import Arithmetic
    replay(a)
