"""A forced collision under arbitrary linear source-only quotient changes."""
from pathlib import Path
import importlib.util,json,numpy as np
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';prev=base/'bit-simultaneous-d1509-s032';here=Path(__file__).parent
s=importlib.util.spec_from_file_location('s032_solve',prev/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
g,a,ff,Ks,C=m.common_data(repo);gg=m.ex.read(prev/'output/CONSTRAINED-GAUGES.json.gz');src=m.ex.read(prev/'output/SOURCES.json.gz');fib=m.ex.read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];target=95;prot=list(range(48))+list(range(240,288));pr=[0,1,2,15,16,17]
def constraints(j,h):
 vs=[];labels=[]
 for center,rr in fib.items():
  if j not in a.planes[int(center)]:continue
  for receiver,z in rr.items():
   if int(receiver)>=111:continue
   if int(center)!=h and not a.planes[h]<=a.adj[int(receiver)]:continue
   K0=np.array(z['kernel'],dtype=np.uint8)[:48,:3];Z0=np.zeros_like(K0);vs.append(np.block([[K0,Z0],[Z0,K0]]));labels.append(['H',int(center),int(receiver)])
 for r in R:
  if a.planes[h]<=a.adj[r]:vs.append(L[:,8*R.index(r):8*R.index(r)+8]);labels.append(['D',1509,r])
 return (m.basis(np.hstack(vs),g,a) if vs else np.zeros((96,0),dtype=np.uint8)),labels
G61=np.array(gg['gauges']['61'],dtype=np.uint8);U61=a.mm(g.inverse(G61,a),ff[61][target]);N=m.null(np.hstack([L,U61]),g,a);K=a.mm(U61,N[32:]);assert K.shape==(96,4)and a.rank(K)==4
forced=[]
for h in a.by_donor[61]:
 if not a.planes[h]<=a.adj[target]:continue
 B,labels=constraints(61,h);assert a.rank(np.hstack([B,K]))==B.shape[1];forced.append({'H':h,'constraint_rank':B.shape[1],'sources':labels})
witnesses=[]
for j in sorted(ff):
 if j==61:continue
 for h in a.by_donor[j]:
  if not a.planes[h]<=a.adj[target]or a.planes[h]<=a.charts[1509]:continue
  B,labels=constraints(j,h);N=m.null(np.hstack([B,K]),g,a);V=a.mm(K,N[B.shape[1]:]);F=np.array(src['paired_maps'][str(j)][str(h)],dtype=np.uint8)[np.ix_(pr,prot)];bad=a.mm(F,V)
  if np.any(bad):
   q=int(np.flatnonzero(np.any(bad,axis=0))[0]);v=V[:,q];witnesses.append({'donor':j,'H':h,'constraint_rank':B.shape[1],'collision_intersection_rank':V.shape[1],'nonzero_image_rank':a.rank(bad),'vector':v.tolist(),'image':a.mm(F,v[:,None])[:,0].tolist(),'constraint_sources':labels})
print('FORCED',len(forced),'WITNESSES',len(witnesses),[(w['donor'],w['H'],w['collision_intersection_rank'],w['nonzero_image_rank'])for w in witnesses[:12]],flush=True)
res={'target_receiver':target,'D':1509,'retained_receivers':R,'forced_donor':61,'forced_collision':K.tolist(),'forced_all_visible_quotients':forced,'witnesses':witnesses};(here/'FORCED-COLLISION.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n')
proper=m.ex.read(prev/'output/PROPER.json.gz');readouts=m.ex.read(prev/'output/READOUTS.json.gz');dw=m.ex.read(prev/'output/D-WORD.json.gz');readout_values={}
for j in ff:
 rec=proper[str(j)][str(target)];A=np.array(rec['matrix'],dtype=np.uint8);labels=[tuple(x)for x in rec['labels']];Gj=np.array(gg['gauges'][str(j)],dtype=np.uint8);rd=readouts[str(j)][str(target)];indices=[labels.index(tuple(dw['owners'][p][:3]))for p in rd['D_inputs']];CC=np.array(rd['section'],dtype=np.uint8);readout_values[j]=a.mm(CC,a.mm(A[indices],a.mm(Gj,K)))
print('FIXED_D_READOUT_DIFFERENCES',[(j,a.rank(M^readout_values[61]))for j,M in readout_values.items()],flush=True)
res['forced_D_readouts']={j:M.tolist()for j,M in readout_values.items()};res['D_readout_difference_ranks']={j:a.rank(M^readout_values[61])for j,M in readout_values.items()};(here/'FORCED-COLLISION.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n')

def raw_constraints(j,h):
 vs=[];labels=[]
 for center,rr in fib.items():
  if j not in a.planes[int(center)]:continue
  for receiver,z in rr.items():
   if int(receiver)>=111:continue
   if int(center)!=h and not a.planes[h]<=a.adj[int(receiver)]:continue
   K0=np.array(z['kernel'],dtype=np.uint8)[:48,:3];Z0=np.zeros_like(K0);vs.append(np.block([[K0,Z0],[Z0,K0]]));labels.extend([['H',int(center),int(receiver),q]for q in range(6)])
 for r in R:
  if a.planes[h]<=a.adj[r]:vs.append(L[:,8*R.index(r):8*R.index(r)+8]);labels.extend([['D',1509,r,q]for q in range(8)])
 return np.hstack(vs),labels

def solve(B,v):
 _,p=g.rref(B,a);Q=B[:,p];_,rs=g.rref(Q.T,a);x=np.zeros(B.shape[1],dtype=np.uint8);x[p]=a.mm(g.inverse(Q[rs],a),v[rs,None])[:,0];assert np.array_equal(a.mm(B,x[:,None])[:,0],v);return[[q,int(t)]for q,t in enumerate(x)if t]
q=int(np.flatnonzero(np.any(readout_values[0]^readout_values[61],axis=0))[0]);v=K[:,q];cert={'receiver':95,'D':1509,'forced_donor':61,'contradicting_donor':0,'vector':v.tolist(),'four_frame_coefficients':solve(L,v),'quotient_decompositions':[]}
for item in forced:
 h=item['H'];B,labels=raw_constraints(61,h);cert['quotient_decompositions'].append({'H':h,'generator_labels':labels,'coefficients':solve(B,v)})
cert['actual_readout_donor61']=readout_values[61][:,q].tolist();cert['actual_readout_donor0']=readout_values[0][:,q].tolist();cert['difference']=(readout_values[61][:,q]^readout_values[0][:,q]).tolist();cert['scope']='arbitrary linear source quotient edits preserving the literal whole H263/H642 and four D1509 fibre/readout interfaces, with physical H/D phase words and source frames fixed'
(here/'WITNESS.json').write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n');print('VECTOR',q,'READOUT61',cert['actual_readout_donor61'],'READOUT0',cert['actual_readout_donor0'],'DIFF',cert['difference'],flush=True)
