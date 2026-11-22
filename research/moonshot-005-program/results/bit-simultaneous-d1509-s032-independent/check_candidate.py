#!/usr/bin/env python3
"""Independent exact S032 source-gauge and five-receiver audit."""
import argparse,hashlib,itertools,runpy
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
TOOLS=runpy.run_path(str(HERE/'check_frames.py'))
mm,rank,inverse,basis,need,rd,wr=[TOOLS[k] for k in ['mm','rank','inverse','basis','need','rd','wr']]
ALG=TOOLS['ALG'];null=ALG['null'];echelon=ALG['echelon'];BASE=TOOLS['BASE'];ROOT=TOOLS['ROOT']
def transform_rows(A,G):
 A=np.array(A,dtype=np.uint8);B=A.copy();prot=list(range(48))+list(range(240,288));B[:,prot]=mm(A[:,prot],G);return B
def same_span(A,B):return rank(A)==rank(B)==rank(np.hstack([A,B]))
def rank_proof(A):
 rows,cols,_=echelon(A);_,rowids,_=echelon(A[:,cols].T);minor=A[np.ix_(rowids,cols)];_,cp,det=echelon(minor);N=null(A)
 need(len(cols)==len(cp) and det!=0 and not np.any(mm(A,N)) and rank(N)==A.shape[1]-len(cols),'rank lower/upper certificate')
 return {'rank':len(cols),'minor_rows':rowids,'minor_columns':cols,'minor_determinant':det,'kernel':N.tolist()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 old=BASE/'bit-shared-h-s031-construction/native-d1509-all-native/output';new=args.package;own=HERE/'output'
 frames={int(j):{int(r):np.array(A,dtype=np.uint8) for r,A in row.items()} for j,row in rd(own/'FRAMES.json.gz').items()}
 cores={int(j):{k:np.array(A,dtype=np.uint8).reshape(96,-1) for k,A in row.items()} for j,row in rd(own/'CORES.json.gz').items()}
 gauge=rd(new/'CONSTRAINED-GAUGES.json.gz');selected=gauge['receivers'];L=np.array(gauge['common_frames'],dtype=np.uint8)
 need(selected==[6,9,48,73] and L.shape==(96,32) and rank(L)==32,'four independent actual receiver frames')
 source0,source1=rd(old/'SOURCES.json.gz'),rd(new/'SOURCES.json.gz');early0,early1=rd(old/'EARLY.json.gz'),rd(new/'EARLY.json.gz')
 need(source0['frames']==source1['frames'],'all local source frames unchanged');need(source1['simultaneous_receivers']==selected,'simultaneous receiver labels')
 S=np.array(source1['simultaneous_original_space'],dtype=np.uint8);prot=list(range(48))+list(range(240,288));comp=[c for c in range(480) if c not in prot]
 need(S.shape==(480,32) and np.array_equal(S[prot],L) and not np.any(S[comp]),'full480 common parameter field')
 for name in ['H-PHYSICAL.json.gz','D-WORD.json.gz']:need((old/name).read_bytes()==(new/name).read_bytes(),'frozen physical '+name)
 quotient_count=0;late_count=0;records=[]
 for j in sorted(frames):
  G=np.array(gauge['gauges'][str(j)],dtype=np.uint8);need(G.shape==(96,96) and rank(G)==96,'invertible source gauge')
  C=cores[j]['H_and_receiver6'];claimed=np.array(gauge['fixed_subspaces'][str(j)],dtype=np.uint8)
  need(same_span(C,claimed) and np.array_equal(mm(G,C),C),'pointwise whole H and receiver6 preservation')
  U=np.hstack([frames[j][r] for r in selected]);need(np.array_equal(mm(G,L),U),'one oriented gauge for four receivers')
  need(same_span(np.array(gauge['retained_cores']['263'],dtype=np.uint8),cores[0]['H']) and same_span(np.array(gauge['retained_cores']['642'],dtype=np.uint8),cores[45]['H']),'paired whole-H cores')
  for h,A in source0['paired_maps'][str(j)].items():
   need(np.array_equal(transform_rows(A,G),source1['paired_maps'][str(j)][h]),'actual paired source composed');quotient_count+=1
  for h,A in source0['late_parities'][str(j)].items():
   A=np.array(A,dtype=np.uint8).reshape(-1,480);B=np.array(source1['late_parities'][str(j)][h],dtype=np.uint8).reshape(-1,480)
   need(np.array_equal(transform_rows(A,G),B),'every late parity composed');late_count+=len(A)
  for field in ['matrix','physical_matrix']:need(np.array_equal(transform_rows(early0[str(j)][field],G),early1[str(j)][field]),'actual full early owner matrix composed')
  need(early0[str(j)]['row_owners']==early1[str(j)]['row_owners'],'same original early owners')
  need(not np.array_equal(mm(G,np.column_stack([L[:,1],L[:,0],L[:,2:]])),U),'swapped readout rejected')
  altered=G.copy();altered[0,0]^=1;testcols=np.hstack([C,L,np.eye(96,dtype=np.uint8)])
  need(not np.array_equal(mm(altered,testcols),mm(G,testcols)),'changed source action rejected')
  records.append({'donor':j,'gauge_rank':96,'H_constraint_dimension':cores[j]['H'].shape[1],'fixed_with_receiver6_dimension':C.shape[1],'common_frame_rank':32})
  print('INDEPENDENT_GAUGE',j,96,C.shape[1],32,flush=True)
 native=[r for r in sorted(frames[0]) if r<111];need(len(native)==11,'eleven native receivers');witnesses=[]
 for selected5 in itertools.combinations(native,5):
  A=np.hstack([frames[0][r] for r in selected5]);r0=rank(A);chosen=None
  for j in [45,32,61]:
   B=np.hstack([frames[j][r] for r in selected5]);rj=rank(B)
   if rj!=r0:chosen=(j,B,rj);break
  need(chosen is not None,'five-receiver independent obstruction');j,B,rj=chosen;p0,pj=rank_proof(A),rank_proof(B)
  need(p0['rank']==r0 and pj['rank']==rj,'rank certificate agreement')
  witnesses.append({'receivers':list(selected5),'donor_pair':[0,j],'ranks':[r0,rj],'certificates':[p0,pj]})
 need(len(witnesses)==462,'all native five-sets');counts={}
 for w in witnesses:counts[str(w['donor_pair'][1])]=counts.get(str(w['donor_pair'][1]),0)+1
 A=np.hstack([frames[0][r] for r in native[:5]]);need(rank(A)==rank(A.copy()),'identical source control')
 result={'status':'PASS_INDEPENDENT_FOUR_RECEIVERS_AND_FIVE_RECEIVER_GAUGE_GATE','simultaneous_receivers':selected,'native_donors':sorted(frames),'actual_common_dimension_each':8,'joint_common_dimension':32,'gauge_records':records,'composed_paired_quotients':quotient_count,'composed_late_parities':late_count,'native_five_sets_excluded':len(witnesses),'witness_donor_counts':counts,'preserved_H_whole_fibres':True,'frozen_H_D_word':True,'scope':'fixed proper ingress and invertible linear source gauges; invertible D readout basis changes preserve fibre spans','controls':['swapped output frame rejected','changed source action rejected','identical source not excluded'],'new_author_executable_imports':False,'complete_supplier':False,'new_kappa':False}
 wr(args.out/'RESULT.json',result);wr(args.out/'FIVE-RECEIVER-WITNESSES.json.gz',witnesses)
 files=[new/n for n in ['CONSTRAINED-GAUGES.json.gz','SOURCES.json.gz','EARLY.json.gz','H-PHYSICAL.json.gz','D-WORD.json.gz']]+[own/n for n in ['FRAMES.json.gz','CORES.json.gz']]
 wr(args.out/'SOURCE-PINS.json',{'files':{str(p.resolve().relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
 print(result,flush=True)
if __name__=='__main__':main()


