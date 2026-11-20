#!/usr/bin/env python3
"""Compute full conservative return minors before and after arbitrary invertible native facet maps."""
from argparse import ArgumentParser
from hashlib import sha256
import json,sys
from pathlib import Path
import numpy as np
from late import mod,req

def main(a):
    t=a.repo/'research/moonshot-005-program/results';f=mod(t/'bit-spread-h263-source/review/check.py','gf')
    sys.path.insert(0,str(a.rank_code.resolve().parent));rk=mod(a.rank_code,'solver').runner(a.library,f)
    A=np.load(a.matrix,mmap_mode='r',allow_pickle=False);expected=json.loads(a.receipt.read_bytes());pin=sha256(A).hexdigest()
    req(A.shape==(53280,53280) and pin==expected['rim_global_original_sha256'],'native authenticated complete copy block')
    a.out.mkdir(parents=True,exist_ok=True)
    if a.full:
        r=rk(np.array(A,copy=True,order='C'),a.panel,a.threads)
        out={'full_global_rim_sha256':pin,'native_complete_rim_rank':int(r),'whole_eight_copy_native_return_lower':7*int(r),'copy_rows':53280,'copy_columns':53280,'genuine_diagonal_included':True}
        dest='RIM-RANK.json'
    else:
        recipients=list(range(55));donors=list(range(55,111));B=np.ascontiguousarray(A[:55*480,55*480:]);small=sha256(B).hexdigest();r=rk(B,a.panel,a.threads)
        out={'full_global_rim_sha256':pin,'disjoint_role_submatrix_sha256':small,'disjoint_receivers':recipients,'disjoint_donors':donors,'exact_disjoint_one_copy_rank':int(r),'whole_return_lower_after_any_facet_bijection':7*int(r),'native_rim_rows':480*len(recipients),'native_rim_columns':480*len(donors),'genuine_diagonal_included':False}
        dest='DISJOINT-RIM.json'
    (a.out/dest).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(dest,r,7*r,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','rank-code','library','matrix','receipt','out'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--threads',type=int,default=4);p.add_argument('--panel',type=int,default=64);p.add_argument('--full',action='store_true');main(p.parse_args())
