"""Reconstruct the exact previously specified facet on all genuine input owners."""
from pathlib import Path
import numpy as np


def restore(field,previous,target,flat_params,primal_params,native,cache):
    adj=[sorted(native.orth[i]&set(range(111))) for i in range(111)]
    U=previous.coefficients(flat_params['U8_SHAKE_tag'],(480,8));terms=target.assignment(native.results/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json')
    raw,copy,body=target.source_target_coordinates();US=np.zeros((8,3840,8),dtype=np.uint8)
    for e,ids in enumerate(raw):US[e,ids]=U
    E={i:np.load(cache/f'E{i}.npy',mmap_mode='r',allow_pickle=False) for i in range(111)}
    B={i:np.load(cache/f'B{i}.npy',mmap_mode='r',allow_pickle=False) for i in range(111)}
    VS={};updates={};tiers=primal_params['dimensions']
    for i,js in enumerate(adj):
        src=E[i];S,V=target.previous_facet(field,previous,flat_params,i,js,B[i],src,U);VS[i]=(V,S)
        active=[j for j in js if (i,j) in terms]
        if not active:continue
        bank=terms[i,active[0]][0];dest=np.arange(64*bank,64*(bank+1));targets={}
        for e in range(8):
            pieces=[]
            for j in js:
                m=tiers[j];Y=np.zeros((64,m),dtype=np.uint8)
                if (i,j) in terms:
                    _,original,op=terms[i,j];Y=field.mm(op,US[e,original*64:64*(original+1),:m])
                pieces.append(Y)
            targets[e]=np.hstack(pieces)
        T=np.hstack(list(targets.values()));A=T[:,field.pivots(T)];positions=field.pivots(A.T)
        left,_=field.invert_and_price(A[positions]);D=np.hstack([field.mm(M,U[:,:tiers[j]]) for M,j in zip(src,js)])
        piv=field.pivots(D.T);right,_=field.invert_and_price(D[piv]);cols={}
        for e,want in targets.items():
            if not np.any(want):continue
            t=primal_params['choices'][str(i)][str(e)];r=A.shape[1];width=src.shape[1]
            L=previous.coefficients(f'exact two-sided/{i}/{e}/{t}',(r,width)).copy() if t else np.zeros((r,width),dtype=np.uint8)
            L[:,piv]^=field.mm(field.mm(left,want[positions])^field.mm(L,D),right)
            if not np.array_equal(field.mm(A,field.mm(L,D)),want):raise ValueError('true preceding target facet reaction')
            M=field.mm(A,L)
            for g in set(copy[dest]):
                selected=np.flatnonzero(copy[dest]==g);part=M[selected]
                if np.any(part):cols[int(g),e]=(body[dest[selected]],part)
        updates[i]=cols
    return {'adj':adj,'E':E,'B':B,'VS':VS,'updates':updates,'raw':raw,'copy':copy,'body':body,'terms':terms,'tiers':tiers,'U':U}
