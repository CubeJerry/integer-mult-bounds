#!/usr/bin/env python3
"""Native fixed-H readout rigidity, including all six binary Frobenius phases."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);base=repo/'research/moonshot-005-program/results'
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','readout_geometry');family,a,previous=g.context(repo)
 pins=Path(__file__).with_name('SOURCE-PINS.json')
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 literal=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
 recorded=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/FIBRES.json.gz').read_bytes()))
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in literal['maps'].items()}
 T=np.array(literal['Hwords']['263'],dtype=np.uint8);ports=[110,132,720,810,1509,1735,1994,2621,2836]
 donors=[0,61,62];companions={0:116,61:642,62:643};receivers=sorted(i for i in a.native if a.planes[263]<=a.adj[i])
 need(len(receivers)==33 and 80 not in receivers and a.rank(T)==9,'retained native H263 word')
 K={}
 for i in receivers:
  vv=[h for h in a.by_donor[0] if h!=263 and a.planes[h]<=a.adj[i]]
  K[i]=previous.null_basis(np.vstack([maps[0][h] for h in vv]),a)
  need(K[i].shape==(48,3),'entire native inverse fibre')
  old=np.array(recorded['263'][str(i)]['kernel'],dtype=np.uint8)
  need(a.rank(np.hstack([K[i],old]))==3,'literal retained inverse fibre')
 raw=np.hstack(list(K.values()));_,pc=g.rref(raw,a);S=raw[:,pc]
 need(S.shape==(48,30),'native thirty-dimensional core')
 _,rr=g.rref(S.T,a);Sinv=g.inverse(S[rr],a);coords={i:a.mm(Sinv,V[rr]) for i,V in K.items()}
 final=4;propagations={};other_planes={};intersections=[]
 for j in donors:
  need(a.planes[companions[j]]<=a.adj[final] and j in a.adj[final],'literal companion incidence')
  other=[h for h in a.by_donor[j] if h not in [263,companions[j]] and a.planes[h]<=a.adj[final]]
  need(len(other)==14,'fourteen other observations')
  annihilators=[];propagations[j]={};other_planes[j]=other
  for h in other:
   Z=np.hstack([V for i,V in K.items() if a.planes[h]<=a.adj[i]]);_,p=g.rref(Z,a);Z=Z[:,p]
   propagations[j][h]=Z;annihilators.append(previous.null_basis(Z.T,a).T)
  Wj=previous.null_basis(np.vstack(annihilators),a);need(Wj.shape==(48,6),'six-dimensional propagation intersection')
  intersections.append(Wj)
 W=intersections[0]
 need(all(a.rank(np.hstack([W,Wj]))==6 for Wj in intersections),'same intersection at all three donors')
 need(a.rank(np.hstack([W,K[final]]))==6,'retained fibre is inside W')
 w=a.mm(Sinv,W[rr]);need(np.array_equal(a.mm(S,w),W),'W is inside the native core')
 visible={i:[p for p,D in enumerate(ports) if a.charts[D]<=a.adj[i]] for i in receivers}
 need(all(len(v)==3 for v in visible.values()),'actual three-port native selections')
 need(all(a.rank(T[np.ix_(visible[final],range(3*j,3*j+3))])==3 for j in range(3)),'invertible witness port blocks')
 def frob(M,e):
  table=np.array([g.power(v,2**e,a) for v in range(64)],dtype=np.uint8);return table[M]
 def equations(values,selection):
  rows=[]
  for V,ports_here in zip(values,selection):
   for p in ports_here:
    for j in [1,2]:
     for t in range(V.shape[1]):
      row=np.zeros((3,3,30),dtype=np.uint8)
      row[0]=a.product[T[p,:3,None],V[None,:,t]]
      row[j]=a.product[T[p,3*j:3*j+3,None],V[None,:,t]]
      rows.append(row.reshape(-1))
  return np.array(rows,dtype=np.uint8)
 phases=[];cert=[]
 for e in range(6):
  M=equations([frob(coords[i],e) for i in receivers],[visible[i] for i in receivers])
  E=equations([frob(w,e)],[visible[final]])
  need(M.shape==(594,270) and E.shape==(36,270),'complete coefficient-system dimensions')
  N=previous.null_basis(M,a);expected=15 if e%2==0 else 12
  need(N.shape==(270,expected) and a.rank(N)==expected,'complete independent phase null basis')
  need(not np.any(a.mm(M,N)) and not np.any(a.mm(E,N)),'native equations imply witness extension equations')
  rank=a.rank(M);need(rank==270-expected and a.rank(np.vstack([M,E]))==rank,'exact conclusion row-space containment')
  phases.append({'phase':e,'rows':594,'columns':270,'rank':rank,'nullity':expected,'conclusion_rows':36,'augmented_rank':rank})
  cert.append({'phase':e,'equations':M.tolist(),'conclusion':E.tolist(),'null_basis':N.tolist()})
 # Removing the companion observation leaves precisely the nonzero common kernel in the literal source.
 L=previous.null_basis(a.mm(maps[0][263],W),a);L=a.mm(W,L)
 need(L.shape==(48,3),'literal companion collision dimension')
 for j in [0,61]:
  other=[h for h in a.by_donor[j] if h!=companions[j] and a.planes[h]<=a.adj[final]]
  need(not np.any(a.mm(np.vstack([maps[j][h] for h in other]),L)),'literal whole companion fibre is the collision space')
 certificate={'native_receivers':receivers,'ports':ports,'core_basis':S.tolist(),'intersection':W.tolist(),
  'witness_receiver':final,'companions':companions,'fourteen_planes':other_planes,
  'propagation_spaces':{str(j):{str(h):Z.tolist() for h,Z in vv.items()} for j,vv in propagations.items()},'phases':cert}
 payload=(json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n').encode();(out/'CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_NATIVE_H_READOUT_RIGIDITY_SIX_PHASES','native_receivers':33,'core_dimension':30,'intersection_dimension':6,
  'witness_receiver':4,'collision_dimension':3,'phases':phases,'arbitrary_binary_linear_central_maps':True,
  'arbitrary_nonlinear_off_centre_source_maps':True,'frozen_native_fibre_diagram_and_H_word':True,
  'all_extensions_and_repetitions':True,'new_complete_kappa':False,'certificate_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],flush=True)

if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
