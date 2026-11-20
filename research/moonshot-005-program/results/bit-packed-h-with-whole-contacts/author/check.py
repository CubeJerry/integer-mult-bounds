#!/usr/bin/env python3
"""Synthesize common original inputs and receiver maps with 31 packed H charts and 51 entire contacts."""
import argparse,hashlib,json,sys
from pathlib import Path
from collections import Counter
from functools import lru_cache
import numpy as np
from panels import module,obtain

def target(i,j,k):
    I=np.eye(32*k,dtype=np.uint8)
    if k==12 or (i!=80 and j!=10):return I
    dest,src=(0,2) if (i,j)==(80,2) else (1,0)
    assert (i,j)in ((80,2),(0,10))
    for half in range(2):
        for t in range(4):I[half*48+4*dest+t,half*48+4*src+t]^=1
    return I

def verify(a):
    at=Atlas(a.repo,a.k_words,a.d_charts,a.library);at.left=lru_cache(111)(at.left);at.right=lru_cache(111)(at.right);mm=at.ops.matmul
    hs,live,L,Z=obtain(a,at,inv);ass={int(j):ii for j,ii in json.loads(a.assignment.read_text()).items()}
    packed={j for h in hs for j in at.H[h]};assert len(packed)==78 and set(ass)==set(range(111))-packed-{10}
    observers={i:j for j,ii in ass.items()for i in ii};assert len(observers)==sum(map(len,ass.values()))==49 and 0 not in observers and 80 not in observers
    previous=json.loads((a.packed_endpoint/'output/RESULT.json').read_text());base=json.loads(a.baseline_source.read_text())
    original=json.loads((a.repo/'research/moonshot-005-program/results/bit-two-sided-covariant-target/author/output/ASSIGNMENT.json').read_text())
    assert [80,2,2]in original['row_transfers']and [0,10,1]in original['column_transfers']
    @lru_cache(100)
    def block(i,j):
        assert i!=j and j in at.orth[i];M=at.block(i,j)
        assert not M[:96,96:].any()and not M[96:,:96].any()
        return M[:96,:96],M[96:,96:]
    O={};G={};costO={};costG={};out={};joint=hashlib.sha256()
    for k in (3,12):
        q=(k==12);eye=np.eye(32*k,dtype=np.uint8)
        for j,ii in ass.items():
            D=np.hstack([L[i,k]for i in ii]);T=np.hstack([mm(inv(block(i,j)[q]),Z[i,k])for i in ii])
            assert rank_fast(D)==rank_fast(T)==D.shape[1]
            G[j,k]=mm(extend_rows(T.T),inv(extend_rows(D.T)))
            assert np.array_equal(mm(G[j,k],D),T)
        for i in range(111):
            if i in observers:
                j=observers[i];O[i,k]=inv(mm(block(i,j)[q],G[j,k]))
            elif i==80:
                O[i,k]=mm(target(80,2,k),inv(mm(block(80,2)[q],G[2,k])))
            else:
                O[i,k]=mm(extend_rows(L[i,k].T),inv(extend_rows(Z[i,k].T)))
            if i!=80:
                assert np.array_equal(mm(O[i,k],Z[i,k]),L[i,k])
            assert rank_fast(O[i,k])==32*k
        G[10,k]=mm(inv(mm(O[0,k],block(0,10)[q])),target(0,10,k))
        for i,j in sorted(list(observers.items())+[(80,2),(0,10)]):
            A=mm(mm(O[i,k],block(i,j)[q]),G[j,k]);assert np.array_equal(A,target(i,j,k))
            joint.update(bytes([i,j,k]));joint.update(A.tobytes())
    hashm=lambda m:hashlib.sha256(m.tobytes()).hexdigest()
    compiler=module(a.compiler,'physical_source_compiler')
    for tab,invp,cost in [(O,'receiver',costO),(G,'source',costG)]:
        for (r,k),M in sorted(tab.items()):
            p=price_map(compiler,M)+18*shuffle(16*k);cost[r,k]=p
            out[f'{invp}/{r}/{k}']={'binary_ADD_each_direction':p,'matrix_sha256':hashm(M)}
    if a.matrices:np.savez_compressed(a.matrices,**{f'{q}{i}-{k}':m for q,tab in [('O',O),('G',G)]for(i,k),m in tab.items()})
    baseline=base['combined'];assert base['native_chart_count']==31
    si=sum(costG.values());te=sum(costO.values())
    info={'packed_H_centres':31,'H_receiver_panels':1041,'retained_H_donor_receiver_fibres':3123,'existing_H_native_identity_directions':749520,
          'additional_entire_native_cells':51,'new_entire_identity_cells':49,'new_entire_target_row80_shear':[80,2,2],'new_entire_target_col10_shear':[0,10,1],
          'additional_full_original_directions':51*3840,'all_verified_target_directions':749520+51*3840,'new_distinct_contacts':51,
          'all_distinct_contacts':2844+51,'retained_foreign_rank_count':6470,'native_binary_matrix_receipts':out,
          'extra_source_gauge_ADD_each_direction':si,'native_source_forward_ADD':baseline['source_forward_ADD']+si,'native_source_inverse_ADD':baseline['source_pure_inverse_ADD']+si,
          'native_source_INIT_and_dirty_CLEAR_each':baseline['source_INIT'],'terminal_gauge_ADD_each_direction':te,'all_added_MOVEs_INIT_CLEAR':0,
          'full_contact_coefficient_stream_sha256':joint.hexdigest(),'source_input_gauge_count':len(G)//2,'receiver_output_gauge_count':len(O)//2}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(info,sort_keys=True,indent=2)+'\n');print({k:v for k,v in info.items()if k!='native_binary_matrix_receipts'},flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','h-author','middle-author','k-words','d-charts','library','inv-lib','packed-endpoint','compiler','assignment','baseline-source','out'):p.add_argument('--'+n,type=Path,required=True)
    for n in ('cache','packing-review','field-review','parameters','matrices'):p.add_argument('--'+n,type=Path)
    a=p.parse_args();sys.path.insert(0,str(a.h_author));sys.path.insert(0,str(a.middle_author))
    sys.path.insert(0,str(a.repo/"research/moonshot-005-program/results/bit-spread-isolated-middle-cut/author"))
    from transfer import Atlas,rank_fast
    from fast import Arithmetic
    from slices import extend_rows
    from verify import price_map,shuffle
    inv=Arithmetic(a.inv_lib.resolve()).inverse
    verify(a)
