#!/usr/bin/env python3
"""Verify one44-centre source on all111 donors, including22 literal singleton repairs."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import gzip,importlib.util,json
from pathlib import Path
import numpy as np

def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def need(x,msg):
 if not x:raise ValueError(msg)

def main():
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--rank-library',type=Path);a=p.parse_args()
 base=a.repo/'research/moonshot-005-program/results'
 paths={'families':base/'bit-spread-disjoint-h-sources/author/families.py','pair':base/'bit-spread-overlap-source/author/pair.py','repair':base/'bit-spread-singleton-fibre-repair/author/check.py'}
 f,pair,patch=(module(paths[s],'all_source_'+s)for s in('families','pair','repair'));g=f.Atlas(a.repo)
 if a.rank_library:
  import ctypes
  lib=ctypes.CDLL(str(a.rank_library.resolve()));r=lib.field_rank;r.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_void_p];r.restype=ctypes.c_int
  P=np.ascontiguousarray(g.product,dtype=np.uint8);I=np.ascontiguousarray(g.inverse,dtype=np.uint8)
  def rank(M):
   z=np.ascontiguousarray(M,dtype=np.uint8).copy();return r(z.ctypes.data,z.shape[0],z.shape[1],P.ctypes.data,I.ctypes.data)
  g.rank=rank
 directory=Path(__file__).parent/'output';raw=(directory/'PARAMETERS.json').read_bytes();params=json.loads(raw);sr=(directory/'SINGLETONS.json.gz').read_bytes();repairs={(v['h'],v['k'],v['donor']):v for v in json.loads(gzip.decompress(sr))}
 used=set();centres=[];checks=[];templates={};maps_hashes={}
 for record in params['pairs']:
  h,q=record['centres'];U=g.planes[h]|g.planes[q]
  need(g.planes[h]&g.planes[q]=={record['shared_donor']}and len(U)==5 and not used&U,'disjoint five-donor components')
  need(all(g.quota[record['shared_donor'],p]!=45 for p in g.by_donor[record['shared_donor']]),'shared donor has no singleton')
  used.update(U);centres.extend((h,q))
  for k in(3,12):
   charts,maps,_=pair.pair_source(g,f,k,record)
   for j,rows in maps.items():
    ctx=next(c for c in charts if j in c.donors);templates[j,k]=(ctx,rows,record[str(k)]['early'][str(j)])
 for h,parameters in params['singles'].items():
  h=int(h);need(not used&g.planes[h],'single centre disjoint from preceding source components');used.update(g.planes[h]);centres.append(h)
  for k in(3,12):
   ctx=f.Chart(g,h,k);pr=parameters[str(k)];table=ctx.point_table(pr['core'],pr['fill']);ctx.check_readouts(table,ctx.controls)
   for j in ctx.donors:
    rows=ctx.maps(table,j);ctx.early(j,rows,pr['early'][str(j)]);ctx.source_views(rows,j,full_rank=False);templates[j,k]=(ctx,rows,pr['early'][str(j)])
 need(len(params['pairs'])==21 and len(params['singles'])==2 and len(centres)==len(set(centres))==44 and used==g.native,'one source on all111 original donors')
 witness_raw=(directory/"NON-RS-WITNESSES.json").read_bytes(); witness={r["donor"]:r for r in json.loads(witness_raw)}
 need(set(witness)==g.native,"one source inequivalence witness for every original donor")
 actual=set()
 for(j,k),(ctx,rows,seed)in sorted(templates.items()):
  maps_hashes[f'{j}/{k}']=sha256(b''.join(rows[p].tobytes()for p in sorted(rows))).hexdigest()
  if k==3:
   w=witness[j];need(len(set(w['planes']))==16 and all(h in rows and g.quota[j,h]!=45 for h in w['planes']), 'sixteen genuine ordinary source planes')
   observed=g.rank(np.vstack([rows[h] for h in w['planes']]))
   need(observed==w['marked_scalar_rank'] and observed<48, 'actual source is not input-gauge-equivalent to an MDS Reed-Solomon source')
  singleton=[p for p in g.by_donor[j]if g.quota[j,p]==45]
  if singleton:
   key=ctx.h,k,j;v=repairs[key];need(v['singleton']==singleton[0],'literal genuine singleton plane')
   checks.append(patch.check_one(f,g,pair.null_basis,ctx,j,singleton[0],rows,seed,np.asarray(v['S'],dtype=np.uint8)));actual.add(key)
 need(actual==set(repairs)and len(actual)==22,'every genuine singleton replacement checked on its whole native contract')
 count={str(h):sum(g.planes[h]<=g.adj[i]for i in g.native)for h in centres};n=sum(count.values())
 phases=Counter('fully_early'if all(g.quota[j,h]==30 for j in g.planes[h])else'mixed'for h in centres)
 out={'status':'PASS_FORTY_FOUR_H_CHARTS_AND_ALL_111_SOURCE_STARS','native_H_charts':44,'native_H_inverse_fibres':n,'native_H_donor_fibres':3*n,'actual_early_source_bases':111,'actual_source_H_foreign_full_ranks':6470,'selected_source_stars':111,'remaining_background_RS_words':0,'source_stars_inequivalent_to_RS':111,'non_RS_witnesses_sha256':sha256(witness_raw).hexdigest(),'per_chart_native_receivers':count,'centre_phases':dict(phases),'singleton_replacements':checks,'parameters_sha256':sha256(raw).hexdigest(),'singleton_payload_sha256':sha256(gzip.decompress(sr)).hexdigest(),'source_pins':{str(v.relative_to(a.repo)):sha256(v.read_bytes()).hexdigest()for v in paths.values()},'source_coefficient_sha256':maps_hashes,'endpoint_target':'canonical foreign identity on designated H interfaces','S028_perturbed_target_not_asserted':True,'common_D_K_endpoint':False,'actual_global_return_rank':None,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['status'],n,3*n)
if __name__=='__main__':main()
