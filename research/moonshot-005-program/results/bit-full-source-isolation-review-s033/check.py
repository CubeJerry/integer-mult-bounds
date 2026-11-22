"""Independent full30 H-section and H-only forced-K review.

Uses the separate physical-gate GF64 arithmetic, without importing either
new obstruction/forced-K constructor. @CubeJerry, OpenAI assistance, Apache-2.0.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib,numpy as np
HERE=Path(__file__).resolve().parent

def main(repo,out):
 root=repo/'research/moonshot-005-program/results';arith=root/'bit-coupled-source-validity-s033/physical-three-receiver-gate/check.py';sp=importlib.util.spec_from_file_location('full_source_independent_field',arith);f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
 four=root/'bit-simultaneous-d1509-s032/output';files=[four/'H-PHYSICAL.json.gz',four/'SOURCES.json.gz',four/'D-WORD.json.gz',four/'PROPER.json.gz',four/'CONSTRAINED-GAUGES.json.gz',root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',root/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',root/'bit-coupled-fifth-review-s033/wave3/isolation-output/CERTIFICATE.json',root/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz']
 physical,src,dw,proper,gauges,z,layout,cert,fib=map(f.read,files);roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];charts=[set(v)for v in layout['D4']];planes=[set(v)for v in layout['A2']];prot=list(range(48))+list(range(240,288));L=np.array(z['common_frames'],dtype=np.uint8);W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8);K=f.mm(L,W);f.need(not np.any(W[:16])and f.rank(W[16:24])==f.rank(W[24:])==4,'rank-four 48/73 coordinate blocks')
 def inv(A):
  n=len(A);R,p=f.rr(np.hstack([A,np.eye(n,dtype=np.uint8)]));f.need(np.array_equal(R[:,:n],np.eye(n,dtype=np.uint8)),'inverse');return R[:,n:]
 j=32;parents=[h for h in sorted(map(int,src['paired_maps']['32']))if planes[h]<=charts[1509]];fullblocks=[];section_records=[]
 for h in parents:
  q=physical[str(h)];xs,ys=q['X_owners'],q['Y_owners'];Q=np.array(src['frames'][f'{j}/{h}'],dtype=np.uint8);f.need(Q.shape==(30,30)and f.rank(Q)==30,'invertible full source phase normalization');xx=[i for i,x in enumerate(xs)if x[1]==j];yy=[i for i,x in enumerate(ys)if x[6]==j];X=np.zeros((len(xs),30),dtype=np.uint8);Y=np.zeros((len(ys),30),dtype=np.uint8);X[xx]=Q[:len(xx)];Y[yy]=Q[len(xx):];E=np.array(q['early'],dtype=np.uint8);B=np.array(q['late'],dtype=np.uint8);G=np.array(q['cross'],dtype=np.uint8).reshape(len(ys),len(xs));full=np.vstack([f.mm(E,X),f.mm(G,X)^f.mm(B,Y)]);owners=xs+ys;F=np.array(src['paired_maps']['32'][str(h)],dtype=np.uint8)[:,prot]
  for r,k in[(48,2),(73,3)]:
   chosen=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[r]];A=full[chosen];f.need(A.shape==(30,30)and f.rank(A)==30,'complete actual H donor section invertible');section_records.append({'H':h,'receiver':r,'rank':30,'rows':[owners[i][:3]for i in chosen]})
   # All retained-frame observations except D1509 are zero, independently
   # of the chosen later D section or its invertible readout rebasing.
   values=f.mm(A,f.mm(F,L[:,8*k:8*k+8]));off=[q0 for q0,i in enumerate(chosen)if owners[i][4]!=1509];f.need(not np.any(values[off]),'old full30 off-D retained-frame values zero')
   inputs=[tuple(dw['owners'][i][:3])for i in z['D_inputs']['32']];insert=np.zeros((30,8),dtype=np.uint8)
   for a,i in enumerate(chosen):
    label=tuple(owners[i][:3])
    if label in inputs:insert[a,inputs.index(label)]=1
   section=np.array(dw['matrix'],dtype=np.uint8)[np.ix_(z['D_outputs'][str(r)],z['D_inputs']['32'])];f.need(f.rank(section)==8 and np.array_equal(f.mm(values,section),insert),'full30 B F L S = exact D-input insertion')
   section_records[-1]['full_isolation_identity']=True
  chosen95=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[95]and x[4]!=1509];block=f.mm(full[chosen95],f.mm(F,L[:,16:32]));fullblocks.append(block)
 C=np.vstack(fullblocks);N=f.null(C);f.need(C.shape==(112,16)and f.rank(C)==12 and N.shape==(16,4)and f.rank(N[:8])==f.rank(N[8:])==2,'full112-row projected kernel obstruction')
 # Directly verify all16 H-only decompositions in full source coordinates.
 forced=[]
 for item in cert['source61_H_only_decompositions']:
  h=item['H'];cols=[];central=0;F=np.array(src['paired_maps']['61'][str(h)],dtype=np.uint8)[:,prot]
  for kind,center,r,q in item['generator_labels']:
   f.need(kind=='H'and r<111 and center in[263,642]and(h==center or planes[h]<=adj[r]),'literal native H observation incidence')
   A=np.array(fib[str(center)][str(r)]['kernel'],dtype=np.uint8)[:48,:3];zero=np.zeros_like(A);col=np.block([[A,zero],[zero,A]])[:,q];cols.append(col)
   if h!=center:f.need(not np.any(f.mm(F,col[:,None])),'noncentral whole-H observation is zero')
   else:central+=1
  X=np.column_stack(cols);coeff=np.array(item['K_coefficients'],dtype=np.uint8);f.need(np.array_equal(f.mm(X,coeff),K),'H-only full forced K decomposition');forced.append({'H':h,'H_only_span_rank':f.rank(X),'central_observation_columns':central,'old_full30_K_image_rank':f.rank(f.mm(F,K))})
 f.need(sorted(x['H']for x in forced)==sorted(h for h in map(int,src['paired_maps']['61'])if planes[h]<=adj[95]),'all sixteen geometrically visible source61 quotients')
 oldA=f.mm(np.array(proper['61']['95']['matrix'],dtype=np.uint8),np.array(gauges['gauges']['61'],dtype=np.uint8));labels=[tuple(x)for x in proper['61']['95']['labels']];ii=[labels.index(tuple(dw['owners'][q][:3]))for q in z['D_inputs']['61']];off=[q for q in range(96)if q not in ii];f.need(not np.any(f.mm(oldA[off],K))and f.rank(f.mm(oldA[ii],K))==4,'old genuine isolated rank-four ingress')
 # Kernel-rank implication control: a full-rank first block cannot fit in
 # the kernel whose first projection has rank two.
 f.need(not np.any(f.mm(C,N))and f.rank(N[:8])==2,'exact projected kernel control')
 result={'status':'PASS_INDEPENDENT_FULL_SOURCE_FIXED_H_ISOLATION_REVIEW','full30_sections':section_records,'full_parent_off95_matrix_shape':list(C.shape),'full_parent_off95_rank':12,'kernel_dimension':4,'kernel_projection_ranks':[2,2],'forced_K_coordinate_block_ranks':[4,4],'H_only_forced_source61_quotients':forced,'arbitrary_full480_source_maps_covered':True,'arbitrary_invertible_retained_D_readout_rebasings_covered':True,'literal_H_interface_values_required_for_forced_K':True,'space_only_H_readout_gauges_admitted':False,'new_complete_kappa':False};out.mkdir(parents=True,exist_ok=True);f.save(out/'RESULT.json',result);f.save(out/'CERTIFICATE.json.gz',{'full_parent_off95_matrix':C.tolist(),'kernel':N.tolist(),'forced_K':K.tolist()});reviewed=[root/'bit-coupled-fifth-review-s033/wave3/ISOLATION-GATE.md',root/'bit-coupled-fifth-review-s033/wave3/isolation_gate.py',root/'bit-coupled-fifth-s033/wave3/FORCED-K.md'];pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files+[arith]+reviewed};f.save(out/'SOURCE-PINS.json',pins);print(result['status'],8,C.shape,16,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
