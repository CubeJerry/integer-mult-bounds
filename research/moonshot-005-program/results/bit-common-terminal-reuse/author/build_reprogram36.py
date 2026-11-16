"""Fresh actual M1 acquisition and a genuinely new common terminal row."""
from pathlib import Path
import argparse,copy,hashlib,json,sys
from loader import load
BASE='e4d451886a134c648f71fadac5b7f6f8693e5495b60416d137cfe0d0e563e050'

def build(w):
 z=copy.deepcopy(w);ops=[['INIT','RAW41','L41'],['ADD','X41','RAW41'],['INIT','CAP46','M1']];mapping={}
 for step,o in enumerate(w['operations'],1):
  if o==['MOVE','X46','C2']:ops.extend([o,['ADD','X46','CAP46']])
  elif o==['ADD','Q1','P3']:ops.append(['ADD','CAP46','P3'])
  elif o==['ADD','ZKEEP2','P3']:ops.extend([o,['ADD','RAW41','P3']])
  elif o==['ADD','ZRAW0','P3']:pass
  elif o[0]=='ADD'and o[1]=='P3'and o[2].startswith('Y'):ops.extend([['ADD','ZRAW0',o[2]],['ADD','E6',o[2]]])
  elif o==['MOVE','Y41','F41']:ops.extend([['ADD','P3','Y41'],['ADD','E6','Y41'],o])
  elif o==['MOVE','Y46','F46']:ops.extend([['MOVE','Y46','L41'],['ADD','ZKEEP2','Y46'],o])
  else:ops.append(o)
  mapping[step]=len(ops)
 ops.extend([['CLEAR','RAW41'],['CLEAR','CAP46']]);z['operations']=ops;z['milestones']={k:mapping[v]for k,v in w['milestones'].items()};z['targets']=sorted(w['targets']+[41,46]);z['seed_rows_hex'][3]=hex((1<<41)^(1<<6));z['base_word_sha256']=BASE
 z['m1_retention'][0]['h_hex']=hex(1<<46);z['m1_retention'][0]['h_recipe']=['CAP46'];z['coded_port_repair']['new_payload_hex']=hex(1<<46);z['coded_port_repair']['actual_new_payload_source']='CAP46';z['coded_port_repair']['terminal_changed_by_actual_RAW41']=True
 z['fresh_common_terminal']={'packet':3,'old_row_hex':w['seed_rows_hex'][3],'new_row_hex':z['seed_rows_hex'][3],'raw_old_source':'ZRAW0','old_reader_replacement':['ZRAW0','E6'],'old_readers':[o[2]for o in w['operations']if o[0]=='ADD'and o[1]=='P3'and o[2].startswith('Y')],'new_raw_capture':'RAW41','raw_capture_point':41,'raw_capture_chart':'L41','uses_existing_final_descent':True,'new_target':41}
 z['fresh_M1_capture']={'owner':'CAP46','point':46,'chart':'M1','actual_read_after':['MOVE','X46','C2'],'chart_equals_existing_source_chart':'C2','new_target':46,'new_receiver_path':['L41','F46']}
 z['affine_scope']='Actual36-output construction: freshCAP46 source and newgroundX41 code fromP3. Every oldY reader is reencoded using actual groundZRAW0+E6. No complete supplier or newkappa.'
 return z

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=a.repo/'research/moonshot-005-program/results';raw=(root/'bit-composed-coded-source/author/output/WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];z=build(w);e=load(root/'bit-composed-coded-source/author/retained/source_history_engine.py','e');S=[int(x,16)for x in z['seed_rows_hex']];run=e.replay(z,R,S,15,False);old=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];ov=old['cuts']['seed']['values'];oa=old['cuts']['seed']['charts'];assert C['M1']==C['C2'] and e.contained(C['L41'],C['F46'])
 assert v['RAW41']==1<<41 and at['RAW41']=='L41';assert v['CAP46']==v['ZKEEP2']==1<<46 and at['CAP46']=='M1' and at['ZKEEP2']=='L41';assert v['P3']==(1<<41)^(1<<6) and at['P3']=='zero'
 assert ov['P3']==ov['ZRAW0']^ov['E6']
 for n in ov:
  assert at[n]==oa[n]
  if n not in ['P3','ZKEEP2']:assert v[n]==ov[n],n
 assert run['count']=={'INIT':117,'ADD':916,'MOVE':437,'CLEAR':117},run['count'];assert run['dirty_CLEAR']==117
 expected=old['profile'].copy();expected[1]+=1;expected[6]+=1;expected[7]-=1;assert run['profile']==expected
 xmask=(1<<111)-1;ground=[v[n]for n in v if at[n]=='zero'and not(v[n]&~xmask)];oldground=[ov[n]for n in ov if oa[n]=='zero'and not(ov[n]&~xmask)];rank=lambda rr:len(e.basis(rr));assert rank(ground)==rank(oldground)+1 and rank(ground+oldground)==rank(ground)
 controls=[]
 for op in [['ADD','X41','RAW41'],['ADD','X46','CAP46'],['ADD','CAP46','P3'],['ADD','RAW41','P3'],['ADD','P3','Y41'],['ADD','E6','Y41'],['ADD','ZKEEP2','Y46'],['MOVE','Y46','L41'],['ADD','ZRAW0','Y2'],['ADD','E6','Y2'],['CLEAR','RAW41'],['CLEAR','CAP46']]:
  q=copy.deepcopy(z);q['operations'].remove(op);q['milestones']={k:-1 for k in q['milestones']};q.pop('source_cut',None)
  try:e.replay(q,R,S,15,False)
  except AssertionError as ex:controls.append({'removed':op,'rejected':str(ex)})
  else:raise AssertionError(('accepted semantic mutant',op))
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(z,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw);out={'status':'PASS_ACTUAL_NEW_COMMON_TERMINAL36','word_sha256':hashlib.sha256(raw).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':z['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'new_targets':[41,46],'old_terminal_was_redundant_with_actual_ground':['ZRAW0','E6'],'common_rank_before':rank(oldground),'common_rank_after':rank(ground),'old_common_space_preserved':True,'ground_row_change':'P3: X0+X6 to X41+X6','new_nonlocal_leaf_row':'ZKEEP2: X46','only_old_seed_cut_values_changed':['P3','ZKEEP2'],'exact_movement_increment':'[1]+[6]-[7]','semantic_negative_controls':controls,'controls_disable_invoice_source_cut_and_milestones':True,'scope':'Literal whole-record binary source and receiver construction for every characteristic-two field/width; all physical framework assumptions retained.36/111 partial endpoints; no newkappa.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');price=load(root/'bit-composed-coded-source/author/price.py','price');(a.out/'PRICE.json').write_text(json.dumps(price.invoice(run['profile']),indent=2)+'\n');print(out['status'],out['word_sha256'],run['count'],'rank',rank(oldground),rank(ground))
if __name__=='__main__':main()
