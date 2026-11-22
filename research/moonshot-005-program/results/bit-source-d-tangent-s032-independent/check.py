#!/usr/bin/env python3
"""Audit tangent and finite lift using independently reconstructed local systems."""
import argparse,hashlib,json,runpy
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parents[2]
H=runpy.run_path(str(BASE/'bit-simultaneous-d1509-s032-independent/check_frames.py'))
mm,rank,inverse,rd,wr,need=[H[k] for k in ['mm','rank','inverse','rd','wr','need']];mul=H['ALG']['MUL']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=HERE/'output');args=ap.parse_args()
 for f,d in rd(HERE/'SOURCE-PINS.json')['files'].items():need(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==d,'source pin '+f)
 old=BASE/'bit-simultaneous-d1509-s032/output';author=BASE/'bit-source-d-tangent-s032';dw=rd(old/'D-WORD.json.gz');gg=rd(old/'CONSTRAINED-GAUGES.json.gz');T=np.array(dw['matrix'],dtype=np.uint8);owners=dw['owners'];L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];donors=sorted(map(int,gg['gauges']))
 layout=rd(BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=np.array(layout['root_table']);adj=[set(np.flatnonzero(z==0).tolist()) for z in roots@roots.T];planes=[set(z) for z in layout['A2']];charts=[set(z) for z in layout['D4']]
 ins={j:[i for i,z in enumerate(owners) if z[3] is not None and j in planes[z[3]]] for j in charts[1509]};receivers=[r for r in range(120) if charts[1509]<=adj[r]];outs={r:[i for i,z in enumerate(owners) if z[5] is not None and r in planes[z[5]]] for r in receivers}
 systems=rd(BASE/'bit-source-d-interpolation-s032-independent/output/RECONSTRUCTED-MATRICES.json.gz');cert=rd(author/'CERTIFICATE.json.gz')
 for j in donors:
  for r in R:
   stacked=np.vstack([np.array(z['target_maps'][str(r)],dtype=np.uint8) for key,z in systems.items() if int(key.split('/')[0])==j]);need(stacked.shape==(24,8) and rank(stacked)==8,'four parent maps detect every D ingress direction')
 allowed=[(q,p) for q in range(35) for p in range(35) if q>=19 or p<19];visible=sorted({(q,p) for j in donors for r in R for q in outs[r] for p in ins[j] if q>=19 or p<19});vi={qp:i for i,qp in enumerate(visible)}
 need(cert['visible_variables']==[list(x) for x in visible],'independent phase-legal visible coordinates');ci={(j,r):inverse(T[np.ix_(outs[r],ins[j])]) for j in donors for r in R};blocks=[];raw=0
 for key,z in systems.items():
  j,h=map(int,key.split('/'));C=np.array(z['native_H_span'],dtype=np.uint8);N=np.array(z['relations'],dtype=np.uint8);k=N.shape[1];raw+=6*k
  if not k:continue
  block=np.zeros((6*k,len(visible)),dtype=np.uint8)
  for t,r in enumerate(R):
   left=mm(np.array(z['target_maps'][str(r)],dtype=np.uint8),ci[j,r]);right=mm(ci[j,r],N[C.shape[1]+8*t:C.shape[1]+8*t+8])
   for a,q in enumerate(outs[r]):
    for b,p in enumerate(ins[j]):
     index=vi.get((q,p))
     if index is not None:block[:,index]^=mul[left[:,a,None],right[b,None,:]].reshape(-1)
  blocks.append(block[np.any(block,axis=1)])
 A=np.vstack(blocks);N=np.array(cert['visible_tangent_basis'],dtype=np.uint8);AA=np.array(cert['constraint_matrix'],dtype=np.uint8)
 need(rank(A)==88 and N.shape==(561,473) and rank(N)==473 and not np.any(mm(A,N)),'complete independently reconstructed visible tangent');need(rank(np.vstack([A,AA]))==88,'author operator has identical row space');need(len(allowed)==921 and len(visible)==561 and len(allowed)-rank(A)==833,'full phase-legal tangent dimensions')
 cand=cert['candidate'];delta=np.array(cand['delta_D'],dtype=np.uint8);S=np.array(cand['D_matrix'],dtype=np.uint8);need(np.array_equal(S,T^delta) and np.count_nonzero(delta)==1 and delta[0,0]==1 and rank(delta)==1,'literal finite D lift');need(not np.any(S[:19,19:]) and rank(S[:19,:19])==19 and rank(S[19:,19:])==16,'finite lift phase ranks')
 vec=np.array([delta[q,p] for q,p in visible],dtype=np.uint8)[:,None];need(not np.any(mm(A,vec)) and np.array_equal(vec[:,0],N[:,0]),'saved finite lift comes from verified tangent basis')
 finite_inverse={(j,r):inverse(S[np.ix_(outs[r],ins[j])]) for j in donors for r in R};changed=[];nil2=True
 for key,z in systems.items():
  j,h=map(int,key.split('/'));F=np.array(z['source'],dtype=np.uint8);C=np.array(z['native_H_span'],dtype=np.uint8);X=np.hstack([C,L]);D=np.array(cand['source_protected_delta'][key],dtype=np.uint8);need(D.shape==(6,96),'protected source delta dimensions');target=np.hstack([mm(F,C)]+[mm(np.array(z['target_maps'][str(r)],dtype=np.uint8),finite_inverse[j,r]) for r in R]);need(np.array_equal(mm(F^D,X),target),'all44 exact finite source equations');need(not np.any(mm(D,C)),'literal native H preservation')
  if np.any(D):changed.append(key)
 for j in donors:
  for r in R:
   rel=mm(delta[np.ix_(outs[r],ins[j])],ci[j,r]);nil2 &= not np.any(mm(rel,rel))
 need(not nil2,'exact inversion required; nilpotence shortcut unavailable');failures=[]
 for j in sorted(ins):
  for r in receivers:
   rr=rank(S[np.ix_(outs[r],ins[j])])
   if rr!=8:failures.append({'donor':j,'receiver':r,'rank':rr})
 K=np.array(rd(BASE/'bit-d1509-coupled-repair-s032-independent/output/FULL-COLLISION-CERTIFICATE.json.gz')['forced_space'],dtype=np.uint8);rows=H['ALG']['echelon'](L.T)[1];W=mm(inverse(L[rows]),K[rows]);need(np.array_equal(mm(L,W),K),'independent fixed K coordinates');BK={}
 for j in donors:
  P=np.zeros((35,32),dtype=np.uint8);P[ins[j]]=np.hstack([finite_inverse[j,r] for r in R]);BK[j]=mm(P,W)
 Z=np.hstack([BK[j]^BK[61] for j in donors if j!=61]);contrast=rank(Z);aug=rank(np.hstack([Z,BK[61]]));need(contrast==30 and aug==32,'local lift retains common-response rank two')
 result={'status':'PASS_INDEPENDENT_FULL_TANGENT_AND_EXACT_LOCAL_LIFT','phase_legal_variables':921,'visible_variables':561,'invisible_coordinate_dimension':360,'independent_raw_equations':raw,'independent_nonzero_equations':len(A),'constraint_rank':88,'visible_tangent_dimension':473,'full_D_tangent_dimension':833,'exact_candidate_nonzero_D_entries':[[0,0,1]],'exact_local_systems_checked':44,'changed_source_quotients':changed,'retained_D_sections_checked':44,'phase_ranks':[19,16],'nilpotence_shortcut_applicable':False,'all_geometric_section_failures':failures,'full_collision_contrast_rank':contrast,'full_collision_augmented_rank':aug,'full_collision_common_response_rank':aug-contrast,'new_author_executable_imports':False,'source_view_ranks_checked':False,'source_phase_word_compiled':False,'complete_fifth_receiver':False,'new_kappa':False}
 wr(args.out/'RESULT.json',result);wr(args.out/'INDEPENDENT-TANGENT-MATRIX.json.gz',{'visible_variables':visible,'matrix':A.tolist()});print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
