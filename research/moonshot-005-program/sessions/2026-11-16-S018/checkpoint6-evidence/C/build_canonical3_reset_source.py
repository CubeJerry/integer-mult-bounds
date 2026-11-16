#!/usr/bin/env python3
"""Actual known48 source, canonical3 modes, proper7 sums and native57 caches."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
PIN='cc505aaf4aee5e1995b4db22f9b53609856d3ecdc3ea1eb0797f2584e375dfee'
PRIMARY=[4,74,78];FIELDS=['ZFIRST3','ZFIRST4','ZFIRST5']
def gname(g):return 'ASC_GROUP_'+'_'.join(map(str,g))
def save(p,z):
 raw=(json.dumps(z,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();p=a.work/'A/ascending-canonical3/WORD.json';require(hashlib.sha256(p.read_bytes()).hexdigest()==PIN,'source pin');old=json.loads(p.read_text());os,ot,_=replay(old,collect=True);oc=old['carrier_interface_before_operation'];ov,oa=ot[oc]
 sr=(a.repo/old['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==old['source_sha256'],'native source pin');R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in old['charts'].items()}
 S=sorted(set(old['targets'])|{61,67});U=sorted(set(range(N))-set(S));sm=sum(1<<i for i in S);um=sum(1<<i for i in U);groups={}
 for i in U:
  g=tuple(k for k in PRIMARY if sum(x*y for x,y in zip(R[k],R[i]))==0);groups.setdefault(g,[]).append(i)
 donor=sorted(i for g,ds in groups.items()if g for i in ds);native=sorted(set(range(N))-set(donor));require(len(S)==48 and len(donor)==57 and len(native)==54,'source partition')
 original={f'{p}{i}'for p in ['X','Y']for i in range(N)};oldowners=set(ov)-original;active={gname(g)for g in groups if g}|set(FIELDS);zeroowners=sorted(oldowners-active);require(len(active)==10 and len(zeroowners)==91,'old named owner partition')
 for n in zeroowners:require(ov[n]&um==0 and ov[n]>>N==0,'omitted old owners known-S only')
 for aa,f in zip(PRIMARY,FIELDS):
  canonical=(1<<aa)^sum(1<<i for i in range(N)if sum(x*y for x,y in zip(R[aa],R[i]))==0)
  require((ov[f]^canonical)&um==0 and oa[f]=='M1','old canonical quotient')
 variants={};traces={};results={}
 for matched in [False,True]:
  label='MATCHED-CUT-WORD'if matched else'LIBERATED-CACHED48-WORD';ops=[];owned=[]
  def add(*rows):ops.extend([list(z)for z in rows])
  for i in S:
   n=f'CANONICAL_RESET_RAW_{i}';owned.append(n);add(('INIT',n,f'L{i}'),('ADD',f'X{i}',n),('MOVE',n,'zero'))
  for i in donor:
   n=f'CANONICAL_NATIVE_RAW_{i}';owned.append(n);add(('INIT',n,f'L{i}'),('ADD',f'X{i}',n))
  for g,ds in sorted(groups.items()):
   if not g:continue
   n=gname(g);owned.append(n);add(('INIT',n,n))
   for i in ds:add(('MOVE',f'X{i}',n),('ADD',f'X{i}',n),('MOVE',f'X{i}','Hub'))
  for aa,f in zip(PRIMARY,FIELDS):
   owned.append(f);add(('INIT',f,'Hub'))
   for i in donor:
    if sum(x*y for x,y in zip(R[aa],R[i]))==0:add(('ADD',f'X{i}',f))
   add(('MOVE',f,'M1'))
  for i in S:
   add(('ADD',f'CANONICAL_RESET_RAW_{i}',f'Y{i}'))
   if not matched or i in old['targets']:add(('MOVE',f'Y{i}',f'F{i}'))
  if matched:
   for i in native:
    if oa[f'X{i}']=='Hub':add(('MOVE',f'X{i}','Hub'))
   for n in zeroowners:owned.append(n);add(('INIT',n,oa[n]))
  cut=len(ops);cutnative=[i for i in native if not matched or oa[f'X{i}']==f'L{i}']
  for i in cutnative:add(('MOVE',f'X{i}','Hub'))
  for i in range(N):
   if i not in S or(matched and i not in old['targets']):add(('MOVE',f'Y{i}',f'F{i}'))
  add(*[('CLEAR',n)for n in owned])
  w={k:copy.deepcopy(old[k])for k in ['source_path','source_sha256','charts']}
  w.update(schema='actual-canonical3-reset-source-v1',base_word_sha256=PIN,operations=ops,targets=S,released_carriers=cutnative,carrier_interface_before_operation=cut,
   source_interface={'actual_ground_raw_coordinates':S,'actual_ground_raw_names':{str(i):f'CANONICAL_RESET_RAW_{i}'for i in S},'actual_native_raw_donor_caches':{str(i):f'CANONICAL_NATIVE_RAW_{i}'for i in donor},'proper_unknown_groups':{'_'.join(map(str,g)):ds for g,ds in groups.items()if g},'proper_group_fields':[gname(g)for g in sorted(groups)if g],'canonical_fields':FIELDS,'canonical_primaries':PRIMARY,'canonical_chart':'M1','raw_native_originals':cutnative,'all48_known_targets_complete_at_cut_facets':not matched,'same_old_named_charts':matched,'continuation_before_operation':cut},
   scope='Actual known48 ground source,57 native raw donor caches,seven proper unknown sums and three canonical unknown modes atM1. All48 known-coordinate outputs complete in the closed word. Matched variant preserves every old named cut unknown-X/Y column and chart; liberated variant leaves54 raw native originals. No all111 supplier or kappa.')
  stats,tr,_=replay(w,collect=True);v,at=tr[cut];variants[label]=w;traces[label]=tr
  require(stats['movement_profile']=={1:67,2:37,3:4,4:1,5:37,6:19,7:165},'complete expected native profile')
  require(stats['counts']=={'INIT':206 if matched else 115,'ADD':306,'MOVE':330,'CLEAR':206 if matched else 115}and stats['dirty_CLEAR']==115,'complete actual source invoice')
  for i in S:require(v[f'CANONICAL_RESET_RAW_{i}']==1<<i and at[f'CANONICAL_RESET_RAW_{i}']=='zero','actual raw known source at ground')
  for i in donor:require(v[f'CANONICAL_NATIVE_RAW_{i}']==1<<i and at[f'CANONICAL_NATIVE_RAW_{i}']==f'L{i}','actual native unknown side cache')
  for g,ds in groups.items():
   if g:require(v[gname(g)]==ov[gname(g)]==sum(1<<i for i in ds)and at[gname(g)]==oa[gname(g)],'each proper unknown group preserved exactly')
  for aa,f in zip(PRIMARY,FIELDS):require(v[f]==ov[f]&um and at[f]=='M1','actual canonical unknown mode without known offset')
  for i in range(N):require(v[f'X{i}']==1<<i,'all cut originals raw')
  if matched:
   for n,z in ov.items():require((v[n]^z)&~sm==0 and C[at[n]]==C[oa[n]],('old named unknown/Y columns and actual charts',n))
  else:
   require(len(cutnative)==54,'54 raw native originals')
   for i in S:require(v[f'Y{i}']==(1<<(N+i))^(1<<i)and at[f'Y{i}']==f'F{i}','all48 known targets complete at facets')
   for i in U:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','all63 unknown receivers raw ground')
  ownrows=[z for n,z in v.items()if n not in original];require(all(z>>N==0 for z in ownrows)and len(binary_basis(ownrows))==105,'pureX owned rank105')
  a.out.mkdir(parents=True,exist_ok=True);pin=save(a.out/(label+'.json'),w);results[label]={'word_sha256':pin,'cut':cut,'stats':stats,'raw_native_originals':cutnative,'actual_pure_X_owned_rank':105,'same_old_named_unknown_and_Y_columns_and_charts':matched,'all48_targets_complete_at_cut_facets':not matched}
 # Pin source semantics independently of partial endpoint correctness.
 w=variants['LIBERATED-CACHED48-WORD'];cut=w['carrier_interface_before_operation'];v,at=traces['LIBERATED-CACHED48-WORD'][cut];controls=[]
 tests=[('missing native raw donor capture',['ADD','X5','CANONICAL_NATIVE_RAW_5']),('missing actual proper group input',['ADD','X5',gname(tuple(PRIMARY))]),('missing real Hub mode input',['ADD','X5','ZFIRST3']),('missing actual common descent',['MOVE','ZFIRST3','M1']),('missing actual known source acquisition',['ADD','X0','CANONICAL_RESET_RAW_0']),('missing source lifetime end',['CLEAR','ZFIRST3'])]
 for label,event in tests:
  bad=copy.deepcopy(w);k=bad['operations'].index(event);bad['operations'].pop(k);nc=cut-(k<cut)
  try:
   _,tt,_=replay(bad,collect=True);vv,aa=tt[nc];require(vv==v and all(C[aa[n]]==C[at[n]]for n in v),'actual cut source identity')
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':str(e)})
  else:raise ValueError(('accepted source mutation',label))
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(results['LIBERATED-CACHED48-WORD']['stats']['movement_profile']);oq=moment(os['movement_profile']);direct=moment({7:222,1:48})
 result={'status':'PASS_ACTUAL_CANONICAL3_RESET_SOURCE_AND_LIBERATED_NATIVE_INTERFACE','source_word_sha256':PIN,'native_source_sha256':old['source_sha256'],'source_known_coordinates_S48':S,'source_unknown_coordinates_U63':U,'actual_moving_unknown_donors':donor,'unknown_inputs_remaining_native':groups[()], 'actual_group_sizes':{'_'.join(map(str,g)):len(ds)for g,ds in groups.items()if g},'canonical_mode_count':3,'mode_rank_mod_S48':len(binary_basis(v[f]&um for f in FIELDS)),'variants':results,'whole_moment':record(q),'movement_change_from_ascending_source':record((q[0]-oq[1],q[1]-oq[0])),'extra_movement_over_actual_known48_direct_baseline':record((q[0]-direct[1],q[1]-direct[0])),'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'controls':controls,'scope':'Two distinct real source contracts. Same-old-chart version matches every original and old-owner unknown-X/Y column but changes known-S offsets, so use the retained conditional reset/Hub-invertibility theorem for continuations. Liberated version has54 raw native originals and48 completed Y at facets, with57 actual native unknown caches. Its additional native side data is not a simultaneous multi-chart read grant. All five global foundations and full111 supplier remain open; no kappa.'}
 save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
