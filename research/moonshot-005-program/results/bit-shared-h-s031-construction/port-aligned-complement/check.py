#!/usr/bin/env python3
"""Replay the aligned width12 pair and all shared native D compatibility conditions."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);here=Path(__file__).parent
 s=importlib.util.spec_from_file_location('aligned',here/'construction.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);g,family,a,previous=m.context(repo)
 if (here/'SOURCE-PINS.json').exists():
  for p,d in json.loads((here/'SOURCE-PINS.json').read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'pin '+p)
 raw=json.loads(gzip.decompress((here/'SOURCE-COEFFICIENTS.json.gz').read_bytes()));r=m.build_aligned(12,0,1,True);maps=r['maps'];charts=r['charts']
 need(raw['core_seed']==0 and raw['fill_seed']==1 and set(r['early_seeds'].values())=={0},'exact finite parameters and actual early bases')
 for j,vv in maps.items():
  for h,M in vv.items():need(np.array_equal(M,np.array(raw['maps'][str(j)][str(h)],dtype=np.uint8)),'all literal source coefficients')
 for c in charts:need(c.ports==raw['H'][str(c.h)]['ports'] and np.array_equal(c.V,np.array(raw['H'][str(c.h)]['word'],dtype=np.uint8)),'current physical ports and words')
 need(np.array_equal(r['relations'],np.array(raw['relations'],dtype=np.uint8)) and a.rank(r['relations'])==8,'eight same-D cross equations')
 need(np.array_equal(r['lift'],np.array(raw['lift'],dtype=np.uint8)) and r['lift'].shape==(144,136),'complete cross-equation lift')
 need(all(np.array_equal(X,np.array(Y,dtype=np.uint8)) for X,Y in zip(r['selectors'],raw['selectors'])),'actual same-D shared-donor selectors')
 fibres={};H=[]
 for c in charts:
  fibres[c.h]={};joined=[];native=0
  for i in c.views:
   j=c.donors[0];off=[h for h in a.by_donor[j] if h!=c.h and a.planes[h]<=a.adj[i]];K=previous.null_basis(np.vstack([maps[j][h] for h in off]),a);need(K.shape==(192,12),'whole off-H inverse fibre');vis=[p for p,D in enumerate(c.ports) if a.charts[D]<=a.adj[i]];Rs=[]
   for t,j in enumerate(c.donors):
    off=[h for h in a.by_donor[j] if h!=c.h and a.planes[h]<=a.adj[i]];need(not np.any(a.mm(np.vstack([maps[j][h] for h in off]),K)),'entire common fibre at all donors')
    Rs.append(a.mm(c.V[np.ix_(vis,range(12*t,12*t+12))],a.mm(maps[j][c.h],K)))
   need(a.rank(Rs[0])==12 and all(np.array_equal(Rs[0],R) for R in Rs),'full twelve-port common readout');fibres[c.h][i]={'kernel':K.tolist(),'readout':Rs[0].tolist(),'ports':[c.ports[p] for p in vis]};joined.append(K);native+=i in a.native
  H.append({'H':c.h,'provider_rank':a.rank(c.V),'geometric_readouts':36,'native_readouts':native,'core_rank':a.rank(np.hstack(joined))})
 checks,records=m.cross_check(r,12);need(checks=={'views':46,'cross_fail':0,'outside_fail':0},'all native outside-D and wrong-D annihilations')
 common=sorted(set(charts[0].ports)&set(charts[1].ports));need(common==[296,733,825,1852],'exact common unmarked D charts');details=[]
 for rr in records:
  i=rr['receiver'];D=rr['D'];obs=[];vectors={}
  for j in maps:
   if j not in a.charts[D]:continue
   qs=[h for h in a.by_donor[j] if a.planes[h]<=a.adj[i] and not a.planes[h]<=a.charts[D]];need(len(qs)==12,'twelve actual outside-D planes');obs.extend(maps[j][h] for h in qs)
  outside_dim=192-a.rank(np.vstack(obs))
  for c in charts:
   ff=fibres[c.h][i];K=np.array(ff['kernel'],dtype=np.uint8);R=np.array(ff['readout'],dtype=np.uint8);p=ff['ports'].index(D);vectors[c.h]=a.mm(K,g.inverse(R,a)[:,p:p+1]);other=[p for p,Q in enumerate(c.ports) if Q!=D and a.charts[Q]<=a.adj[i]]
   for t,j in enumerate(c.donors):obs.append(a.mm(c.V[np.ix_(other,range(12*t,12*t+12))],maps[j][c.h]))
  X=np.vstack(obs);V=np.hstack(list(vectors.values()));need(a.rank(V)==2 and not np.any(a.mm(X,V)),'both isolated directions survive all known source/H observations')
  details.append({'D':D,'receiver':i,'outside_source_common_dimension':outside_dim,'known_partial_D_common_dimension':192-a.rank(X),'vectors':{str(h):v[:,0].tolist() for h,v in vectors.items()}})
 for name,payload in [('FIBRES',fibres),('SHARED-D-CHECKS',details)]:
  z=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode();(out/(name+'.json.gz')).write_bytes(gzip.compress(z,mtime=0))
 result={'status':'PASS_PORT_ALIGNED_WIDTH12_TWO_H_COMPLEMENT','source_width':12,'bank_dimension':192,'geometric_source_cuts':sum(len(a.adj[j]) for j in maps),'native_source_cuts':sum(len(a.adj[j]&a.native) for j in maps),'actual_early_bases':[{'donor':j,'seed':r['early_seeds'][j],'rank':384} for j in sorted(maps)],'H':H,'geometric_H_readouts':72,'native_H_readouts':67,'same_D_relation_rank':8,'latent_base_dimension':136,'Hermite_tail_dimension':56,'shared_native_D_cuts':46,'wrong_D_H_failures':0,'outside_D_source_failures':0,'known_partial_D_dimensions':sorted(set(x['known_partial_D_common_dimension'] for x in details)),'protected_width3_repaired':False,'complete_D_word':False,'complete_global_supplier':False,'new_complete_kappa':False}
 need(result['geometric_source_cuts']==315 and result['native_source_cuts']==291,'complete five-source census');(out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],315,291,72,67,46,0,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
