"""Independent normalized-readout receiver74 column obstruction.
@CubeJerry; substantial OpenAI assistance. Apache-2.0. No new kappa.
"""
from pathlib import Path
import argparse,importlib.util,hashlib,numpy as np

def main(repo,out):
 root=repo/'research/moonshot-005-program/results';arith=root/'bit-coupled-source-validity-s033/physical-three-receiver-gate/check.py';sp=importlib.util.spec_from_file_location('rebase74_field',arith);f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
 four=root/'bit-simultaneous-d1509-s032/output';files=[root/'bit-coupled-fifth-s033/other-receivers/output/CERTIFICATE.json.gz',root/'bit-coupled-fifth-review-s033/alternative-receiver-screen/output/RESULT.json',root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',four/'D-WORD.json.gz',four/'SOURCES.json.gz',four/'H-PHYSICAL.json.gz',root/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz',root/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'];cert,prior,z,dw,src,physical,fib,layout=map(f.read,files);cert=next(v for v in cert if v['target']==74 and v['anchor']==0);T=np.array(dw['matrix'],dtype=np.uint8);L=np.array(z['common_frames'],dtype=np.uint8);W=np.array(cert['L_coordinates'],dtype=np.uint8);R=z['retained_receivers'];roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];planes=[set(v)for v in layout['A2']];charts=[set(v)for v in layout['D4']];prot=list(range(48))+list(range(240,288));I0=z['D_inputs']['0'];I38=z['D_inputs']['38'];parents=[h for h in sorted(map(int,src['paired_maps']['0']))if planes[h]<=charts[1509]];f.need(len(parents)==4 and all(c in I0 for c in[4,5,19])and 19 in I38,'minimal input columns and all four parents')
 def solve(A,B):
  rr,p=f.rr(np.hstack([A,B]));f.need(all(q<A.shape[1]for q in p),'exact column containment');X=np.zeros((A.shape[1],B.shape[1]),dtype=np.uint8)
  for i,q in enumerate(p):X[q]=rr[i,A.shape[1]:]
  f.need(np.array_equal(f.mm(A,X),B),'exact coefficient certificate');return X
 blocks=[];C_labels=[];Lc=np.hstack([L[:,:8],L[:,24:32]])
 for h in sorted(map(int,src['paired_maps']['38'])):
  if not planes[h]<=charts[1509]:continue
  q=physical[str(h)];xs,ys=q['X_owners'],q['Y_owners'];Q=np.array(src['frames'][f'38/{h}'],dtype=np.uint8);xx=[i for i,x in enumerate(xs)if x[1]==38];yy=[i for i,x in enumerate(ys)if x[6]==38];X=np.zeros((len(xs),30),dtype=np.uint8);Y=np.zeros((len(ys),30),dtype=np.uint8);X[xx]=Q[:len(xx)];Y[yy]=Q[len(xx):];E=np.array(q['early'],dtype=np.uint8);B=np.array(q['late'],dtype=np.uint8).reshape(len(ys),len(ys));G=np.array(q['cross'],dtype=np.uint8).reshape(len(ys),len(xs));full=np.vstack([f.mm(E,X),f.mm(G,X)^f.mm(B,Y)]);owners=xs+ys;F=np.array(src['paired_maps']['38'][str(h)],dtype=np.uint8)[:,prot];chosen=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[74]and x[4]!=1509];blocks.append(f.mm(full[chosen],f.mm(F,Lc)));C_labels +=[owners[i][:3]for i in chosen]
 C=np.vstack(blocks);f.need(C.shape==(112,16)and f.rank(C)==12 and f.rank(C[:,:8])==f.rank(C[:,8:])==6,'donor38 direct-sum block kernels')
 observations={};physical_parents={}
 for h in sorted(h for h in map(int,src['paired_maps']['0'])if planes[h]<=adj[74]):
  cols=[];labels=[]
  for rs,data in sorted(fib['263'].items(),key=lambda x:int(x[0])):
   rr=int(rs)
   if rr>=111 or not planes[h]<=adj[rr]:continue
   a=np.array(data['kernel'],dtype=np.uint8)[:48,:3];zero=np.zeros_like(a);cols.append(np.block([[a,zero],[zero,a]]));labels.extend([['H',263,rr,k]for k in range(6)])
  H=np.hstack(cols);F=np.array(src['paired_maps']['0'][str(h)],dtype=np.uint8)[:,prot]
  if h!=263:f.need(not np.any(f.mm(F,H)),'noncentral full30 native-H values are zero')
  observations[h]=(H,labels,F);q=physical[str(h)];xs,ys=q['X_owners'],q['Y_owners'];Q=np.array(src['frames'][f'0/{h}'],dtype=np.uint8);xx=[i for i,x in enumerate(xs)if x[1]==0];yy=[i for i,x in enumerate(ys)if x[6]==0];f.need(Q.shape==(30,30)and f.rank(Q)==30 and len(xx)+len(yy)==30,'full source phase normalization');X=np.zeros((len(xs),30),dtype=np.uint8);Y=np.zeros((len(ys),30),dtype=np.uint8);X[xx]=Q[:len(xx)];Y[yy]=Q[len(xx):];E=np.array(q['early'],dtype=np.uint8);B=np.array(q['late'],dtype=np.uint8).reshape(len(ys),len(ys));G=np.array(q['cross'],dtype=np.uint8).reshape(len(ys),len(xs));full=np.vstack([f.mm(E,X),f.mm(G,X)^f.mm(B,Y)]);physical_parents[h]=(full,xs+ys)
 Ktarget=np.array(cert['K'],dtype=np.uint8);f.need(np.array_equal(f.mm(L,W),Ktarget)and f.rank(Ktarget)==2 and not np.any(W[8:24]),'actual forced74 two-space supported6/73');anchor=[];anchor_ingress=np.zeros((35,2),dtype=np.uint8);inputlabels={tuple(dw['owners'][p][:3]):p for p in I0}
 for h,(H,labels,F)in observations.items():
  coef=solve(H,Ktarget);full,owners=physical_parents[h];values=f.mm(full,f.mm(F,Ktarget));off=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[74]and x[4]!=1509];f.need(not np.any(values[off]),'all actual source0 off74 outputs on K vanish')
  for i,x in enumerate(owners):
   label=tuple(x[:3])
   if label in inputlabels:anchor_ingress[inputlabels[label]]=values[i]
  anchor.append({'H':h,'native_H_labels':labels,'K_coefficients':coef.tolist()})
 f.need(len(anchor)==16 and f.rank(anchor_ingress)==2,'sixteen H-only source0 anchor decompositions and injective ingress')
 records=[]
 for block,r in enumerate([6,73]):
  O=z['D_outputs'][str(r)];wr=W[8*R.index(r):8*R.index(r)+8];B=T[np.ix_(O,[4,5])];coef=solve(B,wr);f.need(f.rank(B)==f.rank(coef)==2,'W equals fixed two-column image');X=f.mm(L[:,8*R.index(r):8*R.index(r)+8],B);Dingress=np.zeros((35,2),dtype=np.uint8);parts=[];labels0={tuple(dw['owners'][p][:3]):p for p in I0}
  for h in parents:
   H,labels,F=observations[h];coeff=solve(H,X);full,owners=physical_parents[h];values=f.mm(full,f.mm(F,X));chosen=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[r]];f.need(full[chosen].shape==(30,30)and f.rank(full[chosen])==30,'full30 source0 retained H section');f.need(not np.any(values[[i for i in chosen if owners[i][4]!=1509]]),'old whole retained H outputs on core pair')
   for i,x in enumerate(owners):
    label=tuple(x[:3])
    if label in labels0:Dingress[labels0[label]]=values[i]
   parts.append({'H':h,'native_H_labels':labels,'coefficients':coeff.tolist(),'old_full30_core_image':f.mm(F,X).tolist()})
  expected=np.zeros((35,2),dtype=np.uint8);expected[[4,5]]=np.eye(2,dtype=np.uint8);f.need(np.array_equal(Dingress,expected),'all four parents give exactly input flags4,5')
  U=f.null(C[:,8*block:8*block+8]);S=T[np.ix_(O,I38)];V=solve(S,U);e=np.zeros((8,1),dtype=np.uint8);e[I38.index(19),0]=1;ec=solve(V,e);records.append({'receiver':r,'outputs':O,'old_fixed_columns':B.tolist(),'W_coordinates':coef.tolist(),'source0_H_core_decompositions':parts,'source0_physical_ingress':Dingress.tolist(),'donor38_block_kernel':U.tolist(),'donor38_old_input_kernel':V.tolist(),'local_e19':e.tolist(),'e19_in_input_kernel':ec.tolist()})
 result={'status':'PASS_REBASED_RECEIVER74_COLUMN_OBSTRUCTION','anchor_source':0,'tight_donor':38,'active_receivers':[6,73],'source0_parents':parents,'source0_input_columns':I0,'minimal_dependent_columns':[4,5,19],'source0_normalized_section_rank_upper':7,'native_H_core_decompositions':8,'H_only_forced_K_quotients':16,'all_four_parent_ingress_identity':True,'common_invertible_D_readout_rebases_covered':True,'fixed_literal_H_actions_required':True,'literal_D_rectangle_required':False,'D_phase_zero_pattern_used':False,'affine833_family_required':False,'arbitrary_full480_source_maps_covered':True,'new_complete_kappa':False};out.mkdir(parents=True,exist_ok=True);f.save(out/'RESULT.json',result);f.save(out/'CERTIFICATE.json.gz',{'receiver_witnesses':records,'donor38_parent_matrix':C.tolist(),'donor38_parent_labels':C_labels,'source0_forced_K_H_decompositions':anchor,'source0_forced_K_ingress':anchor_ingress.tolist()});pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files+[arith]};f.save(out/'SOURCE-PINS.json',pins);print(result['status'],parents,[(x['receiver'],x['W_coordinates'],x['e19_in_input_kernel'])for x in records],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
