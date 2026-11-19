#!/usr/bin/env python3
"""Exact controls for the written repair gates, not a native code search."""
import argparse, gzip, hashlib, json, random
from pathlib import Path
import numpy as np

def gf_mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        b>>=1; a<<=1
        if a&8:a^=11
    return c
MUL=np.array([[gf_mul(a,b) for b in range(8)] for a in range(8)],dtype=np.uint8)
INV=np.array([0]+[next(b for b in range(1,8) if gf_mul(a,b)==1) for a in range(1,8)],dtype=np.uint8)

def gf_rank(a):
    a=np.array(a,dtype=np.uint8,copy=True)
    if a.ndim!=2: raise ValueError('matrix')
    row=0
    for col in range(a.shape[1]):
        candidates=np.flatnonzero(a[row:,col])
        if not len(candidates):continue
        p=row+int(candidates[0]); a[[row,p]]=a[[p,row]]
        a[row]=MUL[INV[a[row,col]],a[row]]
        inds=np.flatnonzero(a[:,col]); inds=inds[inds!=row]
        a[inds]^=MUL[a[inds,col,None],a[row][None,:]]
        row+=1
        if row==len(a):break
    return row

def gf_product(a,b):
    ans=np.zeros((a.shape[0],b.shape[1]),dtype=np.uint8)
    for k in range(a.shape[1]):ans^=MUL[a[:,k,None],b[k,None,:]]
    return ans

