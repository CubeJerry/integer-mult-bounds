#!/usr/bin/env python3
"""Independent initial-chart graphs, sharp whole-field controls and cache repair."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
PROOF='dbf00c71814d1c274cfd5bb474fb063e1b8c07e1a30c523437deaf8090cbc58c'
SOURCES=[('paid59','A/lower-history59-paid/WORD.json','dd60233b57be5fdef83b86a2d2b816e665e3d939850da94b680838d1d6d178ce',1380),('five46','A/shared-proper-five46/WORD.json','14503b00ad6f9d1e4d85ec09769a51c14eca36d61edabe19d9ae2907608c7501',1364),('liberated55','C/mask-preserving-reset/LIBERATED-SOURCE-WORD.json','4fe64237569a99a41578a378145a7df7ceac8394d33c82ca4f5e1be166b8859c',350)]
W26=[5,13,14,31,33,52,57,58,59,60,82,83,86,87,89,91,96,97,98,99,100,101,105,106,107,109]
DONORS=[13,14,31,33,52,57,58,59,60,82,83,86,87,96,97,100,101,105,109]
CACHED='7df1fc8f696545185c417c6df4161b324869bf084b503138506425510e841fa2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sink_order(rows,W):
 remaining=set(W);order=[];batches=[]
 while remaining:
  ready=sorted(i for i in remaining if not(set(rows[i])&remaining))
  if not ready:return None
  batches.append(ready);order+=ready;remaining-=set(ready)
 return order,batches
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();root=a.work/'R/initial-chart-cut';require(sha(root/'PROOF.md')==PROOF,'final root proof pin')
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};reports={};gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6)
 def native(w):
  raw=(a.repo/w['source_path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native source pin')
  R=json.loads(raw)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
  for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'all actual native charts')
  return C
 def access(w,C,tr,cut):
  v,at=tr[cut];U=sorted(set(range(N))-set(w['targets']));um=sum(1<<i for i in U);rows={i:set()for i in U};memo={};ledger={}
  for n,z in v.items():
   if not z&um:continue
   supp={i for i in U if z>>i&1};dest=[]
   for i in U:
    key=(at[n],i)
    if key not in memo:memo[key]=len(C[at[n]])<=7 and len(rref(C[at[n]]+C[f'F{i}'])[0])==7
    if memo[key]:rows[i]|=supp;dest.append(i)
   ledger[n]={'chart':at[n],'unknown_support':sorted(supp),'accessible_targets':dest}
  return {i:sorted(z)for i,z in rows.items()},ledger
 for label,path,pin,cut in SOURCES:
  p=a.work/path;require(sha(p)==pin,'source word pin');w=json.loads(p.read_text());C=native(w);stats,tr,_=replay(w,collect=True);v,at=tr[cut]
  require(w['carrier_interface_before_operation']==cut,'literal declared cut');rows,ledger=access(w,C,tr,cut);U=sorted(rows);W=U if label!='liberated55'else W26;ordered=sink_order(rows,W);require(ordered is not None,'actual explicit acyclic witness')
  if label in ['paid59','five46']:
   keys=[26,61,67,72,84]if label=='paid59'else[18,26,61,67,68,71,72,81,84,85]
   require(rows=={i:([5,15]if i in keys else [])for i in U},'exact entire acyclic graph')
   require(all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(N)),'all originals already raw Hub')
  else:
   require(set(W26)==set(DONORS)|{5,89,91,98,99,106,107},'26 witness is19 donors plus7 native roles')
   require(ordered[1][0]==[5,89,91,98,99,106,107]and len(ordered[1])==2,'exact two-level witness')
   require(all(set(rows[i])&set(W26)<=set(ordered[1][0])for i in DONORS),'all witness arcs go donors to seven sinks')
  tail=w['operations'][cut:];owned=set(v)-originals;require(all(v[n]>>N==0 for n in owned),'pure-X actual cut owners')
  for i in U:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','every unfinished Y raw ground')
  moves=[o for o in tail if o[0]=='MOVE'];clears=[o for o in tail if o[0]=='CLEAR'];require(len(tail)==len(moves)+len(clears),'suffix has only original closures and CLEARs')
  require({o[1]for o in clears}==owned and len(clears)==len(owned),'every actual owned lifetime ends')
  for o in moves:require(o[1]in originals and o[2]==('Hub'if o[1].startswith('X')else f'F{o[1][1:]}'),'suffix only direct final original closures')
  profile=stats['movement_profile'];floor=dict(profile);floor[1]=floor.get(1,0)+len(W);q,low=moment(profile),moment(floor);require(low[0]>limit[1],'exact witnessed floor exceeds necessary limit')
  report={'word_sha256':pin,'cut':cut,'stats':stats,'actual_access_rows':rows,'field_access_ledger':ledger,'acyclic_witness':W,'sink_order':ordered[0],'sink_batches':ordered[1],'minimum_future_owned_descents':len(W),'suffix_original_MOVEs':len(moves),'suffix_CLEARs':len(clears),'closed_partial_price':record(q),'completion_floor':record(low),'excess_above_necessary_allowance':record((low[0]-limit[1],low[1]-limit[0]))}
  if label in ['paid59','five46']:
   cp=root/'control'/f'{label.upper()}-ALL111-WORD.json';cw=json.loads(cp.read_text());native(cw);cs,ct,_=replay(cw,collect=True)
   require(cw['targets']==list(range(N))and cw['operations'][:cut]==w['operations'][:cut],'actual all111 control preserves exact frozen prefix')
   require(cs['movement_profile']==floor,'all111 control attains complete exact floor')
   births={o[1]for o in w['operations']if o[0]=='INIT'};newborn={o[1]for o in cw['operations']if o[0]=='INIT'}-births;require(len(newborn)==len(U),'one actual new owner per missing endpoint')
   owned_moves=[]
   for k,o in enumerate(cw['operations'][cut:],cut):
    if o[0]=='MOVE'and o[1]in births|newborn:
     require(o[1]in newborn and ct[k][1][o[1]]=='Hub'and len(C[o[2]])==7,'each new owned MOVE is actual unit Hub-to-facet descent');owned_moves.append(o)
   require(len(owned_moves)==len(U),'exact52 or65 additional owned descents')
   report['sharp_all111_control']={'word_sha256':sha(cp),'stats':cs,'new_owners':len(newborn),'actual_new_unit_descents':len(owned_moves),'all222_endpoint_identity':True,'movement_floor_attained':True}
  else:
   cp=root/'control/NATIVE-CACHED57-WORD.json';require(sha(cp)==CACHED,'cached57 final pin');cw=json.loads(cp.read_text());CC=native(cw);cs,ct,_=replay(cw,collect=True);nc=cw['carrier_interface_before_operation'];require(nc==392,'cached source cut392');nv,na=ct[nc]
   require(cw['targets']==sorted(set(w['targets'])|{61,67}),'two actual known-coordinate completions')
   expected=[]
   for i in DONORS:expected += [['INIT',f'RAW_NATIVE_SNAPSHOT_{i}',f'L{i}'],['ADD',f'X{i}',f'RAW_NATIVE_SNAPSHOT_{i}']]
   require(cw['operations'][:38]==expected and cw['operations'][38:388]==w['operations'][:350],'native snapshot prelude then literal old prefix')
   require(cw['operations'][388:392]==[['ADD','MASK_RESET_RAW_61','Y61'],['MOVE','Y61','F61'],['ADD','MASK_RESET_RAW_67','Y67'],['MOVE','Y67','F67']],'real known raw reads and native receiver arrivals')
   for n,z in v.items():
    if n not in {'Y61','Y67'}:require(nv[n]==z and CC[na[n]]==C[at[n]],('every old cut field unchanged',n))
   for i in DONORS:
    n=f'RAW_NATIVE_SNAPSHOT_{i}';require(nv[n]==1<<i and na[n]==f'L{i}','actual native raw donor cache')
    require([o for o in cw['operations']if o[0]=='ADD'and o[2]==n]==[['ADD',f'X{i}',n]]and not any(o[0]=='MOVE'and o[1]==n for o in cw['operations']),'one raw capture and no cache MOVE')
   require(sum(na[f'X{i}']==f'L{i}'for i in range(N))==92 and all(nv[f'X{i}']==1<<i for i in range(N)),'92 native raw originals, all originals raw')
   for i in [61,67]:require(nv[f'Y{i}']==(1<<(N+i))^(1<<i)and na[f'Y{i}']==f'F{i}','two completed endpoints at actual facets')
   for i in set(range(N))-set(cw['targets']):require(nv[f'Y{i}']==1<<(N+i)and na[f'Y{i}']=='zero','remaining54 actual raw ground Ys')
   nrows,nledger=access(cw,CC,ct,nc);require(sink_order(nrows,W26)is None,'old26 witness no longer acyclic')
   cycles=[[i,j]for i in W26 for j in W26 if i<j and j in nrows[i]and i in nrows[j]];require(bool(cycles),'explicit real two-cycle in repaired source')
   require(cs['movement_profile']==profile and cs['counts']=={'INIT':82,'ADD':155,'MOVE':301,'CLEAR':82}and cs['dirty_CLEAR']==82,'whole repaired source invoice, zero additional MOVE')
   # Missing snapshot is invisible at endpoints but invalidates the actual source contract.
   bad=copy.deepcopy(cw);bad['operations'].remove(['ADD','X13','RAW_NATIVE_SNAPSHOT_13']);_,badtr,_=replay(bad,collect=True);require(badtr[nc-1][0]['RAW_NATIVE_SNAPSHOT_13']==0,'endpoint-pass/cache-source-fail negative control')
   bad=copy.deepcopy(cw);bad['operations'].remove(['ADD','MASK_RESET_RAW_61','Y61'])
   try:replay(bad)
   except ValueError as e:known_negative=str(e)
   else:raise ValueError('missing actual known-coordinate update accepted')
   report['native_cached57']={'word_sha256':CACHED,'cut':nc,'stats':cs,'native_originals':92,'native_raw_donor_caches':19,'same_full_movement_profile':True,'all_old_cut_rows_except_two_Y_unchanged':True,'new_actual_access_rows':nrows,'actual_two_cycles_in_old_witness':cycles,'missing_native_capture_passes_endpoints_but_fails_source_contract':True,'missing_known_coordinate_ADD_rejection':known_negative,'scope':'Different actual prefix and source graph. Gives actual native data without asserting simultaneous access to incomparable charts.'}
  reports[label]=report
  print('PASS',label,'witness',len(W),flush=True)
 result={'status':'PASS_INDEPENDENT_INITIAL_CHART_TRANSCRIPT_AND_PHYSICAL_CONTROLS','proof_sha256':PROOF,'retained_acyclic_proof_sha256':sha(a.repo/'research/moonshot-005-program/results/endpoint-side-information/PROOF.md'),'native_cached57_word_sha256':CACHED,'sources':reports,'scope':'Independent exact native Fraction geometry, all222 endpoint columns, complete initial-chart access graphs, explicit acyclic witnesses, actual source preservation and complete movement floors. Universal nonlinear proof reviewed in accompanying markdown. All five global foundations and complete supplier remain open; no kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
