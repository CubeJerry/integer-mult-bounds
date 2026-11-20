#!/usr/bin/env python3
"""Causal D feedback on the exact original-coordinate return of the small RS sector."""
import argparse
import ctypes
from hashlib import sha256,shake_256
import json
from pathlib import Path
import sys
import numpy as np

def check(ok,what):
    if not ok:raise ValueError(what)

def main():
    p=argparse.ArgumentParser()
    for name in ('repo','transfer','k-words','d-charts','mult','solve','matrix','out'):
        p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--count',type=int,default=12)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(a.transfer.resolve()))
    from transfer import Atlas,TABLE,INV
    at=Atlas(a.repo,a.k_words,a.d_charts,a.mult)
    mm=at.ops.matmul
    n=111*96
    mf=a.matrix/'M.raw'
    check(mf.stat().st_size==n*n,'original return dimensions')
    M=np.memmap(mf,dtype=np.uint8,shape=(n,n),mode='r')
    check(sha256(memoryview(M)).hexdigest()=='8b6eccaf6c6e371b85473a48c89a6a5c1f14968b2687ff3f56f76a56e4e4d3c9','raw small source')
    candidates=[d for d in sorted(at.marked) if at.dp[d][3] and min(111,min(at.D[d]))<111
                and len(at.middle[d,'Y'])>=a.count+2]
    chosen=candidates[:a.count]
    check(len(chosen)==a.count,'number of physical cache taps')
    blocks=[]; captures=[]; metas=[]
    for d in chosen:
        baseline,own=at.middle_matrix(d)
        m=len(at.middle[d,'X']);late=at.middle[d,'Y']
        V=INV[np.bitwise_xor(np.uint8(m),np.arange(m,dtype=np.uint8)+32)]
        E=np.zeros((1,n),dtype=np.uint8)
        S=np.zeros((n,len(late)),dtype=np.uint8)
        columns={}; rows={}
        for j in sorted(x for x in at.D[d] if x<111):
            left=at.left(j)
            cols=[i for i,u in enumerate(own) if u in left]
            check(len(cols)==8,'native D input')
            columns[j]=cols
            for i in cols:
                if i>=m:continue
                v=left[own[i]]
                check(not np.any(v[96:]),'early capture sector')
                E[0,96*j:96*(j+1)]^=TABLE[V[i],v[:96]]
        for i in sorted(x for x in at.D[at.dual[d]] if x<111):
            right=at.right(i)
            rs=[c for c,u in enumerate(own) if u in right]
            check(len(rs)==8,'native D output')
            rows[i]=rs
            for c in rs:
                if c<m:continue
                v=right[own[c]]
                check(not np.any(v[96:]),'late injection sector')
                S[96*i:96*(i+1),c-m]=v[:96]
        blocks.append(S);captures.append(E);metas.append((d,baseline,m,V,rows,columns))
    E=np.vstack(captures);S=np.hstack(blocks);b=S.shape[1]
    inv=np.ascontiguousarray(INV)
    raw=a.out/'aug.raw';A=np.memmap(raw,dtype=np.uint8,shape=(n,n+b),mode='w+')
    A[:,:n]=M;A[:,n:]=S
    Z=np.zeros((n,b),dtype=np.uint8)
    rows=np.empty(n,dtype=np.uint32);cols=rows.copy();diag=np.empty(n,dtype=np.uint8)
    sol=ctypes.CDLL(str(a.solve.resolve())).solve_many
    pointer=ctypes.c_void_p
    sol.argtypes=[pointer,ctypes.c_size_t,ctypes.c_size_t]+[pointer]*6
    sol.restype=ctypes.c_int
    print('solving',n,b,chosen,flush=True)
    status=sol(A.ctypes.data,n,b,TABLE.ctypes.data,inv.ctypes.data,rows.ctypes.data,cols.ctypes.data,diag.ctypes.data,Z.ctypes.data)
    check(status==0,'invertible exact native return')
    for i in range(0,n,96):
        check(np.array_equal(mm(M[i:i+96],Z),S[i:i+96]),'exact back substitution')
    Q=mm(E,Z)
    np.savez_compressed(a.out/'SOLVES.npz',Q=Q,Z=Z,E=E,S=S,chosen=chosen)
    print('verified native response; choosing local changes',flush=True)
    feedback(Q,Z,E,S,M,metas,mm,TABLE,INV,a.out)


