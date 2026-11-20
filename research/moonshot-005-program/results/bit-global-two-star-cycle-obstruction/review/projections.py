"""Direct original source and dual endpoint probes against the complete native Schur words."""
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
def run(q,ar,pr,op,adj,body,lane,fun,E,B,VS,Taps,L):
    mm=ar.mm;y=pr.rand('complete nonflat bridge output probe',(3840,134));x=pr.rand('complete nonflat bridge input probe',(3840,130));left={};right={}
    for i in sorted(adj[10]):
        P=op('B',i,10);M=P.apply(y,True,True);assert np.array_equal(P.apply(M,False,True),y);Y=M.reshape(8,480,-1)
        D=[mm(VS[i]['V'].T,g)for g in Y];early=[mm(VS[i]['S'].T,d)for d in D]
        if f'A-{i}' in fun:
            amp=fun[f'A-{i}'];ids=fun[f'ids-{i}'];raw=np.stack([Y[int(g),int(b)]for g,b in zip(lane[ids],body[ids])])
            c=mm(amp.T,raw)
            for e in range(8):
                if f'Q-{i}-{e}' in fun:early[e]^=mm(fun[f'Q-{i}-{e}'].T,c)
        left[i]=(Y,D,early)
    for j in sorted(adj[80]):
        P=op('B',80,j);M=P.apply(x,True);assert np.array_equal(P.apply(M),x);X=M.reshape(8,480,-1);t=Taps[j];l=[mm(t['rim' if g else 'central'],X[g])for g in range(8)]
        for k in t:
            if k.startswith('H-'):
                _,g,e=k.split('-');l[int(g)]^=mm(t[k],mm(t['G-'+g+'-'+e],X[int(e)]))
        right[j]=(X,l)
    pins=sha256();seq=[];mats=[]
    for i,(Y,D,early)in sorted(left.items()):
        for j in sorted(set(adj[i])&set(right)):
            X,l=right[j];ix=adj[i].index(j);la=L[j][adj[j].index(i)];M=np.zeros((134,130),dtype=np.uint8)
            for g in range(8):M^=mm(D[g].T,mm(B[i][ix],X[g]))^mm(early[g].T,mm(E[i][ix],X[g]))^mm(Y[g].T,mm(la,l[g]))
            pins.update(M);seq.append((i,j));mats.append(M)
    x={'complete_native_probe_arrays':len(seq),'full_native_probe_sha256':pins.hexdigest(),'native_vertex_order_sha256':sha256(np.asarray(seq,dtype=np.uint8)).hexdigest()}
    assert x['full_native_probe_sha256']=='3f9bbea433c6f7f0b39723533ca6b6b0daabf385c60cd866badea32c1158833f' and len(seq)==1956
    q.mkdir(exist_ok=True,parents=True);(q/'NATIVE-PROBES.json').write_text(json.dumps(x,sort_keys=True,indent=2)+'\n');np.save(q/'DOUBLE-BRIDGES.npy',np.stack(mats));print(x,flush=True)
