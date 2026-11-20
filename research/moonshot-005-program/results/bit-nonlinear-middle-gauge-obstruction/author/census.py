#!/usr/bin/env python3
"""Enumerate native coset-join obstructions of fixed ordinary source/H stars."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from itertools import combinations
import ctypes,importlib.util,json
from pathlib import Path
import numpy as np

def mod(p,name):
 s=importlib.util.spec_from_file_location(name,p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);return v

def req(v,msg):
 if not v:raise ValueError(msg)

class Elim:
 def __init__(self,field,shared):
  self.f=field;self.fn=ctypes.CDLL(str(shared.resolve())).gf_eliminate if shared else None
  if self.fn:
   self.fn.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p]
   self.fn.restype=ctypes.c_int
 def reduce(self,A,inv=False):
  n,w=A.shape;f=self.f
  if self.fn:
   B=np.ascontiguousarray(np.hstack([A,np.eye(n,dtype=np.uint8)])if inv else A.copy())
   rank=self.fn(B.ctypes.data,n,w,B.shape[1],inv,f.MUL.ctypes.data,f.INVERSE.ctypes.data)
   return (rank,B[:,w:]) if inv else rank
  return f.eliminate(A,np.eye(n,dtype=np.uint8)) if inv else f.eliminate(A)[0]

def main():
 p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--library',type=Path)
 for s in ('middle-review','field-review','packing-review'):p.add_argument('--'+s,type=Path)
 p.add_argument('--degree',type=int,default=2,choices=(0,2,3,4));p.add_argument('--save-fibres',type=Path);p.add_argument('--saved-fibres',type=Path);p.add_argument('--limit',type=int)
 a=p.parse_args();root=a.repo/'research/moonshot-005-program/results';r=mod(a.packing_review or root/'bit-spread-overlap-source/review/check.py','packed');f=mod(a.field_review or root/'bit-spread-h263-source/review/check.py','field');middle=mod(a.middle_review or root/'bit-spread-isolated-middle-cut/review/check.py','middle')
 n=middle.NativeLeft(a.repo,r,f,{'components':{'3':{}}},{'frames':[],'gauges':[]},{49:3,97:1,53:1,77:7,93:1,8:1,82:3,58:2,106:1,31:1,105:1})
 elim=Elim(f,a.library);native=set(range(111));donors=sorted(native-{0,10,61,62});selected=set(n.n.marked)
 if a.limit:selected=set(sorted(selected)[:a.limit])
 all_fib=defaultdict(lambda:defaultdict(dict));count=0
 if a.saved_fibres:
  data=np.load(a.saved_fibres);indices=data['indices'];mat=data['matrices'];count=len(mat)//12
  for idx,M in zip(indices,mat):
   d,j,i=map(int,idx)
   if d in selected:all_fib[d][j][i]=M
 else:
  for j in donors:
   source=n.rows(j);stars=[d for d in n.n.marked if j in n.n.D[d]];tables={}
   if not selected.intersection(stars):continue
   for d in stars:
    R=[source[u] for u in n.mid[d] if u in source];req(len(R)==8,'native eight-D-source coordinates');tables[d]=np.stack(R)
   for i in sorted((n.n.adj[j]&native)-{80}):
    seen=sorted(d for d in stars if n.n.D[d]<=n.n.adj[i]);req(len(seen)==12,'actual marked saturated separator')
    if not selected.intersection(seen):continue
    A=np.vstack([tables[d] for d in seen]);rank,X=elim.reduce(A,True);req(rank==96,'complete ordinary marked native cut')
    if count%73==0:req(np.array_equal(f.matmul(A,X),np.eye(96,dtype=np.uint8)),'independent field inverse product')
    for t,d in enumerate(seen):
     if d in selected:all_fib[d][j][i]=X[:,8*t:8*t+8].T.copy()
    count+=1
  if a.save_fibres:
   ids=[];data=[]
   for d in sorted(all_fib):
    for j,h in all_fib[d].items():
     for i,v in h.items():ids.append((d,j,i));data.append(v)
   np.savez(a.save_fibres,indices=np.array(ids,dtype=np.int16),matrices=np.array(data));print('saved',len(data),'physical isolated chart/donor/receiver fibres',flush=True)
 full=[];small=[];degrees=Counter();eligible=0
 for d in sorted(all_fib):
  js=sorted(all_fib[d]);rs=sorted(all_fib[d][js[0]]);req(all(set(all_fib[d][j])==set(rs)for j in js),'common native receiver roster')
  eligible+=1
  def witnessed(S):
   ranks={j:elim.reduce(np.vstack([all_fib[d][j][i]for i in S])) for j in js}
   z=min(ranks,key=ranks.get);w=max(ranks,key=ranks.get)
   if ranks[z]!=ranks[w]:return {'d':d,'receivers':list(S),'donors':[z,w],'ranks':[ranks[z],ranks[w]]}
   return None
  got=witnessed(rs)
  if got:full.append(got)
  hit=False
  for k in range(2,a.degree+1):
   for S in combinations(rs,k):
    found=witnessed(S)
    if found:small.append(found);degrees[k]+=1;hit=True;break
   if hit:break
 out={'examined_marked_D':eligible,'original_native_edge_inversions':count,'all_native_receivers_excluding_80':True,
      'ordinary_donors_excluding':[0,10,61,62],'complete_receiver_set_mismatch_count':len(full),'complete_receiver_set_witnesses':full,
      'max_small_arity_examined':a.degree,'small_witness_histogram':dict(degrees),'minimum_found_by_D':small,
      'new_complete_kappa':False}
 a.out.mkdir(exist_ok=True,parents=True);(a.out/'CENSUS.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(eligible,len(full),degrees)

if __name__=='__main__':main()
