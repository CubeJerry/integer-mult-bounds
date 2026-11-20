#!/usr/bin/env python3
"""Exact rank-eight native H642 provider and full one-edit source component."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def main(repo,out):
 out.mkdir(parents=True,exist_ok=True)
 spec=importlib.util.spec_from_file_location('rank8_construction',Path(__file__).with_name('construction.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 pins=Path(__file__).with_name('SOURCE-PINS.json')
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 d=mod.build(repo);a=d['atlas'];chart=d['chart'];p=d['previous'];P=d['Hword'];maps=d['maps'];zero=np.zeros((3,3),dtype=np.uint8)
 need(chart.h==642 and chart.donors==[45,61,100] and chart.ports==[302,594,673,1089,1297,1509,1726,2230,3067],'actual native centre, donors and physical nine-port ownership')
 need(10 not in chart.donors and 80 not in chart.views and all(a.planes[642]<=a.charts[q] for q in chart.ports),'ordinary identity target and actual incidences')
 source=[]
 for j in chart.donors:
  need(max(a.quota[j,h] for h in a.by_donor[j])==30,'ordinary source role')
  chart.source_views(maps[j],j)
  for seed in range(100):
   try:chart.early(j,maps[j],seed,fixed_centres=(642,));break
   except ValueError:pass
  else:raise ValueError('actual early source basis not found')
  source.append({'donor':j,'geometric_cuts':len(a.adj[j]),'native_cuts':len(a.adj[j]&a.native),'actual_early_seed':seed,'actual_early_rank':96,'changed_source_planes':[642],'uniform_propagation_upper':27,'saturation_threshold':45})
 fibres={};counts={'geometric':0,'native':0}
 for i,r in d['receivers'].items():
  s=a.mm(d['E'],np.array(r,dtype=np.uint8)[:,None])[:,0];V=a.product[s[:,None],d['E']]
  A=np.hstack([a.product[d['t'][:,None],V],V]);D=d['pencils'][i]
  block=np.block([[D[0],D[0]],[D[1],zero],[zero,D[2]]])
  need(np.array_equal(a.mm(d['G'],A),a.mm(d['Q'],block)),'exact finite constraint identity')
  need(np.array_equal(a.mm(P,block),A),'rank-eight provider sends the difference space to unseen ports')
  visible=[q for q,port in enumerate(chart.ports) if a.charts[port]<=a.adj[i]]
  need(len(visible)==3 and set(visible)==set(np.flatnonzero(s==0)) and not np.any(A[visible]),'actual receiver sees exactly the three zero evaluations')
  K=d['fibres'][i]
  for j in chart.donors:
   off=[h for h in a.by_donor[j] if h!=642 and a.planes[h]<=a.adj[i]];X=np.vstack([maps[j][h] for h in off])
   need(a.rank(X)==45 and not np.any(a.mm(X,K)) and a.rank(K)==3,'entire common off-H inverse fibre')
  need(all(a.rank(X)==3 for X in D),'all three central source pencils invertible')
  readouts=[a.mm(P[np.ix_(visible,range(3*j,3*j+3))],D[j]) for j in range(3)]
  need(a.rank(readouts[0])==3 and all(np.array_equal(readouts[0],X) for X in readouts),'common invertible actual receiver readout')
  fibres[str(i)]={'kernel':K.tolist(),'readout':readouts[0].tolist(),'ports':[chart.ports[q] for q in visible]};counts['geometric']+=1;counts['native']+=i in a.native
 need(counts=={'geometric':36,'native':34},'complete receiver scope')
 kernel=np.zeros((9,1),dtype=np.uint8);kernel[[0,3,6]]=1;complement=np.zeros((1,9),dtype=np.uint8);complement[0,0]=1
 need(a.rank(P)==8 and not np.any(a.mm(P,kernel)),'exact one-dimensional provider kernel')
 need(a.rank(np.vstack([P,complement]))==9 and a.mm(complement,kernel)[0,0]==1,'one independent complement restores information')
 _,rows=d['geometry'].rref(P.T,a);square=np.vstack([P[rows],complement]);need(square.shape==(9,9) and a.rank(square)==9,'eight real port rows plus paid complement form a square basis')
 coefficients={'H':642,'donors':chart.donors,'ports':chart.ports,'field_modulus':67,'Hword':P.tolist(),'complement':complement.tolist(),'independent_port_indices':rows,
  'source_maps':{str(j):{str(h):M.tolist() for h,M in vv.items()} for j,vv in maps.items()},'fibres':fibres,
  'E':d['E'].tolist(),'E2':d['E2'].tolist(),'N':d['N'].tolist(),'G':d['G'].tolist(),'Q':d['Q'].tolist(),
  'source_core':d['source_core'].tolist(),'pencils':{str(i):[D.tolist() for D in DD] for i,DD in d['pencils'].items()},'source_reports':source}
 payload=(json.dumps(coefficients,sort_keys=True,separators=(',',':'))+'\n').encode();(out/'COEFFICIENTS.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_NATIVE_RANK_EIGHT_H642_COMPONENT','H':642,'source_bank_dimension':48,'source_width':3,'H_input_dimension':9,'H_port_dimension':9,
  'provider_rank':8,'paid_complement_dimension':1,'receiver_checks':counts,'sources':source,
  'geometric_source_cuts':sum(x['geometric_cuts'] for x in source),'native_source_cuts':sum(x['native_cuts'] for x in source),
  'source_early_bases':3,'complete_early_H_without_paid_repair':False,'full_forty_five_port_component':False,
  'independent_complementary_width_twelve':False,'complete_global_supplier':False,'new_complete_kappa':False,'coefficient_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
