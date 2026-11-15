#!/usr/bin/env python3
"""Replace every conditional lane by a distinct, fully paid scalar owner."""
import argparse,json,hashlib
from pathlib import Path

def expand(w,sha):
 def bank(n,a):return f'{n}_b{a}'
 ops=[];boundaries=[];handoff=None
 for index,op in enumerate(w['operations']):
  kind,n,*a=op
  if kind=='ADD_LANE':ops.append(['ADD',bank(n,a[0]),bank(a[1],a[2])])
  elif kind=='ADD':ops.extend([['ADD',bank(n,b),bank(a[0],b)]for b in range(2)])
  elif kind in ['INIT','MOVE']:ops.extend([[kind,bank(n,b),a[0]]for b in range(2)])
  elif kind=='CLEAR':ops.extend([['CLEAR',bank(n,b)]for b in range(2)])
  else:raise ValueError(kind)
  boundaries.append(len(ops))
  if index+1==w['handoff']:handoff=len(ops)
 expected={bank(n,a):[c,rows[a]]for n,(c,rows)in w['expected'].items()for a in range(2)}
 return {'schema':'two-copy-packed-scalar-source-v1','physical_copies':2,'scalar_word_grammar':True,'single_wide_record_claim':False,
  'source_conditional_word_sha256':sha,'native_roots_sha256':w['native_roots_sha256'],'charts':w['charts'],'operations':ops,'expected':expected,'handoff':handoff,'closed':w['closed'],
  'completed_targets':[[i,b]for i in w['completed_targets']for b in range(2)],'W_rows_lanes_hex':w['W_rows_lanes_hex'],'h_coordinates':w['h_coordinates'],'W_pivot_h_hex':w['W_pivot_h_hex'],
  'physical_scope':'Every bank is a separate full ordinary record; native bodies, target jobs, caller constants and transport must all be counted twice.',
  'conditional_to_scalar_operation_boundaries':boundaries,'new_complete_kappa':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 for name in ['WORD','CLOSED-WORD']:
  raw=(a.source/(name+'.json')).read_bytes();w=expand(json.loads(raw),hashlib.sha256(raw).hexdigest());(a.out/(name+'.json')).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('EXPANDED_TWO_PAID_PHYSICAL_COPIES')
if __name__=='__main__':main()
