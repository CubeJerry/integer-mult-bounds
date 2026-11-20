#!/usr/bin/env python3
"""Test every all-canonical proper 4-cycle, allowing arbitrary original-site endpoint bijections."""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
import check as local

H,W=76,71


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--probe-cache',type=Path)
    for n in ('bilateral-author','star-author','target-author','flat-author','cache-dir','late-cache','source-cache'):p.add_argument('--'+n,type=Path)
    a=p.parse_args();home=Path(__file__).resolve().parent;res=a.repo/'research/moonshot-005-program/results';bil=a.bilateral_author or res/'bit-global-source-facet-row-column/author';star=a.star_author or res/'bit-global-two-star-target/author';flat=a.flat_author or res/'bit-global-facet-shared-coordinates/author';sys.path.insert(0,str(bil.resolve()));pre=local.module(bil/'check.py','native_bilateral');native=local.module(star/'native.py','native_star');params=json.loads((bil/'output/PARAMETERS.json').read_text());pins=json.loads((star/'output/SOURCE-PINS.json').read_text())
    with tempfile.TemporaryDirectory(prefix='all-flat-native-cycles-')as td:
        temp=Path(td);first,_,field,_,s,late=pre.setup(a,temp);A=s['adj'];active=s['terms'];sets=[set(j for j in js if (i,j)not in active)for i,js in enumerate(A)]
        order=[[i,k,sorted(sets[i]&sets[k])]for i in range(111)for k in range(i+1,111)if sets[i]&sets[k]];order_sha=hashlib.sha256(json.dumps(order).encode()).hexdigest();left={};right={};mat=None
        if a.probe_cache:mat=np.load(a.probe_cache,mmap_mode='r',allow_pickle=False)
        else:
            dummy=np.eye(5760,dtype=np.uint8)
            for j in range(111):
                src=native.cached(a.source_cache/f'{j:03}.npz')if a.source_cache else pre.donor.verify_donor(j,field,first.coefficients,s,params,late,dummy)[1];Ls=np.load(late/f'L{j}.npy',mmap_mode='r')
                if native.source_pin(*src)!=pins[str(j)] or hashlib.sha256(Ls).hexdigest()!=params['donors'][str(j)]['late_transfer_sha256']:raise ValueError('authentic native source/late physical transfer')
                for ii,i in enumerate(A[j]):
                    if j not in sets[i]:continue
                    n=A[i].index(j);V,S=s['VS'][i];R=field.mm(V,s['B'][i][n]^field.mm(S,s['E'][i][n]))^field.mm(Ls[ii],src[0]);inv,_=field.invert_and_price(R);left[i,j]=R[:H].copy();right[i,j]=inv[:,:W].copy()
        lib=temp/'rankpairs.so';subprocess.run(['cc','-O3','-march=native','-shared','-fPIC','-I',str(flat),str(home/'pair_rank.c'),'-o',str(lib)],check=True);fn=ctypes.CDLL(str(lib)).screen_deltas;ptr=ctypes.c_void_p;size=ctypes.c_size_t;fn.argtypes=[ptr,size,size,size,ptr,ptr,size,size,ptr];fn.restype=size;hist=np.zeros(W+1,dtype=np.uint64);start=0;count=0;digest=hashlib.sha256()
        for i,k,js in order:
            if mat is None:records=np.stack([field.mm(left[i,j],right[k,j])for j in js])
            else:records=mat[start:start+len(js)]
            start+=len(js);digest.update(records);small=np.zeros(W+1,dtype=np.uint64);count+=fn(records.ctypes.data,len(js),H,W,field.product.ctypes.data,field.inv.ctypes.data,0,1,small.ctypes.data);hist+=small
        if mat is not None and start!=len(mat):raise ValueError('improper number of native probe arrays')
        if np.any(hist[:69]) or count!=sum(len(v)*(len(v)-1)//2 for _,_,v in order):raise ValueError('unresolved genuine canonical rectangle')
        minimum=int(np.flatnonzero(hist)[0]);digest=digest.hexdigest();pin=json.loads((home/'output/ALL-FLAT-INPUT.json').read_text())
        if digest!=pin['array_sha'] or order_sha!=pin['assignment_sha']:raise ValueError('authentic native projected arrays or canonical edge order')
        # For 111 left and right sites, 111*binom(11,2)=binom(111,2). Any 1,222nd edge forces a repeated pair.
        upper=111*11;canonical=sum(map(len,sets));result={'status':'PASS_UNCONDITIONAL_FOUR_CYCLE_FREE_EXACT_CANONICAL_EDGE_GRAPH_FOR_FIXED_PHYSICAL_WORD','canonical_target_edges':canonical,'original_receiver_pairs':len(order),'all_canonical_native_4_cycles':count,'native_rim_projected_difference_rank_histogram':{str(i):int(n)for i,n in enumerate(hist)if n},'true_2_by_2_full_rank_lower_each_cycle':7*(480+minimum),'required_2_by_2_rank_for_four_canonical_edges':3840,'simultaneously_correct_whole_flat_blocks_upper':upper,'unavoidable_wrong_whole_flat_blocks':canonical-upper,'simultaneously_correct_entire_native_blocks_upper':upper+len(active),'target_nonflat_edges_may_be_arbitrary':True,'native_array_sha256':digest,'original_edge_order_sha256':order_sha,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'ALL-FLAT-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('PASS',count,canonical-upper,'unconditional canonical failures')

if __name__=='__main__':main()
