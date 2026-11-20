from collections import Counter,defaultdict
from hashlib import sha256
from itertools import combinations
import json
import numpy as np
def run(q,ar,pr,op,adj,body,lane,fun,E,B,VS,Taps,L):
 mm=ar.mm;res={};q.mkdir(parents=True,exist_ok=True)
 for tr in (False,True):
  probe=pr.rand('native endpoint cycle controls/'+str(int(tr)),(3840,80));center=10 if tr else 80;site=defaultdict(dict)
  for leaf in adj[center]:
   i0,j0=(leaf,10) if tr else(80,leaf);P=op('B',i0,j0);X=P.apply(probe,True,tr).reshape(8,480,80);assert np.array_equal(P.apply(X.reshape(3840,80),False,tr),probe)
   for v in adj[leaf]:
    if v==center:continue
    i,j=(leaf,v)if tr else(v,leaf);ix=adj[i].index(j);base=B[i][ix];early=E[i][ix];V,S=VS[i]['V'],VS[i]['S'];ls=L[j][adj[j].index(i)];t=Taps[j]
    if tr:
     D=mm(V.T,X[1]);EE=mm(S.T,D);lr=mm(ls.T,X[1]);M=mm(base[:,:80].T,D)^mm(t['rim'][:,:80].T,lr)
     if f'A-{i}'in fun and f'Q-{i}-1'in fun:
      ids=fun[f'ids-{i}'];a=fun[f'A-{i}'];raw=np.stack([X[int(g),int(r)]for g,r in zip(lane[ids],body[ids])]);EE^=mm(fun[f'Q-{i}-1'].T,mm(a.T,raw))
     M^=mm(early[:,:80].T,EE)
     for g in range(8):
      k=f'H-{g}-1'
      if k in t:M^=mm(t[f'G-{g}-1'][:,:80].T,mm(t[k].T,mm(ls.T,X[g])))
    else:
     e=mm(early,X[1]);rel=mm(t['rim'],X[1]);M=mm(V[:80],mm(base,X[1])^mm(S,e))
     for e0 in range(8):
      k=f'H-1-{e0}'
      if k in t:rel^=mm(t[k],mm(t[f'G-1-{e0}'],X[e0]))
     M^=mm(ls[:80],rel)
     if f'A-{i}' in fun:
      ids=fun[f'ids-{i}'];a=fun[f'A-{i}'];ii=(lane[ids]==1)&(body[ids]<80)
      if ii.any():
       for e0 in range(8):
        if f'Q-{i}-{e0}'in fun:M[body[ids[ii]]]^=mm(a[ii],mm(fun[f'Q-{i}-{e0}'],mm(early,X[e0])))
    site[v][leaf]=M
  hist=Counter();dig=sha256()
  for v,T in sorted(site.items()):
   for j,k in combinations(sorted(T),2):
    r=len(ar.reduce(T[j]^T[k]));hist[r]+=1;dig.update(bytes([v,j,k,r]))
  assert min(hist)>64;res[str(tr)]={'native_exact_pair_ranks':dict(hist),'ordered_sha256':dig.hexdigest(),'complete_pair_count':sum(hist.values())}
  (q/'ONE-SIDED.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(tr,res[str(tr)],flush=True)
