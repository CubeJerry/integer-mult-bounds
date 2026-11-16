"""Extend two physical pair codes to source-compatible triple codes."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load
BASE='0ce7ccb671300c1af9548f091e972e81feb09f7f8d8cf115d0e46b3bb0762bc2'

def build(w,R):
 z=copy.deepcopy(w);newcharts={'P4_K':(40,29),'P4_A':(42,29),'P4_B':(42,40),'P5_K':(49,45),'P5_A':(48,45),'P5_B':(48,49)}
 for n,idx in newcharts.items():z['charts'][n]={'kind':'span','rows':[R[j]for j in idx]}
 ops=[['INIT','RAW40','L40'],['ADD','X40','RAW40'],['INIT','RAW49','L49'],['ADD','X49','RAW49']]
 ops +=[['INIT',n,c]for n,c in [('P4_RET','P4_K'),('P4_RAW29','P4_A'),('P4_RAW42','P4_B'),('P5_RET','P5_K'),('P5_RAW45','P5_A'),('P5_RAW48','P5_B')]];mapping={}
 targets={'Y29','Y42','Y40','Y45','Y48','Y49'}
 for step,o in enumerate(w['operations'],1):
  if 'ZCORR2'in o:
   pass
  elif o[0]=='ADD'and o[2]in targets:pass
  elif o[0]=='MOVE'and o[1]in targets:
   if o[2]=='F29':ops.extend([['ADD','P4','Y29'],['ADD','E75','Y29'],['MOVE','Y29','L40'],['ADD','RAW40','Y29'],['MOVE','Y29','P4_B'],['ADD','P4_RAW42','Y29'],o])
   elif o[2]=='F42':ops.extend([['MOVE','Y42','L29'],['ADD','RAW29','Y42'],['MOVE','Y42','P4_K'],['ADD','P4_RET','Y42'],o])
   elif o[2]=='F40':ops.extend([['ADD','P4','Y40'],['ADD','E75','Y40'],['MOVE','Y40','L42'],['ADD','RAW42','Y40'],['MOVE','Y40','P4_A'],['ADD','P4_RAW29','Y40'],o])
   elif o[2]=='F45':
    ops +=[['ADD',n,'Y45']for n in ['P5','E79','ZRAW0','ZRAW44']];ops +=[['MOVE','Y45','L49'],['ADD','RAW49','Y45'],['MOVE','Y45','P5_B'],['ADD','P5_RAW48','Y45'],o]
   elif o[2]=='F48':ops.extend([['ADD','ZRAW0','Y48'],['ADD','ZRAW44','Y48'],['MOVE','Y48','L45'],['ADD','ZCORR48','Y48'],['MOVE','Y48','P5_K'],['ADD','P5_RET','Y48'],o])
   elif o[2]=='F49':
    ops +=[['ADD',n,'Y49']for n in ['P5','E79','ZRAW0','ZRAW44']];ops +=[['MOVE','Y49','L48'],['ADD','RAW48','Y49'],['MOVE','Y49','P5_A'],['ADD','P5_RAW45','Y49'],o]
  elif o==['MOVE','Y2','Jnew2']:ops.extend([['MOVE','Y2','L29'],['ADD','RAW29','Y2'],o])
  elif o==['MOVE','X29','Jnew2']:pass
  elif o in [['MOVE',f'X{j}','C2']for j in [29,42,45,48]]:
   j=int(o[1][1:]);c,n={29:('P4_A','P4_RAW29'),42:('P4_B','P4_RAW42'),45:('P5_A','P5_RAW45'),48:('P5_B','P5_RAW48')}[j];ops.extend([['MOVE',o[1],c],['ADD',o[1],n],o])
  elif o==['MOVE','P4','zero']:ops.extend([['MOVE','P4','P4_K'],['ADD','P4','P4_RET'],['MOVE','P4','L40'],['ADD','RAW40','P4'],o])
  elif o==['MOVE','P5','zero']:ops.extend([['MOVE','P5','P5_K'],['ADD','P5','P5_RET'],['MOVE','P5','L49'],['ADD','RAW49','P5'],o])
  else:ops.append(o)
  mapping[step]=len(ops)
 ops +=[['CLEAR',n]for n in ['RAW40','RAW49','P4_RET','P4_RAW29','P4_RAW42','P5_RET','P5_RAW45','P5_RAW48']];z['operations']=ops;z['milestones']={k:mapping[v]for k,v in w['milestones'].items()};z['targets']=sorted(w['targets']+[40,49]);z['seed_rows_hex'][4]=hex(int(w['seed_rows_hex'][4],16)^(1<<40));z['seed_rows_hex'][5]=hex(int(w['seed_rows_hex'][5],16)^(1<<49));z['base_word_sha256']=BASE;z.get('source_cut',{}).pop('ZCORR2',None)
 z['three_actual_triples']={'common_codes':[[29,40,42],[41,43,46],[45,48,49]],'new_targets':[40,49],'common_P4_hex':z['seed_rows_hex'][4],'common_P5_hex':z['seed_rows_hex'][5],'new_source_charts':newcharts,'old_Y2_raw_correction_now_at_native_L29':'RAW29 replaces ZCORR2; Y2 visits L29 before Jnew2/BACK2','original_X29_Jnew2_visit_removed_only_after_reader_repair':True,'new_source_raw40_raw49':'Captured at native births and read by respective principal on actual final descent','actual_retained_partial_rows':{'P4_RET':hex((1<<29)^(1<<42)),'P5_RET':w['third_common_channel']['source_payload_hex']},'scope':'Retentions store unmasked P4/P5 values before their ground E75/E79 additions; operation-derived values control.'}
 z['affine_scope']='Actual41-output source: three physical triple codes with higher retentions and nested source/receiver corrections. All old39 endpoints preserved; no complete111 supplier or newkappa.'
 return z

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=json.loads(raw);root=a.repo/'research/moonshot-005-program/results';e=load(root/'bit-composed-coded-source/author/retained/source_history_engine.py','e');src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];z=build(w,R);S=[int(x,16)for x in z['seed_rows_hex']];run=e.replay(z,R,S,15,False);old=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];mask=(1<<111)-1;rank=lambda rr:len(e.basis(rr));ground=[r for n,r in v.items()if at[n]=='zero'and not(r&~mask)]
 for n in ['P4_K','P4_A','P4_B','P5_K','P5_A','P5_B']:assert len(C[n])==2 and e.contained(C[n],C['M1'])
 assert v['P4_RET']==(1<<29)^(1<<42);assert v['P5_RET']==sum(1<<j for j in[0,44,45,48]);assert v['RAW40']==1<<40 and v['RAW49']==1<<49;assert 'ZCORR2'not in v
 for n,i in [('P4_RAW29',29),('P4_RAW42',42),('P5_RAW45',45),('P5_RAW48',48)]:assert v[n]==1<<i
 expected=old['profile'].copy()
 for d,c in {1:17,2:-1,3:5,4:-3,5:4,6:-4,7:-2}.items():expected[d]+=c
 assert run['profile']==expected,(run['profile'],expected)
 controls=[]
 tests=[['ADD','X40','RAW40'],['ADD','X49','RAW49'],['ADD','RAW40','P4'],['ADD','RAW49','P5'],['ADD','P4','P4_RET'],['ADD','P5','P5_RET'],['MOVE','Y2','L29'],['ADD','RAW29','Y2'],['ADD','X29','P4_RAW29'],['ADD','X42','P4_RAW42'],['ADD','X45','P5_RAW45'],['ADD','X48','P5_RAW48'],['ADD','P4_RET','Y42'],['ADD','P5_RET','Y48'],['ADD','P4_RAW29','Y40'],['ADD','P5_RAW45','Y49'],['MOVE','Y29','P4_B'],['MOVE','Y45','P5_B'],['CLEAR','P5_RET']]
 for op in tests:
  q=copy.deepcopy(z);q['operations'].remove(op);q['milestones']={k:-1 for k in q['milestones']};q.pop('source_cut',None)
  try:e.replay(q,R,S,15,False)
  except AssertionError as ex:controls.append({'removed':op,'rejected':str(ex)})
  else:raise AssertionError(('accepted semantic mutant',op))
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(z,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw);out={'status':'PASS_ACTUAL_THREE_TRIPLES41','word_sha256':hashlib.sha256(raw).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':z['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'common_rank':rank(ground),'new_targets':[40,49],'common_code_supports':[[29,40,42],[41,43,46],[45,48,49]],'exact_movement_increment_from39':'17[1]-[2]+5[3]-3[4]+4[5]-4[6]-2[7]','all_old39_targets_preserved':True,'semantic_negative_controls':controls,'controls_disable_invoice_source_cut_and_milestones':True,'scope':'Three actual common triple codes with source-compatible partial retentions, raw captures and complete invoice.41/111 partial endpoints; no newkappa.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');price=load(root/'bit-composed-coded-source/author/price.py','price');q=price.invoice(run['profile']);(a.out/'PRICE.json').write_text(json.dumps(q,indent=2)+'\n');print(out['status'],out['word_sha256'],run['count'],'commonrank',rank(ground),'Q',q['moment']['lower'],'room',q['limiting_room']['lower'])
if __name__=='__main__':main()
