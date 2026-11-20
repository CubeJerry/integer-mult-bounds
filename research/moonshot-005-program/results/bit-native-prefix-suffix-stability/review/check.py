#!/usr/bin/env python3
"""Rebuild both rank obstructions by pushing independent literal delta packets."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np

def replay(a):
    sp=importlib.util.spec_from_file_location('independent_canonical',a.canonical/'check.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
    alg=r.load_replay(a.replay);eng=r.Engine(a.stream_lib);alg.mm=eng.mm
    n=alg.Native(a);eye=np.eye(480,dtype=np.uint8);out={}
    def inv(m):
        aug=np.hstack([m,eye]);cols=len(m)
        for k in range(cols):
            hits=np.flatnonzero(aug[k:,k]);assert len(hits)
            z=k+int(hits[0]);aug[[k,z]]=aug[[z,k]]
            aug[k]=alg.MUL[alg.INV[aug[k,k]],aug[k]];mult=aug[:,k].copy();mult[k]=0
            aug^=alg.MUL[mult[:,None],aug[k]]
        assert np.array_equal(aug[:,:cols],eye)
        return aug[:,cols:]
    def rank(m):
        m=np.ascontiguousarray(m);lib=eng.lib;ctx=lib.begin(m.shape[1])
        try:
            assert lib.consume(ctx,m.ctypes.data,len(m))==1
            return int(lib.present_rank(ctx))
        finally:lib.finish(ctx)
    def visible(i,j):return [d for d,ss in enumerate(n.D) if j in ss and i in n.D[n.dual[d]]]
    def lanes(d,h,j):return [u for u in n.byd[d]['X']+n.byd[d]['Y'] if n.rt[u][h] in n.planes[j]]
    suffix=json.loads((a.author/'RESULT.json').read_text());prefix=json.loads((a.author/'PREFIX.json').read_text())
    def output(k,AA,expected):
        hashes=[hashlib.sha256(x.tobytes()).hexdigest() for x in AA]
        assert hashes==expected,(k,hashes,expected)
        ranks=[rank(x)for x in AA]+[rank(np.hstack(AA))];assert ranks==[480,480,960]
        out[k]={'forward_owner_stack_sha256':hashes,'independent_reciprocal_field_ranks':ranks}
    js=prefix['donors'];obs=prefix['receivers'];labels=[(i,d)for i in obs for d in visible(i,js[0]) if js[1] in n.D[d]];AA=[]
    for j in js:
        dv=n.through_d(j,obs);blocks={}
        for i in obs:
            ds=visible(i,j);M=inv(np.vstack([dv[u]for d in ds for u in lanes(d,5,i)]))
            for k,d in enumerate(ds):blocks[i,d]=M[:,8*k:8*k+8].T
        AA.append(np.vstack([blocks[x]for x in labels]))
    output('prefix',AA,prefix['matrix_sha256']);print('prefix independent',flush=True)
    def through_middle(i,j):
        ds=visible(i,j);dv={};pos=0
        for d in ds:
            _,m,nn,w=n.dword[d];xs=n.byd[d]['X'];ys=n.byd[d]['Y'];source={u:eye[pos+k]for k,u in enumerate(lanes(d,3,j))};pos+=8
            X,Y=alg.at(source,xs),alg.at(source,ys);ex=eng.mm(alg.cauchy(range(m),range(m)),X);ly=eng.mm(alg.cauchy(range(nn),range(nn)),Y)
            b=len(w)
            if b:
                cache=eng.mm(alg.cauchy(range(m,m+b),range(m)),X);cache=alg.MUL[np.asarray(w,dtype=np.uint8)[:,None],cache]
                ly^=eng.mm(alg.cauchy(range(nn),range(nn,nn+b)),cache)
            dv.update(zip(xs,ex));dv.update(zip(ys,ly))
        assert pos==480
        return ds,dv
    u,v=suffix['receivers'];J=suffix['donors'];labels=[(j,d)for j in J for d in visible(u,j)if v in n.D[n.dual[d]]]
    stacks={k:[]for k in suffix['tests']}
    for i in (u,v):
        blocks={k:{} for k in stacks}
        for j in J:
            ds,dv=through_middle(i,j)
            for mode in ('spread','mixed'):
                _,_,rs,minimum=n.facet(dv,i,mode)
                for kind,m in [('rs',rs),('min',minimum)]:
                    key=mode+'_'+kind;iv=inv(m)
                    for k,d in enumerate(ds):blocks[key][j,d]=iv[8*k:8*k+8]
        for key in stacks:stacks[key].append(np.vstack([blocks[key][x]for x in labels]))
    for key,AA in stacks.items():output(key,AA,suffix['tests'][key]['native_matrix_sha256']);print(key,'independent',flush=True)
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('canonical','replay','repo','h-words','d-words','k-words','f-words','stream-lib','author','out'):p.add_argument('--'+k,type=Path,required=True)
    replay(p.parse_args())
