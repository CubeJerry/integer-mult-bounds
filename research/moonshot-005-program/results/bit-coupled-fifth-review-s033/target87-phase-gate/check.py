#!/usr/bin/env python3
"""Exact receiver87 phase premise audit; no all-native feasibility claim."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('phase_gf',HERE.parent/'check.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def extend(X):
 B=X.copy()
 for v in np.eye(8,dtype=np.uint8).T:
  if a.rank(np.column_stack([B,v]))>B.shape[1]:B=np.column_stack([B,v])
 a.need(B.shape==(8,8) and a.rank(B)==8,'basis extension');return B

def main(repo,out):
 B=repo/'research/moonshot-005-program/results';four=B/'bit-simultaneous-d1509-s032/output'
 paths=[B/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',four/'D-WORD.json.gz',HERE.parent/'target54-normalized-singularity/output/EXTENSION-CERTIFICATE.json',HERE.parent/'target54-normalized-singularity/SOURCE-PINS.json',HERE.parent/'check.py']
 z,dw,prior,pins=map(a.read,paths[:-1])
 for p,h in pins.items():a.need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'prior frozen review input')
 T=np.array(dw['matrix'],dtype=np.uint8);I={int(j):v for j,v in z['D_inputs'].items()};O={r:z['D_outputs'][str(r)] for r in[9,73]}
 a.need(I[0]==[0,3,4,5,15,19,20,22],'literal donor0 inputs')
 census=[dict(donor=j,inputs=ii,early_count=sum(p<19 for p in ii),late_count=sum(p>=19 for p in ii)) for j,ii in I.items()]
 a.need(next(x for x in census if x['donor']==0)['early_count']==5,'donor0 five early three late')
 a.need(all(sum(q<19 for q in oo)==4 for oo in O.values()),'four early and four late outputs')
 pairdonors=[j for j,ii in I.items() if {4,5}<=set(ii)];a.need(pairdonors==[0,61,62],'all pinned-pair donors')
 lower={j:max(0,6-sum(p<19 for p in I[j])) for j in pairdonors};a.need(max(lower.values())==1,'early profile rank lower bound is one')
 containing27=[j for j,ii in I.items() if 27 in ii];a.need(containing27==[35,45] and not any({27,31}<=set(ii) for ii in I.values()),'late union input incidence')
 prior87=next(x for x in prior['targets'] if x['target']==87);Uc=[2,4,5,14,16,17,27,31]
 for x in prior87['input_union_gates']:a.need(x['coordinate_support']==Uc and x['span_dimension']==8,'frozen exact input union')
 # Abstract two-dimensional U-code: the second coordinate is late.
 code=np.array([[1,1,1,1,1,1,0,0],[0,0,1,0,0,1,1,1]],dtype=np.uint8)
 pairchecks=[]
 for j,ii in I.items():
  pair=sorted(set(ii)&set(Uc));a.need(len(pair)==2,'two union coordinates per native donor')
  v=code[:,[Uc.index(p) for p in pair]];a.need(a.rank(v)==2,'every native U-pair independent')
  pairchecks.append(dict(donor=j,pair=pair,rank=2))
 a.need(not np.any(code[0,[Uc.index(27),Uc.index(31)]]),'late union inputs annihilated by early projection')
 e=np.eye(8,dtype=np.uint8);C=np.column_stack([e[:,0],e[:,0]^e[:,4]])
 assignments={0:e[:,1],1:e[:,2],2:e[:,0],3:e[:,2],4:C[:,0],5:C[:,1],6:e[:,3],10:e[:,2],14:e[:,0],15:e[:,3],16:e[:,0],17:C[:,1],18:e[:,3],19:e[:,5],20:e[:,6],22:e[:,7],23:e[:,5],25:e[:,5],26:e[:,6],27:e[:,4],31:e[:,4],32:e[:,6]}
 cert=[]
 for r,oo in O.items():
  oldF=T[np.ix_(oo,[4,5])];a.need(a.rank(oldF[:4])==2,'literal readout profile has early rank two');Q=a.mm(extend(C),a.inverse(extend(oldF)));a.need(np.array_equal(a.mm(Q,oldF),C),'common readout image')
  P=np.zeros((8,35),dtype=np.uint8)
  for q,v in assignments.items():P[:,q]=v
  P[:,[7,8]]=a.mm(Q,T[np.ix_(oo,[7,8])])
  a.need(not np.any(P[:4,19:]),'late to early zeros')
  a.need(a.rank(P[:,[4,5]])==2 and a.rank(P[:4,[4,5]])==1,'full profile rank two early rank one')
  a.need(a.rank(np.hstack([C,P[:,Uc]]))==2 and np.any(P[:,27]) and np.any(P[:,31]),'nonzero late columns remain in profile')
  normalized=a.mm(a.inverse(Q),P);a.need(np.array_equal(normalized[:,[4,5,7,8]],T[np.ix_(oo,[4,5,7,8])]),'all four normalized pins')
  sr={j:a.rank(P[:,I[j]]) for j in[0,32,35]};a.need(set(sr.values())=={8},'three specified native sections invertible')
  cert.append(dict(receiver=r,output_rows=oo,physical_partial_rows=P.tolist(),common_readout=Q.tolist(),normalized_partial_rows=normalized.tolist(),profile=C.tolist(),checked_section_ranks=sr))
 result=dict(status='PASS_RECEIVER87_PHASE_PREMISE_AUDIT',donor_phase_census=census,donors_containing_pinned_pair=pairdonors,pair_based_early_rank_lower_bounds=lower,donors_containing_late27=containing27,necessary_physical_profile_early_rank=1,proposed_rank_two_premise_valid=False,abstract_U_pair_checks=pairchecks,receiver87_excluded=False,literal_readout_phase_subfamily_excluded=True,partial_counterexample_checked_donors=[0,32,35],all_native_candidate_claim=False,new_complete_kappa=False)
 sourcepins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};expected=HERE/'SOURCE-PINS.json'
 if expected.exists():a.need(sourcepins==a.read(expected),'source pins')
 out.mkdir(parents=True,exist_ok=True)
 for name,data in [('RESULT',result),('CERTIFICATE',dict(U_coordinates=Uc,abstract_U_code=code.tolist(),partial_models=cert)),('SOURCE-PINS',sourcepins)]:(out/(name+'.json')).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
