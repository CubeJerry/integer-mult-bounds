"""Bounded exact source/D interpolation with actual retained H observations."""
from pathlib import Path
import importlib.util,json,gzip,hashlib,numpy as np,time
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032';here=Path(__file__).parent
s=importlib.util.spec_from_file_location('solver',four/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);g,a,ff,Ks,C=m.common_data(repo)
src=m.ex.read(four/'output/SOURCES.json.gz');gg=m.ex.read(four/'output/CONSTRAINED-GAUGES.json.gz');prop=m.ex.read(four/'output/PROPER.json.gz');dw=m.ex.read(four/'output/D-WORD.json.gz');ph=m.ex.read(four/'output/H-PHYSICAL.json.gz');fib=m.ex.read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');T=np.array(dw['matrix'],dtype=np.uint8);owners=dw['owners'];L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];J=sorted(map(int,src['paired_maps']));prot=list(range(48))+list(range(240,288));pr=[0,1,2,15,16,17]
K=np.array(json.loads((base/'bit-fifth-receiver-quotient-s032/FORCED-COLLISION.json').read_text())['forced_collision'],dtype=np.uint8)
def solve(X,Y):
 _,cols=g.rref(X,a);B=X[:,cols];_,rows=g.rref(B.T,a);c=a.mm(g.inverse(B[rows],a),Y[rows]);ans=np.zeros((X.shape[1],Y.shape[1]),dtype=np.uint8);ans[cols]=c;assert np.array_equal(a.mm(X,ans),Y);return ans
W=solve(L,K);Hby={tuple(x[:3]):int(h)for h,z in ph.items()for nam in ['X_owners','Y_owners']for x in z[nam]};In={j:[q for q,x in enumerate(owners)if x[3]is not None and j in a.planes[x[3]]]for j in J};Out={r:[q for q,x in enumerate(owners)if x[5]is not None and r in a.planes[x[5]]]for r in R};inowners={j:{tuple(owners[q][:3]):t for t,q in enumerate(In[j])}for j in J};local={};cinv={(j,r):g.inverse(T[np.ix_(Out[r],In[j])],a)for j in J for r in R}
for j in J:
 G=np.array(gg['gauges'][str(j)],dtype=np.uint8)
 for hs,F0 in src['paired_maps'][str(j)].items():
  h=int(hs)
  if not a.planes[h]<=a.charts[1509]:continue
  F=np.array(F0,dtype=np.uint8)[np.ix_(pr,prot)];vs=[]
  for center,rr in fib.items():
   if j not in a.planes[int(center)]:continue
   for r,z in rr.items():
    if int(r)>=111 or (int(center)!=h and not a.planes[h]<=a.adj[int(r)]):continue
    k=np.array(z['kernel'],dtype=np.uint8)[:48,:3];zero=np.zeros_like(k);vs.append(np.block([[k,zero],[zero,k]]))
  C=m.basis(np.hstack(vs),g,a)if vs else np.zeros((96,0),dtype=np.uint8);X=np.hstack([C,L]);N=m.null(X,g,a);maps=[]
  for r in R:
   z=prop[str(j)][str(r)];labels=[tuple(x)for x in z['labels']];ix=[q for q,x in enumerate(labels)if Hby[x]==h];A=a.mm(np.array(z['matrix'],dtype=np.uint8)[ix],G);_,p=g.rref(F,a);B=a.mm(A[:,p],g.inverse(F[:,p],a));assert B.shape==(6,6)and np.array_equal(a.mm(B,F),A)
   E=np.zeros((6,8),dtype=np.uint8)
   for q,x in enumerate([labels[t]for t in ix]):
    if x in inowners[j]:E[q,inowners[j][x]]=1
   maps.append(a.mm(g.inverse(B,a),E))
  old=np.hstack([a.mm(F,C),a.mm(F,L)]);assert not np.any(a.mm(old,N));local[j,h]={'F':F,'C':C,'N':N,'maps':maps,'X':X}
print('READY',len(local),'local interpolation systems',flush=True)
admitted=np.array(json.loads((base/'bit-d1509-coupled-repair-s032/ALL-DONOR-VECTOR.json').read_text())['witness']['matrix'],dtype=np.uint8)
for j in J:
 for r in R:assert np.array_equal(admitted[np.ix_(Out[r],In[j])],T[np.ix_(Out[r],In[j])])
