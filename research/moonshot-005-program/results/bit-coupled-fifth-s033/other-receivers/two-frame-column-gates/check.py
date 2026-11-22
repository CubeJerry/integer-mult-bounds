"""Exact normalized column-dependence gates for two-frame target receivers."""
from pathlib import Path
import argparse,importlib.util,json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('s033_screen',HERE.parent/'screen.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
mm,rank,inverse,solve,read,save,need,null=s.mm,s.rank,s.inverse,s.solve,s.read,s.save,s.need,s.null
BASE=s.BASE

def main(repo,out):
 for p,h in read(HERE/'SOURCE-PINS.json').items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 z=read(repo/BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');R=z['retained_receivers'];I={int(j):v for j,v in z['D_inputs'].items()};O={int(j):v for j,v in z['D_outputs'].items()};old=np.array(read(repo/BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz')['matrix'],dtype=np.uint8);cert=read(HERE.parent/'output/CERTIFICATE.json.gz');E=[4,5];result=[]
 for target in[54,74,87]:
  rec=next(v for v in cert if v['target']==target);W=np.array(rec['L_coordinates'],dtype=np.uint8);active=[r for k,r in enumerate(R)if np.any(W[8*k:8*k+8])];need(len(active)==2,'two supported frames');witness=[];allkernels={r:[]for r in active}
  for gate in rec['donor_gates']:
   j=gate['donor'];M=np.array(gate['off_matrix'],dtype=np.uint8)
   if gate['kernel_dimension']!=4:continue
   for b,r in enumerate(active):
    wr=W[8*R.index(r):8*R.index(r)+8];need(rank(wr)==2 and rank(np.hstack([wr,old[np.ix_(O[r],E)]]))==2,'fixed two-column profile');U=null(M[:,8*b:8*b+8]);need(U.shape[1]==2,'tight block kernel');V=mm(inverse(old[np.ix_(O[r],I[j])]),U);embedded=np.zeros((35,2),dtype=np.uint8);embedded[I[j]]=V;allkernels[r].append(embedded)
    for q,p in enumerate(I[j]):
     if p in E:continue
     e=np.eye(8,dtype=np.uint8)[:,q:q+1]
     if rank(np.hstack([V,e]))>2:continue
     containing=[k for k,ii in I.items()if set(E+[p])<=set(ii)]
     if containing:witness.append({'tight_donor':j,'receiver':r,'forced_profile_columns':E,'dependent_column':p,'violated_section_donors':containing,'off_matrix':M.tolist(),'block_kernel':U.tolist(),'old_input_kernel':V.tolist(),'unit_kernel_coefficients':solve(V,e).tolist(),'W_block':wr.tolist(),'W_profile_factor':solve(old[np.ix_(O[r],E)],wr).tolist()})
  unions=[]
  for r in active:
   B=s.basis(np.hstack([np.eye(35,dtype=np.uint8)[:,E]]+allkernels[r]));dims={j:s.meet(B,np.eye(35,dtype=np.uint8)[:,ii]).shape[1]for j,ii in I.items()};unions.append({'receiver':r,'forced_input_span':B.tolist(),'span_dimension':B.shape[1],'native_section_intersection_dimensions':dims})
  if witness:
   zz=witness[0];VV=np.array(zz['old_input_kernel'],dtype=np.uint8);cc=np.array(zz['unit_kernel_coefficients'],dtype=np.uint8);bad=cc.copy();bad[0,0]^=1;need(not np.array_equal(mm(VV,cc),mm(VV,bad)),'unit-kernel coefficient corruption rejected')
  need(bool(witness)==(target in[54,74]),'precise closure census');need(target!=87 or all(v['span_dimension']==8 and set(v['native_section_intersection_dimensions'].values())=={2}for v in unions),'receiver87 exact surviving profile census');result.append({'target':target,'active_receivers':active,'witnesses':witness,'input_union_gates':unions});print('TARGET',target,'column witnesses',len(witness),flush=True)
 layout=read(repo/BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];planes=[set(v)for v in layout['A2']];charts=[set(v)for v in layout['D4']];hf=read(repo/BASE/'bit-simultaneous-d1509-s032-independent/output/H-FIBRES.json.gz')['0'];source=read(repo/BASE/'bit-simultaneous-d1509-s032/output/SOURCES.json.gz');L=np.array(z['common_frames'],dtype=np.uint8);parents=[int(h)for h in source['paired_maps']['0']if planes[int(h)]<=charts[1509]];need(len(parents)==4,'source0 four D parents');normal=[]
 for r in R:
  X=mm(L[:,8*R.index(r):8*R.index(r)+8],old[np.ix_(O[r],E)])
  for h in parents:
   C=np.hstack([np.array(v,dtype=np.uint8)for key,v in hf.items()if int(key.split('/')[1])<111 and planes[h]<=adj[int(key.split('/')[1])]]);coeff=solve(C,X);need(np.array_equal(mm(C,coeff),X),'H-only normalized columns');normal.append({'receiver':r,'parent':h,'profile_frame':X.tolist(),'H_generators':C.tolist(),'coefficients':coeff.tolist()})
 out.mkdir(parents=True,exist_ok=True);save(out/'CERTIFICATE.json.gz',{'target_gates':result,'normalized_fixed_column_H_decompositions':normal});save(out/'RESULT.json',{'status':'EXACT_COLUMN_DEPENDENCE_OBSTRUCTIONS','excluded_targets':[54,74],'unexcluded_by_this_test':[87],'witness_counts':{x['target']:len(x['witnesses'])for x in result},'arbitrary_common_receiver_readout_rebasing':True,'phase_or_shared_row_constraints_used':False,'normalization_uses_fixed_H_and_retained_frames':True,'new_complete_kappa':False})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
