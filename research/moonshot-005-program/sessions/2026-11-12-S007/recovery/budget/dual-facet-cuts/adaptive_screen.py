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
from scipy.sparse import coo_matrix,csr_matrix,hstack,eye
from scipy.sparse.csgraph import maximum_flow,breadth_first_order
DEN=1000000;INF=1000000000
nf=len(F);pairs=[];cost=[]
for i,u in enumerate(F):
 for j,v in enumerate(F):
  if dim[j]>dim[i] and u<v:pairs.append((i,j));cost.append((dim[j]-dim[i])**.995)
pa=np.asarray(pairs,dtype=np.int32);cost=np.asarray(cost)
Bi=[];Bj=[]
for c,mm in enumerate(masks):
 for k,z0 in enumerate(mm):
  z=z0
  while z:
   bit=z&-z;z^=bit;Bi.append(c);Bj.append(9*(bit.bit_length()-1)+k)
B=coo_matrix((np.ones(len(Bi)),(Bi,Bj)),shape=(nf,m*9)).tocsr();delta=deficits.ravel().astype(float);cutmeta=[{'frame':j,'layer':k+1} for j in range(m) for k in range(9)];seen={bytes(B[:,j].toarray().astype(np.uint8).ravel()) for j in range(B.shape[1])};del Bi,Bj
own=Counter()
for e in w['program']:
 if e[0]=='MOVE' and e[4] and len(w['frames'][e[2]])<len(w['frames'][e[3]]):own[(old[e[2]],old[e[3]])]+=1
si=nf;ti=nf+1;baseline_i=[int(b) for a,b in pairs]+[a for a,b in own];baseline_j=[int(a) for a,b in pairs]+[b for a,b in own];baseline_v=[INF]*len(pairs)+[DEN*v for v in own.values()];history=[]
for iteration in range(12):
 nc=B.shape[1];eq=hstack([-B,eye(nf)],format='csr');ri=np.repeat(np.arange(len(pairs)),2);rj=(pa+nc).ravel();rv=np.tile([-1.,1.],len(pairs));ub=coo_matrix((rv,(ri,rj)),shape=(len(pairs),nc+nf)).tocsr();obj=np.concatenate([-delta,np.zeros(nf)])
 t0=time.time();r=linprog(obj,A_ub=ub,b_ub=cost,A_eq=eq,b_eq=np.zeros(nf),bounds=[(0,None)]*(nc+nf),method='highs')
 if not r.success:raise ValueError(r.message)
 cover=np.maximum(0.,-r.ineqlin.marginals);positive=np.flatnonzero(cover>1e-10);zcover=np.ceil(cover[positive]*DEN).astype(np.int64);print('iteration',iteration,'cuts',nc,'LP',-r.fun,'cover edges',len(positive),'LP seconds',time.time()-t0,flush=True)
 ei=baseline_i+[int(pa[j,0]) for j in positive];ej=baseline_j+[int(pa[j,1]) for j in positive];ev=baseline_v+zcover.tolist();extra=[];extrad=[];minval=16*DEN;violations=0
 for j,c in enumerate(cl):
  oi=ei+[si]*8+[old[w['initial'][w['live'][v]]] for v in c];oj=ej+[old[w['final'][w['live'][v]+112]] for v in c]+[ti]*8;ov=ev+[INF]*16
  graph=coo_matrix((np.asarray(ov,dtype=np.int64),(oi,oj)),shape=(nf+2,nf+2)).tocsr();flow=maximum_flow(graph,si,ti);minval=min(minval,int(flow.flow_value))
  if flow.flow_value>=16*DEN:continue
  violations+=1;res=graph-flow.flow;res.eliminate_zeros();reached=breadth_first_order(res,si,directed=True,return_predecessors=False);inside=np.ones(nf+2,dtype=np.uint8);inside[reached]=0;inside=inside[:nf];key=bytes(inside)
  if key in seen:continue
  if any(inside[a] and not inside[b] for a,b in pairs):raise ValueError('non-upward mincut')
  owned=sum(n for (a,b),n in own.items() if not inside[a] and inside[b]);d=16-owned
  if not 0<d<=8:raise ValueError(('unexpected deficit',d))
  seen.add(key);extra.append(inside);extrad.append(d);cutmeta.append({'frame':j,'layer':None,'owned_inward':owned,'inside_charts':[i for i,v in enumerate(inside) if v]})
 rec={'iteration':iteration,'cuts':nc,'objective':-r.fun,'cover_edges':len(positive),'minimum_capacity':minval/DEN,'violated_frames':violations,'new_cuts':len(extra),'seconds':time.time()-t0};history.append(rec);print('separation',rec,flush=True)
 out={'history':history,'last_cover':[{'from_frame':basis[int(pa[j,0])],'to_frame':basis[int(pa[j,1])],'rank':dim[int(pa[j,1])]-dim[int(pa[j,0])],'multiplicity':float(cover[j])} for j in positive],'last_weight_support':[{'cut':cutmeta[j],'weight':float(x)} for j,x in enumerate(r.x[:nc]) if x>1e-9],'cut_meta':cutmeta,'source_chart_frames':basis,'complete_separation':not violations,'scope':'Optimistic paid-edge candidate set is native charts plus line511/H511. Separation includes every upward source-chart cut between D_min and D_max for every hosted8 frame. A successful primal cover upper-bounds all such cut weights even for arbitrary new-chart cuts; dual feasibility over all new paid binary-chart edges is not asserted.'}
 (H/'ADAPTIVE-SCREEN.json').write_text(json.dumps(out,indent=2)+'\n')
 if not extra:break
 B=hstack([B,csr_matrix(np.asarray(extra,dtype=float).T)],format='csr');delta=np.concatenate([delta,np.asarray(extrad,dtype=float)])
