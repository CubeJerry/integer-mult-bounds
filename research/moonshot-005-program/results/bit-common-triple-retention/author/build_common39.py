"""A third actual common channel reuses the old P5 M1 payload."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load
BASE='b30cca73a0aafcc98dd98440ba2597119bf79401751f2fc5022dcbd1c22b1059'

def build(w):
 z=copy.deepcopy(w);ops=[['INIT','RAW48','L48'],['ADD','X48','RAW48']];mapping={};h=sum(1<<i for i in [0,44,45,48])
 for step,o in enumerate(w['operations'],1):
  if o[0]=='ADD'and o[2]=='Y48':pass
  elif o[0]=='MOVE'and o[1]=='Y48':
   if o[2]=='F48':
    ops.extend([['ADD',n,'Y48']for n in ['P5','E79','ZRAW0','ZRAW44']]);ops.extend([['MOVE','Y48','L45'],['ADD','ZCORR48','Y48'],o])
  elif 'ZKEEP48'in o:pass
  elif o==['ADD','X44','ZRAW44']:ops.extend([o,['MOVE','ZRAW44','zero']])
  elif o==['INIT','ZCORR48','Jnew48']:ops.extend([['INIT','ZCORR48','L45'],['ADD','X45','ZCORR48']])
  elif o in [['MOVE','X45','Jnew48'],['ADD','X45','ZCORR48'],['MOVE','P5','L44'],['ADD','ZRAW44','P5']]:pass
  elif o[0]=='ADD'and o[1]=='P5'and o[2].startswith('Y'):ops.extend([['ADD','ZRAW44',o[2]],['ADD','E79',o[2]]])
  elif o==['MOVE','Y45','F45']:
   ops.extend([['ADD',n,'Y45']for n in ['P5','E79','ZRAW0','ZRAW44']]);ops.extend([['MOVE','Y45','L48'],['ADD','RAW48','Y45'],o])
  else:ops.append(o)
  mapping[step]=len(ops)
 ops.append(['CLEAR','RAW48']);z['operations']=ops;z['milestones']={k:mapping[v]for k,v in w['milestones'].items()};z['targets']=sorted(w['targets']+[45]);z['seed_rows_hex'][5]=hex(h^(1<<79));z['base_word_sha256']=BASE;z.get('source_cut',{}).pop('ZKEEP48',None)
 for n,ch in [('ZRAW44','zero'),('ZCORR48','L45')]:
  if n in z.get('source_cut',{}):z['source_cut'][n]['chart']=ch
 z['third_common_channel']={'packet':5,'source_payload_hex':hex(h),'source_recipe':['H6_2','H6_3','Q2'],'actual_ground_row_hex':z['seed_rows_hex'][5],'exposed_pair':'X45+X48 using actual groundZRAW0/ZRAW44/E79','old_raw44_preserved_by_paid_unit_descent':'ZRAW44','old_Y44_readers_replaced':['ZRAW44','E79'],'source_ZCORR48_retargeted_to_actual_raw45_birth':'L45','new_raw48_capture':'RAW48 at L48','new_receiver':45,'receiver45_path':['L48','F45'],'receiver48_path':['L45','F48'],'old_ZKEEP48_removed':True,'P5_source_descent_shortcut':'M1 directly to zero','source_X45_shortcut':'L45 directly to C2'}
 z['affine_scope']='Actual39-output three-common-channel source, all previous38 endpoints preserved. Three actual coded common rows, actual local captures, complete costs. No complete111 supplier or newkappa.'
 return z

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=json.loads(raw);root=a.repo/'research/moonshot-005-program/results';e=load(root/'bit-composed-coded-source/author/retained/source_history_engine.py','e');src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];z=build(w);S=[int(x,16)for x in z['seed_rows_hex']];run=e.replay(z,R,S,15,False);old=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];mask=(1<<111)-1;rank=lambda rr:len(e.basis(rr));ground=[r for n,r in v.items()if at[n]=='zero'and not(r&~mask)];ov=old['cuts']['seed']['values'];oa=old['cuts']['seed']['charts'];oldground=[r for n,r in ov.items()if oa[n]=='zero'and not(r&~mask)]
 assert e.contained(C['L48'],C['F45'])and e.contained(C['L45'],C['F48']);assert v['ZRAW44']==1<<44 and at['ZRAW44']=='zero';assert v['ZCORR48']==1<<45 and at['ZCORR48']=='L45';assert v['RAW48']==1<<48 and at['RAW48']=='L48';assert 'ZKEEP48'not in v
 assert v['P5']^v['E79']^v['ZRAW0']^v['ZRAW44']==(1<<45)^(1<<48);assert rank(ground)==rank(oldground)+1 and rank(ground+oldground)==rank(ground)
 controls=[]
 for op in [['MOVE','ZRAW44','zero'],['ADD','X45','ZCORR48'],['ADD','X48','RAW48'],['ADD','RAW48','Y45'],['MOVE','Y45','L48'],['ADD','ZCORR48','Y48'],['MOVE','Y48','L45'],['ADD','P5','Y45'],['ADD','ZRAW0','Y45'],['ADD','ZRAW44','Y45'],['ADD','E79','Y45'],['ADD','ZRAW44','Y44'],['CLEAR','RAW48']]:
  q=copy.deepcopy(z);q['operations'].remove(op);q['milestones']={k:-1 for k in q['milestones']};q.pop('source_cut',None)
  try:e.replay(q,R,S,15,False)
  except AssertionError as ex:controls.append({'removed':op,'rejected':str(ex)})
  else:raise AssertionError(('accepted semantic mutant',op))
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(z,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw);out={'status':'PASS_ACTUAL_THREE_COMMON_CODES39','word_sha256':hashlib.sha256(raw).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':z['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'common_rank':rank(ground),'predecessor38_common_rank':rank(oldground),'old38_common_space_preserved':True,'actual_new_common_pair':'X45+X48','all_old38_targets_preserved':True,'exact_movement_increment_from38':'2[6]-[7]-[3]-[1]','semantic_negative_controls':controls,'controls_disable_invoice_source_cut_and_milestones':True,'scope':'Exact actual common-code source, chronological decoder paths and complete primitive invoice;39/111 partial endpoints, no newkappa.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');price=load(root/'bit-composed-coded-source/author/price.py','price');q=price.invoice(run['profile']);(a.out/'PRICE.json').write_text(json.dumps(q,indent=2)+'\n');print(out['status'],out['word_sha256'],run['count'],'commonrank',rank(ground),'Q',q['moment']['lower'],'room',q['limiting_room']['lower'])
if __name__=='__main__':main()
