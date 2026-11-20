#!/usr/bin/env python3
"""Exact native forced-kernel union and constrained core22 contraction lower bound."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);base=repo/'research/moonshot-005-program/results';here=Path(__file__).parent
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','contraction_geometry');family,a,previous=g.context(repo)
 pins=here/'SOURCE-PINS.json'
 if pins.exists():
  for p,d in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'source pin '+p)
 old=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
 raw=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz').read_bytes()))
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in raw['maps'].items()}
 nodes={int(j):{int(h):n for h,n in vv.items()} for j,vv in old['base_nodes'].items()};eye=np.eye(3,dtype=np.uint8)
 views={j:{i:sorted(h for h in a.by_donor[j] if a.planes[h]<=a.adj[i]) for i in sorted(a.adj[j])} for j in [0,61,45]}
 def basis(Z):
  _,p=g.rref(Z,a);return Z[:,p]
 def intersection(X,Y):
  N=previous.null_basis(np.hstack([X,Y]),a);return basis(a.mm(X,N[:X.shape[1]]))
 def fibres(mm,j,h):
  return {i:previous.null_basis(np.vstack([mm[j][q] for q in vv if q!=h]),a) for i,vv in views[j].items() if h in vv and i in a.native and i!=80}
 B=fibres(maps,61,642);C=fibres(maps,0,116);A=fibres(maps,0,263)
 need((len(A),len(B),len(C))==(33,34,32),'all ordinary native anchor views')
 def forced_spaces(BB,CC):
  forced={}
  for q in a.by_donor[45]:
   cols=[K for h,ff in [(642,BB),(116,CC)] for i,K in ff.items() if q!=h and a.planes[q]<=a.adj[i]]
   forced[q]=basis(np.hstack(cols)) if cols else np.zeros((48,0),dtype=np.uint8)
  return forced
 forced=forced_spaces(B,C);ann={q:previous.null_basis(Z.T,a).T for q,Z in forced.items()}
 kernels={i:previous.null_basis(np.vstack([ann[q] for q in vv]),a) for i,vv in views[45].items() if i in a.native}
 union=basis(np.hstack(list(kernels.values())));defects={i:K.shape[1] for i,K in kernels.items() if K.shape[1]}
 need(len(kernels)==59 and len(defects)==29 and set(defects.values())=={3} and union.shape==(48,15),'exact frozen native union census')
 for i,K in kernels.items():
  for q in views[45][i]:need(a.rank(np.hstack([forced[q],K]))==forced[q].shape[1],'view kernel lies in each forced quotient space')
 # Complete native common-readout system, with geometric H642 fibres retained.
 SA=basis(np.hstack(list(A.values())));Sb=basis(np.hstack(list(B.values())));U=basis(np.hstack([SA,Sb]))
 need((SA.shape[1],Sb.shape[1],U.shape[1])==(22,18,30),'native core ranks')
 _,rr=g.rref(U.T,a);Ui=g.inverse(U[rr],a);dim=U.shape[1]
 P=np.array(old['Hwords']['263'],dtype=np.uint8);ports=[110,132,720,810,1509,1735,1994,2621,2836]
 need(a.rank(P)==9,'fixed invertible H263 word');eq=[]
 for i,K in A.items():
  V=a.mm(Ui,K[rr]);vis=[q for q,D in enumerate(ports) if a.charts[D]<=a.adj[i]];need(len(vis)==3,'actual three visible marked ports')
  for q in vis:
   for j in [1,2]:
    for t in range(3):
     row=np.zeros((3,3,dim),dtype=np.uint8);row[0]=a.product[P[q,:3,None],V[None,:,t]];row[j]=a.product[P[q,3*j:3*j+3,None],V[None,:,t]];eq.append(row.reshape(-1))
 for i,K in B.items():
  if 263 not in views[61][i]:continue
  V=a.mm(Ui,K[rr])
  for u in range(3):
   for t in range(3):
    row=np.zeros((3,3,dim),dtype=np.uint8);row[1,u]=V[:,t];eq.append(row.reshape(-1))
 Eq=np.array(eq,dtype=np.uint8);N=previous.null_basis(Eq,a)
 need(Eq.shape==(765,270) and N.shape==(270,57) and not np.any(a.mm(Eq,N)),'complete native linear solution space')
 scalar=np.zeros((16,6),dtype=np.uint8)
 for c,d in enumerate([0,1,3,7,13,15]):scalar[d,c]=1
 scalar[4,4]=1;S0=np.kron(scalar,eye);Sc=a.mm(Ui,S0[rr]);need(np.array_equal(a.mm(U,Sc),S0),'old geometric core lies in U')
 image=np.column_stack([np.stack([a.mm(T,Sc) for T in N[:,n].reshape(3,3,dim)]).reshape(-1) for n in range(N.shape[1])]);expected=[]
 oldC=[np.array(old['maps'][str(j)]['263'],dtype=np.uint8) for j in [0,61,62]]
 for u in range(3):
  for v in range(3):
   M=np.zeros((3,3),dtype=np.uint8);M[u,v]=1;T=np.kron(np.eye(6,dtype=np.uint8),M)
   expected.append(np.stack([a.mm(a.mm(Cj,S0),T) for Cj in oldC]).reshape(-1))
 expected=np.stack(expected,axis=1)
 need((a.rank(image),a.rank(expected),a.rank(np.hstack([image,expected])))==(9,9,9),'one common amplitude matrix is the complete restriction normal form')
 witness_full=5;need(witness_full in A and 642 not in views[61][witness_full] and 116 not in views[0][witness_full],'native untouched comparison view')
 need(a.rank(a.mm(oldC[0],A[witness_full]))==3,'full source cut forces the common amplitude matrix invertible')
 # Regenerate the full affine companion family in the common amplitude gauge.
 baseline={j:{h:np.kron(a.vandermonde([n],16),eye) for h,n in vv.items()} for j,vv in nodes.items()}
 for j,Cj in zip([0,61,62],oldC):baseline[j][263]=Cj
 inv={j:{i:g.inverse(np.vstack([baseline[j][h] for h in vv]),a) for i,vv in views[j].items()} for j in [0,61]}
 def fibre(j,i,h):
  p=views[j][i].index(h);return inv[j][i][:,3*p:3*p+3]
 A0={i:fibre(0,i,263) for i,vv in views[0].items() if 263 in vv}
 B0={i:fibre(61,i,642) for i in B};C0={i:fibre(0,i,116) for i in C}
 ann0=previous.null_basis(S0.T,a).T;Sb0=basis(np.hstack(list(B0.values())))
 need(a.rank(np.hstack([Sb,Sb0]))==18 and all(not np.any(a.mm(ann0,K)) for K in A0.values()),'normalized old geometric families')
 need(all(a.rank(np.hstack([Sb0,K]))==18 for K in C0.values()),'old companion columns belong to Sb')
 _,picked=g.rref(a.mm(ann0,Sb0).T,a);R=ann0[picked];need(R.shape==(12,48),'twelve effective row directions')
 coefficients={}
 for i,K in C0.items():
  cc=np.zeros((37,48,3),dtype=np.uint8);cc[0]=K
  if i in A0:
   values=a.mm(R,K)
   for u in range(3):
    for t in range(12):cc[1+12*u+t]=a.product[A0[i][:,u,None],values[t,None,:]]
  coefficients[i]=cc
 cache={};origins={}
 for q in a.by_donor[45]:
  cols=[];origins[q]=[]
  if q!=642:
   for i,K in B0.items():
    if a.planes[q]<=a.adj[i]:
     cc=np.zeros((37,48,3),dtype=np.uint8);cc[0]=K;cols.append(cc);origins[q]+=[[642,i,p] for p in range(3)]
  if q!=116:
   for i,cc in coefficients.items():
    if a.planes[q]<=a.adj[i]:cols.append(cc);origins[q]+=[[116,i,p] for p in range(3)]
  cache[q]=np.concatenate(cols,axis=2).reshape(1776,-1)
 witnesses={};constant_columns=[];projection_ranks=[]
 for i in [22,24,30,32]:
  need(i in kernels and not any(a.planes[h]<=a.adj[i] for h in [263,642,116]),'distant native view with sixteen geometric source planes')
  Y=None
  for q in views[45][i]:
   Z=basis(cache[q]);Y=Z if Y is None else intersection(Y,Z)
  need(Y.shape==(1776,3),'three-dimensional universal coefficient intersection at receiver '+str(i));blocks=Y.reshape(37,48,3)
  need(all(not np.any(a.mm(ann0,M)) for M in blocks[1:]),'variable blocks vanish in the common quotient')
  combinations={}
  for q in views[45][i]:
   Z=cache[q];_,pc=g.rref(Z,a);Zb=Z[:,pc];_,rows=g.rref(Zb.T,a)
   L=np.zeros((Z.shape[1],3),dtype=np.uint8);L[pc]=a.mm(g.inverse(Zb[rows],a),Y[rows]);need(np.array_equal(a.mm(Z,L),Y),'constant coefficient identity')
   combinations[q]=L.tolist()
  constant_columns.append(blocks[0]);projection_ranks.append(a.rank(a.mm(ann0,np.hstack(constant_columns))))
  witnesses[i]={'planes':views[45][i],'coefficient_blocks':blocks.tolist(),'constant_combinations':combinations}
 need(projection_ranks==[3,6,9,12],'four constant quotient witnesses are independent')
 constant_union=np.hstack(constant_columns);need(a.rank(a.mm(ann0,constant_union))==12,'exact twelve-dimensional constant-projection certificate')
 certificate={'frozen_native_B':{str(i):K.tolist() for i,K in B.items()},'frozen_native_C':{str(i):K.tolist() for i,K in C.items()},
  'frozen_forced_spaces':{str(q):Z.tolist() for q,Z in forced.items()},'all_native_source45_views':{str(i):views[45][i] for i in kernels},
  'all_native_view_kernels':{str(i):K.tolist() for i,K in kernels.items()},'frozen_union_basis':union.tolist(),
  'normal_form':{'core':U.tolist(),'coordinate_rows':rr,'inverse':Ui.tolist(),'equations':Eq.tolist(),'complete_null_basis':N.tolist(),'restriction_image':image.tolist(),'expected_amplitude_basis':expected.tolist(),'full_cut_witness':5},
  'S0':S0.tolist(),'annihilator_S0':ann0.tolist(),'Sb':Sb0.tolist(),'effective_tail_rows':R.tolist(),
  'base_A_fibres':{str(i):K.tolist() for i,K in A0.items()},'base_B_fibres':{str(i):K.tolist() for i,K in B0.items()},'companion_coefficients':{str(i):cc.tolist() for i,cc in coefficients.items()},
  'origins':origins,'witnesses':witnesses,'constant_union':constant_union.tolist(),'projected_constant_union':a.mm(ann0,constant_union).tolist()}
 payload=(json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n').encode();(out/'CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_NATIVE_CONTRACTION_UNION_GATE','native_source45_views':59,'frozen_deficient_views':defects,'frozen_union_rank':15,
  'native_anchor_counts':[33,34,32],'normal_form_equations':[765,270],'normal_form_nullity':57,'restriction_rank':9,'universal_witness_receivers':[22,24,30,32],
  'constant_projection_ranks':projection_ranks,'universal_constrained_union_lower_bound':12,'all_finite_GF64_extensions':True,'arbitrary_F_linear_repetition_blocks':True,
  'arbitrary_binary_linear_central_redesign':False,'changed_off_H263_quotients':False,'changed_H642_fibre_diagram':False,'target_change_may_relax_forced_constraints':True,
  'complete_global_supplier':False,'new_complete_kappa':False,'certificate_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],15,12,57,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
