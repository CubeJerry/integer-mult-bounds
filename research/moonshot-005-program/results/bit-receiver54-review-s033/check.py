"""Independent receiver54 screen and literal physical candidate review.
@CubeJerry; substantial OpenAI assistance. Apache-2.0. No new kappa.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib,numpy as np

def main(repo,out,candidate):
 root=repo/'research/moonshot-005-program/results';arith=root/'bit-coupled-source-validity-s033/physical-three-receiver-gate/check.py';sp=importlib.util.spec_from_file_location('r54_independent_field',arith);f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
 four=root/'bit-simultaneous-d1509-s032/output';files=[four/'H-PHYSICAL.json.gz',four/'SOURCES.json.gz',four/'D-WORD.json.gz',four/'PROPER.json.gz',four/'CONSTRAINED-GAUGES.json.gz',root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',root/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',root/'bit-coupled-fifth-s033/other-receivers/output/CERTIFICATE.json.gz',root/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz']
 physical,src,dw,proper,gauges,z,layout,cert,fib=map(f.read,files);roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];charts=[set(v)for v in layout['D4']];planes=[set(v)for v in layout['A2']];prot=list(range(48))+list(range(240,288));prows=[0,1,2,15,16,17];L=np.array(z['common_frames'],dtype=np.uint8);J=z['donors'];R=z['retained_receivers'];T=np.array(dw['matrix'],dtype=np.uint8);witnesses=[v for v in cert if v['target']==54];K=np.array(witnesses[0]['K'],dtype=np.uint8);W=np.array(witnesses[0]['L_coordinates'],dtype=np.uint8)
 f.need(f.rank(K)==2 and np.array_equal(f.mm(L,W),K)and not np.any(W[np.r_[0:8,24:32]])and f.rank(W[8:16])==f.rank(W[16:24])==2,'forced two-space with active9/48 blocks')
 native=sorted(j for j in charts[1509]if j<111);f.need(native==J,'all eleven native D donors reconstructed geometrically')
 # D outputs are selected by the recorded dual-H flag in owner slot5.
 O54=[i for i,x in enumerate(dw['owners'])if x[5]is not None and 54 in planes[x[5]]];f.need(len(O54)==8,'actual eight D54 outputs')
 f.need(all([i for i,x in enumerate(dw['owners'])if x[5]is not None and r in planes[x[5]]]==z['D_outputs'][str(r)]for r in R),'D output incidence control')
 parents={j:[h for h in sorted(map(int,src['paired_maps'][str(j)]))if planes[h]<=charts[1509]]for j in J};cache={}
 def full(j,h):
  if(j,h)in cache:return cache[j,h]
  q=physical[str(h)];xs,ys=q['X_owners'],q['Y_owners'];Q=np.array(src['frames'][f'{j}/{h}'],dtype=np.uint8);xx=[i for i,x in enumerate(xs)if x[1]==j];yy=[i for i,x in enumerate(ys)if x[6]==j];f.need(Q.shape==(30,30)and len(xx)+len(yy)==30 and f.rank(Q)==30,'full source phase normalization');X=np.zeros((len(xs),30),dtype=np.uint8);Y=np.zeros((len(ys),30),dtype=np.uint8);X[xx]=Q[:len(xx)];Y[yy]=Q[len(xx):];E=np.array(q['early'],dtype=np.uint8);B=np.array(q['late'],dtype=np.uint8).reshape(len(ys),len(ys));G=np.array(q['cross'],dtype=np.uint8).reshape(len(ys),len(xs));A=np.vstack([f.mm(E,X),f.mm(G,X)^f.mm(B,Y)]);F=np.array(src['paired_maps'][str(j)][str(h)],dtype=np.uint8)[:,prot];cache[j,h]=(A,xs+ys,F);return cache[j,h]
 def solve(A,B):
  C,p=f.rr(np.hstack([A,B]));f.need(all(q<A.shape[1]for q in p),'span containment');X=np.zeros((A.shape[1],B.shape[1]),dtype=np.uint8)
  for i,q in enumerate(p):X[q]=C[i,A.shape[1]:]
  f.need(np.array_equal(f.mm(A,X),B),'exact span coefficients');return X
 def basis(A):return A[:,f.rr(A)[1]]
 # All eleven donors: replace marked sixteen rows by all actual parent rows.
 gates=[];gatecert={};full_section_count=0
 for j in J:
  blocks=[];labels=[];inputs=[tuple(dw['owners'][i][:3])for i in z['D_inputs'][str(j)]]
  for h in parents[j]:
   A,owners,F=full(j,h)
   for r,k in[(9,1),(48,2)]:
    chosen=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[r]];B=A[chosen];f.need(B.shape==(30,30)and f.rank(B)==30,'full30 retained H section');ins=np.zeros((30,8),dtype=np.uint8)
    for a,i in enumerate(chosen):
     label=tuple(owners[i][:3])
     if label in inputs:ins[a,inputs.index(label)]=1
    Sr=T[np.ix_(z['D_outputs'][str(r)],z['D_inputs'][str(j)])];f.need(np.array_equal(f.mm(f.mm(B,f.mm(F,L[:,8*k:8*k+8])),Sr),ins),'whole retained isolation B F L S = E');full_section_count+=1
   chosen=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[54]and x[4]!=1509];blocks.append(f.mm(A[chosen],f.mm(F,L[:,8:24])));labels +=[owners[i][:3]for i in chosen]
  C=np.vstack(blocks);N=f.null(C);profile=[f.rank(N[:8]),f.rank(N[8:]),f.rank(N)];f.need(C.shape==(112,16)and all(q>=2 for q in profile),'full parent54 projection gates permit required rank2');sup=next(x for x in witnesses[0]['donor_gates']if x['donor']==j);marked=np.array(sup['off_matrix'],dtype=np.uint8);f.need(f.rank(np.vstack([C,marked]))==f.rank(C)==f.rank(marked),'full and marked parent equation rowspaces agree');gates.append({'donor':j,'rows':112,'rank':f.rank(C),'kernel_dimension':N.shape[1],'block_ranks':[f.rank(C[:,:8]),f.rank(C[:,8:])],'kernel_is_direct_sum_of_block_kernels':f.rank(C)==f.rank(C[:,:8])+f.rank(C[:,8:]),'projection_ranks':profile,'required_ranks':[2,2,2]});gatecert[str(j)]={'off_labels':labels,'matrix':C.tolist(),'kernel':N.tolist()}
 # Independently rebuild H observations from earlier whole native fibres.
 anchors=[];anchorcert=[]
 for witness in witnesses:
  j=witness['anchor'];Kj=np.array(witness['K'],dtype=np.uint8);f.need(f.rank(np.hstack([K,Kj]))==2,'all anchors force same two-space');observations=[]
  for h in sorted(map(int,src['paired_maps'][str(j)])):
   if not planes[h]<=adj[54]:continue
   A,owners,F=full(j,h);cols=[];kinds=[]
   for center in[263,642]:
    if str(center)not in src['paired_maps'][str(j)]:continue
    for rs,data in sorted(fib[str(center)].items(),key=lambda x:int(x[0])):
     r=int(rs)
     if r>=111 or not planes[h]<=adj[r]:continue
     a=np.array(data['kernel'],dtype=np.uint8)[:48,:3];zero=np.zeros_like(a);B=np.block([[a,zero],[zero,a]]);cols.append(B);kinds +=[['H',center,r,q]for q in range(6)]
     if h!=center:f.need(not np.any(f.mm(F,B)),'noncentral whole H observation zero')
   H=np.hstack(cols)if cols else np.zeros((96,0),dtype=np.uint8);honly=f.rank(np.hstack([H,K]))==f.rank(H)
   if h not in parents[j]:
    for k,r in enumerate(R):
     if planes[h]<=adj[r]:
      B=L[:,8*k:8*k+8];f.need(not np.any(f.mm(F,B)),'nonparent retained D observation full30 zero');chosen=[i for i,x in enumerate(owners)if charts[x[4]]<=adj[r]];f.need(A[chosen].shape==(30,30)and f.rank(A[chosen])==30,'nonparent complete H section forces zero tuple');cols.append(B);kinds +=[['D',r,q]for q in range(8)]
   X=np.hstack(cols)if cols else np.zeros((96,0),dtype=np.uint8);coeff=solve(X,K);observations.append({'H':h,'generator_rank':f.rank(X),'H_only_suffices':honly,'old_full30_K_image_rank':f.rank(f.mm(F,K))});anchorcert.append({'anchor':j,'H':h,'labels':kinds,'coefficients':coeff.tolist(),'H_only_generator_count':H.shape[1],'H_only_coefficients':solve(H,K).tolist()if honly else None})
  f.need(len(observations)==16,'all anchor quotients visible54');old=np.zeros((0,2),dtype=np.uint8);ingress=np.zeros((35,2),dtype=np.uint8)
  for x in observations:
   A,owners,F=full(j,x['H']);values=f.mm(A,f.mm(F,K));off=[i for i,y in enumerate(owners)if charts[y[4]]<=adj[54]and y[4]!=1509];old=np.vstack([old,values[off]])
   for i,y in enumerate(owners):
    label=tuple(y[:3])
    for p in z['D_inputs'][str(j)]:
     if label==tuple(dw['owners'][p][:3]):ingress[p]=values[i]
  f.need(not np.any(old)and f.rank(ingress)==2,'old full actual54 isolated two-space anchor');anchors.append({'donor':j,'quotients':observations,'old_all_off54_rank':0,'old_ingress_rank':2})
 # Literal canonical candidate: no unverified whole-source extension is assumed.
 actual=None;candidate_evidence={}
 if candidate:
  c=f.read(candidate);newT=np.array(c['D_matrix'],dtype=np.uint8);images={};leaks=[]
  for j in J:
   P=np.zeros((35,2),dtype=np.uint8);offblocks=[];nonparentblocks=[];parentblocks=[];inlabels={tuple(dw['owners'][p][:3]):p for p in z['D_inputs'][str(j)]}
   for h in sorted(map(int,src['paired_maps'][str(j)])):
    if not planes[h]<=adj[54]:continue
    A,owners,F=full(j,h);F=F.copy();delta=c['source_protected_delta'].get(f'{j}/{h}')
    if delta is not None:F[prows]^=np.array(delta,dtype=np.uint8)
    values=f.mm(A,f.mm(F,K));off=[i for i,y in enumerate(owners)if charts[y[4]]<=adj[54]and y[4]!=1509];offblocks.append(values[off])
    if h in parents[j]:parentblocks.append(values[off])
    else:nonparentblocks.append(values[off])
    for i,y in enumerate(owners):
     label=tuple(y[:3])
     if label in inlabels:P[inlabels[label]]=values[i]
   images[j]=P;newparent=np.vstack(parentblocks);v=[]
   for r,k in[(9,1),(48,2)]:
    ii=z['D_inputs'][str(j)];oo=z['D_outputs'][str(r)];oldS=T[np.ix_(oo,ii)];newS=newT[np.ix_(oo,ii)];f.need(f.rank(newS)==8,'new section invertible');v.append(f.mm(oldS,solve(newS,W[8*k:8*k+8])))
   predicted=f.mm(np.array(gatecert[str(j)]['matrix'],dtype=np.uint8),np.vstack(v));f.need(np.array_equal(predicted,newparent),'candidate full parent leakage is forced by sections alone');candidate_evidence[str(j)]={'physical_ingress_on_K':P.tolist(),'parent_off54_on_K':newparent.tolist(),'section_forced_blocks':np.vstack(v).tolist()};leaks.append({'donor':j,'all_off54_rank':f.rank(np.vstack(offblocks)),'parent_off54_rank':f.rank(newparent),'nonparent_off54_rank':f.rank(np.vstack(nonparentblocks)),'off54_rows':sum(len(x)for x in offblocks),'section_forced_parent_response_verified':True})
  Z=np.hstack([images[j]^images[J[0]]for j in J[1:]]);responses={j:f.mm(newT[O54],images[j])for j in J};common=responses[J[0]];f.need(f.rank(common)==2 and all(np.array_equal(common,v)for v in responses.values()),'literal actual8-row54 common injective forced2 readout');actual={'candidate':str(candidate),'actual_outputs':O54,'forced_contrast_rank':f.rank(Z),'forced_augmented_rank':f.rank(np.hstack([Z,images[J[0]]])),'actual54_contrast_rank':f.rank(f.mm(newT[O54],Z)),'actual54_common_response_rank':f.rank(common),'common_response':common.tolist(),'full_physical_off54':leaks,'forced_two_space_isolated_at_all_donors':all(x['all_off54_rank']==0 for x in leaks),'complete_fifth_receiver':False,'whole_source_validity_checked':False,'whole_fibre_equality_checked':False};files.append(candidate)
 result={'status':'PASS_INDEPENDENT_RECEIVER54_NECESSARY_SCREEN','native_donors':J,'actual_D54_outputs':O54,'full30_parent_sections':full_section_count,'all_native_parent_projection_gates':gates,'source_anchor_forcing':anchors,'literal_candidate_review':actual,'new_complete_kappa':False};out.mkdir(parents=True,exist_ok=True);f.save(out/'RESULT.json',result);f.save(out/'CERTIFICATE.json.gz',{'K':K.tolist(),'L_coordinates':W.tolist(),'gates':gatecert,'forced_anchor_decompositions':anchorcert,'literal_candidate_physical_evidence':candidate_evidence});pins={str(p.relative_to(repo))if p.is_relative_to(repo)else str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in files+[arith,root/'bit-coupled-fifth-s033/other-receivers/screen.py']};f.save(out/'SOURCE-PINS.json',pins);print(result['status'],full_section_count,[(x['donor'],x['projection_ranks'])for x in gates],actual,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);p.add_argument('--candidate',type=Path);q=p.parse_args();main(q.repo.resolve(),q.out.resolve(),q.candidate.resolve()if q.candidate else None)
