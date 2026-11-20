#!/usr/bin/env python3
"""Check every pair of 1,956 original core-to-core edges against both fixed nonidentity stars."""
import argparse
import ctypes
import hashlib
import json
from multiprocessing import Pool
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
import check as local


HEIGHT=134
WIDTH=130


def prepare(field,first,state,native,program,late):
    A=state['adj'];out=first.coefficients('complete nonflat bridge output probe',(3840,HEIGHT));inp=first.coefficients('complete nonflat bridge input probe',(3840,WIDTH));left={};right={};mm=field.mm
    def block(i,j):return native.whole(field,state,i,j,late[j][A[j].index(i)],program[j])
    for i in A[10]:
        Y=local.solve(field,native,native.adjoint(block(i,10)),out).reshape(8,480,-1);V,S=state['VS'][i];D=[mm(V.T,y)for y in Y];E=[mm(S.T,d)for d in D]
        for (g,f),(ids,M)in state['updates'].get(i,{}).items():E[f]^=mm(M.T,Y[g][ids])
        left[i]=Y,D,E
    for j in A[80]:
        X=local.solve(field,native,block(80,j),inp).reshape(8,480,-1);rim,center,cross=program[j];ls=[mm(center if g==0 else rim,x)for g,x in enumerate(X)]
        for (g,f),(h,r)in cross.items():ls[g]^=mm(h,mm(r,X[f]))
        right[j]=X,ls
    mats=[];sites=[]
    for n,(i,(Y,D,E)) in enumerate(left.items()):
        for j in sorted(set(right)&set(A[i])):
            k=A[i].index(j);B=state['B'][i][k];early=state['E'][i][k];L=late[j][A[j].index(i)];X,lr=right[j];M=np.zeros((HEIGHT,WIDTH),dtype=np.uint8)
            for e in range(8):M^=mm(D[e].T,mm(B,X[e]))^mm(E[e].T,mm(early,X[e]))^mm(Y[e].T,mm(L,lr[e]))
            if len(sites)%401==0:
                direct=mm(Y.reshape(3840,-1).T,native.apply(field,block(i,j),X.reshape(3840,-1)))
                if not np.array_equal(M,direct):raise ValueError('direct full native product crosscheck')
            mats.append(M);sites.append((i,j))
    return np.stack(mats),np.array(sites,dtype=np.uint8)


def subgroup(arg):
    array,lib_path,table_path,inv_path,k,m=arg;d=np.load(array,mmap_mode='r');table=np.load(table_path);inv=np.load(inv_path);fn=ctypes.CDLL(str(lib_path)).screen_deltas;ptr=ctypes.c_void_p;size=ctypes.c_size_t;fn.argtypes=[ptr,size,size,size,ptr,ptr,size,size,ptr];fn.restype=size;hist=np.zeros(WIDTH+1,dtype=np.uint64);n=fn(d.ctypes.data,len(d),HEIGHT,WIDTH,table.ctypes.data,inv.ctypes.data,k,m,hist.ctypes.data)
    if int(sum(hist))!=n:raise ValueError('pair count')
    return list(map(int,hist))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--jobs',type=int,default=4);p.add_argument('--probe-cache',type=Path)
    for n in ('bilateral-author','star-author','target-author','flat-author','cache-dir','late-cache','source-cache'):p.add_argument('--'+n,type=Path)
    a=p.parse_args();base=Path(__file__).resolve().parent;res=a.repo/'research/moonshot-005-program/results';bil=a.bilateral_author or res/'bit-global-source-facet-row-column/author';star=a.star_author or res/'bit-global-two-star-target/author';flat=a.flat_author or res/'bit-global-facet-shared-coordinates/author';sys.path.insert(0,str(bil.resolve()));pre=local.module(bil/'check.py','native_bilateral');native=local.module(star/'native.py','native_star');params=json.loads((bil/'output/PARAMETERS.json').read_text());pins=json.loads((star/'output/SOURCE-PINS.json').read_text());evidence=json.loads((base/'output/DOUBLE-INPUT.json').read_text())
    with tempfile.TemporaryDirectory(prefix='two-star-rectangle-')as td:
        temp=Path(td);first,_,field,_,state,after=pre.setup(a,temp);arr=(a.probe_cache or temp/'rectangle.npy');sites=[(i,j)for i in state['adj'][10]for j in sorted(set(state['adj'][i])&set(state['adj'][80]))];site_hash=hashlib.sha256(np.array(sites,dtype=np.uint8)).hexdigest()
        if not arr.is_file():
            src={};late={};minor=np.eye(5760,dtype=np.uint8)
            for j in range(111):
                src[j]=native.cached(a.source_cache/f'{j:03}.npz')if a.source_cache else pre.donor.verify_donor(j,field,first.coefficients,state,params,after,minor)[1];late[j]=np.load(after/f'L{j}.npy',mmap_mode='r')
                if native.source_pin(*src[j])!=pins[str(j)] or hashlib.sha256(late[j]).hexdigest()!=params['donors'][str(j)]['late_transfer_sha256']:raise ValueError('native two-sided source pin')
            M,J=prepare(field,first,state,native,src,late);np.save(arr,M)
            if not np.array_equal(J,np.array(sites,dtype=np.uint8)):raise ValueError('original order of native rectangle edges')
        actual=np.load(arr,mmap_mode='r');digest=hashlib.sha256(actual).hexdigest()
        if digest!=evidence['sha'] or site_hash!=evidence['ids_sha']or actual.shape!=(len(sites),HEIGHT,WIDTH):raise ValueError('complete two-star physical coefficients and edge order')
        lib=temp/'pairs.so';subprocess.run(['cc','-O3','-march=native','-shared','-fPIC','-I',str(flat),str(base/'pair_rank.c'),'-o',str(lib)],check=True);t=temp/'table.npy';iv=temp/'inv.npy';np.save(t,field.product);np.save(iv,field.inv)
        groups=4*max(1,a.jobs);jobs=[(arr,lib,t,iv,k,groups)for k in range(groups)]
        with Pool(max(1,a.jobs))as workers:hist=np.array(workers.map(subgroup,jobs),dtype=np.uint64).sum(axis=0)
        if int(sum(hist))!=len(sites)*(len(sites)-1)//2 or np.any(hist[:129]):raise ValueError('complete whole-target collision or missing pair')
        result={'status':'PASS_AT_MOST_ONE_CANONICAL_BRIDGE_BETWEEN_COMPLETE_NONFLAT_STARS','core_native_edges':len(sites),'pairwise_native_comparisons':int(sum(hist)),'native_projected_difference_rank_histogram':{str(i):int(n)for i,n in enumerate(hist)if n},'target_difference_rank_upper':128,'native_probe_matrix_sha256':digest,'native_edge_order_sha256':site_hash,'certified_exact_bridges_upper':1,'whole_canonical_union_edges':5055,'sharp_maximum_whole_canonical_edges_in_union':98,'unavoidable_whole_target_failures_in_union':4957,'remaining_global_whole_targets_upper':1513,'endpoint_map_class':'arbitrary original-site bijections, fixed native bilateral internal word','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'DOUBLE-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('PASS',len(sites),int(sum(hist)),result['sharp_maximum_whole_canonical_edges_in_union'])

if __name__=='__main__':main()
