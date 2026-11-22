"""Reproduce the explicit seed59 coupled local candidate; no full source or supplier.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
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


B=[4,5,7,8];VV=sorted(set(sum(I.values(),[])));absent=[p for p in range(35)if p not in VV]
cs={48:np.array([[12,5,10,28],[43,1,0,12]],dtype=np.uint8),73:np.array([[0,49,62,58],[12,11,18,63]],dtype=np.uint8)};ors={48:[21,22,30,34],73:[20,23,25,30]};lam=np.zeros((2,35),dtype=np.uint8)
for r in[48,73]:lam[:,ors[r]]^=cs[r]
assert not np.any(a.mm(lam,T[:,B]));_,lr=g.rref(lam[:,19:],a);pivot=[19+x for x in lr];inv=g.inverse(lam[:,pivot],a)
frozen={(q,p)for q in set(sum(O.values(),[]))for p in B}
oldowners=read(four/'output/D-WORD.json.gz')['owners'];geomJ=sorted(a.charts[1509]);geomR=[r for r in range(120)if a.charts[1509]<=a.adj[r]];gin={j:[q for q,x in enumerate(oldowners)if x[3]is not None and j in a.planes[x[3]]]for j in geomJ};gout={r:[q for q,x in enumerate(oldowners)if x[5]is not None and r in a.planes[x[5]]]for r in geomR}
print('pivot',pivot,'absent',absent,flush=True);stats={};start=time.time()
for seed in [59]:
 rng=np.random.default_rng(seed+3300);TT=T.copy()
 for q in range(35):
  for p in range(35):
   if(q>=19 or p<19)and(q,p)not in frozen:TT[q,p]=rng.integers(0,64)
 for p in VV:
  if p in B:continue
  TT[pivot,p]=0;TT[pivot,p]=a.mm(inv,a.mm(lam,TT[:,p:p+1]))[:,0]
 assert not np.any(a.mm(lam,TT[:,VV]))
 res,ss=assess(TT);stats[res['status']]=stats.get(res['status'],0)+1
 if res['status']=='ok':
  print('EXACT',seed,res,flush=True)
  if res['q']<4:raise ValueError('q not4')
  bad=[[j,r]for j in geomJ for r in geomR if a.rank(TT[np.ix_(gout[r],gin[j])])!=8]
  if bad:print('geom bad',len(bad),flush=True);continue
  deltaF={}
  for(j,h),s in systems.items():
   Y=np.hstack([a.mm(s['old_protected_map'],s['H_observation_core'])]+[a.mm(M,ss[j,r])for M,r in zip(s['receiver_ingress_to_quotient_maps'],R)])
   X=s['input_generators'];change=Y^a.mm(s['old_protected_map'],X);_,cols=g.rref(X,a);bb=X[:,cols];_,rr=g.rref(bb.T,a);D=np.zeros((6,96),dtype=np.uint8);D[:,rr]=a.mm(change[:,cols],g.inverse(bb[rr],a));assert np.array_equal(a.mm(D,X),change);deltaF[f'{j}/{h}']=D.tolist()
  data={'seed':seed,'D_matrix':TT.tolist(),'source_protected_delta':deltaF,'result':res,'overlap_rows':lam.tolist(),'receiver_combinations':{r:c.tolist()for r,c in cs.items()},'receiver_combination_rows':ors,'native_ingress_union':VV,'absent_ingress':absent,'all_geometric_sections':144}
  (args.out/'OVERLAP-CANDIDATE.json').write_text(json.dumps(data));print('SUCCESS',seed,stats,round(time.time()-start,2),flush=True);break
 if seed%100==0:print(seed,stats,round(time.time()-start,2),flush=True)
else:print('NO CANDIDATE',stats,round(time.time()-start,2),flush=True)
