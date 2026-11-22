"""Constrained common whole-fibre gauges; experimental solver."""
from pathlib import Path
import importlib.util,json,gzip,itertools,hashlib,argparse
import numpy as np
here=Path(__file__).parent
spec=importlib.util.spec_from_file_location('s032_explore',here/'explore.py')
ex=importlib.util.module_from_spec(spec);spec.loader.exec_module(ex)

def basis(A,g,a):
 _,p=g.rref(A,a);return A[:,p]
def null(A,g,a):
 R,p=g.rref(A,a);free=[q for q in range(A.shape[1])if q not in p]
 N=np.zeros((A.shape[1],len(free)),dtype=np.uint8);N[free]=np.eye(len(free),dtype=np.uint8)
 for t,q in enumerate(p):N[q]=R[t,free]
 assert not np.any(a.mm(A,N));return N

def common_data(repo):
 g,a,src,ph,dw=ex.load(repo)
 ff={int(j):{int(i):np.array(U,dtype=np.uint8)for i,U in rr.items()}for j,rr in ex.read(here/'output/FRAMES.json.gz').items()}
 fib=ex.read(repo/'research/moonshot-005-program/results/bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');Ks={}
 for h,rr in fib.items():
  K=basis(np.hstack([np.array(z['kernel'],dtype=np.uint8)[:48,:3]for z in rr.values()]),g,a)
  Z=np.zeros_like(K);Ks[int(h)]=np.block([[K,Z],[Z,K]])
 C={j:basis(np.hstack([ff[j][6]]+[Ks[h]for h in Ks if j in a.planes[h]]),g,a)for j in ff}
 return g,a,ff,Ks,C

def attempt(R,g,a,ff,C,seed_count=20):
 js=sorted(ff);Us={j:np.hstack([ff[j][i]for i in R])for j in js}
 ranks={j:a.rank(U)for j,U in Us.items()};r=ranks[js[0]]
 if len(set(ranks.values()))>1:return None,{'R':R,'status':'unequal_joint_ranks','ranks':ranks}
 if any(a.rank(np.vstack([Us[js[0]],U]))!=r for U in Us.values()):return None,{'R':R,'status':'unequal_joint_kernels','ranks':ranks}
 Fs=[];Vs=[]
 for j in js:
  N=null(np.hstack([C[j],Us[j]]),g,a);P=N[C[j].shape[1]:]
  Fs.append(P);Vs.append(a.mm(Us[j],P))
 F=np.hstack(Fs);V=np.hstack(Vs);fr=a.rank(F);aug=a.rank(np.vstack([F,V]))
 info={'R':R,'joint_rank':r,'parameter_dimension':8*len(R),'constraint_rank':fr,'constraint_augmented_rank':aug}
 if fr!=aug:return None,dict(info,status='inconsistent_fixed_H_values')
 _,p=g.rref(F,a);Fb=F[:,p];Vb=V[:,p]
 FB=basis(np.hstack([Fb,np.eye(F.shape[0],dtype=np.uint8)]),g,a);Finv=g.inverse(FB,a)
 for seed in range(seed_count):
  random=np.frombuffer(hashlib.shake_256(('S032-fixed-H/'+','.join(map(str,R))+'/'+str(seed)).encode()).digest(96*(FB.shape[1]-fr)),dtype=np.uint8).reshape(96,-1)&63
  L=a.mm(np.hstack([Vb,random]),Finv);ok=True
  for j in js:
   A=np.hstack([C[j],L]);B=np.hstack([C[j],Us[j]])
   if a.rank(A)!=a.rank(B) or a.rank(np.vstack([A,B]))!=a.rank(A):ok=False;break
  if ok:
   G={}
   for j in js:
    A=np.hstack([C[j],L]);B=np.hstack([C[j],Us[j]]);_,pp=g.rref(A,a)
    Ab=A[:,pp];Bb=B[:,pp]
    Ac=basis(np.hstack([Ab,np.eye(96,dtype=np.uint8)]),g,a)
    Bc=basis(np.hstack([Bb,np.eye(96,dtype=np.uint8)]),g,a)
    Gj=a.mm(Bc,g.inverse(Ac,a))
    assert a.rank(Gj)==96 and np.array_equal(a.mm(Gj,A),B);G[j]=Gj
   return {'receivers':R,'common_frames':L,'gauges':G},dict(info,status='constructible_fixed_H_gauges',seed=seed)
 return None,dict(info,status='no_generic_completion_found')

def main(repo,out,search):
 g,a,ff,Ks,C=common_data(repo);records=[];best=None
 if not search:sets=[[6,9],[6,9,48],[6,9,48,52],[6,9,48,52,54]]
 else:
  census=json.loads((here/'output/CENSUS.json').read_text())
  sets=sorted(r for r in census['joint'][3]['joint_kernel_equal_sets']if 6 in r and all(i<111 for i in r))
 for R in sets:
  sol,info=attempt(R,g,a,ff,C);records.append(info);print(json.dumps(info),flush=True)
  if sol is not None and(best is None or len(R)>len(best['receivers'])):best=sol
  if search and sol is not None and len(R)>=4:break
 out.mkdir(parents=True,exist_ok=True)
 (out/'CONSTRAINED-SEARCH.json').write_text(json.dumps(records,sort_keys=True,indent=2)+'\n')
 if best:
  result={'receivers':best['receivers'],'common_frames':best['common_frames'].tolist(),'gauges':{j:G.tolist()for j,G in best['gauges'].items()},'retained_cores':{h:K.tolist()for h,K in Ks.items()},'fixed_subspaces':{j:B.tolist()for j,B in C.items()}}
  (out/'CONSTRAINED-GAUGES.json.gz').write_bytes(gzip.compress((json.dumps(result,separators=(',',':'),sort_keys=True)+'\n').encode(),mtime=0))
  print('BEST',best['receivers'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'))
 p.add_argument('--out',type=Path,default=here/'output');p.add_argument('--search',action='store_true')
 q=p.parse_args();main(q.repo.resolve(),q.out.resolve(),q.search)
