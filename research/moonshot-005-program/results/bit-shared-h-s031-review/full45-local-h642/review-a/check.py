#!/usr/bin/env python3
"""Independent literal source/readout/early review of the full45 local H642 component."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(path):return json.loads(gzip.decompress(path.read_bytes()))

def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);here=Path(__file__).parent;base=repo/'research/moonshot-005-program/results';author=here.parent/'author'
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','full45_independent_geometry');family,a,previous=g.context(repo)
 pins=here/'SOURCE-PINS.json'
 if pins.exists():
  for p,d in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'source pin '+p)
 raw=read(author/'output/COEFFICIENTS.json.gz');early=read(author/'output/EARLY.json.gz');literal_fibres=read(author/'output/FIBRES.json.gz');partition=json.loads((author/'PARTITION.json').read_text())
 protected=read(base/'bit-shared-h-s031-construction/rank-eight-provider/output/COEFFICIENTS.json.gz')
 donors=sorted(a.planes[642]);ports=[D for D,Q in enumerate(a.charts) if a.planes[642]<=Q];spreads=partition['spreads']
 need(donors==[45,61,100] and ports==raw['ports'] and len(ports)==45,'all actual H642 donors and physical D ports')
 need(sorted(sum(spreads,[]))==ports and len(set(sum(spreads,[])))==45 and all(len(ss)==9 for ss in spreads),'five disjoint nine-port parts cover all forty-five actual ports')
 chart=family.Chart(a,642,3);singular=set(chart.singular)
 for ss in spreads:
  pts=[x for D in ss for x in chart.radical.get(D,sorted(set(a.spread['D_radicals'][D])-{0}))]
  need(len(pts)==27 and set(pts)==singular,'each nine-port part is a literal spread of the twenty-seven singular points')
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in raw['source_maps'].items()};W=np.array(raw['word'],dtype=np.uint8)
 need(W.shape==(45,45) and a.rank(W)==44,'full H map has rank44')
 modules=[np.array(M,dtype=np.uint8) for M in raw['module_words']];need([a.rank(M) for M in modules]==[8,9,9,9,9],'one protected rank-eight and four rank-nine modules')
 expected=np.zeros_like(W)
 for m,(ss,M) in enumerate(zip(spreads,modules)):
  for r,D in enumerate(ss):
   for s in range(3):expected[ports.index(D),15*s+3*m:15*s+3*m+3]=M[r,3*s:3*s+3]
 need(np.array_equal(expected,W),'actual sorted D rows and donor-major input blocks match the literal full word')
 need(np.array_equal(modules[0],np.array(protected['Hword'],dtype=np.uint8)),'protected module is the admitted rank-eight provider')
 complement=np.array(raw['complement'],dtype=np.uint8);need(complement.shape==(1,45) and a.rank(np.vstack([W,complement]))==45,'one scalar complement restores the logical H input information')
 source_records=[];inverse_protected={};propagation={};full_early=[]
 for j in donors:
  need(set(maps[j])==set(a.by_donor[j]),'all twenty-eight actual source quotients')
  for h,M in maps[j].items():
   need(M.shape==(15,240),'full width15 source dimensions');block=np.zeros_like(M)
   for m in range(5):block[3*m:3*m+3,48*m:48*m+48]=M[3*m:3*m+3,48*m:48*m+48]
   need(np.array_equal(block,M),'literal source is the direct sum of five width3 modules')
   need(np.array_equal(M[:3,:48],np.array(protected['source_maps'][str(j)][str(h)],dtype=np.uint8)),'protected first module equals its reviewed source coefficient at every plane')
  views={i:sorted(h for h in a.by_donor[j] if a.planes[h]<=a.adj[i]) for i in sorted(a.adj[j])};inverse_protected[j]={}
  for i,vv in views.items():
   need(len(vv)==16,'actual complete geometric source cut');F=np.vstack([maps[j][h] for h in vv]);need(a.rank(F)==240,'full width15 source cut')
   inverse_protected[j][i]=(vv,g.inverse(np.vstack([maps[j][h][:3,:48] for h in vv]),a))
   source_records.append({'donor':j,'receiver':i,'rank':240,'native':i in a.native})
  # Every ordered distinct quotient pair is checked on all geometric inverse fibres.
  pair_ranks={};maximum=0
  for h in a.by_donor[j]:
   for r in a.by_donor[j]:
    if h==r:continue
    columns=[]
    for i,(vv,Fiv) in inverse_protected[j].items():
     if h in vv and r in vv:
      t=vv.index(h);columns.append(Fiv[:,3*t:3*t+3])
    Z=np.hstack(columns) if columns else np.zeros((48,0),dtype=np.uint8);rank=a.rank(Z);need(rank<=27,'protected uniform propagation bound for every actual quotient pair')
    need(not np.any(a.mm(maps[j][r][:3,:48],Z)),'protected propagated fibres lie in the observed quotient kernel')
    pair_ranks[f'{h}/{r}']=rank;maximum=max(maximum,rank)
  propagation[j]={'ordered_distinct_pairs':len(pair_ranks),'maximum':maximum,'ranks':pair_ranks};need(len(pair_ranks)==756,'complete ordered quotient-pair census')
  E=np.array(early['full'][str(j)]['matrix'],dtype=np.uint8);owners=early['full'][str(j)]['row_owners'];need(E.shape==(480,480) and len(owners)==480 and a.rank(E)==480,'actual complete two-copy early frame')
  need([o[1] for o in owners]==list(range(480)),'actual early owner positions')
  expected_planes=[h for h in sorted(a.by_donor[j]) for _ in range(a.quota[j,h])];need([o[0] for o in owners]==expected_planes,'every early row is at its actual native plane quota')
  for h in a.by_donor[j]:
   ix=[r for r,o in enumerate(owners) if o[0]==h];local=E[ix];F=maps[j][h];two=np.block([[F,np.zeros_like(F)],[np.zeros_like(F),F]])
   need(a.rank(local)==len(ix),'each local early owner group is independent')
   if len(ix)==15:need(a.rank(np.vstack([two,local]))==30,'half quota consists of genuine two-copy quotient rows')
   elif len(ix)==30:need(a.rank(np.vstack([two,local]))==30,'full quota is exactly the genuine two-copy quotient space')
   elif len(ix)==45:need(a.rank(np.vstack([local,two]))==45,'singleton quota contains both genuine quotient copies')
   else:raise ValueError('unknown actual quota')
  for m in range(5):
   C=np.array(early['components'][f'{j}/{m}']['matrix'],dtype=np.uint8);need(C.shape==(96,96) and a.rank(C)==96,'all fifteen literal component early frames are full')
  full_early.append({'donor':j,'rank':480,'genuine_quota_rows':480,'protected_propagation_maximum':maximum})
 fibre_records=[];mutation_failures=0;mutated=W.copy();mutated[ports.index(spreads[0][0]),0]^=1
 for i in range(120):
  if not a.planes[642]<=a.adj[i]:continue
  first=donors[0];off=[h for h in a.by_donor[first] if h!=642 and a.planes[h]<=a.adj[i]];K=previous.null_basis(np.vstack([maps[first][h] for h in off]),a);need(K.shape==(240,15),'whole off-H inverse-fibre dimension fifteen')
  visible=[r for r,D in enumerate(ports) if a.charts[D]<=a.adj[i]];need(len(visible)==15,'all fifteen actual visible D outputs')
  outputs=[];mutated_outputs=[]
  for s,j in enumerate(donors):
   offj=[h for h in a.by_donor[j] if h!=642 and a.planes[h]<=a.adj[i]];need(not np.any(a.mm(np.vstack([maps[j][h] for h in offj]),K)),'one whole inverse fibre serves every actual donor')
   outputs.append(a.mm(W[np.ix_(visible,range(15*s,15*s+15))],a.mm(maps[j][642],K)))
   mutated_outputs.append(a.mm(mutated[np.ix_(visible,range(15*s,15*s+15))],a.mm(maps[j][642],K)))
  need(a.rank(outputs[0])==15 and all(np.array_equal(outputs[0],R) for R in outputs[1:]),'full common fifteen-dimensional native-port readout')
  LK=np.array(literal_fibres[str(i)]['kernel'],dtype=np.uint8);need(LK.shape==(240,15) and a.rank(np.hstack([K,LK]))==15,'literal supplied fibre is the entire independently recovered space')
  need(literal_fibres[str(i)]['ports']==[ports[r] for r in visible],'literal readout lists the actual native ports')
  stored=a.mm(W[np.ix_(visible,range(15))],a.mm(maps[first][642],LK));need(np.array_equal(stored,np.array(literal_fibres[str(i)]['readout'],dtype=np.uint8)),'literal receiver readout agrees with direct source/port multiplication')
  mutation_failures+=int(a.rank(mutated_outputs[0])!=15 or any(not np.array_equal(mutated_outputs[0],R) for R in mutated_outputs[1:]))
  fibre_records.append({'receiver':i,'native':i in a.native,'ports':[ports[r] for r in visible],'kernel_rank':15,'readout_rank':15})
 need(len(source_records)==189 and sum(x['native'] for x in source_records)==176,'all source counts')
 need(len(fibre_records)==36 and sum(x['native'] for x in fibre_records)==34 and mutation_failures>0,'all H views and actual port-mutation sensitivity')
 payload=(json.dumps({'source_cuts':source_records,'readouts':fibre_records,'early':full_early,'protected_propagation':propagation},sort_keys=True,separators=(',',':'))+'\n').encode();(out/'REVIEW-CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_INDEPENDENT_FULL45_LOCAL_H642_SOURCES','all45_ports':True,'source_geometric_cuts':189,'source_native_cuts':176,'geometric_common_full_readouts':36,'native_common_full_readouts':34,
  'source_bank_dimension':240,'source_width':15,'provider_rank':44,'paid_logical_complement_dimension':1,'actual_early_bases':full_early,'protected_ordered_pair_census':2268,
  'protected_uniform_upper':27,'generic_uniform_upper_per_module':45,'full_uniform_propagation_upper':207,'full_saturation_threshold':225,'port_mutation_failed_views':mutation_failures,
  'independent_of_author_executable':True,'physical_compiler_review_deferred_to_root':True,'joint_two_H_width12':False,'complete_global_supplier':False,'new_complete_kappa':False,'certificate_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],189,176,36,34,44,207,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
