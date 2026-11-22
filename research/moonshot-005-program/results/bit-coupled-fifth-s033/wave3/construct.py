"""Reproduce the explicit diagonal-pencil point; no whole fifth receiver claimed.
@CubeJerry, substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import importlib.util,json,gzip,numpy as np,time,sys
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,default=Path.cwd());parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032'
s=importlib.util.spec_from_file_location('solve',four/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);g,a,*_=m.common_data(repo)
read=lambda p:json.loads(gzip.decompress(p.read_bytes()))if p.suffix=='.gz'else json.loads(p.read_text())
z=read(base/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');T=np.array(read(four/'output/D-WORD.json.gz')['matrix'],dtype=np.uint8);R=z['retained_receivers'];J=z['donors'];I={int(j):x for j,x in z['D_inputs'].items()};O={int(r):x for r,x in z['D_outputs'].items()};L=np.array(z['common_frames'],dtype=np.uint8);W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8);systems={tuple(map(int,k.split('/'))):{k:np.array(v,dtype=np.uint8)if k!='receiver_ingress_to_quotient_maps'else[np.array(M,dtype=np.uint8)for M in v]for k,v in vv.items()}for k,vv in z['systems'].items()};ci={(j,r):g.inverse(T[np.ix_(O[r],I[j])],a)for j in J for r in R}


def assess(TT):
 if a.rank(TT[:19,:19])<19 or a.rank(TT[19:,19:])<16:return {'status':'phase'},None
 ss={}
 for j in J:
  for r in R:
   C=TT[np.ix_(O[r],I[j])]
   if a.rank(C)<8:return {'status':'section','pair':[j,r]},None
   ss[j,r]=g.inverse(C,a)
 for (j,h),s in systems.items():
  Y=np.hstack([a.mm(s['old_protected_map'],s['H_observation_core'])]+[a.mm(M,ss[j,r])for M,r in zip(s['receiver_ingress_to_quotient_maps'],R)])
  res=a.mm(Y,s['relation_kernel'])
  if np.any(res):return {'status':'relation','pair':[j,h],'rank':a.rank(res)},None
 BK={}
 for j in J:
  P=np.zeros((35,32),dtype=np.uint8);P[I[j]]=np.hstack([ss[j,r]for r in R]);BK[j]=a.mm(P,W)
 Z=np.hstack([BK[j]^BK[61]for j in J if j!=61]);r=a.rank(Z);q=a.rank(np.hstack([Z,BK[61]]))-r
 return {'status':'ok','contrast':r,'q':q},ss


B=[4,5,7,8];rG=O[48];rH=O[73];rA=[10,13,16,18,30,31,32,33]
alpha=np.array([53,53,58,58],dtype=np.uint8);inv64=np.array([0]+[int(g.inverse(np.array([[x]],dtype=np.uint8),a)[0,0])for x in range(1,64)],dtype=np.uint8);dF=a.product[alpha,inv64[alpha^1]]
GF=T[np.ix_(rG,B)];HF=T[np.ix_(rH,B)];print('Franks',[a.rank(GF[:4]),a.rank(GF[4:]),a.rank(HF[:4]),a.rank(HF[4:])],'dF',dF.tolist(),flush=True)
M=np.zeros((8,8),dtype=np.uint8)
for sl in[slice(0,4),slice(4,8)]:M[sl,sl]=a.mm(a.product[HF[sl],inv64[dF][None,:]],g.inverse(GF[sl],a))
need=lambda b,msg:None if b else (_ for _ in()).throw(ValueError(msg))
need(a.rank(M)==8,'M');N=np.zeros((8,8),dtype=np.uint8)
for r,start in[(10,0),(30,4)]:
 e=np.eye(8,dtype=np.uint8)[rG.index(r)];n=e^M[rH.index(r)];tail=[n]
 for e0 in np.eye(8,dtype=np.uint8)[start:start+4]:
  if a.rank(np.array(tail+[e0]))>len(tail):tail.append(e0)
  if len(tail)==4:break
 N[start:start+4]=np.array(tail)
need(a.rank(N)==8,'A basis');print('M',M.tolist(),'N',N.tolist(),flush=True)
oldowners=read(four/'output/D-WORD.json.gz')['owners'];geomJ=sorted(a.charts[1509]);geomR=[r for r in range(120)if a.charts[1509]<=a.adj[r]];gin={j:[q for q,x in enumerate(oldowners)if x[3]is not None and j in a.planes[x[3]]]for j in geomJ};gout={r:[q for q,x in enumerate(oldowners)if x[5]is not None and r in a.planes[x[5]]]for r in geomR}
need(gout[95]==rA,'actual95outputs');frozen={(q,p)for q in set(sum(O.values(),[]))for p in B};starttime=time.time();stats={}
for seed in [22]:
 rng=np.random.default_rng(333000+seed);d=rng.integers(2,64,size=35,dtype=np.uint8);d[B]=dF;G=np.zeros((8,35),dtype=np.uint8);G[:,B]=GF
 for p in range(35):
  if p in B:continue
  for sl,shared in[(slice(0,4),10),(slice(4,8),30)]:
   if p>=19 and sl.start==0:continue
   e=np.eye(8,dtype=np.uint8)[rG.index(shared)];constraint=e^a.product[d[p],M[rH.index(shared)]];ker=m.null(constraint[None,sl],g,a);G[sl,p]=a.mm(ker,rng.integers(0,64,size=(ker.shape[1],1),dtype=np.uint8))[:,0]
 H=a.product[a.mm(M,G),d[None,:]];AA=a.product[a.mm(N,G),a.product[d,inv64[d^1]][None,:]]
 need(np.array_equal(G[:,B],GF)and np.array_equal(H[:,B],HF),'fixedF');need(np.array_equal(G[rG.index(10)],H[rH.index(10)])and np.array_equal(G[rG.index(30)],H[rH.index(30)]),'sharedGH');need(np.array_equal(G[rG.index(10)],AA[0])and np.array_equal(G[rG.index(30)],AA[4]),'sharedGA')
 TT=T.copy()
 for q in range(35):
  for p in range(35):
   if(q>=19 or p<19)and(q,p)not in frozen:TT[q,p]=rng.integers(0,64)
 TT[rG]=G;TT[rH]=H;TT[rA]=AA
 res,ss=assess(TT);stats[res['status']]=stats.get(res['status'],0)+1
 if res['status']=='ok':
  BK={}
  for j in J:
   Z0=np.zeros((35,32),dtype=np.uint8);Z0[I[j]]=np.hstack([ss[j,r]for r in R]);BK[j]=a.mm(Z0,W)
  Z=np.hstack([BK[j]^BK[61]for j in J if j!=61]);rz=a.rank(Z);ra=a.rank(np.hstack([Z,BK[61]]));response=a.rank(a.mm(TT[rA],Z));commonrank=a.rank(a.mm(TT[rA],BK[61]));print('EXACT',seed,res,'actual95',response,commonrank,flush=True)
  need(response==0 and commonrank==4,'pencilreadout');need(rz<=24,'contrasttarget')
  bad=[[j,r]for j in geomJ for r in geomR if a.rank(TT[np.ix_(gout[r],gin[j])])!=8]
  if bad:print('geom bad',len(bad),flush=True);continue
  deltaF={}
  for(j,h),s in systems.items():
   Y=np.hstack([a.mm(s['old_protected_map'],s['H_observation_core'])]+[a.mm(Q,ss[j,r])for Q,r in zip(s['receiver_ingress_to_quotient_maps'],R)]);X=s['input_generators'];change=Y^a.mm(s['old_protected_map'],X);_,cols=g.rref(X,a);bb=X[:,cols];_,rr=g.rref(bb.T,a);D=np.zeros((6,96),dtype=np.uint8);D[:,rr]=a.mm(change[:,cols],g.inverse(bb[rr],a));need(np.array_equal(a.mm(D,X),change),'sourceextension');deltaF[f'{j}/{h}']=D.tolist()
  VV=sorted(set(sum(I.values(),[])));intdim=16-a.rank(np.vstack([G[:,VV],H[:,VV]]));data={'seed':seed,'D_matrix':TT.tolist(),'source_protected_delta':deltaF,'result':res,'native_union':VV,'d':d.tolist(),'M':M.tolist(),'N':N.tolist(),'alpha':alpha.tolist(),'actual95_contrast_rank':response,'actual95_common_response_rank':commonrank,'intersection_dimension':intdim,'all_geometric_sections':144,'fixed_K_span_rank':ra}
  (args.out/'PENCIL-CANDIDATE.json').write_text(json.dumps(data));print('SUCCESS',seed,stats,'intersection',intdim,round(time.time()-starttime,2),flush=True);break
 if seed%100==0:print(seed,stats,round(time.time()-starttime,2),flush=True)
else:print('NO CANDIDATE',stats,round(time.time()-starttime,2),flush=True)
