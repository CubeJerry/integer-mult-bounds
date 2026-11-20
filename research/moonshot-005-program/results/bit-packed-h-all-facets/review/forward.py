#!/usr/bin/env python3
"""Independent true-source, all-foreign preterminal and F replay."""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import argparse,json,hashlib,importlib.util
import numpy as np
def run(a):
    spec=importlib.util.spec_from_file_location('sourcefirst',a.canonical/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    alg=m.load_replay(a.replay);eng=m.Engine(a.stream_lib);alg.mm=eng.mm;n=alg.Native(a)
    js=json.loads(a.assign.read_text());ass={i:int(j)for j,rr in js.items()for i in rr};ass[80]=2;assert len(ass)==111
    w=96 if a.sector=='small' else 384;k=w//32;lo=0 if k==3 else 96;cas=m.Cascade(n,alg,eng,k==3)
    old=json.loads((a.repo/'research/moonshot-005-program/results/bit-two-sided-covariant-target/author/output/ASSIGNMENT.json').read_text());column={i:l for i,j,l in old['column_transfers']}
    def target(i,j):
        M=np.eye(w,dtype=np.uint8)
        if k==3 and (i==80 or j==10):
            s,t=(2,0) if i==80 else(0,column[i]);assert max(s,t)<12
            for h in range(2):
                for q in range(4):M[48*h+4*t+q,48*h+4*s+q]^=1
        return M
    owners=defaultdict(lambda:defaultdict(list))
    for h,z in n.kwords['spread'].items():
        for phase,src,dst in z['stripes']:
            if len(src)!=3*k:continue
            for u in dst:
                r=n.rt[u];i=r[1]if phase=='Y' else r[7]
                if i is not None:owners[i][phase].append(u)
    words={i:np.load(a.matrices/f'F{i}-{k}.npy')for i in range(111)}
    def rank(mat):
        b=np.ascontiguousarray(mat);ctx=eng.lib.begin(w)
        try:assert eng.lib.consume(ctx,b.ctypes.data,w);return int(eng.lib.present_rank(ctx))
        finally:eng.lib.finish(ctx)
    hits=0;checks=0;dig=hashlib.sha256();zero=np.zeros(w,np.uint8)
    for j in range(111):
        dv=n.through_d(j,range(111),k==3);sig={};foreign=np.flatnonzero(n.orth[:,j])
        for h in cas.by_donor[j]:
            stripes,cross=cas.word[h]
            for src,dst in stripes:
                ab=np.stack([dv[t][lo:lo+w]if t in dv else zero for t in src])
                if ab.any():sig.update(zip(dst,eng.mm(cas.vandermonde,ab)))
            for x,y in cross:
                if x in sig:sig[y]=sig.get(y,zero)^sig[x]
        for i in map(int,foreign):
            ids=sorted(owners[i]['X'])+sorted(owners[i]['Y']);res=eng.mm(words[i],np.stack([sig.get(t,zero)for t in ids]));assert rank(res)==w,(i,j)
            dig.update(bytes([i,j]));dig.update(hashlib.sha256(res.tobytes()).digest());hits+=1
            if ass[i]==j:
                G=np.load(a.sources/f'G{j}-{k}.npy');assert np.array_equal(eng.mm(res,G),target(i,j));checks+=1
        if j%20==0:print(a.sector,j,flush=True)
    assert hits==6470 and checks==111
    a.out.mkdir(exist_ok=True,parents=True);(a.out/(a.sector.upper()+'.json')).write_text(json.dumps({'sector':a.sector,'all_native_contact_ranks':hits,'full_original_source_designations':checks,'actual_designated_coefficients':checks*w*w,'direct_source_first_matrix_stamp':dig.hexdigest()},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','canonical','replay','h-words','d-words','k-words','stream-lib','assign','matrices','sources','out'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--sector',choices=('small','large'),required=True);run(p.parse_args())
