#!/usr/bin/env python3
"""A universal affine tail certificate obstructs the full companion source."""
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
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','paid_tail_geometry');family,a,previous=g.context(repo)
 pins=Path(__file__).with_name('SOURCE-PINS.json')
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 raw=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
 nodes={int(j):{int(h):n for h,n in vv.items()} for j,vv in raw['base_nodes'].items()};eye=np.eye(3,dtype=np.uint8)
 maps={j:{h:np.kron(a.vandermonde([n],16),eye) for h,n in vv.items()} for j,vv in nodes.items()}
 for j in [0,61,62]:maps[j][263]=np.array(raw['maps'][str(j)]['263'],dtype=np.uint8)
 views={j:{i:sorted(h for h in a.by_donor[j] if a.planes[h]<=a.adj[i]) for i in sorted(a.adj[j])} for j in maps}
 inv={j:{i:g.inverse(np.vstack([maps[j][h] for h in vv]),a) for i,vv in views[j].items()} for j in [0,61]}
 def fibre(j,i,h):
  p=views[j][i].index(h);return inv[j][i][:,3*p:3*p+3]
 def basis(Z):
  _,p=g.rref(Z,a);return Z[:,p]
 def intersection(X,Y):
  N=previous.null_basis(np.hstack([X,Y]),a);return basis(a.mm(X,N[:X.shape[1]]))
 A={i:fibre(0,i,263) for i in views[0] if 263 in views[0][i]};S0=basis(np.hstack(list(A.values())))
 B={i:fibre(61,i,642) for i in views[61] if 642 in views[61][i] and i in a.native and i!=80}
 C={i:fibre(0,i,116) for i in views[0] if 116 in views[0][i] and i in a.native and i!=80}
 Sb=basis(np.hstack(list(B.values())));ann0=previous.null_basis(S0.T,a).T
 need(S0.shape==Sb.shape==(48,18) and a.rank(np.hstack([S0,Sb]))==30,'two geometric cores and six-dimensional intersection')
 need(len(B)==34 and len(C)==32 and all(a.rank(np.hstack([Sb,K]))==18 for K in C.values()),'entire native companion families')
 _,picked=g.rref(a.mm(ann0,Sb).T,a);R=ann0[picked]
 need(R.shape==(12,48) and a.rank(a.mm(R,Sb))==12,'all effective tail directions')
 coefficients={}
 for i,K in C.items():
  cc=np.zeros((37,48,3),dtype=np.uint8);cc[0]=K
  if i in A:
   values=a.mm(R,K)
   for u in range(3):
    for t in range(12):cc[1+12*u+t]=a.product[A[i][:,u,None],values[t,None,:]]
  coefficients[i]=cc
 def forced_coefficients(q):
  columns=[];origins=[]
  if q!=642:
   for i,K in B.items():
    if a.planes[q]<=a.adj[i]:
     cc=np.zeros((37,48,3),dtype=np.uint8);cc[0]=K;columns.append(cc);origins += [[642,i,p] for p in range(3)]
  if q!=116:
   for i,cc in coefficients.items():
    if a.planes[q]<=a.adj[i]:columns.append(cc);origins += [[116,i,p] for p in range(3)]
  return np.concatenate(columns,axis=2).reshape(37*48,-1),origins
 witness=22;planes=views[45][witness]
 need(witness in a.native and len(planes)==16 and not any(a.planes[h]<=a.adj[witness] for h in [116,263,642]),'actual distant native witness cut')
 allZ={};origins={};Y=None;intersection_ranks=[]
 for q in planes:
  Z,origins[q]=forced_coefficients(q);allZ[q]=Z;Zb=basis(Z)
  Y=Zb if Y is None else intersection(Y,Zb);intersection_ranks.append(Y.shape[1])
 need(Y.shape==(37*48,3),'three-dimensional universal coefficient-space intersection')
 blocks=Y.reshape(37,48,3)
 need(all(not np.any(a.mm(ann0,M)) for M in blocks[1:]),'all variable coefficients lie in S0')
 need(a.rank(a.mm(ann0,blocks[0]))==3,'constant quotient rank prevents every cancellation')
 combinations={}
 for q,Z in allZ.items():
  _,pc=g.rref(Z,a);Zb=Z[:,pc];_,rr=g.rref(Zb.T,a)
  values=a.mm(g.inverse(Zb[rr],a),Y[rr]);L=np.zeros((Z.shape[1],3),dtype=np.uint8);L[pc]=values
  need(np.array_equal(a.mm(Z,L),Y),'literal universal coefficient identity at plane '+str(q));combinations[q]=L
 # One concrete tail removes the old direct collision but fails the full source census.
 delta=a.mm(family.coefficients('paid-central-tail/0',(3,len(ann0))),ann0)
 sample={j:dict(rows) for j,rows in maps.items()};sample[0][263]=maps[0][263]^delta
 newC={i:K^(a.mm(A[i],a.mm(delta,K)) if i in A else np.zeros_like(K)) for i,K in C.items()}
 for i,K in newC.items():
  off=[h for h in views[0][i] if h!=116];need(not np.any(a.mm(np.vstack([sample[0][h] for h in off]),K)) and a.rank(K)==3,'exact affine full inverse-fibre formula')
 rs=a.mm(R,Sb);_,pc=g.rref(rs,a);t=a.mm(a.mm(delta,Sb)[:,pc],g.inverse(rs[:,pc],a))
 need(np.array_equal(a.mm(t,rs),a.mm(delta,Sb)),'all ninety tail parameters reduce to the thirty-six effective ones')
 yy=blocks[0].copy()
 for value,M in zip(t.reshape(-1),blocks[1:]):yy ^= a.product[value,M]
 need(a.rank(yy)==3 and a.rank(a.mm(ann0,yy))==3,'sample universal kernel rank')
 forced={};ann={}
 for q in a.by_donor[45]:
  cols=[K for h,ff in [(642,B),(116,newC)] for i,K in ff.items() if q!=h and a.planes[q]<=a.adj[i]]
  Z=np.hstack(cols) if cols else np.zeros((48,0),dtype=np.uint8);forced[q]=basis(Z);ann[q]=previous.null_basis(Z.T,a).T
 deficiencies={i:48-a.rank(np.vstack([ann[q] for q in vv])) for i,vv in views[45].items() if i in a.native}
 need(deficiencies[4]==0 and deficiencies[22]==6,'local escape and distant full-cut failure control')
 need(a.rank(np.hstack([B[4],newC[4]]))==6,'direct companion collision is genuinely removed')
 need(all(a.rank(np.hstack([forced[q],yy]))==forced[q].shape[1] for q in planes),'evaluated universal kernel lies in every actual witness forced space')
 source_cuts=0;early=[]
 for j,rows0 in sample.items():
  for i,vv in views[j].items():need(a.rank(np.vstack([rows0[q] for q in vv]))==48,'sample full geometric source cut');source_cuts+=1
  chart=family.Chart(a,263 if j in [0,61,62] else 642,3)
  for seed in range(100):
   try:chart.early(j,rows0,seed,fixed_centres=(263,642));early.append([j,seed]);break
   except ValueError:pass
  else:raise ValueError('sample actual early basis not found')
 need(source_cuts==315,'five source charts')
 ports={263:[110,132,720,810,1509,1735,1994,2621,2836],642:[302,594,673,1089,1297,1509,1726,2230,3067]}
 Hwords={263:np.array(raw['Hwords']['263'],dtype=np.uint8),642:np.hstack([a.vandermonde(list(range(9)),3)]*3)}
 need(a.rank(Hwords[263])==9 and a.rank(Hwords[642])==3,'invertible first provider and lossy rank-three second signal map')
 readout_counts=[]
 for h in [263,642]:
  count=0;donors=sorted(a.planes[h])
  for i in range(120):
   if not a.planes[h]<=a.adj[i]:continue
   kernels=[previous.null_basis(np.vstack([sample[j][q] for q in a.by_donor[j] if q!=h and a.planes[q]<=a.adj[i]]),a) for j in donors]
   need(all(a.rank(np.hstack([kernels[0],K]))==3 for K in kernels),'sample common whole H fibres')
   vv=[p for p,D in enumerate(ports[h]) if a.charts[D]<=a.adj[i]]
   rr=[a.mm(Hwords[h][np.ix_(vv,range(3*s,3*s+3))],a.mm(sample[j][h],kernels[0])) for s,j in enumerate(donors)]
   need(a.rank(rr[0])==3 and all(np.array_equal(rr[0],x) for x in rr),'sample common invertible receiver signal readout');count+=1
  readout_counts.append(count)
 certificate={'witness_receiver':22,'planes':planes,'native_B_receivers':sorted(B),'native_C_receivers':sorted(C),
  'S0':S0.tolist(),'Sb':Sb.tolist(),'effective_tail_rows':R.tolist(),'universal_kernel_coefficients':blocks.tolist(),
  'origins':origins,'constant_combinations':{str(q):L.tolist() for q,L in combinations.items()},
  'B_fibres':{str(i):K.tolist() for i,K in B.items()},'C_fibre_coefficients':{str(i):cc.tolist() for i,cc in coefficients.items()},
  'sample_delta':delta.tolist(),'sample_kernel':yy.tolist(),'sample_Hwords':{str(h):W.tolist() for h,W in Hwords.items()},'actual_early_seeds':early}
 payload=(json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n').encode();(out/'CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_UNIVERSAL_PAID_TAIL_OBSTRUCTION','effective_parameters':36,'coefficient_blocks':37,'universal_kernel_dimension':3,
  'constant_quotient_rank':3,'witness_receiver':22,'intersection_ranks':intersection_ranks,'sample_native_deficiencies':{i:z for i,z in deficiencies.items() if z},
  'sample_source_cuts':source_cuts,'sample_actual_early_seeds':early,'sample_H_readout_counts':readout_counts,'sample_H_provider_ranks':[9,3],
  'all_field_extensions_and_noncommuting_repetitions':True,'paid_complete_H_word':False,'new_complete_kappa':False,'certificate_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],flush=True)

if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
