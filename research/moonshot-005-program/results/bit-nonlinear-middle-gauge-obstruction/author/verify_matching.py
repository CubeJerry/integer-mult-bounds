#!/usr/bin/env python3
"""Small standalone native replay of 27 pairwise disjoint nonlinear-gauge conflicts."""
from argparse import ArgumentParser
from collections import Counter
import importlib.util,json
from pathlib import Path
import numpy as np

def mod(p,name):
 s=importlib.util.spec_from_file_location(name,p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);return v

def require(ok,msg):
 if not ok:raise ValueError(msg)

def main():
 p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 for name in ('middle-review','packing-review','field-review'):p.add_argument('--'+name,type=Path)
 a=p.parse_args();root=a.repo/'research/moonshot-005-program/results';loc=Path(__file__).parent
 c=mod(a.middle_review or root/'bit-spread-isolated-middle-cut/review/check.py','middle');r=mod(a.packing_review or root/'bit-spread-overlap-source/review/check.py','packed');f=mod(a.field_review or root/'bit-spread-h263-source/review/check.py','gf');n=c.NativeLeft(a.repo,r,f,{'components':{'3':{}}},{'frames':[],'gauges':[]},{49:3,97:1,53:1,77:7,93:1,8:1,82:3,58:2,106:1,31:1,105:1})
 q=json.loads((loc/'output/ALL-JOINS.json').read_bytes());witness=json.loads((loc/'MATCHING.json').read_bytes());records=[];used=set()
 for e in witness['disjoint_pairs']:
  u,v=e;w=q['all_conflict_edge_witnesses'][f'{u},{v}'];d=w['D'];reqset=w['receivers'];vals=[];require(not {u,v}&used,'disjoint lower-bound pair');used.update((u,v))
  for j in e:
   orig=[]
   for i in reqset:
    ds,A,blocks=n.marked(i,j);target=np.zeros((96,8),dtype=np.uint8);t=ds.index(d);target[8*t:8*t+8]=np.eye(8,dtype=np.uint8)
    k,X=f.eliminate(A,target);require(k==96 and np.array_equal(f.matmul(A,X),target),'exact labelled native cut inverse columns');orig.append(X)
   vals.append(f.eliminate(np.hstack(orig))[0])
  require(vals==w['ranks'] and vals[0]!=vals[1],'native joined partitions genuinely unequal');records.append({'donors':e,'D':d,'receivers':reqset,'field_ranks':vals,'binary_log2_join_block_cardinalities':[48*t for t in vals]})
 cover=set(witness['cover']);require(len(used)==54 and len(cover)==len(records)==27 and all(cover & set(map(int,e.split(','))) for e in q['all_conflict_edge_witnesses']),'matched upper and lower transversal verifiers')
 b={'minimum_affected_left_stars_for_certified_graph':27,'native_disjoint_witnesses':records,'new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'DISJOINT-REPLAY.json').write_text(json.dumps(b,sort_keys=True,indent=2)+'\n');print(27,'disjoint literal rank conflicts on',len(used),'different donors')

if __name__=='__main__':main()
