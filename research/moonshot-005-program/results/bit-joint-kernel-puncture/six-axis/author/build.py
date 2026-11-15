#!/usr/bin/env python3
"""Compose two real line-retained cells with the frozen four-axis source."""
import argparse,copy,hashlib,json
from pathlib import Path
BASE_SHA='2b13e0b8d534b90b3284ac93a49b5c3d7e79a6cfe0591ac7a8a1889a29fb856b'

def build(base):
 w=copy.deepcopy(base);old=w['operations'];ops=[];extra=[]
 for op in old:
  ops.append(op)
  for q,i in [(2,1),(3,2)]:
   if op==['MOVE',f'P{q}',f'L{i}']:
    name=f'KEEP_P{q}_L{i}';ops.extend([['INIT',name,f'L{i}'],['ADD',f'P{q}',name],['ADD',name,f'P{q}']]);extra.append({'packet':f'P{q}','owner':name,'chart':f'L{i}','terminal_axis':i,'W_role':14 if q==2 else 22})
 assert len(extra)==2
 for q,i in [(2,1),(3,2)]:ops.extend([['ADD',f'P{q}',f'Y{i}'],['MOVE',f'Y{i}',f'F{i}']])
 val={f'X{i}':1<<i for i in range(111)};val.update({f'Y{i}':1<<(111+i) for i in range(111)});loc={f'X{i}':f'L{i}' for i in range(111)};loc.update({f'Y{i}':'zero' for i in range(111)});owners=set()
 for op in ops:
  if op[0]=='INIT':owners.add(op[1]);loc[op[1]]=op[2];val[op[1]]=0
  elif op[0]=='ADD':val[op[2]]^=val[op[1]]
  elif op[0]=='MOVE':loc[op[1]]=op[2]
  else:raise AssertionError(op)
 for e in extra:
  e['row_hex']=hex(val[e['owner']]);assert val[e['owner']]==int(w['W_rows_hex'][e['W_role']],16)^(1<<e['terminal_axis']);assert val[e['packet']]==1<<e['terminal_axis']
 w.update(schema='colored-six-axis-four-mixed-kernel-source-v1',operations=ops,closed=False,handoff=len(ops),expected={k:[loc[k],val[k]] for k in sorted(owners)},completed_targets=[0,1,2,5,6,7],additional_stationary_kernels=extra,terminal_W_roles=[None,None,None,None,30,38,59,66],new_complete_kappa=False)
 w['base_word_sha256']=BASE_SHA
 closed=copy.deepcopy(w);closed['closed']=True;closed['operations'] += [['CLEAR',k] for k in sorted(owners)] + [['MOVE',f'Y{i}',f'F{i}'] for i in range(111) if i not in w['completed_targets']]
 return w,closed

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();assert hashlib.sha256(a.source.read_bytes()).hexdigest()==BASE_SHA;a.out.mkdir(parents=True,exist_ok=True)
 for n,w in zip(['WORD','CLOSED-WORD'],build(json.loads(a.source.read_text()))):(a.out/(n+'.json')).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('BUILT_SIX_AXIS_FOUR_KERNEL_SOURCE')
if __name__=='__main__':main()
