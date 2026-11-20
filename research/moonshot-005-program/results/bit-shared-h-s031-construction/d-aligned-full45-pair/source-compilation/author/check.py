#!/usr/bin/env python3
"""Deterministic owner-positioned, in-place binary source compiler and gross bill."""
from argparse import ArgumentParser
from array import array
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import gzip,json,sys
import numpy as np

def need(ok,why):
    if not ok:raise ValueError(why)

def mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        b>>=1;a<<=1
        if a&64:a^=67
    return out

def lift(matrix):
    table=np.array([[mul(a,1<<k)for k in range(6)]for a in range(64)],dtype=np.uint8)
    out=[]
    for row in matrix:
        blocks=table[row]
        bits=((blocks[:,:,None]>>np.arange(6,dtype=np.uint8))&1).transpose(2,0,1).reshape(6,6*len(row))
        for b in bits:out.append(int.from_bytes(np.packbits(b,bitorder='little').tobytes(),'little'))
    return out

def compile_and_replay(binary):
    n=len(binary);rows=binary.copy();ops=array('H');swaps=0
    def add(t,s):
        need(t!=s and 0<=t<n and 0<=s<n,'actual distinct binary owners')
        rows[t]^=rows[s];ops.extend((t,s))
    for j in range(n):
        mask=1<<j
        k=next((i for i in range(j,n)if rows[i]&mask),None)
        need(k is not None,'source binary full rank')
        if k!=j:
            add(j,k);add(k,j);add(j,k);swaps+=1
        for i in range(n):
            if i!=j and rows[i]&mask:add(i,j)
    identity=[1<<j for j in range(n)]
    need(rows==identity,'complete exact elimination')
    state=identity.copy()
    for i in range(len(ops)-2,-1,-2):state[ops[i]]^=state[ops[i+1]]
    need(state==binary,'complete symbolic forward word on every input bit')
    for i in range(0,len(ops),2):state[ops[i]]^=state[ops[i+1]]
    need(state==identity,'complete symbolic inverse word on every input bit')
    if sys.byteorder!='little':ops.byteswap()
    return len(ops)//2,swaps,sha256(ops.tobytes()).hexdigest()

ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
here=Path(__file__).resolve().parent;base=args.repo/'research/moonshot-005-program/results'
for path,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(sha256((args.repo/path).read_bytes()).hexdigest()==h,'pin '+path)
early=json.loads(gzip.decompress((here.parent.parent/'output/EARLY.json.gz').read_bytes()))
donors=[0,45,61,62,100];owners={j:{}for j in donors}
for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
    phase,j,x,h,d,k,source,target=json.loads(line)
    if phase=='X'and j in owners:
        need(source==j and x not in owners[j],'unique actual source owner')
        owners[j][x]=h
receipts=[]
for j in donors:
    saved=early['full'][str(j)];labels=saved['row_owners'];E=np.array(saved['matrix'],dtype=np.uint8)
    need(E.shape==(480,480)and sorted(owners[j])==list(range(480)),'actual full source dimensions')
    need(len(labels)==480 and sorted(x for h,x in labels)==list(range(480)),'one output per actual owner')
    need(all(owners[j][x]==h for h,x in labels),'source output-to-route binding')
    # The row labelled (H,x) must be written on actual owner x. Columns already
    # use the original coordinates 0..479. This permutation is built into A.
    A=np.empty_like(E)
    for i,(h,x)in enumerate(labels):A[x]=E[i]
    binary=lift(A);count,swaps,digest=compile_and_replay(binary)
    receipt={'donor':j,'field_owners_per_lane':480,'binary_owners_per_lane':2880,'field_matrix_row_major_sha256':sha256(A.tobytes()).hexdigest(),'ADDs_per_direction':count,'three_ADD_swaps':swaps,'binary_elimination_word_u16le_sha256':digest,'eight_lane_forward_inverse_ADDs':16*count,'auxiliary_fields':0,'extra_exports':0}
    receipts.append(receipt);print('COMPILED_ACTUAL_SOURCE',j,count,swaps,digest,flush=True)
source_total=sum(r['eight_lane_forward_inverse_ADDs']for r in receipts)
h_pair=json.loads((here.parent.parent/'root-physical/output/RESULT.json').read_text())
need(h_pair['pair_ADD_total']==1509520 and h_pair['paid_field_exports']==16,'accepted full H-pair bill')
result={'status':'PASS_ACTUAL_FIVE_SOURCE_BINARY_COMPILERS','sources':receipts,'source_forward_inverse_ADD_total':source_total,'H_pair_forward_inverse_ADD_total':1509520,'known_source_and_two_H_ADD_total':source_total+1509520,'H_paid_field_exports':16,'binary_INIT_MOVE_CLEAR_each':96,'paid_MOVE_gap':6,'word_encoding':'deterministic elimination; each ADD is two unsigned16 little-endian indices (target,source); reverse order implements forward matrix','owner_reordering_included_in_matrix':True,'all_forward_inverse_words_symbolically_replayed':True,'free_permutations':False,'gross_replacement_bill_not_incremental_saving':True,'unbuilt_H_D_K_F_and_global_return_costs_not_included':True,'complete_global_invoice':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],source_total,source_total+1509520,flush=True)
