#!/usr/bin/env python3
"""Actual partial reset preserving all unknown mask columns at proper charts."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require
from ground_output_normalization import evaluate,inverse_add_word
from price_projection import moment,record
PIN='fd9ce4903aab198d234e6956a877e97241ed7268c7dba657064fa8ebf8cba84c'

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();raw=(a.work/'A/m0-masked19-pure-pruned55/WORD.json').read_bytes()
 require(hashlib.sha256(raw).hexdigest()==PIN,'actual unknown-mask source pin');b=json.loads(raw)
 sr=(a.repo/b['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==b['source_sha256'],'native root pin')
 before,bt,_=replay(b,collect=True);meta=b['masked_feedback'];cut=meta['continuation_before_operation'];ov,oa=bt[cut]
 common=meta['common'];fields=meta['fields'];parts=meta['fixed_disjoint_partition'];U=sorted(i for p in parts for i in p)
 masks=[sum(1<<i for i in p)for p in parts];S=sorted(set(b['targets'])|{61,67});sm=sum(1<<i for i in S);xm=(1<<N)-1
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};owners=sorted(set(ov)-originals)
 require(len(S)==57 and len(U)==19 and not set(S)&set(U),'actual known/unknown separation')
 require(all(ov[n]>>N==0 for n in owners),'pure original-Y cut signature')
 for n in owners:
  want=0
  for j,u in enumerate(masks):
   if n in {fields[j],f'MASK_SOURCE_{j}'}:want=u
  require(ov[n]&~sm==want,('entire actual unknown cut field',n))
 d=7;bb=34;require(oa[f'X{d}']==f'L{d}','actual released original for continuation')
 carry=[['MOVE',f'X{d}',common],['ADD',fields[0],f'X{d}'],['MOVE',f'X{d}','MASK_CORRECTION_0'],['ADD','MASK_SOURCE_0',f'X{d}'],['MOVE',f'X{d}','Hub'],['ADD',f'X{bb}',f'X{d}']]
 tail=copy.deepcopy(b['operations'][cut:]);require(tail.count(['MOVE',f'X{d}','Hub'])==1,'one closing route replaced');tail.remove(['MOVE',f'X{d}','Hub']);F=carry+tail
 def word(ops,schema):return {'schema':schema,'source_path':b['source_path'],'source_sha256':b['source_sha256'],'charts':copy.deepcopy(b['charts']),'targets':b['targets'],'operations':ops}
 old=word(b['operations'][:cut]+F,'actual-mask-source-nontrivial-continuation-v1');old.update(base_word_sha256=PIN,continuation_before_operation=cut)
 old_result,ot,_=replay(old,collect=True)
 require(ot[cut+2][0][f'X{d}']==(1<<d)^(1<<bb)^masks[0],'old original actually reads the unknown common form')
 raw_names={i:f'MASK_RESET_RAW_{i}'for i in S}
 def prefix(preloads):
  ops=[]
  for i in S:ops.extend([['INIT',raw_names[i],f'L{i}'],['ADD',f'X{i}',raw_names[i]],['MOVE',raw_names[i],'zero']])
  ps=len(ops)
  for i,row in enumerate(preloads):
   for j in S:
    if row>>j&1:ops.append(['ADD',raw_names[j],f'Y{i}'])
  pe=len(ops)
  for j,part in enumerate(parts):
   loc=f'MASK_CORRECTION_{j}';source=f'MASK_SOURCE_{j}';field=fields[j]
   ops.extend([['INIT',source,loc],['INIT',field,loc]])
   for i in part:ops.extend([['MOVE',f'X{i}',loc],['ADD',f'X{i}',source],['MOVE',f'X{i}','Hub']])
   ops.extend([['ADD',source,field],['MOVE',field,common]])
  for i in range(N):
   if i not in U and oa[f'X{i}']!=f'L{i}':ops.append(['MOVE',f'X{i}',oa[f'X{i}']])
   if oa[f'Y{i}']!='zero':ops.append(['MOVE',f'Y{i}',oa[f'Y{i}']])
  keep=set(fields)|{f'MASK_SOURCE_{j}'for j in range(3)}
  for n in owners:
   if n not in keep:ops.append(['INIT',n,oa[n]])
  return ops,ps,pe
 clear_raw=[['CLEAR',raw_names[i]]for i in S]
 empty_prefix,_,_=prefix([0]*N)
 unprepared=word(empty_prefix+F+clear_raw,'unprepared-actual-mask-preserving-reset-v1')
 uv,_,_,_=evaluate(unprepared);M=[uv[f'X{i}']for i in range(N)]
 require(M==[(1<<i)^((1<<bb)if i==d else 0)for i in range(N)],'nontrivial actual reset-original matrix')
 corrections=[uv[f'Y{i}']^(1<<(N+i))^((1<<i)if i in b['targets']else 0)for i in range(N)]
 require(all(z&~sm==0 for z in corrections),'known-ground-only correction')
 pp,ps,pe=prefix(corrections);newcut=len(pp)
 inverse=[[o[0],o[1].replace('Y','X'),o[2].replace('Y','X')]for o in inverse_add_word(M)]
 require(inverse==[['ADD','X34','X7']],'actual one-ADD original inverse')
 reset=word(pp+F+inverse+clear_raw,'actual-unknown-mask-preserving-partial-reset-v1')
 reset.update(base_word_sha256=PIN,released_carriers=b['released_carriers'],carrier_interface_before_operation=newcut,
  mask_reset={'source_S':S,'unknown_sources':U,'partition':parts,'fields':fields,'common':common,
   'continuation_before_operation':newcut,'preload_range':[ps,pe],'literal_F_length':len(F),
   'Hub_inverse_before_operation':newcut+len(F),'Hub_inverse':inverse})
 after,nt,_=replay(reset,collect=True);nv,na=nt[newcut]
 for n,z in ov.items():
  require(chart(reset['charts'][na[n]])==chart(b['charts'][oa[n]]),('same actual cut chart',n))
  require((nv[n]^z)>>N==0 and ((nv[n]^z)&xm)&~sm==0,('all Y and outside-S X columns preserved',n))
 for i,n in raw_names.items():require(nv[n]==1<<i and na[n]=='zero','actual known ground source')
 require(reset['operations'][newcut:newcut+len(F)]==old['operations'][cut:],'unchanged literal continuation')
 require([nt[newcut+len(F)][0][f'X{i}']for i in range(N)]==M,'ground preload preserves the final original matrix')
 require(all(nt[newcut+len(F)][1][f'X{i}']=='Hub'for i in range(N)),'actual Hub inverse cochart')
 source=word(pp+copy.deepcopy(b['operations'][cut:])+clear_raw,'actual-S57-ground-and-three-unknown-mask-source-v1')
 source.update(base_word_sha256=PIN,released_carriers=b['released_carriers'],carrier_interface_before_operation=newcut,
  source_interface={'ground_raw_S':S,'ground_raw_names':raw_names,'unknown_mask_partition':parts,
   'common_fields':fields,'common_chart':common,'proper_mask_fields':[f'MASK_SOURCE_{j}'for j in range(3)],
   'continuation_before_operation':newcut,'all55_targets_complete_at_native_facets':True,
   'remaining56_Y_raw_at_ground':True,'remaining50_X_raw_at_native_lines':True})
 source_result,st,_=replay(source,collect=True)
 require(source_result['counts']=={'INIT':190,'ADD':134,'MOVE':301,'CLEAR':190},'actual source counts')
 require(source_result['movement_profile']=={1:57,2:22,5:19,7:203},'actual source movement')
 zero_owners={n for n in owners if nv[n]==0}
 require(len(zero_owners)==127,'127 obsolete zero owners')
 postponed=[];lib_prefix=[]
 for o in pp:
  if o[0]=='INIT'and o[1]in zero_owners:continue
  if o[0]=='MOVE'and o[1].startswith('X')and int(o[1][1:])not in U:
   require(o[2]=='Hub','only unused direct closure postponed');postponed.append(o);continue
  lib_prefix.append(o)
 lib_tail=[o for o in b['operations'][cut:]if not(o[0]=='CLEAR'and o[1]in zero_owners)]
 liberated=word(lib_prefix+postponed+lib_tail+clear_raw,'actual-liberated-S57-and-three-unknown-mask-source-v1')
 free=sorted(set(range(N))-set(U));libcut=len(lib_prefix)
 liberated.update(base_word_sha256=PIN,released_carriers=free,carrier_interface_before_operation=libcut,
  source_interface={'ground_raw_S':S,'ground_raw_names':raw_names,'unknown_mask_partition':parts,
   'common_fields':fields,'common_chart':common,'proper_mask_fields':[f'MASK_SOURCE_{j}'for j in range(3)],
   'continuation_before_operation':libcut,'all55_targets_complete_at_native_facets':True,
   'remaining56_Y_raw_at_ground':True,'remaining92_X_raw_at_native_lines':True,
   'omitted_unused_zero_owners':sorted(zero_owners),'postponed_raw_original_closures':len(postponed)})
 lib_result,lt,_=replay(liberated,collect=True);lv,la=lt[libcut]
 require(len(free)==92 and len(postponed)==42,'actual92 original release')
 require(lib_result['counts']=={'INIT':63,'ADD':134,'MOVE':301,'CLEAR':63},'liberated source counts')
 require(lib_result['movement_profile']==source_result['movement_profile'],'same complete movement')
 for i in free:require(lv[f'X{i}']==1<<i and la[f'X{i}']==f'L{i}','actual free raw original')
 for i in U:require(lv[f'X{i}']==1<<i and la[f'X{i}']=='Hub','mask original actually at Hub')
 for n in set(raw_names.values())|set(fields)|{f'MASK_SOURCE_{j}'for j in range(3)}:
  require(lv[n]==nv[n]and la[n]==na[n],'known and unknown source fields preserved')
 def verify_unknown_interface(ww):
  _,tr,_=replay(ww,collect=True);v,at=tr[ww['mask_reset']['continuation_before_operation']]
  for n,z in ov.items():
   require(((v[n]^z)&xm)&~sm==0 and (v[n]^z)>>N==0,('actual preserved unknown/Y source column',n))
   require(chart(ww['charts'][at[n]])==chart(b['charts'][oa[n]]),('actual interface chart',n))
 controls=[]
 def reject(label,bad,check=replay):
  try:check(bad)
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
  else:raise ValueError(('accepted mask-reset mutation',label))
 for label,event in [
  ('omit actual proper mask copy',['ADD','MASK_SOURCE_0',fields[0]]),
  ('omit actual source descent',['MOVE',fields[0],common]),
  ('omit native mask arrival',['MOVE','X31','MASK_CORRECTION_0']),
  ('omit paid known ground capture',['ADD','X34',raw_names[34]]),
  ('omit initial known output preload',['ADD',raw_names[34],'Y34']),
  ('omit actual ground source retirement',['CLEAR',raw_names[34]])]:
  bad=copy.deepcopy(reset);bad['operations'].remove(event);reject(label,bad)
 bad=copy.deepcopy(reset);del bad['operations'][newcut+len(F):newcut+len(F)+1];reject('omit actual one-ADD Hub inverse',bad)
 bad=copy.deepcopy(reset);bad['operations'].remove(['ADD','X31','MASK_SOURCE_0'])
 # Both descendant copies lose the same direction, so this F still closes.
 replay(bad);bad['mask_reset']['continuation_before_operation']=newcut-1
 reject('endpoint-correct deletion of unknown source acquisition',bad,verify_unknown_interface)
 require(after['counts']=={'INIT':190,'ADD':138,'MOVE':303,'CLEAR':190},'complete nontrivial reset counts')
 require(after['movement_profile']=={1:57,2:24,3:1,5:19,7:202},'complete nontrivial reset movement')
 for j,u in enumerate(masks):
  require(nv[fields[j]]==u and na[fields[j]]==common,'new pure common unknown form')
  require(nv[f'MASK_SOURCE_{j}']==u and na[f'MASK_SOURCE_{j}']==f'MASK_CORRECTION_{j}','retained actual rank6 mask form')
 all_owned={n:z for n,z in nv.items()if n not in originals}
 require(len(binary_basis(all_owned.values()))==60,'actual known57 plus unknown3 source rank')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(after['movement_profile']);sq=moment(source_result['movement_profile'])
 result={'status':'PASS_AUTHOR_ACTUAL_UNKNOWN_MASK_PRESERVING_RESET','old_source_word_sha256':PIN,
  'native_source_sha256':b['source_sha256'],'source_S':S,'source_count':57,'unknown_mask_sources':U,'unknown_partition':parts,
  'old_cut':cut,'new_cut':newcut,'all_cut_Y_columns_preserved':True,'all_cut_X_columns_outside_S57_preserved':True,
  'old_nontrivial_control':old_result,'reset_nontrivial_control':after,'actual_direct_source':source_result,
  'liberated_direct_source':lib_result,'liberated_source_cut':libcut,'liberated_native_original_count':92,
  'actual_source_owner_rank':60,'actual_common_unknown_rank':3,'actual_raw_ground_rank':57,
  'raw_native_original_count':len(b['released_carriers']),'raw_ground_unfinished_Y_count':N-len(b['targets']),
  'literal_continuation_length':len(F),'original_X7_before_Hub_inverse':hex(M[7]),'actual_Hub_inverse':inverse,
  'source_moment':record(sq),'source_necessary_limiting_room':record((limit[0]-sq[1],limit[1]-sq[0])),
  'nontrivial_control_moment':record(q),'nontrivial_control_room':record((limit[0]-q[1],limit[1]-q[0])),
  'controls':controls,'scope':'Actual55-output source with paid rawS57 ground, three true unknown masks at common rank4 and their real rank6 caches, all222 columns and50 native originals. The separate old-F comparison has a real nonidentity Hub inverse. All five global foundations remain open; no all111 or kappa.'}
 a.out.mkdir(parents=True,exist_ok=True)
 for name,ww in [('OLD-WORD',old),('RESET-WORD',reset),('SOURCE-WORD',source),('LIBERATED-SOURCE-WORD',liberated),('UNPREPARED-WORD',unprepared)]:
  data=(json.dumps(ww,indent=2)+'\n').encode();(a.out/(name+'.json')).write_bytes(data);result[name.lower()+'_sha256']=hashlib.sha256(data).hexdigest()
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ['status','source-word_sha256','reset-word_sha256','actual_direct_source','reset_nontrivial_control','source_moment','source_necessary_limiting_room']},indent=2))
if __name__=='__main__':main()
