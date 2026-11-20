"""One original input separating every unassigned proper block from the full target."""
from collections import Counter
from hashlib import sha256
import numpy as np
def complete(args):
    ar,pr,inputs,outputs,apply,adj,terms,body,lane,fun,E,B,VS,Taps,L=args
    mm=ar.mm;x0=pr.rand('all original targets complete exclusion sample 0',(3840,1));xs=[apply(inputs[j],x0).reshape(8,480).T.copy()for j in range(111)];ls=[]
    for j,x in enumerate(xs):
        t=Taps[j];ell=np.hstack([mm(t['central'],x[:,:1]),mm(t['rim'],x[:,1:])])
        for k in t:
            if k.startswith('H-'):
                _,g,e=k.split('-');ell[:,int(g):int(g)+1]^=mm(t[k],mm(t['G-'+g+'-'+e],x[:,int(e):int(e)+1]))
        ls.append(ell)
    exact=set();diff=Counter();digest=sha256()
    for i,js in enumerate(adj):
        vals=[];target=[]
        for ii,j in enumerate(js):
            x=xs[j];ev=mm(E[i][ii],x);y=mm(VS[i]['V'],mm(B[i][ii],x)^mm(VS[i]['S'],ev))^mm(L[j][adj[j].index(i)],ls[j])
            if f'A-{i}' in fun:
                C=fun[f'A-{i}'];oy=fun[f'ids-{i}']
                for e in range(8):
                    k=f'Q-{i}-{e}'
                    if k not in fun:continue
                    v=mm(C,mm(fun[k],ev[:,e:e+1]))[:,0]
                    for g in set(lane[oy]):
                        ix=lane[oy]==g;y[body[oy[ix]],int(g)]^=v[ix]
            vals.append(y.T.reshape(-1));target.append(apply([('T',i,j,False)] if (i,j)in terms else [],x0)[:,0])
        Z=apply(outputs[i],np.stack(vals,axis=1))^np.stack(target,axis=1);digest.update(np.ascontiguousarray(Z))
        for j,z in zip(js,np.count_nonzero(Z,axis=0)):
            diff[int(z)]+=1
            if not z:exact.add((i,j))
    return exact,{'all_genuine_native_differences_sha256':digest.hexdigest(),'literal_original_input_sha256':sha256(x0).hexdigest(),'separated_proper_edges':sum(v for k,v in diff.items()if k),'equal_proper_edges':len(exact),'minimum_nonzero_fields_per_separated_edge':min(k for k in diff if k),'true_pairs_checked':sum(diff.values())}
