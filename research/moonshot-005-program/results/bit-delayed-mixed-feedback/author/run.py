#!/usr/bin/env python3
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
import delayed as d

def kernel_receipt(word,W):
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};charts={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 witness=None
 for step,op in enumerate(word['operations']):
  if op==['ADD','P0','Y0']:
   witness={'operation_index':step,'chart':charts['P0'],'packet_row_hex':hex(vals['P0']),'receiver_row_hex':hex(vals['Y0'])}
  if op[0]=='INIT':vals[op[1]]=0;charts[op[1]]=op[2]
  elif op[0]=='ADD':vals[op[2]]^=vals[op[1]]
  elif op[0]=='MOVE':charts[op[1]]=op[2]
  elif op[0]=='CLEAR':del vals[op[1]];del charts[op[1]]
 assert witness and witness['packet_row_hex']==word['kernel_x_hex'] and witness['chart']==word['delayed_feedback_chart']
 k=int(word['kernel_x_hex'],16);T=[word['expected'][f'P{i}'][1]for i in range(8)];c=d.c.c
 roots=d.c.p.roots;normals=[roots[i]for i in range(4)];local=c.mask(j for j,r in enumerate(roots)if all(c.dot(r,n)==0 for n in normals))
 external=k&~local&~1
 assert external
 witness.update({'nonlocal_nonzero_non_x0_columns':[j for j in range(111)if external>>j&1],
  'terminal_rank':c.rank_f2(T),'terminal_plus_kernel_rank':c.rank_f2(T+[k]),
  'punctured_terminal_rank':c.rank_f2([x&~1 for x in T]),'punctured_terminal_plus_kernel_rank':c.rank_f2([x&~1 for x in T]+[k&~1])})
 return witness

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);repo=a.repo.resolve();roots,oldh,pins=d.configure(repo)
 spec=importlib.util.spec_from_file_location('_colored_author_runner',d.source_dir/'run.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
 result={'status':'PASS_DELAYED_CLASS_ZERO_MIXED_FEEDBACK','source_pins':pins,'receipts':{},'negative_controls':{},'new_complete_kappa':False}
 for closed in[False,True]:
  w,W=d.build(closed=closed);r=d.c.replay(w,W);r.pop('history');r['kernel']=kernel_receipt(w,W);name=('CLOSED-'if closed else'')+'WORD.json';(a.out/name).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n');result['receipts'][name]=r
  if not closed:(a.out/'HISTORY.json').write_text(json.dumps(runner.history_certificate(w,W),indent=2,sort_keys=True)+'\n')
 w,W=d.build(closed=False)
 mutations={'omit_delayed_prefix_correction':['ADD','C0_1_0','Y0'],'omit_suffix_preload':['ADD','C0_7_0','Y0'],'omit_feedback':['ADD','Y0','P0'],'omit_y_capture':['ADD','Y0','YM0'],'omit_y_unmask':['ADD','YM0','P0'],'omit_packet_source_prefix':['ADD','C0_1_1','P0']}
 for label,op in mutations.items():
  bad=copy.deepcopy(w);i=bad['operations'].index(op);del bad['operations'][i];bad['handoff']-=1
  try:d.c.replay(bad,W);kernel_receipt(bad,W)
  except(AssertionError,ValueError,KeyError)as e:result['negative_controls'][label]={'rejected':True,'reason':type(e).__name__+': '+str(e)}
  else:raise ValueError('Accepted mutant '+label)
 price=d.c.c.price(result['receipts']['CLOSED-WORD.json']['profile']);price['scope']='Closed one-output partial source; mixed kernel rank is an enabling property, not a complete decoder.'
 result['dependency_sha256']={str((d.source_dir/n).relative_to(repo)):hashlib.sha256((d.source_dir/n).read_bytes()).hexdigest()for n in['core.py','construct.py','run.py','PROOF.md','output/COUPLED-WORD.json']}
 result['author_source_sha256']={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest()for n in['delayed.py','run.py']}
 for n,v in[('RESULT.json',result),('PRICE.json',price)]: (a.out/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'counts':result['receipts']['CLOSED-WORD.json']['counts'],'kernel':result['receipts']['WORD.json']['kernel'],'moment':price['moment']['lower_decimal']}))
if __name__=='__main__':main()
