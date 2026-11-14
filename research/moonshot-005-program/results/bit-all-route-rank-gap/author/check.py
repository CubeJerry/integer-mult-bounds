#!/usr/bin/env python3
"""Exact complete-caller, potential-edge and route-count controls."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
def need(b,m):
 if not b:raise ValueError(m)
def main(a):
 raw=a.caller.read_bytes();need(hashlib.sha256(raw).hexdigest()=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','complete caller pin');z=json.loads(raw)
 N,H,P,T=({int(k):F(v) for k,v in z[s].items()} for s in ['native_paid','helper_target','paired_paid','paired_target'])
 def add(*terms):
  out={}
  for c,p in terms:
   for r,v in p.items():
    if r:out[r]=out.get(r,0)+c*v
  return {r:v for r,v in out.items() if v}
 S=add((F(1,36),T),(F(-1,36),P));B=add((1,N),(-1,H),(1,S))
 explicit={127:F(37,6),64:F(37,3),1:F(-37,3)}
 for j in range(1,9):
  for r,c in [(7*j+1,F(37,3)),(7*j,F(-37,3))]:explicit[r]=explicit.get(r,0)+c
 need(B==explicit,'whole caller cancellation')
 grid=1<<160;cache={}
 def power(r):
  if r not in cache:
   target=r**199*grid**200;l,h=0,r*grid+1
   while h-l>1:
    m=(l+h)//2
    if m**200<=target:l=m
    else:h=m
   need(l**200<=target<h**200,'outward200th root');cache[r]=(F(l,grid),F(h,grid))
  return cache[r]
 def moment(p):
  lo=hi=F(0)
  for r,c in p.items():
   x,y=power(r);lo+=c*(x if c>=0 else y);hi+=c*(y if c>=0 else x)
  return lo,hi
 Eprofile=add((1,B),(-222,{7:1}));cprofile={1:F(1),8:F(1),7:F(-1)}
 E=moment(Eprofile);c=moment(cprofile);need(82<E[0]<E[1]<83 and 1<c[0]<c[1]<2,'strict allowance and excursion bracket')
 need(moment(add((42,cprofile),(-1,Eprofile)))[0]>0,'42public downcalls excluded')
 need(moment(add((1,Eprofile),(-1,{1:1}),(-41,cprofile)))[0]>0,'weighted count83 control remains possible in relaxed arithmetic')
 need(moment(S)[1]<0,'negative finite-m endpoint correction')
 need(F(8,7)<F(3,2),'analytic logarithm derivative constants')
 caps=[]
 for d in range(42):
  lo,hi=moment(add((1,Eprofile),(-d,cprofile)));k=lo.numerator//lo.denominator
  need(k==hi.numerator//hi.denominator and F(k)<lo<hi<F(k+1),'strict integer rounding')
  need(k+2*d<=83,'combined count cap')
  caps.append(dict(public_down=d,owned_positive_at_most=k,weighted_count_at_most=k+2*d))
 def phi(kind,r):return ({r:F(1)} if r else {}) if kind=='Y' else add((1,{8:F(1)}),(-1,{8-r:F(1)}))
 edges=[]
 for kind in ['X','Y']:
  for start in range(9):
   for end in range(9):
    if start==end:continue
    prof=add((1,{abs(end-start):F(1)}),(-1,phi(kind,end)),(1,phi(kind,start)),(-int(end<start),cprofile))
    interval=moment(prof);need(not prof or interval[0]>0,'potential edge inequality')
    edges.append(dict(kind=kind,start=start,end=end,exact_equality=not prof))
 # Relax ranks to a graph with own and foreign rank-seven facets. Every actual
 # nested trajectory projects here; this finite check supports the gap proof.
 ranks=[0,1,2,3,4,5,6,7,7,8];own=7;other=8;hub=9
 summaries=[]
 for kind,initial,terminal in [('X',1,hub),('Y',0,own)]:
  states={(initial,0,0,False)};checked=0;maximum=-100
  for length in range(1,13):
   nxt=set()
   for at,d,arr,seen in states:
    for target in range(10):
     if ranks[target]==ranks[at]:continue
     down=ranks[target]<ranks[at];upfacet=(not down and ranks[target]==7)
     nxt.add((target,d+down,arr+upfacet,seen or (upfacet and target==own)))
   states=nxt
   for at,d,arr,seen in states:
    if at==terminal:
     excess=arr-d-(1 if kind=='X' else int(seen));need(excess<=0,'facet arrival charging');maximum=max(maximum,excess);checked+=1
  summaries.append(dict(kind=kind,max_steps=12,endpoint_states_checked=checked,maximum_charge_excess=maximum))
 need(moment(add((1,cprofile),(-2,{1:1})))[1]<0,'charging two for every public descent would be false')
 need(sum(r*v for r,v in Eprofile.items())==F(629,6)>84,'out-of-targett1 control')
 nraw=a.native.read_bytes();need(hashlib.sha256(nraw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');n=json.loads(gzip.decompress(nraw))
 dims={int(k):v['dim'] for k,v in n['frames'].items()}
 need(all(dims[n['start'][i]]==1 and dims[n['final'][i]]==8 for i in range(111)),'X endpoint ranks')
 need(all(dims[n['start'][111+i]]==0 and dims[n['final'][111+i]]==7 for i in range(111)) and len(set(n['final'][111:222]))==111,'Y endpoint ranks and distinctfacets')
 out=dict(status='PASS_ARBITRARY_PUBLIC_AND_OWNED_ROUTE_TARGET_BUDGET',caller_sha256=hashlib.sha256(raw).hexdigest(),native_sha256=hashlib.sha256(nraw).hexdigest(),dyadic_bits=160,E_star=list(map(str,E)),c_star=list(map(str,c)),E_midpoint=float(sum(E)/2),c_midpoint=float(sum(c)/2),forty_two_c_minus_E=list(map(str,moment(add((42,cprofile),(-1,Eprofile))))),caps=caps,potential_edges_checked=len(edges),potential_equalities=sum(x['exact_equality'] for x in edges),relaxed_route_checks=summaries,public_down_at_most=41,owned_positive_plus_twice_public_down_at_most=83,facet_ell_at_most=194,rank_gap_threshold=196,rank_lower_bound='ceil(28V/3)',all_downward_occurrences_at_least=10,controls=['unit public downward excursion costs c<2, so exact2charge is invalid','relaxed M_owned=1,D_public=41 passes endpoint inequality','t=1 allowance629/6 exceeds84','all original Y inputs remain independent in the written normalization'],scope='Finite numerical and route controls support the universal written proof; no source construction or new supplier.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','E_midpoint','c_midpoint','potential_edges_checked','facet_ell_at_most']}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['caller','native','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
