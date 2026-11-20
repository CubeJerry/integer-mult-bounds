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
    for name in ('repo','replay','engine','h-words','d-words','k-words','stream-lib','feedback','joint','out'):
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    spec=importlib.util.spec_from_file_location('native_stream',a.engine/'check.py')
    pkg=importlib.util.module_from_spec(spec);spec.loader.exec_module(pkg)
    alg=pkg.load_replay(a.replay);engine=pkg.Engine(a.stream_lib);alg.mm=engine.mm
    nat=alg.Native(a);cascade=pkg.Cascade(nat,alg,engine,True)
    meta=json.loads((a.feedback/'RESULT.json').read_text())
    joint=json.loads((a.joint/'RESULT.json').read_text())
    K=np.load(a.joint/'KERNEL.npy');k=K.shape[1];dk=len(meta['chosen_caches'])
    alg.need(k==92 and dk==12,'joint rank conventions')
    alg.need(K.shape==(111*96,k) and len(alg.echelon(K)[0])==k,'independent original input directions')
    alg.need(hashlib.sha256(K.tobytes()).hexdigest()==joint['kernel_sha256'],'kernel payload')
    records={r['D']:r for r in meta['chosen_caches']}
    alg.need(len(records)==dk and all(d in nat.mark for d in records),'distinct marked D caches')
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
    def destination(chosen,changed_facets=()):
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
        for patch in changed_facets:
            i=patch['facet'];holders=patch['base_early_holder_ids'];z=np.array(patch['late_addition_coefficients'],np.uint8)
            true_early={q for (j,c),(ids,_) in cascade.facets.items() if j==i for q in ids if nat.rt[q][0]=='X'}
            alg.need(set(holders)==true_early and len(holders)==len(true_early),'actual marked early facet owners')
            actual[96*i:96*(i+1)]^=engine.mm(z,fetch(physical,holders))
        return actual
    chosen=list(records)
    facet=joint['facet_words'];base0=K^destination([]);justD=K^destination(chosen);full=K^destination(chosen,facet)
    cache=np.stack([stations[d] for d in chosen]);alg.need(np.array_equal(cache[:,:dk],np.eye(dk,dtype=np.uint8)) and not cache[:,dk:].any(),'12 original independent D caches')
    alg.need(len(alg.echelon(base0)[0])==k and len(alg.echelon(justD)[0])==k-dk and not full.any(),'direct original chronological rank and kernel')
    fadds=0;summed=0;added=[]
    for patch in facet:
        m=np.asarray(patch['late_addition_coefficients'],np.uint8);rk=len(alg.echelon(m)[0]);alg.need(rk==patch['independent_modes'],'literal facet perturbation rank');added.append(rk);summed+=rk
        fadds+=sum(int(alg.MUL[int(x),1<<bit]).bit_count()for x in m.ravel()for bit in range(6))
    alg.need(summed==80 and 8*fadds==joint['additional_facet_binary_ADD'] and 8*(adds+fadds)==joint['both_extra_binary_ADD'],'all actuator invoices')
    # Removing one whole facet leaves precisely its independent output dimensions.
    controls=[]
    for m0 in range(len(facet)):
        residual=K^destination(chosen,facet[:m0]+facet[m0+1:]);controls.append(len(alg.echelon(residual)[0]))
    alg.need(controls==added,'three independent whole-facet omission controls')
    a.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_JOINT_NATIVE_D_AND_F_TRAJECTORY','original_independent_field_vectors':k,
      'basis_D_restriction_rank':dk,'unchanged_rank_on_certified_modes':k,'remaining_rank_after_D_only':k-dk,'joint_residual_nonzero_entries':int(np.count_nonzero(full)),
      'one_sector_global_rank':111*96-k,'all_copy_return_fields_saved':8*k,'actual_D_minors_checked':verified,'rank_one_delivery_ADDs':8*adds,'facet_ADDs':8*fadds,
      'total_extra_ADDs':8*(adds+fadds),'removed_single_facet_residual_ranks':controls,'early_capture_rhs_sha256':hashlib.sha256(cache.tobytes()).hexdigest(),
      'physical_kernel_sha256':joint['kernel_sha256'],'tested_coefficient_equalities':int(full.size)}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result,flush=True)
if __name__=='__main__':main()
