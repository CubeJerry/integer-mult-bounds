#!/usr/bin/env python3
"""Independent current-port fullwidth15 two-H shared-source literal review."""
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
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','pair_independent_geometry');family,a,previous=g.context(repo)
 pins=here/'SOURCE-PINS.json'
 if pins.exists():
  for p,d in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'source pin '+p)
 raw=read(author/'output/COEFFICIENTS.json.gz');early=read(author/'output/EARLY.json.gz');stored=read(author/'output/FIBRES.json.gz');twelve=read(author/'PAIR-TWELVE.json.gz')
 protected=read(base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz');old=read(base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz')
 current=read(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');selected=set(current['selected_D'])
 maps={int(j):{int(h):np.array(M,dtype=np.uint8) for h,M in vv.items()} for j,vv in raw['source_maps'].items()};donors=[0,45,61,62,100]
 need(sorted(maps)==donors and raw['shared_donor']==61 and raw['centres']==[263,642],'one literal five-donor source tuple and named shared donor')
 source_records=[];early_records=[];propagation={};source_native=0
 for j in donors:
  need(set(maps[j])==set(a.by_donor[j]),'all actual source planes')
  for h,M in maps[j].items():
   P=np.array(protected['maps'][str(j)][str(h)],dtype=np.uint8);Q=np.array(twelve['maps'][str(j)][str(h)],dtype=np.uint8);expected=np.zeros((15,240),dtype=np.uint8);expected[:3,:48]=P;expected[3:,48:]=Q
   need(M.shape==(15,240) and np.array_equal(M,expected),'exact protected3 plus current-port complementary12 at every actual source plane')
  inv={};views={i:sorted(h for h in a.by_donor[j] if a.planes[h]<=a.adj[i]) for i in sorted(a.adj[j])}
  for i,vv in views.items():
   need(len(vv)==16 and a.rank(np.vstack([maps[j][h] for h in vv]))==240,'entire width15 geometric source cut')
   inv[i]=g.inverse(np.vstack([maps[j][h][:3,:48] for h in vv]),a);source_records.append([j,i]);source_native+=i in a.native
  bound=36 if j in [0,61,62] else 27;ranks={};maximum=0
  for h in a.by_donor[j]:
   for r in a.by_donor[j]:
    if h==r:continue
    cols=[]
    for i,vv in views.items():
     if h in vv and r in vv:
      t=vv.index(h);cols.append(inv[i][:,3*t:3*t+3])
    Z=np.hstack(cols) if cols else np.zeros((48,0),dtype=np.uint8);rank=a.rank(Z);need(rank<=bound and not np.any(a.mm(maps[j][r][:3,:48],Z)),'protected uniform propagation at every ordered actual quotient pair')
    ranks[f'{h}/{r}']=rank;maximum=max(maximum,rank)
  need(len(ranks)==756,'complete protected propagation census');propagation[j]={'all_pair_ranks':ranks,'maximum':maximum,'declared_upper':bound,'full_upper':bound+180}
  E=np.array(early['full'][str(j)]['matrix'],dtype=np.uint8);owners=early['full'][str(j)]['row_owners'];need(E.shape==(480,480) and a.rank(E)==480,'one actual full two-copy early basis per donor')
  need(owners==[[h,r] for r,h in enumerate([h for h in sorted(a.by_donor[j]) for _ in range(a.quota[j,h])])],'literal actual source owner order and quotas')
  for h in a.by_donor[j]:
   rows=[r for r,(q,_) in enumerate(owners) if q==h];local=E[rows];F=maps[j][h];pair=np.block([[F,np.zeros_like(F)],[np.zeros_like(F),F]])
   need(a.rank(local)==len(rows),'independent local early records')
   if len(rows) in [15,30]:need(a.rank(np.vstack([pair,local]))==30,'early records are genuine two-copy quotient forms')
   else:need(len(rows)==45 and a.rank(np.vstack([local,pair]))==45,'singleton includes both genuine quotient copies')
  for k in [3,12]:
   Ek=np.array(early['components'][f'{j}/{k}']['matrix'],dtype=np.uint8);need(Ek.shape==(32*k,32*k) and a.rank(Ek)==32*k,'both component early frames')
  early_records.append({'donor':j,'rank':480,'protected_pair_maximum':maximum,'uniform_full_upper':bound+180})
 Hrecords=[];fibres={};mutation_failures=0
 for h in [263,642]:
  hh=raw['H'][str(h)];ds=sorted(a.planes[h]);ports=[D for D,Q in enumerate(a.charts) if a.planes[h]<=Q];p3=[D for D in ports if D in selected];p12=[D for D in ports if D not in selected]
  need(hh['donors']==ds and hh['ports']==ports and hh['protected_ports']==p3 and hh['complement_ports']==p12 and len(p3)==9 and len(p12)==36,'literal current global protected/complement port partition')
  need(twelve['H'][str(h)]['ports']==p12 and twelve['H'][str(h)]['donors']==ds,'fresh complementary literal is bound to the current allocation')
  P3=np.array(old['Hwords']['263'] if h==263 else protected['Bword'],dtype=np.uint8);P12=np.array(twelve['H'][str(h)]['word'],dtype=np.uint8);W=np.array(hh['word'],dtype=np.uint8);expected=np.zeros((45,45),dtype=np.uint8)
  for ps,P,offset,width in [(p3,P3,0,3),(p12,P12,3,12)]:
   for q,D in enumerate(ps):
    for s in range(3):expected[ports.index(D),15*s+offset:15*s+offset+width]=P[q,width*s:width*s+width]
  need(np.array_equal(expected,W) and a.rank(P12)==36 and a.rank(W)==(45 if h==263 else 44),'full current-port word embeds both components exactly')
  if h==642:
   complement=np.zeros((1,45),dtype=np.uint8);complement[0,0]=1;need(a.rank(np.vstack([W,complement]))==45,'one logical H642 complement suffices')
  allK=[];native=0;fibres[h]={};badW=W.copy();badW[ports.index(p3[0]),0]^=1
  for i in range(120):
   if not a.planes[h]<=a.adj[i]:continue
   off=[q for q in a.by_donor[ds[0]] if q!=h and a.planes[q]<=a.adj[i]];K=previous.null_basis(np.vstack([maps[ds[0]][q] for q in off]),a);need(K.shape==(240,15),'entire fullwidth off-H fibre')
   visible=[r for r,D in enumerate(ports) if a.charts[D]<=a.adj[i]];need(len(visible)==15,'all actual fifteen visible output ports');readouts=[];bad=[]
   for s,j in enumerate(ds):
    offj=[q for q in a.by_donor[j] if q!=h and a.planes[q]<=a.adj[i]];need(not np.any(a.mm(np.vstack([maps[j][q] for q in offj]),K)),'same full inverse fibre for all three donors')
    R=a.mm(maps[j][h],K);readouts.append(a.mm(W[np.ix_(visible,range(15*s,15*s+15))],R));bad.append(a.mm(badW[np.ix_(visible,range(15*s,15*s+15))],R))
   need(a.rank(readouts[0])==15 and all(np.array_equal(readouts[0],R) for R in readouts[1:]),'entire common fifteen-dimensional receiver readout')
   LK=np.array(stored[str(h)][str(i)]['kernel'],dtype=np.uint8);need(LK.shape==(240,15) and a.rank(np.hstack([K,LK]))==15,'stored fibre matches independent full kernel')
   need(stored[str(h)][str(i)]['ports']==[ports[r] for r in visible],'stored actual receiver-port identities')
   lr=a.mm(W[np.ix_(visible,range(15))],a.mm(maps[ds[0]][h],LK));need(np.array_equal(lr,np.array(stored[str(h)][str(i)]['readout'],dtype=np.uint8)),'stored receiver matrix bound to the literal source')
   if h==642:mutation_failures+=int(any(not np.array_equal(bad[0],R) for R in bad[1:]) or a.rank(bad[0])!=15)
   allK.append(K);native+=i in a.native;fibres[h][i]={'ports':[ports[r] for r in visible],'rank':15}
  core=a.rank(np.hstack(allK));need(len(allK)==36 and core==(214 if h==263 else 210),'complete shared fibre core dimension')
  Hrecords.append({'H':h,'donors':ds,'ports':ports,'provider_rank':a.rank(W),'geometric_readouts':36,'native_readouts':native,'core_rank':core})
 need(len(source_records)==315 and source_native==291 and sum(r['native_readouts'] for r in Hrecords)==67 and mutation_failures>0,'all source and H counts and physical mutation sensitivity')
 payload=(json.dumps({'source_cut_receivers':source_records,'early':early_records,'protected_propagation':propagation,'H':Hrecords,'readouts':fibres},sort_keys=True,separators=(',',':'))+'\n').encode();(out/'REVIEW-CERTIFICATE.json.gz').write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_INDEPENDENT_CURRENT_PORT_FULL45_TWO_H_PAIR','geometric_source_cuts':315,'native_source_cuts':291,'geometric_full_readouts':72,'native_full_readouts':67,
  'actual_early_bases':early_records,'H':Hrecords,'single_literal_shared_donor61_source':True,'protected_ordered_pair_census':3780,'full_uniform_upper_by_donor':{str(j):propagation[j]['full_upper'] for j in donors},
  'full_saturation_threshold':225,'port_mutation_failed_views':mutation_failures,'current_global_port_allocation_verified':True,'author_code_imported':False,'physical_compiler_review_deferred_to_root':True,'all111_sources':False,'complete_middle_return_or_invoice':False,'new_complete_kappa':False,'certificate_sha256':hashlib.sha256(payload).hexdigest()}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],315,291,72,67,45,44,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
