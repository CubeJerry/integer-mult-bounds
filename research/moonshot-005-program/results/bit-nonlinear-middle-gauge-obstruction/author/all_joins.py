#!/usr/bin/env python3
"""Exhaust rolewise partition-join invariants for every ordinary native marked cut."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
from itertools import combinations
import ctypes,importlib.util,json
from pathlib import Path
import numpy as np

def mod(p,name):
 spec=importlib.util.spec_from_file_location(name,p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);return v

def require(v,msg):
 if not v:raise ValueError(msg)

def support(x):
 return sum((1<<i) for i,block in enumerate(x.reshape(-1,8)) if block.any())

def nullities(M,r,field,elim,number):
 # Relations: columns of L are exact vectors on the labelled eight-field parts.
 defect=8*number-elim.reduce(M)
 if defect==0:return np.zeros(1<<number,dtype=np.uint8),0,{}
 L=r.nullspace(M.T,field).T;require(len(L)==defect,'computed full relation space')
 if defect>2:
  out=[]
  for S in range(1<<number):
   outside=[8*i+t for i in range(number) for t in range(8) if not(S>>i&1)]
   out.append(defect-elim.reduce(L[:,outside]) if outside else defect)
  return np.array(out,dtype=np.uint8),defect,{}
 forms=[L[0]] if defect==1 else [L[1]]+[L[0]^field.MUL[t,L[1]] for t in range(64)]
 hist=Counter(support(x) for x in forms);require(0 not in hist,'nonzero projective relation')
 z=np.zeros(1<<number,dtype=np.int16)
 for mask,count in hist.items():z[mask]=count
 # Subset zeta transform counts projective lines supported within S.
 for t in range(number):
  paired=z.reshape(-1,2,1<<t);paired[:,1]+=paired[:,0]
 require(set(map(int,z))<={0,1,65},'number of lines in a dimension <=2 subspace over GF64')
 return np.where(z==65,2,z).astype(np.uint8),defect,hist

def main():
 p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--fibres',type=Path,required=True);p.add_argument('--library',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--packing-review',type=Path);p.add_argument('--field-review',type=Path);a=p.parse_args()
 base=a.repo/'research/moonshot-005-program/results';r=mod(a.packing_review or base/'bit-spread-overlap-source/review/check.py','packing');f=mod(a.field_review or base/'bit-spread-h263-source/review/check.py','gf');c=mod(Path(__file__).with_name('census.py'),'census');elim=c.Elim(f,a.library)
 cached=np.load(a.fibres);loc=cached['indices'];mat=cached['matrices'];require(mat.shape==(len(loc),8,96),'true cached isolated fields')
 H=defaultdict(lambda:defaultdict(dict));sha=sha256()
 for row,val in zip(loc,mat):
  d,j,i=map(int,row);H[d][j][i]=val;sha.update(row.astype('>i2').tobytes());sha.update(val.tobytes())
 require(len(loc)==74088 and sha.hexdigest()=='c87f3ff6cd51c57af1fe3dd1a444f864631bd146363a92aad17409afe3acb47f','entire native fibre inventory')
 n=r.Native(a.repo,f);ordinary=set(range(111))-{0,10,61,62};ncuts=0;full_def=Counter();join_h=Counter();witnesses=[];proofedge={};deficient_donors=Counter();all_dims=Counter();native={}
 for d,block in sorted(H.items()):
  js=sorted(block);R=sorted(block[js[0]]);m=len(R)
  require(set(js)==n.D[d]&ordinary and set(R)=={i for i in range(111) if i!=80 and n.D[d]<=n.adj[i]},'all permitted donor and receiver labels')
  columns=[];explain={};active=False
  for j in js:
   require(sorted(block[j])==R,'complete common receiver set')
   M=np.vstack([block[j][i] for i in R]);ds,nu,h=nullities(M,r,f,elim,m);columns.append(ds);full_def[nu]+=1
   if nu:explain[j]={'deficiency':nu,'nonzero_relation_supports':dict(h)};active=True;deficient_donors[j]+=1
  ncuts+=2**m-1
  if not active:continue
  matj=np.vstack(columns);bad=np.flatnonzero(matj.max(axis=0)>matj.min(axis=0)); native[d]={'receivers':R,'donors':js,'deficient_original_donors':explain,'obstructed_receiver_subsets':len(bad)}
  for ss in bad:
   S=int(ss);coords=[R[t]for t in range(m)if S>>t&1];num=len(coords);join_h[num]+=1;defs=matj[:,S];ix0=int(defs.argmax());ix1=int(defs.argmin());w={'D':d,'receivers':coords,'donors':[js[ix0],js[ix1]],'ranks':[8*num-int(defs[ix0]),8*num-int(defs[ix1])]};witnesses.append(w)
   for u,v in combinations(range(len(js)),2):
    if defs[u]!=defs[v]:
     pair=(js[u],js[v]);proofedge.setdefault(pair,{'D':d,'receivers':coords,'ranks':[8*num-int(defs[u]),8*num-int(defs[v])]})
  vals,counts=np.unique(matj[:,-1],return_counts=True);all_dims[m]+=1
 certificate=json.loads(Path(__file__).with_name('MATCHING.json').read_bytes())
 matching=[tuple(v) for v in certificate['disjoint_pairs']];witness=certificate['cover'];edges=set(proofedge)
 require(all(e in edges for e in matching) and len({j for e in matching for j in e})==2*len(matching),'actual disjoint obstructed donor pairs')
 require(len(set(witness))==len(matching) and all(set(e)&set(witness) for e in edges),'matching and cover prove the exact transversal')
 bound=len(matching)
 out={'native_true_fibres':len(loc),'field_fibre_digest':sha.hexdigest(),'all_marked_D':len(H),'examined_nonempty_labelled_receiver_subsets':ncuts,'full_family_deficiency_histogram':dict(full_def),'deficient_donor_stars':dict(deficient_donors),'obstructed_receiver_subsets_by_cardinality':dict(join_h),'number_of_conflicting_D':len({w['D']for w in witnesses}),'conflict_graph_edges':len(edges),'certified_disjoint_conflicts':len(matching),'minimum_number_of_ordinary_left_stars_needing_changes':bound,'witness_affected_native_donor_set':sorted(witness),'disjoint_witnesses':[{'donors':list(e),**proofedge[e]}for e in matching],'all_conflict_edge_witnesses':{f'{u},{v}':z for(u,v),z in sorted(proofedge.items())},'per_D_with_relations':native,'all_obstructed_joins':witnesses,'new_complete_kappa':False}
 a.out.mkdir(exist_ok=True,parents=True);(a.out/'ALL-JOINS.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(len(H),ncuts,len(witnesses),join_h,len(edges),len(matching),bound,flush=True)

if __name__=='__main__':main()
