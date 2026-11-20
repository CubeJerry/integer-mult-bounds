#!/usr/bin/env python3
"""Regenerate and price the common 31-H/111-full-contact physical word."""
import argparse,hashlib,json,sys
from pathlib import Path
from collections import Counter
from functools import lru_cache
import numpy as np
from physical import Physical

def swaps(P):
    assert sorted(P)==list(range(3840));seen=set();count=0
    for i in range(3840):
        if i in seen:continue
        j=i;count+=1
        while j not in seen:seen.add(j);j=P[j]
        assert j==i
    return 3840-count

def verify(x):
    r=x.repo/'research/moonshot-005-program/results';at=Atlas(x.repo,x.k_words,x.d_charts,x.library);at.left=lru_cache(111)(at.left);at.right=lru_cache(111)(at.right)
    E=Arithmetic(x.arith.resolve());proof=json.loads(x.receipts.read_text());previous=json.loads(x.price.read_text());assign={int(j):v for j,v in json.loads(x.assignment.read_text()).items()}
    labelled={i:j for j,ii in assign.items()for i in ii};assert set(labelled)==set(range(111))-{80}and sum(map(len,assign.values()))==110
    labelled[80]=2;target=json.loads((r/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json').read_text());col={i:t for i,j,t in target['column_transfers']};assert [80,2,2]in target['row_transfers']and assign[10]==[0,5,8,12]
    charts=obtain(x,at,E.inverse);catalog={j for h in charts[0]for j in at.H[h]};assert len(catalog)==78 and set(assign)==set(range(111))-catalog
    co=module(x.compiler,'genuine_local_compiler');fm=Physical(x,at,E.inverse,TABLE,INV,extend_rows,row_reduce,charts,price_map,shuffle,co,assign,col)
    x.out.mkdir(parents=True,exist_ok=True);raw=x.out/'matrices'
    if x.emit:raw.mkdir(exist_ok=True)
    sourced={};census=0;cc=Counter();bills={}
    for j in assign:
        fee=0
        for k in (3,12):
            G=fm.source(j,k);fee+=price_map(co,G)+18*shuffle(16*k)
            if x.emit:np.save(raw/f'G{j}-{k}.npy',G)
        sourced[str(j)]=fee
    assert sourced==previous['source_G_per_donor_one_direction']
    weights=np.array([sum(int(TABLE[c,1<<t]).bit_count()for t in range(6))for c in range(64)],dtype=np.int64)
    for i in range(111):
        pure=cross=snaps=0;perm=[-1]*3840
        for k in (3,12):
            F,n=fm.face(i,labelled[i],k,proof[f'F{i}-{k}']);census+=n;e,y,idx,_=fm.holder(i,k);Y=idx[len(e):];w=16*k
            pure+=price_map(co,F[:,len(e):]);cross+=8*int(weights[F[:,:len(e)]].sum());snaps+=48*len(e)
            off=0 if k==3 else 768
            for z,t in enumerate(Y):
                h,s=divmod(z,w);t=t-53280-480*i
                for g in range(8):perm[t*8+g]=off+16*s+8*h+g
            if x.emit:np.save(raw/f'F{i}-{k}.npy',F)
        swap=18*swaps(perm);budget={'pure_Y_ADD':pure,'early_to_late_ADD':cross,'stationary_snapshot_ADD_INIT_dirty_CLEAR':snaps,'terminal_owner_permutation_ADD':swap,'Ground_inverse_ADD':pure+swap,'terminal_and_ground_total_ADD':2*(pure+swap)+cross+snaps}
        assert budget==previous['facet_price'][str(i)];cc.update(budget);bills[str(i)]=budget
        if i%10==0:print('verified native facet',i,flush=True)
    assert census==12940 and dict(cc)==previous['whole_terminal_fee']
    (x.out/'RESULT.json').write_text(json.dumps({'sector_foreign_rank_checks':census,'protected_full_contacts':111,'retained_H_native_fibres':3123,'true_native_target_directions':1175760,'distinct_target_pairs':2955,'source_forward_ADD':previous['source_forward_ADD'],'source_inverse_ADD':previous['source_inverse_ADD'],'terminal_sum':dict(cc)},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('repo','library','arith','out'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--emit',action='store_true');p.add_argument('--cache',type=Path)
    x=p.parse_args();r=x.repo/'research/moonshot-005-program/results';here=Path(__file__).parent
    x.h_author=r/'bit-spread-rs-physical-word/author';x.middle_author=r/'bit-native-complete-middle-charts/author';x.k_words=r/'bit-gf64-actual-k-atlas/author/output';x.d_charts=r/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz'
    x.packed_endpoint=r/'bit-spread-packed-h-facet-fibres/author';x.packing_review=r/'bit-spread-overlap-source/review/check.py';x.field_review=r/'bit-spread-h263-source/review/check.py';x.parameters=r/'bit-spread-two-centre-packing/author/output/PARAMETERS.json'
    x.compiler=r/'bit-spread-source-owner-compiler/author/compile_source.py';x.assignment=here/'output/ASSIGNMENT.json';x.receipts=here/'output/FACES.json';x.price=here/'output/PRICE.json'
    sys.path.insert(0,str(x.h_author));sys.path.insert(0,str(x.middle_author));sys.path.insert(0,str(r/'bit-spread-isolated-middle-cut/author'))
    from transfer import Atlas,TABLE,INV
    from fast import Arithmetic
    from slices import row_reduce,extend_rows
    from verify import price_map,shuffle
    from panels import obtain,module
    verify(x)
