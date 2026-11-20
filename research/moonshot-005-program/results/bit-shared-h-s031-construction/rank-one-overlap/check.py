#!/usr/bin/env python3
"""Two protected native H centres with a rank-one overlap and a rank-eight provider."""
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
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','rank1_overlap_geometry');family,a,previous=g.context(repo)
 moving=load(base/'bit-shared-h-s031-construction/moving-fibres/construction.py','rank1_overlap_formula')
 pins=here/'SOURCE-PINS.json'
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 old=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
 raw=json.loads(gzip.decompress((here/'SOURCE-COEFFICIENTS.json.gz').read_bytes()));literal=json.loads((here/'LITERAL-PROVIDER.json').read_text())
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in raw['maps'].items()}
 nodes={int(j):{int(h):n for h,n in vv.items()} for j,vv in old['base_nodes'].items()};eye=np.eye(3,dtype=np.uint8)
 r=np.array(raw['r'],dtype=np.uint8);lam=np.array(raw['lambda'],dtype=np.uint8);need(r.tolist()==[32,42,1] and lam.tolist()==[17,33,59],'literal fixed amplitude and row')
 ports={263:[110,132,720,810,1509,1735,1994,2621,2836],642:[302,594,673,1089,1297,1509,1726,2230,3067]}
 Hwords={263:np.array(old['Hwords']['263'],dtype=np.uint8),642:np.array(raw['Bword'],dtype=np.uint8)}
 need(np.array_equal(Hwords[642],np.array(literal['word'],dtype=np.uint8)) and a.rank(Hwords[642])==8,'literal paid rank-eight provider')
 # Authenticate the same finite G A=Q F construction as the independently reviewed rank-eight mechanism.
 params=json.loads((base/'bit-coupled-native-geometric-cycle-source/component/output/PARAMETERS.json').read_text())['local']['642']
 chart,field_nodes,rec,E,E2=g.geometry(family,a,params);N=previous.null_basis(E2.T,a).T
 mv=np.array(literal['m'],dtype=np.uint8);nv=np.array(literal['n'],dtype=np.uint8);pv=np.array(literal['p'],dtype=np.uint8)
 _,pc=g.rref(N,a);ni=g.inverse(N[:,pc],a);um=a.mm(mv[pc][None,:],ni)[0];un=a.mm(nv[pc][None,:],ni)[0]
 need(np.array_equal(a.mm(um[None,:],N)[0],mv) and np.array_equal(a.mm(un[None,:],N)[0],nv),'both selected rows lie in N')
 def rowbasis(first):
  rows=[first]
  for z in eye:
   if a.rank(np.array(rows+[z],dtype=np.uint8))>len(rows):rows.append(z)
   if len(rows)==3:return np.array(rows,dtype=np.uint8)
 t=a.product[nv,a.inverse[mv]];W=[a.mm(rowbasis(um^un),a.product[N,a.inverse[t^1]]),a.mm(rowbasis(um),N),a.mm(rowbasis(un),a.product[N,a.inverse[t]])]
 u=a.product[a.product[mv,pv],a.inverse[t^1]];v=a.product[a.product[mv,pv],a.inverse[t]]
 G=np.vstack([mv,u,u^v]+[row for M in W for row in M[1:]]);Q=np.zeros((9,9),dtype=np.uint8);Q[1,[0,3]]=1;Q[2,[0,6]]=1
 for z,c in enumerate([1,2,4,5,7,8],3):Q[z,c]=1
 need(a.rank(G)==9 and np.array_equal(a.mm(g.inverse(G,a),Q),Hwords[642]),'finite rank-eight provider reconstruction')
 # Map the shared source chart to field parameters by its genuine sixteen-node blocks.
 quad=lambda x:g.quadratic(x,a);polar=lambda x,y:quad(x^y)^quad(x)^quad(y)
 Qnodes=[x for x in range(64) if not quad(x)];blocks={frozenset(x for x in Qnodes if polar(vv,x)==1^quad(vv)):vv for vv in range(1,64)}
 Bfibres={};P0=[];Pb=[];correction_ranks=[]
 for i in chart.views:
  observed=frozenset(nodes[61][h] for h in a.by_donor[61] if a.planes[h]<=a.adj[i]);vv=blocks[observed]
  Ub=moving.fibre(g,a,vv,60);Kb=np.kron(Ub[:,None],eye);Bfibres[i]=Kb
  ss=a.mm(E,np.array(rec[i],dtype=np.uint8)[:,None])[:,0];V=a.product[ss[:,None],E]
  D=[a.mm(W[0],a.product[t[:,None],V]),a.mm(W[1],a.product[t[:,None],V]),a.mm(W[2],V)]
  D[0][0]=a.mm(u[None,:],V)[0];D[1][0]=a.mm(a.product[mv,pv][None,:],V)[0];D[2][0]=a.mm(v[None,:],V)[0]
  need(all(np.array_equal(a.mm(maps[j][642],Kb),D[s]) for s,j in enumerate(chart.donors)),'all three transplanted source pencils')
  need(not np.any(a.mm(D[1][1:],r[:,None])),'one fixed amplitude lies in every lower-row kernel')
  if a.planes[263]<=a.adj[i]:
   U0=moving.fibre(g,a,vv,0);Ka=np.kron(U0[:,None],eye);P0.append(Ka);Pb.append(Kb)
   scalar=int(a.mm(D[1],r[:,None])[0,0]);target=np.zeros((3,3),dtype=np.uint8);target[0]=a.product[scalar,lam]
   need(np.array_equal(a.mm(maps[61][642],Ka),target),'rank-one action prescribed on the old first-centre propagation')
   Knew=Ka^a.product[Ub[:,None,None],a.product[r[:,None],lam[None,:]][None,:,:]].reshape(48,3)
   need(not np.any(a.mm(maps[61][642],Knew)) and a.rank(Knew)==3,'explicit new first-centre fibre formula')
   correction_ranks.append(a.rank(Knew^Ka))
 need(len(P0)==20 and a.rank(np.hstack(P0))==a.rank(np.hstack(Pb))==15,'two full old propagation cores')
 need(a.rank(a.mm(maps[61][642],np.hstack(P0)))==1,'global overlap action has exactly rank one')
 need(all(not np.any(a.mm(maps[j][263],np.hstack(Pb))) for j in [0,61,62]),'first central maps annihilate the companion propagation')
 source=[]
 for j,rows in maps.items():
  changed=[h for h,M in rows.items() if not np.array_equal(M,np.kron(a.vandermonde([nodes[j][h]],16),eye))]
  need(set(changed)==({263,{0:116,61:642,62:643}[j]} if j in [0,61,62] else {642}),'exact one/two edited quotient locations')
  chartj=family.Chart(a,263 if j in [0,61,62] else 642,3);chartj.source_views(rows,j);chartj.early(j,rows,0,fixed_centres=(263,642))
  source.append({'donor':j,'geometric_cuts':len(a.adj[j]),'native_cuts':len(a.adj[j]&a.native),'early_seed':0,'early_rank':96,'edited_planes':changed,'propagation_upper':36 if len(changed)==2 else 27,'saturation_threshold':45})
 H=[];fibres={}
 for h in [263,642]:
  kk=[];fibres[h]={};native=0
  for i in range(120):
   if not a.planes[h]<=a.adj[i]:continue
   kernels=[previous.null_basis(np.vstack([maps[j][q] for q in a.by_donor[j] if q!=h and a.planes[q]<=a.adj[i]]),a) for j in sorted(a.planes[h])]
   need(all(a.rank(np.hstack([kernels[0],K]))==3 for K in kernels),'whole common H fibres at every geometric receiver')
   visible=[p for p,Dport in enumerate(ports[h]) if a.charts[Dport]<=a.adj[i]];readouts=[a.mm(Hwords[h][np.ix_(visible,range(3*s,3*s+3))],a.mm(maps[j][h],kernels[0])) for s,j in enumerate(sorted(a.planes[h]))]
   need(a.rank(readouts[0])==3 and all(np.array_equal(readouts[0],R) for R in readouts),'common full native-port readout')
   if h==642:need(a.rank(np.hstack([kernels[0],Bfibres[i]]))==3,'second-centre geometric fibres retained')
   fibres[h][i]=kernels[0].tolist();kk.append(kernels[0]);native+=i in a.native
  rank=a.rank(np.hstack(kk));need(rank==(22 if h==263 else 18),'new exact fibre core dimension')
  H.append({'H':h,'ports':ports[h],'geometric_receivers':len(kk),'native_receivers':native,'provider_rank':a.rank(Hwords[h]),'fibre_core_rank':rank})
 complement=np.zeros((1,9),dtype=np.uint8);complement[0,0]=1;need(a.rank(np.vstack([Hwords[642],complement]))==9,'one paid complement restores H642 input information')
 payload=(json.dumps({'source_reports':source,'H':H,'fibres':fibres,'complement':complement.tolist()},sort_keys=True,separators=(',',':'))+'\n').encode();(out/'VERIFIED-FIBRES.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_RANK_ONE_OVERLAP_TWO_H_COMPONENT','geometric_source_cuts':sum(x['geometric_cuts'] for x in source),'native_source_cuts':sum(x['native_cuts'] for x in source),'actual_early_bases':5,'H':H,'overlap_rank':1,'changed_fibre_ranks':correction_ranks,'paid_complement_dimension':1,'full_width_fifteen_bank':False,'complete_global_supplier':False,'new_complete_kappa':False,'verified_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
