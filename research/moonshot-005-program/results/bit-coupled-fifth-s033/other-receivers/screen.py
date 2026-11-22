"""Exact forced-space and parent off-receiver projection screen. No new kappa.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib,itertools
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('s033_alg',HERE.parent/'check.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
mm,rank,inverse,solve,read,save,need,rref=[getattr(a,k)for k in['mm','rank','inverse','solve','read','save','need','rref']];BASE=Path('research/moonshot-005-program/results')
def basis(A):return A[:,rref(A)[1]]
def null(A):
 rr,p=rref(A);free=[q for q in range(A.shape[1])if q not in p];N=np.zeros((A.shape[1],len(free)),dtype=np.uint8);N[free]=np.eye(len(free),dtype=np.uint8)
 for i,q in enumerate(p):N[q]=rr[i,free]
 need(not np.any(mm(A,N)),'nullspace');return N
def meet(A,B):
 N=null(np.hstack([A,B]));return basis(mm(A,N[:A.shape[1]]))
def main(repo,out):
 for p,h in read(HERE/'SOURCE-PINS.json').items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 z=read(repo/BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');L=np.array(z['common_frames'],dtype=np.uint8);R=z['retained_receivers'];J=z['donors'];I={int(j):v for j,v in z['D_inputs'].items()};O={int(r):v for r,v in z['D_outputs'].items()}
 four=repo/BASE/'bit-simultaneous-d1509-s032/output';source=read(four/'SOURCES.json.gz');proper=read(four/'PROPER.json.gz');gg=read(four/'CONSTRAINED-GAUGES.json.gz');frames=read(four/'FRAMES.json.gz');dw=read(four/'D-WORD.json.gz');hp=read(four/'H-PHYSICAL.json.gz');T=np.array(dw['matrix'],dtype=np.uint8);G={j:np.array(gg['gauges'][str(j)],dtype=np.uint8)for j in J};GI={j:inverse(v)for j,v in G.items()};hf=read(repo/BASE/'bit-simultaneous-d1509-s032-independent/output/H-FIBRES.json.gz')
 layout=read(repo/BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];planes=[set(v)for v in layout['A2']];charts=[set(v)for v in layout['D4']]
 candidates=[r for r in range(111)if charts[1509]<=adj[r]and r not in R];need(candidates==[52,54,74,85,87,95,98],'all native fifth receivers')
 parents={j:{int(h)for h in source['paired_maps'][str(j)]if planes[int(h)]<=charts[1509]}for j in J};Hby={tuple(v[:3]):int(h)for h,d in hp.items()for name in['X_owners','Y_owners']for v in d[name]};C={}
 for j in J:
  for hs in source['paired_maps'][str(j)]:
   h=int(hs);cols=[np.array(v,dtype=np.uint8)for key,v in hf.get(str(j),{}).items()if int(key.split('/')[1])<111 and planes[h]<=adj[int(key.split('/')[1])]];C[j,h]=basis(np.hstack(cols))if cols else np.zeros((96,0),dtype=np.uint8)
 parent_fixed={}
 for j in J:
  special=[p for p in[4,5,7,8]if p in I[j]];X=np.zeros((32,4*len(special)),dtype=np.uint8)
  for t,r in enumerate(R):X[8*t:8*t+8,t*len(special):(t+1)*len(special)]=T[np.ix_(O[r],special)]
  parent_fixed[j]=mm(L,X)
  for h in parents[j]:need(rank(np.hstack([C[j,h],parent_fixed[j]]))==rank(C[j,h]),'parent fixed subspace')
 cache={}
 for target in candidates+[6]:
  for j in J:
   d=proper[str(j)][str(target)];labels=[tuple(v)for v in d['labels']];ins={tuple(dw['owners'][p][:3])for p in I[j]};off=[q for q,x in enumerate(labels)if Hby[x]in parents[j]and x not in ins];A=mm(np.array(d['matrix'],dtype=np.uint8),G[j]);cache[j,target]=(mm(A[off],L),off,labels,A)
 records=[];witnesses=[];anchors=[0,45,61,62,100]
 for target in candidates+[6]:
  for anchor in anchors:
   U=mm(GI[anchor],np.array(frames[str(anchor)][str(target)],dtype=np.uint8));K=meet(U,parent_fixed[anchor]);initial=K.shape[1];constraints=[]
   for hs in source['paired_maps'][str(anchor)]:
    h=int(hs)
    if not planes[h]<=adj[target]:continue
    parts=[C[anchor,h]]
    if h not in parents[anchor]:
     Ffull=np.array(source['paired_maps'][str(anchor)][str(h)],dtype=np.uint8)[:,list(range(48))+list(range(240,288))]
     for t,r in enumerate(R):
      if planes[h]<=adj[r]:need(not np.any(mm(Ffull,L[:,8*t:8*t+8])),'full thirty-row nonparent retained image zero')
     parts +=[L[:,8*t:8*t+8]for t,r in enumerate(R)if planes[h]<=adj[r]]
    X=basis(np.hstack(parts));K=meet(K,X);constraints.append((h,X))
   record={'target':target,'anchor':anchor,'initial_parent_fixed_fibre_dimension':initial,'forced_dimension':K.shape[1]}
   if not K.shape[1]:record['status']='no_nonzero_forced_space_in_this_reduction';records.append(record);continue
   labels=cache[anchor,target][2];oldY=mm(cache[anchor,target][3],K);ing=[labels.index(tuple(dw['owners'][p][:3]))for p in I[anchor]];offall=[q for q in range(len(labels))if q not in ing];need(not np.any(oldY[offall])and rank(oldY[ing])==K.shape[1],'old anchor fibre isolation')
   W=solve(L,K);active=[t for t in range(4)if np.any(W[8*t:8*t+8])];indices=sum([list(range(8*t,8*t+8))for t in active],[]);ks=[];bad=[]
   for j in J:
    M=cache[j,target][0][:,indices];N=null(M);projections=[]
    for size in range(1,len(active)+1):
     for sub in itertools.combinations(range(len(active)),size):
      ns=sum([list(range(8*t,8*t+8))for t in sub],[]);ws=sum([list(range(8*active[t],8*active[t]+8))for t in sub],[]);required=rank(W[ws]);available=rank(N[ns]);projections.append({'receiver_blocks':[R[active[t]]for t in sub],'required_rank':required,'available_rank':available})
      if required>available:bad.append({'donor':j,'subset':[R[active[t]]for t in sub],'required':required,'available':available,'defect':required-available})
    ks.append({'donor':j,'off_matrix':M.tolist(),'kernel':N.tolist(),'kernel_dimension':N.shape[1],'projections':projections})
   record.update(status='universal_parent_off_obstruction'if bad else'projection_gate_does_not_exclude',active_receivers=[R[t]for t in active],blocked_donors=sorted({v['donor']for v in bad}),largest_projection_defect=max([v['defect']for v in bad]or[0]));records.append(record)
   witnesses.append({'target':target,'anchor':anchor,'K':K.tolist(),'L_coordinates':W.tolist(),'forced_decompositions':[{'H':h,'generators':X.tolist(),'coefficients':solve(X,K).tolist()}for h,X in constraints],'donor_gates':ks,'obstructions':bad})
   print(record,flush=True)
 joined={t:rank(np.hstack([np.array(v['K'],dtype=np.uint8)for v in witnesses if v['target']==t]))for t in candidates+[6]}
 need(all(joined[t]==(4 if t in[95,6]else 2)for t in joined),'joined anchor census')
 need(all(not v['blocked_donors']for v in records if v['target']==6 and v['forced_dimension']),'retained receiver positive control')
 v=next(v for v in witnesses if v['target']==6);j=v['anchor'];labels=cache[j,6][2];badrows=[q for q,x in enumerate(labels)if Hby[x]in parents[j]];badM=mm(cache[j,6][3][badrows],L[:,:8]);badN=null(badM);need(len(v['K'][0])>0 and badN.shape[1]==0,'misclassifying D ingress as off output is rejected');controls={'retained6_survives':True,'all_D_ingress_wrongly_marked_off_rejected':True,'bad_partition_kernel_dimension':badN.shape[1]}
 out.mkdir(parents=True,exist_ok=True);save(out/'CERTIFICATE.json.gz',witnesses);save(out/'RESULT.json',{'status':'EXACT_OTHER_RECEIVER_FORCED_SPACE_SCREEN','retained_receivers':R,'fifth_candidates':candidates,'records':records,'positive_control_receiver':6,'joined_anchor_dimensions':joined,'controls':controls,'new_complete_kappa':False});print('DONE',len(records),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
