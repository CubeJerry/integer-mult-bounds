#!/usr/bin/env python3
"""Replay feedback on independent original inputs without a global return matrix."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('repo','replay','engine','h-words','d-words','k-words','stream-lib','feedback','out'):
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    spec=importlib.util.spec_from_file_location('native_stream',a.engine/'check.py')
    pkg=importlib.util.module_from_spec(spec);spec.loader.exec_module(pkg)
    alg=pkg.load_replay(a.replay);engine=pkg.Engine(a.stream_lib);alg.mm=engine.mm
    nat=alg.Native(a);cascade=pkg.Cascade(nat,alg,engine,True)
    meta=json.loads((a.feedback/'RESULT.json').read_text())
    K=np.load(a.feedback/'KERNEL.npy')
    k=len(meta['chosen_caches'])
    alg.need(K.shape==(111*96,k) and len(alg.echelon(K)[0])==k,'independent original input directions')
    alg.need(hashlib.sha256(K.tobytes()).hexdigest()==meta['kernel_sha256'],'kernel payload')
    records={r['D']:r for r in meta['chosen_caches']}
    alg.need(len(records)==k and all(d in nat.mark for d in records),'distinct marked D caches')
    zero=np.zeros(k,dtype=np.uint8)
    def fetch(store,owners):return np.stack([store.get(t,zero) for t in owners])
    hv={}
    for h,plane in enumerate(nat.H):
        donors=[i for i in plane if i<111]
        if not donors:continue
        outs=nat.byh[h]; ports=sorted({d for phase,d in outs if d in nat.mark})
        ph=nat.p[h];early={};v=np.asarray(nat.hword[9]['V'],dtype=np.uint8)
        for phase,tag in [('X','early'),('Y','late')]:
            for stripe in range(ph[tag]):
                s=np.zeros((9,k),dtype=np.uint8)
                for j in donors:
                    u=nat.source_in(j,h,phase,9,stripe)[:,:96]
                    s^=engine.mm(u,K[96*j:96*(j+1)])
                jet=engine.mm(v,s)
                if phase=='X':early[stripe]=s
                if phase=='Y' and len(donors)<3:
                    typ='two' if len(donors)==2 else 'singleton'
                    dv=np.asarray(nat.hword[9][typ]['cross_coefficients'],dtype=np.uint8)
                    jet^=engine.mm(dv,early[stripe])
                for z,d in enumerate(ports):hv[outs[phase,d][stripe]]=jet[z]
    base={};changes={};stations={};verified=0;minor=hashlib.sha256();adds=0
    for d in sorted(nat.mark):
        _,m,n,weights=nat.dword[d];x,y=nat.byd[d]['X'],nat.byd[d]['Y']
        e,l=fetch(hv,x),fetch(hv,y);r=len(weights)
        V=alg.cauchy(range(m,m+r),range(m));S=engine.mm(V,e)
        A=alg.cauchy(range(m),range(m));C=alg.cauchy(range(n),range(n))
        U=alg.MUL[alg.cauchy(range(n),range(n,n+r)),np.asarray(weights,dtype=np.uint8)[None,:]]
        Ex,Lx=engine.mm(A,e),engine.mm(C,l)^engine.mm(U,S)
        base.update(zip(x,Ex));base.update(zip(y,Lx))
        if d not in records:continue
        q=records[d];t=q['early_cache_index'];v=np.asarray(q['late_coefficients'],dtype=np.uint8)
        alg.need(0<=t<r and len(v)==n,'declared capture and actual late owner count')
        stations[d]=S[t].copy()
        delta=alg.MUL[v[:,None],S[t][None,:]]
        changes[d]=dict(zip(y,delta))
        total=0
        for coeff in v:
            total+=sum(int(alg.MUL[coeff,1<<bit]).bit_count() for bit in range(6))
        alg.need(total==q['extra_binary_ADD_per_copy'],'literal delivery ADD bill')
        adds+=total
        native_D=sorted(t for t in nat.D[d] if t<111)
        native_Dstar=sorted(t for t in nat.D[nat.dual[d]] if t<111)
        owners=x+y
        operator=np.block([[A,np.zeros((m,n),dtype=np.uint8)],[engine.mm(U,V)^alg.MUL[v[:,None],V[t][None,:]],C]])
        count=0
        for i in native_Dstar:
            rr=[k for k,w in enumerate(owners) if nat.rt[w][5] is not None and i in nat.H[nat.rt[w][5]]]
            for j in native_D:
                cc=[k for k,w in enumerate(owners) if nat.rt[w][3] is not None and j in nat.H[nat.rt[w][3]]]
                alg.need(len(rr)==len(cc)==8,'actual tight restriction')
                piv,det=alg.echelon(operator[np.ix_(rr,cc)])
                alg.need(len(piv)==8 and det!=0,'patched physical foreign rank')
                count+=1;minor.update(bytes([det]))
        alg.need(count==q['local_foreign_minors'],'changed-D counts')
        verified+=count
    def destination(chosen):
        dstate=dict(base)
        for d in chosen:
            for t,delta in changes[d].items():
                dstate[t]=dstate[t]^delta
        physical={}
        for h,(stripes,cross) in cascade.word.items():
            for src,dst in stripes:
                yy=engine.mm(cascade.vandermonde,fetch(dstate,src));physical.update(zip(dst,yy))
            for e,l in cross:physical[l]^=physical[e]
        actual=np.empty_like(K)
        for (i,c),(ids,v) in cascade.facets.items():
            actual[i*96+c*16:i*96+(c+1)*16]=engine.mm(v,fetch(physical,ids))
        return actual
    chosen=list(records)
    fix=K^destination(chosen)
    baseline=K^destination([])
    failed=K^destination(chosen[1:])
    st=np.stack([stations[d] for d in chosen])
    alg.need(np.array_equal(st,np.eye(k,dtype=np.uint8)),'true cached fields see all independent modes')
    selected=alg.echelon(baseline)[0]; control=alg.echelon(failed)[0]
    alg.need(not fix.any() and len(selected)==k and control==[0],'actual physical kernel and omitted-gate control')
    a.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_DIRECT_FIELD_TRAJECTORY_OF_NATIVE_D_FEEDBACK','verified_original_inputs':k,
            'modified_charts':chosen,'reconstructed_modified_foreign_minors':verified,
            'local_determinants_sha256':minor.hexdigest(),'actual_cache_matrix_sha256':hashlib.sha256(st.tobytes()).hexdigest(),
            'unmodified_endpoint_residual_rank':len(selected),'modified_endpoint_residual_rank':0,
            'omitting_first_delivery_residual_rank':len(control),'modified_residual_SHA256':hashlib.sha256(fix.tobytes()).hexdigest(),
            'extra_ADDs_at_3840':8*adds,'fixed_sector_rank':111*96-k,'fixed_bank_return_rank_decrease':8*k}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result,flush=True)
if __name__=='__main__':main()
