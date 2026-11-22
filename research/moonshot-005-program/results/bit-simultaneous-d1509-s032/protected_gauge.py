"""Constrained simultaneous gauge feasibility for retained H whole fibres."""
from pathlib import Path
import importlib.util, json, gzip
import numpy as np
here=Path(__file__).parent
sp=importlib.util.spec_from_file_location('ex',here/'explore.py');ex=importlib.util.module_from_spec(sp);sp.loader.exec_module(ex)
repo=Path.cwd();g,a,src,ph,dw=ex.load(repo)
ff={int(j):{int(i):np.array(U,dtype=np.uint8)for i,U in rr.items()}for j,rr in ex.read(here/'output/FRAMES.json.gz').items()}
old=repo/'research/moonshot-005-program/results/bit-shared-h-s031-construction/d-aligned-full45-pair/output'
fib=ex.read(old/'FIBRES.json.gz')
def basis(A):
 _,p=g.rref(A,a);return A[:,p]
def null(A):
 R,p=g.rref(A,a);free=[q for q in range(A.shape[1])if q not in p];N=np.zeros((A.shape[1],len(free)),dtype=np.uint8);N[free]=np.eye(len(free),dtype=np.uint8)
 for t,q in enumerate(p):N[q]=R[t,free]
 assert not np.any(a.mm(A,N));return N
Ks={}
for h,rr in fib.items():
 K=np.hstack([np.array(z['kernel'],dtype=np.uint8)[:48,:3]for z in rr.values()]);K=basis(K); Z=np.zeros_like(K);Ks[int(h)]=np.block([[K,Z],[Z,K]])
print('CORES',[(h,a.rank(K))for h,K in Ks.items()],flush=True)
C={}
for j in ff:
 H=[h for h in Ks if j in a.planes[h]]
 C[j]=basis(np.hstack([ff[j][6]]+[Ks[h]for h in H]))
print('CONSTRAINTS',[(j,B.shape[1])for j,B in C.items()],flush=True)
records=[]
for i in sorted(ff[0]):
 if i==6:continue
 blocks=[];vals=[];dims={}
 for j in ff:
  U=ff[j][i];B=C[j];N=null(np.hstack([B,U]));P=N[len(B[0]):];assert a.rank(P)==P.shape[1];blocks.append(P);vals.append(a.mm(U,P));dims[j]=P.shape[1]
 T=np.hstack(blocks);V=np.hstack(vals);rk=a.rank(T);ra=a.rank(np.vstack([T,V]));rec={'receiver':i,'intersections':dims,'parameter_rank':rk,'augmented_rank':ra,'consistent_forced_map':rk==ra}
 if rk==ra:
  _,p=g.rref(T,a);TT=T[:,p];VV=V[:,p];L=a.mm(VV,g.inverse(TT,a))if rk==8 else None
  if L is not None:
   rec['forced_common_frame']=L.tolist();rec['frame_rank']=a.rank(L);rec['gauge_extension_ranks']={j:[a.rank(np.hstack([C[j],L])),a.rank(np.hstack([C[j],ff[j][i]]))]for j in ff};rec['kernel_checks']={j:a.rank(np.vstack([np.hstack([C[j],L]),np.hstack([C[j],ff[j][i]])]))==a.rank(np.hstack([C[j],L])) for j in ff}
 print('CONSTRAINED',i,rk,ra,dims,rec.get('kernel_checks'),flush=True);records.append(rec)
(here/'output/PROTECTED-GAUGE.json').write_text(json.dumps({'core_dimensions':{h:K.shape[1]for h,K in Ks.items()},'constraint_dimensions':{j:K.shape[1]for j,K in C.items()},'records':records},sort_keys=True,indent=2)+'\n')
