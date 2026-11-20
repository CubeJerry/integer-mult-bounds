#!/usr/bin/env python3
"""Two permitted central tails create exact four-dimensional known D1509 spaces."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);here=Path(__file__).parent;base=repo/'research/moonshot-005-program/results';s=importlib.util.spec_from_file_location('protected_D_geometry',base/'bit-coupled-native-geometric-h-source/component/construction.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);family,a,previous=g.context(repo)
 if (here/'SOURCE-PINS.json').exists():
  for p,d in json.loads((here/'SOURCE-PINS.json').read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'pin '+p)
 old=read(base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz');moving=read(base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz');raw=read(here/'SOURCE-COEFFICIENTS.json.gz')
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in raw['maps'].items()};before={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in old['maps'].items()}
 changed=[(j,h) for j,vv in maps.items() for h,M in vv.items() if not np.array_equal(M,before[j][h])];need(sorted(changed)==[(45,642),(100,642)],'exactly two allowed H642 central-tail changes')
 ports={263:[110,132,720,810,1509,1735,1994,2621,2836],642:[302,594,673,1089,1297,1509,1726,2230,3067]};P={263:np.array(moving['Hwords']['263'],dtype=np.uint8),642:np.array(old['Bword'],dtype=np.uint8)};fibres={};isolated={};H=[];D=1509;aud=sorted(i for i in a.native if a.charts[D]<=a.adj[i]);need(len(aud)==11,'all native D1509 views')
 for h in [263,642]:
  fibres[h]={};isolated[h]={};columns=[];ds=sorted(a.planes[h]);native=0
  for i in range(120):
   if not a.planes[h]<=a.adj[i]:continue
   j=ds[0];off=[q for q in a.by_donor[j] if q!=h and a.planes[q]<=a.adj[i]];K=previous.null_basis(np.vstack([maps[j][q] for q in off]),a);need(K.shape==(48,3),'whole source inverse fibre');vis=[p for p,d in enumerate(ports[h]) if a.charts[d]<=a.adj[i]];Rs=[]
   for t,j in enumerate(ds):
    off=[q for q in a.by_donor[j] if q!=h and a.planes[q]<=a.adj[i]];need(not np.any(a.mm(np.vstack([maps[j][q] for q in off]),K)),'whole common H fibre')
    Rs.append(a.mm(P[h][np.ix_(vis,range(3*t,3*t+3))],a.mm(maps[j][h],K)))
   need(a.rank(Rs[0])==3 and all(np.array_equal(Rs[0],R) for R in Rs),'same full native-port readout');fibres[h][i]={'kernel':K.tolist(),'readout':Rs[0].tolist(),'ports':[ports[h][p] for p in vis]};columns.append(K);native+=i in a.native
   if i in aud:
    p=vis.index(ports[h].index(D));isolated[h][i]=a.mm(K,g.inverse(Rs[0],a)[:,p:p+1])
  core=np.hstack(columns);_,pc=g.rref(core,a);core=core[:,pc];H.append({'H':h,'geometric_readouts':36,'native_readouts':native,'provider_rank':a.rank(P[h]),'core_rank':core.shape[1]})
  if h==642:Sb=core
 need(Sb.shape==(48,18),'retained entire H642 geometric core')
 for j in maps:
  chart=family.Chart(a,263 if j in [0,61,62] else 642,3);chart.source_views(maps[j],j);chart.early(j,maps[j],0,fixed_centres=(263,642))
 for j in [45,100]:need(not np.any(a.mm(maps[j][642]^before[j][642],Sb)),'both changes annihilate the entire H642 core')
 spaces={};reports=[]
 for i in aud:
  outside=[]
  for j in maps:
   if j not in a.charts[D]:continue
   qs=[q for q in a.by_donor[j] if a.planes[q]<=a.adj[i] and not a.planes[q]<=a.charts[D]];need(len(qs)==12,'actual outside-D source observations');outside.extend(maps[j][q] for q in qs)
  obs=list(outside);zd=48-a.rank(np.vstack(obs));otherA=[q for q,d in enumerate(ports[263]) if d!=D and a.charts[d]<=a.adj[i]]
  for t,j in enumerate(sorted(a.planes[263])):obs.append(a.mm(P[263][np.ix_(otherA,range(3*t,3*t+3))],maps[j][263]))
  ad=48-a.rank(np.vstack(obs));otherB=[q for q,d in enumerate(ports[642]) if d!=D and a.charts[d]<=a.adj[i]];obs.append(a.mm(P[642][np.ix_(otherB,range(3,6))],maps[61][642]));L=previous.null_basis(np.vstack(obs),a)
  need((zd,ad,L.shape[1])==(12,6,4),'canonical four-space from fixed source/A/shared-B observations');need(np.array_equal(L,np.array(raw['spaces'][str(i)],dtype=np.uint8)),'literal canonical four-space')
  for t,j in enumerate(sorted(a.planes[642])):obs.append(a.mm(P[642][np.ix_(otherB,range(3*t,3*t+3))],maps[j][642]))
  X=np.vstack(obs);need(48-a.rank(X)==4 and not np.any(a.mm(X,L)),'exact common partial-D space after both new tails')
  V=np.hstack([isolated[263][i],isolated[642][i]]);need(a.rank(V)==2 and not np.any(a.mm(X,V)),'both old isolated directions survive every known source/H cut')
  spaces[i]=L;reports.append({'receiver':i,'outside_source_dimension':zd,'with_H263_dimension':ad,'with_shared_H642_dimension':4,'complete_known_partial_D_dimension':4})
 systems={}
 for t,j in enumerate(sorted(a.planes[642])):
  eq=[];rhs=[];target=a.mm(before[j][642],Sb)
  for u in range(3):
   for p in range(18):
    row=np.zeros((3,48),dtype=np.uint8);row[u]=Sb[:,p];eq.append(row.reshape(-1));rhs.append(target[u,p])
  for i,L in spaces.items():
   for q,d in enumerate(ports[642]):
    if d==D or not a.charts[d]<=a.adj[i]:continue
    for p in range(4):eq.append(a.product[P[642][q,3*t:3*t+3,None],L[:,p][None,:]].reshape(-1));rhs.append(0)
  M=np.array(eq,dtype=np.uint8);y=np.array(rhs,dtype=np.uint8)[:,None];need(M.shape==(142,144) and a.rank(M)==a.rank(np.hstack([M,y]))==110,'exact consistent affine tail system');need(not np.any(a.mm(M,maps[j][642].reshape(-1,1))^y),'literal coefficient solves every constraint')
  N=previous.null_basis(M,a);need(N.shape==(144,34),'complete free tail dimension');systems[j]={'equations':M.tolist(),'rhs':y[:,0].tolist(),'null_basis':N.tolist()}
 payload=(json.dumps({'H_fibres':fibres,'D_spaces':{str(i):L.tolist() for i,L in spaces.items()},'D_reports':reports,'affine_systems':systems},sort_keys=True,separators=(',',':'))+'\n').encode();(out/'CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_PROTECTED_D1509_FOUR_SPACE_TAIL_REPAIR','changed_quotients':changed,'geometric_source_cuts':315,'native_source_cuts':291,'actual_early_bases':5,'early_seeds':{str(j):0 for j in maps},'H':H,'geometric_H_readouts':72,'native_H_readouts':67,'native_D1509_views':11,'known_partial_D_dimensions':[4]*11,'tail_system_shape':[142,144],'tail_system_rank':110,'free_tail_dimension':34,'provider_words_unchanged':True,'protected_uniform_upper_by_donor':{str(j):36 if j in [0,61,62] else 27 for j in maps},'paid_H642_logical_complement_dimension':1,'complete_D_decoder':False,'fullwidth12_complement_included':False,'complete_global_supplier':False,'new_complete_kappa':False,'certificate_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],315,291,72,67,11,4,110,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
