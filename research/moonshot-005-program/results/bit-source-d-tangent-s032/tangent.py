"""Exact full tangent of the 44 retained-H/source interpolation equations."""
from pathlib import Path
import importlib.util,json,gzip,numpy as np
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';here=Path(__file__).parent;four=base/'bit-simultaneous-d1509-s032'
s=importlib.util.spec_from_file_location('solve',four/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);g,a,*_=m.common_data(repo)
read=lambda p:json.loads(gzip.decompress(p.read_bytes()))if p.suffix=='.gz'else json.loads(p.read_text())
z=read(base/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');T=np.array(read(four/'output/D-WORD.json.gz')['matrix'],dtype=np.uint8);R=z['retained_receivers'];J=z['donors'];I={int(j):x for j,x in z['D_inputs'].items()};O={int(r):x for r,x in z['D_outputs'].items()};L=np.array(z['common_frames'],dtype=np.uint8);W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8);systems={tuple(map(int,k.split('/'))):{k:np.array(v,dtype=np.uint8)if k!='receiver_ingress_to_quotient_maps'else[np.array(M,dtype=np.uint8)for M in v]for k,v in vv.items()}for k,vv in z['systems'].items()};ci={(j,r):g.inverse(T[np.ix_(O[r],I[j])],a)for j in J for r in R}
allowed=[(q,p)for q in range(35)for p in range(35)if q>=19 or p<19];visible=sorted({(q,p)for j in J for r in R for q in O[r]for p in I[j]if q>=19 or p<19});vindex={qp:t for t,qp in enumerate(visible)};blocks=[];meta=[]
for (j,h),s in systems.items():
 N=s['relation_kernel'];c=s['H_observation_core'].shape[1];k=N.shape[1]
 if not k:continue
 block=np.zeros((6*k,len(visible)),dtype=np.uint8)
 for t,r in enumerate(R):
  A=a.mm(s['receiver_ingress_to_quotient_maps'][t],ci[j,r]);B=a.mm(ci[j,r],N[c+8*t:c+8*t+8]);tensor=a.product[A[:,None,:,None],B.T[None,:,None,:]].reshape(6*k,64)
  for oq,q in enumerate(O[r]):
   for ip,p in enumerate(I[j]):
    if(q,p)in vindex:block[:,vindex[q,p]]^=tensor[:,8*oq+ip]
 keep=np.flatnonzero(np.any(block,axis=1));blocks.append(block[keep]);meta.append({'donor':j,'H':h,'raw_equations':6*k,'nonzero_equations':len(keep)})
A=np.vstack(blocks);print('MATRIX',A.shape,'variables',len(allowed),'visible',len(visible),flush=True);RR,piv=g.rref(A,a);free=[q for q in range(len(visible))if q not in piv];N=np.zeros((len(visible),len(free)),dtype=np.uint8);N[free]=np.eye(len(free),dtype=np.uint8)
for q,t in enumerate(piv):N[t]=RR[q,free]
assert not np.any(a.mm(A,N));print('RANK',len(piv),'VISIBLE_TANGENT',len(free),'FULL_TANGENT',len(allowed)-len(piv),flush=True)
results=[];candidate=None
for col in range(min(8,len(free))):
 d=np.zeros((35,35),dtype=np.uint8)
 for qp,v in zip(visible,N[:,col]):d[qp]=v
 trial={'basis_column':col,'delta_rank':a.rank(d),'nonzero_coefficients':int(np.count_nonzero(d))};ss={};nil2=True
 for j in J:
  for r in R:
   D=d[np.ix_(O[r],I[j])];B=a.mm(D,ci[j,r]);nil2&=not np.any(a.mm(B,B))
 trial['all_retained_section_relative_squares_zero']=bool(nil2);TT=T^d
 if a.rank(TT[:19,:19])<19 or a.rank(TT[19:,19:])<16:trial['status']='singular_phase';results.append(trial);continue
 for j in J:
  for r in R:
   C=TT[np.ix_(O[r],I[j])]
   if a.rank(C)<8:trial['status']='singular_retained_section';break
   ss[j,r]=g.inverse(C,a)
  if'status'in trial:break
 if'status'in trial:results.append(trial);continue
 target={}
 for (j,h),s in systems.items():
  Y=np.hstack([a.mm(s['old_protected_map'],s['H_observation_core'])]+[a.mm(M,ss[j,r])for M,r in zip(s['receiver_ingress_to_quotient_maps'],R)]);res=a.mm(Y,s['relation_kernel']);target[j,h]=Y
  if np.any(res):trial.update(status='nonlinear_interpolation_obstruction',first_failure=[j,h],residual_rank=a.rank(res));break
 if'status'in trial:results.append(trial);continue
 BK={}
 for j in J:
  P=np.zeros((35,32),dtype=np.uint8);P[I[j]]=np.hstack([ss[j,r]for r in R]);BK[j]=a.mm(P,W)
 Z=np.hstack([BK[j]^BK[61]for j in J if j!=61]);trial.update(status='exact_interpolation_at_t1',contrast_rank=a.rank(Z),augmented_rank=a.rank(np.hstack([Z,BK[61]])));trial['common_response_rank']=trial['augmented_rank']-trial['contrast_rank'];results.append(trial)
 deltaF={}
 for (j,h),s in systems.items():
  X=s['input_generators'];change=target[j,h]^a.mm(s['old_protected_map'],X);_,cols=g.rref(X,a);B=X[:,cols];_,rows=g.rref(B.T,a);D=np.zeros((6,96),dtype=np.uint8);D[:,rows]=a.mm(change[:,cols],g.inverse(B[rows],a));assert np.array_equal(a.mm(D,X),change);deltaF[f'{j}/{h}']=D.tolist()
 candidate={'delta_D':d.tolist(),'D_matrix':TT.tolist(),'source_protected_delta':deltaF,'trial':trial};break
result={'status':'EXACT_FULL_SOURCE_D_TANGENT','phase_legal_variables':len(allowed),'retained_visible_variables':len(visible),'invisible_dimension':len(allowed)-len(visible),'equations':int(A.shape[0]),'constraint_rank':len(piv),'full_tangent_dimension':len(allowed)-len(piv),'source_image_changing_tangent_dimension':len(free),'local_systems':len(systems),'tests':results,'exact_candidate':candidate is not None,'full_source_rank_checks':False,'complete_fifth_receiver':False,'new_complete_kappa':False};(here/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');data={'visible_variables':visible,'constraint_matrix':A.tolist(),'constraint_pivots':piv,'visible_tangent_basis':N.tolist(),'local_equation_counts':meta,'candidate':candidate};(here/'CERTIFICATE.json.gz').write_bytes(gzip.compress((json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0));print(json.dumps(result),flush=True)