assert a.rank(L)==32 and m.null(L,g,a).shape[1]==0
certificate={'retained_receivers':R,'donors':J,'D_inputs':In,'D_outputs':Out,'common_frames':L.tolist(),'forced_K_coordinates_in_L':W.tolist(),'systems':{f'{j}/{h}':{'old_protected_map':z['F'].tolist(),'H_observation_core':z['C'].tolist(),'input_generators':z['X'].tolist(),'relation_kernel':z['N'].tolist(),'receiver_ingress_to_quotient_maps':[M.tolist()for M in z['maps']]}for (j,h),z in local.items()}}
(here/'INTERPOLATION.json.gz').write_bytes(gzip.compress((json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
used=sorted(set(sum(Out.values(),[])));pairs=[(q,p)for q in used for p in range(35)if q!=p and(q>=19 or p<19)];pairs=sorted(pairs,key=lambda z:hashlib.sha256(str(z).encode()).digest())[:128]
records=[];best=None;deadline=time.time()+240
for q,p in pairs:
 if time.time()>deadline:break
 c=1;TT=T.copy();TT[q]^=T[p];ci={};bad=None
 for j in J:
  for r in R:
   A=TT[np.ix_(Out[r],In[j])]
   if a.rank(A)<8:bad=['singular_section',j,r];break
   ci[j,r]=g.inverse(A,a)
  if bad:break
 if bad:records.append({'output_shear':[q,p,c],'status':bad});continue
 targets={}
 for (j,h),z in local.items():
  Y=np.hstack([a.mm(z['F'],z['C'])]+[a.mm(M,ci[j,r])for M,r in zip(z['maps'],R)])
  residual=a.mm(Y,z['N'])
  if np.any(residual):bad=['H_source_interpolation_inconsistent',j,h,a.rank(residual)];break
  targets[j,h]=Y
 if bad:records.append({'output_shear':[q,p,c],'status':bad});continue
 BK={}
 for j in J:
  Z=np.zeros((35,32),dtype=np.uint8);Z[In[j]]=np.hstack([ci[j,r]for r in R]);BK[j]=a.mm(Z,W)
 contrasts=np.hstack([BK[j]^BK[61]for j in J if j!=61]);rank=a.rank(contrasts);joint=a.rank(np.hstack([contrasts,BK[61]]));improve=joint-rank
 rec={'output_shear':[q,p,c],'status':'linear_source_interpolation_feasible','contrast_rank':rank,'augmented_rank':joint,'common_response_rank':improve,'changed_ingress_coordinates':np.flatnonzero(np.any(np.hstack([BK[j]^a.mm(np.array(m.ex.read(base/'bit-d1509-coupled-repair-s032/DATA.json.gz')['ingress'][str(j)],dtype=np.uint8),K)for j in J]),axis=1)).tolist()};records.append(rec)
 if improve>2:
  best={'matrix':TT.tolist(),'record':rec,'source_protected_changes':{}}
  for (j,h),z in local.items():
   delta=targets[j,h]^a.mm(z['F'],z['X']);_,cols=g.rref(z['X'],a);B=z['X'][:,cols];_,rows=g.rref(B.T,a);D=np.zeros((6,96),dtype=np.uint8);D[:,rows]=a.mm(delta[:,cols],g.inverse(B[rows],a));assert np.array_equal(a.mm(D,z['X']),delta);best['source_protected_changes'][f'{j}/{h}']=D.tolist()
  break
result={'status':'BOUNDED_SOURCE_D_INTERPOLATION','actual_local_systems':len(local),'trial_limit':128,'trials_run':len(records),'time_limit_seconds':240,'records':records,'candidate':best,'positive_controls':['original D word with literal old source maps','admitted six-free-row D repair has identical retained sections','without H constraints, L has no kernel and all nonsingular sections interpolate'],'prescribed_K_fixed':True,'restricted_source_family':'protected six quotient rows on 96 source coordinates; four D parents per donor; all other source coefficients unchanged','full_source_rank_checks_done':False,'complete_fifth_receiver':False,'new_complete_kappa':False}
(here/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('DONE',len(records),'feasible',sum(z['status']=='linear_source_interpolation_feasible'for z in records),'improved',best is not None,flush=True)