def binary_basis(rows):
    basis={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
    return list(basis.values())

def nullspace(rows,n):
    rows=list(rows); piv=[];r=0
    for c in range(n):
        found=next((k for k in range(r,len(rows)) if rows[k]>>c&1),None)
        if found is None:continue
        rows[r],rows[found]=rows[found],rows[r]
        for k in range(len(rows)):
            if k!=r and rows[k]>>c&1:rows[k]^=rows[r]
        piv.append(c);r+=1
    free=[c for c in range(n) if c not in piv]
    return [((1<<c)|sum((1<<p) for p,row in zip(piv,rows) if row>>c&1)) for c in free]

def arr(rows,n):return np.array([[(r>>i)&1 for i in range(n)] for r in rows],dtype=np.uint8)
def span_dim(rows):return len(binary_basis(rows))
def intersection_dim(spaces,n):return n-span_dim([v for s in spaces for v in nullspace(s,n)])
def random_subspace(rng,ambient,dim):
    out=[]
    for _ in range(500):
        x=0
        for v in ambient:
            if rng.randrange(2):x^=v
        out=binary_basis(out+[x])
        if len(out)==dim:return out
    raise ValueError('failed bounded finite control generation')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    root=a.repo/'research/moonshot-005-program'
    path=root/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    roots=json.loads(raw)['root_table']
    orows=[sum(1<<j for j in range(111) if sum(x*y for x,y in zip(roots[i],roots[j]))==0) for i in range(111)]
    krows=[r^(1<<i) for i,r in enumerate(orows)];hrows=binary_basis(krows)
    assert len(hrows)==9 and span_dim(orows)==108
    mask=(1<<111)-1
    assert all(span_dim([h&(mask^o) for h in hrows])==9 for o in orows)
    crows=nullspace(hrows,111);assert len(crows)==102
    H=np.kron(arr(hrows,111),np.eye(2,dtype=np.uint8))
    C=np.kron(arr(crows,111).T,np.eye(2,dtype=np.uint8))
    O=np.kron(arr(orows,111),np.eye(2,dtype=np.uint8))
    i=0;j=next(j for j in range(111) if orows[i]>>j&1)
    spectral=[]
    for perturb in (0,2,3,4,5,6,7):
        B=O.copy();B[2*i+1,2*j+1]^=perturb
        ranks=[]
        for t in range(1,8):
            scale=np.array([1,t]*111,dtype=np.uint8)
            Bt=MUL[B,scale[None,:]];E=Bt^O
            rc=gf_rank(gf_product(E,C))
            rq=gf_rank(np.concatenate([H,E]))-18
            assert rc==rq
            assert np.all(E[::2,:]==0)
            for ii,o in enumerate(orows):
                block=E[2*ii:2*ii+2,:]
                assert gf_rank(block)<=rq
            ranks.append(rc)
        N=102
        assert sum(max(0,N-r) for r in ranks)<=N
        cheap=[(t,r) for t,r in enumerate(ranks,1) if r<=1]
        assert len(cheap)<=1
        if cheap:
            tt,rr=cheap[0]
            assert all(r>=N-rr for t,r in enumerate(ranks,1) if t!=tt)
        spectral.append({'perturbation':perturb,'ranks_t1_to_t7':ranks,'N':N,'cheap':cheap})
    rng=random.Random(261119);robust=0;nontrivial=0
    for _ in range(4000):
        n=8;r=rng.choice([1,2]);q=rng.choice([1,2,3]);s=rng.choice([2,3,4]);p=rng.choice([q,q+1,q+2])
        full=[1<<i for i in range(n)];U=random_subspace(rng,full,q);R=random_subspace(rng,full,r)
        targets=[]
        for ii in range(s):
            Z=U[:]
            while len(Z)<p:Z=binary_basis(Z+[rng.randrange(1<<n)])
            T=random_subspace(rng,binary_basis(Z+R),p)
            assert span_dim(T+Z+R)==span_dim(Z+R)
            assert q-intersection_dim([U,T],n)<=r
            targets.append(T)
        shared=intersection_dim(targets,n);ur=intersection_dim([U,R],n)
        bound=shared+(s-1)*(r-ur)
        assert q<=bound
        robust+=1;nontrivial+=q>shared
    sharp=[]
    for r in (1,2,3):
        for s in (2,3,4,5):
            q=(s-1)*r;n=q+r;U=[1<<i for i in range(q)];R=[1<<(q+i) for i in range(r)]
            targets=[U]
            for i in range(s-1):
                targets.append([v^(R[j%r] if j//r==i else 0) for j,v in enumerate(U)])
            inter=intersection_dim(targets,n)
            assert inter==0 and q==(s-1)*r
            sharp.append({'receivers':s,'repair_rank':r,'port_rank':q,'target_intersection_rank':inter})
    result={'status':'PASS_EXACT_REPAIR_GATES','native':{'roles':111,'rank_O':108,'rank_H':9,'outside_neighbor_restrictions_full_rank':111},'spectral_native_algebra_controls':spectral,'robust_random_exact_cases':robust,'nontrivial_robust_cases':nontrivial,'sharp_shared_repair_cases':sharp,'target_constants':{'b':5760,'k':70,'R':202,'canonical_null_dimension':587520,'required_fixed_dimension':587318,'scaling_U_dimension':580380,'other_scale_rank_floor':580178},'scope':'Algebraic controls only; native algebra matrices are not asserted to have physical balanced realizations.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    pins=[]
    for p in ['results/bit-seventy-common-coordinates/author/PROOF.md','results/bit-native-cycle-and-inlet-gates/author/PROOF.md','results/bit-stripe-varying-port-cut/author/PROOF.md','results/bit-all111-balanced-causal-atlas/author/BALANCED-PROOF.md']:
        data=(root/p).read_bytes();pins.append({'path':'research/moonshot-005-program/'+p,'sha256':hashlib.sha256(data).hexdigest()})
    (a.out/'SOURCE-PINS.json').write_text(json.dumps({'programme_baseline':'d8544284cbd0527cd03a0aad576a2d2c6eddcc0e','sources':pins,'layout_uncompressed_sha256':hashlib.sha256(raw).hexdigest()},indent=2)+'\n')
    print(result['status'],len(spectral),'native algebra controls;',robust,'robust cases')

if __name__=='__main__':main()
