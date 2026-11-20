#!/usr/bin/env python3
"""Test canonical rectangle consistency after fixing either actual S028 nonidentity star."""
import argparse
from collections import Counter,defaultdict
from itertools import combinations
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import numpy as np


def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def solve(field,native,z,Y):
    R,C,X,A=z;inv=field.invert_and_price(R)[0];top=C.copy();split=Y.reshape(8,480,-1);rhs=split[0].copy();u=[field.mm(inv,x)for x in split[1:]];v=[field.mm(inv,x)for x in A]
    for e in range(7):top^=field.mm(X[e],v[e]);rhs^=field.mm(X[e],u[e])
    center=field.mm(field.invert_and_price(top)[0],rhs);out=np.vstack([center]+[u[e]^field.mm(v[e],center)for e in range(7)])
    if not np.array_equal(native.apply(field,z,out),Y):raise ValueError('actual native inversion of every probe column')
    return out


def project(field,s,program,j,i,L,X,transpose):
    mm=field.mm;idx=s['adj'][i].index(j);E=s['E'][i][idx];B=s['B'][i][idx];V,S=s['VS'][i];F=X.reshape(8,480,-1);rim,_,cross=program;updates=s['updates'].get(i,{});e=1;rows=np.arange(80)
    if not transpose:
        early=mm(E,F[e]);out=mm(V[rows],mm(B,F[e])^mm(S,early));late=mm(rim,F[e])
        for (g,f),(a,b)in cross.items():
            if g==e:late^=mm(a,mm(b,F[f]))
        out^=mm(L[rows],late)
        for (g,f),(ids,M)in updates.items():
            if g!=e:continue
            take=np.flatnonzero(ids<80)
            if len(take):out[ids[take]]^=mm(M[take],mm(E,F[f]))
        return out
    v=mm(V.T,F[e]);out=mm(B[:,rows].T,v);early=mm(S.T,v);out^=mm(rim[:,rows].T,mm(L.T,F[e]))
    for (g,f),(ids,M)in updates.items():
        if f==e:early^=mm(M.T,F[g][ids])
    out^=mm(E[:,rows].T,early)
    for (g,f),(a,b)in cross.items():
        if f==e:out^=mm(b[:,rows].T,mm(a.T,mm(L.T,F[g])))
    return out


def screen(state,field,first,native,program,late,transposed):
    A=state['adj'];center=10 if transposed else 80;test=first.coefficients(f'native endpoint cycle controls/{int(transposed)}',(3840,80));images=defaultdict(dict);crosschecks=0
    def native_block(i,j):return native.whole(field,state,i,j,late[j][A[j].index(i)],program[j])
    for ix,leaf in enumerate(A[center]):
        z=native.adjoint(native_block(leaf,center)) if transposed else native_block(center,leaf);T=solve(field,native,z,test)
        for v in A[leaf]:
            if v==center:continue
            i,j=(leaf,v)if transposed else(v,leaf);M=project(field,state,program[j],j,i,late[j][A[j].index(i)],T,transposed);images[v][leaf]=M
            if v==A[leaf][0] and ix%10==0:
                actual=native_block(i,j);direct=native.apply(field,native.adjoint(actual)if transposed else actual,T)[480:560]
                if not np.array_equal(M,direct):raise ValueError('direct original-component forward/adjoint control')
                crosschecks+=1
    hist=Counter();digest=hashlib.sha256();sizes={v:len(items)for v,items in images.items()}
    for v,items in sorted(images.items()):
        for j,k in combinations(sorted(items),2):
            r=field.rank(items[j]^items[k]);hist[r]+=1;digest.update(bytes((v,j,k,r)))
    if min(hist)<=64:raise ValueError('a canonical bridge pair survived the original-area necessary inequality')
    return {'transpose':transposed,'role':center,'observed_sites':len(images),'canonical_anchor_bridges':sum(sizes.values()),'bridge_pairs':sum(hist.values()),'compressed_rank_hist':hist,'failures':[],'sha':digest.hexdigest(),'direct_physical_probe_checks':crosschecks,'counts':sizes}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for n in ('bilateral-author','star-author','target-author','flat-author','cache-dir','late-cache','source-cache'):p.add_argument('--'+n,type=Path)
    a=p.parse_args();res=a.repo/'research/moonshot-005-program/results';bil=a.bilateral_author or res/'bit-global-source-facet-row-column/author';star=a.star_author or res/'bit-global-two-star-target/author';sys.path.insert(0,str(bil.resolve()));pre=module(bil/'check.py','physical_bilateral');native=module(star/'native.py','actual_endpoint_words');params=json.loads((bil/'output/PARAMETERS.json').read_text());pins=json.loads((star/'output/SOURCE-PINS.json').read_text())
    with tempfile.TemporaryDirectory(prefix='anchored-native-')as td:
        first,_,field,_,state,after=pre.setup(a,Path(td));minor=np.eye(12*480,dtype=np.uint8);program={};late={}
        for j in range(111):
            program[j]=native.cached(a.source_cache/f'{j:03}.npz') if a.source_cache else pre.donor.verify_donor(j,field,first.coefficients,state,params,after,minor)[1]
            late[j]=np.load(after/f'L{j}.npy',mmap_mode='r',allow_pickle=False)
            if native.source_pin(*program[j])!=pins[str(j)] or hashlib.sha256(late[j]).hexdigest()!=params['donors'][str(j)]['late_transfer_sha256']:raise ValueError('original native source/late response coefficient pin')
        A=state['adj'];terms=state['terms'];X={(80,j)for j in A[80]};Y={(i,10)for i in A[10]}
        if set(terms)!=X|Y or not all(terms[t][0]==0 for t in X) or not all(terms[t][1]==0 for t in Y):raise ValueError('common original bank of the two native stars')
        output=[screen(state,field,first,native,program,late,t)for t in (False,True)]
        num_intersect=sum(len(set(A[i])&set(A[80]))for i in A[10]);union=sum(o['canonical_anchor_bridges']for o in output)-num_intersect
        cap=(111-1-len(A[10]))+(111-1-len(A[80]))+min(len(A[10]),len(A[80]))
        receipt={'status':'PASS_FIXED_NATIVE_STAR_ARBITRARY_ENDPOINT_BIJECTION_CONSISTENCY_EXCLUSION','original_nonflat_edges':123,'verified_canonical_rectangle_pairs':sum(o['bridge_pairs']for o in output),'true_target_difference_rank_upper':64,'native_projected_difference_rank_lower':min(min(o['compressed_rank_hist'])for o in output),'intersection_canonical_edges':num_intersect,'union_canonical_edges':union,'max_canonical_exact_in_union_if_all_nonflat_exact':cap,'unavoidable_failed_whole_target_edges_in_union':union-cap,'word_scope':'fixed physical bilateral word, allowing arbitrary local endpoint bijections','directional_census':output,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print('PASS',receipt['verified_canonical_rectangle_pairs'],union,cap)

if __name__=='__main__':main()