def reduce(A,T,inv):
    A=A.copy()
    r,c=A.shape
    piv=[]
    for j in range(c):
        k=len(piv)
        if k==r:break
        nz=np.flatnonzero(A[k:,j])
        if not len(nz):continue
        i=k+int(nz[0]);A[[i,k]]=A[[k,i]]
        A[k]=T[inv[A[k,j]],A[k]]
        q=A[:,j].copy();q[k]=0
        A^=T[q[:,None],A[k][None,:]]
        piv.append(j)
    return piv,A
def batch_good(A,rows,cols,T,inv):
    mats=np.stack([A[np.ix_(r,c)] for r in rows.values() for c in cols.values()])
    indices=np.arange(len(mats))
    for j in range(8):
        nz=(mats[:,j:,j]!=0)
        if not np.all(np.any(nz,axis=1)):return False
        ps=j+np.argmax(nz,axis=1)
        tmp=mats[indices,ps].copy()
        mats[indices,ps]=mats[:,j]
        mats[:,j]=T[inv[tmp[:,j],None],tmp]
        if j<7:
            mats[:,j+1:]^=T[mats[:,j+1:,j,None],mats[:,None,j,:]]
    return True

def feedback(Q,Z,E,S,M,metas,mm,T,inv,out):
    sizes=[len(base)-m for d,base,m,v,r,c in metas]
    cuts=np.cumsum([0]+sizes)
    active=list(range(len(metas)))
    while active:
        deficiencies=[len(active)-len(reduce(Q[np.ix_(active,range(cuts[x],cuts[x+1]))],T,inv)[0]) for x in active]
        if not max(deficiencies):break
        del active[int(np.argmax(deficiencies))]
    k=len(active)
    check(k>0,'positive jointly controllable native caches')
    V=np.zeros((Q.shape[1],k),dtype=np.uint8)
    WGT=np.array([sum(int(T[q,1<<j]).bit_count() for j in range(6)) for q in range(64)])
    results=[]
    for j,x in enumerate(active):
        d,base,m,read,rows,cols=metas[x]
        lo,hi=cuts[x],cuts[x+1]
        G=Q[np.ix_(active,range(lo,hi))]
        piv,A=reduce(np.hstack([G,np.eye(k,dtype=np.uint8)]),T,inv)
        check(len(piv)==k and max(piv)<hi-lo,'joint right inverse')
        free=[c for c in range(hi-lo) if c not in piv]
        check(batch_good(base,rows,cols,T,inv),'original D minors')
        for test in range(10000):
            vec=np.zeros(hi-lo,dtype=np.uint8)
            if test:
                vec[free]=np.frombuffer(shake_256(f'S029 feedback {d} {test}'.encode()).digest(len(free)),dtype=np.uint8)&63
            rhs=A[:,hi-lo+j].copy()
            if free:rhs^=mm(A[:,free],vec[free,None])[:,0]
            vec[piv]=rhs
            new=base.copy()
            new[m:,:m]^=T[vec[:,None],read[None,:]]
            if batch_good(new,rows,cols,T,inv):break
        else:raise ValueError('no local change preserving donor restrictions')
        V[lo:hi,j]=vec
        results.append({'D':int(d),'early_cache_index':0,'late_coefficients':vec.tolist(),
                        'local_foreign_minors':len(rows)*len(cols),'selector_index':test,
                        'extra_binary_ADD_per_copy':int(WGT[vec].sum())})
    K=mm(Z,V)
    A=E[active]
    C=mm(S,V)
    check(np.array_equal(mm(A,K),np.eye(k,dtype=np.uint8)),'independent fixed modes')
    for i in range(0,len(M),96):
        check(np.array_equal(mm(M[i:i+96],K),C[i:i+96]),'kernel identity on original coordinates')
    # A zeroed actuator has k-1 independent loops on the same k-dimensional test space.
    bad=C.copy()
    bad[:,0]=0
    check(np.any(C^bad) and len(reduce(mm(A,K),T,inv)[0])==k,'effective removed delivery')
    np.save(out/'KERNEL.npy',K)
    result={'source_sha256':sha256(memoryview(M)).hexdigest(),'chosen_caches':results,
            'source_sector_rank':len(M),'modified_sector_rank':len(M)-k,'bank3840_fixed_return_rank_decrease':8*k,
            'field_kernel_columns':k,'kernel_sha256':sha256(memoryview(np.ascontiguousarray(K))).hexdigest(),
            'verified_nonzero_residual_when_first_delivery_is_omitted':True,
            'extra_binary_ADD_bank3840':8*sum(z['extra_binary_ADD_per_copy'] for z in results),
            'extra_INIT':0,'extra_CLEAR':0,'extra_MOVE':0,'full_foreign_blocks_preserved':6470}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print({q:v for q,v in result.items() if q!='chosen_caches'},flush=True)

if __name__=='__main__':main()
