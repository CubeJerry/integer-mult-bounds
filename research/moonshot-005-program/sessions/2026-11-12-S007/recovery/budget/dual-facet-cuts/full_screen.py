import json,gzip,time
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.optimize import linprog
H=Path(__file__).resolve().parent;ROOT=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds')
w=json.loads(gzip.decompress((ROOT/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()));cl=json.loads((H/'FRAMES.json').read_text())['eight_or_larger_cliques'];m=len(cl);ALL=(1<<m)-1;PB=[0]*len(w['ports'])
for j,c in enumerate(cl):
 for i in c:PB[i]|=1<<j

def span(b):
 s={0}
 for v in b:s.update(x^v for x in tuple(s))
 return frozenset(s)
F=list(map(span,w['frames']));basis=list(w['frames'])
for b in ([511],[257,258,260,264,272,288,320,384]):
 f=span(b)
 if f not in F:F.append(f);basis.append(b)
uniq={f:b for f,b in zip(F,basis)};F=list(uniq);basis=list(uniq.values());dim=[len(b) for b in basis];index={f:i for i,f in enumerate(F)};old=[index[span(b)] for b in w['frames']];masks=[]
for f,b,d in zip(F,basis,dim):
 a=0;z=0
 for i,v in enumerate(w['ports']):
  if v in f:a|=PB[i]
  if all((v&x).bit_count()%2==0 for x in b):z|=PB[i]
 if a&z:raise ValueError('frame intersects both orthogonal subspaces')
 masks.append([a|(ALL^z if d>=k else 0) for k in range(1,10)])
for j,c in enumerate(cl):
 for i,v in enumerate(w['ports']):
  if all((v&w['ports'][a]).bit_count()%2 for a in c)!=(i in c):raise ValueError('external active common odd neighbour')
inward=np.zeros((m,9),dtype=np.int32)
for e in w['program']:
 if e[0]!='MOVE' or not e[4]:continue
 a,b=old[e[2]],old[e[3]]
 for k in range(9):
  z=masks[b][k]&~masks[a][k]
  while z:
   bit=z&-z;z^=bit;inward[bit.bit_length()-1,k]+=1
deficits=16-inward
print('owned inward histogram',dict(Counter(map(int,inward.ravel()))),'deficit totals',deficits.sum(axis=0).tolist(),flush=True)
from scipy.sparse import coo_matrix,csr_matrix
start=time.time();nc=m*9;nf=len(F);ei=[];ej=[];ev=[]
for c,mm in enumerate(masks):
 for k,z0 in enumerate(mm):
  z=z0
  while z:
   bit=z&-z;z^=bit;ei.append(c);ej.append(9*(bit.bit_length()-1)+k);ev.append(-1.)
 ei.append(c);ej.append(nc+c);ev.append(1.)
eq=coo_matrix((ev,(ei,ej)),shape=(nf,nc+nf)).tocsr();del ei,ej,ev
pairs=[];cost=[]
for i,u in enumerate(F):
 for j,v in enumerate(F):
  if dim[j]>dim[i] and u<v:pairs.append((i,j));cost.append((dim[j]-dim[i])**.995)
ri=np.repeat(np.arange(len(pairs)),2);rj=np.asarray([[nc+a,nc+b] for a,b in pairs]).ravel();rv=np.tile([-1.,1.],len(pairs));ub=coo_matrix((rv,(ri,rj)),shape=(len(pairs),nc+nf)).tocsr()
obj=np.concatenate([-deficits.ravel(),np.zeros(nf)])
print('LP matrices',eq.shape,eq.nnz,ub.shape,ub.nnz,'start',flush=True)
r=linprog(obj,A_ub=ub,b_ub=cost,A_eq=eq,b_eq=np.zeros(nf),bounds=[(0,None)]*(nc+nf),method='highs')
print('LP',r.message,'objective',-r.fun,'seconds',time.time()-start,flush=True)
weights=r.x[:nc].reshape(m,9);support=[]
for j in range(m):
 if max(weights[j])>1e-10:support.append({'frame_index':j,'ports':cl[j],'weights':weights[j].tolist()})
active=[]
for i in np.flatnonzero(r.ineqlin.marginals< -1e-9):
 a,b=pairs[int(i)];active.append({'from_frame':basis[a],'to_frame':basis[b],'rank':dim[b]-dim[a],'cover_multiplicity':float(-r.ineqlin.marginals[i])})
out={'source_only_optimistic_objective':-r.fun,'support':support,'dual_edge_cover':active,'source_chart_count':nf,'inequalities':len(pairs),'equalities':nf,'scope':'Optimistic LP over native chart subspaces plus line511 and H511. Upper bound on the strength of this cut family under unrestricted new-chart normalization; no universal feasibility claim.'}
(H/'FULL-SCREEN.json').write_text(json.dumps(out,indent=2)+'\n');print('supported frames',len(support),'dual edges',len(active),flush=True)
