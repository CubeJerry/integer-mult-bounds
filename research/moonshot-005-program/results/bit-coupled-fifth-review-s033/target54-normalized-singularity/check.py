#!/usr/bin/env python3
"""Independent normalized receiver54 singularity certificate. No new kappa."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_gf64',HERE.parent/'check.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

def main(repo,out):
 B=repo/'research/moonshot-005-program/results';four=B/'bit-simultaneous-d1509-s032/output'
 paths=[B/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',four/'D-WORD.json.gz',four/'PROPER.json.gz',four/'CONSTRAINED-GAUGES.json.gz',four/'H-PHYSICAL.json.gz',B/'bit-coupled-fifth-s033/other-receivers/output/CERTIFICATE.json.gz',HERE.parent/'alternative-receiver-screen/SOURCE-PINS.json',HERE.parent/'check.py']
 z,dw,proper,gauges,hp,screen,priorpins=map(a.read,paths[:-1])
 for name,digest in priorpins.items():a.need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'accepted screen source pin')
 L=np.array(z['common_frames'],dtype=np.uint8);T=np.array(dw['matrix'],dtype=np.uint8)
 witness=next(x for x in screen if x['target']==54 and x['anchor']==0)
 W=np.array(witness['L_coordinates'],dtype=np.uint8);K=np.array(witness['K'],dtype=np.uint8)
 a.need(a.rank(K)==2 and np.array_equal(a.mm(L,W),K),'reviewed forced two-space')
 a.need(not np.any(W[:8]) and not np.any(W[24:]),'only blocks9 and48 active')
 Hby={tuple(x[:3]):int(h) for h,p in hp.items() for typ in ['X_owners','Y_owners'] for x in p[typ]}
 parents={int(key.split('/')[1]) for key in z['systems'] if key.startswith('32/')}
 labels=list(map(tuple,proper['32']['54']['labels']));inputs={tuple(dw['owners'][q][:3]) for q in z['D_inputs']['32']}
 ix=[i for i,label in enumerate(labels) if Hby[label] in parents and label not in inputs]
 Aold=a.mm(np.array(proper['32']['54']['matrix'],dtype=np.uint8),np.array(gauges['gauges']['32'],dtype=np.uint8))
 M=a.mm(Aold[ix],L[:,8:24]);N=a.null(M)
 a.need(M.shape==(16,16) and N.shape[1]==4,'tight donor32 joint kernel')
 kernels=[a.null(M[:,8*b:8*b+8]) for b in range(2)]
 a.need(all(U.shape==(8,2) for U in kernels),'two separate two-dimensional kernels')
 a.need(a.rank(np.block([[kernels[0],np.zeros((8,2),dtype=np.uint8)],[np.zeros((8,2),dtype=np.uint8),kernels[1]]]))==4,'joint kernel is direct sum')
 results=[];cert=[]
 for b,r in enumerate([9,48]):
  O=z['D_outputs'][str(r)];I32=z['D_inputs']['32'];I0=z['D_inputs']['0']
  Wr=W[8*(b+1):8*(b+2)];U=kernels[b];Sold=T[np.ix_(O,I32)];V=a.mm(a.inverse(Sold),U)
  e=np.zeros((8,1),dtype=np.uint8);e[I32.index(22),0]=1
  n=a.solve(V,e);a.need(np.array_equal(a.mm(V,n),e),'global22 belongs to necessary kernel input space')
  F=T[np.ix_(O,[4,5])];D=a.solve(F,Wr)
  a.need(a.rank(F)==2 and a.rank(D)==2,'W equals pinned columns4,5 span')
  physical_pins=a.mm(L[:,8*(b+1):8*(b+2)],F);pin_coefficients=[]
  for key,system in z['systems'].items():
   if not key.startswith('0/'):continue
   C=np.array(system['H_observation_core'],dtype=np.uint8)
   pin_coefficients.append(dict(system=key,coefficients=a.solve(C,physical_pins).tolist()))
  a.need(len(pin_coefficients)==4,'all donor0 parents fix the two physical pin inputs')
  item0=proper['0'][str(r)];labels0=list(map(tuple,item0['labels']))
  Aphys0=a.mm(np.array(item0['matrix'],dtype=np.uint8),np.array(gauges['gauges']['0'],dtype=np.uint8))
  E0=np.zeros((96,2),dtype=np.uint8)
  for q,p in enumerate([4,5]):E0[labels0.index(tuple(dw['owners'][p][:3])),q]=1
  a.need(np.array_equal(a.mm(Aphys0,physical_pins),E0),'fixed source action exposes literal D inputs4,5')
  Ann=a.null(Wr.T).T
  a.need(Ann.shape==(6,8) and not np.any(a.mm(Ann,Wr)),'exact annihilator of W')
  a.need({4,5,22}<=set(I0),'receiver0 contains dependent triple')
  early=[q for q,row in enumerate(O) if row<19]
  a.need(a.rank(Wr[early])==2 and 22>=19,'literal causal special case')
  # Independently set up the much larger per-receiver normalized relaxation:
  # only four pinned columns, no phase restrictions, no shared output rows.
  pinned=[4,5,7,8];free=[(q,p) for q in range(8) for p in range(35) if p not in pinned]
  index={v:i for i,v in enumerate(free)};A0=np.zeros((8,35),dtype=np.uint8);A0[:,pinned]=T[np.ix_(O,pinned)]
  eqs=[];rhs=[];tight=[]
  for gate in witness['donor_gates']:
   if gate['kernel_dimension']!=4:continue
   j=gate['donor'];tight.append(j);Mg=np.array(gate['off_matrix'],dtype=np.uint8)
   Ug=a.null(Mg[:,8*b:8*b+8]);Ig=z['D_inputs'][str(j)]
   Vg=a.mm(a.inverse(T[np.ix_(O,Ig)]),Ug)
   E=np.zeros((12,len(free)),dtype=np.uint8)
   for u in range(6):
    for v in range(2):
     for q in range(8):
      for p,col in enumerate(Ig):
       if (q,col) in index:E[2*u+v,index[q,col]]^=a.MUL[Ann[u,q],Vg[p,v]]
   eqs.append(E);rhs.append(a.mm(a.mm(Ann,A0[:,Ig]),Vg).reshape(-1))
  E=np.vstack(eqs);rhs=np.hstack(rhs)[:,None]
  a.need(a.rank(E)==a.rank(np.hstack([E,rhs])),'relaxed normalized affine consistency')
  xp=a.solve(E,rhs)[:,0];point=A0.copy()
  for (q,p),val in zip(free,xp):point[q,p]^=val
  a.need(not np.any(a.mm(Ann,point[:,22,None])),'normalized column22 belongs to W')
  a.need(a.rank(point[:,I0])<8,'normalized affine point has singular donor0 section')
  # Removing the required relation permits the old invertible section;
  # this catches an accidental conclusion from the pins alone.
  violation=a.mm(Ann,T[:,22][O,None])
  a.need(np.any(violation) and a.rank(T[np.ix_(O,I0)])==8,'old section violates required isolation relation')
  results.append(dict(receiver=r,pinned_span_rank=2,forced_column=22,singular_donor=0,universal_section_rank_upper_bound=7,normalized_free_entries=len(free),normalized_equation_rank=a.rank(E),normalized_family_dimension=len(free)-a.rank(E),tight_donors=tight))
  cert.append(dict(receiver=r,output_rows=O,donor32_inputs=I32,donor0_inputs=I0,off_block=M[:,8*b:8*b+8].tolist(),separate_kernel=U.tolist(),old_section=Sold.tolist(),input_kernel=V.tolist(),input22_coefficients=n.tolist(),W=Wr.tolist(),pinned_columns45=F.tolist(),W_in_pinned_columns=D.tolist(),pin_H_decompositions=pin_coefficients,ann_W=Ann.tolist(),relaxed_affine_point=point.tolist(),old_relation_violation=violation.tolist()))
 result=dict(status='PASS_INDEPENDENT_NORMALIZED_RECEIVER54_SINGULARITY',records=results,phase_constraints_used=False,shared_row_constraints_used=False,common_readout_rebasing_covered_under_normalized_pins=True,literal_phase_case_forces_zero_column=True,forced_two_space_inherited_from_pinned_review=True,new_complete_kappa=False)
 pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};expected=HERE/'SOURCE-PINS.json'
 if expected.exists():a.need(pins==a.read(expected),'source pins')
 out.mkdir(parents=True,exist_ok=True)
 for name,data in [('RESULT',result),('CERTIFICATE',cert),('SOURCE-PINS',pins)]:
  (out/(name+'.json')).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
