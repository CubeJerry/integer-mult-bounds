#!/usr/bin/env python3
"""Independent target74 obstruction and target87 nonexclusion census."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('extension_gf',HERE.parent/'check.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def main(repo,out):
 B=repo/'research/moonshot-005-program/results';four=B/'bit-simultaneous-d1509-s032/output'
 pins=a.read(HERE/'output/SOURCE-PINS.json')
 for p,h in pins.items():a.need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'base review source pins')
 z=a.read(B/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');dw=a.read(four/'D-WORD.json.gz');proper=a.read(four/'PROPER.json.gz');gg=a.read(four/'CONSTRAINED-GAUGES.json.gz');hp=a.read(four/'H-PHYSICAL.json.gz');screen=a.read(B/'bit-coupled-fifth-s033/other-receivers/output/CERTIFICATE.json.gz')
 L=np.array(z['common_frames'],dtype=np.uint8);T=np.array(dw['matrix'],dtype=np.uint8);I={int(k):v for k,v in z['D_inputs'].items()};R=z['retained_receivers']
 Hby={tuple(x[:3]):int(h) for h,p in hp.items() for typ in ['X_owners','Y_owners'] for x in p[typ]};eye=np.eye(35,dtype=np.uint8)
 targets=[];allcert=[]
 for target in[74,87]:
  witness=next(v for v in screen if v['target']==target and v['anchor']==0);W=np.array(witness['L_coordinates'],dtype=np.uint8)
  active=[r for b,r in enumerate(R) if np.any(W[8*b:8*b+8])];a.need(len(active)==2,'two active blocks')
  indices=sum([list(range(8*R.index(r),8*R.index(r)+8)) for r in active],[]);unions={r:[eye[:,[4,5]]] for r in active};small=[]
  for j in z['donors']:
   parents={int(k.split('/')[1]) for k in z['systems'] if k.startswith(str(j)+'/')};item=proper[str(j)][str(target)];labels=list(map(tuple,item['labels']));inlabels={tuple(dw['owners'][p][:3]) for p in I[j]}
   off=[q for q,label in enumerate(labels) if Hby[label] in parents and label not in inlabels]
   A=a.mm(np.array(item['matrix'],dtype=np.uint8),np.array(gg['gauges'][str(j)],dtype=np.uint8));M=a.mm(A[off],L[:,indices]);N=a.null(M)
   if N.shape[1]!=4:continue
   for b,r in enumerate(active):
    U=a.null(M[:,8*b:8*b+8]);a.need(U.shape[1]==2,'tight direct sum block')
    O=z['D_outputs'][str(r)];V=a.mm(a.inverse(T[np.ix_(O,I[j])]),U);Ve=np.zeros((35,2),dtype=np.uint8);Ve[I[j]]=V;unions[r].append(Ve)
    Wr=W[8*R.index(r):8*R.index(r)+8];F=T[np.ix_(O,[4,5])];D=a.solve(F,Wr);a.need(a.rank(D)==2,'pinned two-column image')
    if target==74 and j==38:
     e=np.zeros((8,1),dtype=np.uint8);e[I[j].index(19),0]=1;n=a.solve(V,e)
     a.need({4,5,19}<=set(I[0]),'donor0 dependent triple for target74')
     small.append(dict(receiver=r,tight_donor=38,global_dependent_column=19,violated_donor=0,input_kernel=V.tolist(),unit_coefficients=n.tolist(),W_profile_factor=D.tolist()))
  records=[]
  for r in active:
   X=np.hstack(unions[r]);U=X[:,a.rref(X)[1]]
   dims={j:a.rank(U)+8-a.rank(np.hstack([U,eye[:,ii]])) for j,ii in I.items()}
   support=np.flatnonzero(np.any(U,axis=1)).tolist()
   if target==87:a.need(U.shape[1]==8 and support==[2,4,5,14,16,17,27,31] and set(dims.values())=={2},'exact target87 unexcluded union profile')
   records.append(dict(receiver=r,span_dimension=U.shape[1],coordinate_support=support,native_intersection_dimensions=dims,span_basis=U.tolist()))
  if target==74:a.need(len(small)==2,'both target74 retained blocks force singularity')
  targets.append(dict(target=target,active_receivers=active,status='excluded_by_normalized_column_dependence' if target==74 else'not_excluded_by_input_union_test',witness_count=len(small)))
  allcert.append(dict(target=target,witnesses=small,input_union_gates=records))
 # The two additional normalized pin frames are fixed by all source0 parents.
 normals=[]
 for r in[6,73]:
  O=z['D_outputs'][str(r)];X=a.mm(L[:,8*R.index(r):8*R.index(r)+8],T[np.ix_(O,[4,5])]);cs=[]
  for key,system in z['systems'].items():
   if key.startswith('0/'):cs.append(dict(system=key,coefficients=a.solve(np.array(system['H_observation_core'],dtype=np.uint8),X).tolist()))
  a.need(len(cs)==4,'four H-only parent normalization decompositions')
  item=proper['0'][str(r)];labels=list(map(tuple,item['labels']));A=a.mm(np.array(item['matrix'],dtype=np.uint8),np.array(gg['gauges']['0'],dtype=np.uint8));E=np.zeros((96,2),dtype=np.uint8)
  for q,p in enumerate([4,5]):E[labels.index(tuple(dw['owners'][p][:3])),q]=1
  a.need(np.array_equal(a.mm(A,X),E),'literal H-preserved D input4,5 action')
  normals.append(dict(receiver=r,H_decompositions=cs))
 result=dict(status='PASS_INDEPENDENT_TARGET74_OBSTRUCTION_AND_TARGET87_UNION_SCREEN',targets=targets,additional_H_normalization_checks=8,phase_or_shared_row_constraints_used=False,target87_existence_claim=False,new_complete_kappa=False)
 out.mkdir(parents=True,exist_ok=True)
 for name,data in [('EXTENSION-RESULT',result),('EXTENSION-CERTIFICATE',dict(targets=allcert,normalized_pins=normals))]:(out/(name+'.json')).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
