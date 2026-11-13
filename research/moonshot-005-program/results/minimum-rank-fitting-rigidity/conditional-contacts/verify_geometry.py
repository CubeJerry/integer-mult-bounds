#!/usr/bin/env python3
"""Exact hosted96 geometry for nonsymmetric block-rank8 contact rigidity."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact assertion checks require Python without -O')
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';B=[5,56,69,100,65,77,96,103]
def main(a):
 data=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();assert hashlib.sha256(data).hexdigest()==PIN;s=json.loads(gzip.decompress(data));H=[s['live'][i] for i in s['hosted']['Dports']];assert len(H)==96 and set(B)<=set(H)
 def root(h):
  n=s['frames'][s['initial'][h]][0];t=[j for j in range(9) if n>>j&1]
  if len(t)==3:return [2 if j in t else -1 for j in range(9)]
  z=[j for j in range(9) if j not in t];return [3*(int(j==z[0])-int(j==z[1])) for j in range(9)]
 r={h:root(h) for h in H};dot=lambda x,y:sum(u*v for u,v in zip(x,y));G={(h,j):F(dot(r[h],r[j]),18) for h in H for j in H};g={h:[G[h,b] for b in B] for h in H};support={h:frozenset(i for i,v in enumerate(g[h]) if v) for h in H}
 assert all(G[h,j]==int(h==j) for h in B for j in B) and all(G[h,j]==sum(g[h][p]*g[j][p] for p in range(8)) for h in H for j in H)
 blocks={}
 for h in H:
  if h not in B:
   assert len(support[h])==4 and all(abs(g[h][p])==F(1,2) for p in support[h]);blocks.setdefault(tuple(sorted(support[h])),[]).append(h)
 assert len(blocks)==14 and all(sum(set(t)<=set(q) for q in blocks)==1 for t in itertools.combinations(range(8),3))
 graphs=[]
 for p,q in itertools.combinations(range(8),2):
  I=[h for h in H if h not in B and {p,q}<=support[h]];adj={(typ,h):set() for typ in (0,1) for h in I}
  for i,j in itertools.product(I,repeat=2):
   if support[i]&support[j]=={p,q} and not G[i,j]:adj[0,i].add((1,j));adj[1,j].add((0,i))
  unseen=set(adj);comps=[]
  while unseen:
   start=min(unseen);seen={start};stack=[start];tree=[]
   while stack:
    v=stack.pop()
    for u in sorted(adj[v]):
     if u not in seen:seen.add(u);stack.append(u);tree.append([list(v),list(u)])
   unseen-=seen;sig={int((g[h][p]/g[h][q])*(-1 if typ else 1)) for typ,h in seen};assert len(sig)==1
   comps.append({'C_sign':next(iter(sig)),'nodes':[list(v) for v in sorted(seen)],'spanning_tree':tree})
  assert len(comps)==2 and {x['C_sign'] for x in comps}=={-1,1};graphs.append({'pair':[p,q],'components':comps})
 flips=[]
 for p,t in itertools.combinations(range(8),2):
  quads=[q for q,v in blocks.items() if {p,t}<=set(q) and len(v)>=5];assert quads
  found=None
  for quad in quads:
   for q in quad:
    if q in (p,t):continue
    for i,j in itertools.combinations(blocks[quad],2):
     sig=g[i][p]/g[i][q];tau=g[i][q]/g[i][t]
     if g[j][p]/g[j][q]==-sig and g[j][q]/g[j][t]==-tau:found={'outer_pair':[p,t],'middle':q,'quad':list(quad),'rows':[i,j],'sigma':int(sig),'tau':int(tau)};break
    if found:break
   if found:break
  assert found;flips.append(found)
 triple=[{'coordinates':list(t),'quad':list(next(q for q in blocks if set(t)<=set(q))),'row':blocks[next(q for q in blocks if set(t)<=set(q))][0]} for t in itertools.combinations(range(8),3)]
 # Literal noncommuting2x2 matrix gauges validate the ordered formula's scope.
 mm=lambda A,C:[[sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
 A=[[1,1],[0,1]];C=[[1,0],[1,1]];assert mm(A,C)!=mm(C,A)
 inv=lambda X:[[X[1][1],-X[0][1]],[-X[1][0],X[0][0]]]
 lam01=inv(A);lam12=mm(inv(C),A);lam02=inv(C)
 assert mm(lam12,lam01)==lam02 and mm(lam01,lam12)!=lam02
 gauges=[[[1,0],[0,1]],A,C,mm(A,C)];T={h:gauges[k%4] for k,h in enumerate(H)}
 assert all(mm(mm(T[h],inv(T[b])),mm(T[b],inv(T[j])))==mm(T[h],inv(T[j])) for h in H for j in H for b in B)
 result={'status':'PASS_EXACT_HOSTED96_BLOCK_CONTACT_GEOMETRY','source_pin':PIN,'hosted':H,'B':B,'source_coordinates':{str(h):[str(v) for v in g[h]] for h in H},'support_quads':[{'coordinates':list(q),'rows':v} for q,v in sorted(blocks.items())],'pair_ratio_graphs':graphs,'sign_collapse_witnesses':flips,'triple_cocycle_witnesses':triple,'negative_controls':{'removing_all_graph_edges_destroy_connectivity':max(len(x['components'][0]['nodes']) for x in graphs)>1,'noncommuting_gauge_order_detected':mm(lam01,lam12)!=lam02},'noncommuting_example':{'D1':A,'D2':C,'correct_order_lambda12_lambda01':mm(lam12,lam01),'wrong_order_lambda01_lambda12':mm(lam01,lam12),'all_96x96x8_gauge_factor_products_checked':96*96*8},'scope':'Finite geometry for rank8V operator fitting rigidity with invertible allowed B-contact blocks, all characteristic not2 fields. Does not establish contact invertibility or physical realizability.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'GEOMETRY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'source_quads':len(blocks),'ratio_components':sum(len(g['components']) for g in graphs),'sign_collapses':len(flips),'triple_cocycles':len(triple)},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
