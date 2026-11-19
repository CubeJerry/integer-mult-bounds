#!/usr/bin/env python3
"""Finite witness search for full covariant Clifford source family."""
from __future__ import annotations
from pathlib import Path
from itertools import combinations
from collections import Counter,deque
import argparse,gzip,json,time
import numpy as np
import algebra as mod

HERE=Path(__file__).resolve().parent

def tables():
    def mul(a,b):
        c=0
        while b:
            if b&1:c^=a
            a<<=1
            if a&16:a^=19
            b>>=1
        return c
    T=np.array([[mul(a,b)for b in range(16)]for a in range(16)],dtype=np.uint8)
    inv=np.array([0]+[next(b for b in range(1,16)if T[a,b]==1)for a in range(1,16)],dtype=np.uint8)
    return T,inv

def field_rank(A,T,inv):
    A=A.copy();r=0
    for c in range(A.shape[1]):
        ids=np.flatnonzero(A[r:,c])
        if not len(ids):continue
        k=r+int(ids[0]);A[[r,k]]=A[[k,r]];A[r]=T[inv[A[r,c]],A[r]]
        factors=A[r+1:,c].copy();A[r+1:]^=T[factors[:,None],A[r][None,:]];r+=1
        if r==A.shape[0]:break
    return r

def binary_array(A,n):return np.array([[(row>>j)&1 for j in range(n)]for row in A],dtype=np.uint8)
def bapply(A,v):
    out=np.zeros(A.shape[0],dtype=np.uint8)
    for j in range(A.shape[1]):out^=A[:,j]*v[j]
    return out

def family(j,k,vectors):
    # Actual full 16x256 map sum_C tau_H(C X) v_C.
    jA=binary_array(j,16);kA=binary_array(k,16);out=np.zeros((16,16,16),dtype=np.uint8)
    jk=mod.mm(j,k);kj=mod.mm(k,j)
    for C,v in zip([mod.eye(16),j,k,jk],vectors):
        factors=[(mod.mm(jk,C),v),(mod.mm(j,C),bapply(kA,v)),
                 (mod.mm(k,C),bapply(jA,v)),(C,bapply(binary_array(kj,16),v))]
        for L,r in factors:out^=binary_array(L,16)[:,:,None]*r[None,None,:]
    return out.reshape(16,256)

def early_quota(routes,planes):
    counts=Counter()
    for row in routes:
        if row[0]=='X':counts[row[1],row[3]]+=1
    out={}
    for (j,h),count in counts.items():
        assert count%15==0;out[j,h]=count*8//15
    assert set(out.values())=={8,16,24}
    for j in range(111):assert sum(v for (k,h),v in out.items()if j==k)==256
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--only-pair',action='store_true');args=ap.parse_args();start=time.time()
    base=args.repo/'research/moonshot-005-program/results'
    layout=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    cert=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    gam,adj,K=mod.geometry(layout,cert);roots=layout['root_table'];planes=list(map(set,layout['A2']))
    alladj=[{j for j,y in enumerate(roots)if i!=j and sum(a*b for a,b in zip(x,y))==0}for i,x in enumerate(roots)]
    # All q=1 orthogonal ordered pairs form one explicit transvection orbit.
    rootlookup={tuple(root):i for i,root in enumerate(roots)}
    # Native gamma matrices uniquely encode quadratic vectors; XOR is addition.
    gl={tuple(g):i for i,g in enumerate(gam)}
    perms=[]
    for u in range(120):
        perm=[]
        for v in range(120):
            gv=mod.mm(mod.mm(gam[u],gam[v]),gam[u]);perm.append(gl[tuple(gv)])
        assert len(set(perm))==120;perms.append(perm)
    origin=(5,77);parents={origin:None};queue=deque([origin])
    while queue:
        pair=queue.popleft()
        for u,perm in enumerate(perms):
            nxt=(perm[pair[0]],perm[pair[1]])
            if nxt not in parents:parents[nxt]=[pair[0],pair[1],u];queue.append(nxt)
    expected={(i,j)for i in range(120)for j in alladj[i]}
    assert set(parents)==expected and len(expected)==7560
    T,inv=tables();rng=np.random.default_rng(276464)
    i,j=origin;hs=[h for h,H in enumerate(planes)if j in H and H<=alladj[i]];assert len(hs)==16
    pair_witness=None;pair_hist=Counter()
    for trial in range(32):
        vs=rng.integers(0,16,(16,4,16),dtype=np.uint8)
        F=np.concatenate([family(gam[j],gam[next(k for k in sorted(planes[h])if k!=j)],v)for h,v in zip(hs,vs)])
        r=field_rank(F,T,inv);pair_hist[r]+=1
        if r==256:pair_witness={'pair':[i,j],'planes':hs,'vectors':vs.tolist(),'trial':trial};break
    assert pair_witness is not None
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'PAIR-WITNESS.json').write_text(json.dumps(pair_witness,indent=2)+'\n')
    orbit={'origin':list(origin),'count':len(parents),'edges':[[i,j]+p for(i,j),p in sorted(parents.items())if p is not None]}
    (args.out/'ORBIT.json.gz').write_bytes(gzip.compress((json.dumps(orbit,separators=(',',':'))+'\n').encode(),mtime=0))
    print(json.dumps({'pair_histogram':dict(pair_hist),'orbit':len(parents),'elapsed':time.time()-start}),flush=True)
    if args.only_pair:return
    routes=[json.loads(line)for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
    quota=early_quota(routes,planes);early=[];early_hist=Counter()
    for donor in range(111):
        hs=sorted(h for(j,h)in quota if j==donor)
        found=None
        for trial in range(32):
            rows=[];assignment=[]
            for h in hs:
                vectors=rng.integers(0,16,(4,16),dtype=np.uint8)
                F=family(gam[donor],gam[next(k for k in sorted(planes[h])if k!=donor)],vectors)
                n=min(16,quota[donor,h]);L=rng.integers(0,16,(n,16),dtype=np.uint8)
                E=np.zeros((n,256),dtype=np.uint8)
                for k in range(16):E^=T[L[:,k,None],F[k,None,:]]
                rows.append(E)
                extra=rng.integers(0,16,(max(0,quota[donor,h]-16),256),dtype=np.uint8)
                if len(extra):rows.append(extra)
                assignment.append({'plane':h,'vectors':vectors.tolist(),'early_output_rows':L.tolist(),'extra_rows':extra.tolist()})
            M=np.concatenate(rows);assert M.shape==(256,256)
            r=field_rank(M,T,inv);early_hist[r]+=1
            if r==256:found={'donor':donor,'trial':trial,'flags':assignment};break
        assert found is not None,('early failure',donor,dict(early_hist))
        early.append(found)
        if donor%10==0:print(json.dumps({'early_complete':donor+1,'early_histogram':dict(early_hist),'elapsed':time.time()-start}),flush=True)
    (args.out/'EARLY-WITNESSES.json.gz').write_bytes(gzip.compress((json.dumps(early,separators=(',',':'))+'\n').encode(),mtime=0))
    summary={'status':'FOUND_FULL_COVARIANT_SOURCE_WITNESSES','pair_histogram':dict(pair_hist),'early_histogram':dict(early_hist),
             'orthogonal_pair_orbit':len(parents),'native_foreign_pairs':6470,'early_donors':len(early),'elapsed_seconds':time.time()-start}
    (args.out/'SEARCH.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
