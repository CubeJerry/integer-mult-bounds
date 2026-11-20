from pathlib import Path
from collections import defaultdict
import importlib.util,gzip,json,numpy as np
from argparse import ArgumentParser
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results';oldpath=base/'bit-shared-h-s031-construction/native-d1509-cut'
if (Path(__file__).parent/'SOURCE-PINS.json').exists():
 import hashlib
 for p,d in json.loads((Path(__file__).parent/'SOURCE-PINS.json').read_text()).items():
  if hashlib.sha256((repo/p).read_bytes()).hexdigest()!=d:raise ValueError('pin '+p)
s=importlib.util.spec_from_file_location('g',base/'bit-coupled-native-geometric-h-source/component/construction.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);family,a,previous=g.context(repo)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def block(ms):
 X=np.zeros((sum(M.shape[0]for M in ms),sum(M.shape[1]for M in ms)),dtype=np.uint8);r=c=0
 for M in ms:X[r:r+len(M),c:c+M.shape[1]]=M;r+=len(M);c+=M.shape[1]
 return X
def basis(M):
 _,p=g.rref(M,a);return M[:,p]
def complete(M):return basis(np.hstack([M,np.eye(len(M),dtype=np.uint8)]))
routes=[json.loads(x)for x in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()];HX=defaultdict(list);HY=defaultdict(list);Xj=defaultdict(list);Yj=defaultdict(list);key=lambda x:(x[1],x[2])
for x in routes:
 if x[3]is None:continue
 (HX if x[0]=='X'else HY)[x[3]].append(x)
 if x[0]=='X':Xj[x[1],x[3]].append(x)
 elif x[6]is not None:Yj[x[6],x[3]].append(x)
for d in [HX,HY,Xj,Yj]:
 for k in d:d[k].sort(key=key)
physical={int(h):v for h,v in read(oldpath/'output/H-PHYSICAL.json.gz').items()};src=read(oldpath/'output/SOURCES.json.gz');old_early=read(oldpath/'output/EARLY.json.gz');dw=read(oldpath/'output/D-WORD.json.gz');T=np.array(dw['matrix'],dtype=np.uint8);D=1509;i=6;downers=dw['owners'];di={(x[0],x[1],x[2]):q for q,x in enumerate(downers)};outputs=dw['selected_output_indices'];LF=np.array(src['selected_original_space'],dtype=np.uint8);prot=list(range(48))+list(range(240,288));LL=LF[prot];nodes=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())['H_nodes'];marked=set(read(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D']);newdonors=[32,35,38,68,69,90];V={k:a.vandermonde(range(1,3*k+1),3*k)for k in[3,12]};DV={k:np.array([[g.power(p+1,c-1,a)if c%2 else 0 for c in range(3*k)]for p in range(3*k)],dtype=np.uint8)for k in[3,12]}
def generic_h(h):
 ds=sorted(a.planes[h]&a.native);xs=HX[h];ys=HY[h];xi={(x[1],x[2]):q for q,x in enumerate(xs)};yi={(x[1],x[2]):q for q,x in enumerate(ys)};E=np.zeros((len(xs),len(xs)),dtype=np.uint8);B=np.zeros((len(ys),len(ys)),dtype=np.uint8);G=np.zeros((len(ys),len(xs)),dtype=np.uint8);psall=[d for d,Q in enumerate(a.charts)if a.planes[h]<=Q];kind='double'if len(ds)==3 and len(xs)==90 else'single'if len(ds)==3 else'partial'
 def xc(j,k,copy=None):
  rr=Xj[j,h];loc=list(range(3))if k==3 else list(range(3,15))
  if copy is not None:loc=[q+15*copy for q in loc]
  elif len(rr)==30:loc+=[q+15 for q in loc]
  return[xi[rr[q][1],rr[q][2]]for q in loc]
 def yc(j,k):
  rr=Yj[j,h]if j is not None else[x for x in ys if x[6]is None];loc=(list(range(3))if k==3 else list(range(3,15)))if j is not None else(list(range(6))if k==3 else list(range(6,30)))
  return[yi[rr[q][1],rr[q][2]]for q in loc]
 for k in[3,12]:
  ps=[d for d in psall if(d in marked)==(k==3)]
  if kind=='double':
   for copy in range(2):
    cols=sum([xc(j,k,copy)for j in ds],[])
    for q,d in enumerate(ps):rr=sorted([x for x in xs if x[4]==d],key=key);E[xi[rr[copy][1],rr[copy][2]],cols]=V[k][q]
  else:
   if kind=='single':xe=sum([xc(j,k)for j in ds],[]);yl=sum([yc(j,k)for j in ds],[]);PG=np.zeros_like(V[k])
   else:
    large=next(j for j in ds if a.quota[j,h]==30);small=next(j for j in ds if a.quota[j,h]==15);xe=xc(large,k)+xc(small,k);yl=yc(small,k)+yc(None,k);PG=DV[k].copy();PG[:,2*k:]=0
   for q,d in enumerate(ps):xr=next(x for x in xs if x[4]==d);yr=next(x for x in ys if x[4]==d);rx=xi[xr[1],xr[2]];ry=yi[yr[1],yr[2]];E[rx,xe]=V[k][q];B[ry,yl]=V[k][q];G[ry,xe]=PG[q]
 assert a.rank(E)==len(E)and(not len(B)or a.rank(B)==len(B));return{'kind':kind,'X_owners':xs,'Y_owners':ys,'early':E.tolist(),'late':B.tolist(),'cross':G.tolist(),'ports':psall}
for j in newdonors:
 for h in a.by_donor[j]:
  if h not in physical:physical[h]=generic_h(h)
print('ALL_NATIVE_PHYSICAL_H',len(physical),flush=True)
def local_transfer(j,h,Q):
 z=physical[h];xs=z['X_owners'];ys=z['Y_owners'];E=np.array(z['early'],dtype=np.uint8);B=np.array(z['late'],dtype=np.uint8);G=np.array(z['cross'],dtype=np.uint8);xi={(x[1],x[2]):q for q,x in enumerate(xs)};yi={(x[1],x[2]):q for q,x in enumerate(ys)};XE=np.zeros((len(xs),30),dtype=np.uint8);YL=np.zeros((len(ys),30),dtype=np.uint8);quota=len(Xj[j,h])
 for t,x in enumerate(Xj[j,h]):XE[xi[x[1],x[2]]]=Q[t]
 for t,x in enumerate(Yj[j,h]):YL[yi[x[1],x[2]]]=Q[quota+t]
 return a.mm(E,XE),a.mm(G,XE)^a.mm(B,YL)if len(B)else np.zeros((0,30),dtype=np.uint8)
paired={int(j):{int(h):block([np.array(M,dtype=np.uint8),np.array(M,dtype=np.uint8)])for h,M in vv.items()}for j,vv in src['maps'].items()};frames={tuple(map(int,k.split('/'))):np.array(M,dtype=np.uint8)for k,M in src['frames'].items()};early={int(j):v for j,v in old_early.items()};late={int(j):{int(h):np.array(M,dtype=np.uint8).reshape(-1,480)for h,M in vv.items()}for j,vv in src['late_parities'].items()};gauges={};receipts=[];new_local=0
for j in newdonors:
 hs=sorted(a.by_donor[j]);full=[h for h in hs if a.quota[j,h]==30];half=[h for h in hs if a.quota[j,h]==15];assert len(full)==4 and len(half)==24 and len(set(nodes[h]for h in hs))==28
 baseM={};baseQ={};transfer={};rows=[];labels=[];scalar_inv={};views={}
 for h in hs:
  F=block([np.kron(a.vandermonde([nodes[h]],16),np.eye(k,dtype=np.uint8))for k in[3,12]]);baseM[h]=block([F,F]);Q=np.eye(30,dtype=np.uint8)
  if h in half[12:]:Q=np.block([[np.zeros((15,15),dtype=np.uint8),np.eye(15,dtype=np.uint8)],[np.eye(15,dtype=np.uint8),np.zeros((15,15),dtype=np.uint8)]])
  baseQ[h]=Q;RX,RY=local_transfer(j,h,Q);transfer[h]=(RX,RY)
  for ii in range(120):
   if not a.planes[h]<=a.adj[ii]:continue
   xx=[q for q,x in enumerate(HX[h])if a.charts[x[4]]<=a.adj[ii]];yy=[q for q,x in enumerate(HY[h])if a.charts[x[4]]<=a.adj[ii]];assert a.rank(np.vstack([RX[xx],RY[yy]]))==30;new_local+=1
  if a.planes[h]<=a.adj[i]:
   for ph,os,R in [('X',HX[h],RX),('Y',HY[h],RY)]:
    A=a.mm(R,baseM[h][:,prot])
    for q,x in enumerate(os):
     if x[4]in marked and a.charts[x[4]]<=a.adj[i]:rows.append(A[q]);labels.append((ph,x[1],x[2]))
 A=np.array(rows,dtype=np.uint8);assert A.shape==(96,96)and a.rank(A)==96
 inn=[q for q,x in enumerate(downers)if x[3]is not None and j in a.planes[x[3]]];C=T[np.ix_(outputs,inn)];Cinv=g.inverse(C,a);target=np.zeros((96,8),dtype=np.uint8)
 for q,p in enumerate(inn):x=downers[p];target[labels.index((x[0],x[1],x[2]))]=Cinv[q]
 U=a.mm(g.inverse(A,a),target);G96=a.mm(complete(U),g.inverse(complete(LL),a));assert a.rank(G96)==96 and np.array_equal(a.mm(G96,LL),U)
 GG=np.eye(480,dtype=np.uint8);GG[np.ix_(prot,prot)]=G96;paired[j]={h:a.mm(M,GG)for h,M in baseM.items()};Ephys=np.zeros((480,480),dtype=np.uint8);Erows=[];owners=[];late[j]={}
 for h in hs:
  Q=baseQ[h];frames[j,h]=Q;R=a.mm(Q,paired[j][h]);quota=a.quota[j,h]
  for q,x in enumerate(Xj[j,h]):Ephys[x[2]]=R[q]
  Erows.extend(R[:quota]);owners.extend([[h,x[2]]for x in Xj[j,h]]);late[j][h]=R[quota:]
 assert a.rank(Ephys)==480;early[j]={'matrix':np.array(Erows,dtype=np.uint8).tolist(),'physical_matrix':Ephys.tolist(),'row_owners':owners}
 for ii in sorted(a.adj[j]):
  vv=[h for h in hs if a.planes[h]<=a.adj[ii]];assert len(vv)==16 and a.rank(np.vstack([paired[j][h]for h in vv]))==480;views[ii]=vv;scalar_inv[ii]=g.inverse(a.vandermonde([nodes[h]for h in vv],16),a)
 mx=0
 for h in hs:
  for q in hs:
   if h==q:continue
   P=np.hstack([scalar_inv[ii][:,vv.index(h):vv.index(h)+1]for ii,vv in views.items()if h in vv and q in vv]);rank=a.rank(P);assert rank==5;mx=max(mx,rank)
 gauges[j]={'protected96':G96.tolist(),'source_frame_first_early_half':half[:12],'base_H_nodes':{str(h):nodes[h]for h in hs},'base_D_inverse_fibre':U.tolist(),'base_proper_left':A.tolist(),'base_proper_left_owner_labels':[list(x)for x in labels],'D_section':C.tolist()};receipts.append({'donor':j,'geometric_source_views':63,'native_source_views':len(a.adj[j]&a.native),'early_rank':480,'geometric_scalar_propagation_maximum':mx,'paired_full_propagation_bound':150,'gauge_rank':96});print('EXTENDED_NATIVE_D_DONOR',j,63,480,150,flush=True)
all_donors=sorted(paired);assert all_donors==sorted(a.charts[D]&a.native);M=np.zeros((35,8*len(all_donors)),dtype=np.uint8)
for t,j in enumerate(all_donors):
 for h in a.by_donor[j]:
  if not a.planes[h]<=a.adj[i]:continue
  RX,RY=local_transfer(j,h,frames[j,h]);state=a.mm(paired[j][h],LF)
  for ph,os,R in [('X',HX[h],RX),('Y',HY[h],RY)]:
   vals=a.mm(R,state)
   for q,x in enumerate(os):
    if x[4]==D:M[di[ph,x[1],x[2]],8*t:8*t+8]=vals[q]
    elif a.charts[x[4]]<=a.adj[i]:assert not np.any(vals[q])
assert np.array_equal(a.mm(T[outputs],M),np.tile(np.eye(8,dtype=np.uint8),(1,11)));print('ALL_ELEVEN_NATIVE_D_IDENTITY',M.shape,len(physical),5040+new_local,flush=True)
out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
def save(name,v):
 z=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();(out/name).write_bytes(gzip.compress(z,mtime=0))
save('SOURCES.json.gz',{'paired_maps':{str(j):{str(h):A.tolist()for h,A in vv.items()}for j,vv in paired.items()},'frames':{f'{j}/{h}':Q.tolist()for(j,h),Q in frames.items()},'late_parities':{str(j):{str(h):A.tolist()for h,A in vv.items()}for j,vv in late.items()},'selected_original_space':LF.tolist()});save('EARLY.json.gz',early);save('H-PHYSICAL.json.gz',physical);dw['ingress']=M.tolist();dw['supplied_donors']=all_donors;save('D-WORD.json.gz',dw);save('GAUGES.json.gz',gauges);(out/'RESULT.json').write_text(json.dumps({'status':'PASS_ALL_ELEVEN_NATIVE_D1509_CUT_EXTENSION','supplied_donors':all_donors,'new_donors':receipts,'geometric_source_views':693,'native_source_views':sum(len(a.adj[j]&a.native)for j in all_donors),'paired_source_width':30,'paired_source_bank':480,'paired_uniform_propagation_by_donor':{str(j):150 if j in newdonors else 444 for j in all_donors},'paired_saturation_threshold':450,'physical_H_modules':len(physical),'H_section_checks':5040+new_local,'D_phase_word_unchanged':True,'H642_paid_fields_unchanged':16,'other_D_common_cuts':False,'complete_global_supplier':False,'new_complete_kappa':False},sort_keys=True,indent=2)+'\n')

print('PASS_ALL_ELEVEN_NATIVE_D1509_CUT_EXTENSION',693,sum(len(a.adj[j]&a.native)for j in all_donors),280,11088,11,8,flush=True)
