"""Compile the exact packed E24 terminal matrices on the earlier admitted eight true copies."""
import argparse
from collections import Counter
import ctypes
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import importlib.util
_spec = importlib.util.spec_from_file_location("packed_terminal_build", Path(__file__).with_name("build.py"))
_packed = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_packed)
Field, need = _packed.Field, _packed.need
from make_field import make,mul


def perm(sw):
    n=len(sw);seen=set();cycles=0
    need(sorted(sw)==list(range(n)),'actual native terminal labelling')
    for r in range(n):
        if r in seen:continue
        cycles+=1;v=r
        while v not in seen:seen.add(v);v=sw[v]
    return n-cycles


def main():
    ap=argparse.ArgumentParser()
    for t in ('repo','transfer','k-words','d-charts','mult','packed','small','large','out'):ap.add_argument('--'+t,type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(a.transfer.resolve()));from transfer import Atlas
    at=Atlas(a.repo,a.k_words,a.d_charts,a.mult);field=Field(a.packed);desc=make();basis=np.array(desc['native_basis'],dtype=np.uint32)
    transforms=[]
    for e in basis:
        cols=[int(field.change(np.array(mul(int(e),1<<c,field.poly),dtype=np.uint32),field.bwd)) for c in range(24)]
        transforms.append(field.lookup(cols))
    t=np.ascontiguousarray(transforms,dtype=np.uint32);qty=np.zeros(1<<24,dtype=np.uint16)
    ptr=ctypes.c_void_p;field.lib.all_prices.argtypes=[ptr,ptr];field.lib.all_prices.restype=None
    field.lib.all_prices(t.ctypes.data,qty.ctypes.data);need(qty[1]==24 and qty[0]==0,'native direct ADD counts')
    field.lib.price24.argtypes=[ptr,ctypes.c_size_t,ptr,ptr,ptr,ptr];field.lib.price24.restype=ctypes.c_uint64
    receipt={};whole=Counter();allforeign=0
    for i in range(111):
        ei,ec,yi,yc=at.facet(i);native=[None]*3840;local=Counter()
        for folder,lo,hi in [(a.small,0,96),(a.large,96,480)]:
            rec=json.loads((folder/f'F{i:03}.json').read_bytes());payload=(folder/f'F{i:03}.bin').read_bytes()
            need(rec['actual_GF24_terminal_word_SHA256']==hashlib.sha256(payload).hexdigest(),'actual physical matrix checksum')
            w=hi-lo;e=rec['early_count'];m=rec['preterminal_count'];sel=np.flatnonzero(np.any(yc[lo:hi],axis=0))
            need(len(sel)==w and len(np.flatnonzero(np.any(ec[lo:hi],axis=0)))==e,'authenticated native X/Y groups')
            b=np.frombuffer(payload,dtype=np.uint8).reshape(w,m,3).astype(np.uint32);F=b[:,:,0]|(b[:,:,1]<<8)|(b[:,:,2]<<16)
            W=F[:,e:].copy();stats=np.zeros(3,dtype=np.uint64)
            charge=field.lib.price24(W.ctypes.data,w,qty.ctypes.data,basis.ctypes.data,field.bwd.ctypes.data,stats.ctypes.data)
            need(np.array_equal(W,np.eye(w,dtype=np.uint32)),'literal E24 pure F elimination')
            local['pure_F_ADD']+=2*int(charge);local['early_to_late_ADD']+=2*int(qty[F[:,:e]].sum(dtype=np.int64))
            local['stationary_original_copy_ADD_INIT_dirty_CLEAR']+=2*24*e
            for span,raw in enumerate(sel):
                orig=yi[raw]-(53280+480*i);need(orig in range(480),'true final Y')
                for copy in range(8):native[orig*8+copy]=(0 if lo==0 else 768)+copy*w+span
            allforeign+=len(rec['actual_foreign_nonzero_determinants'])
        local['F_final_owner_permutation_ADD']=18*perm(native)
        local['Ground_inverse_ADD']=local['pure_F_ADD']+local['F_final_owner_permutation_ADD']
        local['actual_F_total_ADD']=sum(local.values());whole.update(local);receipt[i]=dict(local)
    need(allforeign==12940 and whole['stationary_original_copy_ADD_INIT_dirty_CLEAR']==1926000,'all actual donors and records')
    out={'whole_atlas':dict(whole),'facets':receipt,'all_protected_sector_determinants':allforeign,'extra_MOVE':0,'native_nullity_at_least':6720,
         'standalone_native_return_rank_at_most':419520,'field_components':'two disjoint E24 groups, each four actual six-bit original owner copies'}
    (a.out/'PRICE.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['whole_atlas'],flush=True)


if __name__=='__main__':main()
