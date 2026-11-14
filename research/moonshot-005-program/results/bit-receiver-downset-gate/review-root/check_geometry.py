#!/usr/bin/env python3
"""Independent shortening, receiver-code and multicast geometry review."""
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
def need(x,s):
 if not x:raise ValueError(s)
def basis(rows):
 b={}
 for r in rows:
  while r:
   p=(r&-r).bit_length()-1
   if p in b:r^=b[p]
   else:b[p]=r;break
 return b
def reduce(r,b):
 for p in sorted(b):
  if r>>p&1:r^=b[p]
 return r
def realrank(rows):
 b={}
 for row in rows:
  row=list(map(F,row))
  for p,r in sorted(b.items()):
   if row[p]:c=row[p];row=[x-c*y for x,y in zip(row,r)]
  p=next((i for i,x in enumerate(row) if x),None)
  if p is not None:c=row[p];b[p]=[x/c for x in row]
 return len(b)
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');q=json.loads(gzip.decompress(raw));v=[[F(x) for x in q['frames'][str(q['start'][i])]['B'][0]] for i in range(111)]
 raw=a.partition.read_bytes();need(hashlib.sha256(raw).hexdigest()=='7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117','partition pin');groups=json.loads(raw)['groups'];need(sorted(sum(groups,[]))==list(range(111)) and len(groups)==15,'partition')
 dot=lambda i,j:sum(x*y for x,y in zip(v[i],v[j]));K=[sum((1<<j) for j in range(111) if i==j or dot(i,j)==0) for i in range(111)];U=[sum(1<<j for j in g) for g in groups];cls={j:c for c,g in enumerate(groups) for j in g};local=[K[i]^(1<<i) for i in range(111)];full=(1<<111)-1;Ub=basis(U);Cb=basis(K);Sb=basis(U+K)
 need([len(Ub),len(Cb),len(Sb)]==[15,9,19],'code ranks');need(all(dot(i,j)==0 for g in groups for i,j in combinations(g,2)),'orthogonal classes')
 L=[K[i]^U[cls[i]] for i in range(111)];cosets=[reduce(K[g[0]],Ub) for g in groups];need(len(set(cosets))==15 and all(cosets),'15 nonzero classes')
 checks=[]
 for i in range(111):
  mask=full^local[i];need(len(basis([x&mask for x in U]))==15,'U receiver invisible')
  need(len(basis([x&mask for x in Sb.values()]))==18,'U+C shortening one')
  need(L[i] and not L[i]&mask and realrank([v[j] for j in range(111) if L[i]>>j&1])==7,'full-facet local generator')
  dims=[]
  for c,g in enumerate(groups):
   W=U+[K[g[0]]];d=16-len(basis([x&mask for x in W]));need(d==int(c==cls[i]),'Wc exact shortening');dims.append(d)
  need(reduce(K[i],Ub)==cosets[cls[i]],'class quotient agreement');checks.append(dims)
 spaces={frozenset({0})}
 for vq in cosets:
  for H in list(spaces):spaces.add(H|frozenset(x^vq for x in H))
 need(len(spaces)==67,'all binary four-space subspaces');hist=Counter()
 for H in spaces:
  h=len(H).bit_length()-1;need(len(H)==1<<h,'subspace dimension');enabled=sum(x in H for x in cosets);need(enabled==2**h-1,'enabled classes');hist[h]+=1
 need(dict(sorted(hist.items()))=={0:1,1:15,2:35,3:15,4:1},'Gaussian counts')
 c0=cls[0];need(groups[c0]==list(range(8)) or set(groups[c0])==set(range(8)),'coordinate class')
 Li=[K[i]^U[c0] for i in range(8)];Hi=[K[i]^(1<<i) for i in range(8)];Wmix=list(basis(K[:8]+Hi).values());need([len(basis(K[:8])),len(basis(Li)),len(basis(Hi)),len(Wmix)]==[4,4,8,12],'mixed history ranks')
 inside=[i for i in range(111) if v[i][0]==v[i][1]==0];mask=sum(1<<i for i in inside);need(len(inside)==28 and (Li[0]&mask)==(Li[1]&mask) and (Li[0]&mask).bit_count()==22,'pair common restriction')
 fit=[];twins={}
 for i in range(111):
  forbidden=full^local[i];ok=reduce(1<<i,basis([w&forbidden for w in Wmix]))==0
  if ok:fit.append(i)
  if i>=8:
   support=tuple(j for j,x in enumerate(v[i]) if x)
   twin=next((j for j in range(8,111) if j!=i and tuple(k for k,x in enumerate(v[j]) if x)==support and dot(i,j)!=0),None)
   need(twin is not None and all(((w>>i)^(w>>twin))&1==0 for w in Wmix),'noncontact twin');twins[str(i)]=twin
 need(fit==list(range(8)) and len(twins)==103,'only coordinate receivers fit')
 masked=[Hi[i]|(1<<(111+i)) for i in range(8)];need(len(basis(masked))==8,'unknown-Y masks remove redundancy')
 for i in range(8):
  Y=Hi[i]|(1<<(111+i));P=K[i];Y^=P;P^=Y
  need(Y==((1<<i)|(1<<(111+i))) and P==masked[i],'exact masked exchange')
 out={'status':'PASS_INDEPENDENT_RECEIVER_AND_CUT_GEOMETRY','code_ranks':{'U':15,'C':9,'U_plus_C':19},'all_Wc_receiver_shortening_dimensions':checks,'subspace_counts':dict(hist),'scalar_h_packet_lower_bounds':{h:16-2**h for h in range(5)},'pair_inside_X':inside,'pair_common_X': [i for i in inside if Li[0]>>i&1],'pure_coordinate_rank':4,'pure_all_eight_cut_excess_per_V':4,'masked_rank':8,'masked_cut_excess':0,'mixed_history_rank':12,'mixed_fitting_receivers':fit,'noncoordinate_noncontact_twins':twins,'negative_controls':['own-class shortening is nonzero; unique projection forbidden there','empty witness directions cannot supply full class projections','discarding unknownY changes actual output','rank12 mixed code cannot fit103 noncoordinate receivers'],'scope':'Exact source premises; universal downset projection and reversible-cut arguments separately reviewed. No physical availability or complete supplier.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'code_ranks':out['code_ranks'],'subspace_counts':out['subspace_counts'],'mixed_fitting_receivers':fit}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','partition','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
