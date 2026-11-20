#!/usr/bin/env python3
"""Indigenous donor-labelled true late taps through H,D,K and calibrated physical facets."""
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
import importlib.util,json
from pathlib import Path
import numpy as np
def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def req(q,msg):
 if not q:raise ValueError(msg)
def make(a):
 root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','field');n=mod(root/'bit-spread-overlap-source/review/check.py','geom').Native(a.repo,f);past=mod(a.physical,'phys');p=past.Physical(a.repo,n,f,a.library)
 groups=defaultdict(list)
 for u,(ph,role,_,h,d,k,donor,facet) in p.routes.items():
  if ph=='Y' and donor is not None and h is not None:groups[donor,h].append(u)
 for arr in groups.values():arr.sort()
 end={}
 for i in range(111):
  _,held=p.terminal(i);V=np.load(a.gauges/f'F{i}.npz')['V'];scale={}
  for h,(k,v) in held.items():
   if h<53280:continue
   t=0 if k==3 else 96
   scale[h]=p.mm(V[:,t:t+32*k],v[:,None])[:,0]
  end[i]=scale
 hashes={};a.cache.mkdir(parents=True,exist_ok=True)
 for j in range(111):
  owners=sorted(u for h in n.hlist[j]for u in groups[j,h]);at={u:t for t,u in enumerate(owners)};width=len(owners);left={}
  for h in n.hlist[j]:
   ids=groups[j,h]
   if not ids:continue
   who=sorted(n.H[h]&set(range(111)));q=n.early[j,h]//15;req(len(ids)==15 and q==1,'actual 15 late fields at each true late donor incidence')
   for k,low in [(3,0),(12,3)]:
    grp=who.index(j) if len(who)==3 else 0;w=p.waves[k][:,k*grp:k*grp+k]
    for rr,d in enumerate(p.fans[h][k]):
     u=p.flags[h,d,'Y'][0];v=np.zeros(width,dtype=np.uint8);v[[at[z] for z in ids[low:low+k]]]=w[rr];left[u]=v
  mids={}
  for d in {p.routes[u][4] for u in left}:
   ids=p.middle[d];ix=[q for q,u in enumerate(ids) if u in left];iy=[q for q,u in enumerate(ids) if u>=53280]
   Z=p.mm(p.dword(d)[np.ix_(iy,ix)],np.vstack([left[ids[q]]for q in ix]));mids.update((ids[q],z)for q,z in zip(iy,Z))
  values={}
  for h in {p.routes[u][5] for u in mids if str(p.routes[u][5]) in p.K}:
   for ph,ins,outs in p.K[str(h)]['stripes']:
    if ph!='Y':continue
    ix=[q for q,u in enumerate(ins)if u in mids]
    if ix:
     k=len(ins)//3;Z=p.mm(p.waves[k][ix].T,np.vstack([mids[ins[q]]for q in ix]));values.update(zip(outs,Z))
  records=[]
  for i in sorted(n.adj[j]&set(range(111))):
   ys=sorted(set(values)&end[i].keys());records.append(p.mm(np.stack([end[i][t]for t in ys]).T,np.stack([values[t]for t in ys])))
  actual=np.stack(records);hashes[j]=sha256(actual.tobytes()).hexdigest();np.save(a.cache/f'L{j}.npy',actual);np.save(a.cache/f'IDs{j}.npy',np.asarray(owners))
 a.out.mkdir(exist_ok=True,parents=True);(a.out/'GENUINE-LATE-INPUTS.json').write_text(json.dumps(hashes,sort_keys=True,indent=2)+'\n');print('Independent late-to-facet maps',len(hashes),flush=True)
if __name__=='__main__':
 p=ArgumentParser()
 for n in ('repo','physical','library','gauges','cache','out'):p.add_argument('--'+n,type=Path,required=True)
 make(p.parse_args())
