"""A physically realized three-row clique code with shared proper-chart corrections."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load
BASE='c7c8eb65cdc69d01d61cb82949ad85ff4de675606462ae7d3ce772fc885eb757'

def build(w,R):
 z=copy.deepcopy(w);ops=[['INIT','PAIR_RAW43','J41_PAIR'],['INIT','PAIR_RAW46','J43_PAIR']];mapping={};payload=(1<<43)^(1<<46)
 assert w['charts']['Jnew43']['kind']=='span';jj=w['charts']['Jnew43']['rows']
 z['charts']['K46_PAIR']={'kind':'span','rows':[R[41],R[43]]};z['charts']['J41_PAIR']={'kind':'span','rows':jj+[R[43]]};z['charts']['J43_PAIR']={'kind':'span','rows':jj+[R[41]]}
 for step,oo in enumerate(w['operations'],1):
  o=['RAW43_LOCAL'if x=='RAW43_COMMON'else x for x in oo]
  if o==['MOVE','RAW43_LOCAL','zero']:pass
  elif o[0]=='ADD'and o[2]in ['Y41','Y43','Y46']:pass
  elif o[0]=='MOVE'and o[1]in ['Y41','Y43','Y46']:
   if o[2]=='F41':ops.extend([['ADD','P3','Y41'],['ADD','E6','Y41'],['MOVE','Y41','Jnew43'],['ADD','ZCORR43','Y41'],['MOVE','Y41','J41_PAIR'],['ADD','PAIR_RAW43','Y41'],o])
   elif o[2]=='F43':ops.extend([['ADD','P3','Y43'],['ADD','E6','Y43'],['MOVE','Y43','L41'],['ADD','RAW41','Y43'],['MOVE','Y43','J43_PAIR'],['ADD','PAIR_RAW46','Y43'],o])
   elif o[2]=='F46':ops.extend([['MOVE','Y46','L43'],['ADD','RAW43_LOCAL','Y46'],['MOVE','Y46','K46_PAIR'],['ADD','ZKEEP2','Y46'],o])
  elif o==['INIT','ZCORR43','L46']:ops.append(['INIT','ZCORR43','Jnew43'])
  elif o==['ADD','X46','ZCORR43']:pass
  elif o==['MOVE','X43','C2']:ops.extend([['MOVE','X43','J41_PAIR'],['ADD','X43','PAIR_RAW43'],o,['ADD','X43','CAP46']])
  elif o==['MOVE','X46','C2']:ops.extend([['MOVE','X46','Jnew43'],['ADD','X46','ZCORR43'],['MOVE','X46','J43_PAIR'],['ADD','X46','PAIR_RAW46'],o])
  elif o==['INIT','ZKEEP2','L41']:ops.append(['INIT','ZKEEP2','K46_PAIR'])
  elif o==['MOVE','P3','L41']:ops.extend([['MOVE','P3','K46_PAIR'],['ADD','P3','ZKEEP2'],o])
  elif o==['ADD','P3','ZKEEP2']:pass
  else:ops.append(o)
  mapping[step]=len(ops)
 ops.extend([['CLEAR','PAIR_RAW43'],['CLEAR','PAIR_RAW46']]);z['operations']=ops;z['milestones']={k:mapping[v]for k,v in w['milestones'].items()};z['seed_rows_hex'][3]=hex((1<<41)^payload^(1<<6));z['base_word_sha256']=BASE
 for n,ch in [('ZCORR43','Jnew43'),('ZKEEP2','K46_PAIR')]:
  if n in z.get('source_cut',{}):z['source_cut'][n]['chart']=ch
 z['m1_retention'][0]['h_hex']=hex(payload);z['m1_retention'][0]['h_recipe']=['CAP46'];z['m1_retention'][0]['retention_chart']='K46_PAIR';z['coded_port_repair']['new_payload_hex']=hex(payload);z['coded_port_repair']['retention_chart']='K46_PAIR'
 z['three_row_clique_code']={'common_codes':[[29,42],[41,43,46],[45,48]],'target_triple':[41,43,46],'triple_is_pairwise_orthogonal':True,'actual_payload_source':'CAP46 now captures raw43+raw46 at C2=M1','higher_payload_retention':'ZKEEP2 at K46_PAIR=span(L41,L43)','actual_common_P3_hex':z['seed_rows_hex'][3],'raw43_is_local_not_common':True,'removed_owned_movement':['MOVE','RAW43_COMMON','zero'],'original_X41_route_unchanged':True,'source_corrections':{'X43':['J41_PAIR','C2'],'X46':['Jnew43','J43_PAIR','C2']},'receiver_paths':{'Y41':['Jnew43','J41_PAIR','F41'],'Y43':['L41','J43_PAIR','F43'],'Y46':['L43','K46_PAIR','F46']}}
 z['affine_scope']='Actual39-output clique-code source: all prior endpoints preserved; true three common rows plus higher retained payload and chronological raw corrections remove raw43 ground grant. No complete111 supplier or newkappa.'
 return z

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=json.loads(raw);root=a.repo/'research/moonshot-005-program/results';e=load(root/'bit-composed-coded-source/author/retained/source_history_engine.py','e');src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];z=build(w,R);S=[int(x,16)for x in z['seed_rows_hex']];run=e.replay(z,R,S,15,False);old=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];mask=(1<<111)-1;rank=lambda rr:len(e.basis(rr));ground=[r for n,r in v.items()if at[n]=='zero'and not(r&~mask)];ov=old['cuts']['seed']['values'];oa=old['cuts']['seed']['charts'];oldground=[r for n,r in ov.items()if oa[n]=='zero'and not(r&~mask)]
 assert len(C['K46_PAIR'])==2 and len(C['J41_PAIR'])==3 and len(C['J43_PAIR'])==3
 assert e.contained(C['K46_PAIR'],C['F46'])and e.contained(C['J41_PAIR'],C['F41'])and e.contained(C['J43_PAIR'],C['F43'])
 assert v['CAP46']==v['ZKEEP2']==(1<<43)^(1<<46);assert at['ZKEEP2']=='K46_PAIR';assert v['PAIR_RAW43']==v['RAW43_LOCAL']==1<<43;assert v['PAIR_RAW46']==v['ZCORR43']==1<<46;assert at['RAW43_LOCAL']=='L43' and at['ZCORR43']=='Jnew43';assert 'RAW43_COMMON'not in v
 assert [o for o in z['operations']if o[:2]==['MOVE','X41']]==[o for o in w['operations']if o[:2]==['MOVE','X41']]
 expected=old['profile'].copy()
 for d,c in {1:4,2:5,3:1,4:-1,5:1,6:-2,7:-1}.items():expected[d]+=c
 assert run['profile']==expected,(run['profile'],expected)
 controls=[]
 for op in [['ADD','X43','CAP46'],['MOVE','X43','J41_PAIR'],['ADD','X43','PAIR_RAW43'],['MOVE','X46','J43_PAIR'],['ADD','X46','PAIR_RAW46'],['MOVE','P3','K46_PAIR'],['ADD','P3','ZKEEP2'],['ADD','PAIR_RAW43','Y41'],['MOVE','Y41','J41_PAIR'],['ADD','RAW41','Y43'],['ADD','PAIR_RAW46','Y43'],['MOVE','Y43','J43_PAIR'],['ADD','RAW43_LOCAL','Y46'],['ADD','ZKEEP2','Y46'],['MOVE','Y46','K46_PAIR'],['CLEAR','PAIR_RAW46']]:
  q=copy.deepcopy(z);q['operations'].remove(op);q['milestones']={k:-1 for k in q['milestones']};q.pop('source_cut',None)
  try:e.replay(q,R,S,15,False)
  except AssertionError as ex:controls.append({'removed':op,'rejected':str(ex)})
  else:raise AssertionError(('accepted semantic mutant',op))
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(z,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw);out={'status':'PASS_ACTUAL_THREE_ROW_CLIQUE39','word_sha256':hashlib.sha256(raw).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':z['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'common_rank':rank(ground),'predecessor_common_rank':rank(oldground),'raw43_not_common':e.solve(ground,1<<43)is None,'common_code_supports':[[29,42],[41,43,46],[45,48]],'exact_movement_increment_from39':'4[1]+5[2]+[3]-[4]+[5]-2[6]-[7]','all_old39_targets_preserved':True,'original_X41_route_unchanged':True,'new_chart_dimensions':{n:len(C[n])for n in ['K46_PAIR','J41_PAIR','J43_PAIR']},'semantic_negative_controls':controls,'controls_disable_invoice_source_cut_and_milestones':True,'scope':'Physical realization of one three-receiver clique and two pairs by actual common codes plus retained proper-chart payload. All costs and source custody charged.39/111 partial endpoints; no newkappa.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');price=load(root/'bit-composed-coded-source/author/price.py','price');q=price.invoice(run['profile']);(a.out/'PRICE.json').write_text(json.dumps(q,indent=2)+'\n');print(out['status'],out['word_sha256'],run['count'],'commonrank',rank(ground),'Q',q['moment']['lower'],'room',q['limiting_room']['lower'])
if __name__=='__main__':main()
