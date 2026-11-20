"""Forward K/F replay and a native facet calibration on the common D120 fibres."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import numpy as np


def pivots(A,atlas):
    M=A.copy();p=[]
    for col in range(M.shape[1]):
        r=len(p);nz=np.flatnonzero(M[r:,col])
        if not len(nz):
            continue
        t=r+int(nz[0]);M[[t,r]]=M[[r,t]]
        M[r]=atlas.product[atlas.inverse[M[r,col]],M[r]]
        fac=M[:,col].copy();fac[r]=0;M^=atlas.product[fac[:,None],M[r,None,:]];p.append(col)
        if len(p)==len(M):
            break
    return p,M


def calibrate(atlas,matrix,target):
    """Both 96-by-eight matrices have full column rank; extend each to a basis."""
    def basis(M):
        pp,_=pivots(M.T,atlas)
        assert len(pp)==8
        rest=[s for s in range(len(M)) if s not in pp]
        return np.hstack([M,np.eye(len(M),dtype=np.uint8)[:,rest]])
    X=basis(matrix);Z=basis(target)
    p,M=pivots(np.hstack([X,np.eye(len(X),dtype=np.uint8)]),atlas)
    assert p==list(range(96))
    out=atlas.mm(Z,M[:,len(X):]);assert np.array_equal(atlas.mm(out,matrix),target)
    return out


def forward(base,atlas,terminal,rs,compiler,routes,physical_rows,ks,U,responses):
    def identity(r):
        return (53280 if r[0]=='Y' else 0)+480*r[1]+r[2]
    route={identity(r):r for r in routes}
    d_out=sorted(identity(r) for r in routes if r[4]==120)
    k_dir=base/'bit-gf64-actual-k-atlas/author/output'
    words=terminal.payload(k_dir/'SPREAD-OWNERS.json.gz',terminal.K_PINS['spread'])
    phases=json.loads(compiler.unpack(base,'phases'))
    out={};Id=np.eye(8,dtype=np.uint8);zero=np.zeros(8,dtype=np.uint8)
    for i,small in responses.items():
        keys=[q for q in ks if i in atlas.planes[q]]
        ids=[d_out[physical_rows[q,b]] for b in range(2) for q in keys]
        assert len(ids)==len(set(ids))==8 and all(route[u][5] in keys for u in ids)
        delivered=dict(zip(ids,Id));facet=np.zeros((480,8),dtype=np.uint8)
        planes=atlas.by_donor[i]
        first=set([h for h in planes if atlas.quota[i,h]==15][:12])
        for pos,h in enumerate(planes):
            p=phases[str(h)];chart=words[str(h)];values={};meta={};stripes=Counter()
            for kind,ins,outs in chart['stripes']:
                n=len(ins);s=stripes[kind,n];stripes[kind,n]+=1
                V=atlas.vandermonde(range(1,n+1),n)
                X=np.array([delivered.get(u,zero) for u in ins])
                YY=atlas.mm(V.T,X)
                for t,(u,row) in enumerate(zip(outs,YY)):
                    values[u]=row;meta[u]=(kind,n,s,t)
            for a,b in chart['early_cache_to_late']:
                values[b]^=values[a]
            for u,row in values.items():
                kind,n,s,t=meta[u];destination=route[u][1] if kind=='Y' else route[u][7]
                if destination!=i:
                    continue
                _,channel,derivative,scale=terminal.k_row(kind,p['m'],atlas.quota[i,h],i,t,n,h in first,s,0)
                offset=(0 if n==9 else 96)+16*channel
                coeff=rs.coefficients(pos+1,derivative,scale)
                facet[offset:offset+16]^=atlas.product[np.array(coeff,dtype=np.uint8)[:,None],row[None,:]]
        assert atlas.rank(facet)==8 and not np.any(facet[96:])
        expected=np.zeros((96,8),dtype=np.uint8)
        for lane in range(2):
            for t in range(16):
                for beta in range(3):
                    expected[(3*lane+beta)*16+t,4*lane:4*lane+4]=U[i][3*t+beta]
        actual=atlas.mm(facet[:96],small);calibration=calibrate(atlas,actual,expected)
        assert atlas.rank(calibration)==96 and np.array_equal(atlas.mm(calibration,actual),expected)
        ops=len(compiler.compile_binary(compiler.bit_rows(calibration.tolist())))
        # The source kept the H263 physical original address 16s+8*lane+e.
        # Its eight-copy grouped positions at the raw RS facet use a different permutation.
        perm=[None]*768
        raw=np.zeros((768,64),dtype=np.uint8)
        wanted=np.zeros_like(raw)
        for e in range(8):
            raw[96*e:96*(e+1),8*e:8*(e+1)]=atlas.mm(calibration,actual)
            for lane in range(2):
                for t in range(16):
                    for beta in range(3):
                        s=3*t+beta;dest=16*s+8*lane+e
                        perm[dest]=96*e+(3*lane+beta)*16+t
                        wanted[dest,8*e+4*lane:8*e+4*(lane+1)]=U[i][s]
        assert sorted(perm)==list(range(768)) and np.array_equal(raw[perm],wanted)
        assert not np.array_equal(raw,wanted)
        swaps=compiler.swap_cycles(perm)
        out[i]={'D_boundary_real_field_owner_ids':ids,'K_labels':keys,'raw_facet_rank':atlas.rank(actual),
                'raw_facet_common_readout_sha256':hashlib.sha256(actual.tobytes()).hexdigest(),
                'calibrated_original_readout_sha256':hashlib.sha256(expected.tobytes()).hexdigest(),
                'calibration_field_coefficients_sha256':hashlib.sha256(calibration.tobytes()).hexdigest(),
                'physical_original_identity_sha256':hashlib.sha256(wanted.tobytes()).hexdigest(),
                'actual_cross_copy_permutation_field_swaps':swaps,
                'actual_cross_copy_permutation_forward_ADD':18*swaps,
                'facet_calibration_forward_ADD_on_eight_actual_copies':8*ops+18*swaps,
                'facet_calibration_reserved_inverse_ADD_on_eight_actual_copies':8*ops+18*swaps}
    return out
