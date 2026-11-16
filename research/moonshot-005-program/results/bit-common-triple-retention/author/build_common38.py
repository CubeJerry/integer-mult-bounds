"""Coupled common-code construction from two protected terminal channels."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load
BASE='af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474'

def build(w):
 z=copy.deepcopy(w);ops=[['INIT','RAW43_COMMON','L43'],['ADD','X43','RAW43_COMMON'],['MOVE','RAW43_COMMON','zero'],['INIT','RAW29','L29'],['ADD','X29','RAW29'],['INIT','RAW42','L42'],['ADD','X42','RAW42'],['INIT','CAP2942','M1']];mapping={};newcode=(1<<29)^(1<<42)
 for step,o in enumerate(w['operations'],1):
  if o[0]=='ADD'and o[2]=='Y43':pass
  elif o[0]=='MOVE'and o[1]=='Y43':
   if o[2]=='F43':ops.extend([['ADD','RAW43_COMMON','Y43'],o])
  elif 'ZKEEP43'in o:pass
  elif o==['ADD','X28','ZRAW28']:ops.extend([o,['MOVE','ZRAW28','zero']])
  elif o==['INIT','ZCORR43','Jnew43']:ops.extend([['INIT','ZCORR43','L46'],['ADD','X46','ZCORR43']])
  elif o in [['MOVE','X46','Jnew43'],['ADD','X46','ZCORR43']]:pass
  elif o in [['MOVE','X29','C2'],['MOVE','X42','C2']]:ops.extend([o,['ADD',o[1],'CAP2942']])
  elif o==['ADD','ZKEEP2','P3']:pass
  elif o in [['ADD','H6_1','P4'],['ADD','H6_3','P4']]:pass
  elif o==['ADD','Q2','P4']:ops.append(['ADD','CAP2942','P4'])
  elif o in [['MOVE','P4','L28'],['ADD','ZRAW28','P4']]:pass
  elif o[0]=='ADD'and o[1]=='P4'and o[2].startswith('Y'):ops.extend([['ADD','ZRAW28',o[2]],['ADD','E75',o[2]]])
  elif o==['MOVE','Y41','F41']:ops.extend([['MOVE','Y41','L46'],['ADD','ZCORR43','Y41'],o])
  elif o in [['MOVE','Y29','F29'],['MOVE','Y42','F42']]:
   target=o[1];other=42 if target=='Y29' else 29
   ops.extend([['ADD','P4',target],['ADD','E75',target],['MOVE',target,f'L{other}'],['ADD',f'RAW{other}',target],o])
  else:ops.append(o)
  mapping[step]=len(ops)
 ops.extend([['CLEAR',n]for n in ['RAW43_COMMON','RAW29','RAW42','CAP2942']]);z['operations']=ops;z['milestones']={k:mapping[v]for k,v in w['milestones'].items()};z['targets']=sorted(w['targets']+[29,42]);z['seed_rows_hex'][3]=hex((1<<41)^(1<<46)^(1<<6));z['seed_rows_hex'][4]=hex(newcode^(1<<75));z['base_word_sha256']=BASE
 z.get('source_cut',{}).pop('ZKEEP43',None)
 for name, chart in [('ZRAW28','zero'),('ZCORR43','L46')]:
  if name in z.get('source_cut',{}):z['source_cut'][name]['chart']=chart
 z['two_common_channels']={'P3':{'value_hex':z['seed_rows_hex'][3],'information':'X41+X46 with X6 mask','real_raw46_source':'CAP46','leaf_retention_still':'ZKEEP2=X46','old_decoder_replacement':['ZRAW0','E6']},'P4':{'value_hex':z['seed_rows_hex'][4],'information':'X29+X42 with X75 mask','actual_source':'CAP2942 at M1, reads X29/X42 on actual C2 visits','old_raw28_preserved_at_ground':'ZRAW28','old_reader_replacement':['ZRAW28','E75']},'raw43_paid_common_source':'RAW43_COMMON: native L43 birth/capture and owned unit descent','old_Y43_replaced_by_direct_common_decoder':True,'obsolete_ZKEEP43_removed':True,'ZCORR43_retargeted_to_actual_raw46_birth':'L46; serves Y41 instead of Y43','original_X46_route_shortened':'L46 to C2 directly; old Jnew43 no longer required','new_targets_over36':[29,42]}
 z['affine_scope']='Actual38 native outputs with two genuine common coded channels and fully paid raw28/raw43 protection; all prior36 endpoints preserved. No complete supplier or newkappa.'
 return z

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=json.loads(raw);root=a.repo/'research/moonshot-005-program/results';e=load(root/'bit-composed-coded-source/author/retained/source_history_engine.py','e');src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];z=build(w);S=[int(x,16)for x in z['seed_rows_hex']];run=e.replay(z,R,S,15,False);old=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);C=run['C'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];mask=(1<<111)-1;rank=lambda rr:len(e.basis(rr));ground=[r for n,r in v.items()if at[n]=='zero'and not(r&~mask)];ov=old['cuts']['seed']['values'];oa=old['cuts']['seed']['charts'];oldground=[r for n,r in ov.items()if oa[n]=='zero'and not(r&~mask)];assert e.contained(C['L42'],C['F29'])and e.contained(C['L29'],C['F42'])and e.contained(C['L46'],C['F41'])
 assert v['CAP2942']==(1<<29)^(1<<42);assert v['RAW43_COMMON']==1<<43 and at['RAW43_COMMON']=='zero';assert v['ZRAW28']==1<<28 and at['ZRAW28']=='zero';assert v['ZCORR43']==1<<46 and at['ZCORR43']=='L46';assert 'ZKEEP43'not in v
 assert v['P3']==(1<<41)^(1<<46)^(1<<6)and v['P4']==(1<<29)^(1<<42)^(1<<75)
 controls=[]
 for op in [['MOVE','RAW43_COMMON','zero'],['ADD','X43','RAW43_COMMON'],['MOVE','ZRAW28','zero'],['ADD','X29','CAP2942'],['ADD','X42','CAP2942'],['ADD','CAP2942','P4'],['ADD','RAW43_COMMON','Y43'],['ADD','RAW42','Y29'],['MOVE','Y29','L42'],['ADD','RAW29','Y42'],['MOVE','Y42','L29'],['ADD','ZCORR43','Y41'],['MOVE','Y41','L46'],['ADD','ZRAW28','Y2'],['ADD','E75','Y2'],['CLEAR','CAP2942']]:
  q=copy.deepcopy(z);q['operations'].remove(op);q['milestones']={k:-1 for k in q['milestones']};q.pop('source_cut',None)
  try:e.replay(q,R,S,15,False)
  except AssertionError as ex:controls.append({'removed':op,'rejected':str(ex)})
  else:raise AssertionError(('accepted semantic mutant',op))
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(z,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw);out={'status':'PASS_ACTUAL_TWO_COMMON_CODES38','word_sha256':hashlib.sha256(raw).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':z['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'common_rank':rank(ground),'predecessor36_common_rank':rank(oldground),'common_union_rank':rank(ground+oldground),'ground41_no_longer_granted_alone':e.solve(ground,1<<41)is None,'actual_common_code_rows':{'P3':hex(v['P3']),'P4':hex(v['P4'])},'all_old36_targets_preserved':True,'semantic_negative_controls':controls,'controls_disable_invoice_source_cut_and_milestones':True,'scope':'Exact two common coded channels with actual source acquisitions, all chronological decoder reads, original restoration and complete literal invoices.38/111 partial outputs; no newkappa.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');price=load(root/'bit-composed-coded-source/author/price.py','price');q=price.invoice(run['profile']);(a.out/'PRICE.json').write_text(json.dumps(q,indent=2)+'\n');print(out['status'],out['word_sha256'],run['count'],'commonrank',rank(ground),'Q',q['moment']['lower'],'room',q['limiting_room']['lower'])
if __name__=='__main__':main()
