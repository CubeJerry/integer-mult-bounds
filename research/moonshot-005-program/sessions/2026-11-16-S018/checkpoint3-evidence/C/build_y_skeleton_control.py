#!/usr/bin/env python3
"""Actual homogeneous-Y reset with dirty owned data and nontrivial X inverse."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,chart,replay,require,binary_basis
from ground_output_normalization import evaluate,inverse_add_word
from price_projection import moment,record
PIN='c7e48e002da3ce642707b25d74dc15d0915945f319053eb97f2016045afe4615'

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();wp=a.work/'A/d4-feedback-pruned78/WORD.json';raw=wp.read_bytes()
 require(hashlib.sha256(raw).hexdigest()==PIN,'dirty52 source pin');b=json.loads(raw)
 sr=(a.repo/b['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==b['source_sha256'],'native pin')
 before,bt,_=replay(b,collect=True);cut=b['cohort_feedback']['continuation_before_operation'];ov,oa=bt[cut]
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};owners=sorted(set(ov)-originals)
 common=b['cohort']['meet'];primaries=[4,74,78];fields=['ZFIRST3','ZFIRST4','ZFIRST5'];frame=[3,4,47,51]
 S=sorted(set(b['targets'])|{61,67});sm=sum(1<<i for i in S);xm=(1<<N)-1
 for n,z in ov.items():
  baseline=(1<<int(n[1:])if n.startswith('X')and n in originals else 1<<(N+int(n[1:]))if n.startswith('Y')and n in originals else 0)
  require(((z^baseline)&xm)&~sm==0,'cut nonidentity X support S54')
 require({n:z>>N for n,z in ov.items()if n not in originals and z>>N}=={f:1<<p for f,p in zip(fields,primaries)},'actual old owned Y signature')
 require(oa['X0']=='L0','changed continuation starts with actual released X0')
 # One legal continuation really uses dirty owner and primary Y, then restores.
 carry=[['MOVE','X0',common],['ADD','ZFIRST3','X0'],['MOVE','X0','F4'],['ADD','Y4','X0'],['MOVE','X0','Hub']]+[['ADD',f'X{i}','X0']for i in frame]
 tail=copy.deepcopy(b['operations'][cut:]);require(tail.count(['MOVE','X0','Hub'])==1,'unique raw closure replaced')
 tail.remove(['MOVE','X0','Hub']);F=carry+tail
 def shell(ops,schema):
  return {'schema':schema,'source_path':b['source_path'],'source_sha256':b['source_sha256'],'charts':copy.deepcopy(b['charts']),'targets':b['targets'],'operations':ops}
 old=shell(b['operations'][:cut]+F,'dirty52-actual-dirty-owner-feedback-continuation-v1')
 old.update(base_word_sha256=PIN,continuation_before_operation=cut)
 old_result,ot,_=replay(old,collect=True)
 require(ot[cut+2][0]['X0']==(1<<0)^(1<<(N+4))^sum(1<<i for i in [3,47,51]),'old X0 actually carries arbitrary original y4')
 raw_names={i:f'SKELETON_RAW_{i}'for i in S}
 def prefix(preloads):
  ops=[]
  for i in S:ops.extend([['INIT',raw_names[i],f'L{i}'],['ADD',f'X{i}',raw_names[i]],['MOVE',raw_names[i],'zero']])
  preload_start=len(ops)
  for i,row in enumerate(preloads):
   for j in S:
    if row>>j&1:ops.append(['ADD',raw_names[j],f'Y{i}'])
  preload_end=len(ops)
  for p,f in zip(primaries,fields):ops.extend([['MOVE',f'Y{p}',common],['INIT',f,common],['ADD',f'Y{p}',f],['MOVE',f'Y{p}',f'F{p}']])
  for i in range(N):
   if i not in primaries and oa[f'Y{i}']!='zero':ops.append(['MOVE',f'Y{i}',oa[f'Y{i}']])
   if oa[f'X{i}']!=f'L{i}':ops.append(['MOVE',f'X{i}',oa[f'X{i}']])
  for n in owners:
   if n not in fields:ops.append(['INIT',n,oa[n]])
  return ops,preload_start,preload_end
 clear_raw=[['CLEAR',raw_names[i]]for i in S]
 zero_prefix,_,_=prefix([0]*N)
 unprepared=shell(zero_prefix+F+clear_raw,'unprepared-actual-Y-skeleton-v1')
 uv,_,ut,_=evaluate(unprepared);M=[uv[f'X{i}']for i in range(N)]
 require(all(z>>N==0 for z in M),'unprepared endpoint X has no Y residue')
 require(M==[(1<<i)^(sum(1<<j for j in frame)if i==0 else 0)for i in range(N)],'actual nontrivial original matrix')
 corrections=[uv[f'Y{i}']^(1<<(N+i))^((1<<i)if i in b['targets']else 0)for i in range(N)]
 require(all(z&~sm==0 for z in corrections),'all actual Y endpoint errors in S54')
 actual_prefix,ps,pe=prefix(corrections);newcut=len(actual_prefix)
 # The same fixed continuation is replayed literally, then a real Hub inverse.
 inverse=[[o[0],o[1].replace('Y','X'),o[2].replace('Y','X')]for o in inverse_add_word(M)]
 require(len(inverse)==4,'real four-ADD Hub inverse')
 reset=shell(actual_prefix+F+inverse+clear_raw,'actual-Y-skeleton-reset-with-Hub-restoration-v1')
 reset.update(base_word_sha256=PIN,continuation_before_operation=newcut,
  skeleton={'source_S':S,'fields':fields,'primaries':primaries,'initial_preload_range':[ps,pe],
   'literal_continuation_length':len(F),'Hub_inverse_before_operation':newcut+len(F),'Hub_inverse':inverse})
 after,nt,_=replay(reset,collect=True);nv,na=nt[newcut]
 for n,z in ov.items():
  require(chart(reset['charts'][na[n]])==chart(b['charts'][oa[n]]),'same named interface chart')
  require((nv[n]^z)>>N==0,'identical entire cut Y signature')
  require(((nv[n]^z)&xm)&~sm==0,'identical entire cut X columns outside S54')
 for i,n in raw_names.items():require(nv[n]==1<<i and na[n]=='zero','actual separately named ground source')
 require(reset['operations'][newcut:newcut+len(F)]==old['operations'][cut:],'literal unchanged fixed continuation')
 require([nt[newcut+len(F)][0][f'X{i}']for i in range(N)]==M,'initial preload changes no final original row')
 require(all(nt[newcut+len(F)][1][f'X{i}']=='Hub'for i in range(N)),'actual original inverse cochart')
 controls=[]
 def reject(label,bad):
  try:replay(bad)
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
  else:raise ValueError(('accepted skeleton mutation',label))
 for label,event in [
  ('omit actual owned original-Y copy',['ADD','Y4','ZFIRST3']),
  ('omit actual raw ground acquisition',['ADD','X3',raw_names[3]]),
  ('omit initial ground endpoint preload',['ADD',raw_names[3],'Y3']),
  ('omit actual Y copy visit',['MOVE','Y4',common]),
  ('omit ground source retirement',['CLEAR',raw_names[3]])]:
  bad=copy.deepcopy(reset);bad['operations'].remove(event);reject(label,bad)
 bad=copy.deepcopy(reset);del bad['operations'][newcut+len(F):newcut+len(F)+len(inverse)]
 reject('omit actual nontrivial Hub original inverse',bad)
 # A completely legal late preload changes Y4 without its already-made copy.
 late_rows=corrections.copy();late_rows[4]=0;late_prefix,_,_=prefix(late_rows)
 late_packet=[['INIT','LATE_X4','Hub'],['ADD','X4','LATE_X4'],['MOVE','LATE_X4','F4'],['ADD','LATE_X4','Y4'],['CLEAR','LATE_X4']]
 late=shell(late_prefix+late_packet+F+inverse+clear_raw,'rejected-legal-late-Y-preload-v1')
 lv,_,_,late_cost=evaluate(late)
 require(lv['X0']==(1<<0)^(1<<4),'late preload leaves actual x4 error on restored X0')
 require(all(lv[f'Y{i}']==(1<<(N+i))^((1<<i)if i in b['targets']else 0)for i in range(N)),'late preload still completes every claimed Y')
 reject('legal late preload fails to propagate into owned Y copy',late)
 require(after['counts']=={'INIT':166,'ADD':119,'MOVE':281,'CLEAR':166},'complete actual skeleton control counts')
 require(after['movement_profile']=={1:55,3:5,4:3,7:218},'complete actual skeleton control profile')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(after['movement_profile'])
 result={'status':'PASS_AUTHOR_ACTUAL_HOMOGENEOUS_Y_SKELETON_RESET','source_word_sha256':PIN,
  'native_source_sha256':b['source_sha256'],'source_S':S,'source_count':len(S),'targets':b['targets'],
  'old_cut':cut,'new_cut':newcut,'same_named_cut_Y_columns':True,'same_named_cut_X_columns_outside_S':True,
  'old_owned_Y_signature':{f:p for f,p in zip(fields,primaries)},'old_continuation':old_result,
  'reset':after,'literal_continuation_length':len(F),'old_continuation_X0_transient':hex(ot[cut+2][0]['X0']),
  'reset_X0_before_Hub_inverse':hex(M[0]),'final_original_matrix_rank':len(binary_basis(M)),
  'actual_Hub_inverse':inverse,'initial_ground_preload_count':pe-ps,
  'whole_moment':record(q),'old_moment':record(moment(old_result['movement_profile'])),
  'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),
  'skeleton_direct_closure_reference':record(moment({1:54,3:3,4:3,7:219})),
  'controls':controls,'legal_late_preload_control':{'all_Y_endpoints_correct':True,'X0_error':'x4','cost':late_cost},
  'scope':'Author actual52-output physical reset with dirty owner read, arbitrary-Y feedback, paid S54 acquisition, identical cut Y signature and nontrivial Hub inverse. Not all111, not a supplier, no kappa. Five foundations remain.'}
 a.out.mkdir(parents=True,exist_ok=True)
 for name,word in [('OLD-WORD',old),('RESET-WORD',reset),('UNPREPARED-WORD',unprepared),('LATE-PRELOAD-NEGATIVE',late)]:
  data=(json.dumps(word,indent=2)+'\n').encode();(a.out/(name+'.json')).write_bytes(data);result[name.lower()+'_sha256']=hashlib.sha256(data).hexdigest()
 proof=Path(__file__).with_name('HOMOGENEOUS-SIGNATURE-RESET.md');result['proof_sha256']=hashlib.sha256(proof.read_bytes()).hexdigest()
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ['status','old-word_sha256','reset-word_sha256','reset','whole_moment','necessary_limiting_room']},indent=2))
if __name__=='__main__':main()
