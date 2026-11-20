#!/usr/bin/env python3
"""A forced translation kernel prevents the frozen companion closure."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def need(ok,text):
 if not ok:raise ValueError(text)

def main(repo,out):
 out.mkdir(parents=True,exist_ok=True)
 base=repo/'research/moonshot-005-program/results'
 geom=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','closing_geometry')
 family,a,previous=geom.context(repo)
 data=json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in rows.items()} for j,rows in data['maps'].items()}
 pins=Path(__file__).with_name('SOURCE-PINS.json')
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 reports=[];details=[]
 for third,target,anchor,final in [(116,45,0,4),(643,100,62,2)]:
  specifications=[(642,61),(third,anchor)]
  need(target!=10 and final!=80 and target in a.adj[final],'ordinary identity target')
  need(all(max(a.quota[j,h] for h in a.by_donor[j])==30 for j in [target,61,anchor]),'ordinary nonsingleton source roles')
  prescribed={}
  for h,j in specifications:
   need(j in a.planes[h] and target in a.planes[h],'actual shared H')
   fibres={}
   for i in sorted(a.native):
    if i==80 or not a.planes[h]<=a.adj[i]:continue
    visible=[r for r in a.by_donor[j] if a.planes[r]<=a.adj[i]]
    need(len(visible)==16 and a.rank(np.vstack([maps[j][r] for r in visible]))==48,'anchor native source cut')
    off=[r for r in visible if r!=h]
    K=previous.null_basis(np.vstack([maps[j][r] for r in off]),a)
    need(K.shape==(48,3),'full native anchor inverse fibre')
    fibres[i]=K
   prescribed[h]=fibres
  constraints={};ann={};origins={}
  for r in a.by_donor[target]:
   uses=[(h,i,K) for h,fibres in prescribed.items() if h!=r for i,K in fibres.items() if a.planes[r]<=a.adj[i]]
   Z=np.hstack([K for h,i,K in uses]) if uses else np.zeros((48,0),dtype=np.uint8)
   _,piv=geom.rref(Z,a);constraints[r]=Z[:,piv]
   ann[r]=previous.null_basis(Z.T,a).T
   origins[r]=[[h,i] for h,i,K in uses]
  deficiencies={}
  for i in sorted(a.adj[target]&a.native):
   visible=[r for r in a.by_donor[target] if a.planes[r]<=a.adj[i]]
   defect=48-a.rank(np.vstack([ann[r] for r in visible]))
   if defect:deficiencies[i]=defect
  visible=[r for r in a.by_donor[target] if a.planes[r]<=a.adj[final]]
  common=previous.null_basis(np.vstack([ann[r] for r in visible]),a)
  need(len(visible)==16 and common.shape==(48,3),'specified three-dimensional forced kernel')
  need(all(a.rank(np.hstack((constraints[r],common)))==constraints[r].shape[1] for r in visible),'common kernel lies in every forced quotient invariance space')
  need(len(deficiencies)==(29 if target==45 else 27) and set(deficiencies.values())=={3},'complete finite native-cut census')
  controls=[]
  for only in prescribed:
   single={}
   for r in a.by_donor[target]:
    cols=[K for h,fibres in prescribed.items() if h==only and h!=r for i,K in fibres.items() if a.planes[r]<=a.adj[i]]
    Z=np.hstack(cols) if cols else np.zeros((48,0),dtype=np.uint8)
    single[r]=previous.null_basis(Z.T,a).T
   failures=[]
   for i in sorted(a.adj[target]&a.native):
    vv=[r for r in a.by_donor[target] if a.planes[r]<=a.adj[i]]
    if a.rank(np.vstack([single[r] for r in vv]))!=48:failures.append(i)
   need(not failures,'one-anchor negative control has no forced common kernel')
   controls.append(only)
  reports.append({'third_H':third,'target_donor':target,'anchors':[61,anchor],'witness_receiver':final,
   'witness_planes':visible,'forced_kernel_rank':3,'deficient_native_views':deficiencies,'single_anchor_controls_pass':controls})
  details.append({'third_H':third,'target_donor':target,'witness_receiver':final,'kernel':common.tolist(),
   'planes':{str(r):{'forced_space':constraints[r].tolist(),'annihilator':ann[r].tolist(),'origins':origins[r]} for r in visible},
   'anchor_fibres':{str(h):{str(i):K.tolist() for i,K in fibres.items()} for h,fibres in prescribed.items()}})
 payload=(json.dumps(details,sort_keys=True,separators=(',',':'))+'\n').encode()
 (out/'WITNESSES.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_FROZEN_TWO_H_COMPANION_OBSTRUCTION','reports':reports,'witness_payload_sha256':hashlib.sha256(payload).hexdigest(),
  'arbitrary_target_source_functions':True,'independent_redesign_of_frozen_anchor_fibres':False,'new_complete_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(result['status'],flush=True)

if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
