#!/usr/bin/env python3
"""Direct full-bank basis and S028 row tests for the final weighted facet profile."""
from argparse import ArgumentParser
from hashlib import sha256
import ctypes,json
from pathlib import Path
import numpy as np
from aggregate import mod,req

def materialize(blocks):
    a=np.zeros((3840,3840),dtype=np.uint8);a[:480,:480]=blocks[1]
    for g in range(7):
        s=slice(480*(1+g),480*(2+g));a[s,s]=blocks[0];a[:480,s]=blocks[2+g];a[s,:480]=blocks[9+g]
    return a
def price(ar,M):
    A=np.ascontiguousarray(M.copy());n=len(A);pc=np.empty(n,dtype=np.int32);rr=ctypes.c_int()
    value=ar.r(A.ctypes.data,n,n,n,1,pc.ctypes.data,ar.f.MUL.ctypes.data,ar.f.INVERSE.ctypes.data,ar.weights.ctypes.data,ar.scales.ctypes.data,ctypes.byref(rr))
    req(rr.value==n,'literal paid invertible full-bank factor');return int(value)
def run(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','gf');n=mod(root/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','price')
    ar=mod(a.arithmetic,'field').Arithmetic(a.library,f,helper);pr=mod(a.previous,'initial');mm=ar.mm;raw,body,copy=pr.coords();terms=pr.target_blocks(root)
    flat,first,last,trial=[json.loads(p.read_bytes()) for p in (a.flat_config,a.input_config,a.output_config,a.profile)]
    P=pr.rand('globally shared native output rows 0',(8,480));U=pr.rand(flat['U8_SHAKE_tag'],(480,8))[:,:7];w=np.array(flat['weights'],dtype=np.uint8);t=first['dimensions'];z=last['output_dimensions'];adj=[sorted(n.adj[i]&set(range(111))) for i in range(111)]
    common=np.kron(np.eye(8,dtype=np.uint8),U);images={};qrows=[];a.out.mkdir(parents=True,exist_ok=True)
    for i,js in enumerate(adj):
        B=np.load(a.aggregate/f'W{i:03}.npy',mmap_mode='r');req(sha256(B).hexdigest()==trial['aggregate_sha256'][str(i)],'all native aggregate arrays')
        C=materialize(B);Pi=P[:z[i]];K=np.vstack([mm(Pi,C[480*g:480*(g+1)])for g in range(8)]);K^=f.MUL[w[i],np.kron(np.eye(8,dtype=np.uint8),Pi)]
        expected=np.zeros_like(K);allv=[common]
        for j in js:
            if (i,j) not in terms:continue
            out,src,T=terms[i,j];iy=np.arange(64*out,64*out+64);ix=np.arange(64*src,64*src+64);idsy=480*copy[iy]+body[iy];idsx=480*copy[ix]+body[ix]
            functional=np.zeros((8*len(Pi),64),dtype=np.uint8)
            for g in range(8):
                sel=copy[iy]==g
                if sel.any():functional[g*len(Pi):(g+1)*len(Pi),sel]=Pi[:,body[iy[sel]]]
            expected[:,idsx]^=f.MUL[w[j],mm(functional,T)]
            VV=np.zeros((3840,8*t[j]),dtype=np.uint8)
            for e in range(8):
                sel=copy[ix]==e
                if sel.any():VV[idsy,e*t[j]:(e+1)*t[j]]=mm(T[:,sel],U[body[ix[sel]],:t[j]])
            allv.append(VV)
        req(np.array_equal(K,expected),'all genuine weighted native output functionals on every original input')
        V=np.hstack(allv);V=V[:,ar.reduce(V)];req(V.shape[1]==trial['facets'][str(i)]['v'],'actual tested full-bank output space');images[i]=V
        if K.any():qrows.append(K[ar.reduce(K.T)])
    Q=np.vstack(qrows);Q=Q[ar.reduce(Q.T)];req(len(Q)==trial['q']==71,'complete weighted native row constraints')
    Z=np.vstack([Q,pr.rand(f"common bilateral profile/{trial['plus']}/{trial['seed']}",(trial['extra']+trial['plus'],3840))]);req(sha256(Z).hexdigest()==trial['annihilator_sha256'],'actual common profile')
    piv=list(map(int,ar.reduce(Z)));free=sorted(set(range(3840))-set(piv));req(len(piv)==len(Z)==120,'full profile annihilator rank')
    W=np.zeros((3840,len(free)),dtype=np.uint8);W[free]=np.eye(len(free),dtype=np.uint8);W[piv]=mm(ar.reduce(Z[:,piv],True)[0],Z[:,free]);req(not mm(Z,W).any() and len(ar.reduce(mm(Z,common)))==common.shape[1],'actual synchronized native subspace excludes old input panel')
    record={};verify_all=a.only is None
    for i in (range(111) if verify_all else a.only):
        V=images[i];native=trial['facets'][str(i)];C=materialize(np.load(a.aggregate/f'W{i:03}.npy',mmap_mode='r'))
        # Use the actual free-coordinate identity in the explicit nullspace basis.
        CW=C[:,free]^mm(C[:,piv],W[piv]);N=pr.rand(f"bilateral facet common complement/{i}/{native['complement']}",(3840,native['d']))
        left=np.hstack([V,CW,N]);right=np.hstack([V,f.MUL[w[i],W],N])
        req(left.shape==right.shape==(3840,3840),'both actual facet basis changes')
        Pi=P[:z[i]]
        for e in range(8):req(np.array_equal(mm(Pi,CW[480*e:480*(e+1)]),f.MUL[w[i],mm(Pi,W[480*e:480*(e+1)] )]),'local true output functionals pointwise fixed by calibrated factors')
        lprice=price(ar,left);rprice=price(ar,right)
        record[str(i)]={'raw_X':sha256(left).hexdigest(),'raw_Y':sha256(right).hexdigest(),'X':lprice,'Y':rprice}
        if a.prices:req(record[str(i)]==json.loads(a.prices.read_bytes())[str(i)],'native 3840-dimensional complete primitive budget')
        (a.out/'PARTIAL-PRICES.json').write_text(json.dumps(record,sort_keys=True)+'\n')
        if i%10==0:print('physical facet basis',i,flush=True)
    if verify_all:
        extra=sum(v['X']+v['Y']for v in record.values());result={'native_facets':111,'true_owner_width':3840,'actual_target_perturbations':len(terms),'physical_common_kernel':len(free),'disjoint_prior_target_kernel':4819,'whole_native_return_upper':426240-4819-len(free),'all_native_facet_factors_invertible':222,'forward_binary_ADD':extra,'inverse_binary_ADD':extra,'new_INIT_CLEAR_MOVE':0,'complete_target':False}
        (a.out/'PRICES.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n');(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','arithmetic','library','previous','flat-config','input-config','output-config','profile','aggregate','out'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--prices',type=Path);p.add_argument('--only',type=int,nargs='+');run(p.parse_args())
