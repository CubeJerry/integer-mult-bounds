"""Exact numerical interfaces for three-copy covariant source experiments."""
from collections import Counter
from hashlib import sha256
import gzip,json
import numpy as np
import algebra as a
from check import inverse,mm

def data(repo):
    base=repo/a.PROGRAMME/'results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    rp=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    layout=a.unpack(lp);masks,gamma,adj=a.geometry(layout,a.unpack(bp));planes=list(map(set,layout['A2']))
    counts=Counter()
    for line in gzip.decompress(rp.read_bytes()).splitlines():
        z=json.loads(line)
        if z[0]=='X':counts[z[1],z[3]]+=1
    quotas={key:n*8//15 for key,n in counts.items()}
    actual={j:sorted(h for donor,h in quotas if donor==j)for j in range(111)}
    views={j:{i:[h for h in actual[j]if planes[h]<=adj[i]]for i in sorted(adj[j]&set(range(111)))}for j in range(111)}
    return {'layout':layout,'gamma':gamma,'adj':adj,'planes':planes,'quotas':quotas,'actual':actual,'views':views,
            'pins':[{'path':str(p.relative_to(repo)),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [lp,bp,rp]]}

def units(gamma,plane,j):
    k=min(plane-{j});I=np.eye(16,dtype=np.uint8)
    N,M=gamma[j]^I,gamma[k]^I
    return [a.binary_product(N,M),N,M,a.binary_product(M,N)]

def source(C,R):
    """R[unit,column,out_copy,in_copy]; input copy,row,column order."""
    s=C[0].shape[0];out=np.zeros((3,s,3,s,16),dtype=np.uint16)
    for matrix,r in zip(C,R):
        out^=r.transpose(1,2,0)[:,None,:,None,:]*matrix[None,:,None,:,None]
    return out.reshape(3*s,3*s*16)

def kernel_coordinates(gamma,T,iv):
    N=gamma^np.eye(16,dtype=np.uint8);cols=[];ids=[]
    for t in range(16):
        new=np.column_stack(cols+[N[:,t]])
        if a.rank(new,T,iv)>len(cols):cols.append(N[:,t]);ids.append(t)
    a.require(len(cols)==8,'rank-eight nilpotent gamma+I')
    K=np.column_stack(cols);L=np.eye(16,dtype=np.uint16)[:,ids]
    P=np.column_stack([K,L]);R=inverse(P,T,iv)[:8]
    a.require(np.array_equal(mm(R,K,T),np.eye(8,dtype=np.uint16)),'kernel coordinates left inverse')
    a.require(not np.any(a.binary_product(N,K)),'image is kernel')
    return K.astype(np.uint8),R.astype(np.uint8)

def prepare(d,j,T,iv):
    full={h:units(d['gamma'],d['planes'][h],j)for h in d['actual'][j]};reduced={}
    for i,hs in d['views'][j].items():
        K,R=kernel_coordinates(d['gamma'][i],T,iv);entry={}
        for h in hs:
            cs=[]
            for C in full[h]:
                cr=a.binary_product(a.binary_product(R,C),K)
                a.require(np.array_equal(a.binary_product(C,K),a.binary_product(K,cr)),'visible covariance restriction')
                a.require(a.rank(cr,T,iv)==4,'rank-four reduced parameter update')
                cs.append(cr)
            entry[h]=cs
        reduced[i]=entry
    return full,reduced

def view_rank(R,reduced,i,hs,T,iv):
    M=np.vstack([source(reduced[i][h],R[h])for h in hs])
    return a.rank(M,T,iv)

def early_map(d,j,R,full,T,iv,rng,tries=32):
    for attempt in range(1,tries+1):
        frames={};extras={};rows=[]
        for h in d['actual'][j]:
            q=3*d['quotas'][j,h]
            frames[h]=rng.integers(0,512,size=(24,48),dtype=np.uint16)if q==24 else np.eye(48,dtype=np.uint16)
            extras[h]=rng.integers(0,512,size=(24,768),dtype=np.uint16)if q==72 else np.zeros((0,768),dtype=np.uint16)
            F=source(full[h],R[h]);rows.append(mm(frames[h],F,T))
            if q==72:rows.append(extras[h])
        E=np.vstack(rows);a.require(E.shape==(768,768),'entire actual three-copy early map')
        rank=a.rank(E,T,iv)
        if rank==768:return frames,extras,attempt
    return None,None,tries
