#!/usr/bin/env python3
"""Exact full-portfolio relay screen with every incoming chart into a common receiver recoded."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from side_stock import *
from collections import deque
cs=defaultdict(list)
for (aa,b),X in edge.items():
 for c in {moves[e][1] for e in out[b] if e in moves}:
  if (dim[aa]-dim[b])*(dim[b]-dim[c])<=0:continue
  Y=edge[b,c];W=[f for f in out[b] if f not in Y];ker=relations([{i:forms[f][x]for i,f in enumerate(W)if x in forms[f]}for x in X],len(W))
  if not ker:continue
  mu=ker[0];lost={inc[c].index(f):sum(forms[f].get(x,0)*mu.get(i,0)for i,x in enumerate(X))for f in Y};lost={i:v for i,v in lost.items()if v}
  cs[c].append((aa,b,X,Y,mu,lost))

@cache
def projected(c,s):return [v for u,v in intersect(s,c)]

stats=Counter();edges0=[];all_receivers=[];blocked=[];start=time.monotonic()
for c,proposals in cs.items():
 sources={moves[f][0] for f in inc[c] if f in moves}|{aa for aa,_,_,_,_,_ in proposals}
 ni=len(proposals);comp={i:set()for i in range(ni)};probes=[]
 for j,(aa,b,X,Y,mu,lost)in enumerate(proposals):
  pivot=next(iter(lost));xpos=[inc[b].index(x) for x in X]
  reachable=set();pred=defaultdict(set);cross={}
  for s in sources:
   rows=projected(c,s)
   if s==b:
    original=intersect(s,c);lv=[{0:sum(u.get(xpos[i],0)*k for i,k in mu.items())}for u,v in original]
    rows=[combine(z,rows)for z in relations(lv,1)]
   hits=set()
   for v in rows:
    if sum(lost.get(i,0)*k for i,k in v.items()):reachable.add(s);break
    for i,k in v.items():
     f=inc[c][i]
     if f in moves and i!=pivot:hits.add(moves[f][0])
   else:
    for g in hits:pred[g].add(s)
  queue=deque(reachable)
  while queue:
   s=queue.popleft()
   for x in pred[s]-reachable:reachable.add(x);queue.append(x)
  possible=[i for i,(a1,b1,*_)in enumerate(proposals) if a1 in reachable]
  for i in possible:comp[i].add(j);edges0.append([c,proposals[i][0],proposals[i][1],aa,b]);stats['edge']+=1
  assert j not in possible
  probes.append([aa,b,sorted(reachable),possible]);stats['target']+=1;stats['seen_source_pairs']+=len(proposals)
 # General acyclicity on all distinct candidate indices, ignoring hardware compatibility.
 indeg=[0]*ni
 for a1,children in comp.items():
  for j in children:indeg[j]+=1
 queue=deque(i for i,v in enumerate(indeg)if not v);order=[]
 while queue:
  i=queue.popleft();order.append(i)
  for j in comp[i]:
   indeg[j]-=1
   if not indeg[j]:queue.append(j)
 remain=[i for i,v in enumerate(indeg)if v];stats['cyclic_core']+=len(remain)
 if remain:blocked.append([c,[proposals[i][:2]for i in remain]])
 all_receivers.append([c,probes,order]);
 if len(proposals)>15:print('pooled sink',c,'size',ni,'edges',sum(map(len,comp.values())),'core',remain,'t',round(time.monotonic()-start,1),flush=True)
receipt={'stats':stats,'cross_edges':edges0,'unpeeled':blocked,'grouped_sink_certificates':all_receivers}
(a.out/'POOLED-CUT.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n');print('complete',stats,'difficult sinks',blocked,flush=True)
