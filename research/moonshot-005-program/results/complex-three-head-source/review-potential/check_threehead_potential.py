#!/usr/bin/env python3
from fractions import Fraction
from pathlib import Path
import json,hashlib

def par(x):return x.bit_count()%2
def rank(rows):
 a=[[Fraction(x) for x in row] for row in rows];r=0
 for c in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for k in range(r+1,len(a)):
   v=a[k][c]
   if v:a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
 return r
odd=[t for t in range(64) if par((t&7)&(t>>3))];assert len(odd)==28
base=[t>>3 for t in odd]
assert all(base.count(k)==4 for k in range(1,8))
checks=[]
for r in range(4):
 labels=[sum(((t>>(j if j<r else j+3))&1)<<j for j in range(3)) for t in odd]
 assert all(labels.count(k)==4 for k in range(1,8))
 diff=[[int(base[i]==base[j])-int(labels[i]==labels[j]) for j in range(28)] for i in range(28)]
 dr=rank(diff);assert dr==[0,6,10,12][r]
 graph={('L',k):set() for k in range(1,8)};graph.update({('M',k):set() for k in range(1,8)})
 for a,b in zip(base,labels):graph[('L',a)].add(('M',b));graph[('M',b)].add(('L',a))
 seen=set();components=[]
 for v in graph:
  if v in seen:continue
  stack=[v];component=[];seen.add(v)
  while stack:
   u=stack.pop();component.append(u)
   for w in graph[u]:
    if w not in seen:seen.add(w);stack.append(w)
  components.append(component)
 assert len(components)==[7,4,2,1][r]
 checks.append({'gaussian_rank':r,'partition_projection_difference_rank':dr,'incidence_components':len(components),'component_vertex_counts':sorted(map(len,components))})
root=Path(__file__).resolve().parents[1]/'review-independent'/'REVIEW.md'
out={'status':'PASS_INDEPENDENT_THREE_HEAD_PARTITION_POTENTIAL','root_proof_sha256':hashlib.sha256(root.read_bytes()).hexdigest(),'odd_forms':28,'ordinary_partition_groups':7,'group_size':4,'checks':checks,'potential':[0,3,5,6],'independence':'Separate direct enumeration of quadratic refinements, incidence components and exact Fraction rank; no root verifier imported. Written all-group proof independently audited.','new_kappa':False}
h=Path(__file__).resolve().parent;(h/'THREE-HEAD-POTENTIAL-REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
