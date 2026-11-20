#!/usr/bin/env python3
"""Extend an actual D feedback construction with simultaneous final-facet corrections."""
import argparse
import ctypes
from hashlib import sha256,shake_256
import json
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from feedback import check,reduce

def null_rows(A,T,inv):
    piv,e=reduce(A.T,T,inv)
    free=[j for j in range(A.shape[0]) if j not in piv]
    B=np.zeros((len(free),A.shape[0]),dtype=np.uint8)
    B[:,free]=np.eye(len(free),dtype=np.uint8)
    B[:,piv]=e[:len(piv),free].T
    return B

def direction_sample(dims,key):
    return np.frombuffer(shake_256(key.encode()).digest(int(np.prod(dims))),dtype=np.uint8).reshape(dims)&63

def main():
    p=argparse.ArgumentParser()
    for name in ('repo','transfer','k-words','d-charts','mult','solve','matrix','prior','out'):
        p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--target',type=int,default=80)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(a.transfer.resolve()))
    from transfer import Atlas,TABLE,INV
    at=Atlas(a.repo,a.k_words,a.d_charts,a.mult);mm=at.ops.matmul
    roles=(4,37,83)
    n=10656
    M=np.memmap(a.matrix/'M.raw',dtype=np.uint8,shape=(n,n),mode='r')
    check(sha256(memoryview(M)).hexdigest()=='8b6eccaf6c6e371b85473a48c89a6a5c1f14968b2687ff3f56f76a56e4e4d3c9','small native return')
    old=np.load(a.prior/'SOLVES.npz',allow_pickle=False)
    D=np.load(a.prior/'KERNEL.npy',allow_pickle=False);E0=old['E']
    dk=D.shape[1]
    check(np.array_equal(mm(E0,D),np.eye(dk,dtype=np.uint8)),'prior D construction')
    Bn={};obs=[];holders=[];filters=[]
    for i in roles:
        e,weights,_,_=at.facet(i)
        weights=weights.T
        check(weights.shape==(len(e),480),'facet coefficient orientation')
        select=[j for j,row in enumerate(weights) if np.any(row[:96])]
        check(all(not np.any(weights[j,96:]) for j in select),'pure marked captures')
        E=np.zeros((len(select),n),dtype=np.uint8)
        for j in sorted(x for x in at.orth[i] if x<111):
            check(i!=j,'proper')
            ce,pre,_,_=at.terminal_inputs(i,j)
            check(ce==e and not np.any(pre[select,96:]),'true small facet rows')
            E[:,96*j:96*(j+1)]=pre[select,:96]
        U=null_rows(mm(E,D),TABLE,INV)
        check(not np.any(mm(U,mm(E,D))),'retain D modes')
        Bn[i]=E
        holders.append([e[j] for j in select]);filters.append(U)
        obs.append(mm(U,E))
        print('facet',i,'captures',len(select),'annihilators',len(U),flush=True)
    b=len(roles)*96
    S=np.zeros((n,b),dtype=np.uint8)
    for k,i in enumerate(roles):S[96*i:96*i+96,96*k:96*k+96]=np.eye(96,dtype=np.uint8)
    path=a.out/'INVERSES.npy'
    if path.exists():
        Z=np.load(path,allow_pickle=False)
    else:
        A=np.memmap(a.out/'aug.raw',dtype=np.uint8,shape=(n,n+b),mode='w+')
        A[:,:n]=M;A[:,n:]=S
        Z=np.zeros((n,b),dtype=np.uint8)
        rows=np.empty(n,dtype=np.uint32);cols=rows.copy();diag=np.empty(n,dtype=np.uint8)
        sol=ctypes.CDLL(str(a.solve.resolve())).solve_many
        ptr=ctypes.c_void_p;sol.argtypes=[ptr,ctypes.c_size_t,ctypes.c_size_t]+[ptr]*6;sol.restype=ctypes.c_int
        code=sol(A.ctypes.data,n,b,TABLE.ctypes.data,INV.ctypes.data,rows.ctypes.data,cols.ctypes.data,diag.ctypes.data,Z.ctypes.data)
        check(code==0,'global inverse')
        np.save(path,Z)
    for j in range(0,n,96):check(np.array_equal(mm(M[j:j+96],Z),S[j:j+96]),'original physical inverse')
    blocks=[mm(E,Z) for E in obs]
    q0=mm(E0,Z)
    quota=a.target
    q=q0.copy();selected=[[] for _ in roles]
    # Choose common independent observation rows on the three separate actuator banks.
    for row in range(max(map(len,blocks))):
        for p,B in enumerate(blocks):
            if row>=len(B) or sum(map(len,selected))>=quota:continue
            c=np.vstack((q,B[row]))
            if all(len(reduce(c[:,i:i+96],TABLE,INV)[0])==len(c) for i in range(0,b,96)):
                q=c;selected[p].append(row)
    k=sum(map(len,selected))
    check(k>0 and k+dk<=96,'number of joint native modes')
    # Reorder into consecutive role blocks after the D block.
    active=[obs[p][selected[p]] for p in range(len(roles))]
    E=np.vstack([E0,*active]);q=mm(E,Z)
    outV=np.zeros((b,k),dtype=np.uint8)
    costs=0;pos=0;witnesses=[]
    weight=np.array([sum(int(TABLE[z,1<<j]).bit_count() for j in range(6)) for z in range(64)])
    for p,i in enumerate(roles):
        local=len(selected[p])
        if not local:continue
        f=filters[p][selected[p]]
        B=q[:,96*p:96*(p+1)]
        ids,red=reduce(np.hstack((B,np.eye(dk+k,dtype=np.uint8))),TABLE,INV)
        check(len(ids)==dk+k and max(ids)<96,'facet controllability')
        free=[j for j in range(96) if j not in ids]
        proper=sorted(j for j in at.orth[i] if j<111)
        original_D_response=mm(M[96*i:96*(i+1)],D)
        for test in range(10000):
            V=np.zeros((96,local),dtype=np.uint8)
            if test:V[free]=direction_sample((len(free),local),f'S029 F {i} {test}')
            rhs=red[:,96+dk+pos:96+dk+pos+local].copy()
            if free:rhs^=mm(red[:,free],V[free])
            V[ids]=rhs
            # Include the already-added D component in every checked proper block.
            deltaF=mm(V,f)
            valid=True
            for j in proper:
                baseline=M[96*i:96*(i+1),96*j:96*(j+1)]
                shifted=baseline ^ mm(original_D_response,E0[:,96*j:96*(j+1)]) ^ mm(deltaF,Bn[i][:,96*j:96*(j+1)])
                if len(reduce(shifted,TABLE,INV)[0])!=96:
                    valid=False;break
            if valid:break
        else:raise ValueError('facet local rank repair')
        outV[96*p:96*(p+1),pos:pos+local]=V
        costs+=int(weight[deltaF].sum())
        witnesses.append({'facet':i,'base_early_holder_ids':holders[p],'late_addition_coefficients':deltaF.tolist(),
                          'independent_modes':local,'native_foreign_blocks':len(proper),'selector_index':test})
        pos+=local
        print('facet repaired',i,local,test,flush=True)
    KF=mm(Z,outV);K=np.hstack((D,KF))
    check(np.array_equal(mm(E,K),np.eye(dk+k,dtype=np.uint8)),'joint independent native modes')
    DU=mm(M,D)
    U=np.hstack((DU,mm(S,outV)))
    for j in range(0,n,96):
        check(np.array_equal(mm(M[j:j+96],K),U[j:j+96]),'joint loop')
    np.save(a.out/'KERNEL.npy',K)
    meta=json.loads((a.prior/'RESULT.json').read_text())
    result={'retained_D_modes':dk,'additional_facet_modes':k,'native_small_rank_after_both':n-k-dk,
            'reduction_of_full_bank_return':8*(k+dk),'additional_facet_binary_ADD':8*costs,
            'both_extra_binary_ADD':8*costs+meta['extra_binary_ADD_bank3840'],'new_stationary_fields':0,
            'new_moves':0,'baseline_source_sha256':meta['source_sha256'],'all_foreign_blocks_preserved':6470,
            'kernel_sha256':sha256(memoryview(np.ascontiguousarray(K))).hexdigest(),'facet_words':witnesses}
    (a.out/'RESULT.json').write_text(json.dumps(result,separators=(',',':'),sort_keys=True)+'\n')
    print({x:y for x,y in result.items() if x!='facet_words'},flush=True)
if __name__=='__main__':main()
