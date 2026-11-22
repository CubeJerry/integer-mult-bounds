"""Check full retained H and D fibres for the S033 t=26 specialization."""
from pathlib import Path
import argparse,importlib.util,json,gzip
import numpy as np

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def check(repo,candidate,out):
 here=Path(__file__).parent;b=mod(here/'check.py','s033_source');g,a,olds,olde,src,cc,changes=b.load(repo,candidate);base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032';read=b.read
 ph=read(four/'output/H-PHYSICAL.json.gz');dw=read(four/'output/D-WORD.json.gz');T=np.array(cc['D_matrix'],dtype=np.uint8);owners=dw['owners'];L=np.array(olds['simultaneous_original_space'],dtype=np.uint8)[b.PROT];fib=read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');marked=set(read(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D']);Hrecords=[];Hbad=[]
 for h0,rr in fib.items():
  for r,z in rr.items():
   K=np.array(z['kernel'],dtype=np.uint8);Z=np.zeros_like(K);K2=np.block([[K,Z],[Z,K]]);bad=[]
   for j,mm in src.items():
    if j not in a.planes[int(h0)]:continue
    for h,F in mm.items():
     if h==int(h0) or a.planes[h]<=a.adj[int(r)]:
      delta=F^np.array(olds['paired_maps'][str(j)][str(h)],dtype=np.uint8)
      if np.any(a.mm(delta,K2)):bad.append([j,h])
   Hrecords.append({'H':int(h0),'receiver':int(r),'native':int(r)<111,'all_source_observations_identical':not bad})
   if bad:Hbad.append({'H':int(h0),'receiver':int(r),'native':int(r)<111,'changed_observations':bad})
 print('H_INTERFACES',len(Hrecords),'bad',Hbad,flush=True)
 Drecords=[];fullrecords=[];inputindices={j:[q for q,x in enumerate(owners)if x[3]is not None and j in a.planes[x[3]]]for j in src};outputindices={r:[q for q,x in enumerate(owners)if x[5]is not None and r in a.planes[x[5]]]for r in range(120)if a.charts[1509]<=a.adj[r]}
 ingress={}
 for j,mm in sorted(src.items()):
  rows=[];P=np.zeros((35,96),dtype=np.uint8)
  for h,F in mm.items():
   Q=np.array(olds['frames'][f'{j}/{h}'],dtype=np.uint8);z=ph[str(h)];xs=z['X_owners'];ys=z['Y_owners'];E=np.array(z['early'],dtype=np.uint8);B=np.array(z['late'],dtype=np.uint8);G=np.array(z['cross'],dtype=np.uint8).reshape(len(ys),len(xs));XE=np.zeros((len(xs),30),dtype=np.uint8);YL=np.zeros((len(ys),30),dtype=np.uint8)
   xx=[q for q,x in enumerate(xs)if x[1]==j];yy=[q for q,x in enumerate(ys)if x[6]==j];XE[xx]=Q[:len(xx)];YL[yy]=Q[len(xx):]
   RX=a.mm(a.mm(E,XE),F[:,b.PROT]);RY=a.mm(a.mm(G,XE)^a.mm(B,YL),F[:,b.PROT])if len(ys)else np.zeros((0,96),dtype=np.uint8)
   for os,M in [(xs,RX),(ys,RY)]:
    for x,v in zip(os,M):
     if x[4]in marked:rows.append((h,x,v))
     if x[4]==1509:P[[tuple(y[:3])for y in owners].index(tuple(x[:3]))]=v
  ingress[j]=P.tolist()
  for r,oi in sorted(outputindices.items()):
   visible=[(x,v)for h,x,v in rows if a.planes[h]<=a.adj[r]and a.charts[x[4]]<=a.adj[r]];A=np.array([v for x,v in visible],dtype=np.uint8);rk=a.rank(A);need(A.shape==(96,96)and rk==96,f'complete proper restriction {j}/{r}')
   fullrecords.append([j,r,rk])
   if r not in [6,9,48,73]:continue
   ii=inputindices[j];C=T[np.ix_(oi,ii)];need(a.rank(C)==8,'D retained section');target=np.zeros((96,8),dtype=np.uint8);Ci=g.inverse(C,a);labels=[tuple(x[:3])for x,v in visible]
   for q,p in enumerate(ii):target[labels.index(tuple(owners[p][:3]))]=Ci[q]
   U=L[:,8*[6,9,48,73].index(r):8*([6,9,48,73].index(r)+1)];need(np.array_equal(a.mm(A,U),target),f'proper isolation and entire fibre {j}/{r}');need(np.array_equal(a.mm(a.mm(T[oi],P),U),np.eye(8,dtype=np.uint8)),f'physical identity readout {j}/{r}')
   Drecords.append([j,r,96,8])
  print('D_INTERFACES',j,12,4,flush=True)
 phase=[a.rank(T[:19,:19]),a.rank(T[19:,19:])];need(phase==[19,16]and not np.any(T[:19,19:]),'phase legal and invertible')
 section=[]
 for j in sorted(a.charts[1509]):
  ii=[q for q,x in enumerate(owners)if x[3]is not None and j in a.planes[x[3]]]
  for r,oi in sorted(outputindices.items()):
   rk=a.rank(T[np.ix_(oi,ii)]);need(rk==8,'geometric D section');section.append([j,r,rk])
 need(not any(x['native']for x in Hbad),'every retained native H fibre unchanged')
 result={'status':'PASS_COUPLED_SOURCE_H_D_INTERFACES_T26','H_observation_records':Hrecords,'geometric_H_observation_changes':Hbad,'retained_native_H_interfaces':sum(x['native']for x in Hrecords),'retained_geometric_H_interfaces':sum(x['all_source_observations_identical']for x in Hrecords),'all_proper_left_restrictions':fullrecords,'whole_D_identity_readouts':Drecords,'phase_ranks':phase,'D_sections':section,'full_supplier':False,'new_complete_kappa':False};out.mkdir(parents=True,exist_ok=True);(out/'INTERFACE-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(out/'INGRESS.json.gz').write_bytes(gzip.compress((json.dumps(ingress,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0));print(result['status'],len(Hrecords),len(Hbad),len(Drecords),len(section),flush=True)
 return result

def need(v,msg):
 if not v:raise ValueError(msg)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();check(q.repo.resolve(),q.candidate.resolve(),q.out.resolve())
