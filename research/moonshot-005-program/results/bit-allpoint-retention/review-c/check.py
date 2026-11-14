#!/usr/bin/env python3
"""Independent all-clique receiver-union cut reduction; no author imports."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PPIN='8c11ca368995bc6a77f8d0425ac259384a7edf6164bc4254dfc0c7d780e26e19'

def need(ok,s):
 if not ok:raise ValueError(s)

def basis(rows):
 b={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 return list(b.values())

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--pivots',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.native.read_bytes();pr=a.pivots.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native bytes');need(hashlib.sha256(pr).hexdigest()==PPIN,'pivot assignment')
 n=json.loads(gzip.decompress(raw));roots=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 dot=lambda x,y:sum(a*b for a,b in zip(x,y))
 K=[sum(int(i==j or dot(x,y)==0)<<j for j,y in enumerate(roots)) for i,x in enumerate(roots)]
 groups={}
 for i,r in enumerate(roots):
  support=tuple(j for j,x in enumerate(r) if x);sign=1 if r[support[0]]>0 else-1
  groups.setdefault((support,sum(x*sign<0 for x in r)%2),[]).append(i)
 groups=list(groups.values());piv=list(range(8))+json.loads(pr)['pivots'];need(all(p in g for p,g in zip(piv,groups)),'own-group pivots')
 masks=[sum(1<<j for j in g) for g in groups];rows=[]
 for row in K:
  for m,j in zip(masks,piv):
   if row>>j&1:row^=m
  rows.append(row)
 E=basis(rows);need(len(E)==3,'independently reconstructed core')
 allmask=(1<<111)-1;adj=[allmask^r for r in K];closed=[m|(1<<i) for i,m in enumerate(adj)]
 hist=Counter();dhist=Counter();tested=0;best=-1;witness=None
 def visit(chosen,mask,candidates,unknown):
  nonlocal tested,best,witness
  k=len(chosen)
  if k:
   hist[k]+=1
   if k>=7:
    tested+=1;rall=len(basis([e&unknown for e in E]));noise=unknown&~mask;rnoise=len(basis([e&noise for e in E]));d=k+rnoise-rall;dhist[d]+=1
    need(d<=6,'all exact receiver-clique deficits at most6')
    if d>best:best=d;witness={'targets':chosen,'unknown_inputs':[j for j in range(111) if unknown>>j&1],
                            'nuisance_inputs':[j for j in range(111) if noise>>j&1],'core_unknown_rank':rall,'core_nuisance_rank':rnoise,'deficit':d}
  while candidates:
   bit=candidates&-candidates;candidates^=bit;i=bit.bit_length()-1
   visit(chosen+[i],mask|bit,candidates&adj[i],unknown&closed[i])
 visit([],0,allmask,allmask)
 need(max(hist)==8 and best==6,'exact maximum attained')
 need(sum(hist.values())==485330 and tested==62003,'complete all111-port census')
 witness_mask=sum(1<<j for j in witness['targets'])
 naive=len(witness['targets'])-len(basis([e&witness_mask for e in E]))
 need(naive<witness['deficit'],'outside target nuisance changes the actual cut')
 frame=witness['unknown_inputs'];frame_mask=sum(1<<j for j in frame)
 need(len(frame)==8 and all(adj[i]>>j&1 for i in frame for j in frame if i!=j),'eight-frame control')
 one_core=8-len(basis([E[0]&frame_mask]));need(one_core>=7,'one pure core mode does not pass the bound')
 out={'status':'PASS_INDEPENDENT_ALL_RECEIVER_UNION_CUT_REDUCTION','native_sha256':PIN,'pivot_assignment_sha256':PPIN,
      'author_code_imported':False,'core_basis_hex':[hex(e) for e in E],
      'nonempty_clique_count':sum(hist.values()),'cliques_by_size':dict(sorted(hist.items())),'nontrivial_rank_cases':tested,
      'deficits_by_size7_or8_clique':dict(sorted(dhist.items())),'maximum_deficit':best,'witness':witness,
      'negative_controls':{'ignoring_nuisance_would_underestimate':{'naive':naive,'actual':witness['deficit']},
                           'only_one_pure_core_mode':{'frame':frame,'deficit':one_core},'no_pure_core_mode_deficit':8},
      'scope':'all original input copies at their actual lines, pure core atground; necessary cut test only','new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cliques':sum(hist.values()),'nontrivial':tested,'maximum_deficit':best}))

if __name__=='__main__':main()
