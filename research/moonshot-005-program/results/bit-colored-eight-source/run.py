#!/usr/bin/env python3
"""Emit four literal source words, exact history witnesses and rejecting controls."""
import argparse,copy,hashlib,json
from pathlib import Path
import construct as c

def history_certificate(word,W):
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 charts={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 B={};selected=[]
 for step,o in enumerate(word['operations']):
  if o[0]=='INIT':vals[o[1]]=0;charts[o[1]]=o[2]
  elif o[0]=='ADD':vals[o[2]]^=vals[o[1]]
  elif o[0]=='MOVE':charts[o[1]]=o[2]
  elif o[0]=='CLEAR':del vals[o[1]];del charts[o[1]]
  for q in range(8):
   n=f'P{q}'
   if n not in vals or charts[n]=='Hub':continue
   original=vals[n];row=original;expression=1<<len(selected)
   while row:
    key=row.bit_length()-1
    if key in B:v,e=B[key];row^=v;expression^=e
    else:
     B[key]=(row,expression);selected.append({'packet':n,'operation_index':step,'chart':charts[n],'row_hex':hex(original)});break
 witnesses=[]
 for i,original in enumerate(W):
  row=original;expression=0
  while row:
   key=row.bit_length()-1
   if key not in B:raise ValueError('Missing W fitting row')
   v,e=B[key];row^=v;expression^=e
  actual=0
  for j,s in enumerate(selected):
   if expression>>j&1:actual^=int(s['row_hex'],16)
  assert actual==original
  witnesses.append({'role':i,'W_row_hex':hex(original),'selected_history_coefficients_hex':hex(expression)})
 return {'status':'PASS_LITERAL_ALL111_W_HISTORY_RELATIONS','all_input_columns':222,'history_rank':len(selected),'history_basis':selected,'W_rows':witnesses,'scope':'Binary identities hold over every characteristic-two field and tensor with every positive whole-record width; no free historical access is granted.'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=parser.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 repo=a.repo.resolve();roots,oldh,pins=c.configure(repo)
 result={'status':'PASS_COLORED_EIGHT_QUERY_W15_SOURCE','source_pins':pins,'receipts':{},'negative_controls':{},'new_complete_kappa':False}
 for coupled in[False,True]:
  for closed in[False,True]:
   word,W=c.build_coloured(coupled=coupled,closed=closed);receipt=c.replay(word,W);receipt.pop('history')
   receipt['all_original_input_columns']=222;receipt['completed_targets']=word['completed_targets'];receipt['rank_length']=sum(k*v for k,v in receipt['profile'].items())
   prefix=('COUPLED-'if coupled else'UNCOUPLED-')+('CLOSED-'if closed else'');name=prefix+'WORD.json'
   (a.out/name).write_text(json.dumps(word,indent=2,sort_keys=True)+'\n');result['receipts'][name]=receipt
   if not closed:(a.out/(prefix+'HISTORY.json')).write_text(json.dumps(history_certificate(word,W),indent=2,sort_keys=True)+'\n')
 base,W=c.build_coloured(coupled=True,closed=False)
 mutations={'omit_y_capture':['ADD','Y0','YM0'],'omit_y_feedback':['ADD','Y0','P0'],'omit_y_unmask':['ADD','YM0','P0'],
   'omit_y_preload':['ADD','C0_7_0','Y0'],'omit_class_zero_read':['ADD','C0_1_0','P0'],'omit_class_one_read':['ADD','C0_1_1','P0'],
   'omit_free_terminal_seed':next(op for op in base['operations']if op[0]=='ADD'and op[-1]=='P7'and op[1].startswith('X'))}
 for label,op in mutations.items():
  bad=copy.deepcopy(base);i=bad['operations'].index(op);del bad['operations'][i];bad['handoff']-=1
  try:c.replay(bad,W)
  except(AssertionError,ValueError,KeyError)as e:result['negative_controls'][label]={'rejected':True,'reason':type(e).__name__+': '+str(e)}
  else:raise ValueError('Accepted mutant '+label)
 q=result['receipts']['COUPLED-CLOSED-WORD.json']['profile'];assert q=={1:183,2:12,3:119,4:71,7:110}
 price=c.c.price(q);price['scope']='Full closed one-output partial invoice, including all110 other Y ascents. No complete supplier or new kappa.'
 deps=repo/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a'
 result['dependency_sha256']={str((deps/n).relative_to(repo)):hashlib.sha256((deps/n).read_bytes()).hexdigest()for n in['shared_facet_source.py','full_singular_history.py','eight_packet_source.py','price.py','triple_source.py','coupled_two_receiver.py']}
 result['author_source_sha256']={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest()for n in['core.py','construct.py','run.py']}
 for name,value in[('RESULT.json',result),('PRICE.json',price)]: (a.out/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
 r=result['receipts']['COUPLED-CLOSED-WORD.json'];print(json.dumps({'status':result['status'],'profile':q,'counts':r['counts'],'history_W':r['history_W'],'history_rank':r['history_rank'],'terminal_W':r['terminal_W_intersection'],'moment':price['moment']['lower_decimal'],'room':price['limiting_room']['lower_decimal']}))
if __name__=='__main__':main()
